# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/monitoring/plugin/log.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(spaceone/api/monitoring/plugin/log.proto\x12\x1espaceone.api.monitoring.plugin\x1a\x1cgoogle/protobuf/struct.proto\"!\n\x04Sort\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x65sc\x18\x02 \x01(\x08\"\x8c\x02\n\nLogRequest\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12,\n\x0bsecret_data\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0e\n\x06schema\x18\x03 \x01(\t\x12&\n\x05query\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0f\n\x07keyword\x18\x05 \x01(\t\x12\r\n\x05start\x18\n \x01(\t\x12\x0b\n\x03\x65nd\x18\x0b \x01(\t\x12\x32\n\x04sort\x18\x0c \x01(\x0b\x32$.spaceone.api.monitoring.plugin.Sort\x12\r\n\x05limit\x18\r \x01(\x05\"8\n\x0cLogsDataInfo\x12(\n\x07results\x18\x01 \x03(\x0b\x32\x17.google.protobuf.Struct2k\n\x03Log\x12\x64\n\x04list\x12*.spaceone.api.monitoring.plugin.LogRequest\x1a,.spaceone.api.monitoring.plugin.LogsDataInfo\"\x00\x30\x01\x42\x45ZCgithub.com/cloudforet-io/api/dist/go/spaceone/api/monitoring/pluginb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.monitoring.plugin.log_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZCgithub.com/cloudforet-io/api/dist/go/spaceone/api/monitoring/plugin'
  _globals['_SORT']._serialized_start=106
  _globals['_SORT']._serialized_end=139
  _globals['_LOGREQUEST']._serialized_start=142
  _globals['_LOGREQUEST']._serialized_end=410
  _globals['_LOGSDATAINFO']._serialized_start=412
  _globals['_LOGSDATAINFO']._serialized_end=468
  _globals['_LOG']._serialized_start=470
  _globals['_LOG']._serialized_end=577
# @@protoc_insertion_point(module_scope)
