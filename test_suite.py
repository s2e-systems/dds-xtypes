#################################################################
# Use and redistribution is source and binary forms is permitted
# subject to the OMG-DDS INTEROPERABILITY TESTING LICENSE found
# at the following URL:
#
# https://github.com/omg-dds/dds-rtps/blob/master/LICENSE.md
#
#################################################################
from rtps_test_utilities import ReturnCode
import test_suite_functions as tsf

xtypes_v2_extensibility_test_suite = {
    'ext_final_struct_1' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_f1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_f1 --data-folder data --data-file struct_num_x1 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'ext_final_struct_2' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_f1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_f2 --data-folder data --data-file struct_num_x1 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'ext_appendable_struct_1' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_a1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_a1 --data-folder data --data-file struct_num_x1 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'ext_appendable_struct_2' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_a1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_a2 --data-folder data --data-file struct_num_x1 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'ext_appendable_struct_3' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_a2 --data-folder data --data-file struct_num_x1_x2',
                  'sub-exe -S -t test -y Test::struct_a1 --data-folder data --data-file struct_num_x1 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'ext_appendable_struct_4' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_a2 --data-folder data --data-file struct_num_x1_x2',
                  'sub-exe -S -t test -y Test::struct_a3 --data-folder data --data-file struct_num_x1_x2 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'ext_appendable_struct_5' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_a3 --data-folder data --data-file struct_num_x1_x3_x2',
                  'sub-exe -S -t test -y Test::struct_a2 --data-folder data --data-file struct_num_x1_x2 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },

    'ext_mutable_struct_1' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_m1 --data-folder data --data-file struct_num_x1 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'ext_mutable_struct_2' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_m2 --data-folder data --data-file struct_num_x1 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'ext_mutable_struct_3' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m2 --data-folder data --data-file struct_num_x1_x2',
                  'sub-exe -S -t test -y Test::struct_m1 --data-folder data --data-file struct_num_x1 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'ext_mutable_struct_4' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m2 --data-folder data --data-file struct_num_x1_x2',
                  'sub-exe -S -t test -y Test::struct_m3 --data-folder data --data-file struct_num_x1_x2 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'ext_mutable_struct_5' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m3 --data-folder data --data-file struct_num_x1_x3_x2',
                  'sub-exe -S -t test -y Test::struct_m2 --data-folder data --data-file struct_num_x1_x2 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'ext_mutable_struct_6' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m2 --data-folder data --data-file struct_num_x1_x2',
                  'sub-exe -S -t test -y Test::struct_m4 --data-folder data --data-file struct_num_x1_x2 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'ext_autoid_1' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_hashid_1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_hashid_2 --data-folder data --data-file struct_num_x2'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
}


xtypes_v2_type_consistency_test_suite = {
    'tc_force_type_validation_1' : {
        'apps' : ['pub-exe -P -t test --type-folder types --type-file type_consistency                -y Test::struct_x1 --data-folder data --data-file struct_num_x1 --disable-type-info',
                  'sub-exe -S -t test --type-folder types --type-file type_consistency_force_type_val -y Test::struct_x1 --data-folder data --data-file struct_num_x1 --force-type-validation t --disable-type-info'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_force_type_validation_2' : {
        'apps' : ['pub-exe -P -t test --type-folder types --type-file type_consistency                -y Test::struct_x1 --data-folder data --data-file struct_num_x1 --disable-type-info',
                  'sub-exe -S -t test --type-folder types --type-file type_consistency_force_type_val -y Test::struct_x1 --data-folder data --data-file struct_num_x1 --force-type-validation f --disable-type-info'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_force_type_validation_3' : {
        'apps' : ['pub-exe -P -t test --type-folder types --type-file type_consistency -y Test::struct_x1 --data-folder data --data-file struct_num_x1 --disable-type-info',
                  'sub-exe -S -t test --type-folder types --type-file type_consistency_force_type_val -y Test::struct_x1 --data-folder data --data-file struct_num_x1 --force-type-validation d --disable-type-info'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_member_names_1' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::struct_x1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_x2 --data-folder data --data-file struct_num_x2 --ignore-member-names t'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_member_names_2' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::struct_x1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_x2 --data-folder data --data-file struct_num_x2 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_member_names_3' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::struct_x1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_x2 --data-folder data --data-file struct_num_x2 --ignore-member-names d'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_seq_bounds_1' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_10 --ignore-seq-bounds t'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_seq_bounds_2' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_10 --ignore-seq-bounds f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_seq_bounds_3' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_10 --ignore-seq-bounds d'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_seq_bounds_4' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::seq_int32x10 --data-folder data --data-file array_num_10 --ignore-seq-bounds t'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_seq_bounds_5' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::seq_int32x10 --data-folder data --data-file array_num_10 --ignore-seq-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_seq_bounds_6' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::seq_int32x10 --data-folder data --data-file array_num_10 --ignore-seq-bounds d'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_seq_bounds_7' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::seq_int32x10 --data-folder data --data-file array_num_10 --ignore-seq-bounds t'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_str_bounds_1' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::string10 --data-folder data --data-file strings_hello',
                  'sub-exe -S -t test -y Test::string20 --data-folder data --data-file strings_hello --ignore-str-bounds t'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_str_bounds_2' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::string10 --data-folder data --data-file strings_hello',
                  'sub-exe -S -t test -y Test::string20 --data-folder data --data-file strings_hello --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_str_bounds_3' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::string10 --data-folder data --data-file strings_hello',
                  'sub-exe -S -t test -y Test::string20 --data-folder data --data-file strings_hello --ignore-str-bounds d'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_str_bounds_4' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10 --data-folder data --data-file strings --ignore-str-bounds t'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_str_bounds_5' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10 --data-folder data --data-file strings --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_str_bounds_6' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10 --data-folder data --data-file strings --ignore-str-bounds d'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_ignore_str_bounds_7' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings_hello',
                  'sub-exe -S -t test -y Test::string10 --data-folder data --data-file strings_hello --ignore-str-bounds t'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_prevent_type_widening_1' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_f1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_f2 --data-folder data --data-file struct_num_x1 --prevent-type-widening t'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_prevent_type_widening_2' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_f1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_f2 --data-folder data --data-file struct_num_x1 --prevent-type-widening f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_prevent_type_widening_3' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_f1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_f2 --data-folder data --data-file struct_num_x1 --prevent-type-widening d'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_prevent_type_widening_4' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_a1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_a2 --data-folder data --data-file struct_num_x1 --prevent-type-widening t'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_prevent_type_widening_5' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_a1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_a2 --data-folder data --data-file struct_num_x1 --prevent-type-widening f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_prevent_type_widening_6' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_a1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_a2 --data-folder data --data-file struct_num_x1 --prevent-type-widening d'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_prevent_type_widening_7' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_m2 --data-folder data --data-file struct_num_x1 --prevent-type-widening t'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_prevent_type_widening_8' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_m2 --data-folder data --data-file struct_num_x1 --prevent-type-widening f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tc_prevent_type_widening_9' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_m2 --data-folder data --data-file struct_num_x1 --prevent-type-widening d'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
}


xtypes_v2_array_test_suite = {
    'int32[10]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::int32x10 --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between int32 arrays of the same size',
        'description' : ''
    },
    'int32[10]_int32[20]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::int32x20 --data-folder data --data-file array_num_20'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No communication between int32 arrays of different sizes (publisher bigger)',
        'description' : ''
    },
    'int32[20]_int32[10]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::int32x20 --data-folder data --data-file array_num_20'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No communication between int32 arrays of different sizes (subscriber bigger)',
        'description' : ''
    },
    'int32[10]_uint32[10]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::uint32x10 --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No communication between arrays of different types',
        'description' : ''
    },
    'int32[10][2]_int32[20]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::int32x10x2 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::int32x20 --data-folder data --data-file array_num_20'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No communication between arrays of different types',
        'description' : ''
    },
    'string10[10]_string20[10]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::string10x10 --data-folder data --data-file array_string_10',
                  'sub-exe -S -t test -y Test::string20x10 --data-folder data --data-file array_string_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'enum1[10]_enum2[10]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::enum1x10 --data-folder data --data-file array_enum_10',
                  'sub-exe -S -t test -y Test::enum2x10 --data-folder data --data-file array_enum_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'appendable_enum' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::enum1 --data-folder data --data-file enum',
                  'sub-exe -S -t test -y Test::enum2 --data-folder data --data-file enum'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'SFinal[10]_S[20]_SFinalAlt[10]_S[20]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::F_S__array10_F_S__array20_uint32 --data-folder data --data-file array_array_num_10_20',
                  'sub-exe -S -t test -y Test::F_S__array10_F_S__array20_uint32_alt --data-folder data --data-file array_array_num_10_20_alt'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'SAppendable[10]_S[20]_SAppendableAlt[10]_S[20]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::F_S__array10_A_S__array20_uint32 --data-folder data --data-file array_array_num_10_20',
                  'sub-exe -S -t test -y Test::F_S__array10_A_S__array20_uint32_alt --data-folder data --data-file array_array_num_10_20_alt'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'SMutable[10]_S[20]_SMutableAlt[10]_S[20]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::F_S__array10_M_S__array20_uint32 --data-folder data --data-file array_array_num_10_20',
                  'sub-exe -S -t test -y Test::F_S__array10_M_S__array20_uint32_alt --data-folder data --data-file array_array_num_10_20_alt'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    # # basic array (strongly assignable element type) with various dimensions
    # 'int32[10]'                           : [ 'types/arrays.xml', 'data/arrays.xml', ['-P -y Test::int32x10',       '-S -y Test::int32x10'],               [ReturnCode.OK, ReturnCode.OK] ],
    # 'int32[10]_int32[20]'                 : [ 'types/arrays.xml', 'data/arrays.xml', ['-P -y Test::int32x10',       '-S -y Test::int32x20'],               [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'int32[20]_int32[10]'                 : [ 'types/arrays.xml', 'data/arrays.xml', ['-P -y Test::int32x20',       '-S -y Test::int32x10'],               [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'int32[10]_uint32[10]'                : [ 'types/arrays.xml', 'data/arrays.xml', ['-P -y Test::int32x20',       '-S -y Test::uint32x10'],              [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # # how does one verify 'bounds[] == bounds[]' (total count? dimension by dimension?)
    # 'int32[10][2]_int32[20]'              : [ 'types/arrays.xml', 'data/arrays.xml', ['-P -y Test::int32x10x2',     '-S -y Test::int32x20'],               [ReturnCode.OK, ReturnCode.OK] ],

    # # some more arrays with 'strongly assignable' element types
    # 'string10[10]_string20[10]'           : [ 'types/arrays.xml', 'data/arrays.xml', ['-P -y Test::string10x10',    '-S -y Test::string20x10'],            [ReturnCode.OK, ReturnCode.OK] ],

    # # enums
    # 'enum1[10]_enum2[10]'                 : [ 'types/arrays.xml', 'data/arrays.xml', ['-P -y Test::enum1x10',       '-S -y Test::enum2x10'],               [ReturnCode.OK, ReturnCode.OK] ],
    # 'check'                               : [ 'types/arrays.xml', 'data/arrays.xml', ['-P -y Test::enum1',          '-S -y Test::enum2'],                  [ReturnCode.OK, ReturnCode.OK] ],

    # # array with '!strongly_assignable' element type
    # 'SFinal[10]_SFinalAlt[10]'            : [ 'types/arrays.xml', 'data/arrays.xml', ['-P -y Test::sfinalx10',      '-S -y Test::sfinalx10_alt'],          [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # # - struct element, appendable --> strongly assignable
    # 'SAppendable[10]_SAppendableAlt[10]'  : [ 'types/arrays.xml', 'data/arrays.xml', ['-P -y Test::sappendablex10', '-S -y Test::sappendablex10_alt'],     [ReturnCode.OK, ReturnCode.OK] ],

}

