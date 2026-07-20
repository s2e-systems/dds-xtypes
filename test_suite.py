#################################################################
# Use and redistribution is source and binary forms is permitted
# subject to the OMG-DDS INTEROPERABILITY TESTING LICENSE found
# at the following URL:
#
# https://github.com/omg-dds/dds-rtps/blob/master/LICENSE.md
#
#################################################################
from interoperability_test_utilities import ReturnCode
import test_suite_functions as tsf

xtypes_v2_extensibility_test_suite = {
    'ext_final_struct_1' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_f1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_f1 --data-folder data --data-file struct_num_x1 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between identical struct_f1 (subscriber with ignore_member_names false)',
        'description' : 'Verifies identical final structs can communicate:\n\n'
                        ' * Publisher and Subscriber use `struct_f1` (final) from `extensibility`.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'ext_final_struct_2' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_f1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_f2 --data-folder data --data-file struct_num_x1 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between struct_f1 and struct_f2 (subscriber with ignore_member_names false)',
        'description' : 'Verifies final structs with different member counts are not assignable:\n\n'
                        ' * Publisher uses `struct_f1` (final) from `extensibility`.\n'
                        ' * Subscriber uses `struct_f2` (final) from `extensibility`.\n'
                        ' * `struct_f2` has an extra member `x2` (`int32`) at the end.\n'
                        ' * Final extensibility forbids appending members.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'ext_appendable_struct_1' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_a1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_a1 --data-folder data --data-file struct_num_x1 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between identical struct_a1 (subscriber with ignore_member_names false)',
        'description' : 'Verifies identical appendable structs can communicate:\n\n'
                        ' * Publisher and Subscriber use `struct_a1` (appendable) from `extensibility`.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'ext_appendable_struct_2' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_a1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_a2 --data-folder data --data-file struct_num_x1 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between struct_a1 and struct_a2 (subscriber with ignore_member_names false)',
        'description' : 'Verifies appendable structs allow an appended trailing member:\n\n'
                        ' * Publisher uses `struct_a1` (appendable) from `extensibility`.\n'
                        ' * Subscriber uses `struct_a2` (appendable) from `extensibility`.\n'
                        ' * `struct_a2` has an extra member `x2` (`int32`) appended at the end.\n'
                        ' * Appendable extensibility permits this.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'ext_appendable_struct_3' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_a2 --data-folder data --data-file struct_num_x1_x2',
                  'sub-exe -S -t test -y Test::struct_a1 --data-folder data --data-file struct_num_x1 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between struct_a2 and struct_a1 (subscriber with ignore_member_names false)',
        'description' : 'Verifies appendable structs allow the publisher to have additional trailing members:\n\n'
                        ' * Publisher uses `struct_a2` (appendable) from `extensibility`.\n'
                        ' * Subscriber uses `struct_a1` (appendable) from `extensibility`.\n'
                        ' * Publisher\'s `struct_a2` has an extra trailing member `x2` (`int32`) that the subscriber\'s `struct_a1` ignores.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'ext_appendable_struct_4' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_a2 --data-folder data --data-file struct_num_x1_x2',
                  'sub-exe -S -t test -y Test::struct_a3 --data-folder data --data-file struct_num_x1_x2 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between struct_a2 and struct_a3 (subscriber with ignore_member_names false)',
        'description' : 'Verifies appendable structs with a member inserted in the middle are not assignable:\n\n'
                        ' * Publisher uses `struct_a2` (appendable) from `extensibility`.\n'
                        ' * Subscriber uses `struct_a3` (appendable) from `extensibility`.\n'
                        ' * `struct_a3` inserts member `x3` between `x1` and `x2`, changing the serialization order.\n'
                        ' * Appendable types require positional matching.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'ext_appendable_struct_5' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_a3 --data-folder data --data-file struct_num_x1_x3_x2',
                  'sub-exe -S -t test -y Test::struct_a2 --data-folder data --data-file struct_num_x1_x2 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between struct_a3 and struct_a2 (subscriber with ignore_member_names false)',
        'description' : 'Verifies appendable structs with a member inserted in the middle are not assignable:\n\n'
                        ' * Publisher uses `struct_a3` (appendable) from `extensibility`.\n'
                        ' * Subscriber uses `struct_a2` (appendable) from `extensibility`.\n'
                        ' * `struct_a3` has member `x3` inserted between `x1` and `x2`.\n'
                        ' * Since position matters for appendable types, this breaks assignability.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },

    'ext_mutable_struct_1' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_m1 --data-folder data --data-file struct_num_x1 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between identical struct_m1 (subscriber with ignore_member_names false)',
        'description' : 'Verifies identical mutable structs can communicate:\n\n'
                        ' * Publisher and Subscriber use `struct_m1` (mutable) from `extensibility`.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'ext_mutable_struct_2' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_m2 --data-folder data --data-file struct_num_x1 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between struct_m1 and struct_m2 (subscriber with ignore_member_names false)',
        'description' : 'Verifies mutable structs allow an extra member with explicit ID:\n\n'
                        ' * Publisher uses `struct_m1` (mutable) from `extensibility`.\n'
                        ' * Subscriber uses `struct_m2` (mutable) from `extensibility`.\n'
                        ' * `struct_m2` has an extra member `x2` with explicit `id=2`.\n'
                        ' * Mutable types match by member ID, so extra members are allowed.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'ext_mutable_struct_3' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m2 --data-folder data --data-file struct_num_x1_x2',
                  'sub-exe -S -t test -y Test::struct_m1 --data-folder data --data-file struct_num_x1 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between struct_m2 and struct_m1 (subscriber with ignore_member_names false)',
        'description' : 'Verifies mutable structs allow the publisher to have additional members:\n\n'
                        ' * Publisher uses `struct_m2` (mutable) from `extensibility`.\n'
                        ' * Subscriber uses `struct_m1` (mutable) from `extensibility`.\n'
                        ' * Publisher\'s `struct_m2` has member `x2` (`id=2`) that the subscriber\'s `struct_m1` does not.\n'
                        ' * Mutable types allow this.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'ext_mutable_struct_4' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m2 --data-folder data --data-file struct_num_x1_x2',
                  'sub-exe -S -t test -y Test::struct_m3 --data-folder data --data-file struct_num_x1_x2 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between struct_m2 and struct_m3 (subscriber with ignore_member_names false)',
        'description' : 'Verifies mutable structs remain assignable when a member is inserted in the middle with an explicit ID:\n\n'
                        ' * Publisher uses `struct_m2` (mutable) from `extensibility`.\n'
                        ' * Subscriber uses `struct_m3` (mutable) from `extensibility`.\n'
                        ' * `struct_m3` inserts member `x3` (`id=3`) between `x1` and `x2`.\n'
                        ' * Since mutable types match by ID (not position), this is valid.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'ext_mutable_struct_5' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m3 --data-folder data --data-file struct_num_x1_x3_x2',
                  'sub-exe -S -t test -y Test::struct_m2 --data-folder data --data-file struct_num_x1_x2 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between struct_m3 and struct_m2 (subscriber with ignore_member_names false)',
        'description' : 'Verifies mutable structs remain assignable when the publisher has an extra member identified by ID:\n\n'
                        ' * Publisher uses `struct_m3` (mutable) from `extensibility`.\n'
                        ' * Subscriber uses `struct_m2` (mutable) from `extensibility`.\n'
                        ' * Publisher\'s `struct_m3` has member `x3` (`id=3`) between `x1` and `x2` that the subscriber does not.\n'
                        ' * Mutable ID-based matching allows this.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'ext_mutable_struct_6' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m2 --data-folder data --data-file struct_num_x1_x2',
                  'sub-exe -S -t test -y Test::struct_m4 --data-folder data --data-file struct_num_x1_x2 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between struct_m2 and struct_m4 (subscriber with ignore_member_names false)',
        'description' : 'Verifies mutable structs without explicit IDs are not assignable to those with explicit IDs:\n\n'
                        ' * Publisher uses `struct_m2` (mutable) from `extensibility`.\n'
                        ' * Subscriber uses `struct_m4` (mutable) from `extensibility`.\n'
                        ' * `struct_m2` uses explicit member IDs (`x1` id=1, `x2` id=2).\n'
                        ' * `struct_m4` has no explicit IDs, so auto-assigned IDs differ, causing mismatch.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'ext_autoid_1' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_hashid_1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_hashid_2 --data-folder data --data-file struct_num_x2'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between struct_hashid_1 and struct_hashid_2',
        'description' : 'Verifies structs using `hashid` can communicate when hash IDs match:\n\n'
                        ' * Publisher uses `struct_hashid_1` (final) from `extensibility`.\n'
                        ' * Subscriber uses `struct_hashid_2` (final) from `extensibility`.\n'
                        ' * Publisher\'s `struct_hashid_1` has member `x1` with `autoid=hash`.\n'
                        ' * Subscriber\'s `struct_hashid_2` has member `x2` with `hashid="x1"`, resolving to the same hash ID.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
}


