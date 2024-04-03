"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ..common.types import base_types_pb2 as common_dot_types_dot_base__types__pb2
from ..board import board_pb2 as board_dot_board__pb2
from ..board import board_types_pb2 as board_dot_board__types__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1aboard/board_commands.proto\x12\x14kiapi.board.commands\x1a\x1dcommon/types/base_types.proto\x1a\x11board/board.proto\x1a\x17board/board_types.proto"G\n\x0fGetBoardStackup\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier"B\n\x14BoardStackupResponse\x12*\n\x07stackup\x18\x01 \x01(\x0b2\x19.kiapi.board.BoardStackup"v\n\x12UpdateBoardStackup\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier\x12*\n\x07stackup\x18\x02 \x01(\x0b2\x19.kiapi.board.BoardStackup"K\n\x13GetGraphicsDefaults\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier"K\n\x18GraphicsDefaultsResponse\x12/\n\x08defaults\x18\x01 \x01(\x0b2\x1d.kiapi.board.GraphicsDefaults"X\n\x07GetNets\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier\x12\x17\n\x0fnetclass_filter\x18\x02 \x03(\t"4\n\x0cNetsResponse\x12$\n\x04nets\x18\x01 \x03(\x0b2\x16.kiapi.board.types.Net"\x9b\x01\n\rGetItemsByNet\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x12+\n\x05types\x18\x02 \x03(\x0b2\x1c.kiapi.common.types.ItemType\x12-\n\tnet_codes\x18\x03 \x03(\x0b2\x1a.kiapi.board.types.NetCode"\x86\x01\n\x12GetItemsByNetClass\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x12+\n\x05types\x18\x02 \x03(\x0b2\x1c.kiapi.common.types.ItemType\x12\x13\n\x0bnet_classes\x18\x03 \x03(\t"7\n\x0eGetTextExtents\x12%\n\x04text\x18\x01 \x01(\x0b2\x17.kiapi.board.types.Text"u\n\x14InteractiveMoveItems\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier\x12\'\n\x05items\x18\x02 \x03(\x0b2\x18.kiapi.common.types.KIIDb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'board.board_commands_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_GETBOARDSTACKUP']._serialized_start = 127
    _globals['_GETBOARDSTACKUP']._serialized_end = 198
    _globals['_BOARDSTACKUPRESPONSE']._serialized_start = 200
    _globals['_BOARDSTACKUPRESPONSE']._serialized_end = 266
    _globals['_UPDATEBOARDSTACKUP']._serialized_start = 268
    _globals['_UPDATEBOARDSTACKUP']._serialized_end = 386
    _globals['_GETGRAPHICSDEFAULTS']._serialized_start = 388
    _globals['_GETGRAPHICSDEFAULTS']._serialized_end = 463
    _globals['_GRAPHICSDEFAULTSRESPONSE']._serialized_start = 465
    _globals['_GRAPHICSDEFAULTSRESPONSE']._serialized_end = 540
    _globals['_GETNETS']._serialized_start = 542
    _globals['_GETNETS']._serialized_end = 630
    _globals['_NETSRESPONSE']._serialized_start = 632
    _globals['_NETSRESPONSE']._serialized_end = 684
    _globals['_GETITEMSBYNET']._serialized_start = 687
    _globals['_GETITEMSBYNET']._serialized_end = 842
    _globals['_GETITEMSBYNETCLASS']._serialized_start = 845
    _globals['_GETITEMSBYNETCLASS']._serialized_end = 979
    _globals['_GETTEXTEXTENTS']._serialized_start = 981
    _globals['_GETTEXTEXTENTS']._serialized_end = 1036
    _globals['_INTERACTIVEMOVEITEMS']._serialized_start = 1038
    _globals['_INTERACTIVEMOVEITEMS']._serialized_end = 1155