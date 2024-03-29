from __future__ import annotations

import abc
import asyncio
import dataclasses
import inspect
from dataclasses import dataclass
from datetime import datetime
from inspect import Parameter, isclass
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    AsyncIterable,
    AsyncIterator,
    Callable,
    Collection,
    Dict,
    Generator,
    Generic,
    Iterable,
    Iterator,
    List,
    Literal,
    Optional,
    Protocol,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

import pyarrow
from typing_extensions import ParamSpec, TypeAlias, get_args, get_origin

from chalk._lsp.error_builder import ResolverErrorBuilder, get_resolver_error_builder
from chalk.features.dataframe import DataFrame, DataFrameMeta
from chalk.features.feature_field import Feature
from chalk.features.feature_set import Features, is_feature_set_class
from chalk.features.feature_wrapper import FeatureWrapper, unwrap_feature
from chalk.features.filter import Filter
from chalk.features.live_updates import register_live_updates_if_in_notebook
from chalk.features.namespace_context import build_namespaced_name
from chalk.features.pseudofeatures import PSEUDONAMESPACE
from chalk.features.tag import Environments, Tags
from chalk.features.underscore import Underscore
from chalk.sink import SinkIntegrationProtocol
from chalk.state import StateWrapper
from chalk.streams import StreamSource, get_name_with_duration
from chalk.streams.types import (
    StreamResolverParam,
    StreamResolverParamKeyedState,
    StreamResolverParamMessage,
    StreamResolverParamMessageWindow,
    StreamResolverSignature,
)
from chalk.utils import MachineType, notebook
from chalk.utils.annotation_parsing import ResolverAnnotationParser
from chalk.utils.cached_type_hints import cached_get_type_hints
from chalk.utils.collections import ensure_tuple
from chalk.utils.duration import CronTab, Duration, parse_chalk_duration
from chalk.utils.log_with_context import get_logger
from chalk.utils.pydanticutil.pydantic_compat import is_pydantic_basemodel

try:
    from types import UnionType
except ImportError:
    UnionType = Union

if TYPE_CHECKING:
    from pydantic import BaseModel

    from chalk.sql import BaseSQLSourceProtocol
    from chalk.sql._internal.sql_source import BaseSQLSource
else:
    try:
        from pydantic.v1 import BaseModel
    except ImportError:
        from pydantic import BaseModel

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
P = ParamSpec("P")
V = TypeVar("V")

ResolverHook: TypeAlias = "Callable[[Resolver], None] | None"

_logger = get_logger(__name__)


@dataclasses.dataclass(frozen=True)
class ResolverArgErrorHandler:
    default_value: Any


@dataclass
class StateDescriptor(Generic[T]):
    kwarg: str
    pos: int
    initial: T
    typ: Type[T]


class Cron:
    """
    Detailed options for specify the schedule and filtering
    functions for Chalk batch jobs.
    """

    def __init__(
        self,
        schedule: CronTab | Duration,
        filter: Callable[..., bool] | None = None,
        sample: Callable[[], DataFrame] | None = None,
    ):
        """Run an online or offline resolver on a schedule.

        This class lets you add a filter or sample function
        to your cron schedule for a resolver. See the
        overloaded signatures for more information.

        Parameters
        ----------
        schedule
            The period of the cron job. Can be either a crontab (`"0 * * * *"`)
            or a `Duration` (`"2h"`).
        filter
            Optionally, a function to filter down the arguments to consider.

            See https://docs.chalk.ai/docs/resolver-cron#filtering-examples for more information.
        sample
            Explicitly provide the sample function for the cron job.

            See https://docs.chalk.ai/docs/resolver-cron#custom-examples for more information.


        Examples
        --------
        Using a filter

        >>> def fltr(v: Account.active):
        ...     return v
        >>> @online(cron=Cron(schedule="1d", filter=fltr))
        ... def fn(balance: Account.balance) -> ...:

        Using a sample function

        >>> def s() -> DataFrame[User.id]:
        ...     return DataFrame.read_csv(...)
        >>> @offline(cron=Cron(schedule="1d", sample=s))
        ... def fn(balance: User.account.balance) -> ...:
        """
        super().__init__()
        self.schedule = schedule
        self.filter = filter
        self.sample = sample
        self.trigger_downstream = False


def _flatten_features(output: Optional[Type[Features]]) -> Sequence[Feature]:
    if output is None:
        return []
    features = output.features
    if len(features) == 1 and isinstance(features[0], type) and issubclass(features[0], DataFrame):
        return features[0].columns
    return features


class ResolverProtocol(Protocol[P, T_co]):
    """A resolver, returned from the decorators `@offline` and `@online`."""

    function_definition: str
    """The content of the resolver as a string."""

    owner: str | None
    """ Individual or team responsible for this resolver.
    The Chalk Dashboard will display this field, and alerts
    can be routed to owners.
    """

    environment: list[str] | None
    """
    Environments are used to trigger behavior
    in different deployments such as staging, production, and
    local development. For example, you may wish to interact with
        a vendor via an API call in the production environment, and
        opt to return a constant value in a staging environment.

        Environment can take one of three types:
        - `None` (default) - candidate to run in every environment
        - `str` - run only in this environment
        - `list[str]` - run in any of the specified environment and no others

    Read more at https://docs.chalk.ai/docs/resolver-environments
    """

    tags: list[str] | None
    """
    Allow you to scope requests within an
    environment. Both tags and environment need to match for a
    resolver to be a candidate to execute.

    You might consider using tags, for example, to change out
    whether you want to use a sandbox environment for a vendor,
    or to bypass the vendor and return constant values in a
    staging environment.

    Read more at https://docs.chalk.ai/docs/resolver-tags
    """

    __doc__: Optional[str]
    """The docstring of the resolver."""

    __name__: str
    """The function name of the resolver."""

    __module__: str
    """The python module where the function is defined"""

    __annotations__: dict[str, Any]
    """The type annotations for the resolver"""

    filename: str
    """The filename in which the resolver is defined."""

    name: str
    """The name of the resolver, either given by the name of the function,
    or by the keyword argument `name` given to `@offline` or `@online`.
    """

    fqn: str
    """The fully qualified name for the resolver"""

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T_co:
        """Returns the result of calling the function decorated
        with `@offline` or `@online` with the given arguments.

        Parameters
        ----------
        args
            The arguments to pass to the decorated function.
            If one of the arguments is a `DataFrame` with a
            filter or projection applied, the resolver will
            only be called with the filtered or projected
            data. Read more at
            https://docs.chalk.ai/docs/unit-tests#data-frame-inputs

        Returns
        -------
        T
            The result of calling the decorated function
            with `args`. Useful for unit-testing.

            Read more at https://docs.chalk.ai/docs/unit-tests

        Examples
        --------
        >>> @online
        ... def get_num_bedrooms(
        ...     rooms: Home.rooms[Room.name == 'bedroom']
        ... ) -> Home.num_bedrooms:
        ...     return len(rooms)
        >>> rooms = [
        ...     Room(id=1, name="bedroom"),
        ...     Room(id=2, name="kitchen"),
        ...     Room(id=3, name="bedroom"),
        ... ]
        >>> assert get_num_bedrooms(rooms) == 2
        """
        ...


class ResolverRegistry:
    def __init__(self):
        super().__init__()
        self._online_and_offline_resolvers: set[OnlineResolver | OfflineResolver] = set()
        self._stream_resolvers: set[StreamResolver] = set()
        self._sink_resolvers: set[SinkResolver] = set()
        self._short_name_to_resolver: dict[str, Resolver] = {}
        self._deferred_resolvers: list[tuple[Callable[[], Resolver], bool]] = []
        self.hook: Callable[[Resolver], None] | None = None

    def get_online_and_offline_resolvers(self) -> Collection[OnlineResolver | OfflineResolver]:
        self._load_deferred_resolvers()
        return self._online_and_offline_resolvers

    def get_stream_resolvers(self) -> Collection[StreamResolver]:
        self._load_deferred_resolvers()
        return self._stream_resolvers

    def get_sink_resolvers(self) -> Collection[SinkResolver]:
        self._load_deferred_resolvers()
        return self._sink_resolvers

    def _load_deferred_resolvers(self):
        while len(self._deferred_resolvers) > 0:
            deferred_resolver, override = self._deferred_resolvers.pop()
            # Not overriding because deferred resolvers only exist
            self.add_to_registry(deferred_resolver(), override=override)

    def add_to_deferred_registry(self, deferred_resolver: Callable[[], Resolver], *, override: bool):
        self._deferred_resolvers.append((deferred_resolver, override))

    def get_resolver(self, name: str):
        self._load_deferred_resolvers()
        short_name = name.split(".")[-1]
        return self._short_name_to_resolver.get(short_name)

    def get_all_resolvers(self) -> Collection[Resolver]:
        self._load_deferred_resolvers()
        return self._short_name_to_resolver.values()

    def remove_resolver(self, resolver_name: str):
        if self.hook:
            raise RuntimeError(
                "Cannot remove resolvers if there is a hook defined, as the hook does not provide an interface to unregister a resolver."
            )
        existing_resolver = self._short_name_to_resolver.get(resolver_name)
        if existing_resolver is None:
            # Resolver not in the registry
            return
        if isinstance(existing_resolver, (OnlineResolver, OfflineResolver)):
            self._online_and_offline_resolvers.discard(existing_resolver)
        if isinstance(existing_resolver, StreamResolver):
            self._stream_resolvers.discard(existing_resolver)
        if isinstance(existing_resolver, SinkResolver):
            self._sink_resolvers.discard(existing_resolver)

    def add_to_registry(self, resolver: Resolver, *, override: bool):
        """
        Adds the given resolver to the registry.
        If in a notebook or if override is True, first removes any existing resolvers
        with the same short-name.
        """
        short_name = resolver.name
        if short_name in self._short_name_to_resolver:
            if not override and not notebook.is_notebook():
                if resolver.fqn == self._short_name_to_resolver[short_name]:
                    # Same resolver was redefined
                    resolver.lsp_builder.add_diagnostic(
                        message=f"Duplicate resolver '{resolver.fqn}'. Multiple resolvers cannot have the same name.",
                        code="71",
                        label="duplicate name",
                        range=resolver.lsp_builder.function_name(),
                        raise_error=ValueError,
                    )
                else:
                    # Same short name was reused
                    resolver.lsp_builder.add_diagnostic(
                        message=(
                            f"Another resolver with the same function name '{resolver.name}' in module "
                            f"'{self._short_name_to_resolver[short_name].__module__}' exists. "
                            f"Resolver function names must be unique. Please rename this resolver in module '{resolver.__module__}'."
                        ),
                        label="duplicate resolver shortname",
                        code="71",
                        range=resolver.lsp_builder.function_name(),
                        raise_error=ValueError,
                    )
                return
            existing_resolver = self._short_name_to_resolver[short_name]
            # Need to remove the resolver from the typed registry
            # Using discard instead of pop to be graceful if the resolver is not in there for some reason (would likely involve some exception being raised when registering the resolver)
            if isinstance(existing_resolver, (OnlineResolver, OfflineResolver)):
                self._online_and_offline_resolvers.discard(existing_resolver)
            if isinstance(existing_resolver, StreamResolver):
                self._stream_resolvers.discard(existing_resolver)
            if isinstance(existing_resolver, SinkResolver):
                self._sink_resolvers.discard(existing_resolver)
        self._short_name_to_resolver[short_name] = resolver
        if isinstance(resolver, (OnlineResolver, OfflineResolver)):
            self._online_and_offline_resolvers.add(resolver)
        if isinstance(resolver, StreamResolver):
            self._stream_resolvers.add(resolver)
        if isinstance(resolver, SinkResolver):
            self._sink_resolvers.add(resolver)
        if self.hook:
            self.hook(resolver)


