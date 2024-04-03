"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ..common.types import base_types_pb2 as common_dot_types_dot_base__types__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17board/board_types.proto\x12\x11kiapi.board.types\x1a\x19google/protobuf/any.proto\x1a\x1dcommon/types/base_types.proto"\x18\n\x07NetCode\x12\r\n\x05value\x18\x01 \x01(\x05"=\n\x03Net\x12(\n\x04code\x18\x01 \x01(\x0b2\x1a.kiapi.board.types.NetCode\x12\x0c\n\x04name\x18\x02 \x01(\t"\xb0\x02\n\x05Track\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x12*\n\x05start\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12(\n\x03end\x18\x03 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12+\n\x05width\x18\x04 \x01(\x0b2\x1c.kiapi.common.types.Distance\x12/\n\x06locked\x18\x05 \x01(\x0e2\x1f.kiapi.common.types.LockedState\x12(\n\x05layer\x18\x06 \x01(\x0b2\x19.kiapi.common.types.Layer\x12#\n\x03net\x18\x07 \x01(\x0b2\x16.kiapi.board.types.Net"\xd8\x02\n\x03Arc\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x12*\n\x05start\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12(\n\x03mid\x18\x03 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12(\n\x03end\x18\x04 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12+\n\x05width\x18\x05 \x01(\x0b2\x1c.kiapi.common.types.Distance\x12/\n\x06locked\x18\x06 \x01(\x0e2\x1f.kiapi.common.types.LockedState\x12(\n\x05layer\x18\x07 \x01(\x0b2\x19.kiapi.common.types.Layer\x12#\n\x03net\x18\x08 \x01(\x0b2\x16.kiapi.board.types.Net"f\n\x14ChamferedRectCorners\x12\x10\n\x08top_left\x18\x01 \x01(\x08\x12\x11\n\ttop_right\x18\x02 \x01(\x08\x12\x13\n\x0bbottom_left\x18\x03 \x01(\x08\x12\x14\n\x0cbottom_right\x18\x04 \x01(\x08"\xc8\x02\n\rPadStackLayer\x12)\n\x06layers\x18\x01 \x03(\x0b2\x19.kiapi.common.types.Layer\x12/\n\x05shape\x18\x02 \x01(\x0e2 .kiapi.board.types.PadStackShape\x12)\n\x04size\x18\x03 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12\x1d\n\x15corner_rounding_ratio\x18\x04 \x01(\x02\x12\x15\n\rchamfer_ratio\x18\x05 \x01(\x02\x12B\n\x11chamfered_corners\x18\x06 \x01(\x0b2\'.kiapi.board.types.ChamferedRectCorners\x126\n\rcustom_shapes\x18\x07 \x03(\x0b2\x1f.kiapi.board.types.GraphicShape"\xf7\x02\n\x08PadStack\x12-\n\x04type\x18\x01 \x01(\x0e2\x1f.kiapi.board.types.PadStackType\x12.\n\x0bstart_layer\x18\x02 \x01(\x0b2\x19.kiapi.common.types.Layer\x12,\n\tend_layer\x18\x03 \x01(\x0b2\x19.kiapi.common.types.Layer\x12M\n\x19unconnected_layer_removal\x18\x04 \x01(\x0e2*.kiapi.board.types.UnconnectedLayerRemoval\x123\n\x0edrill_diameter\x18\x05 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x120\n\x06layers\x18\x06 \x03(\x0b2 .kiapi.board.types.PadStackLayer\x12(\n\x05angle\x18\x07 \x01(\x0b2\x19.kiapi.common.types.Angle"\xe0\x01\n\x03Via\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x12-\n\x08position\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12.\n\tpad_stack\x18\x03 \x01(\x0b2\x1b.kiapi.board.types.PadStack\x12/\n\x06locked\x18\x04 \x01(\x0e2\x1f.kiapi.common.types.LockedState\x12#\n\x03net\x18\x05 \x01(\x0b2\x16.kiapi.board.types.Net"p\n\x18GraphicSegmentAttributes\x12*\n\x05start\x18\x01 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12(\n\x03end\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2"~\n\x1aGraphicRectangleAttributes\x12-\n\x08top_left\x18\x01 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x121\n\x0cbottom_right\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2"\x96\x01\n\x14GraphicArcAttributes\x12*\n\x05start\x18\x01 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12(\n\x03mid\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12(\n\x03end\x18\x03 \x01(\x0b2\x1b.kiapi.common.types.Vector2"t\n\x17GraphicCircleAttributes\x12+\n\x06center\x18\x01 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12,\n\x06radius\x18\x02 \x01(\x0b2\x1c.kiapi.common.types.Distance"\xcd\x01\n\x17GraphicBezierAttributes\x12*\n\x05start\x18\x01 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12-\n\x08control1\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12-\n\x08control2\x18\x03 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12(\n\x03end\x18\x04 \x01(\x0b2\x1b.kiapi.common.types.Vector2"\xe3\x04\n\x0cGraphicShape\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x12/\n\x06locked\x18\x02 \x01(\x0e2\x1f.kiapi.common.types.LockedState\x12(\n\x05layer\x18\x03 \x01(\x0b2\x19.kiapi.common.types.Layer\x12#\n\x03net\x18\x04 \x01(\x0b2\x16.kiapi.board.types.Net\x129\n\nattributes\x18\x05 \x01(\x0b2%.kiapi.common.types.GraphicAttributes\x12>\n\x07segment\x18\x06 \x01(\x0b2+.kiapi.board.types.GraphicSegmentAttributesH\x00\x12B\n\trectangle\x18\x07 \x01(\x0b2-.kiapi.board.types.GraphicRectangleAttributesH\x00\x126\n\x03arc\x18\x08 \x01(\x0b2\'.kiapi.board.types.GraphicArcAttributesH\x00\x12<\n\x06circle\x18\t \x01(\x0b2*.kiapi.board.types.GraphicCircleAttributesH\x00\x12.\n\x07polygon\x18\n \x01(\x0b2\x1b.kiapi.common.types.PolySetH\x00\x12<\n\x06bezier\x18\x0b \x01(\x0b2*.kiapi.board.types.GraphicBezierAttributesH\x00B\n\n\x08geometry".\n\x04Text\x12&\n\x04text\x18\x01 \x01(\x0b2\x18.kiapi.common.types.Text"\x9a\x02\n\x03Pad\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x12/\n\x06locked\x18\x02 \x01(\x0e2\x1f.kiapi.common.types.LockedState\x12\x0e\n\x06number\x18\x03 \x01(\t\x12#\n\x03net\x18\x04 \x01(\x0b2\x16.kiapi.board.types.Net\x12(\n\x04type\x18\x05 \x01(\x0e2\x1a.kiapi.board.types.PadType\x12.\n\tpad_stack\x18\x06 \x01(\x0b2\x1b.kiapi.board.types.PadStack\x12-\n\x08position\x18\x07 \x01(\x0b2\x1b.kiapi.common.types.Vector2"\x06\n\x04Zone"\x0b\n\tDimension"\x10\n\x0eReferenceImage"\x07\n\x05Group"\x15\n\x07FieldId\x12\n\n\x02id\x18\x01 \x01(\x05"d\n\x05Field\x12&\n\x02id\x18\x01 \x01(\x0b2\x1a.kiapi.board.types.FieldId\x12\x0c\n\x04name\x18\x02 \x01(\t\x12%\n\x04text\x18\x03 \x01(\x0b2\x17.kiapi.board.types.Text"\t\n\x07Model3D"\xaa\x02\n\x13FootprintAttributes\x12\x13\n\x0bdescription\x18\x01 \x01(\t\x12\x10\n\x08keywords\x18\x02 \x01(\t\x12\x18\n\x10not_in_schematic\x18\x03 \x01(\x08\x12#\n\x1bexclude_from_position_files\x18\x04 \x01(\x08\x12&\n\x1eexclude_from_bill_of_materials\x18\x05 \x01(\x08\x12)\n!exempt_from_courtyard_requirement\x18\x06 \x01(\x08\x12\x17\n\x0fdo_not_populate\x18\x07 \x01(\x08\x12A\n\x0emounting_style\x18\x08 \x01(\x0e2).kiapi.board.types.FootprintMountingStyle"\x9f\x02\n\x13DesignRuleOverrides\x12/\n\tclearance\x18\x01 \x01(\x0b2\x1c.kiapi.common.types.Distance\x128\n\x12solder_mask_margin\x18\x02 \x01(\x0b2\x1c.kiapi.common.types.Distance\x129\n\x13solder_paste_margin\x18\x03 \x01(\x0b2\x1c.kiapi.common.types.Distance\x12!\n\x19solder_paste_margin_ratio\x18\x04 \x01(\x01\x12?\n\x0fzone_connection\x18\x05 \x01(\x0e2&.kiapi.board.types.ZoneConnectionStyle"&\n\x10NetTieDefinition\x12\x12\n\npad_number\x18\x01 \x03(\t"\xbb\x04\n\tFootprint\x121\n\x02id\x18\x01 \x01(\x0b2%.kiapi.common.types.LibraryIdentifier\x12+\n\x06anchor\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12:\n\nattributes\x18\x03 \x01(\x0b2&.kiapi.board.types.FootprintAttributes\x129\n\toverrides\x18\x04 \x01(\x0b2&.kiapi.board.types.DesignRuleOverrides\x125\n\x08net_ties\x18\x05 \x03(\x0b2#.kiapi.board.types.NetTieDefinition\x121\n\x0eprivate_layers\x18\x06 \x03(\x0b2\x19.kiapi.common.types.Layer\x121\n\x0freference_field\x18\x07 \x01(\x0b2\x18.kiapi.board.types.Field\x12-\n\x0bvalue_field\x18\x08 \x01(\x0b2\x18.kiapi.board.types.Field\x121\n\x0fdatasheet_field\x18\t \x01(\x0b2\x18.kiapi.board.types.Field\x123\n\x11description_field\x18\n \x01(\x0b2\x18.kiapi.board.types.Field\x12#\n\x05items\x18\x0b \x03(\x0b2\x14.google.protobuf.Any"\xe6\x04\n\x11FootprintInstance\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x12-\n\x08position\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12.\n\x0borientation\x18\x03 \x01(\x0b2\x19.kiapi.common.types.Angle\x12(\n\x05layer\x18\x04 \x01(\x0b2\x19.kiapi.common.types.Layer\x12/\n\x06locked\x18\x05 \x01(\x0e2\x1f.kiapi.common.types.LockedState\x120\n\ndefinition\x18\x06 \x01(\x0b2\x1c.kiapi.board.types.Footprint\x121\n\x0freference_field\x18\x07 \x01(\x0b2\x18.kiapi.board.types.Field\x12-\n\x0bvalue_field\x18\x08 \x01(\x0b2\x18.kiapi.board.types.Field\x121\n\x0fdatasheet_field\x18\t \x01(\x0b2\x18.kiapi.board.types.Field\x123\n\x11description_field\x18\n \x01(\x0b2\x18.kiapi.board.types.Field\x12:\n\nattributes\x18\x0b \x01(\x0b2&.kiapi.board.types.FootprintAttributes\x129\n\toverrides\x18\x0c \x01(\x0b2&.kiapi.board.types.DesignRuleOverrides*F\n\x0cPadStackType\x12\x0f\n\x0bPST_UNKNOWN\x10\x00\x12\x0f\n\x0bPST_THROUGH\x10\x01\x12\x14\n\x10PST_BLIND_BURIED\x10\x02*m\n\x17UnconnectedLayerRemoval\x12\x0f\n\x0bULR_UNKNOWN\x10\x00\x12\x0c\n\x08ULR_KEEP\x10\x01\x12\x0e\n\nULR_REMOVE\x10\x02\x12#\n\x1fULR_REMOVE_EXCEPT_START_AND_END\x10\x03*\x9e\x01\n\rPadStackShape\x12\x0f\n\x0bPSS_UNKNOWN\x10\x00\x12\x0e\n\nPSS_CIRCLE\x10\x01\x12\x11\n\rPSS_RECTANGLE\x10\x02\x12\x0c\n\x08PSS_OVAL\x10\x03\x12\x11\n\rPSS_TRAPEZOID\x10\x04\x12\x11\n\rPSS_ROUNDRECT\x10\x05\x12\x15\n\x11PSS_CHAMFEREDRECT\x10\x06\x12\x0e\n\nPSS_CUSTOM\x10\x07*U\n\x07PadType\x12\x0e\n\nPT_UNKNOWN\x10\x00\x12\n\n\x06PT_PTH\x10\x01\x12\n\n\x06PT_SMD\x10\x02\x12\x15\n\x11PT_EDGE_CONNECTOR\x10\x03\x12\x0b\n\x07PT_NPTH\x10\x04*a\n\x16FootprintMountingStyle\x12\x0f\n\x0bFMS_UNKNOWN\x10\x00\x12\x14\n\x10FMS_THROUGH_HOLE\x10\x01\x12\x0b\n\x07FMS_SMD\x10\x02\x12\x13\n\x0fFMS_UNSPECIFIED\x10\x03*{\n\x13ZoneConnectionStyle\x12\x0f\n\x0bZCS_UNKNOWN\x10\x00\x12\x11\n\rZCS_INHERITED\x10\x01\x12\x0c\n\x08ZCS_NONE\x10\x02\x12\x0f\n\x0bZCS_THERMAL\x10\x03\x12\x0c\n\x08ZCS_FULL\x10\x04\x12\x13\n\x0fZCS_PTH_THERMAL\x10\x05b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'board.board_types_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_PADSTACKTYPE']._serialized_start = 5561
    _globals['_PADSTACKTYPE']._serialized_end = 5631
    _globals['_UNCONNECTEDLAYERREMOVAL']._serialized_start = 5633
    _globals['_UNCONNECTEDLAYERREMOVAL']._serialized_end = 5742
    _globals['_PADSTACKSHAPE']._serialized_start = 5745
    _globals['_PADSTACKSHAPE']._serialized_end = 5903
    _globals['_PADTYPE']._serialized_start = 5905
    _globals['_PADTYPE']._serialized_end = 5990
    _globals['_FOOTPRINTMOUNTINGSTYLE']._serialized_start = 5992
    _globals['_FOOTPRINTMOUNTINGSTYLE']._serialized_end = 6089
    _globals['_ZONECONNECTIONSTYLE']._serialized_start = 6091
    _globals['_ZONECONNECTIONSTYLE']._serialized_end = 6214
    _globals['_NETCODE']._serialized_start = 104
    _globals['_NETCODE']._serialized_end = 128
    _globals['_NET']._serialized_start = 130
    _globals['_NET']._serialized_end = 191
    _globals['_TRACK']._serialized_start = 194
    _globals['_TRACK']._serialized_end = 498
    _globals['_ARC']._serialized_start = 501
    _globals['_ARC']._serialized_end = 845
    _globals['_CHAMFEREDRECTCORNERS']._serialized_start = 847
    _globals['_CHAMFEREDRECTCORNERS']._serialized_end = 949
    _globals['_PADSTACKLAYER']._serialized_start = 952
    _globals['_PADSTACKLAYER']._serialized_end = 1280
    _globals['_PADSTACK']._serialized_start = 1283
    _globals['_PADSTACK']._serialized_end = 1658
    _globals['_VIA']._serialized_start = 1661
    _globals['_VIA']._serialized_end = 1885
    _globals['_GRAPHICSEGMENTATTRIBUTES']._serialized_start = 1887
    _globals['_GRAPHICSEGMENTATTRIBUTES']._serialized_end = 1999
    _globals['_GRAPHICRECTANGLEATTRIBUTES']._serialized_start = 2001
    _globals['_GRAPHICRECTANGLEATTRIBUTES']._serialized_end = 2127
    _globals['_GRAPHICARCATTRIBUTES']._serialized_start = 2130
    _globals['_GRAPHICARCATTRIBUTES']._serialized_end = 2280
    _globals['_GRAPHICCIRCLEATTRIBUTES']._serialized_start = 2282
    _globals['_GRAPHICCIRCLEATTRIBUTES']._serialized_end = 2398
    _globals['_GRAPHICBEZIERATTRIBUTES']._serialized_start = 2401
    _globals['_GRAPHICBEZIERATTRIBUTES']._serialized_end = 2606
    _globals['_GRAPHICSHAPE']._serialized_start = 2609
    _globals['_GRAPHICSHAPE']._serialized_end = 3220
    _globals['_TEXT']._serialized_start = 3222
    _globals['_TEXT']._serialized_end = 3268
    _globals['_PAD']._serialized_start = 3271
    _globals['_PAD']._serialized_end = 3553
    _globals['_ZONE']._serialized_start = 3555
    _globals['_ZONE']._serialized_end = 3561
    _globals['_DIMENSION']._serialized_start = 3563
    _globals['_DIMENSION']._serialized_end = 3574
    _globals['_REFERENCEIMAGE']._serialized_start = 3576
    _globals['_REFERENCEIMAGE']._serialized_end = 3592
    _globals['_GROUP']._serialized_start = 3594
    _globals['_GROUP']._serialized_end = 3601
    _globals['_FIELDID']._serialized_start = 3603
    _globals['_FIELDID']._serialized_end = 3624
    _globals['_FIELD']._serialized_start = 3626
    _globals['_FIELD']._serialized_end = 3726
    _globals['_MODEL3D']._serialized_start = 3728
    _globals['_MODEL3D']._serialized_end = 3737
    _globals['_FOOTPRINTATTRIBUTES']._serialized_start = 3740
    _globals['_FOOTPRINTATTRIBUTES']._serialized_end = 4038
    _globals['_DESIGNRULEOVERRIDES']._serialized_start = 4041
    _globals['_DESIGNRULEOVERRIDES']._serialized_end = 4328
    _globals['_NETTIEDEFINITION']._serialized_start = 4330
    _globals['_NETTIEDEFINITION']._serialized_end = 4368
    _globals['_FOOTPRINT']._serialized_start = 4371
    _globals['_FOOTPRINT']._serialized_end = 4942
    _globals['_FOOTPRINTINSTANCE']._serialized_start = 4945
    _globals['_FOOTPRINTINSTANCE']._serialized_end = 5559