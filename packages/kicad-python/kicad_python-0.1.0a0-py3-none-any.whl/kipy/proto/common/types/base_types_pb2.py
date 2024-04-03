"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dcommon/types/base_types.proto\x12\x12kiapi.common.types\x1a google/protobuf/field_mask.proto"J\n\x15CommandStatusResponse\x121\n\x06status\x18\x01 \x01(\x0e2!.kiapi.common.types.CommandStatus"Q\n\x0cKiCadVersion\x12\r\n\x05major\x18\x01 \x01(\r\x12\r\n\x05minor\x18\x02 \x01(\r\x12\r\n\x05patch\x18\x03 \x01(\r\x12\x14\n\x0cfull_version\x18\x04 \x01(\t"\x15\n\x04KIID\x12\r\n\x05value\x18\x01 \x01(\t"A\n\x11LibraryIdentifier\x12\x18\n\x10library_nickname\x18\x01 \x01(\t\x12\x12\n\nentry_name\x18\x02 \x01(\t"P\n\tSheetPath\x12&\n\x04path\x18\x01 \x03(\x0b2\x18.kiapi.common.types.KIID\x12\x1b\n\x13path_human_readable\x18\x02 \x01(\t".\n\x10ProjectSpecifier\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t"\x90\x02\n\x11DocumentSpecifier\x12.\n\x04type\x18\x01 \x01(\x0e2 .kiapi.common.types.DocumentType\x127\n\x06lib_id\x18\x02 \x01(\x0b2%.kiapi.common.types.LibraryIdentifierH\x00\x123\n\nsheet_path\x18\x03 \x01(\x0b2\x1d.kiapi.common.types.SheetPathH\x00\x12\x18\n\x0eboard_filename\x18\x04 \x01(\tH\x00\x125\n\x07project\x18\x05 \x01(\x0b2$.kiapi.common.types.ProjectSpecifierB\x0c\n\nidentifier"\x18\n\x08ItemType\x12\x0c\n\x04type\x18\x01 \x01(\x05"\xa2\x01\n\nItemHeader\x127\n\x08document\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier\x12+\n\tcontainer\x18\x02 \x01(\x0b2\x18.kiapi.common.types.KIID\x12.\n\nfield_mask\x18\x03 \x01(\x0b2\x1a.google.protobuf.FieldMask"%\n\x07Vector2\x12\x0c\n\x04x_nm\x18\x01 \x01(\x03\x12\x0c\n\x04y_nm\x18\x02 \x01(\x03"3\n\x07Vector3\x12\x0c\n\x04x_nm\x18\x01 \x01(\x03\x12\x0c\n\x04y_nm\x18\x02 \x01(\x03\x12\x0c\n\x04z_nm\x18\x03 \x01(\x03"\x1c\n\x08Distance\x12\x10\n\x08value_nm\x18\x01 \x01(\x03"\x1e\n\x05Angle\x12\x15\n\rvalue_degrees\x18\x01 \x01(\x01"3\n\x05Color\x12\t\n\x01r\x18\x01 \x01(\x01\x12\t\n\x01g\x18\x02 \x01(\x01\x12\t\n\x01b\x18\x03 \x01(\x01\x12\t\n\x01a\x18\x04 \x01(\x01"\x90\x01\n\x0eArcStartMidEnd\x12*\n\x05start\x18\x01 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12(\n\x03mid\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12(\n\x03end\x18\x03 \x01(\x0b2\x1b.kiapi.common.types.Vector2"{\n\x0cPolyLineNode\x12,\n\x05point\x18\x01 \x01(\x0b2\x1b.kiapi.common.types.Vector2H\x00\x121\n\x03arc\x18\x02 \x01(\x0b2".kiapi.common.types.ArcStartMidEndH\x00B\n\n\x08geometry"K\n\x08PolyLine\x12/\n\x05nodes\x18\x01 \x03(\x0b2 .kiapi.common.types.PolyLineNode\x12\x0e\n\x06closed\x18\x02 \x01(\x08"n\n\x10PolygonWithHoles\x12-\n\x07outline\x18\x01 \x01(\x0b2\x1c.kiapi.common.types.PolyLine\x12+\n\x05holes\x18\x02 \x03(\x0b2\x1c.kiapi.common.types.PolyLine"A\n\x07PolySet\x126\n\x08polygons\x18\x01 \x03(\x0b2$.kiapi.common.types.PolygonWithHoles"\x13\n\x05Layer\x12\n\n\x02id\x18\x01 \x01(\x05"\xca\x03\n\x0eTextAttributes\x12\x11\n\tfont_name\x18\x01 \x01(\t\x12E\n\x14horizontal_alignment\x18\x02 \x01(\x0e2\'.kiapi.common.types.HorizontalAlignment\x12A\n\x12vertical_alignment\x18\x03 \x01(\x0e2%.kiapi.common.types.VerticalAlignment\x12(\n\x05angle\x18\x04 \x01(\x0b2\x19.kiapi.common.types.Angle\x12\x14\n\x0cline_spacing\x18\x05 \x01(\x01\x122\n\x0cstroke_width\x18\x06 \x01(\x0b2\x1c.kiapi.common.types.Distance\x12\x0e\n\x06italic\x18\x07 \x01(\x08\x12\x0c\n\x04bold\x18\x08 \x01(\x08\x12\x12\n\nunderlined\x18\t \x01(\x08\x12\x0f\n\x07visible\x18\n \x01(\x08\x12\x10\n\x08mirrored\x18\x0b \x01(\x08\x12\x11\n\tmultiline\x18\x0c \x01(\x08\x12\x14\n\x0ckeep_upright\x18\r \x01(\x08\x12)\n\x04size\x18\x0e \x01(\x0b2\x1b.kiapi.common.types.Vector2"\xa1\x02\n\x04Text\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x12-\n\x08position\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x126\n\nattributes\x18\x03 \x01(\x0b2".kiapi.common.types.TextAttributes\x12/\n\x06locked\x18\x04 \x01(\x0e2\x1f.kiapi.common.types.LockedState\x12(\n\x05layer\x18\x05 \x01(\x0b2\x19.kiapi.common.types.Layer\x12\x0c\n\x04text\x18\x06 \x01(\t\x12\x11\n\thyperlink\x18\x07 \x01(\t\x12\x10\n\x08knockout\x18\x08 \x01(\x08"\xb2\x02\n\x07TextBox\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x12-\n\x08top_left\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x121\n\x0cbottom_right\x18\x03 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x126\n\nattributes\x18\x04 \x01(\x0b2".kiapi.common.types.TextAttributes\x12/\n\x06locked\x18\x05 \x01(\x0e2\x1f.kiapi.common.types.LockedState\x12(\n\x05layer\x18\x06 \x01(\x0b2\x19.kiapi.common.types.Layer\x12\x0c\n\x04text\x18\x07 \x01(\t"\x9d\x01\n\x10StrokeAttributes\x12+\n\x05width\x18\x01 \x01(\x0b2\x1c.kiapi.common.types.Distance\x122\n\x05style\x18\x02 \x01(\x0e2#.kiapi.common.types.StrokeLineStyle\x12(\n\x05color\x18\x03 \x01(\x0b2\x19.kiapi.common.types.Color"y\n\x15GraphicFillAttributes\x126\n\tfill_type\x18\x01 \x01(\x0e2#.kiapi.common.types.GraphicFillType\x12(\n\x05color\x18\x02 \x01(\x0b2\x19.kiapi.common.types.Color"\x82\x01\n\x11GraphicAttributes\x124\n\x06stroke\x18\x01 \x01(\x0b2$.kiapi.common.types.StrokeAttributes\x127\n\x04fill\x18\x02 \x01(\x0b2).kiapi.common.types.GraphicFillAttributes*9\n\rCommandStatus\x12\x0e\n\nCS_UNKNOWN\x10\x00\x12\t\n\x05CS_OK\x10\x01\x12\r\n\tCS_FAILED\x10\x02*\xc3\x01\n\tFrameType\x12\x0e\n\nFT_UNKNOWN\x10\x00\x12\x16\n\x12FT_PROJECT_MANAGER\x10\x01\x12\x17\n\x13FT_SCHEMATIC_EDITOR\x10\x02\x12\x11\n\rFT_PCB_EDITOR\x10\x03\x12\x16\n\x12FT_SPICE_SIMULATOR\x10\x04\x12\x14\n\x10FT_SYMBOL_EDITOR\x10\x05\x12\x17\n\x13FT_FOOTPRINT_EDITOR\x10\x06\x12\x1b\n\x17FT_DRAWING_SHEET_EDITOR\x10\x07*\x91\x01\n\x0cDocumentType\x12\x13\n\x0fDOCTYPE_UNKNOWN\x10\x00\x12\x15\n\x11DOCTYPE_SCHEMATIC\x10\x01\x12\x12\n\x0eDOCTYPE_SYMBOL\x10\x02\x12\x0f\n\x0bDOCTYPE_PCB\x10\x03\x12\x15\n\x11DOCTYPE_FOOTPRINT\x10\x04\x12\x19\n\x15DOCTYPE_DRAWING_SHEET\x10\x05*h\n\x11ItemRequestStatus\x12\x0f\n\x0bIRS_UNKNOWN\x10\x00\x12\n\n\x06IRS_OK\x10\x01\x12\x1a\n\x16IRS_DOCUMENT_NOT_FOUND\x10\x02\x12\x1a\n\x16IRS_FIELD_MASK_INVALID\x10\x03*=\n\x0bLockedState\x12\x0e\n\nLS_UNKNOWN\x10\x00\x12\x0f\n\x0bLS_UNLOCKED\x10\x01\x12\r\n\tLS_LOCKED\x10\x02*e\n\x13HorizontalAlignment\x12\x0e\n\nHA_UNKNOWN\x10\x00\x12\x0b\n\x07HA_LEFT\x10\x01\x12\r\n\tHA_CENTER\x10\x02\x12\x0c\n\x08HA_RIGHT\x10\x03\x12\x14\n\x10HA_INDETERMINATE\x10\x04*c\n\x11VerticalAlignment\x12\x0e\n\nVA_UNKNOWN\x10\x00\x12\n\n\x06VA_TOP\x10\x01\x12\r\n\tVA_CENTER\x10\x02\x12\r\n\tVA_BOTTOM\x10\x03\x12\x14\n\x10VA_INDETERMINATE\x10\x04*\x82\x01\n\x0fStrokeLineStyle\x12\x0f\n\x0bSLS_UNKNOWN\x10\x00\x12\x0f\n\x0bSLS_DEFAULT\x10\x01\x12\r\n\tSLS_SOLID\x10\x02\x12\x0c\n\x08SLS_DASH\x10\x03\x12\x0b\n\x07SLS_DOT\x10\x04\x12\x0f\n\x0bSLS_DASHDOT\x10\x05\x12\x12\n\x0eSLS_DASHDOTDOT\x10\x06*D\n\x0fGraphicFillType\x12\x0f\n\x0bGFT_UNKNOWN\x10\x00\x12\x10\n\x0cGFT_UNFILLED\x10\x01\x12\x0e\n\nGFT_FILLED\x10\x02b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'common.types.base_types_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_COMMANDSTATUS']._serialized_start = 3166
    _globals['_COMMANDSTATUS']._serialized_end = 3223
    _globals['_FRAMETYPE']._serialized_start = 3226
    _globals['_FRAMETYPE']._serialized_end = 3421
    _globals['_DOCUMENTTYPE']._serialized_start = 3424
    _globals['_DOCUMENTTYPE']._serialized_end = 3569
    _globals['_ITEMREQUESTSTATUS']._serialized_start = 3571
    _globals['_ITEMREQUESTSTATUS']._serialized_end = 3675
    _globals['_LOCKEDSTATE']._serialized_start = 3677
    _globals['_LOCKEDSTATE']._serialized_end = 3738
    _globals['_HORIZONTALALIGNMENT']._serialized_start = 3740
    _globals['_HORIZONTALALIGNMENT']._serialized_end = 3841
    _globals['_VERTICALALIGNMENT']._serialized_start = 3843
    _globals['_VERTICALALIGNMENT']._serialized_end = 3942
    _globals['_STROKELINESTYLE']._serialized_start = 3945
    _globals['_STROKELINESTYLE']._serialized_end = 4075
    _globals['_GRAPHICFILLTYPE']._serialized_start = 4077
    _globals['_GRAPHICFILLTYPE']._serialized_end = 4145
    _globals['_COMMANDSTATUSRESPONSE']._serialized_start = 87
    _globals['_COMMANDSTATUSRESPONSE']._serialized_end = 161
    _globals['_KICADVERSION']._serialized_start = 163
    _globals['_KICADVERSION']._serialized_end = 244
    _globals['_KIID']._serialized_start = 246
    _globals['_KIID']._serialized_end = 267
    _globals['_LIBRARYIDENTIFIER']._serialized_start = 269
    _globals['_LIBRARYIDENTIFIER']._serialized_end = 334
    _globals['_SHEETPATH']._serialized_start = 336
    _globals['_SHEETPATH']._serialized_end = 416
    _globals['_PROJECTSPECIFIER']._serialized_start = 418
    _globals['_PROJECTSPECIFIER']._serialized_end = 464
    _globals['_DOCUMENTSPECIFIER']._serialized_start = 467
    _globals['_DOCUMENTSPECIFIER']._serialized_end = 739
    _globals['_ITEMTYPE']._serialized_start = 741
    _globals['_ITEMTYPE']._serialized_end = 765
    _globals['_ITEMHEADER']._serialized_start = 768
    _globals['_ITEMHEADER']._serialized_end = 930
    _globals['_VECTOR2']._serialized_start = 932
    _globals['_VECTOR2']._serialized_end = 969
    _globals['_VECTOR3']._serialized_start = 971
    _globals['_VECTOR3']._serialized_end = 1022
    _globals['_DISTANCE']._serialized_start = 1024
    _globals['_DISTANCE']._serialized_end = 1052
    _globals['_ANGLE']._serialized_start = 1054
    _globals['_ANGLE']._serialized_end = 1084
    _globals['_COLOR']._serialized_start = 1086
    _globals['_COLOR']._serialized_end = 1137
    _globals['_ARCSTARTMIDEND']._serialized_start = 1140
    _globals['_ARCSTARTMIDEND']._serialized_end = 1284
    _globals['_POLYLINENODE']._serialized_start = 1286
    _globals['_POLYLINENODE']._serialized_end = 1409
    _globals['_POLYLINE']._serialized_start = 1411
    _globals['_POLYLINE']._serialized_end = 1486
    _globals['_POLYGONWITHHOLES']._serialized_start = 1488
    _globals['_POLYGONWITHHOLES']._serialized_end = 1598
    _globals['_POLYSET']._serialized_start = 1600
    _globals['_POLYSET']._serialized_end = 1665
    _globals['_LAYER']._serialized_start = 1667
    _globals['_LAYER']._serialized_end = 1686
    _globals['_TEXTATTRIBUTES']._serialized_start = 1689
    _globals['_TEXTATTRIBUTES']._serialized_end = 2147
    _globals['_TEXT']._serialized_start = 2150
    _globals['_TEXT']._serialized_end = 2439
    _globals['_TEXTBOX']._serialized_start = 2442
    _globals['_TEXTBOX']._serialized_end = 2748
    _globals['_STROKEATTRIBUTES']._serialized_start = 2751
    _globals['_STROKEATTRIBUTES']._serialized_end = 2908
    _globals['_GRAPHICFILLATTRIBUTES']._serialized_start = 2910
    _globals['_GRAPHICFILLATTRIBUTES']._serialized_end = 3031
    _globals['_GRAPHICATTRIBUTES']._serialized_start = 3034
    _globals['_GRAPHICATTRIBUTES']._serialized_end = 3164