RESOLVER_REGISTRY = ResolverRegistry()


# Turn the ResolverRegistry class into a sing
def _prevent_duplicate_construction(*args: Any, **kwargs: Any):
    raise RuntimeError(
        "The ResolverRegistry class is a singleton. Please use chalk.features.resolver.RESOLVER_REGISTRY"
    )


ResolverRegistry.__new__ = _prevent_duplicate_construction


class Resolver(ResolverProtocol[P, T], abc.ABC):
    def __init__(
        self,
        function_definition: str,
        fqn: str,
        filename: str,
        doc: str | None,
        inputs: Sequence[Feature | type[DataFrame]],
        output: Type[Features] | None,
        fn: Callable[P, T],
        environment: list[str] | None,
        tags: list[str] | None,
        cron: CronTab | Duration | Cron | None,
        machine_type: MachineType | None,
        when: Filter | None,
        state: StateDescriptor | None,
        default_args: list[ResolverArgErrorHandler | None],
        owner: str | None,
        timeout: Duration | None,
        is_sql_file_resolver: bool,
        source_line: int | None,
        data_sources: list[BaseSQLSource] | None,
        lsp_builder: ResolverErrorBuilder,
        underscore: Underscore | None,
        name: None = None,  # deprecated
    ):
        self.function_definition = function_definition
        self.fqn = fqn
        self.filename = filename
        self.inputs = inputs
        self.output = output
        self.fn = fn
        self.__name__ = self.fn.__name__
        self.__module__ = fn.__module__
        self.__doc__ = fn.__doc__
        self.__annotations__ = fn.__annotations__
        self.environment = environment
        self.tags = tags
        self.max_staleness = None
        self.cron = cron
        self.doc = doc
        self.machine_type = machine_type
        self.when = when
        self.state = state
        self.default_args = default_args
        self.owner = owner
        if isinstance(timeout, str):
            timeout = parse_chalk_duration(timeout)
        self.timeout = timeout
        self.is_sql_file_resolver = is_sql_file_resolver
        self.source_line = source_line
        self.data_sources = data_sources
        self.lsp_builder = lsp_builder
        self.underscore = underscore
        self.is_cell_magic = False
        self.name = fqn.split(".")[-1]
        super().__init__()

    def _process_call(self, *args: P.args, **kwargs: P.kwargs) -> T:
        # __call__ is defined to support userland code that invokes a resolver
        # as if it is a normal python function
        # If the user returns a ChalkQuery, then we'll want to automatically execute it
        from chalk.sql import FinalizedChalkQuery
        from chalk.sql._internal.chalk_query import ChalkQuery
        from chalk.sql._internal.string_chalk_query import StringChalkQuery

        result = self.fn(*args, **kwargs)

        if isinstance(result, (ChalkQuery, StringChalkQuery)):
            result = result.all()
        if isinstance(result, FinalizedChalkQuery):
            result = result.execute(_flatten_features(self.output))
        return result

    async def _process_async_call(self, *args: P.args, **kwargs: P.kwargs):
        # __call__ is defined to support userland code that invokes a resolver
        # as if it is a normal python function
        # If the user returns a ChalkQuery, then we'll want to automatically execute it
        from chalk.sql import FinalizedChalkQuery
        from chalk.sql._internal.chalk_query import ChalkQuery
        from chalk.sql._internal.string_chalk_query import StringChalkQuery

        assert asyncio.iscoroutinefunction(self.fn)

        result = await self.fn(*args, **kwargs)

        if isinstance(result, (ChalkQuery, StringChalkQuery)):
            result = result.all()
        if isinstance(result, FinalizedChalkQuery):
            result = await result.async_execute(_flatten_features(self.output))
        return result

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        bound = inspect.signature(self.fn).bind(*args, **kwargs)
        updated_args = []
        inputs = self.inputs
        if self.state is not None:
            inputs = (*self.inputs[: self.state.pos], None, *inputs[self.state.pos :])
        for i, (val, input_) in enumerate(zip(bound.args, inputs)):
            if isinstance(input_, type) and issubclass(
                input_, DataFrame
            ):  # pyright: ignore[reportUnnecessaryIsInstance]
                annotation = input_
            elif input_ is not None and input_.is_has_many:
                annotation = input_.typ.as_dataframe()
                assert annotation is not None, f"Expected DataFrame, found {annotation}"
            else:
                annotation = None

            if annotation is not None:
                if not isinstance(val, DataFrame):
                    val = DataFrame(val)

                if annotation.filters and len(annotation.filters) > 0:
                    try:
                        val = val[annotation.filters]
                        assert isinstance(val, DataFrame)
                        val._materialize()  # pyright: ignore[reportPrivateUsage]
                    except:
                        kwarg_name = list(bound.signature.parameters)[i]
                        _logger.warn(
                            (
                                f"The resolver '{self.fqn}' takes a DataFrame as '{kwarg_name}', but the provided "
                                "input is missing columns on which it filters."
                            )
                        )

                updated_args.append(val)
            else:
                updated_args.append(val)
        if asyncio.iscoroutinefunction(self.fn):
            # Not awaiting this coroutine here -- when the caller awaits it,
            # it will run
            return cast(T, self._process_async_call(*updated_args))
        else:
            return self._process_call(*updated_args)

    def add_to_registry(self, *, override: bool):
        """
        Shorthand for RESOLVER_REGISTRY.add_to_registry()
        """
        RESOLVER_REGISTRY.add_to_registry(self, override=override)


register_live_updates_if_in_notebook(RESOLVER_REGISTRY)


class SinkResolver(Resolver[P, T]):
    def __init__(
        self,
        function_definition: str,
        fqn: str,
        filename: str,
        doc: str | None,
        inputs: list[Feature],
        fn: Callable[P, T],
        environment: Optional[list[str]],
        tags: Optional[list[str]],
        machine_type: Optional[MachineType],
        buffer_size: int | None,
        debounce: Duration | None,
        max_delay: Duration | None,
        upsert: bool,
        owner: str | None,
        input_is_df: bool,
        default_args: list[ResolverArgErrorHandler | None],
        integration: Optional[Union[BaseSQLSourceProtocol, SinkIntegrationProtocol]],
        source_line: int | None,
        data_sources: Optional[list[BaseSQLSource]],
        lsp_builder: ResolverErrorBuilder,
    ):
        super().__init__(
            function_definition=function_definition,
            lsp_builder=lsp_builder,
            filename=filename,
            environment=environment,
            machine_type=machine_type,
            fqn=fqn,
            fn=fn,
            doc=doc,
            inputs=inputs,
            output=None,
            tags=tags,
            cron=None,
            when=None,
            state=None,
            default_args=default_args,
            owner=owner,
            source_line=source_line,
            timeout=None,
            is_sql_file_resolver=False,
            data_sources=data_sources,
            underscore=None,
        )
        self.buffer_size = buffer_size
        if isinstance(debounce, str):
            debounce = parse_chalk_duration(debounce)
        self.debounce = debounce
        if isinstance(max_delay, str):
            max_delay = parse_chalk_duration(max_delay)
        self.max_delay = max_delay
        self.upsert = upsert
        self.integration = integration
        self.input_is_df = input_is_df

    def __repr__(self):
        return f"SinkResolver(name={self.fqn})"


class OnlineResolver(Resolver[P, T]):
    def __repr__(self):
        return f"OnlineResolver(name={self.fqn})"


class OfflineResolver(Resolver[P, T]):
    def __repr__(self):
        return f"OfflineResolver(name={self.fqn})"


@dataclasses.dataclass(frozen=True)
class ResolverParseResult(Generic[P, T]):
    fqn: str
    inputs: list[Feature]
    state: Optional[StateDescriptor]
    output: Optional[Type[Features]]
    function: Callable[P, T]
    function_definition: str
    doc: Optional[str]
    default_args: list[Optional[ResolverArgErrorHandler]]


@dataclasses.dataclass(frozen=True)
class SinkResolverParseResult(Generic[P, T]):
    fqn: str
    input_features: list[Feature]
    input_is_df: bool
    function: Callable[P, T]
    function_definition: str
    doc: Optional[str]
    input_feature_defaults: list[Optional[ResolverArgErrorHandler]]


def get_resolver_fqn(function: Callable, name: str | None = None):
    name = function.__name__ if name is None else name
    # We need to prepend the namespace onto the short name, since that is what we ensure uniqueness on
    name = build_namespaced_name(name=name)
    if notebook.is_notebook() and not notebook.is_defined_in_module(function):
        return name
    return f"{function.__module__}.{name}"


def get_state_default_value(
    state_typ: type,
    declared_default: Any,
    parameter_name_for_errors: str,
    resolver_fqn_for_errors: str,
    error_builder: ResolverErrorBuilder,
) -> Any:
    if not is_pydantic_basemodel(state_typ) and not dataclasses.is_dataclass(state_typ):
        error_builder.add_diagnostic(
            message=(
                f"State value must be a pydantic model or dataclass, "
                f"but argument '{parameter_name_for_errors}' has type '{type(state_typ).__name__}'"
            ),
            code="117",
            label="invalid state type",
            range=error_builder.function_arg_annotation_by_name(parameter_name_for_errors),
            raise_error=ValueError,
        )

    default = declared_default
    if default is inspect.Signature.empty:
        try:
            default = state_typ()
        except Exception as e:
            cls_name = state_typ.__name__
            error_builder.add_diagnostic(
                message=(
                    "State parameter must have a default value, or be able to be instantiated "
                    f"with no arguments. For resolver '{resolver_fqn_for_errors}', no default found, and default "
                    f"construction failed with '{str(e)}'. Assign a default in the resolver's "
                    f"signature ({parameter_name_for_errors}: {cls_name} = {cls_name}(...)), or assign a default"
                    f" to each of the fields of '{cls_name}'."
                ),
                code="118",
                label="state value must have a default",
                range=error_builder.function_arg_annotation_by_name(parameter_name_for_errors),
                raise_error=ValueError,
            )

    if not isinstance(default, cast(Type, state_typ)):
        error_builder.add_diagnostic(
            message=(
                f"Expected type '{state_typ.__name__}' for '{parameter_name_for_errors}', "
                f"but default '{default}' does not match."
            ),
            code="119",
            label="invalid default state",
            range=error_builder.function_arg_value_by_name(parameter_name_for_errors),
            raise_error=ValueError,
        )

    return default


