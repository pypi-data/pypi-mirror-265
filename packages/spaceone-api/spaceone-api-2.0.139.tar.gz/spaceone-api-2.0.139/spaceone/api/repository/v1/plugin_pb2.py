# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/repository/v1/plugin.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from spaceone.api.core.v2 import query_pb2 as spaceone_dot_api_dot_core_dot_v2_dot_query__pb2
from spaceone.api.repository.v1 import repository_pb2 as spaceone_dot_api_dot_repository_dot_v1_dot_repository__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'spaceone/api/repository/v1/plugin.proto\x12\x1aspaceone.api.repository.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v2/query.proto\x1a+spaceone/api/repository/v1/repository.proto\"\xe9\x02\n\x15RegisterPluginRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x15\n\rresource_type\x18\x02 \x01(\t\x12\r\n\x05image\x18\x03 \x01(\t\x12\x10\n\x08provider\x18\x04 \x01(\t\x12\x45\n\rregistry_type\x18\x05 \x01(\x0e\x32..spaceone.api.repository.v1.PublicRegistryType\x12\x30\n\x0fregistry_config\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\x12+\n\ncapability\x18\x07 \x01(\x0b\x32\x17.google.protobuf.Struct\x12*\n\x06labels\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12%\n\x04tags\x18\t \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tplugin_id\x18\n \x01(\t\"\xb6\x01\n\x13UpdatePluginRequest\x12\x11\n\tplugin_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12+\n\ncapability\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12*\n\x06labels\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12%\n\x04tags\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\"\"\n\rPluginRequest\x12\x11\n\tplugin_id\x18\x01 \x01(\t\"C\n\x17RepositoryPluginRequest\x12\x11\n\tplugin_id\x18\x01 \x01(\t\x12\x15\n\rrepository_id\x18\x15 \x01(\t\"\xcd\x02\n\x0bPluginQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v2.Query\x12\x11\n\tplugin_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12<\n\x05state\x18\x04 \x01(\x0e\x32-.spaceone.api.repository.v1.PluginQuery.State\x12\x15\n\rresource_type\x18\x05 \x01(\t\x12\x10\n\x08provider\x18\x06 \x01(\t\x12\x45\n\rregistry_type\x18\x07 \x01(\x0e\x32..spaceone.api.repository.v1.PublicRegistryType\x12\x15\n\rrepository_id\x18\x15 \x01(\t\",\n\x05State\x12\x08\n\x04NONE\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\x0c\n\x08\x44ISABLED\x10\x02\"\xdf\x04\n\nPluginInfo\x12\x11\n\tplugin_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12;\n\x05state\x18\x03 \x01(\x0e\x32,.spaceone.api.repository.v1.PluginInfo.State\x12\x15\n\rresource_type\x18\x04 \x01(\t\x12\r\n\x05image\x18\x05 \x01(\t\x12\x10\n\x08provider\x18\x06 \x01(\t\x12\x45\n\rregistry_type\x18\x07 \x01(\x0e\x32..spaceone.api.repository.v1.PublicRegistryType\x12\x14\n\x0cregistry_url\x18\x08 \x01(\t\x12\x30\n\x0fregistry_config\x18\t \x01(\x0b\x32\x17.google.protobuf.Struct\x12+\n\ncapability\x18\n \x01(\x0b\x32\x17.google.protobuf.Struct\x12*\n\x06labels\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12%\n\x04tags\x18\x0c \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x15 \x01(\t\x12\x43\n\x0frepository_info\x18\x16 \x01(\x0b\x32*.spaceone.api.repository.v1.RepositoryInfo\x12\x12\n\ncreated_at\x18\x1f \x01(\t\x12\x12\n\nupdated_at\x18  \x01(\t\",\n\x05State\x12\x08\n\x04NONE\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\x0c\n\x08\x44ISABLED\x10\x02\"[\n\x0bPluginsInfo\x12\x37\n\x07results\x18\x01 \x03(\x0b\x32&.spaceone.api.repository.v1.PluginInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"E\n\x0cVersionsInfo\x12\x0f\n\x07version\x18\x01 \x03(\t\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\x12\x0f\n\x07results\x18\x03 \x03(\t\"^\n\x0fPluginStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v2.StatisticsQuery\x12\x15\n\rrepository_id\x18\x02 \x01(\t*i\n\x12PublicRegistryType\x12\x16\n\x12NONE_REGISTRY_TYPE\x10\x00\x12\x0e\n\nDOCKER_HUB\x10\x01\x12\x13\n\x0f\x41WS_PRIVATE_ECR\x10\x02\x12\n\n\x06HARBOR\x10\x03\x12\n\n\x06GITHUB\x10\x04\x32\xe1\x08\n\x06Plugin\x12\x90\x01\n\x08register\x12\x31.spaceone.api.repository.v1.RegisterPluginRequest\x1a&.spaceone.api.repository.v1.PluginInfo\")\x82\xd3\xe4\x93\x02#\"\x1e/repository/v1/plugin/register:\x01*\x12\x8a\x01\n\x06update\x12/.spaceone.api.repository.v1.UpdatePluginRequest\x1a&.spaceone.api.repository.v1.PluginInfo\"\'\x82\xd3\xe4\x93\x02!\"\x1c/repository/v1/plugin/update:\x01*\x12|\n\nderegister\x12).spaceone.api.repository.v1.PluginRequest\x1a\x16.google.protobuf.Empty\"+\x82\xd3\xe4\x93\x02%\" /repository/v1/plugin/deregister:\x01*\x12\x84\x01\n\x06\x65nable\x12).spaceone.api.repository.v1.PluginRequest\x1a&.spaceone.api.repository.v1.PluginInfo\"\'\x82\xd3\xe4\x93\x02!\"\x1c/repository/v1/plugin/enable:\x01*\x12\x86\x01\n\x07\x64isable\x12).spaceone.api.repository.v1.PluginRequest\x1a&.spaceone.api.repository.v1.PluginInfo\"(\x82\xd3\xe4\x93\x02\"\"\x1d/repository/v1/plugin/disable:\x01*\x12\x9c\x01\n\x0cget_versions\x12\x33.spaceone.api.repository.v1.RepositoryPluginRequest\x1a(.spaceone.api.repository.v1.VersionsInfo\"-\x82\xd3\xe4\x93\x02\'\"\"/repository/v1/plugin/get-versions:\x01*\x12\x88\x01\n\x03get\x12\x33.spaceone.api.repository.v1.RepositoryPluginRequest\x1a&.spaceone.api.repository.v1.PluginInfo\"$\x82\xd3\xe4\x93\x02\x1e\"\x19/repository/v1/plugin/get:\x01*\x12\x7f\n\x04list\x12\'.spaceone.api.repository.v1.PluginQuery\x1a\'.spaceone.api.repository.v1.PluginsInfo\"%\x82\xd3\xe4\x93\x02\x1f\"\x1a/repository/v1/plugin/list:\x01*BAZ?github.com/cloudforet-io/api/dist/go/spaceone/api/repository/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.repository.v1.plugin_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z?github.com/cloudforet-io/api/dist/go/spaceone/api/repository/v1'
  _globals['_PLUGIN'].methods_by_name['register']._options = None
  _globals['_PLUGIN'].methods_by_name['register']._serialized_options = b'\202\323\344\223\002#\"\036/repository/v1/plugin/register:\001*'
  _globals['_PLUGIN'].methods_by_name['update']._options = None
  _globals['_PLUGIN'].methods_by_name['update']._serialized_options = b'\202\323\344\223\002!\"\034/repository/v1/plugin/update:\001*'
  _globals['_PLUGIN'].methods_by_name['deregister']._options = None
  _globals['_PLUGIN'].methods_by_name['deregister']._serialized_options = b'\202\323\344\223\002%\" /repository/v1/plugin/deregister:\001*'
  _globals['_PLUGIN'].methods_by_name['enable']._options = None
  _globals['_PLUGIN'].methods_by_name['enable']._serialized_options = b'\202\323\344\223\002!\"\034/repository/v1/plugin/enable:\001*'
  _globals['_PLUGIN'].methods_by_name['disable']._options = None
  _globals['_PLUGIN'].methods_by_name['disable']._serialized_options = b'\202\323\344\223\002\"\"\035/repository/v1/plugin/disable:\001*'
  _globals['_PLUGIN'].methods_by_name['get_versions']._options = None
  _globals['_PLUGIN'].methods_by_name['get_versions']._serialized_options = b'\202\323\344\223\002\'\"\"/repository/v1/plugin/get-versions:\001*'
  _globals['_PLUGIN'].methods_by_name['get']._options = None
  _globals['_PLUGIN'].methods_by_name['get']._serialized_options = b'\202\323\344\223\002\036\"\031/repository/v1/plugin/get:\001*'
  _globals['_PLUGIN'].methods_by_name['list']._options = None
  _globals['_PLUGIN'].methods_by_name['list']._serialized_options = b'\202\323\344\223\002\037\"\032/repository/v1/plugin/list:\001*'
  _globals['_PUBLICREGISTRYTYPE']._serialized_start=2099
  _globals['_PUBLICREGISTRYTYPE']._serialized_end=2204
  _globals['_REGISTERPLUGINREQUEST']._serialized_start=240
  _globals['_REGISTERPLUGINREQUEST']._serialized_end=601
  _globals['_UPDATEPLUGINREQUEST']._serialized_start=604
  _globals['_UPDATEPLUGINREQUEST']._serialized_end=786
  _globals['_PLUGINREQUEST']._serialized_start=788
  _globals['_PLUGINREQUEST']._serialized_end=822
  _globals['_REPOSITORYPLUGINREQUEST']._serialized_start=824
  _globals['_REPOSITORYPLUGINREQUEST']._serialized_end=891
  _globals['_PLUGINQUERY']._serialized_start=894
  _globals['_PLUGINQUERY']._serialized_end=1227
  _globals['_PLUGINQUERY_STATE']._serialized_start=1183
  _globals['_PLUGINQUERY_STATE']._serialized_end=1227
  _globals['_PLUGININFO']._serialized_start=1230
  _globals['_PLUGININFO']._serialized_end=1837
  _globals['_PLUGININFO_STATE']._serialized_start=1183
  _globals['_PLUGININFO_STATE']._serialized_end=1227
  _globals['_PLUGINSINFO']._serialized_start=1839
  _globals['_PLUGINSINFO']._serialized_end=1930
  _globals['_VERSIONSINFO']._serialized_start=1932
  _globals['_VERSIONSINFO']._serialized_end=2001
  _globals['_PLUGINSTATQUERY']._serialized_start=2003
  _globals['_PLUGINSTATQUERY']._serialized_end=2097
  _globals['_PLUGIN']._serialized_start=2207
  _globals['_PLUGIN']._serialized_end=3328
# @@protoc_insertion_point(module_scope)