xtypes_v2_sequence_test_suite = {

    'seq(int32)_seq(int32,10)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::int32_unbounded --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::int32x10 --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'seq(int32)_seq(int32,10)_check_bounds' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::int32_unbounded --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::int32x10 --data-folder data --data-file array_num_10 --ignore-seq-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'seq(int32,20)_seq(int32,10)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::int32x10 --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'seq(int32,20)_seq(int32,10)_check_bounds' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::int32x10 --data-folder data --data-file array_num_10 --ignore-seq-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'seq(int32,10)_seq(int32,20)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::int32x20 --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'seq(int32,10)_seq(int32,20)_check_bounds' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::int32x20 --data-folder data --data-file array_num_10 --ignore-seq-bounds f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'seq(str10,10)_seq(str20,10)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::string10x10 --data-folder data --data-file array_string_10',
                  'sub-exe -S -t test -y Test::string20x10 --data-folder data --data-file array_string_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'seq(str20,10)_seq(str10,10)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::string20x10 --data-folder data --data-file array_string_10',
                  'sub-exe -S -t test -y Test::string10x10 --data-folder data --data-file array_string_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'seq(str20,10)_seq(str10,10)_check' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::string20x10 --data-folder data --data-file array_string_10',
                  'sub-exe -S -t test -y Test::string10x10 --data-folder data --data-file array_string_10 --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'seq(enum1)_seq(enum2)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::enum1 --data-folder data --data-file array_enum_10',
                  'sub-exe -S -t test -y Test::enum2 --data-folder data --data-file array_enum_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'seq(SFinal,10)_seq(SFinalAlt,10)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::F_S__seq10_F_S__seq20_uint32 --data-folder data --data-file array_array_num_10_20',
                  'sub-exe -S -t test -y Test::F_S__seq10_F_S__seq20_uint32_alt --data-folder data --data-file array_array_num_10_20_alt'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'seq(SAppendable,10)_seq(SAppendableAlt,10)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::F_S__seq10_A_S__seq20_uint32 --data-folder data --data-file array_array_num_10_20',
                  'sub-exe -S -t test -y Test::F_S__seq10_A_S__seq20_uint32_alt --data-folder data --data-file array_array_num_10_20_alt'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'seq(SMutable,10)_seq(SMutableAlt,10)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::F_S__seq10_M_S__seq20_uint32 --data-folder data --data-file array_array_num_10_20',
                  'sub-exe -S -t test -y Test::F_S__seq10_M_S__seq20_uint32_alt --data-folder data --data-file array_array_num_10_20_alt'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },

    # # basic array (strongly assignable element type) with various dimensions
    # 'seq(int32)_seq(int32,10)'                   : [ 'types/sequences.xml', 'data/sequences.xml', ['-P -y Test::int32',           '-S -y Test::int32x10'],                           [ReturnCode.OK, ReturnCode.OK] ],
    # 'seq(int32)_seq(int32,10)_check_bounds'      : [ 'types/sequences.xml', 'xml/sequences.xml',      ['-P -y Test::int32',           '-S -y Test::int32x10 --check-seq-bounds'],        [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # 'seq(int32,20)_seq(int32,10)'                : [ 'types/sequences.xml', 'xml/sequences.xml',      ['-P -y Test::int32x20',        '-S -y Test::int32x10'],                           [ReturnCode.OK, ReturnCode.OK] ],
    # 'seq(int32,20)_seq(int32,10)_check_bounds'   : [ 'types/sequences.xml', 'xml/sequences.xml',      ['-P -y Test::int32x20',        '-S -y Test::int32x10 --check-seq-bounds'],        [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # 'seq(int32,10)_seq(int32,20)'                : [ 'types/sequences.xml', 'data/sequences.xml', ['-P -y Test::int32x10',        '-S -y Test::int32x20'],                           [ReturnCode.OK, ReturnCode.OK] ],
    # 'seq(int32,10)_seq(int32,20)_check_bounds'   : [ 'types/sequences.xml', 'data/sequences.xml', ['-P -y Test::int32x10',        '-S -y Test::int32x20 --check-seq-bounds'],        [ReturnCode.OK, ReturnCode.OK] ],

    # # some more sequences with 'strongly assignable' element types
    # 'seq(str10,10)_seq(str20,10)'                : [ 'types/sequences.xml', 'data/sequences.xml', ['-P -y Test::string10x10',     '-S -y Test::string20x10'],                        [ReturnCode.OK, ReturnCode.OK] ],
    # 'seq(str20,10)_seq(str10,10)'                : [ 'types/sequences.xml', 'data/sequences.xml', ['-P -y Test::string20x10',     '-S -y Test::string10x10'],                        [ReturnCode.OK, ReturnCode.OK] ],
    # 'seq(str20,10)_seq(str10,10)_check'          : [ 'types/sequences.xml', 'data/sequences.xml', ['-P -y Test::string20x10',     '-S -y Test::string10x10 --check-str-bounds'],     [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # seq<enum>
    # 'seq(enum1)_seq(enum2)'                      : [ 'types/sequences.xml', 'data/sequences.xml', ['-P -y Test::enum1',           '-S -y Test::enum2'],                              [ReturnCode.OK, ReturnCode.OK] ],

    # # seq with '!strongly_assignable' element type
    # 'seq(SFinal,10)_seq(SFinalAlt,10)'           : [ 'types/sequences.xml', 'data/sequences.xml', ['-P -y Test::sfinalx10',       '-S -y Test::sfinalx10_alt'],                      [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # # - struct element, appendable --> strongly assignable
    # 'seq(SAppendable,10)_seq(SAppendableAlt,10)' : [ 'types/sequences.xml', 'data/sequences.xml', ['-P -y Test::sappendablex10',  '-S -y Test::sappendablex10_alt'],                 [ReturnCode.OK, ReturnCode.OK] ],

}