def _explode_features(ret_val: Type[Features], inputs: list[Feature]) -> Type[Features]:
    new_features = []
    if getattr(ret_val, "__is_exploded__", False):
        # already exploded by Features[]. Take out inputs and return
        return Features[[feature for feature in ret_val.features if feature not in inputs]]
    if is_feature_set_class(ret_val):
        # Is a root namespace feature class. Return only scalars.
        return Features[
            [
                f
                for f in ret_val.features
                if not f.is_autogenerated
                and not f.is_windowed
                and not f.is_has_many
                and not f.is_has_one
                and f not in inputs
            ]
        ]
    flattened_features = [f for f in _flatten_features(ret_val) if not f.is_autogenerated]
    # These features should be exploded

    is_dataframe = (
        len(ret_val.features) == 1
        and isinstance(ret_val.features[0], type)
        and issubclass(ret_val.features[0], DataFrame)
    )

    for f in flattened_features:
        if f.is_windowed:
            for d in f.window_durations:
                windowed_name = get_name_with_duration(name_or_fqn=f.name, duration=d)
                windowed_feature = getattr(f.features_cls, windowed_name)
                new_features.append(unwrap_feature(windowed_feature))
        elif f.is_has_many and is_dataframe:
            dataframe_typ = f.typ.as_dataframe()
            assert dataframe_typ is not None
            new_features.extend(
                [
                    col
                    for col in dataframe_typ.columns
                    if not col.is_autogenerated and not col.is_windowed and not col.is_has_many and not col.is_has_one
                ]
            )
        elif f.is_has_one:
            assert f.joined_class is not None
            new_features.extend(
                [
                    f.copy_with_path(x)
                    for x in f.joined_class.features
                    if not x.is_autogenerated and not x.is_windowed and not x.is_has_many and not x.is_has_one
                ]
            )
        elif not f.is_autogenerated:
            new_features.append(f)

    if is_dataframe:
        return Features[DataFrame[new_features]]

    return Features[new_features]


def parse_function(
    fn: Callable[P, T],
    glbs: Optional[Dict[str, Any]],
    lcls: Optional[Dict[str, Any]],
    error_builder: ResolverErrorBuilder,
    ignore_return: bool = False,
    allow_custom_args: bool = False,
    is_streaming_resolver: bool = False,
    name: str | None = None,
) -> ResolverParseResult[P, T]:
    fqn = get_resolver_fqn(function=fn, name=name)
    short_name = fqn.split(".")[-1]
    sig = inspect.signature(fn)

    function_source = inspect.getsource(fn)

    return_annotation = cached_get_type_hints(fn).get("return")

    annotation_parser = ResolverAnnotationParser(fn, glbs, lcls, error_builder)

    if return_annotation is None and not ignore_return:
        error_builder.add_diagnostic(
            message=f"Resolver '{short_name}' must have a return annotation.",
            code="81",
            label="resolver lacks a return annotation",
            range=error_builder.function_return_annotation(),
            raise_error=TypeError,
            code_href="https://docs.chalk.ai/docs/resolver-outputs",
        )

    ret_val = None

    origin = get_origin(return_annotation)

    if isinstance(origin, type) and issubclass(origin, (Iterable, Iterator, AsyncIterable, AsyncIterator)):
        # If it's iterable, then it might be a generator
        args = get_args(return_annotation)
        if len(args) != 1:
            error_builder.add_diagnostic(
                message=(
                    f"Resolver '{short_name}' has a return annotation '{return_annotation}' which does not specify any features. "
                    f"Please include features inside the type signature -- for example, `{origin.__name__}[Features[MyFeatureSet.id, MyFeatureSet.feature_2]]`"
                ),
                code="100",
                label="resolver return does not include features",
                range=error_builder.function_return_annotation(),
                raise_error=TypeError,
            )

        return_annotation = get_args(return_annotation)[0]
        if not (isinstance(return_annotation, type) and issubclass(return_annotation, DataFrame)):
            # If a function is annotated to return an iterable, treat it as a DF resolver. This is because generators can yield more than one row
            # Treat scalar-returning generator resolvers as DF-returning, as they could yield more than one row
            return_annotation = DataFrame[return_annotation]
        origin = get_origin(return_annotation)

    if isinstance(origin, type) and issubclass(origin, (Generator, AsyncGenerator)):
        args = get_args(return_annotation)
        if len(args) != 3:
            error_builder.add_diagnostic(
                message=(
                    f"Resolver '{short_name}' has a return annotation '{return_annotation}' which does not specify any features. "
                    f"Please include features inside the type signature -- for example, `{origin.__name__}[Features[MyFeatureSet.id, MyFeatureSet.feature_2], Any, Any]`"
                ),
                code="100",
                label="resolver return does not include features",
                range=error_builder.function_return_annotation(),
                raise_error=TypeError,
            )

        return_annotation = get_args(return_annotation)[0]
        if not (isinstance(return_annotation, type) and issubclass(return_annotation, DataFrame)):
            # If a function is annotated to return an generator, treat it as a DF resolver. This is because generators can yield more than one row
            # Treat scalar-returning generator resolvers as DF-returning, as they could yield more than one row
            return_annotation = DataFrame[return_annotation]
        origin = get_origin(return_annotation)

    if (inspect.isgeneratorfunction(fn) or inspect.isasyncgenfunction(fn)) and not (
        isinstance(return_annotation, type) and issubclass(return_annotation, DataFrame)
    ):
        # If a function is a generator, treat it as a DF resolver. This is because generators can yield more than one row
        # Treat scalar-returning generator resolvers as DF-returning, as they could yield more than one row
        return_annotation = DataFrame[return_annotation]
        origin = get_origin(return_annotation)

    if isinstance(return_annotation, FeatureWrapper):
        return_annotation = unwrap_feature(return_annotation)

    if isinstance(return_annotation, Feature):
        # we handle any explosions in _explode_features()
        maybe_dataframe = return_annotation.typ.parsed_annotation
        if return_annotation.is_has_many and issubclass(maybe_dataframe, DataFrame):
            _validate_dataframe(maybe_dataframe, error_builder, fqn=return_annotation.fqn)
        ret_val = Features[return_annotation]

    if ret_val is None and not ignore_return:
        if not isinstance(return_annotation, type):
            error_builder.add_diagnostic(
                message=(
                    f"Resolver '{short_name}' has a return annotation '{return_annotation}' of type "
                    f"{type(return_annotation)}. "
                    "Resolver return annotations must be a type."
                ),
                code="82",
                label="resolver return annotation is not a type",
                range=error_builder.function_return_annotation(),
                raise_error=TypeError,
            )
        if issubclass(return_annotation, Features):
            # function annotated like def get_account_id(user_id: User.id) -> Features[User.account_id]
            # or def get_account_id(user_id: User.id) -> User:
            ret_val = return_annotation
        elif issubclass(return_annotation, DataFrame):
            # function annotated like def get_transactions(account_id: Account.id) -> DataFrame[Transaction]
            _validate_dataframe(return_annotation, error_builder)
            ret_val = Features[return_annotation]

    if ret_val is None and not ignore_return:
        error_builder.add_diagnostic(
            message=(
                f"Resolver '{short_name}' does not specify a return type. "
                "Please add an annotation (like `-> User.first_name`) to the resolver."
            ),
            code="83",
            label="resolver lacks a return type",
            range=error_builder.function_return_annotation(),
            raise_error=TypeError,
        )

    inputs = [annotation_parser.parse_annotation(p) for p in sig.parameters.keys()]

    # Unwrap anything that is wrapped with FeatureWrapper
    inputs = [unwrap_feature(p) if isinstance(p, FeatureWrapper) else p for p in inputs]

    if len(inputs) == 0:
        default_arg_count = 0
    elif isinstance(inputs[0], type) and issubclass(inputs[0], DataFrame):
        default_arg_count = len(inputs[0].columns)
    else:
        default_arg_count = len(inputs)

    state = None
    default_args: list[Optional[ResolverArgErrorHandler]] = [None for _ in range(default_arg_count)]

    function_definition = get_function_definition(function_source)
    """inexpensive heuristic: if errors, the following inspect code is expensive"""
    datetime_now = "datetime.now()"
    if datetime_now in function_definition:
        caller_filename = inspect.getsourcefile(fn)
        if caller_filename is not None:
            with open(caller_filename, "r") as f:
                content = f.read()
            lines = content.split("\n")
            for i, arg_name in enumerate(sig.parameters.keys()):
                arg_node = error_builder.function_arg_value_by_index(i)
                if arg_node is not None:
                    datetime_now_range = error_builder.string_in_node(node=arg_node, string=datetime_now, text=lines)
                    if datetime_now_range is not None:
                        error_builder.add_diagnostic(
                            message=(
                                f"Do not use 'datetime.now()' in your resolver arguments. "
                                f"If you want the current time for inference or backfills, "
                                f"replace this annotation with chalk.Now."
                            ),
                            code="87",
                            label="replace with chalk.Now",
                            range=datetime_now_range,
                            raise_error=ValueError,
                            code_href="https://docs.chalk.ai/docs/time",
                        )

    for i, (arg_name, parameter) in enumerate(sig.parameters.items()):
        bad_input_message = (
            "Resolver inputs must be Features, DataFrame, or State. "
            f"Resolver '{short_name}' received '{str(inputs[i])}' for argument '{arg_name}'."
        )
        arg = inputs[i]

        if get_origin(arg) in (UnionType, Union):
            args = get_args(arg)
            if len(args) != 2:
                error_builder.add_diagnostic(
                    message=bad_input_message,
                    code="87",
                    label="invalid input type",
                    range=error_builder.function_arg_annotation_by_name(arg_name),
                    raise_error=ValueError,
                )
            if type(None) not in args:
                error_builder.add_diagnostic(
                    message=bad_input_message,
                    code="87",
                    label="invalid input type",
                    range=error_builder.function_arg_annotation_by_name(arg_name),
                    raise_error=ValueError,
                )
            real_arg = next((a for a in args if a is not type(None)), None)
            if real_arg is None:
                error_builder.add_diagnostic(
                    message=bad_input_message,
                    code="87",
                    label="invalid input type",
                    range=error_builder.function_arg_annotation_by_name(arg_name),
                    raise_error=ValueError,
                )
            default_args[i] = ResolverArgErrorHandler(None)
            arg = unwrap_feature(real_arg)
            inputs[i] = arg

        if parameter.empty != parameter.default:
            default_args[i] = ResolverArgErrorHandler(parameter.default)

        if not isinstance(arg, (StateWrapper, Feature)) and not (isinstance(arg, type) and issubclass(arg, DataFrame)):
            if allow_custom_args:
                continue
            if isinstance(arg, datetime) or arg == datetime:
                error_builder.add_diagnostic(
                    message=f"{bad_input_message} If you want the current time for inference or backfills, replace this annotation with chalk.Now.",
                    code="87",
                    label="replace with chalk.Now",
                    range=error_builder.function_arg_annotation_by_name(arg_name),
                    raise_error=ValueError,
                    code_href="https://docs.chalk.ai/docs/time",
                )
            else:
                error_builder.add_diagnostic(
                    message=bad_input_message,
                    code="87",
                    label="invalid input type",
                    range=error_builder.function_arg_annotation_by_name(arg_name),
                    raise_error=ValueError,
                )

        if isinstance(arg, Feature) and arg.last_for is not None and default_args[i] is None:
            default_args[i] = ResolverArgErrorHandler(None)

        if isinstance(arg, Feature) and arg.is_windowed:
            # Windowed arguments in resolver signatures must specify a window bucket
            available_windows = ", ".join(f"{x}s" for x in arg.window_durations)

            error_builder.add_diagnostic(
                message=(
                    f"Resolver argument '{arg_name}' to '{short_name}' does not select a window period. "
                    f"Add a selected window, like {arg.name}('{next(iter(arg.window_durations), '')}'). "
                    f"Available windows: {available_windows}."
                ),
                code="88",
                label="missing period",
                range=error_builder.function_arg_annotation_by_name(arg_name),
                raise_error=ValueError,
            )

        if isinstance(arg, Feature) and arg.is_has_many:
            maybe_dataframe = arg.typ.parsed_annotation
            if issubclass(maybe_dataframe, DataFrame):
                _validate_dataframe(maybe_dataframe, error_builder, fqn=arg.fqn, arg_index=i)

        if not isinstance(arg, StateWrapper):
            continue

        if state is not None:
            error_builder.add_diagnostic(
                message=(
                    f"Only one state argument is allowed. "
                    f"Two provided to '{short_name}': '{state.kwarg}' and '{arg_name}'"
                ),
                code="89",
                label="second state argument",
                range=error_builder.function_arg_annotations()[arg_name],
                raise_error=ValueError,
            )

        arg_name = parameter.name

        arg = cast(StateWrapper, arg)

        state = StateDescriptor(
            kwarg=arg_name,
            pos=i,
            initial=get_state_default_value(
                state_typ=arg.typ,
                resolver_fqn_for_errors=fqn,
                parameter_name_for_errors=arg_name,
                declared_default=parameter.default,
                error_builder=error_builder,
            ),
            typ=arg.typ,
        )

    if not is_streaming_resolver:
        assert ret_val is not None
        ret_val = _explode_features(ret_val, inputs)

    assert ret_val is None or issubclass(ret_val, Features)
    if not ignore_return and ret_val is not None and issubclass(ret_val, Features):
        # Streaming resolvers are themselves windowed, so the outputs must not specify a window explicitly.
        for f in _flatten_features(ret_val):
            if f.is_windowed_pseudofeature and is_streaming_resolver:
                feature_name_without_duration = "__".join(f.root_fqn.split("__")[:-1])  # A bit hacky, but should work
                error_builder.add_diagnostic(
                    message=(
                        "Stream resolvers should not resolve features of particular window periods in the return type. "
                        f"Resolver '{short_name}' returned feature '{f.root_fqn}'. "
                        f"Instead, return '{feature_name_without_duration}'."
                    ),
                    code="90",
                    label="invalid outputs",
                    range=error_builder.function_return_annotation(),
                    raise_error=ValueError,
                )

    if not is_streaming_resolver:
        # TODO(rkargon) If inputs are DataFrames, then the output must be a DataFrame as well.
        #   Remove this once we support resolvers of type DF[X] --> Y.y
        #   (e.g. 'population-level' aggregations)
        if any((isinstance(x, type) and issubclass(x, DataFrame)) for x in inputs):
            assert ret_val is not None
            if not (
                len(ret_val.features) == 1
                and isinstance(ret_val.features[0], type)
                and issubclass(cast(type, ret_val.features[0]), DataFrame)
            ):
                error_builder.add_diagnostic(
                    message=(
                        f"Resolver that has DataFrame inputs cannot have a non-DataFrame output feature."
                        f"The resolver '{short_name}' returns '{ret_val}', which is not a DataFrame."
                    ),
                    code="91",
                    label="non-DataFrame output",
                    range=error_builder.function_return_annotation(),
                    raise_error=TypeError,
                )

    state_index = state.pos if state is not None else None
    return ResolverParseResult(
        fqn=fqn,
        inputs=[v for i, v in enumerate(inputs) if i != state_index],
        output=ret_val,
        function=cast(Callable[P, T], fn),
        function_definition=function_source,
        doc=fn.__doc__,
        state=state,
        default_args=default_args,
    )


