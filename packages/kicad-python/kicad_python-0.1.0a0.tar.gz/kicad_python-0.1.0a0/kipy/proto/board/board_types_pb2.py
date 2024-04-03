"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ..common.types import base_types_pb2 as common_dot_types_dot_base__types__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17board/board_types.proto\x12\x11kiapi.board.types\x1a\x19google/protobuf/any.proto\x1a\x1dcommon/types/base_types.proto"\x18\n\x07NetCode\x12\r\n\x05value\x18\x01 \x01(\x05"=\n\x03Net\x12(\n\x04code\x18\x01 \x01(\x0b2\x1a.kiapi.board.types.NetCode\x12\x0c\n\x04name\x18\x02 \x01(\t"\xb4\x02\n\x05Track\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x12*\n\x05start\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12(\n\x03end\x18\x03 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12+\n\x05width\x18\x04 \x01(\x0b2\x1c.kiapi.common.types.Distance\x12/\n\x06locked\x18\x05 \x01(\x0e2\x1f.kiapi.common.types.LockedState\x12,\n\x05layer\x18\x06 \x01(\x0e2\x1d.kiapi.board.types.BoardLayer\x12#\n\x03net\x18\x07 \x01(\x0b2\x16.kiapi.board.types.Net"\xdc\x02\n\x03Arc\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x12*\n\x05start\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12(\n\x03mid\x18\x03 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12(\n\x03end\x18\x04 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12+\n\x05width\x18\x05 \x01(\x0b2\x1c.kiapi.common.types.Distance\x12/\n\x06locked\x18\x06 \x01(\x0e2\x1f.kiapi.common.types.LockedState\x12,\n\x05layer\x18\x07 \x01(\x0e2\x1d.kiapi.board.types.BoardLayer\x12#\n\x03net\x18\x08 \x01(\x0b2\x16.kiapi.board.types.Net"f\n\x14ChamferedRectCorners\x12\x10\n\x08top_left\x18\x01 \x01(\x08\x12\x11\n\ttop_right\x18\x02 \x01(\x08\x12\x13\n\x0bbottom_left\x18\x03 \x01(\x08\x12\x14\n\x0cbottom_right\x18\x04 \x01(\x08"\xcc\x02\n\rPadStackLayer\x12-\n\x06layers\x18\x01 \x03(\x0e2\x1d.kiapi.board.types.BoardLayer\x12/\n\x05shape\x18\x02 \x01(\x0e2 .kiapi.board.types.PadStackShape\x12)\n\x04size\x18\x03 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12\x1d\n\x15corner_rounding_ratio\x18\x04 \x01(\x02\x12\x15\n\rchamfer_ratio\x18\x05 \x01(\x02\x12B\n\x11chamfered_corners\x18\x06 \x01(\x0b2\'.kiapi.board.types.ChamferedRectCorners\x126\n\rcustom_shapes\x18\x07 \x03(\x0b2\x1f.kiapi.board.types.GraphicShape"\xff\x02\n\x08PadStack\x12-\n\x04type\x18\x01 \x01(\x0e2\x1f.kiapi.board.types.PadStackType\x122\n\x0bstart_layer\x18\x02 \x01(\x0e2\x1d.kiapi.board.types.BoardLayer\x120\n\tend_layer\x18\x03 \x01(\x0e2\x1d.kiapi.board.types.BoardLayer\x12M\n\x19unconnected_layer_removal\x18\x04 \x01(\x0e2*.kiapi.board.types.UnconnectedLayerRemoval\x123\n\x0edrill_diameter\x18\x05 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x120\n\x06layers\x18\x06 \x03(\x0b2 .kiapi.board.types.PadStackLayer\x12(\n\x05angle\x18\x07 \x01(\x0b2\x19.kiapi.common.types.Angle"\xe0\x01\n\x03Via\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x12-\n\x08position\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12.\n\tpad_stack\x18\x03 \x01(\x0b2\x1b.kiapi.board.types.PadStack\x12/\n\x06locked\x18\x04 \x01(\x0e2\x1f.kiapi.common.types.LockedState\x12#\n\x03net\x18\x05 \x01(\x0b2\x16.kiapi.board.types.Net"p\n\x18GraphicSegmentAttributes\x12*\n\x05start\x18\x01 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12(\n\x03end\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2"~\n\x1aGraphicRectangleAttributes\x12-\n\x08top_left\x18\x01 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x121\n\x0cbottom_right\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2"\x96\x01\n\x14GraphicArcAttributes\x12*\n\x05start\x18\x01 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12(\n\x03mid\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12(\n\x03end\x18\x03 \x01(\x0b2\x1b.kiapi.common.types.Vector2"y\n\x17GraphicCircleAttributes\x12+\n\x06center\x18\x01 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x121\n\x0cradius_point\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2"\xcd\x01\n\x17GraphicBezierAttributes\x12*\n\x05start\x18\x01 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12-\n\x08control1\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12-\n\x08control2\x18\x03 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12(\n\x03end\x18\x04 \x01(\x0b2\x1b.kiapi.common.types.Vector2"\xe7\x04\n\x0cGraphicShape\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x12/\n\x06locked\x18\x02 \x01(\x0e2\x1f.kiapi.common.types.LockedState\x12,\n\x05layer\x18\x03 \x01(\x0e2\x1d.kiapi.board.types.BoardLayer\x12#\n\x03net\x18\x04 \x01(\x0b2\x16.kiapi.board.types.Net\x129\n\nattributes\x18\x05 \x01(\x0b2%.kiapi.common.types.GraphicAttributes\x12>\n\x07segment\x18\x06 \x01(\x0b2+.kiapi.board.types.GraphicSegmentAttributesH\x00\x12B\n\trectangle\x18\x07 \x01(\x0b2-.kiapi.board.types.GraphicRectangleAttributesH\x00\x126\n\x03arc\x18\x08 \x01(\x0b2\'.kiapi.board.types.GraphicArcAttributesH\x00\x12<\n\x06circle\x18\t \x01(\x0b2*.kiapi.board.types.GraphicCircleAttributesH\x00\x12.\n\x07polygon\x18\n \x01(\x0b2\x1b.kiapi.common.types.PolySetH\x00\x12<\n\x06bezier\x18\x0b \x01(\x0b2*.kiapi.board.types.GraphicBezierAttributesH\x00B\n\n\x08geometry"\\\n\x04Text\x12&\n\x04text\x18\x01 \x01(\x0b2\x18.kiapi.common.types.Text\x12,\n\x05layer\x18\x02 \x01(\x0e2\x1d.kiapi.board.types.BoardLayer"e\n\x07TextBox\x12,\n\x07textbox\x18\x01 \x01(\x0b2\x1b.kiapi.common.types.TextBox\x12,\n\x05layer\x18\x02 \x01(\x0e2\x1d.kiapi.board.types.BoardLayer"\\\n\x14ThermalSpokeSettings\x12\r\n\x05width\x18\x01 \x01(\x03\x12(\n\x05angle\x18\x02 \x01(\x0b2\x19.kiapi.common.types.Angle\x12\x0b\n\x03gap\x18\x03 \x01(\x03"\x96\x03\n\x03Pad\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x12/\n\x06locked\x18\x02 \x01(\x0e2\x1f.kiapi.common.types.LockedState\x12\x0e\n\x06number\x18\x03 \x01(\t\x12#\n\x03net\x18\x04 \x01(\x0b2\x16.kiapi.board.types.Net\x12(\n\x04type\x18\x05 \x01(\x0e2\x1a.kiapi.board.types.PadType\x12.\n\tpad_stack\x18\x06 \x01(\x0b2\x1b.kiapi.board.types.PadStack\x12-\n\x08position\x18\x07 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x129\n\toverrides\x18\x08 \x01(\x0b2&.kiapi.board.types.DesignRuleOverrides\x12?\n\x0ethermal_spokes\x18\t \x01(\x0b2\'.kiapi.board.types.ThermalSpokeSettings"\x06\n\x04Zone"\x0b\n\tDimension"\x10\n\x0eReferenceImage"\x07\n\x05Group"\x15\n\x07FieldId\x12\n\n\x02id\x18\x01 \x01(\x05"d\n\x05Field\x12&\n\x02id\x18\x01 \x01(\x0b2\x1a.kiapi.board.types.FieldId\x12\x0c\n\x04name\x18\x02 \x01(\t\x12%\n\x04text\x18\x03 \x01(\x0b2\x17.kiapi.board.types.Text"\t\n\x07Model3D"\xaa\x02\n\x13FootprintAttributes\x12\x13\n\x0bdescription\x18\x01 \x01(\t\x12\x10\n\x08keywords\x18\x02 \x01(\t\x12\x18\n\x10not_in_schematic\x18\x03 \x01(\x08\x12#\n\x1bexclude_from_position_files\x18\x04 \x01(\x08\x12&\n\x1eexclude_from_bill_of_materials\x18\x05 \x01(\x08\x12)\n!exempt_from_courtyard_requirement\x18\x06 \x01(\x08\x12\x17\n\x0fdo_not_populate\x18\x07 \x01(\x08\x12A\n\x0emounting_style\x18\x08 \x01(\x0e2).kiapi.board.types.FootprintMountingStyle"\xba\x02\n\x13DesignRuleOverrides\x12/\n\tclearance\x18\x01 \x01(\x0b2\x1c.kiapi.common.types.Distance\x128\n\x12solder_mask_margin\x18\x02 \x01(\x0b2\x1c.kiapi.common.types.Distance\x129\n\x13solder_paste_margin\x18\x03 \x01(\x0b2\x1c.kiapi.common.types.Distance\x12<\n\x19solder_paste_margin_ratio\x18\x04 \x01(\x0b2\x19.kiapi.common.types.Ratio\x12?\n\x0fzone_connection\x18\x05 \x01(\x0e2&.kiapi.board.types.ZoneConnectionStyle"&\n\x10NetTieDefinition\x12\x12\n\npad_number\x18\x01 \x03(\t"\xbf\x04\n\tFootprint\x121\n\x02id\x18\x01 \x01(\x0b2%.kiapi.common.types.LibraryIdentifier\x12+\n\x06anchor\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12:\n\nattributes\x18\x03 \x01(\x0b2&.kiapi.board.types.FootprintAttributes\x129\n\toverrides\x18\x04 \x01(\x0b2&.kiapi.board.types.DesignRuleOverrides\x125\n\x08net_ties\x18\x05 \x03(\x0b2#.kiapi.board.types.NetTieDefinition\x125\n\x0eprivate_layers\x18\x06 \x03(\x0e2\x1d.kiapi.board.types.BoardLayer\x121\n\x0freference_field\x18\x07 \x01(\x0b2\x18.kiapi.board.types.Field\x12-\n\x0bvalue_field\x18\x08 \x01(\x0b2\x18.kiapi.board.types.Field\x121\n\x0fdatasheet_field\x18\t \x01(\x0b2\x18.kiapi.board.types.Field\x123\n\x11description_field\x18\n \x01(\x0b2\x18.kiapi.board.types.Field\x12#\n\x05items\x18\x0b \x03(\x0b2\x14.google.protobuf.Any"\xea\x04\n\x11FootprintInstance\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x12-\n\x08position\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12.\n\x0borientation\x18\x03 \x01(\x0b2\x19.kiapi.common.types.Angle\x12,\n\x05layer\x18\x04 \x01(\x0e2\x1d.kiapi.board.types.BoardLayer\x12/\n\x06locked\x18\x05 \x01(\x0e2\x1f.kiapi.common.types.LockedState\x120\n\ndefinition\x18\x06 \x01(\x0b2\x1c.kiapi.board.types.Footprint\x121\n\x0freference_field\x18\x07 \x01(\x0b2\x18.kiapi.board.types.Field\x12-\n\x0bvalue_field\x18\x08 \x01(\x0b2\x18.kiapi.board.types.Field\x121\n\x0fdatasheet_field\x18\t \x01(\x0b2\x18.kiapi.board.types.Field\x123\n\x11description_field\x18\n \x01(\x0b2\x18.kiapi.board.types.Field\x12:\n\nattributes\x18\x0b \x01(\x0b2&.kiapi.board.types.FootprintAttributes\x129\n\toverrides\x18\x0c \x01(\x0b2&.kiapi.board.types.DesignRuleOverrides*\xdc\x07\n\nBoardLayer\x12\x0e\n\nBL_UNKNOWN\x10\x00\x12\x10\n\x0cBL_UNDEFINED\x10\x01\x12\x11\n\rBL_UNSELECTED\x10\x02\x12\x0b\n\x07BL_F_Cu\x10\x03\x12\r\n\tBL_In1_Cu\x10\x04\x12\r\n\tBL_In2_Cu\x10\x05\x12\r\n\tBL_In3_Cu\x10\x06\x12\r\n\tBL_In4_Cu\x10\x07\x12\r\n\tBL_In5_Cu\x10\x08\x12\r\n\tBL_In6_Cu\x10\t\x12\r\n\tBL_In7_Cu\x10\n\x12\r\n\tBL_In8_Cu\x10\x0b\x12\r\n\tBL_In9_Cu\x10\x0c\x12\x0e\n\nBL_In10_Cu\x10\r\x12\x0e\n\nBL_In11_Cu\x10\x0e\x12\x0e\n\nBL_In12_Cu\x10\x0f\x12\x0e\n\nBL_In13_Cu\x10\x10\x12\x0e\n\nBL_In14_Cu\x10\x11\x12\x0e\n\nBL_In15_Cu\x10\x12\x12\x0e\n\nBL_In16_Cu\x10\x13\x12\x0e\n\nBL_In17_Cu\x10\x14\x12\x0e\n\nBL_In18_Cu\x10\x15\x12\x0e\n\nBL_In19_Cu\x10\x16\x12\x0e\n\nBL_In20_Cu\x10\x17\x12\x0e\n\nBL_In21_Cu\x10\x18\x12\x0e\n\nBL_In22_Cu\x10\x19\x12\x0e\n\nBL_In23_Cu\x10\x1a\x12\x0e\n\nBL_In24_Cu\x10\x1b\x12\x0e\n\nBL_In25_Cu\x10\x1c\x12\x0e\n\nBL_In26_Cu\x10\x1d\x12\x0e\n\nBL_In27_Cu\x10\x1e\x12\x0e\n\nBL_In28_Cu\x10\x1f\x12\x0e\n\nBL_In29_Cu\x10 \x12\x0e\n\nBL_In30_Cu\x10!\x12\x0b\n\x07BL_B_Cu\x10"\x12\x0e\n\nBL_B_Adhes\x10#\x12\x0e\n\nBL_F_Adhes\x10$\x12\x0e\n\nBL_B_Paste\x10%\x12\x0e\n\nBL_F_Paste\x10&\x12\x0e\n\nBL_B_SilkS\x10\'\x12\x0e\n\nBL_F_SilkS\x10(\x12\r\n\tBL_B_Mask\x10)\x12\r\n\tBL_F_Mask\x10*\x12\x10\n\x0cBL_Dwgs_User\x10+\x12\x10\n\x0cBL_Cmts_User\x10,\x12\x10\n\x0cBL_Eco1_User\x10-\x12\x10\n\x0cBL_Eco2_User\x10.\x12\x10\n\x0cBL_Edge_Cuts\x10/\x12\r\n\tBL_Margin\x100\x12\x0e\n\nBL_B_CrtYd\x101\x12\x0e\n\nBL_F_CrtYd\x102\x12\x0c\n\x08BL_B_Fab\x103\x12\x0c\n\x08BL_F_Fab\x104\x12\r\n\tBL_User_1\x105\x12\r\n\tBL_User_2\x106\x12\r\n\tBL_User_3\x107\x12\r\n\tBL_User_4\x108\x12\r\n\tBL_User_5\x109\x12\r\n\tBL_User_6\x10:\x12\r\n\tBL_User_7\x10;\x12\r\n\tBL_User_8\x10<\x12\r\n\tBL_User_9\x10=*F\n\x0cPadStackType\x12\x0f\n\x0bPST_UNKNOWN\x10\x00\x12\x0f\n\x0bPST_THROUGH\x10\x01\x12\x14\n\x10PST_BLIND_BURIED\x10\x02*m\n\x17UnconnectedLayerRemoval\x12\x0f\n\x0bULR_UNKNOWN\x10\x00\x12\x0c\n\x08ULR_KEEP\x10\x01\x12\x0e\n\nULR_REMOVE\x10\x02\x12#\n\x1fULR_REMOVE_EXCEPT_START_AND_END\x10\x03*\x9e\x01\n\rPadStackShape\x12\x0f\n\x0bPSS_UNKNOWN\x10\x00\x12\x0e\n\nPSS_CIRCLE\x10\x01\x12\x11\n\rPSS_RECTANGLE\x10\x02\x12\x0c\n\x08PSS_OVAL\x10\x03\x12\x11\n\rPSS_TRAPEZOID\x10\x04\x12\x11\n\rPSS_ROUNDRECT\x10\x05\x12\x15\n\x11PSS_CHAMFEREDRECT\x10\x06\x12\x0e\n\nPSS_CUSTOM\x10\x07*U\n\x07PadType\x12\x0e\n\nPT_UNKNOWN\x10\x00\x12\n\n\x06PT_PTH\x10\x01\x12\n\n\x06PT_SMD\x10\x02\x12\x15\n\x11PT_EDGE_CONNECTOR\x10\x03\x12\x0b\n\x07PT_NPTH\x10\x04*Y\n\x1eCustomPadShapeZoneFillStrategy\x12\x10\n\x0cCPSZ_UNKNOWN\x10\x00\x12\x10\n\x0cCPSZ_OUTLINE\x10\x01\x12\x13\n\x0fCPSZ_CONVEXHULL\x10\x02*a\n\x16FootprintMountingStyle\x12\x0f\n\x0bFMS_UNKNOWN\x10\x00\x12\x14\n\x10FMS_THROUGH_HOLE\x10\x01\x12\x0b\n\x07FMS_SMD\x10\x02\x12\x13\n\x0fFMS_UNSPECIFIED\x10\x03*{\n\x13ZoneConnectionStyle\x12\x0f\n\x0bZCS_UNKNOWN\x10\x00\x12\x11\n\rZCS_INHERITED\x10\x01\x12\x0c\n\x08ZCS_NONE\x10\x02\x12\x0f\n\x0bZCS_THERMAL\x10\x03\x12\x0c\n\x08ZCS_FULL\x10\x04\x12\x13\n\x0fZCS_PTH_THERMAL\x10\x05b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'board.board_types_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_BOARDLAYER']._serialized_start = 5993
    _globals['_BOARDLAYER']._serialized_end = 6981
    _globals['_PADSTACKTYPE']._serialized_start = 6983
    _globals['_PADSTACKTYPE']._serialized_end = 7053
    _globals['_UNCONNECTEDLAYERREMOVAL']._serialized_start = 7055
    _globals['_UNCONNECTEDLAYERREMOVAL']._serialized_end = 7164
    _globals['_PADSTACKSHAPE']._serialized_start = 7167
    _globals['_PADSTACKSHAPE']._serialized_end = 7325
    _globals['_PADTYPE']._serialized_start = 7327
    _globals['_PADTYPE']._serialized_end = 7412
    _globals['_CUSTOMPADSHAPEZONEFILLSTRATEGY']._serialized_start = 7414
    _globals['_CUSTOMPADSHAPEZONEFILLSTRATEGY']._serialized_end = 7503
    _globals['_FOOTPRINTMOUNTINGSTYLE']._serialized_start = 7505
    _globals['_FOOTPRINTMOUNTINGSTYLE']._serialized_end = 7602
    _globals['_ZONECONNECTIONSTYLE']._serialized_start = 7604
    _globals['_ZONECONNECTIONSTYLE']._serialized_end = 7727
    _globals['_NETCODE']._serialized_start = 104
    _globals['_NETCODE']._serialized_end = 128
    _globals['_NET']._serialized_start = 130
    _globals['_NET']._serialized_end = 191
    _globals['_TRACK']._serialized_start = 194
    _globals['_TRACK']._serialized_end = 502
    _globals['_ARC']._serialized_start = 505
    _globals['_ARC']._serialized_end = 853
    _globals['_CHAMFEREDRECTCORNERS']._serialized_start = 855
    _globals['_CHAMFEREDRECTCORNERS']._serialized_end = 957
    _globals['_PADSTACKLAYER']._serialized_start = 960
    _globals['_PADSTACKLAYER']._serialized_end = 1292
    _globals['_PADSTACK']._serialized_start = 1295
    _globals['_PADSTACK']._serialized_end = 1678
    _globals['_VIA']._serialized_start = 1681
    _globals['_VIA']._serialized_end = 1905
    _globals['_GRAPHICSEGMENTATTRIBUTES']._serialized_start = 1907
    _globals['_GRAPHICSEGMENTATTRIBUTES']._serialized_end = 2019
    _globals['_GRAPHICRECTANGLEATTRIBUTES']._serialized_start = 2021
    _globals['_GRAPHICRECTANGLEATTRIBUTES']._serialized_end = 2147
    _globals['_GRAPHICARCATTRIBUTES']._serialized_start = 2150
    _globals['_GRAPHICARCATTRIBUTES']._serialized_end = 2300
    _globals['_GRAPHICCIRCLEATTRIBUTES']._serialized_start = 2302
    _globals['_GRAPHICCIRCLEATTRIBUTES']._serialized_end = 2423
    _globals['_GRAPHICBEZIERATTRIBUTES']._serialized_start = 2426
    _globals['_GRAPHICBEZIERATTRIBUTES']._serialized_end = 2631
    _globals['_GRAPHICSHAPE']._serialized_start = 2634
    _globals['_GRAPHICSHAPE']._serialized_end = 3249
    _globals['_TEXT']._serialized_start = 3251
    _globals['_TEXT']._serialized_end = 3343
    _globals['_TEXTBOX']._serialized_start = 3345
    _globals['_TEXTBOX']._serialized_end = 3446
    _globals['_THERMALSPOKESETTINGS']._serialized_start = 3448
    _globals['_THERMALSPOKESETTINGS']._serialized_end = 3540
    _globals['_PAD']._serialized_start = 3543
    _globals['_PAD']._serialized_end = 3949
    _globals['_ZONE']._serialized_start = 3951
    _globals['_ZONE']._serialized_end = 3957
    _globals['_DIMENSION']._serialized_start = 3959
    _globals['_DIMENSION']._serialized_end = 3970
    _globals['_REFERENCEIMAGE']._serialized_start = 3972
    _globals['_REFERENCEIMAGE']._serialized_end = 3988
    _globals['_GROUP']._serialized_start = 3990
    _globals['_GROUP']._serialized_end = 3997
    _globals['_FIELDID']._serialized_start = 3999
    _globals['_FIELDID']._serialized_end = 4020
    _globals['_FIELD']._serialized_start = 4022
    _globals['_FIELD']._serialized_end = 4122
    _globals['_MODEL3D']._serialized_start = 4124
    _globals['_MODEL3D']._serialized_end = 4133
    _globals['_FOOTPRINTATTRIBUTES']._serialized_start = 4136
    _globals['_FOOTPRINTATTRIBUTES']._serialized_end = 4434
    _globals['_DESIGNRULEOVERRIDES']._serialized_start = 4437
    _globals['_DESIGNRULEOVERRIDES']._serialized_end = 4751
    _globals['_NETTIEDEFINITION']._serialized_start = 4753
    _globals['_NETTIEDEFINITION']._serialized_end = 4791
    _globals['_FOOTPRINT']._serialized_start = 4794
    _globals['_FOOTPRINT']._serialized_end = 5369
    _globals['_FOOTPRINTINSTANCE']._serialized_start = 5372
    _globals['_FOOTPRINTINSTANCE']._serialized_end = 5990