xtypes_v2_type_consistency_test_suite = {
    'tc_force_type_validation_1' : {
        'apps' : ['pub-exe -P -t test --type-folder types --type-file type_consistency                -y Test::struct_x1 --data-folder data --data-file struct_num_x1 --disable-type-info',
                  'sub-exe -S -t test --type-folder types --type-file type_consistency_force_type_val -y Test::struct_x1 --data-folder data --data-file struct_num_x1 --force-type-validation t --disable-type-info'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between identical struct_x1 (subscriber with force_type_validation true)',
        'description' : 'Verifies identical `struct_x1` types:\n\n'
                        ' * Publisher and Subscriber use `struct_x1` from `type_consistency`.\n'
                        ' * Subscriber sets `--force-type-validation` to `true`.\n'
                        ' * Both endpoints set `--disable-type-info`.\n'
                        'With `force_type_validation` enabled and type information disabled, the subscriber cannot confirm type compatibility.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'tc_force_type_validation_2' : {
        'apps' : ['pub-exe -P -t test --type-folder types --type-file type_consistency                -y Test::struct_x1 --data-folder data --data-file struct_num_x1 --disable-type-info',
                  'sub-exe -S -t test --type-folder types --type-file type_consistency_force_type_val -y Test::struct_x1 --data-folder data --data-file struct_num_x1 --force-type-validation f --disable-type-info'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between identical struct_x1 (subscriber with force_type_validation false)',
        'description' : 'Verifies identical `struct_x1` types:\n\n'
                        ' * Publisher and Subscriber use `struct_x1` from `type_consistency`.\n'
                        ' * Subscriber sets `--force-type-validation` to `false`.\n'
                        ' * Both endpoints set `--disable-type-info`.\n'
                        'With `force_type_validation` disabled, the subscriber does not require type information for discovery.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tc_force_type_validation_3' : {
        'apps' : ['pub-exe -P -t test --type-folder types --type-file type_consistency -y Test::struct_x1 --data-folder data --data-file struct_num_x1 --disable-type-info',
                  'sub-exe -S -t test --type-folder types --type-file type_consistency_force_type_val -y Test::struct_x1 --data-folder data --data-file struct_num_x1 --force-type-validation d --disable-type-info'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between identical struct_x1 (subscriber with force_type_validation default)',
        'description' : 'Verifies identical `struct_x1` types:\n\n'
                        ' * Publisher and Subscriber use `struct_x1` from `type_consistency`.\n'
                        ' * Subscriber sets `--force-type-validation` to `default`.\n'
                        ' * Both endpoints set `--disable-type-info`.\n'
                        'With `force_type_validation` disabled, the subscriber does not require type information for discovery.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tc_ignore_member_names_1' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::struct_x1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_x2 --data-folder data --data-file struct_num_x2 --ignore-member-names t'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between struct_x1 and struct_x2 (subscriber with ignore_member_names true)',
        'description' : 'Verifies structs with same-type members but different member names:\n\n'
                        ' * Publisher uses `struct_x1` from `type_consistency`.\n'
                        ' * Subscriber uses `struct_x2` from `type_consistency`.\n'
                        ' * Both have one `int32` member, but named `x1` in publisher and `x2` in subscriber.\n'
                        ' * Subscriber sets `--ignore-member-names` to `true`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tc_ignore_member_names_2' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::struct_x1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_x2 --data-folder data --data-file struct_num_x2 --ignore-member-names f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between struct_x1 and struct_x2 (subscriber with ignore_member_names false)',
        'description' : 'Verifies structs with same-type members but different member names:\n\n'
                        ' * Publisher uses `struct_x1` from `type_consistency`.\n'
                        ' * Subscriber uses `struct_x2` from `type_consistency`.\n'
                        ' * Both have one `int32` member, but named `x1` in publisher and `x2` in subscriber.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'tc_ignore_member_names_3' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::struct_x1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_x2 --data-folder data --data-file struct_num_x2 --ignore-member-names d'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between struct_x1 and struct_x2 (subscriber with ignore_member_names default)',
        'description' : 'Verifies structs with same-type members but different member names:\n\n'
                        ' * Publisher uses `struct_x1` from `type_consistency`.\n'
                        ' * Subscriber uses `struct_x2` from `type_consistency`.\n'
                        ' * Both have one `int32` member, but named `x1` in publisher and `x2` in subscriber.\n'
                        ' * Subscriber sets `--ignore-member-names` to `default`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'tc_ignore_seq_bounds_1' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_10 --ignore-seq-bounds t'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between seq_int32x10 and seq_int32x20 (subscriber with ignore_seq_bounds true)',
        'description' : 'Verifies sequences with different bounds (smaller publisher bound):\n\n'
                        ' * Publisher uses `seq_int32x10` from `type_consistency`.\n'
                        ' * Subscriber uses `seq_int32x20` from `type_consistency`.\n'
                        ' * Publisher sequence bound is 10.\n'
                        ' * Subscriber sequence bound is 20.\n'
                        ' * Subscriber bound >= publisher bound.\n'
                        ' * Subscriber sets `--ignore-seq-bounds` to `true`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tc_ignore_seq_bounds_2' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_10 --ignore-seq-bounds f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between seq_int32x10 and seq_int32x20 (subscriber with ignore_seq_bounds false)',
        'description' : 'Verifies sequences with different bounds (smaller publisher bound):\n\n'
                        ' * Publisher uses `seq_int32x10` from `type_consistency`.\n'
                        ' * Subscriber uses `seq_int32x20` from `type_consistency`.\n'
                        ' * Publisher sequence bound is 10.\n'
                        ' * Subscriber sequence bound is 20.\n'
                        ' * Subscriber bound >= publisher bound.\n'
                        ' * Subscriber sets `--ignore-seq-bounds` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tc_ignore_seq_bounds_3' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_10 --ignore-seq-bounds d'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between seq_int32x10 and seq_int32x20 (subscriber with ignore_seq_bounds default)',
        'description' : 'Verifies sequences with different bounds (smaller publisher bound):\n\n'
                        ' * Publisher uses `seq_int32x10` from `type_consistency`.\n'
                        ' * Subscriber uses `seq_int32x20` from `type_consistency`.\n'
                        ' * Publisher sequence bound is 10.\n'
                        ' * Subscriber sequence bound is 20.\n'
                        ' * Subscriber bound >= publisher bound.\n'
                        ' * Subscriber sets `--ignore-seq-bounds` to `default`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tc_ignore_seq_bounds_4' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::seq_int32x10 --data-folder data --data-file array_num_10 --ignore-seq-bounds t'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between seq_int32x20 and seq_int32x10 but sample rejected (subscriber with ignore_seq_bounds true)',
        'description' : 'Verifies sequence without explicit `@try_construct` and oversized data:\n\n'
                        ' * Publisher uses `seq_int32x20` from `type_consistency`.\n'
                        ' * Subscriber uses `seq_int32x10` from `type_consistency`.\n'
                        ' * Publisher sequence bound is 20.\n'
                        ' * Subscriber bound is 10 with no `@try_construct` annotation.\n'
                        ' * Default behavior (discard) applies to oversized data.\n'
                        ' * Subscriber sets `--ignore-seq-bounds` to `true`.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },
    'tc_ignore_seq_bounds_5' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::seq_int32x10 --data-folder data --data-file array_num_10 --ignore-seq-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between seq_int32x20 and seq_int32x10 (subscriber with ignore_seq_bounds false)',
        'description' : 'Verifies sequence without explicit `@try_construct` and oversized data:\n\n'
                        ' * Publisher uses `seq_int32x20` from `type_consistency`.\n'
                        ' * Subscriber uses `seq_int32x10` from `type_consistency`.\n'
                        ' * Publisher sequence bound is 20.\n'
                        ' * Subscriber bound is 10 with no `@try_construct` annotation.\n'
                        ' * Default behavior (discard) applies to oversized data.\n'
                        ' * Subscriber sets `--ignore-seq-bounds` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'tc_ignore_seq_bounds_6' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::seq_int32x10 --data-folder data --data-file array_num_10 --ignore-seq-bounds d'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between seq_int32x20 and seq_int32x10 but sample rejected (subscriber with ignore_seq_bounds default)',
        'description' : 'Verifies sequence without explicit `@try_construct` and oversized data:\n\n'
                        ' * Publisher uses `seq_int32x20` from `type_consistency`.\n'
                        ' * Subscriber uses `seq_int32x10` from `type_consistency`.\n'
                        ' * Publisher sequence bound is 20.\n'
                        ' * Subscriber bound is 10 with no `@try_construct` annotation.\n'
                        ' * Default behavior (discard) applies to oversized data.\n'
                        ' * Subscriber sets `--ignore-seq-bounds` to `default`.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },
    'tc_ignore_seq_bounds_7' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::seq_int32x10 --data-folder data --data-file array_num_10 --ignore-seq-bounds t'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between seq_int32x20 and seq_int32x10 (subscriber with ignore_seq_bounds true)',
        'description' : 'Verifies sequence without explicit `@try_construct` and oversized data:\n\n'
                        ' * Publisher uses `seq_int32x20` from `type_consistency`.\n'
                        ' * Subscriber uses `seq_int32x10` from `type_consistency`.\n'
                        ' * Publisher sequence bound is 20.\n'
                        ' * Subscriber bound is 10 with no `@try_construct` annotation.\n'
                        ' * Default behavior (discard) applies to oversized data.\n'
                        ' * Subscriber sets `--ignore-seq-bounds` to `true`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tc_ignore_str_bounds_1' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::string10 --data-folder data --data-file strings_hello',
                  'sub-exe -S -t test -y Test::string20 --data-folder data --data-file strings_hello --ignore-str-bounds t'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between string10 and string20 (subscriber with ignore_str_bounds true)',
        'description' : 'Verifies string with smaller bound is assignable to string with larger bound:\n\n'
                        ' * Publisher uses `string10` from `type_consistency`.\n'
                        ' * Subscriber uses `string20` from `type_consistency`.\n'
                        ' * Publisher uses `string<10>`.\n'
                        ' * Subscriber uses `string<20>`.\n'
                        ' * Subscriber bound >= publisher bound.\n'
                        ' * Subscriber sets `--ignore-str-bounds` to `true`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tc_ignore_str_bounds_2' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::string10 --data-folder data --data-file strings_hello',
                  'sub-exe -S -t test -y Test::string20 --data-folder data --data-file strings_hello --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between string10 and string20 (subscriber with ignore_str_bounds false)',
        'description' : 'Verifies string with smaller bound is assignable to string with larger bound:\n\n'
                        ' * Publisher uses `string10` from `type_consistency`.\n'
                        ' * Subscriber uses `string20` from `type_consistency`.\n'
                        ' * Publisher uses `string<10>`.\n'
                        ' * Subscriber uses `string<20>`.\n'
                        ' * Subscriber bound >= publisher bound.\n'
                        ' * Subscriber sets `--ignore-str-bounds` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tc_ignore_str_bounds_3' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::string10 --data-folder data --data-file strings_hello',
                  'sub-exe -S -t test -y Test::string20 --data-folder data --data-file strings_hello --ignore-str-bounds d'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between string10 and string20 (subscriber with ignore_str_bounds default)',
        'description' : 'Verifies string with smaller bound is assignable to string with larger bound:\n\n'
                        ' * Publisher uses `string10` from `type_consistency`.\n'
                        ' * Subscriber uses `string20` from `type_consistency`.\n'
                        ' * Publisher uses `string<10>`.\n'
                        ' * Subscriber uses `string<20>`.\n'
                        ' * Subscriber bound >= publisher bound.\n'
                        ' * Subscriber sets `--ignore-str-bounds` to `default`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tc_ignore_str_bounds_4' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10 --data-folder data --data-file strings --ignore-str-bounds t'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between string20 and string10 but sample rejected (subscriber with ignore_str_bounds true)',
        'description' : 'Verifies string without explicit `@try_construct` and oversized data:\n\n'
                        ' * Publisher uses `string20` from `type_consistency`.\n'
                        ' * Subscriber uses `string10` from `type_consistency`.\n'
                        ' * Publisher string bound is 20.\n'
                        ' * Subscriber bound is 10 with no `@try_construct` annotation.\n'
                        ' * Default behavior (discard) applies to oversized strings.\n'
                        ' * Subscriber sets `--ignore-str-bounds` to `true`.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },
    'tc_ignore_str_bounds_5' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10 --data-folder data --data-file strings --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between string20 and string10 (subscriber with ignore_str_bounds false)',
        'description' : 'Verifies string without explicit `@try_construct` and oversized data:\n\n'
                        ' * Publisher uses `string20` from `type_consistency`.\n'
                        ' * Subscriber uses `string10` from `type_consistency`.\n'
                        ' * Publisher string bound is 20.\n'
                        ' * Subscriber bound is 10 with no `@try_construct` annotation.\n'
                        ' * Default behavior (discard) applies to oversized strings.\n'
                        ' * Subscriber sets `--ignore-str-bounds` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'tc_ignore_str_bounds_6' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10 --data-folder data --data-file strings --ignore-str-bounds d'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between string20 and string10 but sample rejected (subscriber with ignore_str_bounds default)',
        'description' : 'Verifies string without explicit `@try_construct` and oversized data:\n\n'
                        ' * Publisher uses `string20` from `type_consistency`.\n'
                        ' * Subscriber uses `string10` from `type_consistency`.\n'
                        ' * Publisher string bound is 20.\n'
                        ' * Subscriber bound is 10 with no `@try_construct` annotation.\n'
                        ' * Default behavior (discard) applies to oversized strings.\n'
                        ' * Subscriber sets `--ignore-str-bounds` to `default`.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },
    'tc_ignore_str_bounds_7' : {
        'common_args' : ['--type-folder types --type-file type_consistency'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings_hello',
                  'sub-exe -S -t test -y Test::string10 --data-folder data --data-file strings_hello --ignore-str-bounds t'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between string20 and string10 (subscriber with ignore_str_bounds true)',
        'description' : 'Verifies string without explicit `@try_construct` and oversized data:\n\n'
                        ' * Publisher uses `string20` from `type_consistency`.\n'
                        ' * Subscriber uses `string10` from `type_consistency`.\n'
                        ' * Publisher string bound is 20.\n'
                        ' * Subscriber bound is 10 with no `@try_construct` annotation.\n'
                        ' * Default behavior (discard) applies to oversized strings.\n'
                        ' * Subscriber sets `--ignore-str-bounds` to `true`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tc_prevent_type_widening_1' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_f1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_f2 --data-folder data --data-file struct_num_x1 --prevent-type-widening t'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between struct_f1 and struct_f2 (subscriber with prevent_type_widening true)',
        'description' : 'Verifies final structs with different member counts are not assignable:\n\n'
                        ' * Publisher uses `struct_f1` (final) from `extensibility`.\n'
                        ' * Subscriber uses `struct_f2` (final) from `extensibility`.\n'
                        ' * `struct_f2` has an extra member `x2` (`int32`) at the end.\n'
                        ' * Final extensibility forbids appending members.\n'
                        ' * Subscriber sets `--prevent-type-widening` to `true`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'tc_prevent_type_widening_2' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_f1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_f2 --data-folder data --data-file struct_num_x1 --prevent-type-widening f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between struct_f1 and struct_f2 (subscriber with prevent_type_widening false)',
        'description' : 'Verifies final structs with different member counts are not assignable:\n\n'
                        ' * Publisher uses `struct_f1` (final) from `extensibility`.\n'
                        ' * Subscriber uses `struct_f2` (final) from `extensibility`.\n'
                        ' * `struct_f2` has an extra member `x2` (`int32`) at the end.\n'
                        ' * Final extensibility forbids appending members.\n'
                        ' * Subscriber sets `--prevent-type-widening` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'tc_prevent_type_widening_3' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_f1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_f2 --data-folder data --data-file struct_num_x1 --prevent-type-widening d'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between struct_f1 and struct_f2 (subscriber with prevent_type_widening default)',
        'description' : 'Verifies final structs with different member counts are not assignable:\n\n'
                        ' * Publisher uses `struct_f1` (final) from `extensibility`.\n'
                        ' * Subscriber uses `struct_f2` (final) from `extensibility`.\n'
                        ' * `struct_f2` has an extra member `x2` (`int32`) at the end.\n'
                        ' * Final extensibility forbids appending members.\n'
                        ' * Subscriber sets `--prevent-type-widening` to `default`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'tc_prevent_type_widening_4' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_a1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_a2 --data-folder data --data-file struct_num_x1 --prevent-type-widening t'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between struct_a1 and struct_a2 (subscriber with prevent_type_widening true)',
        'description' : 'Verifies appendable structs allow an appended trailing member:\n\n'
                        ' * Publisher uses `struct_a1` (appendable) from `extensibility`.\n'
                        ' * Subscriber uses `struct_a2` (appendable) from `extensibility`.\n'
                        ' * `struct_a2` has an extra member `x2` (`int32`) appended at the end.\n'
                        ' * Appendable extensibility permits this.\n'
                        ' * Subscriber sets `--prevent-type-widening` to `true`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'tc_prevent_type_widening_5' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_a1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_a2 --data-folder data --data-file struct_num_x1 --prevent-type-widening f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between struct_a1 and struct_a2 (subscriber with prevent_type_widening false)',
        'description' : 'Verifies appendable structs allow an appended trailing member:\n\n'
                        ' * Publisher uses `struct_a1` (appendable) from `extensibility`.\n'
                        ' * Subscriber uses `struct_a2` (appendable) from `extensibility`.\n'
                        ' * `struct_a2` has an extra member `x2` (`int32`) appended at the end.\n'
                        ' * Appendable extensibility permits this.\n'
                        ' * Subscriber sets `--prevent-type-widening` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tc_prevent_type_widening_6' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_a1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_a2 --data-folder data --data-file struct_num_x1 --prevent-type-widening d'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between struct_a1 and struct_a2 (subscriber with prevent_type_widening default)',
        'description' : 'Verifies appendable structs allow an appended trailing member:\n\n'
                        ' * Publisher uses `struct_a1` (appendable) from `extensibility`.\n'
                        ' * Subscriber uses `struct_a2` (appendable) from `extensibility`.\n'
                        ' * `struct_a2` has an extra member `x2` (`int32`) appended at the end.\n'
                        ' * Appendable extensibility permits this.\n'
                        ' * Subscriber sets `--prevent-type-widening` to `default`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tc_prevent_type_widening_7' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_m2 --data-folder data --data-file struct_num_x1 --prevent-type-widening t'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between struct_m1 and struct_m2 (subscriber with prevent_type_widening true)',
        'description' : 'Verifies mutable structs allow an extra member with explicit ID:\n\n'
                        ' * Publisher uses `struct_m1` (mutable) from `extensibility`.\n'
                        ' * Subscriber uses `struct_m2` (mutable) from `extensibility`.\n'
                        ' * `struct_m2` has an extra member `x2` with explicit `id=2`.\n'
                        ' * Mutable types match by member ID, so extra members are allowed.\n'
                        ' * Subscriber sets `--prevent-type-widening` to `true`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'tc_prevent_type_widening_8' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_m2 --data-folder data --data-file struct_num_x1 --prevent-type-widening f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between struct_m1 and struct_m2 (subscriber with prevent_type_widening false)',
        'description' : 'Verifies mutable structs allow an extra member with explicit ID:\n\n'
                        ' * Publisher uses `struct_m1` (mutable) from `extensibility`.\n'
                        ' * Subscriber uses `struct_m2` (mutable) from `extensibility`.\n'
                        ' * `struct_m2` has an extra member `x2` with explicit `id=2`.\n'
                        ' * Mutable types match by member ID, so extra members are allowed.\n'
                        ' * Subscriber sets `--prevent-type-widening` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tc_prevent_type_widening_9' : {
        'common_args' : ['--type-folder types --type-file extensibility'],
        'apps' : ['pub-exe -P -t test -y Test::struct_m1 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_m2 --data-folder data --data-file struct_num_x1 --prevent-type-widening d'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between struct_m1 and struct_m2 (subscriber with prevent_type_widening default)',
        'description' : 'Verifies mutable structs allow an extra member with explicit ID:\n\n'
                        ' * Publisher uses `struct_m1` (mutable) from `extensibility`.\n'
                        ' * Subscriber uses `struct_m2` (mutable) from `extensibility`.\n'
                        ' * `struct_m2` has an extra member `x2` with explicit `id=2`.\n'
                        ' * Mutable types match by member ID, so extra members are allowed.\n'
                        ' * Subscriber sets `--prevent-type-widening` to `default`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
}


xtypes_v2_array_test_suite = {
    'int32[10]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::int32x10 --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between identical int32x10',
        'description' : 'Verifies identical `int32` arrays communicate:\n\n'
                        ' * Publisher and Subscriber use `int32x10` from `arrays`.\n'
                        ' * Both use `int32[10]` arrays with the same element type and dimension.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'int32[10]_int32[20]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::int32x20 --data-folder data --data-file array_num_20'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between int32x10 and int32x20',
        'description' : 'Verifies sequence with smaller bound is assignable to sequence with larger bound:\n\n'
                        ' * Publisher uses `int32x10` from `arrays`.\n'
                        ' * Subscriber uses `int32x20` from `arrays`.\n'
                        ' * Publisher uses `sequence<int32, 10>`.\n'
                        ' * Subscriber uses `sequence<int32, 20>`.\n'
                        ' * Subscriber bound >= publisher bound, and data fits.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'int32[20]_int32[10]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::int32x20 --data-folder data --data-file array_num_20'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between int32x10 and int32x20',
        'description' : 'Verifies sequence with smaller bound is assignable to sequence with larger bound:\n\n'
                        ' * Publisher uses `int32x10` from `arrays`.\n'
                        ' * Subscriber uses `int32x20` from `arrays`.\n'
                        ' * Publisher uses `sequence<int32, 10>`.\n'
                        ' * Subscriber uses `sequence<int32, 20>`.\n'
                        ' * Subscriber bound >= publisher bound, and data fits.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'int32[10]_uint32[10]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::uint32x10 --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between int32x10 and uint32x10',
        'description' : 'Verifies arrays with different element types are not assignable:\n\n'
                        ' * Publisher uses `int32x10` from `arrays`.\n'
                        ' * Subscriber uses `uint32x10` from `arrays`.\n'
                        ' * Publisher element type is `int32`.\n'
                        ' * Subscriber element type is `uint32`.\n'
                        ' * Array elements must be strongly assignable.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'int32[10][2]_int32[20]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::int32x10x2 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::int32x20 --data-folder data --data-file array_num_20'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between int32x10x2 and int32x20',
        'description' : 'Verifies multi-dimensional and single-dimensional arrays of same total size are not assignable:\n\n'
                        ' * Publisher uses `int32x10x2` from `arrays`.\n'
                        ' * Subscriber uses `int32x20` from `arrays`.\n'
                        ' * Publisher is `int32[10][2]` (2D, 20 elements total).\n'
                        ' * Subscriber is `int32[20]` (1D).\n'
                        ' * Dimensions must match structurally, not just in total count.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'string10[10]_string20[10]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::string10x10 --data-folder data --data-file array_string_10',
                  'sub-exe -S -t test -y Test::string20x10 --data-folder data --data-file array_string_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between string10x10 and string20x10',
        'description' : 'Verifies sequences of strings with different string bounds are assignable:\n\n'
                        ' * Publisher uses `string10x10` from `arrays`.\n'
                        ' * Subscriber uses `string20x10` from `arrays`.\n'
                        ' * Both are `sequence<string, 10>`.\n'
                        ' * Publisher string bound is 10, subscriber is 20.\n'
                        ' * String elements are strongly assignable since subscriber bound >= publisher bound.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'enum1[10]_enum2[10]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::enum1x10 --data-folder data --data-file array_enum_10',
                  'sub-exe -S -t test -y Test::enum2x10 --data-folder data --data-file array_enum_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between enum1x10 and enum2x10',
        'description' : 'Verifies arrays of appendable enums with subset literals are assignable:\n\n'
                        ' * Publisher uses `enum1x10` from `arrays`.\n'
                        ' * Subscriber uses `enum2x10` from `arrays`.\n'
                        ' * Both are enum arrays of size 10.\n'
                        ' * Publisher uses `E1` (3 literals: VAL0-VAL2), subscriber uses `E2` (4 literals: VAL0-VAL3).\n'
                        ' * `E2` is a superset of `E1`, so elements are strongly assignable.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'appendable_enum' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::enum1 --data-folder data --data-file enum',
                  'sub-exe -S -t test -y Test::enum2 --data-folder data --data-file enum'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between enum1 and enum2',
        'description' : 'Verifies appendable enums where subscriber is a superset are assignable:\n\n'
                        ' * Publisher uses `enum1` from `arrays`.\n'
                        ' * Subscriber uses `enum2` from `arrays`.\n'
                        ' * Publisher uses `E1` (3 literals: VAL0-VAL2).\n'
                        ' * Subscriber uses `E2` (4 literals: VAL0-VAL3).\n'
                        ' * `E2` is a superset of `E1`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'SFinal[10]_S[20]_SFinalAlt[10]_S[20]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::F_S__array10_F_S__array20_uint32 --data-folder data --data-file array_array_num_10_20',
                  'sub-exe -S -t test -y Test::F_S__array10_F_S__array20_uint32_alt --data-folder data --data-file array_array_num_10_20_alt'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between F_S__array10_F_S__array20_uint32 and F_S__array10_F_S__array20_uint32_alt',
        'description' : 'Verifies arrays of final structs are assignable when inner struct elements are strongly assignable:\n\n'
                        ' * Publisher uses `F_S__array10_F_S__array20_uint32` from `arrays`.\n'
                        ' * Subscriber uses `F_S__array10_F_S__array20_uint32_alt` from `arrays`.\n'
                        ' * Both are arrays of 10 final structs containing `uint32[20]`.\n'
                        ' * Member names differ (`x1` vs `altx1`) but the types are structurally equivalent.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'SAppendable[10]_S[20]_SAppendableAlt[10]_S[20]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::F_S__array10_A_S__array20_uint32 --data-folder data --data-file array_array_num_10_20',
                  'sub-exe -S -t test -y Test::F_S__array10_A_S__array20_uint32_alt --data-folder data --data-file array_array_num_10_20_alt'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between F_S__array10_A_S__array20_uint32 and F_S__array10_A_S__array20_uint32_alt',
        'description' : 'Verifies arrays of appendable structs are assignable when inner struct elements are strongly assignable:\n\n'
                        ' * Publisher uses `F_S__array10_A_S__array20_uint32` from `arrays`.\n'
                        ' * Subscriber uses `F_S__array10_A_S__array20_uint32_alt` from `arrays`.\n'
                        ' * Both are arrays of 10 structs containing appendable inner structs with `uint32[20]`.\n'
                        ' * Member names differ (`x1` vs `altx1`).\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'SMutable[10]_S[20]_SMutableAlt[10]_S[20]' : {
        'common_args' : ['--type-folder types --type-file arrays'],
        'apps' : ['pub-exe -P -t test -y Test::F_S__array10_M_S__array20_uint32 --data-folder data --data-file array_array_num_10_20',
                  'sub-exe -S -t test -y Test::F_S__array10_M_S__array20_uint32_alt --data-folder data --data-file array_array_num_10_20_alt'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between F_S__array10_M_S__array20_uint32 and F_S__array10_M_S__array20_uint32_alt',
        'description' : 'Verifies arrays of mutable structs are assignable when inner struct elements are strongly assignable:\n\n'
                        ' * Publisher uses `F_S__array10_M_S__array20_uint32` from `arrays`.\n'
                        ' * Subscriber uses `F_S__array10_M_S__array20_uint32_alt` from `arrays`.\n'
                        ' * Both are arrays of 10 mutable structs containing `uint32[20]`.\n'
                        ' * Member names differ (`x1` vs `altx1`).\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
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
        'title' : 'Communication between int32_unbounded and int32x10',
        'description' : 'Verifies unbounded sequence is assignable to bounded sequence (default ignore_seq_bounds):\n\n'
                        ' * Publisher uses `int32_unbounded` from `sequences`.\n'
                        ' * Subscriber uses `int32x10` from `sequences`.\n'
                        ' * Publisher uses unbounded `sequence<int32>`.\n'
                        ' * Subscriber uses `sequence<int32, 10>`.\n'
                        ' * By default, sequence bounds are ignored for assignability.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'seq(int32)_seq(int32,10)_check_bounds' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::int32_unbounded --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::int32x10 --data-folder data --data-file array_num_10 --ignore-seq-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between int32_unbounded and int32x10 (subscriber with ignore_seq_bounds false)',
        'description' : 'Verifies unbounded sequence is assignable to bounded sequence (default ignore_seq_bounds):\n\n'
                        ' * Publisher uses `int32_unbounded` from `sequences`.\n'
                        ' * Subscriber uses `int32x10` from `sequences`.\n'
                        ' * Publisher uses unbounded `sequence<int32>`.\n'
                        ' * Subscriber uses `sequence<int32, 10>`.\n'
                        ' * By default, sequence bounds are ignored for assignability.\n'
                        ' * Subscriber sets `--ignore-seq-bounds` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'seq(int32,20)_seq(int32,10)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::int32x10 --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between int32x20 and int32x10 but sample rejected',
        'description' : 'Verifies sequence with larger bound sending data exceeding subscriber bound:\n\n'
                        ' * Publisher uses `int32x20` from `sequences`.\n'
                        ' * Subscriber uses `int32x10` from `sequences`.\n'
                        ' * Publisher uses `sequence<int32, 20>` with 20 elements.\n'
                        ' * Subscriber uses `sequence<int32, 10>`.\n'
                        ' * The actual data size (20) exceeds subscriber bound (10).\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },
    'seq(int32,20)_seq(int32,10)_check_bounds' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::int32x10 --data-folder data --data-file array_num_10 --ignore-seq-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between int32x20 and int32x10 (subscriber with ignore_seq_bounds false)',
        'description' : 'Verifies sequence with larger bound sending data exceeding subscriber bound:\n\n'
                        ' * Publisher uses `int32x20` from `sequences`.\n'
                        ' * Subscriber uses `int32x10` from `sequences`.\n'
                        ' * Publisher uses `sequence<int32, 20>` with 20 elements.\n'
                        ' * Subscriber uses `sequence<int32, 10>`.\n'
                        ' * The actual data size (20) exceeds subscriber bound (10).\n'
                        ' * Subscriber sets `--ignore-seq-bounds` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'seq(int32,10)_seq(int32,20)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::int32x20 --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between int32x10 and int32x20',
        'description' : 'Verifies sequence with smaller bound is assignable to sequence with larger bound:\n\n'
                        ' * Publisher uses `int32x10` from `sequences`.\n'
                        ' * Subscriber uses `int32x20` from `sequences`.\n'
                        ' * Publisher uses `sequence<int32, 10>`.\n'
                        ' * Subscriber uses `sequence<int32, 20>`.\n'
                        ' * Subscriber bound >= publisher bound, and data fits.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'seq(int32,10)_seq(int32,20)_check_bounds' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::int32x10 --data-folder data --data-file array_num_10',
                  'sub-exe -S -t test -y Test::int32x20 --data-folder data --data-file array_num_10 --ignore-seq-bounds f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between int32x10 and int32x20 (subscriber with ignore_seq_bounds false)',
        'description' : 'Verifies sequence with smaller bound is assignable to sequence with larger bound:\n\n'
                        ' * Publisher uses `int32x10` from `sequences`.\n'
                        ' * Subscriber uses `int32x20` from `sequences`.\n'
                        ' * Publisher uses `sequence<int32, 10>`.\n'
                        ' * Subscriber uses `sequence<int32, 20>`.\n'
                        ' * Subscriber bound >= publisher bound, and data fits.\n'
                        ' * Subscriber sets `--ignore-seq-bounds` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'seq(str10,10)_seq(str20,10)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::string10x10 --data-folder data --data-file array_string_10',
                  'sub-exe -S -t test -y Test::string20x10 --data-folder data --data-file array_string_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between string10x10 and string20x10',
        'description' : 'Verifies sequences of strings with different string bounds are assignable:\n\n'
                        ' * Publisher uses `string10x10` from `sequences`.\n'
                        ' * Subscriber uses `string20x10` from `sequences`.\n'
                        ' * Both are `sequence<string, 10>`.\n'
                        ' * Publisher string bound is 10, subscriber is 20.\n'
                        ' * String elements are strongly assignable since subscriber bound >= publisher bound.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'seq(str20,10)_seq(str10,10)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::string20x10 --data-folder data --data-file array_string_10',
                  'sub-exe -S -t test -y Test::string10x10 --data-folder data --data-file array_string_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between string20x10 and string10x10',
        'description' : 'Verifies sequences of strings where publisher string bound exceeds subscriber string bound:\n\n'
                        ' * Publisher uses `string20x10` from `sequences`.\n'
                        ' * Subscriber uses `string10x10` from `sequences`.\n'
                        ' * Both are `sequence<string, 10>`.\n'
                        ' * Publisher string bound is 20, subscriber is 10.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'seq(str20,10)_seq(str10,10)_check' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::string20x10 --data-folder data --data-file array_string_10',
                  'sub-exe -S -t test -y Test::string10x10 --data-folder data --data-file array_string_10 --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between string20x10 and string10x10 (subscriber with ignore_str_bounds false)',
        'description' : 'Verifies sequences of strings where publisher string bound exceeds subscriber string bound:\n\n'
                        ' * Publisher uses `string20x10` from `sequences`.\n'
                        ' * Subscriber uses `string10x10` from `sequences`.\n'
                        ' * Both are `sequence<string, 10>`.\n'
                        ' * Publisher string bound is 20, subscriber is 10.\n'
                        ' * Subscriber sets `--ignore-str-bounds` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'seq(enum1)_seq(enum2)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::enum1 --data-folder data --data-file array_enum_10',
                  'sub-exe -S -t test -y Test::enum2 --data-folder data --data-file array_enum_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between enum1 and enum2',
        'description' : 'Verifies appendable enums where subscriber is a superset are assignable:\n\n'
                        ' * Publisher uses `enum1` from `sequences`.\n'
                        ' * Subscriber uses `enum2` from `sequences`.\n'
                        ' * Publisher uses `E1` (3 literals: VAL0-VAL2).\n'
                        ' * Subscriber uses `E2` (4 literals: VAL0-VAL3).\n'
                        ' * `E2` is a superset of `E1`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'seq(SFinal,10)_seq(SFinalAlt,10)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::F_S__seq10_F_S__seq20_uint32 --data-folder data --data-file array_array_num_10_20',
                  'sub-exe -S -t test -y Test::F_S__seq10_F_S__seq20_uint32_alt --data-folder data --data-file array_array_num_10_20_alt'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between F_S__seq10_F_S__seq20_uint32 and F_S__seq10_F_S__seq20_uint32_alt',
        'description' : 'Verifies sequences of final structs are assignable when inner elements are strongly assignable:\n\n'
                        ' * Publisher uses `F_S__seq10_F_S__seq20_uint32` from `sequences`.\n'
                        ' * Subscriber uses `F_S__seq10_F_S__seq20_uint32_alt` from `sequences`.\n'
                        ' * Both are sequences of final structs containing `uint32` sequences.\n'
                        ' * Member names differ (`x1` vs `altx1`) but types are structurally equivalent.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'seq(SAppendable,10)_seq(SAppendableAlt,10)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::F_S__seq10_A_S__seq20_uint32 --data-folder data --data-file array_array_num_10_20',
                  'sub-exe -S -t test -y Test::F_S__seq10_A_S__seq20_uint32_alt --data-folder data --data-file array_array_num_10_20_alt'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between F_S__seq10_A_S__seq20_uint32 and F_S__seq10_A_S__seq20_uint32_alt',
        'description' : 'Verifies sequences of appendable structs are assignable when inner elements are strongly assignable:\n\n'
                        ' * Publisher uses `F_S__seq10_A_S__seq20_uint32` from `sequences`.\n'
                        ' * Subscriber uses `F_S__seq10_A_S__seq20_uint32_alt` from `sequences`.\n'
                        ' * Both are sequences of appendable structs containing `uint32` sequences.\n'
                        ' * Member names differ (`x1` vs `altx1`).\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'seq(SMutable,10)_seq(SMutableAlt,10)' : {
        'common_args' : ['--type-folder types --type-file sequences'],
        'apps' : ['pub-exe -P -t test -y Test::F_S__seq10_M_S__seq20_uint32 --data-folder data --data-file array_array_num_10_20',
                  'sub-exe -S -t test -y Test::F_S__seq10_M_S__seq20_uint32_alt --data-folder data --data-file array_array_num_10_20_alt'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between F_S__seq10_M_S__seq20_uint32 and F_S__seq10_M_S__seq20_uint32_alt',
        'description' : 'Verifies sequences of mutable structs are assignable when inner elements are strongly assignable:\n\n'
                        ' * Publisher uses `F_S__seq10_M_S__seq20_uint32` from `sequences`.\n'
                        ' * Subscriber uses `F_S__seq10_M_S__seq20_uint32_alt` from `sequences`.\n'
                        ' * Both are sequences of mutable structs containing `uint32` sequences.\n'
                        ' * Member names differ (`x1` vs `altx1`).\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
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
        'title' : 'Communication between identical string_unbounded',
        'description' : 'Verifies identical unbounded strings communicate:\n\n'
                        ' * Publisher and Subscriber use `string_unbounded` from `strings`.\n'
                        ' * Both use unbounded `string` type.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'string_string10' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::string_unbounded --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10 --data-folder data --data-file strings'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between string_unbounded and string10 but sample rejected',
        'description' : 'Verifies unbounded string sending data exceeding subscriber bound:\n\n'
                        ' * Publisher uses `string_unbounded` from `strings`.\n'
                        ' * Subscriber uses `string10` from `strings`.\n'
                        ' * Publisher uses unbounded `string`.\n'
                        ' * Subscriber uses `string<10>`.\n'
                        ' * The published string ("hello world!") exceeds the subscriber bound.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },
    'string_string10_check' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::string_unbounded --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10 --data-folder data --data-file strings --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between string_unbounded and string10 (subscriber with ignore_str_bounds false)',
        'description' : 'Verifies unbounded string sending data exceeding subscriber bound:\n\n'
                        ' * Publisher uses `string_unbounded` from `strings`.\n'
                        ' * Subscriber uses `string10` from `strings`.\n'
                        ' * Publisher uses unbounded `string`.\n'
                        ' * Subscriber uses `string<10>`.\n'
                        ' * The published string ("hello world!") exceeds the subscriber bound.\n'
                        ' * Subscriber sets `--ignore-str-bounds` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'string10_string20_check' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::string10 --data-folder data --data-file strings_hello',
                  'sub-exe -S -t test -y Test::string20 --data-folder data --data-file strings_hello --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between string10 and string20 (subscriber with ignore_str_bounds false)',
        'description' : 'Verifies string with smaller bound is assignable to string with larger bound:\n\n'
                        ' * Publisher uses `string10` from `strings`.\n'
                        ' * Subscriber uses `string20` from `strings`.\n'
                        ' * Publisher uses `string<10>`.\n'
                        ' * Subscriber uses `string<20>`.\n'
                        ' * Subscriber bound >= publisher bound.\n'
                        ' * Subscriber sets `--ignore-str-bounds` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'string20_string10_check' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10 --data-folder data --data-file strings --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between string20 and string10 (subscriber with ignore_str_bounds false)',
        'description' : 'Verifies string without explicit `@try_construct` and oversized data:\n\n'
                        ' * Publisher uses `string20` from `strings`.\n'
                        ' * Subscriber uses `string10` from `strings`.\n'
                        ' * Publisher string bound is 20.\n'
                        ' * Subscriber bound is 10 with no `@try_construct` annotation.\n'
                        ' * Default behavior (discard) applies to oversized strings.\n'
                        ' * Subscriber sets `--ignore-str-bounds` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },

    'wstring_wstring' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::wstring_unbounded --data-folder data --data-file wstrings',
                  'sub-exe -S -t test -y Test::wstring_unbounded --data-folder data --data-file wstrings'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between identical wstring_unbounded',
        'description' : 'Verifies identical unbounded wide strings communicate:\n\n'
                        ' * Publisher and Subscriber use `wstring_unbounded` from `strings`.\n'
                        ' * Both use unbounded `wstring` type.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'wstring_wstring10' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::wstring_unbounded --data-folder data --data-file wstrings',
                  'sub-exe -S -t test -y Test::wstring10 --data-folder data --data-file wstrings'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between wstring_unbounded and wstring10 but sample rejected',
        'description' : 'Verifies unbounded wstring sending data exceeding subscriber bound:\n\n'
                        ' * Publisher uses `wstring_unbounded` from `strings`.\n'
                        ' * Subscriber uses `wstring10` from `strings`.\n'
                        ' * Publisher uses unbounded `wstring`.\n'
                        ' * Subscriber uses `wstring<10>`.\n'
                        ' * The published wstring exceeds the subscriber bound.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },
    'wstring_wstring10_check' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::wstring_unbounded --data-folder data --data-file wstrings',
                  'sub-exe -S -t test -y Test::wstring10 --data-folder data --data-file wstrings --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between wstring_unbounded and wstring10 (subscriber with ignore_str_bounds false)',
        'description' : 'Verifies unbounded wstring sending data exceeding subscriber bound:\n\n'
                        ' * Publisher uses `wstring_unbounded` from `strings`.\n'
                        ' * Subscriber uses `wstring10` from `strings`.\n'
                        ' * Publisher uses unbounded `wstring`.\n'
                        ' * Subscriber uses `wstring<10>`.\n'
                        ' * The published wstring exceeds the subscriber bound.\n'
                        ' * Subscriber sets `--ignore-str-bounds` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'wstring10_wstring20_check' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::wstring10 --data-folder data --data-file wstrings_hello',
                  'sub-exe -S -t test -y Test::wstring20 --data-folder data --data-file wstrings_hello --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between wstring10 and wstring20 (subscriber with ignore_str_bounds false)',
        'description' : 'Verifies wstring with smaller bound is assignable to wstring with larger bound:\n\n'
                        ' * Publisher uses `wstring10` from `strings`.\n'
                        ' * Subscriber uses `wstring20` from `strings`.\n'
                        ' * Publisher uses `wstring<10>`.\n'
                        ' * Subscriber uses `wstring<20>`.\n'
                        ' * Subscriber bound >= publisher bound.\n'
                        ' * Subscriber sets `--ignore-str-bounds` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'wstring20_wstring10_check' : {
        'common_args' : ['--type-folder types --type-file strings'],
        'apps' : ['pub-exe -P -t test -y Test::wstring20 --data-folder data --data-file wstrings',
                  'sub-exe -S -t test -y Test::wstring10 --data-folder data --data-file wstrings --ignore-str-bounds f'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between wstring20 and wstring10 (subscriber with ignore_str_bounds false)',
        'description' : 'Verifies wstring with larger bound is not assignable when bounds are checked:\n\n'
                        ' * Publisher uses `wstring20` from `strings`.\n'
                        ' * Subscriber uses `wstring10` from `strings`.\n'
                        ' * Publisher uses `wstring<20>`.\n'
                        ' * Subscriber uses `wstring<10>`.\n'
                        ' * Publisher bound exceeds subscriber bound.\n'
                        ' * Subscriber sets `--ignore-str-bounds` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
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
        'title' : 'Communication between identical struct_primitives_final',
        'description' : 'Verifies identical final primitive structs communicate:\n\n'
                        ' * Publisher and Subscriber use `struct_primitives_final` (final) from `primitives`.\n'
                        ' * Both use the same final struct with 14 primitive members (uint8 through char8).\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'primitives_struct_appendable' : {
        'common_args' : ['--type-folder types --type-file primitives'],
        'apps' : ['pub-exe -P -t test -y Test::struct_primitives_appendable --data-folder data --data-file struct_primitives',
                  'sub-exe -S -t test -y Test::struct_primitives_appendable --data-folder data --data-file struct_primitives'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between identical struct_primitives_appendable',
        'description' : 'Verifies identical appendable primitive structs communicate:\n\n'
                        ' * Publisher and Subscriber use `struct_primitives_appendable` (appendable) from `primitives`.\n'
                        ' * Both use the same appendable struct with 14 primitive members.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'primitives_struct_mutable': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitives_mutable --data-folder data --data-file struct_primitives',
                 'sub-exe -S -t test -y Test::struct_primitives_mutable --data-folder data --data-file struct_primitives'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical struct_primitives_mutable',
        'description' : 'Verifies identical mutable primitive structs communicate:\n\n'
                        ' * Publisher and Subscriber use `struct_primitives_mutable` (mutable) from `primitives`.\n'
                        ' * Both use the same mutable struct with 14 primitive members.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_final_appendable': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitives_final --data-folder data --data-file struct_primitives',
                 'sub-exe -S -t test -y Test::struct_primitives_appendable --data-folder data --data-file struct_primitives'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitives_final and struct_primitives_appendable',
        'description' : 'Verifies structs with mismatched extensibility are not assignable:\n\n'
                        ' * Publisher uses `struct_primitives_final` (final) from `primitives`.\n'
                        ' * Subscriber uses `struct_primitives_appendable` (appendable) from `primitives`.\n'
                        ' * Publisher is `final`.\n'
                        ' * Subscriber is `appendable`.\n'
                        ' * Extensibility must match for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_final_mutable': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitives_final --data-folder data --data-file struct_primitives',
                 'sub-exe -S -t test -y Test::struct_primitives_mutable --data-folder data --data-file struct_primitives'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitives_final and struct_primitives_mutable',
        'description' : 'Verifies structs with mismatched extensibility are not assignable:\n\n'
                        ' * Publisher uses `struct_primitives_final` (final) from `primitives`.\n'
                        ' * Subscriber uses `struct_primitives_mutable` (mutable) from `primitives`.\n'
                        ' * Publisher is `final`.\n'
                        ' * Subscriber is `mutable`.\n'
                        ' * Extensibility must match for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_appendable_final': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitives_appendable --data-folder data --data-file struct_primitives',
                 'sub-exe -S -t test -y Test::struct_primitives_final --data-folder data --data-file struct_primitives'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitives_appendable and struct_primitives_final',
        'description' : 'Verifies structs with mismatched extensibility are not assignable:\n\n'
                        ' * Publisher uses `struct_primitives_appendable` (appendable) from `primitives`.\n'
                        ' * Subscriber uses `struct_primitives_final` (final) from `primitives`.\n'
                        ' * Publisher is `appendable`.\n'
                        ' * Subscriber is `final`.\n'
                        ' * Extensibility must match for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_appendable_mutable': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitives_appendable --data-folder data --data-file struct_primitives',
                 'sub-exe -S -t test -y Test::struct_primitives_mutable --data-folder data --data-file struct_primitives'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitives_appendable and struct_primitives_mutable',
        'description' : 'Verifies structs with mismatched extensibility are not assignable:\n\n'
                        ' * Publisher uses `struct_primitives_appendable` (appendable) from `primitives`.\n'
                        ' * Subscriber uses `struct_primitives_mutable` (mutable) from `primitives`.\n'
                        ' * Publisher is `appendable`.\n'
                        ' * Subscriber is `mutable`.\n'
                        ' * Extensibility must match for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_mutable_final': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitives_mutable --data-folder data --data-file struct_primitives',
                 'sub-exe -S -t test -y Test::struct_primitives_final --data-folder data --data-file struct_primitives'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitives_mutable and struct_primitives_final',
        'description' : 'Verifies structs with mismatched extensibility are not assignable:\n\n'
                        ' * Publisher uses `struct_primitives_mutable` (mutable) from `primitives`.\n'
                        ' * Subscriber uses `struct_primitives_final` (final) from `primitives`.\n'
                        ' * Publisher is `mutable`.\n'
                        ' * Subscriber is `final`.\n'
                        ' * Extensibility must match for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_mutable_appendable': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitives_mutable --data-folder data --data-file struct_primitives',
                 'sub-exe -S -t test -y Test::struct_primitives_appendable --data-folder data --data-file struct_primitives'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitives_mutable and struct_primitives_appendable',
        'description' : 'Verifies structs with mismatched extensibility are not assignable:\n\n'
                        ' * Publisher uses `struct_primitives_mutable` (mutable) from `primitives`.\n'
                        ' * Subscriber uses `struct_primitives_appendable` (appendable) from `primitives`.\n'
                        ' * Publisher is `mutable`.\n'
                        ' * Subscriber is `appendable`.\n'
                        ' * Extensibility must match for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_different_ids_ok': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_1 --data-folder data --data-file struct_num_x1_x5',
                 'sub-exe -S -t test -y Test::struct_2 --data-folder data --data-file struct_num_x5'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between struct_1 and struct_2',
        'description' : 'Verifies mutable structs where member names match but IDs differ are assignable by default:\n\n'
                        ' * Publisher uses `struct_1` from `struct_names`.\n'
                        ' * Subscriber uses `struct_2` from `struct_names`.\n'
                        ' * Both have member `x1` but with different IDs (id=1 in publisher, id=2 in subscriber). Both share member `x5` (id=5). By default, `ignore_member_names` is true so ID matching is used.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_different_ids': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_1 --data-folder data --data-file struct_num_x1_x5',
                 'sub-exe -S -t test -y Test::struct_2 --data-folder data --data-file struct_num_x1_x5 --ignore-member-names f'
        ],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_1 and struct_2 (subscriber with ignore_member_names false)',
        'description' : 'Verifies mutable structs where member names match but IDs differ are assignable by default:\n\n'
                        ' * Publisher uses `struct_1` from `struct_names`.\n'
                        ' * Subscriber uses `struct_2` from `struct_names`.\n'
                        ' * Both have member `x1` but with different IDs (id=1 in publisher, id=2 in subscriber). Both share member `x5` (id=5). By default, `ignore_member_names` is true so ID matching is used.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_different_names_ok': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_3 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_4 --data-folder data --data-file struct_num_x2'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between struct_3 and struct_4',
        'description' : 'Verifies final structs where member IDs match but names differ:\n\n'
                        ' * Publisher uses `struct_3` from `struct_names`.\n'
                        ' * Subscriber uses `struct_4` from `struct_names`.\n'
                        ' * Both have one member at id=1, but named `x1` in publisher and `x2` in subscriber.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_different_names': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_3 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_4 --data-folder data --data-file struct_num_x2 --ignore-member-names f'
        ],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_3 and struct_4 (subscriber with ignore_member_names false)',
        'description' : 'Verifies final structs where member IDs match but names differ:\n\n'
                        ' * Publisher uses `struct_3` from `struct_names`.\n'
                        ' * Subscriber uses `struct_4` from `struct_names`.\n'
                        ' * Both have one member at id=1, but named `x1` in publisher and `x2` in subscriber.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_no_common_ids': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_5 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_6 --data-folder data --data-file struct_num_x2'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_5 and struct_6',
        'description' : 'Verifies mutable structs with no common member IDs are not assignable:\n\n'
                        ' * Publisher uses `struct_5` (mutable) from `struct_names`.\n'
                        ' * Subscriber uses `struct_6` (mutable) from `struct_names`.\n'
                        ' * `struct_5` has member `x1` (id=1).\n'
                        ' * `struct_6` has member `x2` (id=2).\n'
                        ' * No common member IDs exist.\n'
                        ' * Mutable extensibility requires at least one member in common (same ID).\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_members_assignable_1': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint8 and struct_primitive_uint16',
        'description' : 'Verifies structs with non-assignable member types are not assignable:\n\n'
                        ' * Publisher uses `struct_primitive_uint8` from `struct_names`.\n'
                        ' * Subscriber uses `struct_primitive_uint16` from `struct_names`.\n'
                        ' * Both are final with one member `x1`, but publisher declares it as `byte` and subscriber as `uint16`. Members with matching IDs must have assignable types.\n'
                        ' * `byte` and `uint16` are not assignable.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_mustUnderstand_1': {
        'common_args': ['--type-folder types --type-file struct_w_mustunderstand'],
        'apps': ['pub-exe -P -t test -y Test::struct_mustUnderstand --data-folder data --data-file struct_num_x1_x2',
                 'sub-exe -S -t test -y Test::struct_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_mustUnderstand and struct_int32',
        'description' : 'Verifies subscriber cannot ignore a `@must_understand` member from the publisher:\n\n'
                        ' * Publisher uses `struct_mustUnderstand` from `struct_w_mustunderstand`.\n'
                        ' * Subscriber uses `struct_int32` from `struct_w_mustunderstand`.\n'
                        ' * Publisher\'s `struct_mustUnderstand` has member `x2` annotated with `@must_understand`.\n'
                        ' * Subscriber\'s `struct_int32` only has `x1`.\n'
                        ' * A non-optional `@must_understand` member must appear in both types.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_mustUnderstand_2': {
        'common_args': ['--type-folder types --type-file struct_w_mustunderstand'],
        'apps': ['pub-exe -P -t test -y Test::struct_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_mustUnderstand --data-folder data --data-file struct_num_x1_x2'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_int32 and struct_mustUnderstand',
        'description' : 'Verifies subscriber\'s extra `@must_understand` member must be present in the publisher type:\n\n'
                        ' * Publisher uses `struct_int32` from `struct_w_mustunderstand`.\n'
                        ' * Subscriber uses `struct_mustUnderstand` from `struct_w_mustunderstand`.\n'
                        ' * Subscriber\'s `struct_mustUnderstand` has member `x2` annotated with `@must_understand`.\n'
                        ' * Publisher\'s `struct_int32` only has `x1`.\n'
                        ' * A non-optional `@must_understand` member must appear in both types.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_key_1': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_1 --data-folder data --data-file struct_num_x1_x2',
                 'sub-exe -S -t test -y Test::struct_key_2 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_key_1 and struct_key_2',
        'description' : 'Verifies `@key` members in one type must be present in the other:\n\n'
                        ' * Publisher uses `struct_key_1` from `struct_names`.\n'
                        ' * Subscriber uses `struct_key_2` from `struct_names`.\n'
                        ' * Publisher\'s `struct_key_1` has `@key` member `x2` (`int32`).\n'
                        ' * Subscriber\'s `struct_key_2` only has `x1`.\n'
                        ' * Key members must appear in both types for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_key_2': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_2 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_key_1 --data-folder data --data-file struct_num_x1_x2'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_key_2 and struct_key_1',
        'description' : 'Verifies `@key` members in one type must be present in the other:\n\n'
                        ' * Publisher uses `struct_key_2` from `struct_names`.\n'
                        ' * Subscriber uses `struct_key_1` from `struct_names`.\n'
                        ' * Subscriber\'s `struct_key_1` has `@key` member `x2` (`int32`).\n'
                        ' * Publisher\'s `struct_key_2` only has `x1`.\n'
                        ' * Key members must appear in both types for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_key_string_1': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_string10 --data-folder data --data-file struct_str_x1',
                 'sub-exe -S -t test -y Test::struct_key_string20 --data-folder data --data-file struct_str_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between struct_key_string10 and struct_key_string20',
        'description' : 'Verifies `@key` string member with smaller publisher bound is assignable to larger subscriber bound:\n\n'
                        ' * Publisher uses `struct_key_string10` from `struct_names`.\n'
                        ' * Subscriber uses `struct_key_string20` from `struct_names`.\n'
                        ' * Both have `@key` string member `x1`.\n'
                        ' * Publisher bound is 10, subscriber bound is 20.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_key_string_2': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_string10 --data-folder data --data-file struct_str_x1',
                 'sub-exe -S -t test -y Test::struct_key_string10 --data-folder data --data-file struct_str_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical struct_key_string10',
        'description' : 'Verifies identical `@key` string structs communicate:\n\n'
                        ' * Publisher and Subscriber use `struct_key_string10` from `struct_names`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
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
        'title' : 'Communication between struct_key_string20 and struct_key_string10',
        'description' : 'Verifies `@key` string member where publisher bound exceeds subscriber bound:\n\n'
                        ' * Publisher uses `struct_key_string20` from `struct_names`.\n'
                        ' * Subscriber uses `struct_key_string10` from `struct_names`.\n'
                        ' * Both have `@key` string member `x1`.\n'
                        ' * Publisher bound is 20, subscriber bound is 10.\n'
                        ' * Key string bounds are checked regardless of `ignore_string_bounds`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_key_enum_1': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_enum_1 --data-folder data --data-file struct_enum',
                 'sub-exe -S -t test -y Test::struct_key_enum_2 --data-folder data --data-file struct_enum'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between struct_key_enum_1 and struct_key_enum_2',
        'description' : 'Verifies `@key` enum member where subscriber enum is a superset:\n\n'
                        ' * Publisher uses `struct_key_enum_1` from `struct_names`.\n'
                        ' * Subscriber uses `struct_key_enum_2` from `struct_names`.\n'
                        ' * Both have `@key` enum member `x1`.\n'
                        ' * Publisher uses `E1` (3 literals: VAL0-VAL2), subscriber uses `E2` (4 literals: VAL0-VAL3).\n'
                        ' * Subscriber\'s enum is a superset.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_key_enum_2': {
        # CT: reader type @key has fewer enum literals than writer type, I don't think should match
        # -- i expect INCONSISTENT_TOPIC here...
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_enum_2 --data-folder data --data-file struct_enum',
                 'sub-exe -S -t test -y Test::struct_key_enum_1 --data-folder data --data-file struct_enum'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between struct_key_enum_2 and struct_key_enum_1',
        'description' : 'Verifies `@key` enum member where publisher has more literals than subscriber:\n\n'
                        ' * Publisher uses `struct_key_enum_2` from `struct_names`.\n'
                        ' * Subscriber uses `struct_key_enum_1` from `struct_names`.\n'
                        ' * Both have `@key` enum member `x1`.\n'
                        ' * Publisher uses `E2` (4 literals: VAL0-VAL3), subscriber uses `E1` (3 literals: VAL0-VAL2).\n'
                        ' * Publisher can send literal `VAL3` which subscriber cannot represent.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_key_seq_1': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_seq10 --data-folder data --data-file struct_seq',
                 'sub-exe -S -t test -y Test::struct_key_seq20 --data-folder data --data-file struct_seq'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between struct_key_seq10 and struct_key_seq20',
        'description' : 'Verifies `@key` sequence member with smaller publisher bound is assignable:\n\n'
                        ' * Publisher uses `struct_key_seq10` from `struct_names`.\n'
                        ' * Subscriber uses `struct_key_seq20` from `struct_names`.\n'
                        ' * Both have `@key` sequence member `x1`.\n'
                        ' * Publisher bound is 10, subscriber bound is 20.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_key_seq_2': {
        # CT: reader type @key has smaller seq bound than writer type, I don't think should match
        # -- i expect INCONSISTENT_TOPIC here...
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_seq20 --data-folder data --data-file struct_seq',
                 'sub-exe -S -t test -y Test::struct_key_seq10 --data-folder data --data-file struct_seq'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between struct_key_seq20 and struct_key_seq10',
        'description' : 'Verifies `@key` sequence member where publisher bound exceeds subscriber bound:\n\n'
                        ' * Publisher uses `struct_key_seq20` from `struct_names`.\n'
                        ' * Subscriber uses `struct_key_seq10` from `struct_names`.\n'
                        ' * Both have `@key` sequence member `x1`.\n'
                        ' * Publisher bound is 20, subscriber bound is 10.\n'
                        ' * Key sequence bounds are checked regardless of `ignore_sequence_bounds`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_key_struct_1': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_struct_1 --data-folder data --data-file struct_str_key',
                 'sub-exe -S -t test -y Test::struct_key_struct_2 --data-folder data --data-file struct_str_key'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between struct_key_struct_1 and struct_key_struct_2',
        'description' : 'Verifies `@key` struct member where inner types are assignable:\n\n'
                        ' * Publisher uses `struct_key_struct_1` from `struct_names`.\n'
                        ' * Subscriber uses `struct_key_struct_2` from `struct_names`.\n'
                        ' * Both have `@key` struct member `x1`.\n'
                        ' * Publisher inner type `key_1` has string bounds (k1=10, x2=20), subscriber inner type `key_2` has (k1=20, x2=10).\n'
                        ' * Key holder assignability is checked.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_key_struct_2': {
        # CT: reader type @key has smaller string bound than writer type, I don't think should match 
        # -- i expect INCONSISTENT_TOPIC here...
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_struct_2 --data-folder data --data-file struct_str_key',
                 'sub-exe -S -t test -y Test::struct_key_struct_1 --data-folder data --data-file struct_str_key'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between struct_key_struct_2 and struct_key_struct_1',
        'description' : 'Verifies `@key` struct member where inner key string bound is reversed:\n\n'
                        ' * Publisher uses `struct_key_struct_2` from `struct_names`.\n'
                        ' * Subscriber uses `struct_key_struct_1` from `struct_names`.\n'
                        ' * Both have `@key` struct member `x1`.\n'
                        ' * Publisher inner type `key_2` has key string bound 20, subscriber inner type `key_1` has key string bound 10.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_key_union_1': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_union_1 --data-folder data --data-file struct_key_union',
                 'sub-exe -S -t test -y Test::struct_key_union_2 --data-folder data --data-file struct_key_union'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between struct_key_union_1 and struct_key_union_2',
        'description' : 'Verifies `@key` union member where subscriber union has additional case:\n\n'
                        ' * Publisher uses `struct_key_union_1` from `struct_names`.\n'
                        ' * Subscriber uses `struct_key_union_2` from `struct_names`.\n'
                        ' * Both have `@key` union member `x1`.\n'
                        ' * Publisher uses `u_1` (cases 1,2), subscriber uses `u_2` (cases 1,2,3).\n'
                        ' * Subscriber union is a superset.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_key_union_2': {
        'common_args': ['--type-folder types --type-file struct_names'],
        'apps': ['pub-exe -P -t test -y Test::struct_key_union_2 --data-folder data --data-file struct_key_union',
                 'sub-exe -S -t test -y Test::struct_key_union_1 --data-folder data --data-file struct_key_union'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between struct_key_union_2 and struct_key_union_1',
        'description' : 'Verifies `@key` union member where publisher union has additional case:\n\n'
                        ' * Publisher uses `struct_key_union_2` from `struct_names`.\n'
                        ' * Subscriber uses `struct_key_union_1` from `struct_names`.\n'
                        ' * Both have `@key` union member `x1`.\n'
                        ' * Publisher uses `u_2` (cases 1,2,3), subscriber uses `u_1` (cases 1,2).\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
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
        'title' : 'Communication between identical union_primitives_final',
        'description' : 'Verifies identical final primitive unions communicate:\n\n'
                        ' * Publisher and Subscriber use `union_primitives_final` (final) from `unions`.\n'
                        ' * Both use the same final union with 14 cases covering all primitive types.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'union_primitives_appendable': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_primitives_appendable --data-folder data --data-file union_primitive',
                 'sub-exe -S -t test -y Test::union_primitives_appendable --data-folder data --data-file union_primitive'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical union_primitives_appendable',
        'description' : 'Verifies identical appendable primitive unions communicate:\n\n'
                        ' * Publisher and Subscriber use `union_primitives_appendable` (appendable) from `unions`.\n'
                        ' * Both use the same appendable union with 14 cases.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'union_primitives_mutable': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_primitives_mutable --data-folder data --data-file union_primitive',
                 'sub-exe -S -t test -y Test::union_primitives_mutable --data-folder data --data-file union_primitive'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical union_primitives_mutable',
        'description' : 'Verifies identical mutable primitive unions communicate:\n\n'
                        ' * Publisher and Subscriber use `union_primitives_mutable` (mutable) from `unions`.\n'
                        ' * Both use the same mutable union with 14 cases.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'union_final_appendable': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_primitives_final --data-folder data --data-file union_primitive',
                 'sub-exe -S -t test -y Test::union_primitives_appendable --data-folder data --data-file union_primitive'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_primitives_final and union_primitives_appendable',
        'description' : 'Verifies unions with mismatched extensibility are not assignable:\n\n'
                        ' * Publisher uses `union_primitives_final` (final) from `unions`.\n'
                        ' * Subscriber uses `union_primitives_appendable` (appendable) from `unions`.\n'
                        ' * Publisher is `final`.\n'
                        ' * Subscriber is `appendable`.\n'
                        ' * Extensibility must match.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_final_mutable': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_primitives_final --data-folder data --data-file union_primitive',
                 'sub-exe -S -t test -y Test::union_primitives_mutable --data-folder data --data-file union_primitive'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_primitives_final and union_primitives_mutable',
        'description' : 'Verifies unions with mismatched extensibility are not assignable:\n\n'
                        ' * Publisher uses `union_primitives_final` (final) from `unions`.\n'
                        ' * Subscriber uses `union_primitives_mutable` (mutable) from `unions`.\n'
                        ' * Publisher is `final`.\n'
                        ' * Subscriber is `mutable`.\n'
                        ' * Extensibility must match.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_appendable_mutable': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_primitives_appendable --data-folder data --data-file union_primitive',
                 'sub-exe -S -t test -y Test::union_primitives_mutable --data-folder data --data-file union_primitive'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_primitives_appendable and union_primitives_mutable',
        'description' : 'Verifies unions with mismatched extensibility are not assignable:\n\n'
                        ' * Publisher uses `union_primitives_appendable` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_primitives_mutable` (mutable) from `unions`.\n'
                        ' * Publisher is `appendable`.\n'
                        ' * Subscriber is `mutable`.\n'
                        ' * Extensibility must match.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_uint32_bitmask32': {
        'common_args': [''],
        'apps': ['pub-exe -P -t test --type-folder types --type-file unions         -y Test::union_uint32    --data-folder data --data-file union_uint32',
                 'sub-exe -S -t test --type-folder types --type-file unions_bitmask -y Test::union_bitmask32 --data-folder data --data-file union_bitmask'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between union_uint32 and union_bitmask32',
        'description' : 'Verifies unions with strongly-assignable discriminator types communicate:\n\n'
                        ' * Publisher uses `union_uint32` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_bitmask32` (appendable) from `unions_bitmask`.\n'
                        ' * Publisher discriminator is `uint32`.\n'
                        ' * Subscriber discriminator is `bitmask` with `bitBound=32`.\n'
                        ' * A 32-bit bitmask is strongly assignable from `uint32`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'union_uint32_bitmask16': {
        'common_args': [''],
        'apps': ['pub-exe -P -t test --type-folder types --type-file unions         -y Test::union_uint32    --data-folder data --data-file union_uint32',
                 'sub-exe -S -t test --type-folder types --type-file unions_bitmask -y Test::union_bitmask16 --data-folder data --data-file union_bitmask'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_uint32 and union_bitmask16',
        'description' : 'Verifies unions with non-assignable discriminator types are not assignable:\n\n'
                        ' * Publisher uses `union_uint32` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_bitmask16` (appendable) from `unions_bitmask`.\n'
                        ' * Publisher discriminator is `uint32`.\n'
                        ' * Subscriber discriminator is `bitmask` with `bitBound=16`.\n'
                        ' * A 16-bit bitmask is not strongly assignable from `uint32`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_uint32_one_key': {
        'common_args': [''],
        'apps': ['pub-exe -P -t test --type-folder types --type-file unions                   -y Test::union_uint32     --data-folder data --data-file union_uint32',
                 'sub-exe -S -t test --type-folder types --type-file unions_key_discriminator -y Test::union_uint32_key --data-folder data --data-file union_uint32'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_uint32 and union_uint32_key',
        'description' : 'Verifies unions where one discriminator is `@key` and the other is not are not assignable:\n\n'
                        ' * Publisher uses `union_uint32` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_uint32_key` (appendable) from `unions_key_discriminator`.\n'
                        ' * Publisher discriminator has no `@key` annotation.\n'
                        ' * Subscriber discriminator has `key="true"`.\n'
                        ' * Both must agree on whether the discriminator is `@key`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_different_ids_1': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_1 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_2 --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between union_1 and union_2',
        'description' : 'Verifies appendable unions with reordered members having different discriminator values:\n\n'
                        ' * Publisher uses `union_1` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_2` (appendable) from `unions`.\n'
                        ' * `union_1` has members `x1`(discriminator=1), `x2`(discriminator=2), `x3`(discriminator=3).\n'
                        ' * `union_2` has same members reordered: `x2`(discriminator=2), `x1`(discriminator=1), `x3`(discriminator=3).\n'
                        ' * Member order differs but discriminator/type pairs match.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'union_different_ids_2': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_1 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_2 --data-folder data --data-file union_x1 --ignore-member-names f'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_1 and union_2 (subscriber with ignore_member_names false)',
        'description' : 'Verifies appendable unions with reordered members having different discriminator values:\n\n'
                        ' * Publisher uses `union_1` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_2` (appendable) from `unions`.\n'
                        ' * `union_1` has members `x1`(discriminator=1), `x2`(discriminator=2), `x3`(discriminator=3).\n'
                        ' * `union_2` has same members reordered: `x2`(discriminator=2), `x1`(discriminator=1), `x3`(discriminator=3).\n'
                        ' * Member order differs but discriminator/type pairs match.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_different_names_1': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_3 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_4 --data-folder data --data-file union_x2'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between union_3 and union_4',
        'description' : 'Verifies appendable unions where same discriminator values map to different member names:\n\n'
                        ' * Publisher uses `union_3` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_4` (appendable) from `unions`.\n'
                        ' * `union_3` has discriminator=1->`x1`(int16), discriminator=2->`x2`(int32).\n'
                        ' * `union_4` has discriminator=1->`x2`(int16), discriminator=2->`x1`(int32).\n'
                        ' * Same discriminator values map to different names but same types.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'union_different_names_2': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_3 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_4 --data-folder data --data-file union_x2 --ignore-member-names f'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_3 and union_4 (subscriber with ignore_member_names false)',
        'description' : 'Verifies appendable unions where same discriminator values map to different member names:\n\n'
                        ' * Publisher uses `union_3` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_4` (appendable) from `unions`.\n'
                        ' * `union_3` has discriminator=1->`x1`(int16), discriminator=2->`x2`(int32).\n'
                        ' * `union_4` has discriminator=1->`x2`(int16), discriminator=2->`x1`(int32).\n'
                        ' * Same discriminator values map to different names but same types.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_different_order_1': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_5 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_6 --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between union_5 and union_6',
        'description' : 'Verifies appendable unions with explicit IDs and reordered cases:\n\n'
                        ' * Publisher uses `union_5` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_6` (appendable) from `unions`.\n'
                        ' * Both have members with explicit IDs (id=1,2,3). `union_5` has discriminator order 1,2,3.\n'
                        ' * `union_6` has discriminator order 2,1,3.\n'
                        ' * Explicit IDs ensure correct matching regardless of order.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'union_different_order_2': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_5 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_6 --data-folder data --data-file union_x1 --ignore-member-names f'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between union_5 and union_6 (subscriber with ignore_member_names false)',
        'description' : 'Verifies appendable unions with explicit IDs and reordered cases:\n\n'
                        ' * Publisher uses `union_5` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_6` (appendable) from `unions`.\n'
                        ' * Both have members with explicit IDs (id=1,2,3). `union_5` has discriminator order 1,2,3.\n'
                        ' * `union_6` has discriminator order 2,1,3.\n'
                        ' * Explicit IDs ensure correct matching regardless of order.\n'
                        ' * Subscriber sets `--ignore-member-names` to `false`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'union_int16_int32': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_int16 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_int32 --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_int16 and union_int32',
        'description' : 'Verifies unions where one discriminator label selects non-assignable member types:\n\n'
                        ' * Publisher uses `union_int16` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_int32` (appendable) from `unions`.\n'
                        ' * For discriminator=2: publisher selects `x2` as `int16`, subscriber selects `x2` as `int32`. A label that selects non-assignable types breaks assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_int16_int32_default': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_int16         --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_int32_default --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_int16 and union_int32_default',
        'description' : 'Verifies union where subscriber default case selects a non-assignable member type:\n\n'
                        ' * Publisher uses `union_int16` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_int32_default` (appendable) from `unions`.\n'
                        ' * Publisher discriminator=2 selects `x2`(`int16`).\n'
                        ' * Subscriber `default` case covers discriminator=2 and selects `x2`(`int32`).\n'
                        ' * `int16` is not assignable from `int32`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_int32_int32_default': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_int32 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_int32_default --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between union_int32 and union_int32_default',
        'description' : 'Verifies union with explicit discriminator=2 vs union with default case:\n\n'
                        ' * Publisher uses `union_int32` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_int32_default` (appendable) from `unions`.\n'
                        ' * Publisher has explicit case discriminator=2 selecting `x2`(`int32`).\n'
                        ' * Subscriber uses `default` case for `x2`(`int32`).\n'
                        ' * The default case covers discriminator=2.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'union_int32_default_int16': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_int32_default --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_int16 --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_int32_default and union_int16',
        'description' : 'Verifies union where publisher default case covers labels that select non-assignable types in subscriber:\n\n'
                        ' * Publisher uses `union_int32_default` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_int16` (appendable) from `unions`.\n'
                        ' * Publisher `default` case selects `x2`(`int32`).\n'
                        ' * Subscriber discriminator=2 selects `x2`(`int16`).\n'
                        ' * `int16` is not assignable from `int32`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_int32_default_int32': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_int32_default --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_int32 --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between union_int32_default and union_int32',
        'description' : 'Verifies union with default case vs union with explicit discriminator=2:\n\n'
                        ' * Publisher uses `union_int32_default` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_int32` (appendable) from `unions`.\n'
                        ' * Publisher uses `default` case for `x2`(`int32`).\n'
                        ' * Subscriber has explicit case discriminator=2 selecting `x2`(`int32`).\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'union_int32_default_int16_default': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_int32_default --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_int16_default --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_int32_default and union_int16_default',
        'description' : 'Verifies unions where both have default cases but with non-assignable member types:\n\n'
                        ' * Publisher uses `union_int32_default` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_int16_default` (appendable) from `unions`.\n'
                        ' * Both have a `default` case: publisher selects `x2`(`int32`), subscriber selects `x2`(`int16`). `int16` is not assignable from `int32`.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_int32_default_int32_default': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_int32_default --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_int32_default --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical union_int32_default',
        'description' : 'Verifies identical unions with default discriminator communicate:\n\n'
                        ' * Publisher and Subscriber use `union_int32_default` (appendable) from `unions`.\n'
                        ' * Both use `union_int32_default` with a `default` case selecting `int32` member `x2`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'union_final_5_vs_6': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_final_5 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_final_6 --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_final_5 and union_final_6',
        'description' : 'Verifies final unions with different numbers of cases:\n\n'
                        ' * Publisher uses `union_final_5` (final) from `unions`.\n'
                        ' * Subscriber uses `union_final_6` (final) from `unions`.\n'
                        ' * `union_final_5` has 5 cases (discriminator 1-5).\n'
                        ' * `union_final_6` has 6 cases (disc 0-5).\n'
                        ' * Final unions must have the same set of discriminator labels.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_final_6_vs_5': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_final_6 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_final_5 --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_final_6 and union_final_5',
        'description' : 'Verifies final unions with different numbers of cases (reverse direction):\n\n'
                        ' * Publisher uses `union_final_6` (final) from `unions`.\n'
                        ' * Subscriber uses `union_final_5` (final) from `unions`.\n'
                        ' * `union_final_6` has 6 cases (disc 0-5).\n'
                        ' * `union_final_5` has 5 cases (discriminator 1-5).\n'
                        ' * Final unions must have the same set of discriminator labels.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_final_one_default_1': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_final_5 --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_final_5_default --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_final_5 and union_final_5_default',
        'description' : 'Verifies final unions where one has a default case:\n\n'
                        ' * Publisher uses `union_final_5` (final) from `unions`.\n'
                        ' * Subscriber uses `union_final_5_default` (final) from `unions`.\n'
                        ' * `union_final_5` has 5 explicit cases (discriminator 1-5).\n'
                        ' * `union_final_5_default` has the same 5 cases plus a `default` case.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_final_one_default_2': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_final_5_default --data-folder data --data-file union_x1',
                 'sub-exe -S -t test -y Test::union_final_5 --data-folder data --data-file union_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_final_5_default and union_final_5',
        'description' : 'Verifies final unions where publisher has default case but subscriber does not:\n\n'
                        ' * Publisher uses `union_final_5_default` (final) from `unions`.\n'
                        ' * Subscriber uses `union_final_5` (final) from `unions`.\n'
                        ' * Publisher `union_final_5_default` has 5 cases plus `default`.\n'
                        ' * Subscriber `union_final_5` has only 5 explicit cases.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_appendable_one_common_1': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_appendable_a --data-folder data --data-file union_a',
                 'sub-exe -S -t test -y Test::union_appendable_b --data-folder data --data-file union_a'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between union_appendable_a and union_appendable_b',
        'description' : 'Verifies appendable unions with one common discriminator label:\n\n'
                        ' * Publisher uses `union_appendable_a` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_appendable_b` (appendable) from `unions`.\n'
                        ' * `union_appendable_a` has cases discriminator=1..5.\n'
                        ' * `union_appendable_b` has cases discriminator=10..15.\n'
                        ' * Only discriminator=3 maps to same member `x3`(`int64`) in both.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'union_appendable_one_common_2': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_appendable_b --data-folder data --data-file union_b',
                 'sub-exe -S -t test -y Test::union_appendable_a --data-folder data --data-file union_b'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between union_appendable_b and union_appendable_a',
        'description' : 'Verifies appendable unions with one common discriminator label (reverse direction):\n\n'
                        ' * Publisher uses `union_appendable_b` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_appendable_a` (appendable) from `unions`.\n'
                        ' * `union_appendable_b` has cases discriminator=10..15.\n'
                        ' * `union_appendable_a` has cases discriminator=1..5.\n'
                        ' * Only discriminator=3 maps to same member `x3`(`int64`) in both.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'union_appendable_no_common_1': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_appendable_a --data-folder data --data-file union_a',
                 'sub-exe -S -t test -y Test::union_appendable_c --data-folder data --data-file union_a'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_appendable_a and union_appendable_c',
        'description' : 'Verifies appendable unions with no common discriminator labels:\n\n'
                        ' * Publisher uses `union_appendable_a` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_appendable_c` (appendable) from `unions`.\n'
                        ' * `union_appendable_a` has cases discriminator=1..5.\n'
                        ' * `union_appendable_c` has cases discriminator=10..15.\n'
                        ' * No discriminator value is shared.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_appendable_no_common_2': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_appendable_c --data-folder data --data-file union_c',
                 'sub-exe -S -t test -y Test::union_appendable_a --data-folder data --data-file union_c'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_appendable_c and union_appendable_a',
        'description' : 'Verifies appendable unions with no common discriminator labels (reverse direction):\n\n'
                        ' * Publisher uses `union_appendable_c` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_appendable_a` (appendable) from `unions`.\n'
                        ' * `union_appendable_c` has cases discriminator=10..15.\n'
                        ' * `union_appendable_a` has cases discriminator=1..5.\n'
                        ' * No discriminator value is shared.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_appendable_no_common_w_default': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_appendable_a_default --data-folder data --data-file union_xd',
                 'sub-exe -S -t test -y Test::union_appendable_b_default --data-folder data --data-file union_xd'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_appendable_a_default and union_appendable_b_default',
        'description' : 'Verifies appendable unions with no common explicit discriminator labels are not assignable even when both have a default case:\n\n'
                        ' * Publisher uses `union_appendable_a_default` (appendable) from `unions`.\n'
                        ' * Subscriber uses `union_appendable_b_default` (appendable) from `unions`.\n'
                        ' * `union_appendable_a_default` has discriminator=5 + default.\n'
                        ' * `union_appendable_b_default` has discriminator=15 + default.\n'
                        ' * No explicit discriminator value is shared.\n'
                        ' * The default case alone does not satisfy the requirement of at least one member in common.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_mutable_one_common': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_mutable_a --data-folder data --data-file union_a',
                 'sub-exe -S -t test -y Test::union_mutable_b --data-folder data --data-file union_a'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between union_mutable_a and union_mutable_b',
        'description' : 'Verifies mutable unions with one common discriminator label:\n\n'
                        ' * Publisher uses `union_mutable_a` (mutable) from `unions`.\n'
                        ' * Subscriber uses `union_mutable_b` (mutable) from `unions`.\n'
                        ' * `union_mutable_a` has cases discriminator=1..5.\n'
                        ' * `union_mutable_b` has cases discriminator=3,10..15.\n'
                        ' * Only discriminator=3 maps to same member `x3`(`int64`) in both. Mutable extensibility requires at least one member in common for assignability.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'union_mutable_no_common': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_mutable_a --data-folder data --data-file union_a',
                 'sub-exe -S -t test -y Test::union_mutable_c --data-folder data --data-file union_a'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_mutable_a and union_mutable_c',
        'description' : 'Verifies mutable unions with no common discriminator labels are not assignable:\n\n'
                        ' * Publisher uses `union_mutable_a` (mutable) from `unions`.\n'
                        ' * Subscriber uses `union_mutable_c` (mutable) from `unions`.\n'
                        ' * `union_mutable_a` has cases discriminator=1..5.\n'
                        ' * `union_mutable_c` has cases discriminator=10..15.\n'
                        ' * No discriminator value is shared.\n'
                        ' * Mutable extensibility requires at least one member in common.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'union_mutable_no_common_w_default': {
        'common_args': ['--type-folder types --type-file unions'],
        'apps': ['pub-exe -P -t test -y Test::union_mutable_a_default --data-folder data --data-file union_xd',
                 'sub-exe -S -t test -y Test::union_mutable_b_default --data-folder data --data-file union_xd'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between union_mutable_a_default and union_mutable_b_default',
        'description' : 'Verifies mutable unions with no common explicit discriminator labels are not assignable even when both have a default case:\n\n'
                        ' * Publisher uses `union_mutable_a_default` (mutable) from `unions`.\n'
                        ' * Subscriber uses `union_mutable_b_default` (mutable) from `unions`.\n'
                        ' * `union_mutable_a_default` has discriminator=5 + default.\n'
                        ' * `union_mutable_b_default` has discriminator=15 + default.\n'
                        ' * No explicit discriminator value is shared.\n'
                        ' * The default case alone does not satisfy the mutable requirement of at least one member in common.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
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
        'title' : 'Communication between identical struct_primitive_uint8',
        'description' : 'Verifies communication between `struct_primitive_uint8` and `struct_primitive_uint8`:\n\n'
                        ' * Publisher and Subscriber use `struct_primitive_uint8` from `primitives`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_uint8_uint16' : {
        'common_args' : ['--type-folder types --type-file primitives'],
        'apps' : ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint8 and struct_primitive_uint16',
        'description' : 'Verifies structs with non-assignable member types are not assignable:\n\n'
                        ' * Publisher uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Both are final with one member `x1`, but publisher declares it as `byte` and subscriber as `uint16`. Members with matching IDs must have assignable types.\n'
                        ' * `byte` and `uint16` are not assignable.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint8_uint32' : {
        'common_args' : ['--type-folder types --type-file primitives'],
        'apps' : ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                  'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes' : [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function' : tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint8 and struct_primitive_uint32',
        'description' : 'Verifies no type assignability between `struct_primitive_uint8` and `struct_primitive_uint32`:\n\n'
                        ' * Publisher uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint8` and subscriber as `uint32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint8_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint8 and struct_primitive_uint64',
        'description' : 'Verifies no type assignability between `struct_primitive_uint8` and `struct_primitive_uint64`:\n\n'
                        ' * Publisher uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint8` and subscriber as `uint64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint8_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint8 and struct_primitive_int8',
        'description' : 'Verifies no type assignability between `struct_primitive_uint8` and `struct_primitive_int8`:\n\n'
                        ' * Publisher uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint8` and subscriber as `int8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint8_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint8 and struct_primitive_int16',
        'description' : 'Verifies no type assignability between `struct_primitive_uint8` and `struct_primitive_int16`:\n\n'
                        ' * Publisher uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint8` and subscriber as `int16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint8_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint8 and struct_primitive_int32',
        'description' : 'Verifies no type assignability between `struct_primitive_uint8` and `struct_primitive_int32`:\n\n'
                        ' * Publisher uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint8` and subscriber as `int32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint8_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint8 and struct_primitive_int64',
        'description' : 'Verifies no type assignability between `struct_primitive_uint8` and `struct_primitive_int64`:\n\n'
                        ' * Publisher uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint8` and subscriber as `int64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint8_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint8 and struct_primitive_float32',
        'description' : 'Verifies no type assignability between `struct_primitive_uint8` and `struct_primitive_float32`:\n\n'
                        ' * Publisher uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint8` and subscriber as `float32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint8_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint8 and struct_primitive_float64',
        'description' : 'Verifies no type assignability between `struct_primitive_uint8` and `struct_primitive_float64`:\n\n'
                        ' * Publisher uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint8` and subscriber as `float64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint8_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint8 and struct_primitive_float128',
        'description' : 'Verifies no type assignability between `struct_primitive_uint8` and `struct_primitive_float128`:\n\n'
                        ' * Publisher uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint8` and subscriber as `float128`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint8_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint8 and struct_primitive_byte',
        'description' : 'Verifies no type assignability between `struct_primitive_uint8` and `struct_primitive_byte`:\n\n'
                        ' * Publisher uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint8` and subscriber as `byte`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint8_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint8 and struct_primitive_char8',
        'description' : 'Verifies no type assignability between `struct_primitive_uint8` and `struct_primitive_char8`:\n\n'
                        ' * Publisher uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint8` and subscriber as `char8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },

    ####### Test uint16 #######

    'struct_uint16_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint16 and struct_primitive_uint8',
        'description' : 'Verifies no type assignability between `struct_primitive_uint16` and `struct_primitive_uint8`:\n\n'
                        ' * Publisher uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint16` and subscriber as `uint8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint16_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical struct_primitive_uint16',
        'description' : 'Verifies communication between `struct_primitive_uint16` and `struct_primitive_uint16`:\n\n'
                        ' * Publisher and Subscriber use `struct_primitive_uint16` from `primitives`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_uint16_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint16 and struct_primitive_uint32',
        'description' : 'Verifies no type assignability between `struct_primitive_uint16` and `struct_primitive_uint32`:\n\n'
                        ' * Publisher uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint16` and subscriber as `uint32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint16_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint16 and struct_primitive_uint64',
        'description' : 'Verifies no type assignability between `struct_primitive_uint16` and `struct_primitive_uint64`:\n\n'
                        ' * Publisher uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint16` and subscriber as `uint64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint16_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint16 and struct_primitive_int8',
        'description' : 'Verifies no type assignability between `struct_primitive_uint16` and `struct_primitive_int8`:\n\n'
                        ' * Publisher uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint16` and subscriber as `int8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint16_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint16 and struct_primitive_int16',
        'description' : 'Verifies no type assignability between `struct_primitive_uint16` and `struct_primitive_int16`:\n\n'
                        ' * Publisher uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint16` and subscriber as `int16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint16_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint16 and struct_primitive_int32',
        'description' : 'Verifies no type assignability between `struct_primitive_uint16` and `struct_primitive_int32`:\n\n'
                        ' * Publisher uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint16` and subscriber as `int32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint16_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint16 and struct_primitive_int64',
        'description' : 'Verifies no type assignability between `struct_primitive_uint16` and `struct_primitive_int64`:\n\n'
                        ' * Publisher uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint16` and subscriber as `int64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint16_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint16 and struct_primitive_float32',
        'description' : 'Verifies no type assignability between `struct_primitive_uint16` and `struct_primitive_float32`:\n\n'
                        ' * Publisher uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint16` and subscriber as `float32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint16_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint16 and struct_primitive_float64',
        'description' : 'Verifies no type assignability between `struct_primitive_uint16` and `struct_primitive_float64`:\n\n'
                        ' * Publisher uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint16` and subscriber as `float64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint16_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint16 and struct_primitive_float128',
        'description' : 'Verifies no type assignability between `struct_primitive_uint16` and `struct_primitive_float128`:\n\n'
                        ' * Publisher uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint16` and subscriber as `float128`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint16_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint16 and struct_primitive_byte',
        'description' : 'Verifies no type assignability between `struct_primitive_uint16` and `struct_primitive_byte`:\n\n'
                        ' * Publisher uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint16` and subscriber as `byte`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint16_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint16 and struct_primitive_char8',
        'description' : 'Verifies no type assignability between `struct_primitive_uint16` and `struct_primitive_char8`:\n\n'
                        ' * Publisher uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint16` and subscriber as `char8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },

    ####### Test uint32 #######

    'struct_uint32_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint32 and struct_primitive_uint8',
        'description' : 'Verifies no type assignability between `struct_primitive_uint32` and `struct_primitive_uint8`:\n\n'
                        ' * Publisher uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint32` and subscriber as `uint8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint32_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint32 and struct_primitive_uint16',
        'description' : 'Verifies no type assignability between `struct_primitive_uint32` and `struct_primitive_uint16`:\n\n'
                        ' * Publisher uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint32` and subscriber as `uint16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint32_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical struct_primitive_uint32',
        'description' : 'Verifies communication between `struct_primitive_uint32` and `struct_primitive_uint32`:\n\n'
                        ' * Publisher and Subscriber use `struct_primitive_uint32` from `primitives`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_uint32_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint32 and struct_primitive_uint64',
        'description' : 'Verifies no type assignability between `struct_primitive_uint32` and `struct_primitive_uint64`:\n\n'
                        ' * Publisher uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint32` and subscriber as `uint64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint32_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint32 and struct_primitive_int8',
        'description' : 'Verifies no type assignability between `struct_primitive_uint32` and `struct_primitive_int8`:\n\n'
                        ' * Publisher uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint32` and subscriber as `int8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint32_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint32 and struct_primitive_int16',
        'description' : 'Verifies no type assignability between `struct_primitive_uint32` and `struct_primitive_int16`:\n\n'
                        ' * Publisher uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint32` and subscriber as `int16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint32_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint32 and struct_primitive_int32',
        'description' : 'Verifies no type assignability between `struct_primitive_uint32` and `struct_primitive_int32`:\n\n'
                        ' * Publisher uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint32` and subscriber as `int32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint32_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint32 and struct_primitive_int64',
        'description' : 'Verifies no type assignability between `struct_primitive_uint32` and `struct_primitive_int64`:\n\n'
                        ' * Publisher uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint32` and subscriber as `int64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint32_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint32 and struct_primitive_float32',
        'description' : 'Verifies no type assignability between `struct_primitive_uint32` and `struct_primitive_float32`:\n\n'
                        ' * Publisher uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint32` and subscriber as `float32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint32_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint32 and struct_primitive_float64',
        'description' : 'Verifies no type assignability between `struct_primitive_uint32` and `struct_primitive_float64`:\n\n'
                        ' * Publisher uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint32` and subscriber as `float64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint32_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint32 and struct_primitive_float128',
        'description' : 'Verifies no type assignability between `struct_primitive_uint32` and `struct_primitive_float128`:\n\n'
                        ' * Publisher uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint32` and subscriber as `float128`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint32_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint32 and struct_primitive_byte',
        'description' : 'Verifies no type assignability between `struct_primitive_uint32` and `struct_primitive_byte`:\n\n'
                        ' * Publisher uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint32` and subscriber as `byte`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint32_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint32 and struct_primitive_char8',
        'description' : 'Verifies no type assignability between `struct_primitive_uint32` and `struct_primitive_char8`:\n\n'
                        ' * Publisher uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint32` and subscriber as `char8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },

    ####### Test uint64 #######

    'struct_uint64_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint64 and struct_primitive_uint8',
        'description' : 'Verifies no type assignability between `struct_primitive_uint64` and `struct_primitive_uint8`:\n\n'
                        ' * Publisher uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint64` and subscriber as `uint8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint64_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint64 and struct_primitive_uint16',
        'description' : 'Verifies no type assignability between `struct_primitive_uint64` and `struct_primitive_uint16`:\n\n'
                        ' * Publisher uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint64` and subscriber as `uint16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint64_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint64 and struct_primitive_uint32',
        'description' : 'Verifies no type assignability between `struct_primitive_uint64` and `struct_primitive_uint32`:\n\n'
                        ' * Publisher uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint64` and subscriber as `uint32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint64_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical struct_primitive_uint64',
        'description' : 'Verifies communication between `struct_primitive_uint64` and `struct_primitive_uint64`:\n\n'
                        ' * Publisher and Subscriber use `struct_primitive_uint64` from `primitives`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_uint64_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint64 and struct_primitive_int8',
        'description' : 'Verifies no type assignability between `struct_primitive_uint64` and `struct_primitive_int8`:\n\n'
                        ' * Publisher uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint64` and subscriber as `int8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint64_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint64 and struct_primitive_int16',
        'description' : 'Verifies no type assignability between `struct_primitive_uint64` and `struct_primitive_int16`:\n\n'
                        ' * Publisher uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint64` and subscriber as `int16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint64_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint64 and struct_primitive_int32',
        'description' : 'Verifies no type assignability between `struct_primitive_uint64` and `struct_primitive_int32`:\n\n'
                        ' * Publisher uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint64` and subscriber as `int32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint64_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint64 and struct_primitive_int64',
        'description' : 'Verifies no type assignability between `struct_primitive_uint64` and `struct_primitive_int64`:\n\n'
                        ' * Publisher uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint64` and subscriber as `int64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint64_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint64 and struct_primitive_float32',
        'description' : 'Verifies no type assignability between `struct_primitive_uint64` and `struct_primitive_float32`:\n\n'
                        ' * Publisher uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint64` and subscriber as `float32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint64_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint64 and struct_primitive_float64',
        'description' : 'Verifies no type assignability between `struct_primitive_uint64` and `struct_primitive_float64`:\n\n'
                        ' * Publisher uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint64` and subscriber as `float64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint64_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint64 and struct_primitive_float128',
        'description' : 'Verifies no type assignability between `struct_primitive_uint64` and `struct_primitive_float128`:\n\n'
                        ' * Publisher uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint64` and subscriber as `float128`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint64_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint64 and struct_primitive_byte',
        'description' : 'Verifies no type assignability between `struct_primitive_uint64` and `struct_primitive_byte`:\n\n'
                        ' * Publisher uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint64` and subscriber as `byte`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_uint64_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_uint64 and struct_primitive_char8',
        'description' : 'Verifies no type assignability between `struct_primitive_uint64` and `struct_primitive_char8`:\n\n'
                        ' * Publisher uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `uint64` and subscriber as `char8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },

    ####### Test int8 #######

    'struct_int8_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int8 and struct_primitive_uint8',
        'description' : 'Verifies no type assignability between `struct_primitive_int8` and `struct_primitive_uint8`:\n\n'
                        ' * Publisher uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int8` and subscriber as `uint8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int8_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int8 and struct_primitive_uint16',
        'description' : 'Verifies no type assignability between `struct_primitive_int8` and `struct_primitive_uint16`:\n\n'
                        ' * Publisher uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int8` and subscriber as `uint16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int8_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int8 and struct_primitive_uint32',
        'description' : 'Verifies no type assignability between `struct_primitive_int8` and `struct_primitive_uint32`:\n\n'
                        ' * Publisher uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int8` and subscriber as `uint32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int8_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int8 and struct_primitive_uint64',
        'description' : 'Verifies no type assignability between `struct_primitive_int8` and `struct_primitive_uint64`:\n\n'
                        ' * Publisher uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int8` and subscriber as `uint64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int8_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical struct_primitive_int8',
        'description' : 'Verifies communication between `struct_primitive_int8` and `struct_primitive_int8`:\n\n'
                        ' * Publisher and Subscriber use `struct_primitive_int8` from `primitives`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_int8_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int8 and struct_primitive_int16',
        'description' : 'Verifies no type assignability between `struct_primitive_int8` and `struct_primitive_int16`:\n\n'
                        ' * Publisher uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int8` and subscriber as `int16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int8_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int8 and struct_primitive_int32',
        'description' : 'Verifies no type assignability between `struct_primitive_int8` and `struct_primitive_int32`:\n\n'
                        ' * Publisher uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int8` and subscriber as `int32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int8_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int8 and struct_primitive_int64',
        'description' : 'Verifies no type assignability between `struct_primitive_int8` and `struct_primitive_int64`:\n\n'
                        ' * Publisher uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int8` and subscriber as `int64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int8_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int8 and struct_primitive_float32',
        'description' : 'Verifies no type assignability between `struct_primitive_int8` and `struct_primitive_float32`:\n\n'
                        ' * Publisher uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int8` and subscriber as `float32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int8_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int8 and struct_primitive_float64',
        'description' : 'Verifies no type assignability between `struct_primitive_int8` and `struct_primitive_float64`:\n\n'
                        ' * Publisher uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int8` and subscriber as `float64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int8_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int8 and struct_primitive_float128',
        'description' : 'Verifies no type assignability between `struct_primitive_int8` and `struct_primitive_float128`:\n\n'
                        ' * Publisher uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int8` and subscriber as `float128`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int8_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int8 and struct_primitive_byte',
        'description' : 'Verifies no type assignability between `struct_primitive_int8` and `struct_primitive_byte`:\n\n'
                        ' * Publisher uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int8` and subscriber as `byte`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int8_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int8 and struct_primitive_char8',
        'description' : 'Verifies no type assignability between `struct_primitive_int8` and `struct_primitive_char8`:\n\n'
                        ' * Publisher uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int8` and subscriber as `char8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },

    ####### Test int16 #######

    'struct_int16_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int16 and struct_primitive_uint8',
        'description' : 'Verifies no type assignability between `struct_primitive_int16` and `struct_primitive_uint8`:\n\n'
                        ' * Publisher uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int16` and subscriber as `uint8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int16_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int16 and struct_primitive_uint16',
        'description' : 'Verifies no type assignability between `struct_primitive_int16` and `struct_primitive_uint16`:\n\n'
                        ' * Publisher uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int16` and subscriber as `uint16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int16_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int16 and struct_primitive_uint32',
        'description' : 'Verifies no type assignability between `struct_primitive_int16` and `struct_primitive_uint32`:\n\n'
                        ' * Publisher uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int16` and subscriber as `uint32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int16_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int16 and struct_primitive_uint64',
        'description' : 'Verifies no type assignability between `struct_primitive_int16` and `struct_primitive_uint64`:\n\n'
                        ' * Publisher uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int16` and subscriber as `uint64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int16_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int16 and struct_primitive_int8',
        'description' : 'Verifies no type assignability between `struct_primitive_int16` and `struct_primitive_int8`:\n\n'
                        ' * Publisher uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int16` and subscriber as `int8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int16_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical struct_primitive_int16',
        'description' : 'Verifies communication between `struct_primitive_int16` and `struct_primitive_int16`:\n\n'
                        ' * Publisher and Subscriber use `struct_primitive_int16` from `primitives`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_int16_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int16 and struct_primitive_int32',
        'description' : 'Verifies no type assignability between `struct_primitive_int16` and `struct_primitive_int32`:\n\n'
                        ' * Publisher uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int16` and subscriber as `int32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int16_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int16 and struct_primitive_int64',
        'description' : 'Verifies no type assignability between `struct_primitive_int16` and `struct_primitive_int64`:\n\n'
                        ' * Publisher uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int16` and subscriber as `int64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int16_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int16 and struct_primitive_float32',
        'description' : 'Verifies no type assignability between `struct_primitive_int16` and `struct_primitive_float32`:\n\n'
                        ' * Publisher uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int16` and subscriber as `float32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int16_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int16 and struct_primitive_float64',
        'description' : 'Verifies no type assignability between `struct_primitive_int16` and `struct_primitive_float64`:\n\n'
                        ' * Publisher uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int16` and subscriber as `float64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int16_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int16 and struct_primitive_float128',
        'description' : 'Verifies no type assignability between `struct_primitive_int16` and `struct_primitive_float128`:\n\n'
                        ' * Publisher uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int16` and subscriber as `float128`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int16_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int16 and struct_primitive_byte',
        'description' : 'Verifies no type assignability between `struct_primitive_int16` and `struct_primitive_byte`:\n\n'
                        ' * Publisher uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int16` and subscriber as `byte`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int16_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int16 and struct_primitive_char8',
        'description' : 'Verifies no type assignability between `struct_primitive_int16` and `struct_primitive_char8`:\n\n'
                        ' * Publisher uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int16` and subscriber as `char8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },

    ####### Test int32 #######

    'struct_int32_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int32 and struct_primitive_uint8',
        'description' : 'Verifies no type assignability between `struct_primitive_int32` and `struct_primitive_uint8`:\n\n'
                        ' * Publisher uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int32` and subscriber as `uint8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int32_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int32 and struct_primitive_uint16',
        'description' : 'Verifies no type assignability between `struct_primitive_int32` and `struct_primitive_uint16`:\n\n'
                        ' * Publisher uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int32` and subscriber as `uint16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int32_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int32 and struct_primitive_uint32',
        'description' : 'Verifies no type assignability between `struct_primitive_int32` and `struct_primitive_uint32`:\n\n'
                        ' * Publisher uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int32` and subscriber as `uint32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int32_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int32 and struct_primitive_uint64',
        'description' : 'Verifies no type assignability between `struct_primitive_int32` and `struct_primitive_uint64`:\n\n'
                        ' * Publisher uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int32` and subscriber as `uint64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int32_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int32 and struct_primitive_int8',
        'description' : 'Verifies no type assignability between `struct_primitive_int32` and `struct_primitive_int8`:\n\n'
                        ' * Publisher uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int32` and subscriber as `int8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int32_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int32 and struct_primitive_int16',
        'description' : 'Verifies no type assignability between `struct_primitive_int32` and `struct_primitive_int16`:\n\n'
                        ' * Publisher uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int32` and subscriber as `int16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int32_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical struct_primitive_int32',
        'description' : 'Verifies communication between `struct_primitive_int32` and `struct_primitive_int32`:\n\n'
                        ' * Publisher and Subscriber use `struct_primitive_int32` from `primitives`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_int32_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int32 and struct_primitive_int64',
        'description' : 'Verifies no type assignability between `struct_primitive_int32` and `struct_primitive_int64`:\n\n'
                        ' * Publisher uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int32` and subscriber as `int64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int32_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int32 and struct_primitive_float32',
        'description' : 'Verifies no type assignability between `struct_primitive_int32` and `struct_primitive_float32`:\n\n'
                        ' * Publisher uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int32` and subscriber as `float32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int32_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int32 and struct_primitive_float64',
        'description' : 'Verifies no type assignability between `struct_primitive_int32` and `struct_primitive_float64`:\n\n'
                        ' * Publisher uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int32` and subscriber as `float64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int32_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int32 and struct_primitive_float128',
        'description' : 'Verifies no type assignability between `struct_primitive_int32` and `struct_primitive_float128`:\n\n'
                        ' * Publisher uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int32` and subscriber as `float128`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int32_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int32 and struct_primitive_byte',
        'description' : 'Verifies no type assignability between `struct_primitive_int32` and `struct_primitive_byte`:\n\n'
                        ' * Publisher uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int32` and subscriber as `byte`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int32_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int32 and struct_primitive_char8',
        'description' : 'Verifies no type assignability between `struct_primitive_int32` and `struct_primitive_char8`:\n\n'
                        ' * Publisher uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int32` and subscriber as `char8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },

    ####### Test int64 #######

    'struct_int64_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int64 and struct_primitive_uint8',
        'description' : 'Verifies no type assignability between `struct_primitive_int64` and `struct_primitive_uint8`:\n\n'
                        ' * Publisher uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int64` and subscriber as `uint8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int64_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int64 and struct_primitive_uint16',
        'description' : 'Verifies no type assignability between `struct_primitive_int64` and `struct_primitive_uint16`:\n\n'
                        ' * Publisher uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int64` and subscriber as `uint16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int64_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int64 and struct_primitive_uint32',
        'description' : 'Verifies no type assignability between `struct_primitive_int64` and `struct_primitive_uint32`:\n\n'
                        ' * Publisher uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int64` and subscriber as `uint32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int64_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int64 and struct_primitive_uint64',
        'description' : 'Verifies no type assignability between `struct_primitive_int64` and `struct_primitive_uint64`:\n\n'
                        ' * Publisher uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int64` and subscriber as `uint64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int64_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int64 and struct_primitive_int8',
        'description' : 'Verifies no type assignability between `struct_primitive_int64` and `struct_primitive_int8`:\n\n'
                        ' * Publisher uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int64` and subscriber as `int8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int64_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int64 and struct_primitive_int16',
        'description' : 'Verifies no type assignability between `struct_primitive_int64` and `struct_primitive_int16`:\n\n'
                        ' * Publisher uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int64` and subscriber as `int16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int64_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int64 and struct_primitive_int32',
        'description' : 'Verifies no type assignability between `struct_primitive_int64` and `struct_primitive_int32`:\n\n'
                        ' * Publisher uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int64` and subscriber as `int32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int64_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical struct_primitive_int64',
        'description' : 'Verifies communication between `struct_primitive_int64` and `struct_primitive_int64`:\n\n'
                        ' * Publisher and Subscriber use `struct_primitive_int64` from `primitives`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_int64_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int64 and struct_primitive_float32',
        'description' : 'Verifies no type assignability between `struct_primitive_int64` and `struct_primitive_float32`:\n\n'
                        ' * Publisher uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int64` and subscriber as `float32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int64_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int64 and struct_primitive_float64',
        'description' : 'Verifies no type assignability between `struct_primitive_int64` and `struct_primitive_float64`:\n\n'
                        ' * Publisher uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int64` and subscriber as `float64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int64_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int64 and struct_primitive_float128',
        'description' : 'Verifies no type assignability between `struct_primitive_int64` and `struct_primitive_float128`:\n\n'
                        ' * Publisher uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int64` and subscriber as `float128`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int64_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int64 and struct_primitive_byte',
        'description' : 'Verifies no type assignability between `struct_primitive_int64` and `struct_primitive_byte`:\n\n'
                        ' * Publisher uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int64` and subscriber as `byte`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_int64_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_int64 and struct_primitive_char8',
        'description' : 'Verifies no type assignability between `struct_primitive_int64` and `struct_primitive_char8`:\n\n'
                        ' * Publisher uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `int64` and subscriber as `char8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },

    ####### Test float32 #######

    'struct_float32_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float32 and struct_primitive_uint8',
        'description' : 'Verifies no type assignability between `struct_primitive_float32` and `struct_primitive_uint8`:\n\n'
                        ' * Publisher uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float32` and subscriber as `uint8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float32_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float32 and struct_primitive_uint16',
        'description' : 'Verifies no type assignability between `struct_primitive_float32` and `struct_primitive_uint16`:\n\n'
                        ' * Publisher uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float32` and subscriber as `uint16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float32_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float32 and struct_primitive_uint32',
        'description' : 'Verifies no type assignability between `struct_primitive_float32` and `struct_primitive_uint32`:\n\n'
                        ' * Publisher uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float32` and subscriber as `uint32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float32_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float32 and struct_primitive_uint64',
        'description' : 'Verifies no type assignability between `struct_primitive_float32` and `struct_primitive_uint64`:\n\n'
                        ' * Publisher uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float32` and subscriber as `uint64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float32_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float32 and struct_primitive_int8',
        'description' : 'Verifies no type assignability between `struct_primitive_float32` and `struct_primitive_int8`:\n\n'
                        ' * Publisher uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float32` and subscriber as `int8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float32_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float32 and struct_primitive_int16',
        'description' : 'Verifies no type assignability between `struct_primitive_float32` and `struct_primitive_int16`:\n\n'
                        ' * Publisher uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float32` and subscriber as `int16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float32_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float32 and struct_primitive_int32',
        'description' : 'Verifies no type assignability between `struct_primitive_float32` and `struct_primitive_int32`:\n\n'
                        ' * Publisher uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float32` and subscriber as `int32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float32_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float32 and struct_primitive_int64',
        'description' : 'Verifies no type assignability between `struct_primitive_float32` and `struct_primitive_int64`:\n\n'
                        ' * Publisher uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float32` and subscriber as `int64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float32_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical struct_primitive_float32',
        'description' : 'Verifies communication between `struct_primitive_float32` and `struct_primitive_float32`:\n\n'
                        ' * Publisher and Subscriber use `struct_primitive_float32` from `primitives`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_float32_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float32 and struct_primitive_float64',
        'description' : 'Verifies no type assignability between `struct_primitive_float32` and `struct_primitive_float64`:\n\n'
                        ' * Publisher uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float32` and subscriber as `float64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float32_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float32 and struct_primitive_float128',
        'description' : 'Verifies no type assignability between `struct_primitive_float32` and `struct_primitive_float128`:\n\n'
                        ' * Publisher uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float32` and subscriber as `float128`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float32_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float32 and struct_primitive_byte',
        'description' : 'Verifies no type assignability between `struct_primitive_float32` and `struct_primitive_byte`:\n\n'
                        ' * Publisher uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float32` and subscriber as `byte`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float32_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float32 and struct_primitive_char8',
        'description' : 'Verifies no type assignability between `struct_primitive_float32` and `struct_primitive_char8`:\n\n'
                        ' * Publisher uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float32` and subscriber as `char8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },

    ####### Test float64 #######

    'struct_float64_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float64 and struct_primitive_uint8',
        'description' : 'Verifies no type assignability between `struct_primitive_float64` and `struct_primitive_uint8`:\n\n'
                        ' * Publisher uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float64` and subscriber as `uint8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float64_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float64 and struct_primitive_uint16',
        'description' : 'Verifies no type assignability between `struct_primitive_float64` and `struct_primitive_uint16`:\n\n'
                        ' * Publisher uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float64` and subscriber as `uint16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float64_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float64 and struct_primitive_uint32',
        'description' : 'Verifies no type assignability between `struct_primitive_float64` and `struct_primitive_uint32`:\n\n'
                        ' * Publisher uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float64` and subscriber as `uint32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float64_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float64 and struct_primitive_uint64',
        'description' : 'Verifies no type assignability between `struct_primitive_float64` and `struct_primitive_uint64`:\n\n'
                        ' * Publisher uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float64` and subscriber as `uint64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float64_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float64 and struct_primitive_int8',
        'description' : 'Verifies no type assignability between `struct_primitive_float64` and `struct_primitive_int8`:\n\n'
                        ' * Publisher uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float64` and subscriber as `int8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float64_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float64 and struct_primitive_int16',
        'description' : 'Verifies no type assignability between `struct_primitive_float64` and `struct_primitive_int16`:\n\n'
                        ' * Publisher uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float64` and subscriber as `int16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float64_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float64 and struct_primitive_int32',
        'description' : 'Verifies no type assignability between `struct_primitive_float64` and `struct_primitive_int32`:\n\n'
                        ' * Publisher uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float64` and subscriber as `int32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float64_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float64 and struct_primitive_int64',
        'description' : 'Verifies no type assignability between `struct_primitive_float64` and `struct_primitive_int64`:\n\n'
                        ' * Publisher uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float64` and subscriber as `int64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float64_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float64 and struct_primitive_float32',
        'description' : 'Verifies no type assignability between `struct_primitive_float64` and `struct_primitive_float32`:\n\n'
                        ' * Publisher uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float64` and subscriber as `float32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float64_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical struct_primitive_float64',
        'description' : 'Verifies communication between `struct_primitive_float64` and `struct_primitive_float64`:\n\n'
                        ' * Publisher and Subscriber use `struct_primitive_float64` from `primitives`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_float64_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float64 and struct_primitive_float128',
        'description' : 'Verifies no type assignability between `struct_primitive_float64` and `struct_primitive_float128`:\n\n'
                        ' * Publisher uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float64` and subscriber as `float128`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float64_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float64 and struct_primitive_byte',
        'description' : 'Verifies no type assignability between `struct_primitive_float64` and `struct_primitive_byte`:\n\n'
                        ' * Publisher uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float64` and subscriber as `byte`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float64_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float64 and struct_primitive_char8',
        'description' : 'Verifies no type assignability between `struct_primitive_float64` and `struct_primitive_char8`:\n\n'
                        ' * Publisher uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float64` and subscriber as `char8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },

    ####### Test float128 #######

    'struct_float128_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float128 and struct_primitive_uint8',
        'description' : 'Verifies no type assignability between `struct_primitive_float128` and `struct_primitive_uint8`:\n\n'
                        ' * Publisher uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float128` and subscriber as `uint8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float128_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float128 and struct_primitive_uint16',
        'description' : 'Verifies no type assignability between `struct_primitive_float128` and `struct_primitive_uint16`:\n\n'
                        ' * Publisher uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float128` and subscriber as `uint16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float128_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float128 and struct_primitive_uint32',
        'description' : 'Verifies no type assignability between `struct_primitive_float128` and `struct_primitive_uint32`:\n\n'
                        ' * Publisher uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float128` and subscriber as `uint32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float128_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float128 and struct_primitive_uint64',
        'description' : 'Verifies no type assignability between `struct_primitive_float128` and `struct_primitive_uint64`:\n\n'
                        ' * Publisher uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float128` and subscriber as `uint64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float128_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float128 and struct_primitive_int8',
        'description' : 'Verifies no type assignability between `struct_primitive_float128` and `struct_primitive_int8`:\n\n'
                        ' * Publisher uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float128` and subscriber as `int8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float128_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float128 and struct_primitive_int16',
        'description' : 'Verifies no type assignability between `struct_primitive_float128` and `struct_primitive_int16`:\n\n'
                        ' * Publisher uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float128` and subscriber as `int16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float128_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float128 and struct_primitive_int32',
        'description' : 'Verifies no type assignability between `struct_primitive_float128` and `struct_primitive_int32`:\n\n'
                        ' * Publisher uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float128` and subscriber as `int32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float128_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float128 and struct_primitive_int64',
        'description' : 'Verifies no type assignability between `struct_primitive_float128` and `struct_primitive_int64`:\n\n'
                        ' * Publisher uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float128` and subscriber as `int64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float128_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float128 and struct_primitive_float32',
        'description' : 'Verifies no type assignability between `struct_primitive_float128` and `struct_primitive_float32`:\n\n'
                        ' * Publisher uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float128` and subscriber as `float32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float128_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float128 and struct_primitive_float64',
        'description' : 'Verifies no type assignability between `struct_primitive_float128` and `struct_primitive_float64`:\n\n'
                        ' * Publisher uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float128` and subscriber as `float64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float128_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical struct_primitive_float128',
        'description' : 'Verifies communication between `struct_primitive_float128` and `struct_primitive_float128`:\n\n'
                        ' * Publisher and Subscriber use `struct_primitive_float128` from `primitives`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_float128_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float128 and struct_primitive_byte',
        'description' : 'Verifies no type assignability between `struct_primitive_float128` and `struct_primitive_byte`:\n\n'
                        ' * Publisher uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float128` and subscriber as `byte`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_float128_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_float128 and struct_primitive_char8',
        'description' : 'Verifies no type assignability between `struct_primitive_float128` and `struct_primitive_char8`:\n\n'
                        ' * Publisher uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `float128` and subscriber as `char8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },

    ####### Test byte #######

    'struct_byte_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_byte and struct_primitive_uint8',
        'description' : 'Verifies no type assignability between `struct_primitive_byte` and `struct_primitive_uint8`:\n\n'
                        ' * Publisher uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `byte` and subscriber as `uint8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_byte_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_byte and struct_primitive_uint16',
        'description' : 'Verifies no type assignability between `struct_primitive_byte` and `struct_primitive_uint16`:\n\n'
                        ' * Publisher uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `byte` and subscriber as `uint16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_byte_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_byte and struct_primitive_uint32',
        'description' : 'Verifies no type assignability between `struct_primitive_byte` and `struct_primitive_uint32`:\n\n'
                        ' * Publisher uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `byte` and subscriber as `uint32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_byte_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_byte and struct_primitive_uint64',
        'description' : 'Verifies no type assignability between `struct_primitive_byte` and `struct_primitive_uint64`:\n\n'
                        ' * Publisher uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `byte` and subscriber as `uint64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_byte_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_byte and struct_primitive_int8',
        'description' : 'Verifies no type assignability between `struct_primitive_byte` and `struct_primitive_int8`:\n\n'
                        ' * Publisher uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `byte` and subscriber as `int8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_byte_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_byte and struct_primitive_int16',
        'description' : 'Verifies no type assignability between `struct_primitive_byte` and `struct_primitive_int16`:\n\n'
                        ' * Publisher uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `byte` and subscriber as `int16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_byte_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_byte and struct_primitive_int32',
        'description' : 'Verifies no type assignability between `struct_primitive_byte` and `struct_primitive_int32`:\n\n'
                        ' * Publisher uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `byte` and subscriber as `int32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_byte_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_byte and struct_primitive_int64',
        'description' : 'Verifies no type assignability between `struct_primitive_byte` and `struct_primitive_int64`:\n\n'
                        ' * Publisher uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `byte` and subscriber as `int64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_byte_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_byte and struct_primitive_float32',
        'description' : 'Verifies no type assignability between `struct_primitive_byte` and `struct_primitive_float32`:\n\n'
                        ' * Publisher uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `byte` and subscriber as `float32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_byte_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_byte and struct_primitive_float64',
        'description' : 'Verifies no type assignability between `struct_primitive_byte` and `struct_primitive_float64`:\n\n'
                        ' * Publisher uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `byte` and subscriber as `float64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_byte_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_byte and struct_primitive_float128',
        'description' : 'Verifies no type assignability between `struct_primitive_byte` and `struct_primitive_float128`:\n\n'
                        ' * Publisher uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `byte` and subscriber as `float128`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_byte_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical struct_primitive_byte',
        'description' : 'Verifies communication between `struct_primitive_byte` and `struct_primitive_byte`:\n\n'
                        ' * Publisher and Subscriber use `struct_primitive_byte` from `primitives`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'struct_byte_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_byte and struct_primitive_char8',
        'description' : 'Verifies no type assignability between `struct_primitive_byte` and `struct_primitive_char8`:\n\n'
                        ' * Publisher uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `byte` and subscriber as `char8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },

    ####### Test char8 #######

    'struct_char8_uint8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_char8 and struct_primitive_uint8',
        'description' : 'Verifies no type assignability between `struct_primitive_char8` and `struct_primitive_uint8`:\n\n'
                        ' * Publisher uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `char8` and subscriber as `uint8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_char8_uint16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_char8 and struct_primitive_uint16',
        'description' : 'Verifies no type assignability between `struct_primitive_char8` and `struct_primitive_uint16`:\n\n'
                        ' * Publisher uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `char8` and subscriber as `uint16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_char8_uint32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_char8 and struct_primitive_uint32',
        'description' : 'Verifies no type assignability between `struct_primitive_char8` and `struct_primitive_uint32`:\n\n'
                        ' * Publisher uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `char8` and subscriber as `uint32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_char8_uint64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_uint64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_char8 and struct_primitive_uint64',
        'description' : 'Verifies no type assignability between `struct_primitive_char8` and `struct_primitive_uint64`:\n\n'
                        ' * Publisher uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_uint64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `char8` and subscriber as `uint64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_char8_int8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int8 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_char8 and struct_primitive_int8',
        'description' : 'Verifies no type assignability between `struct_primitive_char8` and `struct_primitive_int8`:\n\n'
                        ' * Publisher uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int8` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `char8` and subscriber as `int8`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_char8_int16': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int16 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_char8 and struct_primitive_int16',
        'description' : 'Verifies no type assignability between `struct_primitive_char8` and `struct_primitive_int16`:\n\n'
                        ' * Publisher uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int16` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `char8` and subscriber as `int16`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_char8_int32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_char8 and struct_primitive_int32',
        'description' : 'Verifies no type assignability between `struct_primitive_char8` and `struct_primitive_int32`:\n\n'
                        ' * Publisher uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `char8` and subscriber as `int32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_char8_int64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_int64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_char8 and struct_primitive_int64',
        'description' : 'Verifies no type assignability between `struct_primitive_char8` and `struct_primitive_int64`:\n\n'
                        ' * Publisher uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_int64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `char8` and subscriber as `int64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_char8_float32': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float32 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_char8 and struct_primitive_float32',
        'description' : 'Verifies no type assignability between `struct_primitive_char8` and `struct_primitive_float32`:\n\n'
                        ' * Publisher uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float32` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `char8` and subscriber as `float32`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_char8_float64': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float64 --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_char8 and struct_primitive_float64',
        'description' : 'Verifies no type assignability between `struct_primitive_char8` and `struct_primitive_float64`:\n\n'
                        ' * Publisher uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float64` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `char8` and subscriber as `float64`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_char8_float128': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_float128 --data-folder data --data-file struct_float128_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_char8 and struct_primitive_float128',
        'description' : 'Verifies no type assignability between `struct_primitive_char8` and `struct_primitive_float128`:\n\n'
                        ' * Publisher uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_float128` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `char8` and subscriber as `float128`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_char8_byte': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_byte --data-folder data --data-file struct_num_x1'],
        'expected_codes': [ReturnCode.INCONSISTENT_TOPIC, ReturnCode.INCONSISTENT_TOPIC],
        'check_function': tsf.data_is_correct,
        'title' : 'No type assignability between struct_primitive_char8 and struct_primitive_byte',
        'description' : 'Verifies no type assignability between `struct_primitive_char8` and `struct_primitive_byte`:\n\n'
                        ' * Publisher uses `struct_primitive_char8` from `primitives`.\n'
                        ' * Subscriber uses `struct_primitive_byte` from `primitives`.\n'
                        ' * Both are final structs with a single member `x1`, but publisher declares it as `char8` and subscriber as `byte`. Primitive types must match exactly for assignability.\n'
                        '**Test passes if:** Discovery fails due to type incompatibility.\n'
    },
    'struct_char8_char8': {
        'common_args': ['--type-folder types --type-file primitives'],
        'apps': ['pub-exe -P -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1',
                 'sub-exe -S -t test -y Test::struct_primitive_char8 --data-folder data --data-file struct_char_x1'],
        'expected_codes': [ReturnCode.OK, ReturnCode.OK],
        'check_function': tsf.data_is_correct,
        'title' : 'Communication between identical struct_primitive_char8',
        'description' : 'Verifies communication between `struct_primitive_char8` and `struct_primitive_char8`:\n\n'
                        ' * Publisher and Subscriber use `struct_primitive_char8` from `primitives`.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
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
        'title' : 'Communication between seq_int32x20 and seq_int32x10_trim',
        'description' : 'Verifies sequence with `@try_construct(trim)` truncates oversized data:\n\n'
                        ' * Publisher uses `seq_int32x20` from `try_construct`.\n'
                        ' * Subscriber uses `seq_int32x10_trim` from `try_construct`.\n'
                        ' * Publisher sequence bound is 20.\n'
                        ' * Subscriber bound is 10 with `@try_construct(trim)`.\n'
                        ' * Data exceeding 10 elements is trimmed to fit.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tryc_seq_2' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::seq_int32x10_discard --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between seq_int32x20 and seq_int32x10_discard but sample rejected',
        'description' : 'Verifies sequence with `@try_construct(discard)` rejects oversized data:\n\n'
                        ' * Publisher uses `seq_int32x20` from `try_construct`.\n'
                        ' * Subscriber uses `seq_int32x10_discard` from `try_construct`.\n'
                        ' * Publisher sequence bound is 20.\n'
                        ' * Subscriber bound is 10 with `@try_construct(discard)`.\n'
                        ' * Data exceeding 10 elements causes the entire sample to be discarded.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },
    'tryc_seq_3' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::seq_int32x10_default --data-folder data --data-file tryconstruct/seq_num_empty'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between seq_int32x20 and seq_int32x10_default',
        'description' : 'Verifies sequence with `@try_construct(use_default)` uses default value for oversized data:\n\n'
                        ' * Publisher uses `seq_int32x20` from `try_construct`.\n'
                        ' * Subscriber uses `seq_int32x10_default` from `try_construct`.\n'
                        ' * Publisher sequence bound is 20.\n'
                        ' * Subscriber bound is 10 with `@try_construct(use_default)`.\n'
                        ' * Oversized data is replaced with the default (empty sequence).\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tryc_seq_4' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::seq_int32x10 --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between seq_int32x20 and seq_int32x10 but sample rejected',
        'description' : 'Verifies sequence without explicit `@try_construct` and oversized data:\n\n'
                        ' * Publisher uses `seq_int32x20` from `try_construct`.\n'
                        ' * Subscriber uses `seq_int32x10` from `try_construct`.\n'
                        ' * Publisher sequence bound is 20.\n'
                        ' * Subscriber bound is 10 with no `@try_construct` annotation.\n'
                        ' * Default behavior (discard) applies to oversized data.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },

    'tryc_str_1' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10_trim --data-folder data --data-file tryconstruct/strings_trim_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between string20 and string10_trim',
        'description' : 'Verifies string with `@try_construct(trim)` truncates oversized data:\n\n'
                        ' * Publisher uses `string20` from `try_construct`.\n'
                        ' * Subscriber uses `string10_trim` from `try_construct`.\n'
                        ' * Publisher string bound is 20.\n'
                        ' * Subscriber bound is 10 with `@try_construct(trim)`.\n'
                        ' * Strings longer than 10 characters are trimmed.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tryc_str_2' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10_discard --data-folder data --data-file tryconstruct/strings_trim_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between string20 and string10_discard but sample rejected',
        'description' : 'Verifies string with `@try_construct(discard)` rejects oversized data:\n\n'
                        ' * Publisher uses `string20` from `try_construct`.\n'
                        ' * Subscriber uses `string10_discard` from `try_construct`.\n'
                        ' * Publisher string bound is 20.\n'
                        ' * Subscriber bound is 10 with `@try_construct(discard)`.\n'
                        ' * Strings longer than 10 characters cause the sample to be discarded.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },
    'tryc_str_3' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10_default --data-folder data --data-file tryconstruct/strings_default'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between string20 and string10_default',
        'description' : 'Verifies string with `@try_construct(use_default)` uses default value for oversized data:\n\n'
                        ' * Publisher uses `string20` from `try_construct`.\n'
                        ' * Subscriber uses `string10_default` from `try_construct`.\n'
                        ' * Publisher string bound is 20.\n'
                        ' * Subscriber bound is 10 with `@try_construct(use_default)`.\n'
                        ' * Oversized strings are replaced with the default (empty string).\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tryc_str_4' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::string10 --data-folder data --data-file tryconstruct/strings_trim_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between string20 and string10 but sample rejected',
        'description' : 'Verifies string without explicit `@try_construct` and oversized data:\n\n'
                        ' * Publisher uses `string20` from `try_construct`.\n'
                        ' * Subscriber uses `string10` from `try_construct`.\n'
                        ' * Publisher string bound is 20.\n'
                        ' * Subscriber bound is 10 with no `@try_construct` annotation.\n'
                        ' * Default behavior (discard) applies to oversized strings.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },

    'tryc_enum_1' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::struct_enum_1 --data-folder data --data-file tryconstruct/enum_val3',
                  'sub-exe -S -t test -y Test::struct_enum_2_discard --data-folder data --data-file tryconstruct/enum_val1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between struct_enum_1 and struct_enum_2_discard but sample rejected',
        'description' : 'Verifies enum with `@try_construct(discard)` rejects unrepresentable literals:\n\n'
                        ' * Publisher uses `struct_enum_1` from `try_construct`.\n'
                        ' * Subscriber uses `struct_enum_2_discard` from `try_construct`.\n'
                        ' * Publisher uses `E1` (4 literals: VAL0-VAL3).\n'
                        ' * Subscriber uses `E2` (3 literals: VAL0-VAL2) with `@try_construct(discard)`.\n'
                        ' * Literal `VAL3` is not in `E2`, so the sample is discarded.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },
    'tryc_enum_2' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::struct_enum_1 --data-folder data --data-file tryconstruct/enum_val3',
                  'sub-exe -S -t test -y Test::struct_enum_2_default --data-folder data --data-file tryconstruct/enum_val1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between struct_enum_1 and struct_enum_2_default',
        'description' : 'Verifies enum with `@try_construct(use_default)` replaces unrepresentable literals with default:\n\n'
                        ' * Publisher uses `struct_enum_1` from `try_construct`.\n'
                        ' * Subscriber uses `struct_enum_2_default` from `try_construct`.\n'
                        ' * Publisher uses `E1` (4 literals: VAL0-VAL3).\n'
                        ' * Subscriber uses `E2` (3 literals: VAL0-VAL2) with `@try_construct(use_default)`.\n'
                        ' * Literal `VAL3` is replaced with `E2`\'s default literal (`VAL1`).\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tryc_enum_3' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::struct_enum_1 --data-folder data --data-file tryconstruct/enum_val3',
                  'sub-exe -S -t test -y Test::struct_enum_2 --data-folder data --data-file tryconstruct/enum_val1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between struct_enum_1 and struct_enum_2 but sample rejected',
        'description' : 'Verifies enum without explicit `@try_construct` receiving unrepresentable literal:\n\n'
                        ' * Publisher uses `struct_enum_1` from `try_construct`.\n'
                        ' * Subscriber uses `struct_enum_2` from `try_construct`.\n'
                        ' * Publisher uses `E1` (4 literals: VAL0-VAL3).\n'
                        ' * Subscriber uses `E2` (3 literals: VAL0-VAL2) with no `@try_construct`.\n'
                        ' * Default behavior (discard) applies to unrepresentable literal `VAL3`.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },


    'tryc_union_seq_1' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::union_seq_int32x10_trim --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between union_seq_int32x20 and union_seq_int32x10_trim',
        'description' : 'Verifies union with sequence member using `@try_construct(trim)`:\n\n'
                        ' * Publisher uses `union_seq_int32x20` from `try_construct`.\n'
                        ' * Subscriber uses `union_seq_int32x10_trim` from `try_construct`.\n'
                        ' * Publisher union has `sequence<int32, 20>` member.\n'
                        ' * Subscriber has `sequence<int32, 10>` with `@try_construct(trim)`.\n'
                        ' * Oversized data is trimmed.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tryc_union_seq_2' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::union_seq_int32x10_discard --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between union_seq_int32x20 and union_seq_int32x10_discard but sample rejected',
        'description' : 'Verifies union with sequence member using `@try_construct(discard)`:\n\n'
                        ' * Publisher uses `union_seq_int32x20` from `try_construct`.\n'
                        ' * Subscriber uses `union_seq_int32x10_discard` from `try_construct`.\n'
                        ' * Publisher union has `sequence<int32, 20>` member.\n'
                        ' * Subscriber has `sequence<int32, 10>` with `@try_construct(discard)`.\n'
                        ' * Oversized data causes discard.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },
    'tryc_union_seq_3' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::union_seq_int32x10_default --data-folder data --data-file tryconstruct/seq_num_empty'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between union_seq_int32x20 and union_seq_int32x10_default',
        'description' : 'Verifies union with sequence member using `@try_construct(use_default)`:\n\n'
                        ' * Publisher uses `union_seq_int32x20` from `try_construct`.\n'
                        ' * Subscriber uses `union_seq_int32x10_default` from `try_construct`.\n'
                        ' * Publisher union has `sequence<int32, 20>` member.\n'
                        ' * Subscriber has `sequence<int32, 10>` with `@try_construct(use_default)`.\n'
                        ' * Oversized data replaced with empty sequence.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tryc_union_seq_4' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_seq_int32x20 --data-folder data --data-file array_num_20',
                  'sub-exe -S -t test -y Test::union_seq_int32x10 --data-folder data --data-file array_num_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between union_seq_int32x20 and union_seq_int32x10 but sample rejected',
        'description' : 'Verifies union with sequence member without explicit `@try_construct`:\n\n'
                        ' * Publisher uses `union_seq_int32x20` from `try_construct`.\n'
                        ' * Subscriber uses `union_seq_int32x10` from `try_construct`.\n'
                        ' * Publisher union has `sequence<int32, 20>` member.\n'
                        ' * Subscriber has `sequence<int32, 10>` with no `@try_construct`.\n'
                        ' * Default behavior (discard) applies.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },

    'tryc_union_str_1' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::union_string10_trim --data-folder data --data-file tryconstruct/strings_trim_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between union_string20 and union_string10_trim',
        'description' : 'Verifies union with string member using `@try_construct(trim)`:\n\n'
                        ' * Publisher uses `union_string20` from `try_construct`.\n'
                        ' * Subscriber uses `union_string10_trim` from `try_construct`.\n'
                        ' * Publisher union has `string<20>` member.\n'
                        ' * Subscriber has `string<10>` with `@try_construct(trim)`.\n'
                        ' * Oversized strings are trimmed.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tryc_union_str_2' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::union_string10_discard --data-folder data --data-file tryconstruct/strings_trim_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between union_string20 and union_string10_discard but sample rejected',
        'description' : 'Verifies union with string member using `@try_construct(discard)`:\n\n'
                        ' * Publisher uses `union_string20` from `try_construct`.\n'
                        ' * Subscriber uses `union_string10_discard` from `try_construct`.\n'
                        ' * Publisher union has `string<20>` member.\n'
                        ' * Subscriber has `string<10>` with `@try_construct(discard)`.\n'
                        ' * Oversized strings cause discard.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },
    'tryc_union_str_3' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::union_string10_default --data-folder data --data-file tryconstruct/strings_default'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between union_string20 and union_string10_default',
        'description' : 'Verifies union with string member using `@try_construct(use_default)`:\n\n'
                        ' * Publisher uses `union_string20` from `try_construct`.\n'
                        ' * Subscriber uses `union_string10_default` from `try_construct`.\n'
                        ' * Publisher union has `string<20>` member.\n'
                        ' * Subscriber has `string<10>` with `@try_construct(use_default)`.\n'
                        ' * Oversized strings replaced with empty string.\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tryc_union_str_4' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_string20 --data-folder data --data-file strings',
                  'sub-exe -S -t test -y Test::union_string10 --data-folder data --data-file tryconstruct/strings_trim_10'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between union_string20 and union_string10 but sample rejected',
        'description' : 'Verifies union with string member without explicit `@try_construct`:\n\n'
                        ' * Publisher uses `union_string20` from `try_construct`.\n'
                        ' * Subscriber uses `union_string10` from `try_construct`.\n'
                        ' * Publisher union has `string<20>` member.\n'
                        ' * Subscriber has `string<10>` with no `@try_construct`.\n'
                        ' * Default behavior (discard) applies.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },

    'tryc_union_enum_1' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_enum_1 --data-folder data --data-file tryconstruct/enum_val3',
                  'sub-exe -S -t test -y Test::union_enum_2_discard --data-folder data --data-file tryconstruct/enum_val1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between union_enum_1 and union_enum_2_discard but sample rejected',
        'description' : 'Verifies union with enum member using `@try_construct(discard)`:\n\n'
                        ' * Publisher uses `union_enum_1` from `try_construct`.\n'
                        ' * Subscriber uses `union_enum_2_discard` from `try_construct`.\n'
                        ' * Publisher union uses `E1` (4 literals).\n'
                        ' * Subscriber uses `E2` (3 literals) with `@try_construct(discard)`.\n'
                        ' * Unrepresentable literal `VAL3` causes discard.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },
    'tryc_union_enum_2' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_enum_1 --data-folder data --data-file tryconstruct/enum_val3',
                  'sub-exe -S -t test -y Test::union_enum_2_default --data-folder data --data-file tryconstruct/enum_val1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between union_enum_1 and union_enum_2_default',
        'description' : 'Verifies union with enum member using `@try_construct(use_default)`:\n\n'
                        ' * Publisher uses `union_enum_1` from `try_construct`.\n'
                        ' * Subscriber uses `union_enum_2_default` from `try_construct`.\n'
                        ' * Publisher union uses `E1` (4 literals).\n'
                        ' * Subscriber uses `E2` (3 literals) with `@try_construct(use_default)`.\n'
                        ' * Unrepresentable literal replaced with `E2` default (`VAL1`).\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tryc_union_enum_3' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_enum_1 --data-folder data --data-file tryconstruct/enum_val3',
                  'sub-exe -S -t test -y Test::union_enum_2 --data-folder data --data-file tryconstruct/enum_val1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between union_enum_1 and union_enum_2 but sample rejected',
        'description' : 'Verifies union with enum member without explicit `@try_construct`:\n\n'
                        ' * Publisher uses `union_enum_1` from `try_construct`.\n'
                        ' * Subscriber uses `union_enum_2` from `try_construct`.\n'
                        ' * Publisher union uses `E1` (4 literals).\n'
                        ' * Subscriber uses `E2` (3 literals) with no `@try_construct`.\n'
                        ' * Default behavior (discard) applies.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },

    'tryc_union_enum_disc_1' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_disc_enum_1 --data-folder data --data-file tryconstruct/union_x3',
                  'sub-exe -S -t test -y Test::union_disc_enum_2_discard --data-folder data --data-file tryconstruct/union_x1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between union_disc_enum_1 and union_disc_enum_2_discard but sample rejected',
        'description' : 'Verifies union with enum discriminator using `@try_construct(discard)` on discriminator:\n\n'
                        ' * Publisher uses `union_disc_enum_1` from `try_construct`.\n'
                        ' * Subscriber uses `union_disc_enum_2_discard` from `try_construct`.\n'
                        ' * Publisher discriminator is `E1` (4 literals: VAL0-VAL3).\n'
                        ' * Subscriber discriminator is `E2` (3 literals: VAL0-VAL2) with `@try_construct(discard)`.\n'
                        ' * Discriminator value `VAL3` is not representable.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
    },
    'tryc_union_enum_disc_2' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_disc_enum_1 --data-folder data --data-file tryconstruct/union_x3',
                  'sub-exe -S -t test -y Test::union_disc_enum_2_default --data-folder data --data-file tryconstruct/union_x1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.OK],
        'check_function' : tsf.data_is_correct,
        'title' : 'Communication between union_disc_enum_1 and union_disc_enum_2_default',
        'description' : 'Verifies union with enum discriminator using `@try_construct(use_default)` on discriminator:\n\n'
                        ' * Publisher uses `union_disc_enum_1` from `try_construct`.\n'
                        ' * Subscriber uses `union_disc_enum_2_default` from `try_construct`.\n'
                        ' * Publisher discriminator is `E1` (4 literals: VAL0-VAL3).\n'
                        ' * Subscriber discriminator is `E2` (3 literals: VAL0-VAL2) with `@try_construct(use_default)`.\n'
                        ' * Discriminator `VAL3` is replaced with `E2` default (`VAL1`).\n'
                        '**Test passes if:** Discovery succeeds and the subscriber receives the sample.\n'
    },
    'tryc_union_enum_disc_3' : {
        'common_args' : ['--type-folder types --type-file try_construct'],
        'apps' : ['pub-exe -P -t test -y Test::union_disc_enum_1 --data-folder data --data-file tryconstruct/union_x3',
                  'sub-exe -S -t test -y Test::union_disc_enum_2 --data-folder data --data-file tryconstruct/union_x1'],
        'expected_codes' : [ReturnCode.OK, ReturnCode.DATA_NOT_RECEIVED],
        'check_function' : tsf.data_is_correct,
        'title' : 'Type assignability between union_disc_enum_1 and union_disc_enum_2 but sample rejected',
        'description' : 'Verifies union with enum discriminator without explicit `@try_construct`:\n\n'
                        ' * Publisher uses `union_disc_enum_1` from `try_construct`.\n'
                        ' * Subscriber uses `union_disc_enum_2` from `try_construct`.\n'
                        ' * Publisher discriminator is `E1` (4 literals: VAL0-VAL3).\n'
                        ' * Subscriber discriminator is `E2` (3 literals: VAL0-VAL2) with no `@try_construct`.\n'
                        ' * Default behavior (discard) applies.\n'
                        '**Test passes if:** Discovery succeeds but the sample is not delivered.\n'
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