xtypes_v2_string_test_suite = {
    'string_string' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::string_unbounded --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string_unbounded --data-folder data --data-file strings'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'string_string10' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::string_unbounded --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10 --data-folder data --data-file strings'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'string_string10_check' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::string_unbounded --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10 --data-folder data --data-file strings --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'string10_string20_check' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::string10 --data-folder data --data-file strings_hello',
                  'sub-exe -S -t test -y Test::string20 --data-folder data --data-file strings_hello --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'string20_string10_check' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10 --data-folder data --data-file strings --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },

    'wstring_wstring' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::wstring_unbounded --data-folder data --data-file wstrings',
                  'sub-exe -S -t test -y Test::wstring_unbounded --data-folder data --data-file wstrings'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'wstring_wstring10' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::wstring_unbounded --data-folder data --data-file wstrings',
                  'sub-exe -S -t test -y Test::wstring10 --data-folder data --data-file wstrings'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'wstring_wstring10_check' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::wstring_unbounded --data-folder data --data-file wstrings',
                  'sub-exe -S -t test -y Test::wstring10 --data-folder data --data-file wstrings --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'wstring10_wstring20_check' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::wstring10 --data-folder data --data-file wstrings_hello',
                  'sub-exe -S -t test -y Test::wstring20 --data-folder data --data-file wstrings_hello --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'wstring20_wstring10_check' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::wstring20 --data-folder data --data-file wstrings',
                  'sub-exe -S -t test -y Test::wstring10 --data-folder data --data-file wstrings --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },

    # # string to string
    # 'string_string'            : [ 'types/strings.xml', 'data/strings.xml', ['-P -y Test::string',    '-S -y Test::string'],                                 [ReturnCode.OK, ReturnCode.OK] ],

    # # string to string10 [ ignore_string_bounds ]
    # 'string_string10'          : [ 'types/strings.xml', 'data/strings.xml', ['-P -y Test::string',    '-S -y Test::string10'],                               [ReturnCode.OK, ReturnCode.OK] ],

    # # string to string10 [ check_string_bounds ]
    # 'string_string10_check'    : [ 'types/strings.xml', 'data/strings.xml', ['-P -y Test::string',    '-S -y Test::string10 --check-str-bounds'],            [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # string10 to string20 [ check_string_bounds ]
    # 'string10_string20'        : [ 'types/strings.xml', 'data/strings.xml', ['-P -y Test::string10',  '-S -y Test::string20 --check-str-bounds'],            [ReturnCode.OK, ReturnCode.OK] ],

    # # string20 to string10 [ check_string_bounds ]
    # 'string20_string10'        : [ 'types/strings.xml', 'data/strings.xml', ['-P -y Test::string20',  '-S -y Test::string10 --check-str-bounds'],            [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],


    # # wstring to wstring
    # 'wstring_wstring'          : [ 'types/strings.xml', 'data/strings.xml', ['-P -y Test::wstring',    '-S -y Test::wstring'],                               [ReturnCode.OK, ReturnCode.OK] ],
    # # wstring to wstring10 [ ignore_wstring_bounds ]
    # 'wstring_wstring10'        : [ 'types/strings.xml', 'data/strings.xml', ['-P -y Test::wstring',    '-S -y Test::wstring10'],                             [ReturnCode.OK, ReturnCode.OK] ],

    # # wstring to wstring10 [ check_wstring_bounds ]
    # 'wstring_wstring10_check'  : [ 'types/strings.xml', 'data/strings.xml', ['-P -y Test::wstring',    '-S -y Test::wstring10 --check-str-bounds'],          [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # wstring10 to wstring20 [ check_wstring_bounds ]
    # 'wstring10_wstring20'      : [ 'types/strings.xml', 'data/strings.xml', ['-P -y Test::wstring10',  '-S -y Test::wstring20 --check-str-bounds'],          [ReturnCode.OK, ReturnCode.OK] ],

    # # wstring20 to wstring10 [ check_wstring_bounds ]
    # 'wstring20_wstring10'      : [ 'types/strings.xml', 'data/strings.xml', ['-P -y Test::wstring20',  '-S -y Test::wstring10 --check-str-bounds'],          [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
}


