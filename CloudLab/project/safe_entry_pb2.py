# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: safe_entry.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10safe_entry.proto\x12\nsafe_entry\"\"\n\x04User\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04nric\x18\x02 \x01(\t\"\x14\n\x04NRIC\x12\x0c\n\x04nric\x18\x01 \x01(\t\"*\n\x08NRICList\x12\x1e\n\x04nric\x18\x01 \x03(\x0b\x32\x10.safe_entry.NRIC\"\x1e\n\x0eHistoryRequest\x12\x0c\n\x04nric\x18\x01 \x01(\t\"\x1c\n\x0cLoginRequest\x12\x0c\n\x04nric\x18\x01 \x01(\t\"3\n\rLoginResponse\x12\"\n\x06status\x18\x01 \x01(\x0e\x32\x12.safe_entry.Status\"^\n\x0fHistoryResponse\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\x12\x10\n\x08location\x18\x02 \x01(\t\x12\x14\n\x0c\x63heckin_time\x18\x03 \x01(\t\x12\x15\n\rcheckout_time\x18\x04 \x01(\t\"O\n\x13HistoryListResponse\x12\x38\n\x13historyListResponse\x18\x01 \x03(\x0b\x32\x1b.safe_entry.HistoryResponse\"{\n\x0c\x43heckRequest\x12\x1e\n\x04user\x18\x01 \x01(\x0b\x32\x10.safe_entry.User\x12\x0c\n\x04\x64\x61te\x18\x02 \x01(\t\x12\x10\n\x08location\x18\x03 \x01(\t\x12\x14\n\x0c\x63heckin_time\x18\x04 \x01(\t\x12\x15\n\rcheckout_time\x18\x05 \x01(\t\"3\n\rCheckResponse\x12\"\n\x06status\x18\x01 \x01(\x0e\x32\x12.safe_entry.Status\"c\n\x11GroupCheckRequest\x12.\n\x0c\x63heckRequest\x18\x01 \x03(\x0b\x32\x18.safe_entry.CheckRequest\x12\x1e\n\x04nric\x18\x02 \x03(\x0b\x32\x10.safe_entry.NRIC\"X\n\x12GroupCheckResponse\x12\"\n\x06status\x18\x01 \x01(\x0e\x32\x12.safe_entry.Status\x12\x1e\n\x04nric\x18\x02 \x03(\x0b\x32\x10.safe_entry.NRIC\"\x07\n\x05\x45mpty\"8\n\x12NotificationStatus\x12\"\n\x06status\x18\x01 \x01(\x0e\x32\x12.safe_entry.Status\"\'\n\x14NotificationResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"+\n\x18NotificationListResponse\x12\x0f\n\x07message\x18\x01 \x03(\t\"C\n\x13NotificationRequest\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\x12\x0c\n\x04time\x18\x02 \x01(\t\x12\x10\n\x08location\x18\x03 \x01(\t\"\x1c\n\x08\x46ilename\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t*I\n\x06Status\x12\x0b\n\x07SUCCESS\x10\x00\x12\x0b\n\x07\x46\x41ILURE\x10\x01\x12\t\n\x05\x45RROR\x10\x02\x12\x0c\n\x08SFAILURE\x10\x03\x12\x0c\n\x08GFAILURE\x10\x04\x32\xbb\x07\n\tSafeEntry\x12>\n\x05Login\x12\x18.safe_entry.LoginRequest\x1a\x19.safe_entry.LoginResponse\"\x00\x12?\n\x06Logout\x12\x18.safe_entry.LoginRequest\x1a\x19.safe_entry.LoginResponse\"\x00\x12M\n\x11NotificationCheck\x12\x10.safe_entry.NRIC\x1a$.safe_entry.NotificationListResponse\"\x00\x12O\n\x15SubscribeNotification\x12\x10.safe_entry.NRIC\x1a .safe_entry.NotificationResponse\"\x00\x30\x01\x12?\n\x0e\x43heckForStatus\x12\x10.safe_entry.NRIC\x1a\x19.safe_entry.CheckResponse\"\x00\x12M\n\x13\x43heckForGroupStatus\x12\x14.safe_entry.NRICList\x1a\x1e.safe_entry.GroupCheckResponse\"\x00\x12\x46\n\rSingleCheckIn\x12\x18.safe_entry.CheckRequest\x1a\x19.safe_entry.CheckResponse\"\x00\x12G\n\x0eSingleCheckOut\x12\x18.safe_entry.CheckRequest\x1a\x19.safe_entry.CheckResponse\"\x00\x12J\n\x0cGroupCheckIn\x12\x1d.safe_entry.GroupCheckRequest\x1a\x19.safe_entry.CheckResponse\"\x00\x12\x46\n\rGroupCheckOut\x12\x18.safe_entry.CheckRequest\x1a\x19.safe_entry.CheckResponse\"\x00\x12L\n\x0bListHistory\x12\x1a.safe_entry.HistoryRequest\x1a\x1f.safe_entry.HistoryListResponse\"\x00\x12G\n\x0fNotifyCovidCase\x12\x1f.safe_entry.NotificationRequest\x1a\x11.safe_entry.Empty\"\x00\x12\x41\n\x0cLoadJSONFile\x12\x14.safe_entry.Filename\x1a\x19.safe_entry.CheckResponse\"\x00\x62\x06proto3')