def _validate_dataframe(
    df: DataFrameMeta, error_builder: ResolverErrorBuilder, fqn: Optional[str] = None, arg_index: Optional[int] = None
):
    if fqn is not None:
        feature = Feature.from_root_fqn(fqn)
        if feature.joined_class is not None:
            namespace = feature.joined_class.namespace
        else:
            namespace = None
    else:
        namespace = None
    input_output_string = "output" if arg_index is None else "input"
    path_string = f"at '{fqn}' " if fqn is not None else ""
    for feature in df.columns:
        if feature.namespace == PSEUDONAMESPACE:
            continue
        if namespace is not None and feature.root_namespace != namespace:
            if fqn is None:
                node_range = (
                    error_builder.function_return_annotation()
                    if arg_index is None
                    else error_builder.function_arg_annotation_by_index(arg_index)
                )
                error_builder.add_diagnostic(
                    message=(
                        f"Resolver has DataFrame {input_output_string}s {path_string}with different namespaces,"
                        f" '{namespace}' and '{feature.namespace}'."
                        f" DataFrames can only have features from the same feature class."
                    ),
                    code="161",
                    label="different namespaces",
                    range=node_range,
                    raise_error=ValueError,
                )
            else:
                node_range = (
                    error_builder.function_return_annotation()
                    if arg_index is None
                    else error_builder.function_arg_annotation_by_index(arg_index)
                )
                error_builder.add_diagnostic(
                    message=(
                        f"Resolver has DataFrame {input_output_string}s {path_string}with columns of the wrong namespace,"
                        f" Columns must be features of feature class '{namespace}', but found feature '{feature.fqn}'."
                    ),
                    code="161",
                    label="wrong namespace",
                    range=node_range,
                    raise_error=ValueError,
                )
            break
        namespace = feature.root_namespace


def get_function_definition(text: str) -> str:
    lines = text.split("\n")
    if lines[0].startswith("@"):
        lines = lines[1:]
    open_parentheses_count = 0
    started = False
    definition_lines: List[str] = []
    for line in lines:
        if "(" in line:
            open_parentheses_count += line.count("(")
            started = True
        if ")" in line:
            open_parentheses_count -= line.count(")")
            started = True
        definition_lines.append(line)
        if started is True and open_parentheses_count == 0:
            return "\n".join(definition_lines)
    return "\n".join(definition_lines)


def parse_sink_function(
    fn: Callable[P, T],
    glbs: Optional[Dict[str, Any]],
    lcls: Optional[Dict[str, Any]],
    error_builder: ResolverErrorBuilder,
    name: str | None,
) -> SinkResolverParseResult[P, T]:
    fqn = get_resolver_fqn(function=fn, name=name)
    sig = inspect.signature(fn)
    annotation_parser = ResolverAnnotationParser(fn, glbs, lcls, error_builder)
    function_definition = inspect.getsource(fn)
    annotations = [annotation_parser.parse_annotation(p) for p in sig.parameters.keys()]

    if len(annotations) == 1 and isinstance(annotations[0], type) and issubclass(annotations[0], DataFrame):
        # It looks like the user's function wants a DataFrame of features
        df = annotations[0]
        features = df.columns

        return SinkResolverParseResult(
            fqn=fqn,
            input_is_df=True,
            function=fn,
            function_definition=function_definition,
            doc=fn.__doc__,
            input_feature_defaults=[None for _ in range(len(features))],
            input_features=list(features),
        )

    else:
        # It looks like the user's function wants features as individual parameters
        feature_default_values: list[Optional[ResolverArgErrorHandler]] = []
        feature_inputs = []

        for i, (arg_name, parameter) in enumerate(sig.parameters.items()):
            arg = annotations[i]
            default_value = None
            if isinstance(arg, FeatureWrapper):
                # Unwrap anything that is wrapped with FeatureWrapper
                arg = unwrap_feature(arg)

            bad_input_message = (
                f"Sink resolver inputs must be Features. Received {str(arg)} for argument '{arg_name}' for '{fqn}'.\n"
            )

            if get_origin(arg) in (UnionType, Union):  # Optional[] handling
                args = get_args(arg)
                if len(args) != 2:
                    error_builder.add_diagnostic(
                        message=bad_input_message,
                        code="92",
                        label="invalid input",
                        range=error_builder.function_arg_annotation_by_name(arg_name),
                        raise_error=ValueError,
                    )
                if type(None) not in args:
                    error_builder.add_diagnostic(
                        message=bad_input_message,
                        code="92",
                        label="invalid input",
                        range=error_builder.function_arg_annotation_by_name(arg_name),
                        raise_error=ValueError,
                    )
                real_arg = next((a for a in args if a is not type(None)), None)
                if real_arg is None:
                    error_builder.add_diagnostic(
                        message=bad_input_message,
                        code="92",
                        label="invalid input",
                        range=error_builder.function_arg_annotation_by_name(arg_name),
                        raise_error=ValueError,
                    )
                default_value = ResolverArgErrorHandler(None)
                arg = unwrap_feature(real_arg)

            if not isinstance(arg, Feature):
                error_builder.add_diagnostic(
                    message=bad_input_message,
                    code="92",
                    label="invalid input",
                    range=error_builder.function_arg_annotations()[arg_name],
                    raise_error=ValueError,
                )

            if parameter.empty != parameter.default:
                default_value = ResolverArgErrorHandler(parameter.default)

            feature_default_values.append(default_value)
            feature_inputs.append(arg)

        return SinkResolverParseResult(
            fqn=fqn,
            input_features=feature_inputs,
            function=fn,
            function_definition=function_definition,
            doc=fn.__doc__,
            input_is_df=False,
            input_feature_defaults=feature_default_values,
        )


@overload
def online(
    *,
    environment: Optional[Environments] = None,
    tags: Optional[Tags] = None,
    cron: CronTab | Duration | Cron | None = None,
    machine_type: Optional[MachineType] = None,
    when: Optional[Any] = None,
    owner: Optional[str] = None,
    timeout: Optional[Duration] = None,
    name: str | None = None,
) -> Callable[[Callable[P, T]], ResolverProtocol[P, T]]:
    ...


@overload
def online(
    fn: Callable[P, T],
    /,
) -> ResolverProtocol[P, T]:
    ...


