# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/cost_analysis/plugin/job.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+spaceone/api/cost_analysis/plugin/job.proto\x12!spaceone.api.cost_analysis.plugin\x1a\x1cgoogle/protobuf/struct.proto\"\xb9\x01\n\x0fGetTasksRequest\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12,\n\x0bsecret_data\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0e\n\x06schema\x18\x03 \x01(\t\x12\r\n\x05start\x18\x04 \x01(\t\x12\x1c\n\x14last_synchronized_at\x18\x05 \x01(\t\x12\x11\n\tdomain_id\x18\x06 \x01(\t\"9\n\x08TaskInfo\x12-\n\x0ctask_options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"R\n\x0b\x43hangedInfo\x12\r\n\x05start\x18\x01 \x01(\t\x12\x0b\n\x03\x65nd\x18\x02 \x01(\t\x12\'\n\x06\x66ilter\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\"\x88\x01\n\tTasksInfo\x12:\n\x05tasks\x18\x01 \x03(\x0b\x32+.spaceone.api.cost_analysis.plugin.TaskInfo\x12?\n\x07\x63hanged\x18\x02 \x03(\x0b\x32..spaceone.api.cost_analysis.plugin.ChangedInfo2v\n\x03Job\x12o\n\tget_tasks\x12\x32.spaceone.api.cost_analysis.plugin.GetTasksRequest\x1a,.spaceone.api.cost_analysis.plugin.TasksInfo\"\x00\x42HZFgithub.com/cloudforet-io/api/dist/go/spaceone/api/cost_analysis/pluginb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.cost_analysis.plugin.job_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZFgithub.com/cloudforet-io/api/dist/go/spaceone/api/cost_analysis/plugin'
  _globals['_GETTASKSREQUEST']._serialized_start=113
  _globals['_GETTASKSREQUEST']._serialized_end=298
  _globals['_TASKINFO']._serialized_start=300
  _globals['_TASKINFO']._serialized_end=357
  _globals['_CHANGEDINFO']._serialized_start=359
  _globals['_CHANGEDINFO']._serialized_end=441
  _globals['_TASKSINFO']._serialized_start=444
  _globals['_TASKSINFO']._serialized_end=580
  _globals['_JOB']._serialized_start=582
  _globals['_JOB']._serialized_end=700
# @@protoc_insertion_point(module_scope)