xtypes_v2_struct_test_suite = {

    'primitives_struct_final' : {
        'common_args' : ['--type-folder types --type-file primitives'],
        'apps' : ['pub-exe -P -t test -y Test::struct_primitives_final --data-folder data --data-file struct_primitives',
                  'sub-exe -S -t test -y Test::struct_primitives_final --data-folder data --data-file struct_primitives'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'primitives_struct_appendable' : {
        'common_args' : ['--type-folder types --type-file primitives'],
        'apps' : ['pub-exe -P -t test -y Test::struct_primitives_appendable --data-folder data --data-file struct_primitives',
                  'sub-exe -S -t test -y Test::struct_primitives_appendable --data-folder data --data-file struct_primitives'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'primitives_struct_mutable': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitives_mutable --data-folder data --data-file struct_primitives',
                 'sub-exe -S -t test -y Test::struct_primitives_mutable --data-folder data --data-file struct_primitives'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_final_appendable': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitives_final --data-folder data --data-file struct_primitives',
                 'sub-exe -S -t test -y Test::struct_primitives_appendable --data-folder data --data-file struct_primitives'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_final_mutable': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitives_final --data-folder data --data-file struct_primitives',
                 'sub-exe -S -t test -y Test::struct_primitives_mutable --data-folder data --data-file struct_primitives'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_appendable_final': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitives_appendable --data-folder data --data-file struct_primitives',
                 'sub-exe -S -t test -y Test::struct_primitives_final --data-folder data --data-file struct_primitives'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_appendable_mutable': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitives_appendable --data-folder data --data-file struct_primitives',
                 'sub-exe -S -t test -y Test::struct_primitives_mutable --data-folder data --data-file struct_primitives'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_mutable_final': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitives_mutable --data-folder data --data-file struct_primitives',
                 'sub-exe -S -t test -y Test::struct_primitives_final --data-folder data --data-file struct_primitives'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_mutable_appendable': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitives_mutable --data-folder data --data-file struct_primitives',
                 'sub-exe -S -t test -y Test::struct_primitives_appendable --data-folder data --data-file struct_primitives'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_different_ids_ok': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_1 --data-folder data --data-file struct_num_x1_x5',
                 'sub-exe -S -t test -y Test::struct_2 --data-folder data --data-file struct_num_x5'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_different_ids': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_1 --data-folder data --data-file struct_num_x1_x5',
                 'sub-exe -S -t test -y Test::struct_2 --data-folder data --data-file struct_num_x1_x5 --ignore-member-names f'
        ],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_different_names_ok': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_3 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_4 --data-folder data --data-file struct_num_x2'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_different_names': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_3 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_4 --data-folder data --data-file struct_num_x2 --ignore-member-names f'
        ],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_no_common_ids': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_5 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_6 --data-folder data --data-file struct_num_x2'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_members_assignable_1': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_mustUnderstand_1': {
        'common_args': ['--type-folder types --type-file struct_w_mustunderstand'],
        'apps': ['pub-exe -P -t test -y Test::struct_mustUnderstand --data-folder data --data-file struct_num_x1_x2',
                 'sub-exe -S -t test -y Test::struct_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_mustUnderstand_2': {
        'common_args': ['--type-folder types --type-file struct_w_mustunderstand'],
        'apps': ['pub-exe -P -t test -y Test::struct_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_mustUnderstand --data-folder data --data-file struct_num_x1_x2'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_key_1': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_1 --data-folder data --data-file struct_num_x1_x2',
                 'sub-exe -S -t test -y Test::struct_key_2 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_key_2': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_2 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_key_1 --data-folder data --data-file struct_num_x1_x2'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_key_string_1': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_string10 --data-folder data --data-file struct_str_x1',
                 'sub-exe -S -t test -y Test::struct_key_string20 --data-folder data --data-file struct_str_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_key_string_2': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_string10 --data-folder data --data-file struct_str_x1',
                 'sub-exe -S -t test -y Test::struct_key_string10 --data-folder data --data-file struct_str_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_key_string_3': {
        # CT: reader type @key has smaller string bound than writer type, I don't think should match 
        # -- i expect INCONSISTENT_TOPIC here...
        #   ignore_string_bounds is true for this test, but I still think _key_ strings should not match if reader's bound is < writer's bound
        #   maybe it is not clear exactly "where and when" the 'ignore_xyz' flags apply in the spec.
        #   [don't we try to avoid cases where multiple instances at the Writer will coalesce into one instance at the Reader?]
        # -- and, that makes me wonder about a "@try_construct(use_default) enum" as union discriminator, which could also coalesce instances
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_string20 --data-folder data --data-file struct_str_x1',
                 'sub-exe -S -t test -y Test::struct_key_string10 --data-folder data --data-file struct_str_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_key_enum_1': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_enum_1 --data-folder data --data-file struct_enum',
                 'sub-exe -S -t test -y Test::struct_key_enum_2 --data-folder data --data-file struct_enum'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_key_enum_2': {
        # CT: reader type @key has fewer enum literals than writer type, I don't think should match
        # -- i expect INCONSISTENT_TOPIC here...
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_enum_2 --data-folder data --data-file struct_enum',
                 'sub-exe -S -t test -y Test::struct_key_enum_1 --data-folder data --data-file struct_enum'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_key_seq_1': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_seq10 --data-folder data --data-file struct_seq',
                 'sub-exe -S -t test -y Test::struct_key_seq20 --data-folder data --data-file struct_seq'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_key_seq_2': {
        # CT: reader type @key has smaller seq bound than writer type, I don't think should match
        # -- i expect INCONSISTENT_TOPIC here...
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_seq20 --data-folder data --data-file struct_seq',
                 'sub-exe -S -t test -y Test::struct_key_seq10 --data-folder data --data-file struct_seq'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_key_struct_1': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_struct_1 --data-folder data --data-file struct_str_key',
                 'sub-exe -S -t test -y Test::struct_key_struct_2 --data-folder data --data-file struct_str_key'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_key_struct_2': {
        # CT: reader type @key has smaller string bound than writer type, I don't think should match 
        # -- i expect INCONSISTENT_TOPIC here...
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_struct_2 --data-folder data --data-file struct_str_key',
                 'sub-exe -S -t test -y Test::struct_key_struct_1 --data-folder data --data-file struct_str_key'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_key_union_1': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_union_1 --data-folder data --data-file struct_key_union',
                 'sub-exe -S -t test -y Test::struct_key_union_2 --data-folder data --data-file struct_key_union'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_key_union_2': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_union_2 --data-folder data --data-file struct_key_union',
                 'sub-exe -S -t test -y Test::struct_key_union_1 --data-folder data --data-file struct_key_union'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },

    # # PRIMITIVES - struct primitive members assignable
    # 'primitives_struct_final'      : [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitives_final',      '-S -y Test::struct_primitives_final'     ], [ReturnCode.OK, ReturnCode.OK] ],
    # 'primitives_struct_appendable' : [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitives_appendable', '-S -y Test::struct_primitives_appendable'], [ReturnCode.OK, ReturnCode.OK] ],
    # 'primitives_struct_mutable'    : [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitives_mutable',    '-S -y Test::struct_primitives_mutable'   ], [ReturnCode.OK, ReturnCode.OK] ],

    # # EXTENSIBILITY MUST MATCH:
    # 'struct_final_appendable'      : [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitives_final',      '-S -y Test::struct_primitives_appendable'], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_final_mutable'         : [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitives_final',      '-S -y Test::struct_primitives_mutable'],    [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_appendable_final'      : [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitives_appendable', '-S -y Test::struct_primitives_final'],      [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_appendable_mutable'    : [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitives_appendable', '-S -y Test::struct_primitives_mutable'],    [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_mutable_final'         : [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitives_mutable',    '-S -y Test::struct_primitives_final'],      [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_mutable_appendable'    : [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitives_mutable',    '-S -y Test::struct_primitives_appendable'], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # IF MEMBER NAME MATCHES, MEMBER ID MUST MATCH [can be bypassed with TypeConsistency.ignore_member_names]
    # 'struct_different_ids_ok'      : [ 'types/struct_names.xml', 'data/struct_1.xml', ['-P -y Test::struct_1',      '-S -y Test::struct_2'],                                  [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_different_ids'         : [ 'types/struct_names.xml', 'data/struct_1.xml', ['-P -y Test::struct_1',      '-S -y Test::struct_2 --check-member-names'],             [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # IF MEMBER ID MATCHES, MEMBER NAME MUST MATCH [can be bypassed with TypeConsistency.ignore_member_names]
    # 'struct_different_names_ok'    : [ 'types/struct_names.xml', 'data/struct_1.xml', ['-P -y Test::struct_3',      '-S -y Test::struct_4'],                                  [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_different_names'       : [ 'types/struct_names.xml', 'data/struct_1.xml', ['-P -y Test::struct_3',      '-S -y Test::struct_4 --check-member-names'],             [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # AT LEAST ONE MEMBER IN COMMON [ same id ]
    # 'struct_no_common_ids'         : [ 'types/struct_names.xml', 'data/struct_1.xml', ['-P -y Test::struct_5',      '-S -y Test::struct_6'],                                  [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # MEMBERS WITH MATCHING ID ARE ASSIGNABLE [KeyErased]
    # 'struct_members_assignable_1'  : [ 'types/struct_names.xml', 'data/struct_1.xml', ['-P -y Test::struct_primitive_uint8',      '-S -y Test::struct_primitive_uint16'],     [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # !OPTIONAL + MUST_UNDERSTAND MEMBER PRESENT IN ONE TYPE MUST APPEAR IN OTHER TYPE
    # 'struct_grok_1'                : [ 'types/struct_names.xml', 'data/struct_1.xml', ['-P -y Test::struct_grok_1', '-S -y Test::struct_grok_2'],                             [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_grok_2'                : [ 'types/struct_names.xml', 'data/struct_1.xml', ['-P -y Test::struct_grok_2', '-S -y Test::struct_grok_1'],                             [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # KEY MEMBERS PRESENT IN ONE TYPE APPEAR IN THE OTHER
    # 'struct_key_1'                 : [ 'types/struct_names.xml', 'data/struct_1.xml', ['-P -y Test::struct_key_1', '-S -y Test::struct_key_2'],                               [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_key_2'                 : [ 'types/struct_names.xml', 'data/struct_1.xml', ['-P -y Test::struct_key_2', '-S -y Test::struct_key_1'],                               [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # STRING KEY MEMBER IN T2 BOUND CHECK [ not bypassed with TypeConsistency.ignore_string_bounds ]
    # 'struct_key_string_1'          : [ 'types/struct_names.xml', 'data/struct_str.xml', ['-P -y Test::struct_key_string_1', '-S -y Test::struct_key_string_2'],                 [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_key_string_2'          : [ 'types/struct_names.xml', 'data/struct_str.xml', ['-P -y Test::struct_key_string_1', '-S -y Test::struct_key_string_1'],                 [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_key_string_3'          : [ 'types/struct_names.xml', 'data/struct_str.xml', ['-P -y Test::struct_key_string_2', '-S -y Test::struct_key_string_1'],                 [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # ENUM KEY MEMBER IN T2 HAVE SAME CONSTANTS
    # 'struct_key_enum_1'            : [ 'types/struct_names.xml', 'data/struct_enum.xml', ['-P -y Test::struct_key_enum_1', '-S -y Test::struct_key_enum_2'],                     [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_key_enum_2'            : [ 'types/struct_names.xml', 'data/struct_enum.xml', ['-P -y Test::struct_key_enum_2', '-S -y Test::struct_key_enum_1'],                     [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # SEQ KEY MEMBER IN T2 BOUND CHECK [ not bypassed with TypeConsistency.ignore_sequence_bounds ]
    # 'struct_key_seq_1'             : [ 'types/struct_names.xml', 'data/struct_seq.xml', ['-P -y Test::struct_key_seq_1', '-S -y Test::struct_key_seq_2'],                       [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_key_seq_2'             : [ 'types/struct_names.xml', 'data/struct_seq.xml', ['-P -y Test::struct_key_seq_2', '-S -y Test::struct_key_seq_1'],                       [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # STRUCT KEY MEMBER IN T2 CHECK KeyHolder(is-assignable-from)
    # 'struct_key_struct_1'          : [ 'types/struct_names.xml', 'data/struct_key.xml', ['-P -y Test::struct_key_struct_1', '-S -y Test::struct_key_struct_2'],                 [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_key_struct_2'          : [ 'types/struct_names.xml', 'data/struct_key.xml', ['-P -y Test::struct_key_struct_2', '-S -y Test::struct_key_struct_1'],                 [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # UNION KEY MEMBER IN T2 CHECK KeyHolder(is-assignable-from)
    # 'struct_key_union_1'           : [ 'types/struct_names.xml', 'data/struct_key_union.xml', ['-P -y Test::struct_key_union_1', '-S -y Test::struct_key_union_2'],                   [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_key_union_2'           : [ 'types/struct_names.xml', 'data/struct_key_union.xml', ['-P -y Test::struct_key_union_2', '-S -y Test::struct_key_union_1'],                   [ReturnCode.OK, ReturnCode.OK] ],

    # ad nauseam...
}

xtypes_v2_union_test_suite = {

    'union_primitives_final' : {
        'common_args' : ['--type-folder types --type-file unions'],
        'apps' : ['pub-exe -P -t test -y Test::union_primitives_final --data-folder data --data-file union_primitive',
                  'sub-exe -S -t test -y Test::union_primitives_final --data-folder data --data-file union_primitive'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'union_primitives_appendable': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_primitives_appendable --data-folder data --data-file union_primitive',
                 'sub-exe -S -t test -y Test::union_primitives_appendable --data-folder data --data-file union_primitive'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_primitives_mutable': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_primitives_mutable --data-folder data --data-file union_primitive',
                 'sub-exe -S -t test -y Test::union_primitives_mutable --data-folder data --data-file union_primitive'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_final_appendable': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_primitives_final --data-folder data --data-file union_primitive',
                 'sub-exe -S -t test -y Test::union_primitives_appendable --data-folder data --data-file union_primitive'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_final_mutable': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_primitives_final --data-folder data --data-file union_primitive',
                 'sub-exe -S -t test -y Test::union_primitives_mutable --data-folder data --data-file union_primitive'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_appendable_mutable': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_primitives_appendable --data-folder data --data-file union_primitive',
                 'sub-exe -S -t test -y Test::union_primitives_mutable --data-folder data --data-file union_primitive'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_uint32_bitmask32': {
        'common_args': [''],
        'apps': ['pub-exe -P -t test --type-folder types --type-file unions         -y Test::union_uint32    --data-folder data --data-file union_uint32',
                 'sub-exe -S -t test --type-folder types --type-file unions_bitmask -y Test::union_bitmask32 --data-folder data --data-file union_bitmask'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_uint32_bitmask16': {
        'common_args': [''],
        'apps': ['pub-exe -P -t test --type-folder types --type-file unions         -y Test::union_uint32    --data-folder data --data-file union_uint32',
                 'sub-exe -S -t test --type-folder types --type-file unions_bitmask -y Test::union_bitmask16 --data-folder data --data-file union_bitmask'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_uint32_one_key': {
        'common_args': [''],
        'apps': ['pub-exe -P -t test --type-folder types --type-file unions                   -y Test::union_uint32     --data-folder data --data-file union_uint32',
                 'sub-exe -S -t test --type-folder types --type-file unions_key_discriminator -y Test::union_uint32_key --data-folder data --data-file union_uint32'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_different_ids_1': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_1 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_2 --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_different_ids_2': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_1 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_2 --data-folder data --data-file union_x1 --ignore-member-names f'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_different_names_1': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_3 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_4 --data-folder data --data-file union_x2'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_different_names_2': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_3 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_4 --data-folder data --data-file union_x2 --ignore-member-names f'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_different_order_1': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_5 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_6 --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_different_order_2': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_5 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_6 --data-folder data --data-file union_x1 --ignore-member-names f'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_int16_int32': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_int16 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_int32 --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_int16_int32_default': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_int16         --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_int32_default --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_int32_int32_default': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_int32 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_int32_default --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_int32_default_int16': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_int32_default --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_int16 --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_int32_default_int32': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_int32_default --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_int32 --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_int32_default_int16_default': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_int32_default --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_int16_default --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_int32_default_int32_default': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_int32_default --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_int32_default --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_final_5_vs_6': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_final_5 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_final_6 --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_final_6_vs_5': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_final_6 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_final_5 --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_final_one_default_1': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_final_5 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_final_5_default --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_final_one_default_2': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_final_5_default --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_final_5 --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_appendable_one_common_1': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_appendable_a --data-folder data --data-file union_a',
                 'sub-exe -S -t test -y Test::union_appendable_b --data-folder data --data-file union_a'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_appendable_one_common_2': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_appendable_b --data-folder data --data-file union_b',
                 'sub-exe -S -t test -y Test::union_appendable_a --data-folder data --data-file union_b'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_appendable_no_common_1': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_appendable_a --data-folder data --data-file union_a',
                 'sub-exe -S -t test -y Test::union_appendable_c --data-folder data --data-file union_a'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_appendable_no_common_2': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_appendable_c --data-folder data --data-file union_c',
                 'sub-exe -S -t test -y Test::union_appendable_a --data-folder data --data-file union_c'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_appendable_no_common_w_default': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_appendable_a_default --data-folder data --data-file union_xd',
                 'sub-exe -S -t test -y Test::union_appendable_b_default --data-folder data --data-file union_xd'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_mutable_one_common': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_mutable_a --data-folder data --data-file union_a',
                 'sub-exe -S -t test -y Test::union_mutable_b --data-folder data --data-file union_a'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_mutable_no_common': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_mutable_a --data-folder data --data-file union_a',
                 'sub-exe -S -t test -y Test::union_mutable_c --data-folder data --data-file union_a'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'union_mutable_no_common_w_default': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_mutable_a_default --data-folder data --data-file union_xd',
                 'sub-exe -S -t test -y Test::union_mutable_b_default --data-folder data --data-file union_xd'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },


    # # PRIMITIVES - struct primitive members assignable
    # 'union_primitives_final'      : [ 'types/unions.xml', 'data/union_primitive.xml',   ['-P -y Test::union_primitives_final',      '-S -y Test::union_primitives_final'     ], [ReturnCode.OK, ReturnCode.OK] ],
    # 'union_primitives_appendable' : [ 'types/unions.xml', 'data/union_primitive.xml',   ['-P -y Test::union_primitives_appendable', '-S -y Test::union_primitives_appendable'], [ReturnCode.OK, ReturnCode.OK] ],
    # 'union_primitives_mutable'    : [ 'types/unions.xml', 'data/union_primitive.xml',   ['-P -y Test::union_primitives_mutable',    '-S -y Test::union_primitives_mutable'   ], [ReturnCode.OK, ReturnCode.OK] ],

    # # EXTENSIBILITY MISMATCH
    # 'union_final_appendable'      : [ 'types/unions.xml', 'data/union_primitive.xml',   ['-P -y Test::union_primitives_final',      '-S -y Test::union_primitives_appendable'], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'union_final_mutable'         : [ 'types/unions.xml', 'data/union_primitive.xml',   ['-P -y Test::union_primitives_final',      '-S -y Test::union_primitives_mutable'],    [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'union_appendable_mutable'    : [ 'types/unions.xml', 'data/union_primitive.xml',   ['-P -y Test::union_primitives_appendable', '-S -y Test::union_primitives_mutable'],    [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # DISCRIMINATORs STRONGLY ASSIGNABLE
    # 'union_uint32_bitmask32'      : [ 'types/unions.xml', 'data/union_uint32.xml',   ['-P -y Test::union_uint32',                   '-S -y Test::union_bitmask32'],          [ReturnCode.OK, ReturnCode.OK] ],
    # 'union_uint32_bitmask16'      : [ 'types/unions.xml', 'data/union_uint32.xml',   ['-P -y Test::union_uint32',                   '-S -y Test::union_bitmask16'],          [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # DISCRIMINATOR KEY IN ONE BUT NOT OTHER
    # 'union_uint32_one_key'        : [ 'types/unions.xml', 'data/union_uint32.xml',   ['-P -y Test::union_uint32',                    '-S -y Test::union_uint32_key'],        [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # IF MEMBER NAME MATCHES, MEMBER ID MUST MATCH [can be bypassed with TypeConsistency.ignore_member_names]
    # 'union_different_ids_ok'      : [ 'types/unions.xml', 'data/union_1.xml',   ['-P -y Test::union_1',      '-S -y Test::union_2'],                                    [ReturnCode.OK, ReturnCode.OK] ],
    # 'union_different_ids'         : [ 'types/unions.xml', 'data/union_1.xml',   ['-P -y Test::union_1',      '-S -y Test::union_2 --check-member-names'],               [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # IF MEMBER ID MATCHES, MEMBER NAME MUST MATCH [can be bypassed with TypeConsistency.ignore_member_names]
    # 'union_different_names_ok'    : [ 'types/unions.xml', 'data/union_1.xml',   ['-P -y Test::union_3',      '-S -y Test::union_4'],                                    [ReturnCode.OK, ReturnCode.OK] ],
    # 'union_different_names'       : [ 'types/unions.xml', 'data/union_1.xml',   ['-P -y Test::union_3',      '-S -y Test::union_4 --check-member-names'],               [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # LABELS IN T2 SELECT A T1 MEMBER, THEN T1.m1 IS ASSIGNABLE FROM T2's MEMBER
    # 'union_int16_int32'           : [ 'types/unions.xml', 'data/union_1.xml',   ['-P -y Test::union_int16',      '-S -y Test::union_int32'],                            [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'union_int16_int32_default'   : [ 'types/unions.xml', 'data/union_1.xml',   ['-P -y Test::union_int16',      '-S -y Test::union_int32_default'],                    [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'union_int32_int32_default'   : [ 'types/unions.xml', 'data/union_1.xml',   ['-P -y Test::union_int32',      '-S -y Test::union_int32_default'],                    [ReturnCode.OK, ReturnCode.OK] ],

    # # LABELS IN T1 SELECT 'default' in T2 THEN T1.m1 IS ASSIGNABLE FROM T2.default
    # 'union_int32_default_int16'   : [ 'types/unions.xml', 'data/union_1.xml',   ['-P -y Test::union_int32_default',    '-S -y Test::union_int16'],                      [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'union_int32_default_int32'   : [ 'types/unions.xml', 'data/union_1.xml',   ['-P -y Test::union_int32_default',    '-S -y Test::union_int32'],                      [ReturnCode.OK, ReturnCode.OK] ],

    # # BOTH HAVE 'default' THEN T1.default IS ASSIGNABLE FROM T2.default
    # 'union_int32_default_int16_default'  : [ 'types/unions.xml', 'data/union_1.xml', ['-P -y Test::union_int32_default',    '-S -y Test::union_int16_default'],         [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'union_int32_default_int32_default'  : [ 'types/unions.xml', 'data/union_1.xml', ['-P -y Test::union_int32_default',    '-S -y Test::union_int32_default'],         [ReturnCode.OK, ReturnCode.OK] ],

    # # EXT==FINAL: LABEL SETS MATCH EXACTLY [does this include 'default' label?]
    # 'union_final_5_vs_6'             : [ 'types/unions.xml', 'data/union_1.xml', ['-P -y Test::union_final_5',    '-S -y Test::union_final_6'],                         [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'union_final_6_vs_5'             : [ 'types/unions.xml', 'data/union_1.xml', ['-P -y Test::union_final_6',    '-S -y Test::union_final_5'],                         [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'union_final_one_default_1'      : [ 'types/unions.xml', 'data/union_1.xml', ['-P -y Test::union_final_5',    '-S -y Test::union_final_5_default'],                 [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'union_final_one_default_2'      : [ 'types/unions.xml', 'data/union_1.xml', ['-P -y Test::union_final_5_default',    '-S -y Test::union_final_5'],                 [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # # EXT==!FINAL: LABEL SETS HAVE NON-EMPTY INTERSECTION [does this include 'default' label?] [these tests are ignore_member_names=TRUE]
    # 'union_appendable_one_common_1'  : [ 'types/unions.xml', 'data/union_a.xml', ['-P -y Test::union_appendable_a',    '-S -y Test::union_appendable_b'],               [ReturnCode.OK, ReturnCode.OK] ],
    # 'union_appendable_one_common_2'  : [ 'types/unions.xml', 'data/union_b.xml', ['-P -y Test::union_appendable_b',    '-S -y Test::union_appendable_a'],               [ReturnCode.OK, ReturnCode.OK] ],
    # 'union_appendable_no_common_1'   : [ 'types/unions.xml', 'data/union_a.xml', ['-P -y Test::union_appendable_a',    '-S -y Test::union_appendable_c'],               [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'union_appendable_no_common_2'   : [ 'types/unions.xml', 'data/union_c.xml', ['-P -y Test::union_appendable_c',    '-S -y Test::union_appendable_a'],               [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'union_appendable_no_common_w_default' : [ 'types/unions.xml', 'data/union_xd.xml', ['-P -y Test::union_appendable_a_default',    '-S -y Test::union_appendable_b_default'],  [ReturnCode.OK, ReturnCode.OK] ],

    # 'union_mutable_one_common'          : [ 'types/unions.xml', 'data/union_a.xml', ['-P -y Test::union_mutable_a',    '-S -y Test::union_mutable_b'],                  [ReturnCode.OK, ReturnCode.OK] ],
    # 'union_mutable_no_common'           : [ 'types/unions.xml', 'data/union_a.xml', ['-P -y Test::union_mutable_a',    '-S -y Test::union_mutable_c'],                  [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'union_mutable_no_common_w_default' : [ 'types/unions.xml', 'data/union_xd.xml', ['-P -y Test::union_mutable_a_default',    '-S -y Test::union_mutable_b_default'],  [ReturnCode.OK, ReturnCode.OK] ],

}

xtypes_v2_primitive_test_suite = {
    ####### Test uint8 #######
    'struct_uint8_uint8' : {
        'common_args' : ['--type-folder types --type-file primitives'],
        'apps' : ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'struct_uint8_uint16' : {
        'common_args' : ['--type-folder types --type-file primitives'],
        'apps' : ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'struct_uint8_uint32' : {
        'common_args' : ['--type-folder types --type-file primitives'],
        'apps' : ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'struct_uint8_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint8_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint8_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint8_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint8_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint8_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint8_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint8_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint8_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint8_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },

    ####### Test uint16 #######

    'struct_uint16_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint16_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint16_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint16_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint16_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint16_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint16_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint16_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint16_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint16_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint16_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint16_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint16_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },

    ####### Test uint32 #######

    'struct_uint32_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint32_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint32_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint32_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint32_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint32_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint32_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint32_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint32_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint32_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint32_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint32_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint32_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },

    ####### Test uint64 #######

    'struct_uint64_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint64_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint64_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint64_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint64_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint64_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint64_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint64_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint64_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint64_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint64_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint64_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_uint64_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },

    ####### Test int8 #######

    'struct_int8_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int8_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int8_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int8_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int8_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int8_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int8_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int8_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int8_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int8_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int8_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int8_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int8_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },

    ####### Test int16 #######

    'struct_int16_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int16_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int16_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int16_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int16_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int16_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int16_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int16_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int16_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int16_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int16_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int16_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int16_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },

    ####### Test int32 #######

    'struct_int32_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int32_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int32_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int32_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int32_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int32_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int32_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int32_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int32_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int32_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int32_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int32_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int32_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },

    ####### Test int64 #######

    'struct_int64_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int64_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int64_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int64_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int64_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int64_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int64_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int64_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int64_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int64_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int64_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int64_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_int64_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },

    ####### Test float32 #######

    'struct_float32_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float32_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float32_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float32_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float32_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float32_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float32_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float32_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float32_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float32_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float32_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float32_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float32_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },

    ####### Test float64 #######

    'struct_float64_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float64_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float64_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float64_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float64_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float64_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float64_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float64_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float64_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float64_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float64_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float64_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float64_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },

    ####### Test float128 #######

    'struct_float128_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float128_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float128_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float128_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float128_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float128_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float128_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float128_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float128_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float128_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float128_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float128_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_float128_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },

    ####### Test byte #######

    'struct_byte_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_byte_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_byte_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_byte_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_byte_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_byte_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_byte_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_byte_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_byte_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_byte_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_byte_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_byte_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_byte_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },

    ####### Test char8 #######

    'struct_char8_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_char8_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_char8_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_char8_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_char8_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_char8_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_char8_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_char8_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_char8_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_char8_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_char8_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_char8_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },
    'struct_char8_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title': '',
        'description': ''
    },

    # # PRIMITIVES - struct members not assignable (various combinations)
    # 'struct_uint8_uint8'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint8', '-S -y Test::struct_primitive_uint8'     ], [ReturnCode.OK, ReturnCode.OK ] ],
    # 'struct_uint8_uint16' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint8', '-S -y Test::struct_primitive_uint16'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint8_uint32' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint8', '-S -y Test::struct_primitive_uint32'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint8_uint64' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint8', '-S -y Test::struct_primitive_uint64'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint8_int8'   :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint8', '-S -y Test::struct_primitive_int8'      ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint8_int16'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint8', '-S -y Test::struct_primitive_int16'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint8_int32'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint8', '-S -y Test::struct_primitive_int32'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint8_int64'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint8', '-S -y Test::struct_primitive_int64'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint8_float32':   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint8', '-S -y Test::struct_primitive_float32'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint8_float64':   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint8', '-S -y Test::struct_primitive_float64'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint8_float128':  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint8', '-S -y Test::struct_primitive_float128'  ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # 'struct_uint16_uint8'  :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint16', '-S -y Test::struct_primitive_uint8'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint16_uint16' :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint16', '-S -y Test::struct_primitive_uint16'   ], [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_uint16_uint32' :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint16', '-S -y Test::struct_primitive_uint32'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint16_uint64' :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint16', '-S -y Test::struct_primitive_uint64'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint16_int8'   :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint16', '-S -y Test::struct_primitive_int8'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint16_int16'  :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint16', '-S -y Test::struct_primitive_int16'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint16_int32'  :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint16', '-S -y Test::struct_primitive_int32'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint16_int64'  :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint16', '-S -y Test::struct_primitive_int64'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint16_float32':  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint16', '-S -y Test::struct_primitive_float32'  ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint16_float64':  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint16', '-S -y Test::struct_primitive_float64'  ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint16_float128': [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint16', '-S -y Test::struct_primitive_float128' ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # 'struct_uint32_uint8'  :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint32', '-S -y Test::struct_primitive_uint8'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint32_uint16' :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint32', '-S -y Test::struct_primitive_uint16'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint32_uint32' :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint32', '-S -y Test::struct_primitive_uint32'   ], [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_uint32_uint64' :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint32', '-S -y Test::struct_primitive_uint64'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint32_int8'   :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint32', '-S -y Test::struct_primitive_int8'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint32_int16'  :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint32', '-S -y Test::struct_primitive_int16'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint32_int32'  :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint32', '-S -y Test::struct_primitive_int32'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint32_int64'  :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint32', '-S -y Test::struct_primitive_int64'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint32_float32':  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint32', '-S -y Test::struct_primitive_float32'  ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint32_float64':  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint32', '-S -y Test::struct_primitive_float64'  ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint32_float128': [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint32', '-S -y Test::struct_primitive_float128' ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # 'struct_uint64_uint8'  :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint64', '-S -y Test::struct_primitive_uint8'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint64_uint16' :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint64', '-S -y Test::struct_primitive_uint16'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint64_uint32' :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint64', '-S -y Test::struct_primitive_uint32'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint64_uint64' :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint64', '-S -y Test::struct_primitive_uint64'   ], [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_uint64_int8'   :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint64', '-S -y Test::struct_primitive_int8'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint64_int16'  :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint64', '-S -y Test::struct_primitive_int16'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint64_int32'  :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint64', '-S -y Test::struct_primitive_int32'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint64_int64'  :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint64', '-S -y Test::struct_primitive_int64'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint64_float32':  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint64', '-S -y Test::struct_primitive_float32'  ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint64_float64':  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint64', '-S -y Test::struct_primitive_float64'  ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_uint64_float128': [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_uint64', '-S -y Test::struct_primitive_float128' ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # 'struct_int8_uint8'  :    [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int8', '-S -y Test::struct_primitive_uint8'      ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int8_uint16' :    [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int8', '-S -y Test::struct_primitive_uint16'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int8_uint32' :    [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int8', '-S -y Test::struct_primitive_uint32'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int8_uint64' :    [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int8', '-S -y Test::struct_primitive_uint64'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int8_int8'   :    [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int8', '-S -y Test::struct_primitive_int8'       ], [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_int8_int16'  :    [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int8', '-S -y Test::struct_primitive_int16'      ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int8_int32'  :    [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int8', '-S -y Test::struct_primitive_int32'      ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int8_int64'  :    [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int8', '-S -y Test::struct_primitive_int64'      ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int8_float32':    [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int8', '-S -y Test::struct_primitive_float32'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int8_float64':    [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int8', '-S -y Test::struct_primitive_float64'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int8_float128':   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int8', '-S -y Test::struct_primitive_float128'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # 'struct_int16_uint8'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int16', '-S -y Test::struct_primitive_uint8'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int16_uint16' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int16', '-S -y Test::struct_primitive_uint16'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int16_uint32' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int16', '-S -y Test::struct_primitive_uint32'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int16_uint64' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int16', '-S -y Test::struct_primitive_uint64'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int16_int8'   :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int16', '-S -y Test::struct_primitive_int8'      ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int16_int16'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int16', '-S -y Test::struct_primitive_int16'     ], [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_int16_int32'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int16', '-S -y Test::struct_primitive_int32'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int16_int64'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int16', '-S -y Test::struct_primitive_int64'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int16_float32':   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int16', '-S -y Test::struct_primitive_float32'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int16_float64':   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int16', '-S -y Test::struct_primitive_float64'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int16_float128':  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int16', '-S -y Test::struct_primitive_float128'  ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # 'struct_int32_uint8'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int32', '-S -y Test::struct_primitive_uint8'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int32_uint16' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int32', '-S -y Test::struct_primitive_uint16'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int32_uint32' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int32', '-S -y Test::struct_primitive_uint32'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int32_uint64' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int32', '-S -y Test::struct_primitive_uint64'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int32_int8'   :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int32', '-S -y Test::struct_primitive_int8'      ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int32_int16'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int32', '-S -y Test::struct_primitive_int16'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int32_int32'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int32', '-S -y Test::struct_primitive_int32'     ], [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_int32_int64'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int32', '-S -y Test::struct_primitive_int64'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int32_float32':   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int32', '-S -y Test::struct_primitive_float32'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int32_float64':   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int32', '-S -y Test::struct_primitive_float64'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int32_float128':  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int32', '-S -y Test::struct_primitive_float128'  ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # 'struct_int64_uint8'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int64', '-S -y Test::struct_primitive_uint8'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int64_uint16' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int64', '-S -y Test::struct_primitive_uint16'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int64_uint32' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int64', '-S -y Test::struct_primitive_uint32'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int64_uint64' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int64', '-S -y Test::struct_primitive_uint64'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int64_int8'   :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int64', '-S -y Test::struct_primitive_int8'      ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int64_int16'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int64', '-S -y Test::struct_primitive_int16'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int64_int32'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int64', '-S -y Test::struct_primitive_int32'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int64_int64'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int64', '-S -y Test::struct_primitive_int64'     ], [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_int64_float32':   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int64', '-S -y Test::struct_primitive_float32'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int64_float64':   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int64', '-S -y Test::struct_primitive_float64'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_int64_float128':  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_int64', '-S -y Test::struct_primitive_float128'  ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # 'struct_float32_uint8'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float32', '-S -y Test::struct_primitive_uint8'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float32_uint16' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float32', '-S -y Test::struct_primitive_uint16'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float32_uint32' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float32', '-S -y Test::struct_primitive_uint32'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float32_uint64' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float32', '-S -y Test::struct_primitive_uint64'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float32_int8'   :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float32', '-S -y Test::struct_primitive_int8'      ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float32_int16'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float32', '-S -y Test::struct_primitive_int16'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float32_int32'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float32', '-S -y Test::struct_primitive_int32'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float32_int64'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float32', '-S -y Test::struct_primitive_int64'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float32_float32':   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float32', '-S -y Test::struct_primitive_float32'   ], [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_float32_float64':   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float32', '-S -y Test::struct_primitive_float64'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float32_float128':  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float32', '-S -y Test::struct_primitive_float128'  ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # 'struct_float64_uint8'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float64', '-S -y Test::struct_primitive_uint8'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float64_uint16' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float64', '-S -y Test::struct_primitive_uint16'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float64_uint32' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float64', '-S -y Test::struct_primitive_uint32'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float64_uint64' :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float64', '-S -y Test::struct_primitive_uint64'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float64_int8'   :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float64', '-S -y Test::struct_primitive_int8'      ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float64_int16'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float64', '-S -y Test::struct_primitive_int16'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float64_int32'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float64', '-S -y Test::struct_primitive_int32'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float64_int64'  :   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float64', '-S -y Test::struct_primitive_int64'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float64_float32':   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float64', '-S -y Test::struct_primitive_float32'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float64_float64':   [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float64', '-S -y Test::struct_primitive_float64'   ], [ReturnCode.OK, ReturnCode.OK] ],
    # 'struct_float64_float128':  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float64', '-S -y Test::struct_primitive_float128'  ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],

    # 'struct_float128_uint8'  :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float128', '-S -y Test::struct_primitive_uint8'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float128_uint16' :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float128', '-S -y Test::struct_primitive_uint16'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float128_uint32' :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float128', '-S -y Test::struct_primitive_uint32'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float128_uint64' :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float128', '-S -y Test::struct_primitive_uint64'   ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float128_int8'   :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float128', '-S -y Test::struct_primitive_int8'     ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float128_int16'  :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float128', '-S -y Test::struct_primitive_int16'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float128_int32'  :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float128', '-S -y Test::struct_primitive_int32'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float128_int64'  :  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float128', '-S -y Test::struct_primitive_int64'    ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float128_float32':  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float128', '-S -y Test::struct_primitive_float32'  ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float128_float64':  [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float128', '-S -y Test::struct_primitive_float64'  ], [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC] ],
    # 'struct_float128_float128': [ 'types/primitives.xml', 'data/struct_primitives.xml', ['-P -y Test::struct_primitive_float128', '-S -y Test::struct_primitive_float128' ], [ReturnCode.OK, ReturnCode.OK] ],
}

xtypes_v2_tryconstruct_test_suite = {
    'tryc_seq_1' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::seq_int32x10_trim --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_seq_2' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::seq_int32x10_discard --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_seq_3' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::seq_int32x10_default --data-folder data --data-file tryconstruct/seq_num_empty'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_seq_4' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::seq_int32x10 --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },

    'tryc_str_1' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10_trim --data-folder data --data-file tryconstruct/strings_trim_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_str_2' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10_discard --data-folder data --data-file tryconstruct/strings_trim_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_str_3' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10_default --data-folder data --data-file tryconstruct/strings_default'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_str_4' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10 --data-folder data --data-file tryconstruct/strings_trim_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },

    'tryc_enum_1' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::struct_enum_1 --data-folder data --data-file tryconstruct/enum_val3',
                  'sub-exe -S -t test -y Test::struct_enum_2_discard --data-folder data --data-file tryconstruct/enum_val1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_enum_2' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::struct_enum_1 --data-folder data --data-file tryconstruct/enum_val3',
                  'sub-exe -S -t test -y Test::struct_enum_2_default --data-folder data --data-file tryconstruct/enum_val1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_enum_3' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::struct_enum_1 --data-folder data --data-file tryconstruct/enum_val3',
                  'sub-exe -S -t test -y Test::struct_enum_2 --data-folder data --data-file tryconstruct/enum_val1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },


    'tryc_union_seq_1' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::union_seq_int32x10_trim --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_union_seq_2' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::union_seq_int32x10_discard --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_union_seq_3' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::union_seq_int32x10_default --data-folder data --data-file tryconstruct/seq_num_empty'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_union_seq_4' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::union_seq_int32x10 --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },

    'tryc_union_str_1' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::union_string10_trim --data-folder data --data-file tryconstruct/strings_trim_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_union_str_2' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::union_string10_discard --data-folder data --data-file tryconstruct/strings_trim_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_union_str_3' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::union_string10_default --data-folder data --data-file tryconstruct/strings_default'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_union_str_4' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::union_string10 --data-folder data --data-file tryconstruct/strings_trim_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },

    'tryc_union_enum_1' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_enum_1 --data-folder data --data-file tryconstruct/enum_val3',
                  'sub-exe -S -t test -y Test::union_enum_2_discard --data-folder data --data-file tryconstruct/enum_val1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_union_enum_2' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_enum_1 --data-folder data --data-file tryconstruct/enum_val3',
                  'sub-exe -S -t test -y Test::union_enum_2_default --data-folder data --data-file tryconstruct/enum_val1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_union_enum_3' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_enum_1 --data-folder data --data-file tryconstruct/enum_val3',
                  'sub-exe -S -t test -y Test::union_enum_2 --data-folder data --data-file tryconstruct/enum_val1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },

    'tryc_union_enum_disc_1' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_disc_enum_1 --data-folder data --data-file tryconstruct/union_x3',
                  'sub-exe -S -t test -y Test::union_disc_enum_2_discard --data-folder data --data-file tryconstruct/union_x1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_union_enum_disc_2' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_disc_enum_1 --data-folder data --data-file tryconstruct/union_x3',
                  'sub-exe -S -t test -y Test::union_disc_enum_2_default --data-folder data --data-file tryconstruct/union_x1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },
    'tryc_union_enum_disc_3' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_disc_enum_1 --data-folder data --data-file tryconstruct/union_x3',
                  'sub-exe -S -t test -y Test::union_disc_enum_2 --data-folder data --data-file tryconstruct/union_x1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : '',
        'description' : ''
    },




    # 'tryc_union_1' : {
    #     'common_args' : ['--type-folder types --type-file try_construct'],
    #     'apps' : ['pub-exe -P -t test -y Test::union_tryconstruct_big --data-folder data --data-file tryconstruct/union_seq_num_20_x2',
    #               'sub-exe -S -t test -y Test::union_tryconstruct_small --data-folder data --data-file tryconstruct/union_seq_num_10_x2'],
    #     'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
    #     'check_function' : tsf.data_is_correct,
    #     'title' : '',
    #     'description' : ''
    # },
    # 'tryc_union_2' : {
    #     'common_args' : ['--type-folder types --type-file try_construct'],
    #     'apps' : ['pub-exe -P -t test -y Test::union_tryconstruct_big --data-folder data --data-file tryconstruct/union_seq_num_20_x3',
    #               'sub-exe -S -t test -y Test::union_tryconstruct_small --data-folder data --data-file tryconstruct/union_seq_num_10_x3'],
    #     'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
    #     'check_function' : tsf.data_is_correct,
    #     'title' : '',
    #     'description' : ''
    # },
    # 'tryc_union_3' : {
    #     'common_args' : ['--type-folder types --type-file try_construct'],
    #     'apps' : ['pub-exe -P -t test -y Test::union_tryconstruct_big --data-folder data --data-file tryconstruct/union_seq_num_20_x4',
    #               'sub-exe -S -t test -y Test::union_tryconstruct_small --data-folder data --data-file tryconstruct/union_seq_num_empty'],
    #     'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
    #     'check_function' : tsf.data_is_correct,
    #     'title' : '',
    #     'description' : ''
    # },
    # 'tryc_union_4' : {
    #     'common_args' : ['--type-folder types --type-file try_construct'],
    #     'apps' : ['pub-exe -P -t test -y Test::union_tryconstruct_big --data-folder data --data-file tryconstruct/union_str_20_x5',
    #               'sub-exe -S -t test -y Test::union_tryconstruct_small --data-folder data --data-file tryconstruct/union_str_trim10_x5'],
    #     'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
    #     'check_function' : tsf.data_is_correct,
    #     'title' : '',
    #     'description' : ''
    # },
    # 'tryc_union_5' : {
    #     'common_args' : ['--type-folder types --type-file try_construct'],
    #     'apps' : ['pub-exe -P -t test -y Test::union_tryconstruct_big --data-folder data --data-file tryconstruct/union_str_20_x6',
    #               'sub-exe -S -t test -y Test::union_tryconstruct_small --data-folder data --data-file tryconstruct/union_str_10_x6'],
    #     'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
    #     'check_function' : tsf.data_is_correct,
    #     'title' : '',
    #     'description' : ''
    # },
    # 'tryc_union_6' : {
    #     'common_args' : ['--type-folder types --type-file try_construct'],
    #     'apps' : ['pub-exe -P -t test -y Test::union_tryconstruct_big --data-folder data --data-file tryconstruct/union_str_20_x7',
    #               'sub-exe -S -t test -y Test::union_tryconstruct_small --data-folder data --data-file tryconstruct/union_str_default'],
    #     'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
    #     'check_function' : tsf.data_is_correct,
    #     'title' : '',
    #     'description' : ''
    # },
}