_STATUS = DESCRIPTOR.enum_types_by_name['Status']
Status = enum_type_wrapper.EnumTypeWrapper(_STATUS)
SUCCESS = 0
FAILURE = 1
ERROR = 2
SFAILURE = 3
GFAILURE = 4


_USER = DESCRIPTOR.message_types_by_name['User']
_NRIC = DESCRIPTOR.message_types_by_name['NRIC']
_NRICLIST = DESCRIPTOR.message_types_by_name['NRICList']
_HISTORYREQUEST = DESCRIPTOR.message_types_by_name['HistoryRequest']
_LOGINREQUEST = DESCRIPTOR.message_types_by_name['LoginRequest']
_LOGINRESPONSE = DESCRIPTOR.message_types_by_name['LoginResponse']
_HISTORYRESPONSE = DESCRIPTOR.message_types_by_name['HistoryResponse']
_HISTORYLISTRESPONSE = DESCRIPTOR.message_types_by_name['HistoryListResponse']
_CHECKREQUEST = DESCRIPTOR.message_types_by_name['CheckRequest']
_CHECKRESPONSE = DESCRIPTOR.message_types_by_name['CheckResponse']
_GROUPCHECKREQUEST = DESCRIPTOR.message_types_by_name['GroupCheckRequest']
_GROUPCHECKRESPONSE = DESCRIPTOR.message_types_by_name['GroupCheckResponse']
_EMPTY = DESCRIPTOR.message_types_by_name['Empty']
_NOTIFICATIONSTATUS = DESCRIPTOR.message_types_by_name['NotificationStatus']
_NOTIFICATIONRESPONSE = DESCRIPTOR.message_types_by_name['NotificationResponse']
_NOTIFICATIONLISTRESPONSE = DESCRIPTOR.message_types_by_name['NotificationListResponse']
_NOTIFICATIONREQUEST = DESCRIPTOR.message_types_by_name['NotificationRequest']
_FILENAME = DESCRIPTOR.message_types_by_name['Filename']
User = _reflection.GeneratedProtocolMessageType('User', (_message.Message,), {
  'DESCRIPTOR' : _USER,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.User)
  })
_sym_db.RegisterMessage(User)

NRIC = _reflection.GeneratedProtocolMessageType('NRIC', (_message.Message,), {
  'DESCRIPTOR' : _NRIC,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.NRIC)
  })
_sym_db.RegisterMessage(NRIC)

NRICList = _reflection.GeneratedProtocolMessageType('NRICList', (_message.Message,), {
  'DESCRIPTOR' : _NRICLIST,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.NRICList)
  })
_sym_db.RegisterMessage(NRICList)

HistoryRequest = _reflection.GeneratedProtocolMessageType('HistoryRequest', (_message.Message,), {
  'DESCRIPTOR' : _HISTORYREQUEST,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.HistoryRequest)
  })
_sym_db.RegisterMessage(HistoryRequest)

LoginRequest = _reflection.GeneratedProtocolMessageType('LoginRequest', (_message.Message,), {
  'DESCRIPTOR' : _LOGINREQUEST,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.LoginRequest)
  })
_sym_db.RegisterMessage(LoginRequest)

LoginResponse = _reflection.GeneratedProtocolMessageType('LoginResponse', (_message.Message,), {
  'DESCRIPTOR' : _LOGINRESPONSE,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.LoginResponse)
  })
_sym_db.RegisterMessage(LoginResponse)

HistoryResponse = _reflection.GeneratedProtocolMessageType('HistoryResponse', (_message.Message,), {
  'DESCRIPTOR' : _HISTORYRESPONSE,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.HistoryResponse)
  })
_sym_db.RegisterMessage(HistoryResponse)

HistoryListResponse = _reflection.GeneratedProtocolMessageType('HistoryListResponse', (_message.Message,), {
  'DESCRIPTOR' : _HISTORYLISTRESPONSE,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.HistoryListResponse)
  })
_sym_db.RegisterMessage(HistoryListResponse)

CheckRequest = _reflection.GeneratedProtocolMessageType('CheckRequest', (_message.Message,), {
  'DESCRIPTOR' : _CHECKREQUEST,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.CheckRequest)
  })
