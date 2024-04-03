"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ...common.types import base_types_pb2 as common_dot_types_dot_base__types__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%common/commands/editor_commands.proto\x12\x15kiapi.common.commands\x1a\x19google/protobuf/any.proto\x1a\x1dcommon/types/base_types.proto"=\n\rRefreshEditor\x12,\n\x05frame\x18\x01 \x01(\x0e2\x1d.kiapi.common.types.FrameType"B\n\x10GetOpenDocuments\x12.\n\x04type\x18\x01 \x01(\x0e2 .kiapi.common.types.DocumentType"T\n\x18GetOpenDocumentsResponse\x128\n\tdocuments\x18\x01 \x03(\x0b2%.kiapi.common.types.DocumentSpecifier"\x1b\n\tRunAction\x12\x0e\n\x06action\x18\x01 \x01(\t"K\n\x11RunActionResponse\x126\n\x06status\x18\x01 \x01(\x0e2&.kiapi.common.commands.RunActionStatus"\r\n\x0bBeginCommit";\n\x13BeginCommitResponse\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID"w\n\tEndCommit\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x123\n\x06action\x18\x02 \x01(\x0e2#.kiapi.common.commands.CommitAction\x12\x0f\n\x07message\x18\x03 \x01(\t"\x13\n\x11EndCommitResponse"\x8f\x01\n\x0bCreateItems\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x12#\n\x05items\x18\x02 \x03(\x0b2\x14.google.protobuf.Any\x12+\n\tcontainer\x18\x03 \x01(\x0b2\x18.kiapi.common.types.KIID"X\n\nItemStatus\x123\n\x04code\x18\x01 \x01(\x0e2%.kiapi.common.commands.ItemStatusCode\x12\x15\n\rerror_message\x18\x02 \x01(\t"k\n\x12ItemCreationResult\x121\n\x06status\x18\x01 \x01(\x0b2!.kiapi.common.commands.ItemStatus\x12"\n\x04item\x18\x02 \x01(\x0b2\x14.google.protobuf.Any"\xbe\x01\n\x13CreateItemsResponse\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x125\n\x06status\x18\x02 \x01(\x0e2%.kiapi.common.types.ItemRequestStatus\x12@\n\rcreated_items\x18\x03 \x03(\x0b2).kiapi.common.commands.ItemCreationResult"g\n\x08GetItems\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x12+\n\x05types\x18\x02 \x03(\x0b2\x1c.kiapi.common.types.ItemType"\x9e\x01\n\x10GetItemsResponse\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x125\n\x06status\x18\x02 \x01(\x0e2%.kiapi.common.types.ItemRequestStatus\x12#\n\x05items\x18\x03 \x03(\x0b2\x14.google.protobuf.Any"b\n\x0bUpdateItems\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x12#\n\x05items\x18\x02 \x03(\x0b2\x14.google.protobuf.Any"i\n\x10ItemUpdateResult\x121\n\x06status\x18\x01 \x01(\x0b2!.kiapi.common.commands.ItemStatus\x12"\n\x04item\x18\x02 \x01(\x0b2\x14.google.protobuf.Any"\xbc\x01\n\x13UpdateItemsResponse\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x125\n\x06status\x18\x02 \x01(\x0e2%.kiapi.common.types.ItemRequestStatus\x12>\n\rupdated_items\x18\x03 \x03(\x0b2\'.kiapi.common.commands.ItemUpdateResult"i\n\x0bDeleteItems\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x12*\n\x08item_ids\x18\x02 \x03(\x0b2\x18.kiapi.common.types.KIID"u\n\x12ItemDeletionResult\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x129\n\x06status\x18\x02 \x01(\x0e2).kiapi.common.commands.ItemDeletionStatus"\xbe\x01\n\x13DeleteItemsResponse\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x125\n\x06status\x18\x02 \x01(\x0e2%.kiapi.common.types.ItemRequestStatus\x12@\n\rdeleted_items\x18\x03 \x03(\x0b2).kiapi.common.commands.ItemDeletionResult"j\n\x12GetItemBoundingBox\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x12$\n\x02id\x18\x02 \x01(\x0b2\x18.kiapi.common.types.KIID"o\n\x13BoundingBoxResponse\x12-\n\x08position\x18\x01 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12)\n\x04size\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.Vector2*W\n\x0fRunActionStatus\x12\x0f\n\x0bRAS_UNKNOWN\x10\x00\x12\n\n\x06RAS_OK\x10\x01\x12\x0f\n\x0bRAS_INVALID\x10\x02\x12\x16\n\x12RAS_FRAME_NOT_OPEN\x10\x03*=\n\x0cCommitAction\x12\x0f\n\x0bCMA_UNKNOWN\x10\x00\x12\x0e\n\nCMA_COMMIT\x10\x01\x12\x0c\n\x08CMA_DROP\x10\x02*\x93\x01\n\x0eItemStatusCode\x12\x0f\n\x0bISC_UNKNOWN\x10\x00\x12\n\n\x06ISC_OK\x10\x01\x12\x14\n\x10ISC_INVALID_TYPE\x10\x02\x12\x10\n\x0cISC_EXISTING\x10\x03\x12\x13\n\x0fISC_NONEXISTENT\x10\x04\x12\x11\n\rISC_IMMUTABLE\x10\x05\x12\x14\n\x10ISC_INVALID_DATA\x10\x07*Y\n\x12ItemDeletionStatus\x12\x0f\n\x0bIDS_UNKNOWN\x10\x00\x12\n\n\x06IDS_OK\x10\x01\x12\x13\n\x0fIDS_NONEXISTENT\x10\x02\x12\x11\n\rIDS_IMMUTABLE\x10\x03b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'common.commands.editor_commands_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_RUNACTIONSTATUS']._serialized_start = 2505
    _globals['_RUNACTIONSTATUS']._serialized_end = 2592
    _globals['_COMMITACTION']._serialized_start = 2594
    _globals['_COMMITACTION']._serialized_end = 2655
    _globals['_ITEMSTATUSCODE']._serialized_start = 2658
    _globals['_ITEMSTATUSCODE']._serialized_end = 2805
    _globals['_ITEMDELETIONSTATUS']._serialized_start = 2807
    _globals['_ITEMDELETIONSTATUS']._serialized_end = 2896
    _globals['_REFRESHEDITOR']._serialized_start = 122
    _globals['_REFRESHEDITOR']._serialized_end = 183
    _globals['_GETOPENDOCUMENTS']._serialized_start = 185
    _globals['_GETOPENDOCUMENTS']._serialized_end = 251
    _globals['_GETOPENDOCUMENTSRESPONSE']._serialized_start = 253
    _globals['_GETOPENDOCUMENTSRESPONSE']._serialized_end = 337
    _globals['_RUNACTION']._serialized_start = 339
    _globals['_RUNACTION']._serialized_end = 366
    _globals['_RUNACTIONRESPONSE']._serialized_start = 368
    _globals['_RUNACTIONRESPONSE']._serialized_end = 443
    _globals['_BEGINCOMMIT']._serialized_start = 445
    _globals['_BEGINCOMMIT']._serialized_end = 458
    _globals['_BEGINCOMMITRESPONSE']._serialized_start = 460
    _globals['_BEGINCOMMITRESPONSE']._serialized_end = 519
    _globals['_ENDCOMMIT']._serialized_start = 521
    _globals['_ENDCOMMIT']._serialized_end = 640
    _globals['_ENDCOMMITRESPONSE']._serialized_start = 642
    _globals['_ENDCOMMITRESPONSE']._serialized_end = 661
    _globals['_CREATEITEMS']._serialized_start = 664
    _globals['_CREATEITEMS']._serialized_end = 807
    _globals['_ITEMSTATUS']._serialized_start = 809
    _globals['_ITEMSTATUS']._serialized_end = 897
    _globals['_ITEMCREATIONRESULT']._serialized_start = 899
    _globals['_ITEMCREATIONRESULT']._serialized_end = 1006
    _globals['_CREATEITEMSRESPONSE']._serialized_start = 1009
    _globals['_CREATEITEMSRESPONSE']._serialized_end = 1199
    _globals['_GETITEMS']._serialized_start = 1201
    _globals['_GETITEMS']._serialized_end = 1304
    _globals['_GETITEMSRESPONSE']._serialized_start = 1307
    _globals['_GETITEMSRESPONSE']._serialized_end = 1465
    _globals['_UPDATEITEMS']._serialized_start = 1467
    _globals['_UPDATEITEMS']._serialized_end = 1565
    _globals['_ITEMUPDATERESULT']._serialized_start = 1567
    _globals['_ITEMUPDATERESULT']._serialized_end = 1672
    _globals['_UPDATEITEMSRESPONSE']._serialized_start = 1675
    _globals['_UPDATEITEMSRESPONSE']._serialized_end = 1863
    _globals['_DELETEITEMS']._serialized_start = 1865
    _globals['_DELETEITEMS']._serialized_end = 1970
    _globals['_ITEMDELETIONRESULT']._serialized_start = 1972
    _globals['_ITEMDELETIONRESULT']._serialized_end = 2089
    _globals['_DELETEITEMSRESPONSE']._serialized_start = 2092
    _globals['_DELETEITEMSRESPONSE']._serialized_end = 2282
    _globals['_GETITEMBOUNDINGBOX']._serialized_start = 2284
    _globals['_GETITEMBOUNDINGBOX']._serialized_end = 2390
    _globals['_BOUNDINGBOXRESPONSE']._serialized_start = 2392
    _globals['_BOUNDINGBOXRESPONSE']._serialized_end = 2503