def online(
    fn: Callable[P, T] | None = None,
    /,
    *,
    environment: Environments | None = None,
    tags: Tags | None = None,
    cron: CronTab | Duration | Cron | None = None,
    machine_type: MachineType | None = None,
    when: Any | None = None,
    owner: str | None = None,
    timeout: Duration | None = None,
    name: str | None = None,
) -> Union[Callable[[Callable[P, T]], ResolverProtocol[P, T]], ResolverProtocol[P, T]]:
    """Decorator to create an online resolver.

    Parameters
    ----------
    environment
        Environments are used to trigger behavior
        in different deployments such as staging, production, and
        local development. For example, you may wish to interact with
        a vendor via an API call in the production environment, and
        opt to return a constant value in a staging environment.

        Environment can take one of three types:
            - `None` (default) - candidate to run in every environment
            - `str` - run only in this environment
            - `list[str]` - run in any of the specified environment and no others

        Read more at https://docs.chalk.ai/docs/resolver-environments
    owner
        Individual or team responsible for this resolver.
        The Chalk Dashboard will display this field, and alerts
        can be routed to owners.
    tags
        Allow you to scope requests within an
        environment. Both tags and environment need to match for a
        resolver to be a candidate to execute.

        You might consider using tags, for example, to change out
        whether you want to use a sandbox environment for a vendor,
        or to bypass the vendor and return constant values in a
        staging environment.

        Read more at https://docs.chalk.ai/docs/resolver-tags
    cron
        You can schedule resolvers to run on a pre-determined
        schedule via the cron argument to resolver decorators.

        Cron can sample all examples, a subset of all examples,
        or a custom provided set of examples.

        Read more at https://docs.chalk.ai/docs/resolver-cron
    timeout
        You can specify the maximum duration to wait for the
        resolver's result. Once the resolver's runtime exceeds
        the specified duration, a timeout error will be returned
        along with each output feature.

        Please use supported Chalk durations
        'w', 'd', 'h', 'm', 's', and/or 'ms'.

        Read more at https://docs.chalk.ai/docs/timeout
                 and https://docs.chalk.ai/docs/duration
    when
        Like tags, `when` can filter when a resolver is eligible
        to run. Unlike tags, `when` can use feature values,
        so that you can write resolvers like:

        >>> @online(when=User.risk_profile == "low" or User.is_employee)
        ... def resolver_fn(...) -> ...:
        ...     ...

    Other Parameters
    ----------------
    fn
        The function that you're decorating as a resolver.
    machine_type
        You can optionally specify that resolvers need to run on a
        machine other than the default. Must be configured in your
        deployment.
    name
        An alternative shortname for the resolver, to use instead of the function name

    Returns
    -------
    Callable[[Callable[P, T]], ResolverProtocol[P, T]] | ResolverProtocol[P, T]
        A `ResolverProtocol` which can be called as a normal function! You can unit-test
        resolvers as you would unit-test any other code.

        Read more at https://docs.chalk.ai/docs/unit-tests

    Examples
    --------
    >>> @online
    ... def name_match(
    ...     name: User.full_name,
    ...     account_name: User.bank_account.title
    ... ) -> User.account_name_match_score:
    ...     if name.lower() == account_name.lower():
    ...         return 1.
    ...     return 0.
    """
    frame = inspect.currentframe()
    assert frame is not None
    caller_frame = frame.f_back
    assert caller_frame is not None
    caller_globals = caller_frame.f_globals
    caller_locals = caller_frame.f_locals

    def decorator(fn: Callable[P, T]):
        caller_filename = inspect.getsourcefile(fn) or "<unknown file>"
        try:
            caller_lines = inspect.getsourcelines(fn) or None
        except:
            caller_lines = None
        error_builder = get_resolver_error_builder(fn)

        parsed = parse_function(
            fn=fn,
            glbs=caller_globals,
            lcls=caller_locals,
            error_builder=error_builder,
            name=name,
        )
        if parsed.output is None:
            error_builder.add_diagnostic(
                message=f"Online resolvers must return features; '{parsed.fqn}' returns None",
                code="72",
                label="missing output",
                range=error_builder.function_return_annotation(),
                raise_error=TypeError,
            )

        resolver = OnlineResolver(
            filename=caller_filename,
            function_definition=parsed.function_definition,
            fqn=parsed.fqn,
            doc=parsed.doc,
            inputs=parsed.inputs,
            output=parsed.output,
            fn=fn,
            environment=None if environment is None else list(ensure_tuple(environment)),
            tags=None if tags is None else list(ensure_tuple(tags)),
            cron=cron,
            machine_type=machine_type,
            when=when,
            owner=owner,
            state=parsed.state,
            default_args=parsed.default_args,
            timeout=timeout,
            source_line=None if caller_lines is None else caller_lines[1],
            lsp_builder=error_builder,
            data_sources=None,
            is_sql_file_resolver=False,
            underscore=None,
        )

        resolver.add_to_registry(override=False)
        # Return the decorated resolver, which notably implements __call__() so it acts the same as
        # the underlying function if called directly, e.g. from test code
        return resolver

    return decorator(fn) if fn else decorator


@overload
def offline(
    *,
    environment: Environments | None = None,
    tags: Tags | None = None,
    cron: CronTab | Duration | Cron | None = None,
    machine_type: MachineType | None = None,
    when: Any | None = None,
    owner: str | None = None,
    name: str | None = None,
) -> Callable[[Callable[P, T]], ResolverProtocol[P, T]]:
    ...


@overload
def offline(
    fn: Callable[P, T],
    /,
) -> ResolverProtocol[P, T]:
    ...


def offline(
    fn: Optional[Callable[P, T]] = None,
    /,
    *,
    environment: Environments | None = None,
    tags: Tags | None = None,
    cron: CronTab | Duration | Cron | None = None,
    machine_type: MachineType | None = None,
    when: Any | None = None,
    owner: str | None = None,
    timeout: Duration | None = None,
    name: str | None = None,
) -> Union[Callable[[Callable[P, T]], Callable[P, T]], ResolverProtocol[P, T]]:
    """Decorator to create an offline resolver.

    Parameters
    ----------
    environment
        Environments are used to trigger behavior
        in different deployments such as staging, production, and
        local development. For example, you may wish to interact with
        a vendor via an API call in the production environment, and
        opt to return a constant value in a staging environment.

        Environment can take one of three types:
            - `None` (default) - candidate to run in every environment
            - `str` - run only in this environment
            - `list[str]` - run in any of the specified environment and no others

        Read more at https://docs.chalk.ai/docs/resolver-environments
    owner
        Allows you to specify an individual or team
        who is responsible for this resolver. The Chalk Dashboard
        will display this field, and alerts can be routed to owners.
    tags
        Allow you to scope requests within an
        environment. Both tags and environment need to match for a
        resolver to be a candidate to execute.

        You might consider using tags, for example, to change out
        whether you want to use a sandbox environment for a vendor,
        or to bypass the vendor and return constant values in a
        staging environment.

        Read more at https://docs.chalk.ai/docs/resolver-tags
    cron
        You can schedule resolvers to run on a pre-determined
        schedule via the cron argument to resolver decorators.

        Cron can sample all examples, a subset of all examples,
        or a custom provided set of examples.

        Read more at https://docs.chalk.ai/docs/resolver-cron
    timeout
        You can specify the maximum duration to wait for the
        resolver's result. Once the resolver's runtime exceeds
        the specified duration, a timeout error will be raised.

        Please use supported Chalk durations
        'w', 'd', 'h', 'm', 's', and/or 'ms'.

        Read more at https://docs.chalk.ai/docs/timeout
                 and https://docs.chalk.ai/docs/duration
    when
        Like tags, `when` can filter when a resolver
        is eligible to run. Unlike tags, `when` can use feature values,
        so that you can write resolvers like::

        >>> @offline(when=User.risk_profile == "low" or User.is_employee)
        ... def resolver_fn(...) -> ...:
        ...    ...

    Other Parameters
    ----------------
    fn
        The function that you're decorating as a resolver.
    machine_type
        You can optionally specify that resolvers need to run on
        a machine other than the default. Must be configured in
        your deployment.
    name
        An alternative shortname for the resolver, to use instead of the function name

    Returns
    -------
    Union[Callable[[Callable[P, T]], ResolverProtocol[P, T]], ResolverProtocol[P, T]]
        A `ResolverProtocol` which can be called as a normal function! You can unit-test
        resolvers as you would unit-test any other code.

        Read more at https://docs.chalk.ai/docs/unit-tests

    Examples
    --------
    >>> @offline(cron="1h")
    ... def get_fraud_score(
    ...     email: User.email,
    ...     name: User.name,
    ... ) -> User.fraud_score:
    ...     return socure.get_sigma_score(email, name)
    """
    frame = inspect.currentframe()
    assert frame is not None
    caller_frame = frame.f_back
    assert caller_frame is not None
    caller_globals = caller_frame.f_globals
    caller_locals = caller_frame.f_locals
    caller_line = caller_frame.f_lineno

    def decorator(fn: Callable[P, T]):
        caller_filename = inspect.getsourcefile(fn) or "<unknown file>"
        error_builder = get_resolver_error_builder(fn)
        parsed = parse_function(fn, caller_globals, caller_locals, error_builder)
        if parsed.output is None:
            error_builder.add_diagnostic(
                message=f"Offline resolvers must return features; '{parsed.fqn}' returns None",
                code="72",
                label="missing output",
                range=error_builder.function_return_annotation(),
                raise_error=TypeError,
            )
        resolver = OfflineResolver(
            filename=caller_filename,
            function_definition=parsed.function_definition,
            fqn=parsed.fqn,
            doc=parsed.doc,
            inputs=parsed.inputs,
            output=parsed.output,
            fn=fn,
            environment=None if environment is None else list(ensure_tuple(environment)),
            tags=None if tags is None else list(ensure_tuple(tags)),
            cron=cron,
            machine_type=machine_type,
            state=parsed.state,
            when=when,
            owner=owner,
            default_args=parsed.default_args,
            timeout=timeout,
            source_line=caller_line,
            lsp_builder=error_builder,
            is_sql_file_resolver=False,
            data_sources=None,
            underscore=None,
        )
        resolver.add_to_registry(override=False)
        return resolver

    return decorator(fn) if fn else decorator


@overload
def sink(
    *,
    environment: Environments | None = None,
    tags: Tags | None = None,
    machine_type: MachineType | None = None,
    buffer_size: int | None = None,
    debounce: Duration | None = None,
    max_delay: Duration | None = None,
    upsert: bool = False,
    integration: BaseSQLSourceProtocol | SinkIntegrationProtocol | None = None,
    owner: str | None = None,
) -> Callable[[Callable[P, T]], ResolverProtocol[P, T]]:
    ...


@overload
def sink(
    fn: Callable[P, T],
    /,
) -> ResolverProtocol[P, T]:
    ...


