# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/monitoring/v1/alert.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&spaceone/api/monitoring/v1/alert.proto\x12\x1aspaceone.api.monitoring.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v2/query.proto\"I\n\rAlertResource\x12\x13\n\x0bresource_id\x18\x01 \x01(\t\x12\x15\n\rresource_type\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\"\x99\x01\n\x12\x43reateAlertRequest\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x10\n\x08\x61ssignee\x18\x03 \x01(\t\x12\x39\n\x07urgency\x18\x04 \x01(\x0e\x32(.spaceone.api.monitoring.v1.AlertUrgency\x12\x12\n\nproject_id\x18\x05 \x01(\t\"\xc3\x01\n\x12UpdateAlertRequest\x12\x10\n\x08\x61lert_id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\r\n\x05state\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x19\n\x11reset_description\x18\x0c \x01(\x08\x12\x39\n\x07urgency\x18\x05 \x01(\x0e\x32(.spaceone.api.monitoring.v1.AlertUrgency\x12\x12\n\nproject_id\x18\x15 \x01(\t\"N\n\x17UpdateAlertStateRequest\x12\x10\n\x08\x61lert_id\x18\x01 \x01(\t\x12\x12\n\naccess_key\x18\x02 \x01(\t\x12\r\n\x05state\x18\x03 \x01(\t\"7\n\x11\x41ssignUserRequest\x12\x10\n\x08\x61lert_id\x18\x01 \x01(\t\x12\x10\n\x08\x61ssignee\x18\x02 \x01(\t\" \n\x0c\x41lertRequest\x12\x10\n\x08\x61lert_id\x18\x01 \x01(\t\"\xaf\x03\n\nAlertQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v2.Query\x12\x14\n\x0c\x61lert_number\x18\x02 \x01(\x05\x12\x10\n\x08\x61lert_id\x18\x03 \x01(\t\x12\r\n\x05title\x18\x04 \x01(\t\x12\x35\n\x05state\x18\x05 \x01(\x0e\x32&.spaceone.api.monitoring.v1.AlertState\x12\x10\n\x08\x61ssignee\x18\x06 \x01(\t\x12\x39\n\x07urgency\x18\x07 \x01(\x0e\x32(.spaceone.api.monitoring.v1.AlertUrgency\x12\x10\n\x08severity\x18\x08 \x01(\t\x12\x13\n\x0bresource_id\x18\n \x01(\t\x12\x10\n\x08provider\x18\x0b \x01(\t\x12\x0f\n\x07\x61\x63\x63ount\x18\x0c \x01(\t\x12\x14\n\x0ctriggered_by\x18\r \x01(\t\x12\x14\n\x0cworkspace_id\x18\x15 \x01(\t\x12\x12\n\nproject_id\x18\x16 \x01(\t\x12\x12\n\nwebhook_id\x18\x17 \x01(\t\x12\x1c\n\x14\x65scalation_policy_id\x18\x18 \x01(\t\"\xc2\x05\n\tAlertInfo\x12\x14\n\x0c\x61lert_number\x18\x01 \x01(\x05\x12\x10\n\x08\x61lert_id\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\x12\x35\n\x05state\x18\x04 \x01(\x0e\x32&.spaceone.api.monitoring.v1.AlertState\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x10\n\x08\x61ssignee\x18\x06 \x01(\t\x12\x39\n\x07urgency\x18\x07 \x01(\x0e\x32(.spaceone.api.monitoring.v1.AlertUrgency\x12\x10\n\x08severity\x18\x08 \x01(\t\x12\x0c\n\x04rule\x18\t \x01(\t\x12\x11\n\timage_url\x18\n \x01(\t\x12;\n\x08resource\x18\x0b \x01(\x0b\x32).spaceone.api.monitoring.v1.AlertResource\x12\x10\n\x08provider\x18\x0c \x01(\t\x12\x0f\n\x07\x61\x63\x63ount\x18\r \x01(\t\x12\x30\n\x0f\x61\x64\x64itional_info\x18\x0e \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x17\n\x0f\x65scalation_step\x18\x0f \x01(\x05\x12\x16\n\x0e\x65scalation_ttl\x18\x10 \x01(\x05\x12\x14\n\x0ctriggered_by\x18\x11 \x01(\t\x12\x11\n\tdomain_id\x18\x15 \x01(\t\x12\x14\n\x0cworkspace_id\x18\x16 \x01(\t\x12\x12\n\nproject_id\x18\x17 \x01(\t\x12\x12\n\nwebhook_id\x18\x18 \x01(\t\x12\x1c\n\x14\x65scalation_policy_id\x18\x19 \x01(\t\x12\x12\n\ncreated_at\x18\x1f \x01(\t\x12\x12\n\nupdated_at\x18  \x01(\t\x12\x17\n\x0f\x61\x63knowledged_at\x18! \x01(\t\x12\x13\n\x0bresolved_at\x18\" \x01(\t\x12\x14\n\x0c\x65scalated_at\x18# \x01(\t\"Y\n\nAlertsInfo\x12\x36\n\x07results\x18\x01 \x03(\x0b\x32%.spaceone.api.monitoring.v1.AlertInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"F\n\x0e\x41lertStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v2.StatisticsQuery*9\n\x0c\x41lertUrgency\x12\x16\n\x12\x41LERT_URGENCY_NONE\x10\x00\x12\x08\n\x04HIGH\x10\x01\x12\x07\n\x03LOW\x10\x02*\\\n\nAlertState\x12\x14\n\x10\x41LERT_STATE_NONE\x10\x00\x12\r\n\tTRIGGERED\x10\x01\x12\x10\n\x0c\x41\x43KNOWLEDGED\x10\x02\x12\x0c\n\x08RESOLVED\x10\x03\x12\t\n\x05\x45RROR\x10\x04\x32\xfe\x07\n\x05\x41lert\x12\x87\x01\n\x06\x63reate\x12..spaceone.api.monitoring.v1.CreateAlertRequest\x1a%.spaceone.api.monitoring.v1.AlertInfo\"&\x82\xd3\xe4\x93\x02 \"\x1b/monitoring/v1/alert/create:\x01*\x12\x87\x01\n\x06update\x12..spaceone.api.monitoring.v1.UpdateAlertRequest\x1a%.spaceone.api.monitoring.v1.AlertInfo\"&\x82\xd3\xe4\x93\x02 \"\x1b/monitoring/v1/alert/update:\x01*\x12\x90\x01\n\x0b\x61ssign_user\x12-.spaceone.api.monitoring.v1.AssignUserRequest\x1a%.spaceone.api.monitoring.v1.AlertInfo\"+\x82\xd3\xe4\x93\x02%\" /monitoring/v1/alert/assign-user:\x01*\x12l\n\x0cupdate_state\x12\x33.spaceone.api.monitoring.v1.UpdateAlertStateRequest\x1a%.spaceone.api.monitoring.v1.AlertInfo\"\x00\x12r\n\x06\x64\x65lete\x12(.spaceone.api.monitoring.v1.AlertRequest\x1a\x16.google.protobuf.Empty\"&\x82\xd3\xe4\x93\x02 \"\x1b/monitoring/v1/alert/delete:\x01*\x12{\n\x03get\x12(.spaceone.api.monitoring.v1.AlertRequest\x1a%.spaceone.api.monitoring.v1.AlertInfo\"#\x82\xd3\xe4\x93\x02\x1d\"\x18/monitoring/v1/alert/get:\x01*\x12|\n\x04list\x12&.spaceone.api.monitoring.v1.AlertQuery\x1a&.spaceone.api.monitoring.v1.AlertsInfo\"$\x82\xd3\xe4\x93\x02\x1e\"\x19/monitoring/v1/alert/list:\x01*\x12q\n\x04stat\x12*.spaceone.api.monitoring.v1.AlertStatQuery\x1a\x17.google.protobuf.Struct\"$\x82\xd3\xe4\x93\x02\x1e\"\x19/monitoring/v1/alert/stat:\x01*BAZ?github.com/cloudforet-io/api/dist/go/spaceone/api/monitoring/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.monitoring.v1.alert_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z?github.com/cloudforet-io/api/dist/go/spaceone/api/monitoring/v1'
  _globals['_ALERT'].methods_by_name['create']._options = None
  _globals['_ALERT'].methods_by_name['create']._serialized_options = b'\202\323\344\223\002 \"\033/monitoring/v1/alert/create:\001*'
  _globals['_ALERT'].methods_by_name['update']._options = None
  _globals['_ALERT'].methods_by_name['update']._serialized_options = b'\202\323\344\223\002 \"\033/monitoring/v1/alert/update:\001*'
  _globals['_ALERT'].methods_by_name['assign_user']._options = None
  _globals['_ALERT'].methods_by_name['assign_user']._serialized_options = b'\202\323\344\223\002%\" /monitoring/v1/alert/assign-user:\001*'
  _globals['_ALERT'].methods_by_name['delete']._options = None
  _globals['_ALERT'].methods_by_name['delete']._serialized_options = b'\202\323\344\223\002 \"\033/monitoring/v1/alert/delete:\001*'
  _globals['_ALERT'].methods_by_name['get']._options = None
  _globals['_ALERT'].methods_by_name['get']._serialized_options = b'\202\323\344\223\002\035\"\030/monitoring/v1/alert/get:\001*'
  _globals['_ALERT'].methods_by_name['list']._options = None
  _globals['_ALERT'].methods_by_name['list']._serialized_options = b'\202\323\344\223\002\036\"\031/monitoring/v1/alert/list:\001*'
  _globals['_ALERT'].methods_by_name['stat']._options = None
  _globals['_ALERT'].methods_by_name['stat']._serialized_options = b'\202\323\344\223\002\036\"\031/monitoring/v1/alert/stat:\001*'
  _globals['_ALERTURGENCY']._serialized_start=2099
  _globals['_ALERTURGENCY']._serialized_end=2156
  _globals['_ALERTSTATE']._serialized_start=2158
  _globals['_ALERTSTATE']._serialized_end=2250
  _globals['_ALERTRESOURCE']._serialized_start=193
  _globals['_ALERTRESOURCE']._serialized_end=266
  _globals['_CREATEALERTREQUEST']._serialized_start=269
  _globals['_CREATEALERTREQUEST']._serialized_end=422
  _globals['_UPDATEALERTREQUEST']._serialized_start=425
  _globals['_UPDATEALERTREQUEST']._serialized_end=620
  _globals['_UPDATEALERTSTATEREQUEST']._serialized_start=622
  _globals['_UPDATEALERTSTATEREQUEST']._serialized_end=700
  _globals['_ASSIGNUSERREQUEST']._serialized_start=702
  _globals['_ASSIGNUSERREQUEST']._serialized_end=757
  _globals['_ALERTREQUEST']._serialized_start=759
  _globals['_ALERTREQUEST']._serialized_end=791
  _globals['_ALERTQUERY']._serialized_start=794
  _globals['_ALERTQUERY']._serialized_end=1225
  _globals['_ALERTINFO']._serialized_start=1228
  _globals['_ALERTINFO']._serialized_end=1934
  _globals['_ALERTSINFO']._serialized_start=1936
  _globals['_ALERTSINFO']._serialized_end=2025
  _globals['_ALERTSTATQUERY']._serialized_start=2027
  _globals['_ALERTSTATQUERY']._serialized_end=2097
  _globals['_ALERT']._serialized_start=2253
  _globals['_ALERT']._serialized_end=3275
# @@protoc_insertion_point(module_scope)
