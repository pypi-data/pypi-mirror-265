from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class RecomputeSettings(_message.Message):
    __slots__ = ("feature_fqns", "all_features")
    FEATURE_FQNS_FIELD_NUMBER: _ClassVar[int]
    ALL_FEATURES_FIELD_NUMBER: _ClassVar[int]
    feature_fqns: _containers.RepeatedScalarFieldContainer[str]
    all_features: bool
    def __init__(self, feature_fqns: _Optional[_Iterable[str]] = ..., all_features: bool = ...) -> None: ...

class CronQuery(_message.Message):
    __slots__ = (
        "name",
        "cron",
        "file_name",
        "output",
        "max_samples",
        "recompute",
        "lower_bound",
        "upper_bound",
        "tags",
        "required_resolver_tags",
        "store_online",
        "store_offline",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    CRON_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    MAX_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    RECOMPUTE_FIELD_NUMBER: _ClassVar[int]
    LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_RESOLVER_TAGS_FIELD_NUMBER: _ClassVar[int]
    STORE_ONLINE_FIELD_NUMBER: _ClassVar[int]
    STORE_OFFLINE_FIELD_NUMBER: _ClassVar[int]
    name: str
    cron: str
    file_name: str
    output: _containers.RepeatedScalarFieldContainer[str]
    max_samples: int
    recompute: RecomputeSettings
    lower_bound: _timestamp_pb2.Timestamp
    upper_bound: _timestamp_pb2.Timestamp
    tags: _containers.RepeatedScalarFieldContainer[str]
    required_resolver_tags: _containers.RepeatedScalarFieldContainer[str]
    store_online: bool
    store_offline: bool
    def __init__(
        self,
        name: _Optional[str] = ...,
        cron: _Optional[str] = ...,
        file_name: _Optional[str] = ...,
        output: _Optional[_Iterable[str]] = ...,
        max_samples: _Optional[int] = ...,
        recompute: _Optional[_Union[RecomputeSettings, _Mapping]] = ...,
        lower_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        upper_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        required_resolver_tags: _Optional[_Iterable[str]] = ...,
        store_online: bool = ...,
        store_offline: bool = ...,
    ) -> None: ...
