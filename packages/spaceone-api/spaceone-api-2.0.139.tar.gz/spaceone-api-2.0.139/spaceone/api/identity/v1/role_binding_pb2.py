# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/identity/v1/role_binding.proto
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
from spaceone.api.core.v1 import query_pb2 as spaceone_dot_api_dot_core_dot_v1_dot_query__pb2
from spaceone.api.identity.v1 import project_pb2 as spaceone_dot_api_dot_identity_dot_v1_dot_project__pb2
from spaceone.api.identity.v1 import project_group_pb2 as spaceone_dot_api_dot_identity_dot_v1_dot_project__group__pb2
from spaceone.api.identity.v1 import role_pb2 as spaceone_dot_api_dot_identity_dot_v1_dot_role__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+spaceone/api/identity/v1/role_binding.proto\x12\x18spaceone.api.identity.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\x1a&spaceone/api/identity/v1/project.proto\x1a,spaceone/api/identity/v1/project_group.proto\x1a#spaceone/api/identity/v1/role.proto\"\xeb\x01\n\x18\x43reateRoleBindingRequest\x12\x15\n\rresource_type\x18\x01 \x01(\t\x12\x13\n\x0bresource_id\x18\x02 \x01(\t\x12\x0f\n\x07role_id\x18\x03 \x01(\t\x12\x12\n\nproject_id\x18\x04 \x01(\t\x12\x18\n\x10project_group_id\x18\x05 \x01(\t\x12*\n\x06labels\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12%\n\x04tags\x18\x07 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x08 \x01(\t\"\x99\x01\n\x18UpdateRoleBindingRequest\x12\x17\n\x0frole_binding_id\x18\x01 \x01(\t\x12*\n\x06labels\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12%\n\x04tags\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x04 \x01(\t\"@\n\x12RoleBindingRequest\x12\x17\n\x0frole_binding_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"Q\n\x15GetRoleBindingRequest\x12\x17\n\x0frole_binding_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t\"\x8c\x03\n\x0fRoleBindingInfo\x12\x17\n\x0frole_binding_id\x18\x01 \x01(\t\x12\x15\n\rresource_type\x18\x02 \x01(\t\x12\x13\n\x0bresource_id\x18\x03 \x01(\t\x12\x35\n\trole_info\x18\x04 \x01(\x0b\x32\".spaceone.api.identity.v1.RoleInfo\x12;\n\x0cproject_info\x18\x05 \x01(\x0b\x32%.spaceone.api.identity.v1.ProjectInfo\x12\x46\n\x12project_group_info\x18\x06 \x01(\x0b\x32*.spaceone.api.identity.v1.ProjectGroupInfo\x12*\n\x06labels\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12%\n\x04tags\x18\x08 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x0b \x01(\t\x12\x12\n\ncreated_at\x18\x15 \x01(\t\"\xe8\x01\n\x10RoleBindingQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x17\n\x0frole_binding_id\x18\x02 \x01(\t\x12\x15\n\rresource_type\x18\x03 \x01(\t\x12\x13\n\x0bresource_id\x18\x04 \x01(\t\x12\x0f\n\x07role_id\x18\x05 \x01(\t\x12\x11\n\trole_type\x18\x06 \x01(\t\x12\x12\n\nproject_id\x18\x07 \x01(\t\x12\x18\n\x10project_group_id\x18\x08 \x01(\t\x12\x11\n\tdomain_id\x18\t \x01(\t\"c\n\x10RoleBindingsInfo\x12:\n\x07results\x18\x01 \x03(\x0b\x32).spaceone.api.identity.v1.RoleBindingInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"_\n\x14RoleBindingStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t2\xce\x06\n\x0bRoleBinding\x12\x94\x01\n\x06\x63reate\x12\x32.spaceone.api.identity.v1.CreateRoleBindingRequest\x1a).spaceone.api.identity.v1.RoleBindingInfo\"+\x82\xd3\xe4\x93\x02%\" /identity/v1/role-binding/create:\x01*\x12\x94\x01\n\x06update\x12\x32.spaceone.api.identity.v1.UpdateRoleBindingRequest\x1a).spaceone.api.identity.v1.RoleBindingInfo\"+\x82\xd3\xe4\x93\x02%\" /identity/v1/role-binding/update:\x01*\x12{\n\x06\x64\x65lete\x12,.spaceone.api.identity.v1.RoleBindingRequest\x1a\x16.google.protobuf.Empty\"+\x82\xd3\xe4\x93\x02%\" /identity/v1/role-binding/delete:\x01*\x12\x8b\x01\n\x03get\x12/.spaceone.api.identity.v1.GetRoleBindingRequest\x1a).spaceone.api.identity.v1.RoleBindingInfo\"(\x82\xd3\xe4\x93\x02\"\"\x1d/identity/v1/role-binding/get:\x01*\x12\x89\x01\n\x04list\x12*.spaceone.api.identity.v1.RoleBindingQuery\x1a*.spaceone.api.identity.v1.RoleBindingsInfo\")\x82\xd3\xe4\x93\x02#\"\x1e/identity/v1/role-binding/list:\x01*\x12z\n\x04stat\x12..spaceone.api.identity.v1.RoleBindingStatQuery\x1a\x17.google.protobuf.Struct\")\x82\xd3\xe4\x93\x02#\"\x1e/identity/v1/role-binding/stat:\x01*B?Z=github.com/cloudforet-io/api/dist/go/spaceone/api/identity/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.identity.v1.role_binding_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z=github.com/cloudforet-io/api/dist/go/spaceone/api/identity/v1'
  _globals['_ROLEBINDING'].methods_by_name['create']._options = None
  _globals['_ROLEBINDING'].methods_by_name['create']._serialized_options = b'\202\323\344\223\002%\" /identity/v1/role-binding/create:\001*'
  _globals['_ROLEBINDING'].methods_by_name['update']._options = None
  _globals['_ROLEBINDING'].methods_by_name['update']._serialized_options = b'\202\323\344\223\002%\" /identity/v1/role-binding/update:\001*'
  _globals['_ROLEBINDING'].methods_by_name['delete']._options = None
  _globals['_ROLEBINDING'].methods_by_name['delete']._serialized_options = b'\202\323\344\223\002%\" /identity/v1/role-binding/delete:\001*'
  _globals['_ROLEBINDING'].methods_by_name['get']._options = None
  _globals['_ROLEBINDING'].methods_by_name['get']._serialized_options = b'\202\323\344\223\002\"\"\035/identity/v1/role-binding/get:\001*'
  _globals['_ROLEBINDING'].methods_by_name['list']._options = None
  _globals['_ROLEBINDING'].methods_by_name['list']._serialized_options = b'\202\323\344\223\002#\"\036/identity/v1/role-binding/list:\001*'
  _globals['_ROLEBINDING'].methods_by_name['stat']._options = None
  _globals['_ROLEBINDING'].methods_by_name['stat']._serialized_options = b'\202\323\344\223\002#\"\036/identity/v1/role-binding/stat:\001*'
  _globals['_CREATEROLEBINDINGREQUEST']._serialized_start=320
  _globals['_CREATEROLEBINDINGREQUEST']._serialized_end=555
  _globals['_UPDATEROLEBINDINGREQUEST']._serialized_start=558
  _globals['_UPDATEROLEBINDINGREQUEST']._serialized_end=711
  _globals['_ROLEBINDINGREQUEST']._serialized_start=713
  _globals['_ROLEBINDINGREQUEST']._serialized_end=777
  _globals['_GETROLEBINDINGREQUEST']._serialized_start=779
  _globals['_GETROLEBINDINGREQUEST']._serialized_end=860
  _globals['_ROLEBINDINGINFO']._serialized_start=863
  _globals['_ROLEBINDINGINFO']._serialized_end=1259
  _globals['_ROLEBINDINGQUERY']._serialized_start=1262
  _globals['_ROLEBINDINGQUERY']._serialized_end=1494
  _globals['_ROLEBINDINGSINFO']._serialized_start=1496
  _globals['_ROLEBINDINGSINFO']._serialized_end=1595
  _globals['_ROLEBINDINGSTATQUERY']._serialized_start=1597
  _globals['_ROLEBINDINGSTATQUERY']._serialized_end=1692
  _globals['_ROLEBINDING']._serialized_start=1695
  _globals['_ROLEBINDING']._serialized_end=2541
# @@protoc_insertion_point(module_scope)
