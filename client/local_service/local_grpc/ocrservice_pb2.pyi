from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
file_error: OCRretunStatus
other_error: OCRretunStatus
s3_error: OCRretunStatus
sucess: OCRretunStatus

class OCRrequestBatch(_message.Message):
    __slots__ = ["filename", "httplink", "s3Info"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    HTTPLINK_FIELD_NUMBER: _ClassVar[int]
    S3INFO_FIELD_NUMBER: _ClassVar[int]
    filename: _containers.RepeatedScalarFieldContainer[str]
    httplink: _containers.RepeatedScalarFieldContainer[str]
    s3Info: S3request
    def __init__(self, s3Info: _Optional[_Union[S3request, _Mapping]] = ..., filename: _Optional[_Iterable[str]] = ..., httplink: _Optional[_Iterable[str]] = ...) -> None: ...

class OCRrequestInference(_message.Message):
    __slots__ = ["filename", "httplink", "s3Info"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    HTTPLINK_FIELD_NUMBER: _ClassVar[int]
    S3INFO_FIELD_NUMBER: _ClassVar[int]
    filename: _containers.RepeatedScalarFieldContainer[str]
    httplink: _containers.RepeatedScalarFieldContainer[str]
    s3Info: S3request
    def __init__(self, s3Info: _Optional[_Union[S3request, _Mapping]] = ..., filename: _Optional[_Iterable[str]] = ..., httplink: _Optional[_Iterable[str]] = ...) -> None: ...

class OCRresponse(_message.Message):
    __slots__ = ["data", "status"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    status: OCRretunStatus
    def __init__(self, status: _Optional[_Union[OCRretunStatus, str]] = ..., data: _Optional[bytes] = ...) -> None: ...

class OCRuploadFiles(_message.Message):
    __slots__ = ["data", "filename"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    filename: str
    def __init__(self, filename: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class S3args(_message.Message):
    __slots__ = ["bucketname", "command", "endpoint", "file", "localdir", "prefix"]
    BUCKETNAME_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    LOCALDIR_FIELD_NUMBER: _ClassVar[int]
    PREFIX_FIELD_NUMBER: _ClassVar[int]
    bucketname: str
    command: str
    endpoint: str
    file: str
    localdir: str
    prefix: str
    def __init__(self, endpoint: _Optional[str] = ..., command: _Optional[str] = ..., bucketname: _Optional[str] = ..., file: _Optional[str] = ..., prefix: _Optional[str] = ..., localdir: _Optional[str] = ...) -> None: ...

class S3env(_message.Message):
    __slots__ = ["aws_access_key_id", "aws_secret_access_key"]
    AWS_ACCESS_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    AWS_SECRET_ACCESS_KEY_FIELD_NUMBER: _ClassVar[int]
    aws_access_key_id: str
    aws_secret_access_key: str
    def __init__(self, aws_access_key_id: _Optional[str] = ..., aws_secret_access_key: _Optional[str] = ...) -> None: ...

class S3request(_message.Message):
    __slots__ = ["args", "env"]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    args: S3args
    env: S3env
    def __init__(self, args: _Optional[_Union[S3args, _Mapping]] = ..., env: _Optional[_Union[S3env, _Mapping]] = ...) -> None: ...

class S3response(_message.Message):
    __slots__ = ["files", "request", "status"]
    FILES_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedScalarFieldContainer[str]
    request: S3args
    status: int
    def __init__(self, request: _Optional[_Union[S3args, _Mapping]] = ..., status: _Optional[int] = ..., files: _Optional[_Iterable[str]] = ...) -> None: ...

class OCRretunStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
