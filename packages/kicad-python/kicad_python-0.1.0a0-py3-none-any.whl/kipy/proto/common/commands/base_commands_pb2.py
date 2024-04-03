"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...common.types import base_types_pb2 as common_dot_types_dot_base__types__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#common/commands/base_commands.proto\x12\x15kiapi.common.commands\x1a\x1dcommon/types/base_types.proto"\x0c\n\nGetVersion"G\n\x12GetVersionResponse\x121\n\x07version\x18\x01 \x01(\x0b2 .kiapi.common.types.KiCadVersionb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'common.commands.base_commands_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_GETVERSION']._serialized_start = 93
    _globals['_GETVERSION']._serialized_end = 105
    _globals['_GETVERSIONRESPONSE']._serialized_start = 107
    _globals['_GETVERSIONRESPONSE']._serialized_end = 178