_sym_db.RegisterMessage(CheckRequest)

CheckResponse = _reflection.GeneratedProtocolMessageType('CheckResponse', (_message.Message,), {
  'DESCRIPTOR' : _CHECKRESPONSE,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.CheckResponse)
  })
_sym_db.RegisterMessage(CheckResponse)

GroupCheckRequest = _reflection.GeneratedProtocolMessageType('GroupCheckRequest', (_message.Message,), {
  'DESCRIPTOR' : _GROUPCHECKREQUEST,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.GroupCheckRequest)
  })
_sym_db.RegisterMessage(GroupCheckRequest)

GroupCheckResponse = _reflection.GeneratedProtocolMessageType('GroupCheckResponse', (_message.Message,), {
  'DESCRIPTOR' : _GROUPCHECKRESPONSE,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.GroupCheckResponse)
  })
_sym_db.RegisterMessage(GroupCheckResponse)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.Empty)
  })
_sym_db.RegisterMessage(Empty)

NotificationStatus = _reflection.GeneratedProtocolMessageType('NotificationStatus', (_message.Message,), {
  'DESCRIPTOR' : _NOTIFICATIONSTATUS,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.NotificationStatus)
  })
_sym_db.RegisterMessage(NotificationStatus)

NotificationResponse = _reflection.GeneratedProtocolMessageType('NotificationResponse', (_message.Message,), {
  'DESCRIPTOR' : _NOTIFICATIONRESPONSE,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.NotificationResponse)
  })
_sym_db.RegisterMessage(NotificationResponse)

NotificationListResponse = _reflection.GeneratedProtocolMessageType('NotificationListResponse', (_message.Message,), {
  'DESCRIPTOR' : _NOTIFICATIONLISTRESPONSE,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.NotificationListResponse)
  })
_sym_db.RegisterMessage(NotificationListResponse)

NotificationRequest = _reflection.GeneratedProtocolMessageType('NotificationRequest', (_message.Message,), {
  'DESCRIPTOR' : _NOTIFICATIONREQUEST,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.NotificationRequest)
  })
_sym_db.RegisterMessage(NotificationRequest)

Filename = _reflection.GeneratedProtocolMessageType('Filename', (_message.Message,), {
  'DESCRIPTOR' : _FILENAME,
  '__module__' : 'safe_entry_pb2'
  # @@protoc_insertion_point(class_scope:safe_entry.Filename)
  })
_sym_db.RegisterMessage(Filename)

_SAFEENTRY = DESCRIPTOR.services_by_name['SafeEntry']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _STATUS._serialized_start=1047
  _STATUS._serialized_end=1120
  _USER._serialized_start=32
  _USER._serialized_end=66
  _NRIC._serialized_start=68
  _NRIC._serialized_end=88
  _NRICLIST._serialized_start=90
  _NRICLIST._serialized_end=132
  _HISTORYREQUEST._serialized_start=134
  _HISTORYREQUEST._serialized_end=164
  _LOGINREQUEST._serialized_start=166
  _LOGINREQUEST._serialized_end=194
  _LOGINRESPONSE._serialized_start=196
  _LOGINRESPONSE._serialized_end=247
  _HISTORYRESPONSE._serialized_start=249
  _HISTORYRESPONSE._serialized_end=343
  _HISTORYLISTRESPONSE._serialized_start=345
  _HISTORYLISTRESPONSE._serialized_end=424
  _CHECKREQUEST._serialized_start=426
  _CHECKREQUEST._serialized_end=549
  _CHECKRESPONSE._serialized_start=551
  _CHECKRESPONSE._serialized_end=602
  _GROUPCHECKREQUEST._serialized_start=604
  _GROUPCHECKREQUEST._serialized_end=703
  _GROUPCHECKRESPONSE._serialized_start=705
  _GROUPCHECKRESPONSE._serialized_end=793
  _EMPTY._serialized_start=795
  _EMPTY._serialized_end=802
  _NOTIFICATIONSTATUS._serialized_start=804
  _NOTIFICATIONSTATUS._serialized_end=860
  _NOTIFICATIONRESPONSE._serialized_start=862
  _NOTIFICATIONRESPONSE._serialized_end=901
  _NOTIFICATIONLISTRESPONSE._serialized_start=903
  _NOTIFICATIONLISTRESPONSE._serialized_end=946
  _NOTIFICATIONREQUEST._serialized_start=948
  _NOTIFICATIONREQUEST._serialized_end=1015
  _FILENAME._serialized_start=1017
  _FILENAME._serialized_end=1045
  _SAFEENTRY._serialized_start=1123
  _SAFEENTRY._serialized_end=2078
# @@protoc_insertion_point(module_scope)