def sink(
    fn: Callable[P, T] | None = None,
    /,
    *,
    environment: Environments | None = None,
    tags: Tags | None = None,
    machine_type: MachineType | None = None,
    buffer_size: int | None = None,
    debounce: Duration | None = None,
    max_delay: Duration | None = None,
    upsert: bool = False,
    integration: BaseSQLSourceProtocol | SinkIntegrationProtocol | None = None,
    owner: str | None = None,
    name: str | None = None,
) -> Union[Callable[[Callable[P, T]], ResolverProtocol[P, T]], ResolverProtocol[P, T]]:
    """Decorator to create a sink.
    Read more at https://docs.chalk.ai/docs/sinks

    Parameters
    ----------
    environment
        Environments are used to trigger behavior
        in different deployments such as staging, production, and
        local development. For example, you may wish to interact with
        a vendor via an API call in the production environment, and
        opt to return a constant value in a staging environment.

        Environment can take one of three types:
            - `None` (default) - candidate to run in every environment
            - `str` - run only in this environment
            - `list[str]` - run in any of the specified environment and no others

        Read more at https://docs.chalk.ai/docs/resolver-environments
    tags
        Allow you to scope requests within an
        environment. Both tags and environment need to match for a
        resolver to be a candidate to execute.

        You might consider using tags, for example, to change out
        whether you want to use a sandbox environment for a vendor,
        or to bypass the vendor and return constant values in a
        staging environment.

        Read more at https://docs.chalk.ai/docs/resolver-tags
    buffer_size
        Count of updates to buffer.
    owner
        The individual or team responsible for this resolver.
        The Chalk Dashboard will display this field, and alerts
        can be routed to owners.

    Other Parameters
    ----------------
    fn
        The function that you're decorating as a resolver.
    machine_type
        You can optionally specify that resolvers need to run on a
        machine other than the default. Must be configured in your
        deployment.
    debounce
    max_delay
    upsert
    integration

    Examples
    --------
    >>> @sink
    ... def process_updates(
    ...     uid: User.id,
    ...     email: User.email,
    ...     phone: User.phone,
    ... ):
    ...     user_service.update(
    ...         uid=uid,
    ...         email=email,
    ...         phone=phone
    ...     )
    >>> process_updates(123, "sam@chalk.ai", "555-555-5555")

    Returns
    -------
    Callable[[Any, ...], Any]
        A callable function! You can unit-test sinks as you
        would unit test any other code.
        Read more at https://docs.chalk.ai/docs/unit-tests
    """
    frame = inspect.currentframe()
    assert frame is not None
    caller_frame = frame.f_back
    assert caller_frame is not None
    caller_globals = caller_frame.f_globals
    caller_locals = caller_frame.f_locals
    caller_line = caller_frame.f_lineno

    def decorator(fn: Callable[P, T]):
        caller_filename = inspect.getsourcefile(fn) or "unknown_file"
        error_builder = get_resolver_error_builder(fn)
        parsed = parse_sink_function(fn, caller_globals, caller_locals, error_builder, name=name)
        resolver = SinkResolver(
            filename=caller_filename,
            function_definition=parsed.function_definition,
            fqn=parsed.fqn,
            doc=parsed.doc,
            inputs=parsed.input_features,
            fn=fn,
            environment=None if environment is None else list(ensure_tuple(environment)),
            tags=None if tags is None else list(ensure_tuple(tags)),
            machine_type=machine_type,
            buffer_size=buffer_size,
            debounce=debounce,
            max_delay=max_delay,
            upsert=upsert,
            integration=integration,
            owner=owner,
            default_args=parsed.input_feature_defaults,
            input_is_df=parsed.input_is_df,
            source_line=caller_line,
            lsp_builder=error_builder,
            data_sources=None,
        )
        resolver.add_to_registry(override=False)
        return resolver

    return decorator(fn) if fn else decorator


class StreamResolver(Resolver[P, T]):
    def __init__(
        self,
        function_definition: str,
        fqn: str,
        filename: str,
        source: StreamSource,
        fn: Callable[P, T],
        environment: list[str] | None,
        doc: str | None,
        mode: Literal["continuous", "tumbling"] | None,
        machine_type: str | None,
        message: Type[Any] | None,
        output: Type[Features],
        signature: StreamResolverSignature,
        state: StateDescriptor | None,
        sql_query: str | None,
        owner: str | None,
        parse: ParseInfo | None,
        keys: dict[str, Any] | None,
        timestamp: str | None,
        source_line: int | None,
        tags: list[str] | None,
        lsp_builder: ResolverErrorBuilder,
    ):
        super().__init__(
            function_definition=function_definition,
            lsp_builder=lsp_builder,
            filename=filename,
            environment=environment,
            machine_type=machine_type,
            fqn=fqn,
            fn=fn,
            doc=doc,
            inputs=[],
            output=output,
            tags=tags,
            cron=None,
            when=None,
            state=state,
            default_args=[],
            owner=owner,
            source_line=source_line,
            timeout=None,
            is_sql_file_resolver=False,
            data_sources=None,
            underscore=None,
        )
        self.source = source
        self.message = message
        self.mode = mode
        self.signature = signature
        self.sql_query = sql_query
        self.parse = parse
        self.keys = keys
        self.timestamp = timestamp
        fqn_to_windows = {o.fqn: o.window_durations for o in _flatten_features(self.output) if o.is_windowed}
        if len(set(tuple(v) for v in fqn_to_windows.values())) > 1:
            fqn_to_declared_windows = {
                o.fqn: sorted(o.window_durations) for o in _flatten_features(self.output) if o.is_windowed
            }
            periods = [f'{fqn}[{", ".join(f"{window}s")}]' for fqn, window in fqn_to_declared_windows.items()]
            raise ValueError(f"All features must have the same window periods. Found {', '.join(periods)}")
        self.window_periods_seconds = next(iter(fqn_to_windows.values()), ())
        # Mapping of window (in secs) to mapping of (original feature, windowed pseudofeature)
        self.windowed_pseudofeatures: Dict[int, Dict[Feature, Feature]] = {}
        self.window_index = None
        for i, w in enumerate(signature.params):
            if isinstance(w, StreamResolverParamMessageWindow):
                self.window_index = i
                break

        for window_period in self.window_periods_seconds:
            self.windowed_pseudofeatures[window_period] = {}
            for o in _flatten_features(self.output):
                if o.is_windowed:
                    windowed_fqn = get_name_with_duration(o.root_fqn, window_period)
                    windowed_feature = Feature.from_root_fqn(windowed_fqn)
                    self.windowed_pseudofeatures[window_period][o] = windowed_feature

    @property
    def output_features(self) -> Sequence[Feature]:
        return _flatten_features(self.output)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        from chalk._autosql.autosql import query_as_feature_formatted

        raw_result = self.fn(*args, **kwargs)
        if self.window_index is not None and isinstance(raw_result, str) and str(args[self.window_index]) in raw_result:
            raw_result = DataFrame(
                query_as_feature_formatted(
                    formatted_query=raw_result,
                    fqn_to_name={s.root_fqn: s.name for s in self.output_features},
                    table=args[self.window_index],
                )
            )

        return cast(T, raw_result)

    def __repr__(self):
        return f"StreamResolver(name={self.fqn})"


def _is_stream_resolver_body_type(annotation: Type):
    origin = get_origin(annotation)
    if origin is not None:
        return False
    return (
        isinstance(annotation, type) and (issubclass(annotation, (str, bytes)) or is_pydantic_basemodel(annotation))
    ) or dataclasses.is_dataclass(annotation)


def _parse_stream_resolver_param(
    param: Parameter,
    annotation_parser: ResolverAnnotationParser,
    resolver_fqn_for_errors: str,
    is_windowed_resolver: bool,
    error_builder: ResolverErrorBuilder,
) -> StreamResolverParam:
    if param.kind not in {Parameter.KEYWORD_ONLY, Parameter.POSITIONAL_OR_KEYWORD}:
        error_builder.add_diagnostic(
            message=(
                f"Stream resolver '{resolver_fqn_for_errors}' includes unsupported keyword or variadic arg '{param.name}'"
            ),
            code="120",
            label="invalid stream resolver parameter",
            range=error_builder.function_arg_annotation_by_name(param.name),
            raise_error=ValueError,
        )

    annotation = annotation_parser.parse_annotation(param.name)
    if isinstance(annotation, StateWrapper):
        if is_windowed_resolver:
            error_builder.add_diagnostic(
                message=(
                    f"Windowed stream resolvers cannot have state, but '{resolver_fqn_for_errors}' requires state."
                ),
                code="121",
                label="invalid state parameter",
                range=error_builder.function_arg_annotation_by_name(param.name),
                raise_error=ValueError,
            )
        default_value = get_state_default_value(
            state_typ=annotation.typ,
            declared_default=param.default,
            resolver_fqn_for_errors=resolver_fqn_for_errors,
            parameter_name_for_errors=param.name,
            error_builder=error_builder,
        )
        return StreamResolverParamKeyedState(
            name=param.name,
            typ=annotation.typ,
            default_value=default_value,
        )

    if not is_windowed_resolver and _is_stream_resolver_body_type(annotation):
        return StreamResolverParamMessage(name=param.name, typ=annotation)

    if is_windowed_resolver and get_origin(annotation) in (list, List):
        item_typ = get_args(annotation)[0]
        if _is_stream_resolver_body_type(item_typ):
            return StreamResolverParamMessageWindow(name=param.name, typ=annotation)

    if (
        is_windowed_resolver
        and isclass(annotation)
        and (
            issubclass(annotation, pyarrow.Table)
            or is_pydantic_basemodel(annotation)
            or annotation.__name__ in ("DataFrame", "DataFrameImpl", "SubclassedDataFrame")
        )
    ):
        # Using string comparison as polars may not be installed
        return StreamResolverParamMessageWindow(name=param.name, typ=annotation)
    error_builder.add_diagnostic(
        message=(
            f"Stream resolver parameter '{param.name}' of resolver '{resolver_fqn_for_errors}' is not recognized. "
            "Message payloads must be one of `str`, `bytes`, or pydantic model class. "
            "Keyed state parameters must be chalk.KeyedState[T]. "
            f"Received: {annotation}"
        ),
        code="122",
        label="invalid input",
        range=error_builder.function_arg_annotation_by_name(param.name),
        raise_error=ValueError,
    )


def _parse_stream_resolver_params(
    user_func: Callable,
    error_builder: ResolverErrorBuilder,
    *,
    resolver_fqn_for_errors: str,
    annotation_parser: ResolverAnnotationParser,
    is_windowed_resolver: bool,
) -> Sequence[StreamResolverParam]:
    sig = inspect.signature(user_func)
    params = [
        _parse_stream_resolver_param(p, annotation_parser, resolver_fqn_for_errors, is_windowed_resolver, error_builder)
        for p in sig.parameters.values()
    ]
    num_params = len(params)
    if num_params == 1:
        if not isinstance(params[0], (StreamResolverParamMessage, StreamResolverParamMessageWindow)):
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{resolver_fqn_for_errors}' must take as input "
                    "a Pydantic model, `str`, or `bytes` representing the message body. "
                ),
                code="93",
                label="invalid input",
                range=error_builder.function_arg_annotation_by_name(params[0].name),
                raise_error=ValueError,
            )
    elif num_params == 2:
        if isinstance(params[0], StreamResolverParamKeyedState):
            stream_input_model = params[1]
        elif isinstance(params[1], StreamResolverParamKeyedState):
            stream_input_model = params[0]
        else:
            error_builder.add_diagnostic(
                message=(
                    f"Streaming resolver '{resolver_fqn_for_errors}' of length '{num_params}' must have "
                    "exactly one non-State input argument. "
                ),
                code="94",
                label="invalid input",
                range=error_builder.function_arg_annotation_by_name(params[1].name),
                raise_error=ValueError,
            )
            raise  # for type-checking, but the above raises
        if isinstance(stream_input_model, StreamResolverParamKeyedState):
            error_builder.add_diagnostic(
                message=f"Stream resolver '{resolver_fqn_for_errors}' includes more than one KeyedState parameter.",
                code="95",
                label="only one KeyedState parameter permitted",
                range=error_builder.function_arg_annotation_by_name(params[1].name),
                raise_error=ValueError,
            )
        if not isinstance(stream_input_model, (StreamResolverParamMessage, StreamResolverParamMessageWindow)):
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{resolver_fqn_for_errors}' must take as input "
                    "a Pydantic model, `str`, or `bytes` representing the message body. "
                ),
                code="96",
                label="invalid input",
                range=error_builder.function_arg_annotation_by_name(params[0].name),
                raise_error=ValueError,
            )
    else:
        error_builder.add_diagnostic(
            message=(
                f"Streaming resolver '{resolver_fqn_for_errors}' of length '{num_params}' must have "
                "exactly one non-State input argument. "
            ),
            code="97",
            label="invalid input",
            range=error_builder.function_arg_annotation_by_name(params[0].name),
            raise_error=ValueError,
        )

    return params


