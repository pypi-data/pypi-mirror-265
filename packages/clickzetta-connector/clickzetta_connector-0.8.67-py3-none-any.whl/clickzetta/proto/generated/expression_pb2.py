# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: expression.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import data_type_pb2 as data__type__pb2
from . import property_pb2 as property__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x65xpression.proto\x12\x08\x63z.proto\x1a\x0f\x64\x61ta_type.proto\x1a\x0eproperty.proto\"1\n\x0fIntervalDayTime\x12\x0f\n\x07seconds\x18\x01 \x01(\x03\x12\r\n\x05nanos\x18\x02 \x01(\x05\"2\n\nArrayValue\x12$\n\x08\x65lements\x18\x01 \x03(\x0b\x32\x12.cz.proto.Constant\"P\n\x08MapValue\x12 \n\x04keys\x18\x01 \x03(\x0b\x32\x12.cz.proto.Constant\x12\"\n\x06values\x18\x02 \x03(\x0b\x32\x12.cz.proto.Constant\"1\n\x0bStructValue\x12\"\n\x06\x66ields\x18\x01 \x03(\x0b\x32\x12.cz.proto.Constant\"\xe6\x03\n\x08\x43onstant\x12\x0e\n\x04null\x18\x01 \x01(\x08H\x00\x12\x11\n\x07tinyint\x18\x02 \x01(\x05H\x00\x12\x12\n\x08smallInt\x18\x03 \x01(\x05H\x00\x12\r\n\x03int\x18\x04 \x01(\x05H\x00\x12\x10\n\x06\x62igint\x18\x05 \x01(\x03H\x00\x12\x0f\n\x05\x66loat\x18\x06 \x01(\x02H\x00\x12\x10\n\x06\x64ouble\x18\x07 \x01(\x01H\x00\x12\x11\n\x07\x64\x65\x63imal\x18\x08 \x01(\tH\x00\x12\x11\n\x07\x62oolean\x18\t \x01(\x08H\x00\x12\x0e\n\x04\x63har\x18\n \x01(\tH\x00\x12\x11\n\x07varchar\x18\x0b \x01(\tH\x00\x12\x10\n\x06string\x18\x0c \x01(\tH\x00\x12\x10\n\x06\x62inary\x18\r \x01(\x0cH\x00\x12\x0e\n\x04\x64\x61te\x18\x0e \x01(\x05H\x00\x12\x13\n\ttimestamp\x18\x0f \x01(\x03H\x00\x12\x1b\n\x11IntervalYearMonth\x18\x10 \x01(\x03H\x00\x12\x34\n\x0fIntervalDayTime\x18\x11 \x01(\x0b\x32\x19.cz.proto.IntervalDayTimeH\x00\x12%\n\x05\x61rray\x18\x64 \x01(\x0b\x32\x14.cz.proto.ArrayValueH\x00\x12!\n\x03map\x18\x65 \x01(\x0b\x32\x12.cz.proto.MapValueH\x00\x12\'\n\x06struct\x18\x66 \x01(\x0b\x32\x15.cz.proto.StructValueH\x00\x42\x07\n\x05value\"m\n\tReference\x12\n\n\x02id\x18\x01 \x01(\x04\x12\r\n\x05local\x18\x02 \x01(\x08\x12\x0c\n\x04\x66rom\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12)\n\x08ref_type\x18\x05 \x01(\x0e\x32\x17.cz.proto.ReferenceType\"\xda\x01\n\x0eScalarFunction\x12\x0c\n\x04\x66rom\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07\x62uiltIn\x18\x03 \x01(\x08\x12-\n\targuments\x18\x04 \x03(\x0b\x32\x1a.cz.proto.ScalarExpression\x12(\n\nproperties\x18\x05 \x01(\x0b\x32\x14.cz.proto.Properties\x12\x10\n\x08\x65xecDesc\x18\x06 \x01(\t\x12\x30\n\x12\x66unctionProperties\x18\x07 \x01(\x0b\x32\x14.cz.proto.Properties\";\n\x0bVariableDef\x12 \n\x04type\x18\x01 \x01(\x0b\x32\x12.cz.proto.DataType\x12\n\n\x02id\x18\x02 \x01(\x04\"a\n\x0eLambdaFunction\x12%\n\x06params\x18\x01 \x03(\x0b\x32\x15.cz.proto.VariableDef\x12(\n\x04impl\x18\x02 \x01(\x0b\x32\x1a.cz.proto.ScalarExpression\"\xe9\x01\n\x10ScalarExpression\x12 \n\x04type\x18\x01 \x01(\x0b\x32\x12.cz.proto.DataType\x12&\n\x08\x63onstant\x18\x02 \x01(\x0b\x32\x12.cz.proto.ConstantH\x00\x12(\n\treference\x18\x03 \x01(\x0b\x32\x13.cz.proto.ReferenceH\x00\x12,\n\x08\x66unction\x18\x05 \x01(\x0b\x32\x18.cz.proto.ScalarFunctionH\x00\x12*\n\x06lambda\x18\x06 \x01(\x0b\x32\x18.cz.proto.LambdaFunctionH\x00\x42\x07\n\x05value*W\n\rReferenceType\x12\x11\n\rLOGICAL_FIELD\x10\x00\x12\r\n\tREF_LOCAL\x10\x01\x12\x12\n\x0ePHYSICAL_FIELD\x10\x02\x12\x10\n\x0cREF_VARIABLE\x10\x03\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'expression_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_REFERENCETYPE']._serialized_start=1516
  _globals['_REFERENCETYPE']._serialized_end=1603
  _globals['_INTERVALDAYTIME']._serialized_start=63
  _globals['_INTERVALDAYTIME']._serialized_end=112
  _globals['_ARRAYVALUE']._serialized_start=114
  _globals['_ARRAYVALUE']._serialized_end=164
  _globals['_MAPVALUE']._serialized_start=166
  _globals['_MAPVALUE']._serialized_end=246
  _globals['_STRUCTVALUE']._serialized_start=248
  _globals['_STRUCTVALUE']._serialized_end=297
  _globals['_CONSTANT']._serialized_start=300
  _globals['_CONSTANT']._serialized_end=786
  _globals['_REFERENCE']._serialized_start=788
  _globals['_REFERENCE']._serialized_end=897
  _globals['_SCALARFUNCTION']._serialized_start=900
  _globals['_SCALARFUNCTION']._serialized_end=1118
  _globals['_VARIABLEDEF']._serialized_start=1120
  _globals['_VARIABLEDEF']._serialized_end=1179
  _globals['_LAMBDAFUNCTION']._serialized_start=1181
  _globals['_LAMBDAFUNCTION']._serialized_end=1278
  _globals['_SCALAREXPRESSION']._serialized_start=1281
  _globals['_SCALAREXPRESSION']._serialized_end=1514
# @@protoc_insertion_point(module_scope)
