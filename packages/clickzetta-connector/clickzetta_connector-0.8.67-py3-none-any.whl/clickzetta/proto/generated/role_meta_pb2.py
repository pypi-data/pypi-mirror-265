# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: role_meta.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0frole_meta.proto\x12\x08\x63z.proto\"[\n\x04Role\x12\r\n\x05\x61lias\x18\x01 \x01(\t\x12 \n\x04type\x18\x02 \x01(\x0e\x32\x12.cz.proto.RoleType\x12\"\n\x05level\x18\x03 \x01(\x0e\x32\x13.cz.proto.RoleLevel*+\n\x08RoleType\x12\r\n\tRT_SYSTEM\x10\x00\x12\x10\n\x0cRT_CUSTOMIZE\x10\x01*,\n\tRoleLevel\x12\r\n\tRL_SYSTEM\x10\x00\x12\x10\n\x0cRL_WORKSPACE\x10\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'role_meta_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ROLETYPE']._serialized_start=122
  _globals['_ROLETYPE']._serialized_end=165
  _globals['_ROLELEVEL']._serialized_start=167
  _globals['_ROLELEVEL']._serialized_end=211
  _globals['_ROLE']._serialized_start=29
  _globals['_ROLE']._serialized_end=120
# @@protoc_insertion_point(module_scope)
