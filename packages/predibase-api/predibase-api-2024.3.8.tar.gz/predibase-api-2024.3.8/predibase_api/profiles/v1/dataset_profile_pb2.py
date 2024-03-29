# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: predibase_api/profiles/v1/dataset_profile.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/predibase_api/profiles/v1/dataset_profile.proto\x12\x0f\x64\x61taset_profile\"\x8b\x02\n\x0e\x44\x61tasetProfile\x12\x11\n\ttimestamp\x18\x01 \x01(\x05\x12\x14\n\x0cnum_examples\x18\x02 \x01(\x05\x12\x12\n\nsize_bytes\x18\x03 \x01(\x01\x12\x13\n\x0bnum_samples\x18\x04 \x01(\x05\x12N\n\x10\x66\x65\x61ture_profiles\x18\x32 \x03(\x0b\x32\x34.dataset_profile.DatasetProfile.FeatureProfilesEntry\x1aW\n\x14\x46\x65\x61tureProfilesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12.\n\x05value\x18\x02 \x01(\x0b\x32\x1f.dataset_profile.FeatureProfile:\x02\x38\x01\"\xc0\x06\n\x0e\x46\x65\x61tureProfile\x12\x14\n\x0c\x66\x65\x61ture_name\x18\x01 \x01(\t\x12\x14\n\x0csource_dtype\x18\x02 \x01(\t\x12\x15\n\rshould_enable\x18\x03 \x01(\x08\x12\x1f\n\x17should_enable_reasoning\x18\x04 \x01(\t\x12\x15\n\rinferred_type\x18\x05 \x01(\t\x12\x1f\n\x17inferred_type_reasoning\x18\x06 \x01(\t\x12\x61\n\x1a\x61lternative_inferred_types\x18\x07 \x03(\x0b\x32=.dataset_profile.FeatureProfile.AlternativeInferredTypesEntry\x12P\n\x11\x63ross_correlation\x18\x08 \x03(\x0b\x32\x35.dataset_profile.FeatureProfile.CrossCorrelationEntry\x12>\n\x11per_sample_tokens\x18\t \x01(\x0b\x32#.dataset_profile.NumberDistribution\x12\x43\n\x15type_agnostic_profile\x18\x32 \x01(\x0b\x32$.dataset_profile.TypeAgnosticProfile\x12\x36\n\x0e\x62inary_profile\x18\x33 \x01(\x0b\x32\x1e.dataset_profile.BinaryProfile\x12\x36\n\x0enumber_profile\x18\x34 \x01(\x0b\x32\x1e.dataset_profile.NumberProfile\x12:\n\x10\x63\x61tegory_profile\x18\x35 \x01(\x0b\x32 .dataset_profile.CategoryProfile\x12\x32\n\x0ctext_profile\x18\x36 \x01(\x0b\x32\x1c.dataset_profile.TextProfile\x1a?\n\x1d\x41lternativeInferredTypesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x37\n\x15\x43rossCorrelationEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x01:\x02\x38\x01\"\xe8\x01\n\x13TypeAgnosticProfile\x12#\n\x16percent_missing_values\x18\x01 \x01(\x01H\x00\x88\x01\x01\x12\"\n\x15percent_unique_values\x18\x02 \x01(\x01H\x01\x88\x01\x01\x12\x1e\n\x11num_unique_values\x18\x03 \x01(\x05H\x02\x88\x01\x01\x12\x1d\n\x15sampled_unique_values\x18\x04 \x03(\tB\x19\n\x17_percent_missing_valuesB\x18\n\x16_percent_unique_valuesB\x14\n\x12_num_unique_values\"\x9e\x01\n\rBinaryProfile\x12\x12\n\ntrue_label\x18\x01 \x01(\t\x12\x13\n\x0b\x66\x61lse_label\x18\x02 \x01(\t\x12\x14\n\x0cpercent_true\x18\x03 \x01(\x01\x12\x15\n\rpercent_false\x18\x04 \x01(\x01\x12\x17\n\x0fimbalance_ratio\x18\x05 \x01(\x01\x12\x1e\n\x16\x61re_conventional_bools\x18\x06 \x01(\x08\"J\n\rNumberProfile\x12\x39\n\x0c\x64istribution\x18\x01 \x01(\x0b\x32#.dataset_profile.NumberDistribution\"*\n\x0cHistogramBin\x12\x0b\n\x03\x62in\x18\x01 \x01(\t\x12\r\n\x05\x63ount\x18\x02 \x01(\x05\"\x88\x02\n\x12NumberDistribution\x12\x0c\n\x04mean\x18\x01 \x01(\x01\x12\r\n\x05stdev\x18\x02 \x01(\x01\x12\x0b\n\x03min\x18\x03 \x01(\x01\x12\n\n\x02p1\x18\x04 \x01(\x01\x12\n\n\x02p5\x18\x05 \x01(\x01\x12\x0b\n\x03p10\x18\x06 \x01(\x01\x12\x0b\n\x03p25\x18\x07 \x01(\x01\x12\x0e\n\x06median\x18\x08 \x01(\x01\x12\x0b\n\x03p75\x18\t \x01(\x01\x12\x0b\n\x03p95\x18\n \x01(\x01\x12\x0b\n\x03p99\x18\x0b \x01(\x01\x12\x0b\n\x03max\x18\x0c \x01(\x01\x12\x35\n\x0ehistogram_bins\x18\x14 \x03(\x0b\x32\x1d.dataset_profile.HistogramBin\x12\x1b\n\x13percentage_outliers\x18\x15 \x01(\x01\"\xac\x02\n\x0f\x43\x61tegoryProfile\x12:\n\x13most_frequent_items\x18\x01 \x03(\x0b\x32\x1d.dataset_profile.FrequentItem\x12;\n\x14least_frequent_items\x18\x02 \x03(\x0b\x32\x1d.dataset_profile.FrequentItem\x12\x39\n\x12\x61ll_frequent_items\x18\x05 \x03(\x0b\x32\x1d.dataset_profile.FrequentItem\x12\x1f\n\x17majority_minority_ratio\x18\x03 \x01(\x01\x12\x44\n\x17percentage_distribution\x18\x04 \x01(\x0b\x32#.dataset_profile.NumberDistribution\"9\n\x0c\x46requentItem\x12\r\n\x05label\x18\x01 \x01(\t\x12\x1a\n\x12percent_occurrence\x18\x02 \x01(\x01\"o\n\x0bTextProfile\x12\x19\n\x11\x64\x65tected_language\x18\x01 \x01(\t\x12\x45\n\x18word_length_distribution\x18\x02 \x01(\x0b\x32#.dataset_profile.NumberDistribution\"\xb3\x01\n\x0b\x44\x61teProfile\x12\x15\n\rearliest_date\x18\x01 \x01(\t\x12\x13\n\x0blatest_date\x18\x02 \x01(\t\x12\x38\n\x0f\x64\x61te_resolution\x18\x03 \x01(\x0e\x32\x1f.dataset_profile.DateResolution\x12>\n\x11\x64\x61te_distribution\x18\x04 \x01(\x0b\x32#.dataset_profile.NumberDistribution*\xd4\x01\n\x0e\x44\x61teResolution\x12\x1f\n\x1b\x44\x41TE_RESOLUTION_UNSPECIFIED\x10\x00\x12\x18\n\x14\x44\x41TE_RESOLUTION_YEAR\x10\x01\x12\x19\n\x15\x44\x41TE_RESOLUTION_MONTH\x10\x02\x12\x17\n\x13\x44\x41TE_RESOLUTION_DAY\x10\x03\x12\x19\n\x15\x44\x41TE_RESOLUTION_HOURS\x10\x04\x12\x1b\n\x17\x44\x41TE_RESOLUTION_MINUTES\x10\x05\x12\x1b\n\x17\x44\x41TE_RESOLUTION_SECONDS\x10\x06\x42\x30Z.github.com/predibase/predibase_api/profiles/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'predibase_api.profiles.v1.dataset_profile_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z.github.com/predibase/predibase_api/profiles/v1'
  _globals['_DATASETPROFILE_FEATUREPROFILESENTRY']._loaded_options = None
  _globals['_DATASETPROFILE_FEATUREPROFILESENTRY']._serialized_options = b'8\001'
  _globals['_FEATUREPROFILE_ALTERNATIVEINFERREDTYPESENTRY']._loaded_options = None
  _globals['_FEATUREPROFILE_ALTERNATIVEINFERREDTYPESENTRY']._serialized_options = b'8\001'
  _globals['_FEATUREPROFILE_CROSSCORRELATIONENTRY']._loaded_options = None
  _globals['_FEATUREPROFILE_CROSSCORRELATIONENTRY']._serialized_options = b'8\001'
  _globals['_DATERESOLUTION']._serialized_start=2614
  _globals['_DATERESOLUTION']._serialized_end=2826
  _globals['_DATASETPROFILE']._serialized_start=69
  _globals['_DATASETPROFILE']._serialized_end=336
  _globals['_DATASETPROFILE_FEATUREPROFILESENTRY']._serialized_start=249
  _globals['_DATASETPROFILE_FEATUREPROFILESENTRY']._serialized_end=336
  _globals['_FEATUREPROFILE']._serialized_start=339
  _globals['_FEATUREPROFILE']._serialized_end=1171
  _globals['_FEATUREPROFILE_ALTERNATIVEINFERREDTYPESENTRY']._serialized_start=1051
  _globals['_FEATUREPROFILE_ALTERNATIVEINFERREDTYPESENTRY']._serialized_end=1114
  _globals['_FEATUREPROFILE_CROSSCORRELATIONENTRY']._serialized_start=1116
  _globals['_FEATUREPROFILE_CROSSCORRELATIONENTRY']._serialized_end=1171
  _globals['_TYPEAGNOSTICPROFILE']._serialized_start=1174
  _globals['_TYPEAGNOSTICPROFILE']._serialized_end=1406
  _globals['_BINARYPROFILE']._serialized_start=1409
  _globals['_BINARYPROFILE']._serialized_end=1567
  _globals['_NUMBERPROFILE']._serialized_start=1569
  _globals['_NUMBERPROFILE']._serialized_end=1643
  _globals['_HISTOGRAMBIN']._serialized_start=1645
  _globals['_HISTOGRAMBIN']._serialized_end=1687
  _globals['_NUMBERDISTRIBUTION']._serialized_start=1690
  _globals['_NUMBERDISTRIBUTION']._serialized_end=1954
  _globals['_CATEGORYPROFILE']._serialized_start=1957
  _globals['_CATEGORYPROFILE']._serialized_end=2257
  _globals['_FREQUENTITEM']._serialized_start=2259
  _globals['_FREQUENTITEM']._serialized_end=2316
  _globals['_TEXTPROFILE']._serialized_start=2318
  _globals['_TEXTPROFILE']._serialized_end=2429
  _globals['_DATEPROFILE']._serialized_start=2432
  _globals['_DATEPROFILE']._serialized_end=2611
# @@protoc_insertion_point(module_scope)
