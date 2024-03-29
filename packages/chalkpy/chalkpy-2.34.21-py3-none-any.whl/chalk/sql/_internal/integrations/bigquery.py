from __future__ import annotations

import contextlib
import functools
from datetime import date, datetime, time
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, Mapping, Optional, Sequence, cast

import pyarrow as pa

from chalk.clogging import chalk_logger
from chalk.features import Feature
from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.query_execution_parameters import QueryExecutionParameters
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind, validate_dtypes_for_efficient_execution
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from google.cloud.bigquery import ScalarQueryParameterType
    from sqlalchemy.engine import Connection
    from sqlalchemy.engine.url import URL

try:
    import sqlalchemy as sa
except ImportError:
    sa = None

if sa is None:
    _supported_sqlalchemy_types_for_pa_querying = ()
else:
    _supported_sqlalchemy_types_for_pa_querying = (
        sa.BigInteger,
        sa.Boolean,
        sa.BINARY,
        sa.BLOB,
        sa.LargeBinary,
        sa.Float,
        sa.Integer,
        sa.Time,
        sa.String,
        sa.Text,
        sa.VARBINARY,
        sa.DateTime,
        sa.Date,
        sa.SmallInteger,
        sa.BIGINT,
        sa.BOOLEAN,
        sa.CHAR,
        sa.DATETIME,
        sa.FLOAT,
        sa.INTEGER,
        sa.SMALLINT,
        sa.TEXT,
        sa.TIMESTAMP,
        sa.VARCHAR,
    )


_MAX_STATEMENT_LENGTH = 1024 * 1024
"""The actual maximum statement length that bigquery will accept. If the query is much longer than this, then we won't even
get a result from the server. This is likely because they refuse to process a request body this big!"""


def _compile_parameter_to_bq_scalar_type(primitive: Any) -> ScalarQueryParameterType:
    # gated by import check in caller
    from google.cloud.bigquery import SqlParameterScalarTypes

    if isinstance(primitive, bool):
        return SqlParameterScalarTypes.BOOLEAN
    elif isinstance(primitive, int):
        return SqlParameterScalarTypes.INT64
    elif isinstance(primitive, float):
        return SqlParameterScalarTypes.FLOAT64
    elif isinstance(primitive, str):
        return SqlParameterScalarTypes.STRING
    elif isinstance(primitive, datetime):
        return SqlParameterScalarTypes.DATETIME
    elif isinstance(primitive, date):
        return SqlParameterScalarTypes.DATE
    elif isinstance(primitive, Decimal):
        return SqlParameterScalarTypes.DECIMAL
    elif isinstance(primitive, time):
        return SqlParameterScalarTypes.TIME
    elif isinstance(primitive, bytes):
        return SqlParameterScalarTypes.BYTES
    else:
        raise TypeError(f"Unsupported BigQuery parameter type '{type(primitive)}'")


_logger = get_logger(__name__)


