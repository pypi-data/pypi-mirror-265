# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: block_bloom_filter.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import hash_pb2 as hash__pb2
from . import pb_util_pb2 as pb__util__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18\x62lock_bloom_filter.proto\x12\x04kudu\x1a\nhash.proto\x1a\rpb_util.proto\"\xab\x01\n\x12\x42lockBloomFilterPB\x12\x17\n\x0flog_space_bytes\x18\x01 \x01(\x05\x12\x18\n\nbloom_data\x18\x02 \x01(\x0c\x42\x04\x88\xb5\x18\x01\x12\x14\n\x0c\x61lways_false\x18\x03 \x01(\x08\x12\x36\n\x0ehash_algorithm\x18\x04 \x01(\x0e\x32\x13.kudu.HashAlgorithm:\tFAST_HASH\x12\x14\n\thash_seed\x18\x05 \x01(\r:\x01\x30\x42\x11\n\x0forg.apache.kudu')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'block_bloom_filter_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\017org.apache.kudu'
  _globals['_BLOCKBLOOMFILTERPB'].fields_by_name['bloom_data']._options = None
  _globals['_BLOCKBLOOMFILTERPB'].fields_by_name['bloom_data']._serialized_options = b'\210\265\030\001'
  _globals['_BLOCKBLOOMFILTERPB']._serialized_start=62
  _globals['_BLOCKBLOOMFILTERPB']._serialized_end=233
# @@protoc_insertion_point(module_scope)