def _parse_stream_resolver_output_features(
    user_func: Callable,
    error_builder: ResolverErrorBuilder,
    *,
    resolver_fqn_for_errors: str,
) -> Type[Features]:
    return_annotation = cached_get_type_hints(user_func).get("return")
    if return_annotation is None:
        error_builder.add_diagnostic(
            message=f"Resolver '{resolver_fqn_for_errors}' must have a return annotation.",
            code="81",
            label="missing return annotation",
            range=error_builder.function_return_annotation(),
            raise_error=TypeError,
            code_href="https://docs.chalk.ai/docs/resolver-outputs",
        )
    if isinstance(return_annotation, FeatureWrapper):
        return_annotation = Features[unwrap_feature(return_annotation)]

    if not isinstance(return_annotation, type):
        error_builder.add_diagnostic(
            message=(
                f"Resolver '{resolver_fqn_for_errors}' has a return annotation {return_annotation} "
                f"of type {type(return_annotation)}. Resolver return annotation values must be a type. "
            ),
            code="82",
            label="not a type",
            range=error_builder.function_return_annotation(),
            raise_error=TypeError,
        )

    if issubclass(return_annotation, DataFrame):
        return Features[return_annotation]

    if not issubclass(return_annotation, Features):
        error_builder.add_diagnostic(
            message=(
                f"Stream resolver '{resolver_fqn_for_errors}' did not have a valid return type: "
                "must be a features class or Features[...]."
            ),
            code="82",
            label="invalid return type",
            range=error_builder.function_return_annotation(),
            raise_error=TypeError,
        )

    for feature in return_annotation.features:
        if feature.is_windowed_pseudofeature:
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{resolver_fqn_for_errors}' did not have a valid return type: "
                    "For stream resolvers, specific durations should not be specified in the return."
                    "For example, 'A.windowed_feature[\"60m\"]' should be rewritten as 'A.windowed_feature'"
                ),
                code="82",
                label="windowed feature does not need a specified duration",
                range=error_builder.function_return_annotation(),
                raise_error=TypeError,
            )

    # TODO: validate that these features are in the same namespace and include a pkey
    output_features = return_annotation

    return output_features


@dataclass(frozen=True)
class ParseInfo(Generic[T, V]):
    fn: Callable[[T], V]
    input_type: Type[T]
    output_type: Type[V]
    output_is_optional: bool


def _validate_parse_function(
    stream_fn: Callable[P, T],
    parse_fn: Callable[[T], Any],
    globals: dict[str, Any] | None,
    locals: dict[str, Any] | None,
    params: Sequence[StreamResolverParam],
    resolver_error_builder: ResolverErrorBuilder,
    name: str | None,
) -> ParseInfo:
    parse_error_builder = get_resolver_error_builder(parse_fn)
    """We need separate error builders for resolver and parse fn: different AST nodes"""

    stream_fqn = get_resolver_fqn(function=stream_fn, name=name)
    parse_fqn = get_resolver_fqn(function=parse_fn, name=name)
    sig = inspect.signature(parse_fn)
    annotation_parser = ResolverAnnotationParser(parse_fn, globals, locals, parse_error_builder)

    output_optional = False
    return_annotation = cached_get_type_hints(parse_fn).get("return")
    if not return_annotation:
        parse_error_builder.add_diagnostic(
            message=f"Parse function '{parse_fqn}' must have a return annotation.",
            code="98",
            label="missing return annotation",
            range=parse_error_builder.function_return_annotation(),
            raise_error=TypeError,
        )
    if get_origin(return_annotation) in (UnionType, Union):
        return_args = get_args(return_annotation)
        parse_output = next((a for a in return_args if a is not type(None)), None)
        if len(return_args) != 2 or type(None) not in return_args or parse_output is None:
            parse_error_builder.add_diagnostic(
                message=(
                    f"Parse function '{parse_fqn}' return annotation must be a singleton or an optional singleton."
                ),
                code="99",
                label="invalid parse function return annotation",
                range=parse_error_builder.function_return_annotation(),
                raise_error=TypeError,
            )
        output_optional = True
    elif get_origin(return_annotation):
        parse_error_builder.add_diagnostic(
            message=(f"Parse function '{parse_fqn}' return annotation must be a singleton or an optional singleton."),
            code="99",
            label="invalid parse function return annotation",
            range=parse_error_builder.function_return_annotation(),
            raise_error=TypeError,
        )
        raise
    else:
        parse_output = return_annotation
    if not is_pydantic_basemodel(parse_output):
        parse_error_builder.add_diagnostic(
            message=f"Parse function '{parse_fqn}' return annotation must be of type pydantic.BaseModel",
            code="101",
            label="invalid parse function return annotation",
            range=parse_error_builder.function_return_annotation(),
            raise_error=TypeError,
        )
    stream_fn_input_arg = next(
        param for param in params if isinstance(param, (StreamResolverParamMessage, StreamResolverParamMessageWindow))
    )
    stream_fn_input_type = _get_stream_resolver_input_type(stream_fn_input_arg, stream_fqn, resolver_error_builder)
    if parse_output != stream_fn_input_type:
        parse_error_builder.add_diagnostic(
            message=(
                f"Parse function '{parse_fqn}' return annotation must match input annotation of resolver '{stream_fqn}'"
            ),
            code="102",
            label="invalid parse function return annotation",
            range=parse_error_builder.function_return_annotation(),
            raise_error=TypeError,
        )

    parse_inputs = [annotation_parser.parse_annotation(p) for p in sig.parameters.keys()]
    if len(parse_inputs) != 1:
        parse_error_builder.add_diagnostic(
            message=(
                f"Parse function '{parse_fqn}' has {len(parse_inputs)} inputs. "
                f"Parse functions must have one input argument"
            ),
            code="103",
            label="extraneous argument",
            range=parse_error_builder.function_arg_value_by_index(len(parse_inputs) - 1),
            raise_error=TypeError,
        )
    parse_input = parse_inputs[0]
    parse_input_name = list(sig.parameters.keys())[0]
    if get_origin(parse_input):
        parse_error_builder.add_diagnostic(
            message=f"Parse function '{parse_fqn}' input annotation must be a singleton",
            code="104",
            label="extraneous argument",
            range=parse_error_builder.function_arg_value_by_name(parse_input_name),
            raise_error=TypeError,
        )

    if not is_pydantic_basemodel(parse_input) and parse_input != bytes:
        parse_error_builder.add_diagnostic(
            message=f"Parse function '{parse_fqn}' input annotation must be of type pydantic.BaseModel or bytes",
            code="105",
            label="invalid parse function input annotation",
            range=parse_error_builder.function_arg_value_by_name(parse_input_name),
            raise_error=TypeError,
        )

    return ParseInfo(fn=parse_fn, input_type=parse_input, output_type=parse_output, output_is_optional=output_optional)


def _get_stream_resolver_input_type(
    param: Union[StreamResolverParamMessage, StreamResolverParamMessageWindow],
    stream_fqn: str,
    error_builder: ResolverErrorBuilder,
) -> Type[BaseModel]:
    if isinstance(param, StreamResolverParamMessage):
        input_model_type = param.typ
    elif isinstance(param, StreamResolverParamMessageWindow):  # pyright: ignore[reportUnnecessaryIsInstance]
        if get_origin(param.typ) in (List, list):
            input_model_types = get_args(param.typ)
            input_model_type = next((a for a in input_model_types if a is not type(None)), None)
        elif isinstance(param.typ, type) and issubclass(param.typ, DataFrame):
            stream_input_annotation = param.typ
            input_model_type = stream_input_annotation.__pydantic_model__
        else:
            error_builder.add_diagnostic(
                message=f"Stream resolver '{stream_fqn}' input {param.name} must be a list or a DataFrame",
                code="106",
                label="invalid input",
                range=error_builder.function_arg_value_by_name(param.name),
                raise_error=TypeError,
            )
            raise
    else:
        error_builder.add_diagnostic(
            message=f"Unrecognized input argument {param.name} for stream resolver {stream_fqn}",
            code="107",
            label="invalid input",
            range=error_builder.function_arg_value_by_name(param.name),
            raise_error=ValueError,
        )
        raise
    if not (isinstance(input_model_type, type) and is_pydantic_basemodel(input_model_type)):
        error_builder.add_diagnostic(
            message=f"Stream resolver '{stream_fqn}' input {param.name} must take in BaseModel",
            code="108",
            label="invalid input",
            range=error_builder.function_arg_value_by_name(param.name),
            raise_error=ValueError,
        )
    return input_model_type