class BigQuerySourceImpl(BaseSQLSource):
    kind = SQLSourceKind.bigquery

    def __init__(
        self,
        *,
        name: Optional[str] = None,
        project: Optional[str] = None,
        dataset: Optional[str] = None,
        location: Optional[str] = None,
        credentials_base64: Optional[str] = None,
        credentials_path: Optional[str] = None,
        engine_args: Optional[Dict[str, Any]] = None,
    ):
        try:
            import sqlalchemy_bigquery
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[bigquery]")
        del sqlalchemy_bigquery  # unused
        if engine_args is None:
            engine_args = {}
        engine_args.setdefault("pool_size", 20)
        engine_args.setdefault("max_overflow", 60)
        self.location = location or load_integration_variable(integration_name=name, name="BQ_LOCATION")
        self.dataset = dataset or load_integration_variable(integration_name=name, name="BQ_DATASET")
        self.project = project or load_integration_variable(integration_name=name, name="BQ_PROJECT")
        self.credentials_base64 = credentials_base64 or load_integration_variable(
            integration_name=name, name="BQ_CREDENTIALS_BASE64"
        )
        self.credentials_path = credentials_path or load_integration_variable(
            integration_name=name, name="BQ_CREDENTIALS_PATH"
        )
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args={})

    @functools.cached_property
    def bigquery_read_client(self):
        import google.cloud.bigquery_storage

        with self._get_bq_client() as client:
            return google.cloud.bigquery_storage.BigQueryReadClient(
                credentials=client._credentials  # pyright: ignore[reportPrivateUsage]
            )

    def get_sqlglot_dialect(self) -> str | None:
        return "bigquery"

    def compile_query(
        self,
        finalized_query: FinalizedChalkQuery,
        paramstyle: Optional[str] = None,
        use_sqlglot: bool = False,
    ) -> tuple[str, Sequence[Any], Dict[str, Any]]:
        if use_sqlglot:
            compiled_query = self._get_compiled_query(finalized_query, paramstyle)
            query_string = compiled_query.string

            import sqlglot.expressions
            from sqlglot import parse_one

            ast = parse_one(query_string, read=self.get_sqlglot_dialect())
            for placeholder in list(ast.find_all(sqlglot.expressions.Placeholder)):
                if isinstance(placeholder.this, str) and placeholder.this in compiled_query.params:
                    # Convert placeholders to use @ syntax
                    # https://cloud.google.com/bigquery/docs/parameterized-queries
                    placeholder.replace(sqlglot.expressions.var("@" + placeholder.this))
            updated_query_string = ast.sql(dialect="bigquery")

            return updated_query_string, compiled_query.positiontup, compiled_query.params
        else:
            if paramstyle is not None:
                raise ValueError("Bigquery does not support custom param styles")
            import google.cloud.bigquery
            import google.cloud.bigquery.dbapi
            import google.cloud.bigquery.dbapi._helpers
            import google.cloud.bigquery.dbapi.cursor
            from sqlalchemy_bigquery.base import BigQueryCompiler

            dialect = self.get_engine().dialect
            Compiler = cast("type[BigQueryCompiler]", self.get_engine().dialect.statement_compiler)

            compiled_stmt = Compiler(dialect, finalized_query.query)
            operation = compiled_stmt.string
            parameters = compiled_stmt.params
            (
                formatted_operation,
                parameter_types,
            ) = google.cloud.bigquery.dbapi.cursor._format_operation(  # pyright: ignore[reportPrivateUsage]
                operation, parameters
            )
            if len(formatted_operation) > _MAX_STATEMENT_LENGTH:
                raise ValueError("Query string is too large. Max supported size is 1MB.")
            # The DB-API uses the pyformat formatting, since the way BigQuery does
            # query parameters was not one of the standard options. Convert both
            # the query and the parameters to the format expected by the client
            # libraries.
            query_parameters = google.cloud.bigquery.dbapi._helpers.to_query_parameters(parameters, parameter_types)
            return formatted_operation, query_parameters, {}

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        query = {
            k: v
            for k, v in {
                "location": self.location,
                "credentials_base64": self.credentials_base64,
                "credentials_path": self.credentials_path,
            }.items()
            if v is not None
        }
        return URL.create(drivername="bigquery", host=self.project, database=self.dataset, query=query)

    @contextlib.contextmanager
    def _get_bq_client(self):
        # gated already
        import google.cloud.bigquery
        import google.cloud.bigquery.dbapi

        with self.get_engine().connect() as conn:
            dbapi = conn.connection.dbapi_connection
            assert isinstance(dbapi, google.cloud.bigquery.dbapi.Connection)
            client = dbapi._client  # pyright: ignore[reportPrivateUsage]
            assert isinstance(client, google.cloud.bigquery.Client)
            try:
                yield client
            finally:
                client.close()

    def _postprocess_table(
        self,
        features: Mapping[str, Feature],
        table: pa.RecordBatch,
    ):
        columns: list[pa.Array] = []
        column_names: list[str] = []

        for col_name, feature in features.items():
            column = table.column(col_name)
            expected_type = feature.converter.pyarrow_dtype
            if column.type != expected_type:
                column = column.cast(expected_type)
            if isinstance(column, pa.ChunkedArray):
                column = column.combine_chunks()
            columns.append(column)
            column_names.append(feature.root_fqn)
        return pa.RecordBatch.from_arrays(arrays=columns, names=column_names)

    def _execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        try:
            import google.cloud.bigquery
            import google.cloud.bigquery._pandas_helpers
            from sqlalchemy.sql import Select
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[bigquery]")

        if isinstance(finalized_query.query, Select):
            validate_dtypes_for_efficient_execution(finalized_query.query, _supported_sqlalchemy_types_for_pa_querying)

        assert len(finalized_query.temp_tables) == 0, "Should not create temp tables with bigquery source"

        client: google.cloud.bigquery.Client
        with self._get_bq_client() as client:
            chalk_logger.info("Starting to execute BigQuery query")

            formatted_op, positional_params, named_params = self.compile_query(finalized_query)
            if named_params:
                positional_params = [
                    # TODO: Consider type_ parameter more carefully.
                    google.cloud.bigquery.ScalarQueryParameter(
                        name=name, value=value, type_=_compile_parameter_to_bq_scalar_type(value)
                    )
                    for name, value in named_params.items()
                ]

            job_config = google.cloud.bigquery.QueryJobConfig(
                priority="INTERACTIVE",
                query_parameters=positional_params or [],
            )

            res = client.query(formatted_op, job_config=job_config).result()
            yielded = False

            for table in res.to_arrow_iterable(bqstorage_client=self.bigquery_read_client):
                assert isinstance(table, pa.RecordBatch)
                chalk_logger.info(f"Loaded table from Bigquery with {table.nbytes=}, {table.num_rows=}")
                features = columns_to_features(table.schema.names)
                yield self._postprocess_table(features, table)
                yielded = True
            if not yielded and query_execution_parameters.yield_empty_batches:
                # Copied from https://github.com/googleapis/python-bigquery/blob/89dfcb6469d22e78003a70371a0938a6856e033c/google/cloud/bigquery/table.py#L1954
                arrow_schema = google.cloud.bigquery._pandas_helpers.bq_to_arrow_schema(
                    res._schema  # pyright: ignore[reportPrivateUsage]
                )
                if arrow_schema is not None:
                    features = columns_to_features(arrow_schema.names)
                    yield self._postprocess_table(
                        features, pa.RecordBatch.from_pydict({k: [] for k in arrow_schema.names}, schema=arrow_schema)
                    )

    @classmethod
    def register_sqlalchemy_compiler_overrides(cls):
        try:
            from chalk.sql._internal.integrations.bigquery_compiler_overrides import register_bigquery_compiler_hooks
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[bigquery]")

        register_bigquery_compiler_hooks()