def _validate_possibly_nested_key(
    *, stream_fqn: str, input_model_type: Type[BaseModel], key_path: str, error_builder: ResolverErrorBuilder
) -> Any:
    """
    Validates that the given key can be used to look up the corresponding `value` in the original model.

    Examples:
    - if `key` is `"user_id"` then `input_model_type` should have a `user_id` field.
    - if `key` is `"user.id"` then `input_model_type` should have a `user` field that has a `id` field

    This functionality is technically unnecessary given the availability of parse functions
    """
    if not isinstance(key_path, str):  # pyright: ignore[reportUnnecessaryIsInstance]
        # The key must be a string.
        error_builder.add_diagnostic(
            message=f"Stream resolver '{stream_fqn}' key '{key_path}' should be type string",
            code="123",
            label="invalid stream resolver key parameter",
            range=error_builder.function_decorator_key_from_dict("keys", key_path),
            raise_error=TypeError,
        )
    if key_path == "":
        error_builder.add_diagnostic(
            message=f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. Key must not be empty.",
            code="124",
            label="invalid stream resolver key parameter",
            range=error_builder.function_decorator_key_from_dict("keys", key_path),
            raise_error=ValueError,
        )
    if "." in key_path:
        if key_path.startswith("."):
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. "
                    f"Key '{key_path}' must not start with a dot '.'"
                ),
                code="125",
                label="invalid stream resolver key parameter",
                range=error_builder.function_decorator_key_from_dict("keys", key_path),
                raise_error=ValueError,
            )
        if key_path.endswith("."):
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. "
                    f"Key '{key_path}' must not start with a dot '.'"
                ),
                code="125",
                label="invalid stream resolver key parameter",
                range=error_builder.function_decorator_key_from_dict("keys", key_path),
                raise_error=ValueError,
            )

        nested_model_type = input_model_type
        # This is a nested key path, which is treated somewhat differently.
        key_path_parts = key_path.split(".")
        for key_path_part_index, key_path_part in enumerate(key_path_parts):
            # If we're not still on the first field in the path, we should explain how we got here to the user:
            explain_current_path = (
                f" (which is the type of '{'.'.join(key_path_parts[:key_path_part_index])}' on input model class '{input_model_type}')"
                if key_path_part_index != 0
                else ""
            )

            if (
                nested_model_type is None
                or nested_model_type is str
                or nested_model_type is bool
                or nested_model_type is int
                or nested_model_type is float
                or nested_model_type is datetime
            ):
                error_builder.add_diagnostic(
                    message=(
                        f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. "
                        f"Key field '{key_path_part}' cannot be looked up in type '{nested_model_type}' because the latter cannot have fields"
                        f"{explain_current_path}"
                    ),
                    code="126",
                    label="invalid stream resolver key parameter",
                    range=error_builder.function_decorator_key_from_dict("keys", key_path),
                    raise_error=ValueError,
                )

            if not is_pydantic_basemodel(nested_model_type):
                # TODO: Alternatively, we can just stop here, and trust that the user knows what they're doing.
                # It won't immediately break anything here, but could cause problems down the line (but so would type-errors in the actual stream).
                error_builder.add_diagnostic(
                    message=(
                        f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. "
                        f"Key field '{key_path_part}' cannot be looked up in type '{nested_model_type}' because the latter is not a Pydantic Model"
                        f"{explain_current_path}"
                    ),
                    code="127",
                    label="invalid stream resolver key parameter",
                    range=error_builder.function_decorator_key_from_dict("keys", key_path),
                    raise_error=ValueError,
                )

            if key_path_part == "":
                error_builder.add_diagnostic(
                    message=(
                        f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. "
                        f"Key '{key_path}' contains an empty key path part"
                    ),
                    code="128",
                    label="invalid stream resolver key parameter",
                    range=error_builder.function_decorator_key_from_dict("keys", key_path),
                    raise_error=ValueError,
                )
            # Otherwise, look it up in the subtype.
            if key_path_part not in nested_model_type.__fields__.keys():
                error_builder.add_diagnostic(
                    message=(
                        f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. "
                        f"Key field '{key_path_part}' is not an attribute in model class '{nested_model_type}'"
                        f"{explain_current_path}"
                    ),
                    code="129",
                    label="invalid stream resolver key parameter",
                    range=error_builder.function_decorator_key_from_dict("keys", key_path),
                    raise_error=ValueError,
                )

            # Now, drill into the nested model type.
            nested_model_field_info = nested_model_type.__fields__[key_path_part]
            if not nested_model_field_info.annotation:
                # We need to have a type annotation to be able to move forward.
                error_builder.add_diagnostic(
                    message=(
                        f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. "
                        f"Key field '{key_path_part}' is not an attribute in model class '{nested_model_type}'"
                        f"{explain_current_path}"
                    ),
                    code="129",
                    label="invalid stream resolver key parameter",
                    range=error_builder.function_decorator_key_from_dict("keys", key_path),
                    raise_error=ValueError,
                )
            nested_model_type = nested_model_field_info.annotation

    else:
        # This is not a nested key path, so the key should exist as a field directly on the model.
        if key_path not in input_model_type.__fields__.keys():
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{stream_fqn}' specifies an invalid 'key' mapping. "
                    f"Key '{key_path}' is not an attribute in input model class '{input_model_type}'"
                ),
                code="129",
                label="invalid stream resolver key parameter",
                range=error_builder.function_decorator_key_from_dict("keys", key_path),
                raise_error=ValueError,
            )


def _validate_keys(
    stream_fn: Callable[P, Any],
    keys: dict[str, Any],
    params: Sequence[StreamResolverParam],
    error_builder: ResolverErrorBuilder,
    name: str | None,
) -> dict[str, Any]:
    stream_fqn = get_resolver_fqn(function=stream_fn, name=name)

    if not isinstance(keys, dict):  # pyright: ignore[reportUnnecessaryIsInstance]
        error_builder.add_diagnostic(
            message=f"Stream resolver '{stream_fqn}' keys parameter must be of type dict",
            code="109",
            label="invalid stream resolver keys parameter",
            range=error_builder.function_decorator_arg_by_name("keys"),
            raise_error=TypeError,
        )
    input_model_arg = next(
        param for param in params if isinstance(param, (StreamResolverParamMessage, StreamResolverParamMessageWindow))
    )
    input_model_type = _get_stream_resolver_input_type(input_model_arg, stream_fqn, error_builder)

    for key, value in keys.items():
        _validate_possibly_nested_key(
            stream_fqn=stream_fqn, input_model_type=input_model_type, key_path=key, error_builder=error_builder
        )

        if not isinstance(value, FeatureWrapper):
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{stream_fqn}' maps key '{key}' to value '{value}', "
                    f"but '{value}' is not of type Feature"
                ),
                code="110",
                label="invalid stream resolver keys parameter",
                range=error_builder.function_decorator_value_from_dict("keys", key),
                raise_error=TypeError,
            )
        value = unwrap_feature(value)
        if not value.is_scalar:
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{stream_fqn}' maps key '{key}' to value '{value}', "
                    f"but '{value}' is not a scalar feature"
                ),
                code="111",
                label="invalid stream resolver keys parameter",
                range=error_builder.function_decorator_value_from_dict("keys", key),
                raise_error=TypeError,
            )
        if value.is_windowed:
            error_builder.add_diagnostic(
                message=(
                    f"Stream resolver '{stream_fqn}' maps key '{key}' to value '{value}', "
                    f"but '{value}' cannot be a windowed feature"
                ),
                code="112",
                label="invalid stream resolver keys parameter",
                range=error_builder.function_decorator_value_from_dict("keys", key),
                raise_error=TypeError,
            )

    return {key: keys[key] for key in sorted(keys.keys())}


def _validate_timestamp(
    stream_fn: Callable[P, Any],
    timestamp: str,
    params: Sequence[StreamResolverParam],
    error_builder: ResolverErrorBuilder,
    name: str | None,
):
    stream_fqn = get_resolver_fqn(function=stream_fn, name=name)
    input_model_arg = next(
        param for param in params if isinstance(param, (StreamResolverParamMessage, StreamResolverParamMessageWindow))
    )
    input_model_type = _get_stream_resolver_input_type(input_model_arg, stream_fqn, error_builder)

    if timestamp not in input_model_type.__fields__.keys():
        error_builder.add_diagnostic(
            message=(
                f"Stream resolver '{stream_fqn}' specifies an invalid 'timestamp' attribute. "
                f"'{timestamp}' is not an attribute of the input model class '{input_model_type}'"
            ),
            code="113",
            label="invalid stream resolver timestamp parameter",
            range=error_builder.function_decorator_arg_by_name("timestamp"),
            raise_error=ValueError,
        )
    model_field = input_model_type.__fields__[timestamp]

    # handling Optional[datetime] and datetime with get_args
    if model_field.annotation != datetime and datetime not in get_args(model_field.annotation):
        error_builder.add_diagnostic(
            message=(
                f"Stream resolver '{stream_fqn}' specifies an invalid 'timestamp' attribute. "
                f"'{timestamp}' field must be of type datetime.datetime. "
                "Use the parse function to convert your timestamp to a zoned (not naive!) datetime."
            ),
            code="114",
            label="invalid stream resolver timestamp parameter",
            range=error_builder.function_decorator_arg_by_name("timestamp"),
            raise_error=TypeError,
        )


def parse_and_register_stream_resolver(
    *,
    caller_globals: Optional[Dict[str, Any]],
    caller_locals: Optional[Dict[str, Any]],
    fn: Callable[P, T],
    source: StreamSource,
    caller_filename: str,
    error_builder: ResolverErrorBuilder,
    mode: Optional[Literal["continuous", "tumbling"]] = None,
    environment: Optional[Environments] = None,
    machine_type: Optional[MachineType] = None,
    message: Optional[Type[Any]] = None,
    sql_query: Optional[str] = None,
    owner: Optional[str] = None,
    parse: Optional[Callable[[T], Any]] = None,
    keys: Optional[Dict[str, Any]] = None,
    timestamp: Optional[str] = None,
    caller_line: Optional[int] = None,
    name: str | None = None,
) -> StreamResolver[P, T]:
    fqn = f"{fn.__module__}.{fn.__name__}"
    annotation_parser = ResolverAnnotationParser(fn, caller_globals, caller_locals, error_builder)
    output_features = _parse_stream_resolver_output_features(
        fn,
        error_builder,
        resolver_fqn_for_errors=fqn,
    )
    flattened_output_features = (
        df.columns
        if len(output_features.features) == 1
        and isinstance(output_features.features[0], type)
        and issubclass(df := output_features.features[0], DataFrame)
        else output_features.features
    )
    is_windowed_resolver = any(x.is_windowed for x in flattened_output_features)
    params = _parse_stream_resolver_params(
        fn,
        error_builder,
        resolver_fqn_for_errors=fqn,
        annotation_parser=annotation_parser,
        is_windowed_resolver=is_windowed_resolver,
    )
    parse_info = None
    if parse:
        parse_info = _validate_parse_function(
            stream_fn=fn,
            parse_fn=parse,
            globals=caller_globals,
            locals=caller_locals,
            params=params,
            resolver_error_builder=error_builder,
            name=name,
        )
    if keys is not None:
        keys = _validate_keys(stream_fn=fn, keys=keys, params=params, error_builder=error_builder, name=name)
    elif keys is None and mode == "continuous":
        error_builder.add_diagnostic(
            message=(
                f"Stream resolver '{fqn}' must take a 'keys' argument in the decorator "
                "if mode is continuous. The 'keys' argument should be dict mapping from "
                "the attribute of the incoming message to the Chalk feature"
            ),
            code="115",
            label="continuous resolvers need a keys parameter",
            range=error_builder.function_decorator(),
            raise_error=ValueError,
        )
    output_feature_fqns = set(f.fqn for f in flattened_output_features)

    signature = StreamResolverSignature(
        params=params,
        output_feature_fqns=output_feature_fqns,
    )
    parsed = parse_function(
        fn,
        caller_globals,
        caller_locals,
        error_builder,
        allow_custom_args=True,
        is_streaming_resolver=True,
        name=name,
    )

    if timestamp:
        _validate_timestamp(stream_fn=fn, timestamp=timestamp, params=params, error_builder=error_builder, name=name)
    for resolver in RESOLVER_REGISTRY.get_stream_resolvers():
        if resolver.source == source:
            if resolver.timestamp != timestamp:
                error_builder.add_diagnostic(
                    message=(
                        f"Stream resolver '{fqn}' specifies 'timestamp' attribute, "
                        f"but stream resolver '{resolver.fqn}' does not or specifies a different attribute. "
                        "Stream resolvers with the same source must all have the same timestamp value"
                    ),
                    code="116",
                    label="Resolver timestamp inconsistency",
                    range=error_builder.function_decorator(),
                    raise_error=ValueError,
                )

    resolver = StreamResolver(
        function_definition=parsed.function_definition,
        fqn=parsed.fqn,
        filename=caller_filename,
        source=source,
        fn=fn,
        tags=None,
        environment=None if environment is None else list(ensure_tuple(environment)),
        doc=parsed.doc,
        mode=mode,
        machine_type=machine_type,
        message=message,
        output=output_features,
        signature=signature,
        state=parsed.state,
        sql_query=None,
        owner=owner,
        parse=parse_info,
        keys=keys,
        timestamp=timestamp,
        source_line=caller_line,
        lsp_builder=error_builder,
    )
    resolver.add_to_registry(override=False)
    return resolver
