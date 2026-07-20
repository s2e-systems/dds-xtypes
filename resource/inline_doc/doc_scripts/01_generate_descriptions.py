#!/usr/bin/env python3
"""Generate rich titles and descriptions for all tests in ../../../test_suite.py.

This script generates descriptions that explain:
1. What is being tested (concept)
2. What types are used and from where
3. What's DIFFERENT between the types (the key insight)
4. Why this matters for the expected outcome
5. What the test passes on
"""

import re
import sys

FILE = '../../../test_suite.py'

# ===== COMPREHENSIVE TYPE KNOWLEDGE BASE =====
# Maps (pub_type, sub_type) -> (concept_sentence, delta_bullets)
# concept_sentence: a short explanation of what's being verified
# delta_bullets: list of bullet strings explaining the structural differences

TYPE_KNOWLEDGE = {
    # === EXTENSIBILITY types ===
    ('struct_f1', 'struct_f1'): (
        'identical final structs can communicate',
        []  # No delta
    ),
    ('struct_f1', 'struct_f2'): (
        'final structs with different member counts are not assignable',
        ['`struct_f2` has an extra member `x2` (`int32`) at the end; final extensibility forbids appending members.']
    ),
    ('struct_a1', 'struct_a1'): (
        'identical appendable structs can communicate',
        []
    ),
    ('struct_a1', 'struct_a2'): (
        'appendable structs allow an appended trailing member',
        ['`struct_a2` has an extra member `x2` (`int32`) appended at the end; appendable extensibility permits this.']
    ),
    ('struct_a2', 'struct_a1'): (
        'appendable structs allow the publisher to have additional trailing members',
        ['Publisher\'s `struct_a2` has an extra trailing member `x2` (`int32`) that the subscriber\'s `struct_a1` ignores.']
    ),
    ('struct_a2', 'struct_a3'): (
        'appendable structs with a member inserted in the middle are not assignable',
        ['`struct_a3` inserts member `x3` between `x1` and `x2`, changing the serialization order; appendable types require positional matching.']
    ),
    ('struct_a3', 'struct_a2'): (
        'appendable structs with a member inserted in the middle are not assignable',
        ['`struct_a3` has member `x3` inserted between `x1` and `x2`; since position matters for appendable types, this breaks assignability.']
    ),
    ('struct_m1', 'struct_m1'): (
        'identical mutable structs can communicate',
        []
    ),
    ('struct_m1', 'struct_m2'): (
        'mutable structs allow an extra member with explicit ID',
        ['`struct_m2` has an extra member `x2` with explicit `id=2`; mutable types match by member ID, so extra members are allowed.']
    ),
    ('struct_m2', 'struct_m1'): (
        'mutable structs allow the publisher to have additional members',
        ['Publisher\'s `struct_m2` has member `x2` (`id=2`) that the subscriber\'s `struct_m1` does not; mutable types allow this.']
    ),
    ('struct_m2', 'struct_m3'): (
        'mutable structs remain assignable when a member is inserted in the middle with an explicit ID',
        ['`struct_m3` inserts member `x3` (`id=3`) between `x1` and `x2`; since mutable types match by ID (not position), this is valid.']
    ),
    ('struct_m3', 'struct_m2'): (
        'mutable structs remain assignable when the publisher has an extra member identified by ID',
        ['Publisher\'s `struct_m3` has member `x3` (`id=3`) between `x1` and `x2` that the subscriber does not; mutable ID-based matching allows this.']
    ),
    ('struct_m2', 'struct_m4'): (
        'mutable structs without explicit IDs are not assignable to those with explicit IDs',
        ['`struct_m2` uses explicit member IDs (`x1` id=1, `x2` id=2); `struct_m4` has no explicit IDs, so auto-assigned IDs differ, causing mismatch.']
    ),
    ('struct_hashid_1', 'struct_hashid_2'): (
        'structs using `hashid` can communicate when hash IDs match',
        ['Publisher\'s `struct_hashid_1` has member `x1` with `autoid=hash`; subscriber\'s `struct_hashid_2` has member `x2` with `hashid="x1"`, resolving to the same hash ID.']
    ),

    # === TYPE_CONSISTENCY types ===
    ('struct_x1', 'struct_x2'): (
        'structs with same-type members but different member names',
        ['Both have one `int32` member, but named `x1` in publisher and `x2` in subscriber.']
    ),
    ('struct_x1', 'struct_x1'): (
        'identical `struct_x1` types',
        []
    ),
    ('seq_int32x10', 'seq_int32x20'): (
        'sequences with different bounds (smaller publisher bound)',
        ['Publisher sequence bound is 10; subscriber sequence bound is 20. Subscriber bound >= publisher bound.']
    ),
    ('seq_int32x20', 'seq_int32x10'): (
        'sequences with different bounds (larger publisher bound)',
        ['Publisher sequence bound is 20; subscriber sequence bound is 10. The published data exceeds the subscriber bound.']
    ),
    ('string10', 'string20'): (
        'strings with different bounds (smaller publisher bound)',
        ['Publisher string bound is 10; subscriber string bound is 20. Subscriber bound >= publisher bound.']
    ),
    ('string20', 'string10'): (
        'strings with different bounds (larger publisher bound)',
        ['Publisher string bound is 20; subscriber string bound is 10. The published data may exceed the subscriber bound.']
    ),

    # === ARRAY types ===
    ('int32x10', 'int32x10'): (
        'identical `int32` arrays communicate',
        ['Both use `int32[10]` arrays with the same element type and dimension.']
    ),
    ('int32x10', 'int32x20'): (
        'arrays with different dimensions are not assignable',
        ['Publisher array is `int32[10]`; subscriber array is `int32[20]`. Array dimensions must match exactly.']
    ),
    ('int32x20', 'int32x10'): (
        'arrays with different dimensions are not assignable',
        ['Publisher array is `int32[20]`; subscriber array is `int32[10]`. Array dimensions must match exactly.']
    ),
    ('int32x10', 'uint32x10'): (
        'arrays with different element types are not assignable',
        ['Publisher element type is `int32`; subscriber element type is `uint32`. Array elements must be strongly assignable.']
    ),
    ('int32x10x2', 'int32x20'): (
        'multi-dimensional and single-dimensional arrays of same total size are not assignable',
        ['Publisher is `int32[10][2]` (2D, 20 elements total); subscriber is `int32[20]` (1D). Dimensions must match structurally, not just in total count.']
    ),
    ('string10x10', 'string20x10'): (
        'arrays of strings with different string bounds are assignable when element type is strongly assignable',
        ['Both are `string[10]` arrays; publisher elements have `stringMaxLength=10`, subscriber has `stringMaxLength=20`. String elements are strongly assignable since subscriber bound >= publisher bound.']
    ),
    ('enum1x10', 'enum2x10'): (
        'arrays of appendable enums with subset literals are assignable',
        ['Both are enum arrays of size 10; publisher uses `E1` (3 literals: VAL0-VAL2), subscriber uses `E2` (4 literals: VAL0-VAL3). `E2` is a superset of `E1`, so elements are strongly assignable.']
    ),
    ('enum1', 'enum2'): (
        'appendable enums where subscriber is a superset are assignable',
        ['Publisher uses `E1` (3 literals: VAL0-VAL2); subscriber uses `E2` (4 literals: VAL0-VAL3). `E2` is a superset of `E1`.']
    ),
    ('F_S__array10_F_S__array20_uint32', 'F_S__array10_F_S__array20_uint32_alt'): (
        'arrays of final structs are assignable when inner struct elements are strongly assignable',
        ['Both are arrays of 10 final structs containing `uint32[20]`; member names differ (`x1` vs `altx1`) but the types are structurally equivalent.']
    ),
    ('F_S__array10_A_S__array20_uint32', 'F_S__array10_A_S__array20_uint32_alt'): (
        'arrays of appendable structs are assignable when inner struct elements are strongly assignable',
        ['Both are arrays of 10 structs containing appendable inner structs with `uint32[20]`; member names differ (`x1` vs `altx1`).']
    ),
    ('F_S__array10_M_S__array20_uint32', 'F_S__array10_M_S__array20_uint32_alt'): (
        'arrays of mutable structs are assignable when inner struct elements are strongly assignable',
        ['Both are arrays of 10 mutable structs containing `uint32[20]`; member names differ (`x1` vs `altx1`).']
    ),

    # === SEQUENCE types ===
    ('int32_unbounded', 'int32x10'): (
        'unbounded sequence is assignable to bounded sequence (default ignore_seq_bounds)',
        ['Publisher uses unbounded `sequence<int32>`; subscriber uses `sequence<int32, 10>`. By default, sequence bounds are ignored for assignability.']
    ),
    ('int32x20', 'int32x10'): (
        'sequence with larger bound sending data exceeding subscriber bound',
        ['Publisher uses `sequence<int32, 20>` with 20 elements; subscriber uses `sequence<int32, 10>`. The actual data size (20) exceeds subscriber bound (10).']
    ),
    ('int32x10', 'int32x20'): (
        'sequence with smaller bound is assignable to sequence with larger bound',
        ['Publisher uses `sequence<int32, 10>`; subscriber uses `sequence<int32, 20>`. Subscriber bound >= publisher bound, and data fits.']
    ),
    ('string10x10', 'string20x10'): (
        'sequences of strings with different string bounds are assignable',
        ['Both are `sequence<string, 10>`; publisher string bound is 10, subscriber is 20. String elements are strongly assignable since subscriber bound >= publisher bound.']
    ),
    ('string20x10', 'string10x10'): (
        'sequences of strings where publisher string bound exceeds subscriber string bound',
        ['Both are `sequence<string, 10>`; publisher string bound is 20, subscriber is 10.']
    ),
    ('F_S__seq10_F_S__seq20_uint32', 'F_S__seq10_F_S__seq20_uint32_alt'): (
        'sequences of final structs are assignable when inner elements are strongly assignable',
        ['Both are sequences of final structs containing `uint32` sequences; member names differ (`x1` vs `altx1`) but types are structurally equivalent.']
    ),
    ('F_S__seq10_A_S__seq20_uint32', 'F_S__seq10_A_S__seq20_uint32_alt'): (
        'sequences of appendable structs are assignable when inner elements are strongly assignable',
        ['Both are sequences of appendable structs containing `uint32` sequences; member names differ (`x1` vs `altx1`).']
    ),
    ('F_S__seq10_M_S__seq20_uint32', 'F_S__seq10_M_S__seq20_uint32_alt'): (
        'sequences of mutable structs are assignable when inner elements are strongly assignable',
        ['Both are sequences of mutable structs containing `uint32` sequences; member names differ (`x1` vs `altx1`).']
    ),

    # === STRING types ===
    ('string_unbounded', 'string_unbounded'): (
        'identical unbounded strings communicate',
        ['Both use unbounded `string` type.']
    ),
    ('string_unbounded', 'string10'): (
        'unbounded string sending data exceeding subscriber bound',
        ['Publisher uses unbounded `string`; subscriber uses `string<10>`. The published string ("hello world!") exceeds the subscriber bound.']
    ),
    ('wstring_unbounded', 'wstring_unbounded'): (
        'identical unbounded wide strings communicate',
        ['Both use unbounded `wstring` type.']
    ),
    ('wstring_unbounded', 'wstring10'): (
        'unbounded wstring sending data exceeding subscriber bound',
        ['Publisher uses unbounded `wstring`; subscriber uses `wstring<10>`. The published wstring exceeds the subscriber bound.']
    ),
    ('wstring10', 'wstring20'): (
        'wstring with smaller bound is assignable to wstring with larger bound',
        ['Publisher uses `wstring<10>`; subscriber uses `wstring<20>`. Subscriber bound >= publisher bound.']
    ),
    ('wstring20', 'wstring10'): (
        'wstring with larger bound is not assignable when bounds are checked',
        ['Publisher uses `wstring<20>`; subscriber uses `wstring<10>`. Publisher bound exceeds subscriber bound.']
    ),
    ('string10', 'string20'): (
        'string with smaller bound is assignable to string with larger bound',
        ['Publisher uses `string<10>`; subscriber uses `string<20>`. Subscriber bound >= publisher bound.']
    ),
    ('string20', 'string10'): (
        'string with larger bound is not assignable when bounds are checked',
        ['Publisher uses `string<20>`; subscriber uses `string<10>`. Publisher bound exceeds subscriber bound.']
    ),

    # === STRUCT types (struct_names.xml) ===
    ('struct_1', 'struct_2'): (
        'mutable structs where member names match but IDs differ are assignable by default',
        ['Both have member `x1` but with different IDs (id=1 in publisher, id=2 in subscriber). Both share member `x5` (id=5). By default, `ignore_member_names` is true so ID matching is used.']
    ),
    ('struct_3', 'struct_4'): (
        'final structs where member IDs match but names differ',
        ['Both have one member at id=1, but named `x1` in publisher and `x2` in subscriber.']
    ),
    ('struct_5', 'struct_6'): (
        'mutable structs with no common member IDs are not assignable',
        ['`struct_5` has member `x1` (id=1)', '`struct_6` has member `x2` (id=2)', 'No common member IDs exist.', 'Mutable extensibility requires at least one member in common (same ID).']
    ),
    ('struct_primitive_uint8', 'struct_primitive_uint16'): (
        'structs with non-assignable member types are not assignable',
        ['Both are final with one member `x1`, but publisher declares it as `byte` and subscriber as `uint16`. Members with matching IDs must have assignable types; `byte` and `uint16` are not assignable.']
    ),
    ('struct_mustUnderstand', 'struct_int32'): (
        'subscriber cannot ignore a `@must_understand` member from the publisher',
        ['Publisher\'s `struct_mustUnderstand` has member `x2` annotated with `@must_understand`; subscriber\'s `struct_int32` only has `x1`. A non-optional `@must_understand` member must appear in both types.']
    ),
    ('struct_int32', 'struct_mustUnderstand'): (
        'subscriber\'s extra `@must_understand` member must be present in the publisher type',
        ['Subscriber\'s `struct_mustUnderstand` has member `x2` annotated with `@must_understand`; publisher\'s `struct_int32` only has `x1`. A non-optional `@must_understand` member must appear in both types.']
    ),
    ('struct_key_1', 'struct_key_2'): (
        '`@key` members in one type must be present in the other',
        ['Publisher\'s `struct_key_1` has `@key` member `x2` (`int32`); subscriber\'s `struct_key_2` only has `x1`. Key members must appear in both types for assignability.']
    ),
    ('struct_key_2', 'struct_key_1'): (
        '`@key` members in one type must be present in the other',
        ['Subscriber\'s `struct_key_1` has `@key` member `x2` (`int32`); publisher\'s `struct_key_2` only has `x1`. Key members must appear in both types for assignability.']
    ),
    ('struct_key_string10', 'struct_key_string20'): (
        '`@key` string member with smaller publisher bound is assignable to larger subscriber bound',
        ['Both have `@key` string member `x1`; publisher bound is 10, subscriber bound is 20.']
    ),
    ('struct_key_string10', 'struct_key_string10'): (
        'identical `@key` string structs communicate',
        []
    ),
    ('struct_key_string20', 'struct_key_string10'): (
        '`@key` string member where publisher bound exceeds subscriber bound',
        ['Both have `@key` string member `x1`; publisher bound is 20, subscriber bound is 10. Key string bounds are checked regardless of `ignore_string_bounds`.']
    ),
    ('struct_key_enum_1', 'struct_key_enum_2'): (
        '`@key` enum member where subscriber enum is a superset',
        ['Both have `@key` enum member `x1`; publisher uses `E1` (3 literals: VAL0-VAL2), subscriber uses `E2` (4 literals: VAL0-VAL3). Subscriber\'s enum is a superset.']
    ),
    ('struct_key_enum_2', 'struct_key_enum_1'): (
        '`@key` enum member where publisher has more literals than subscriber',
        ['Both have `@key` enum member `x1`; publisher uses `E2` (4 literals: VAL0-VAL3), subscriber uses `E1` (3 literals: VAL0-VAL2). Publisher can send literal `VAL3` which subscriber cannot represent.']
    ),
    ('struct_key_seq10', 'struct_key_seq20'): (
        '`@key` sequence member with smaller publisher bound is assignable',
        ['Both have `@key` sequence member `x1`; publisher bound is 10, subscriber bound is 20.']
    ),
    ('struct_key_seq20', 'struct_key_seq10'): (
        '`@key` sequence member where publisher bound exceeds subscriber bound',
        ['Both have `@key` sequence member `x1`; publisher bound is 20, subscriber bound is 10. Key sequence bounds are checked regardless of `ignore_sequence_bounds`.']
    ),
    ('struct_key_struct_1', 'struct_key_struct_2'): (
        '`@key` struct member where inner types are assignable',
        ['Both have `@key` struct member `x1`; publisher inner type `key_1` has string bounds (k1=10, x2=20), subscriber inner type `key_2` has (k1=20, x2=10). Key holder assignability is checked.']
    ),
    ('struct_key_struct_2', 'struct_key_struct_1'): (
        '`@key` struct member where inner key string bound is reversed',
        ['Both have `@key` struct member `x1`; publisher inner type `key_2` has key string bound 20, subscriber inner type `key_1` has key string bound 10.']
    ),
    ('struct_key_union_1', 'struct_key_union_2'): (
        '`@key` union member where subscriber union has additional case',
        ['Both have `@key` union member `x1`; publisher uses `u_1` (cases 1,2), subscriber uses `u_2` (cases 1,2,3). Subscriber union is a superset.']
    ),
    ('struct_key_union_2', 'struct_key_union_1'): (
        '`@key` union member where publisher union has additional case',
        ['Both have `@key` union member `x1`; publisher uses `u_2` (cases 1,2,3), subscriber uses `u_1` (cases 1,2).']
    ),

    # === PRIMITIVE struct types (primitives.xml) ===
    ('struct_primitives_final', 'struct_primitives_final'): (
        'identical final primitive structs communicate',
        ['Both use the same final struct with 14 primitive members (uint8 through char8).']
    ),
    ('struct_primitives_appendable', 'struct_primitives_appendable'): (
        'identical appendable primitive structs communicate',
        ['Both use the same appendable struct with 14 primitive members.']
    ),
    ('struct_primitives_mutable', 'struct_primitives_mutable'): (
        'identical mutable primitive structs communicate',
        ['Both use the same mutable struct with 14 primitive members.']
    ),
    ('struct_primitives_final', 'struct_primitives_appendable'): (
        'structs with mismatched extensibility are not assignable',
        ['Publisher is `final`; subscriber is `appendable`. Extensibility must match for assignability.']
    ),
    ('struct_primitives_final', 'struct_primitives_mutable'): (
        'structs with mismatched extensibility are not assignable',
        ['Publisher is `final`; subscriber is `mutable`. Extensibility must match for assignability.']
    ),
    ('struct_primitives_appendable', 'struct_primitives_final'): (
        'structs with mismatched extensibility are not assignable',
        ['Publisher is `appendable`; subscriber is `final`. Extensibility must match for assignability.']
    ),
    ('struct_primitives_appendable', 'struct_primitives_mutable'): (
        'structs with mismatched extensibility are not assignable',
        ['Publisher is `appendable`; subscriber is `mutable`. Extensibility must match for assignability.']
    ),
    ('struct_primitives_mutable', 'struct_primitives_final'): (
        'structs with mismatched extensibility are not assignable',
        ['Publisher is `mutable`; subscriber is `final`. Extensibility must match for assignability.']
    ),
    ('struct_primitives_mutable', 'struct_primitives_appendable'): (
        'structs with mismatched extensibility are not assignable',
        ['Publisher is `mutable`; subscriber is `appendable`. Extensibility must match for assignability.']
    ),

    # === UNION types (unions.xml) ===
    ('union_primitives_final', 'union_primitives_final'): (
        'identical final primitive unions communicate',
        ['Both use the same final union with 14 cases covering all primitive types.']
    ),
    ('union_primitives_appendable', 'union_primitives_appendable'): (
        'identical appendable primitive unions communicate',
        ['Both use the same appendable union with 14 cases.']
    ),
    ('union_primitives_mutable', 'union_primitives_mutable'): (
        'identical mutable primitive unions communicate',
        ['Both use the same mutable union with 14 cases.']
    ),
    ('union_primitives_final', 'union_primitives_appendable'): (
        'unions with mismatched extensibility are not assignable',
        ['Publisher is `final`; subscriber is `appendable`. Extensibility must match.']
    ),
    ('union_primitives_final', 'union_primitives_mutable'): (
        'unions with mismatched extensibility are not assignable',
        ['Publisher is `final`; subscriber is `mutable`. Extensibility must match.']
    ),
    ('union_primitives_appendable', 'union_primitives_final'): (
        'unions with mismatched extensibility are not assignable',
        ['Publisher is `appendable`; subscriber is `final`. Extensibility must match.']
    ),
    ('union_primitives_appendable', 'union_primitives_mutable'): (
        'unions with mismatched extensibility are not assignable',
        ['Publisher is `appendable`; subscriber is `mutable`. Extensibility must match.']
    ),
    ('union_primitives_mutable', 'union_primitives_final'): (
        'unions with mismatched extensibility are not assignable',
        ['Publisher is `mutable`; subscriber is `final`. Extensibility must match.']
    ),
    ('union_primitives_mutable', 'union_primitives_appendable'): (
        'unions with mismatched extensibility are not assignable',
        ['Publisher is `mutable`; subscriber is `appendable`. Extensibility must match.']
    ),
    ('union_uint32', 'union_uint32'): (
        'identical union with uint32 discriminator communicates',
        []
    ),
    ('union_uint32', 'union_bitmask32'): (
        'unions with strongly-assignable discriminator types communicate',
        ['Publisher discriminator is `uint32`; subscriber discriminator is `bitmask` with `bitBound=32`. A 32-bit bitmask is strongly assignable from `uint32`.']
    ),
    ('union_uint32', 'union_bitmask16'): (
        'unions with non-assignable discriminator types are not assignable',
        ['Publisher discriminator is `uint32`; subscriber discriminator is `bitmask` with `bitBound=16`. A 16-bit bitmask is not strongly assignable from `uint32`.']
    ),
    ('union_uint32', 'union_uint32_key'): (
        'unions where one discriminator is `@key` and the other is not are not assignable',
        ['Publisher discriminator has no `@key` annotation; subscriber discriminator has `key="true"`. Both must agree on whether the discriminator is `@key`.']
    ),
    ('union_1', 'union_2'): (
        'appendable unions with reordered members having different discriminator values',
        ['`union_1` has members `x1`(discriminator=1), `x2`(discriminator=2), `x3`(discriminator=3); `union_2` has same members reordered: `x2`(discriminator=2), `x1`(discriminator=1), `x3`(discriminator=3). Member order differs but discriminator/type pairs match.']
    ),
    ('union_3', 'union_4'): (
        'appendable unions where same discriminator values map to different member names',
        ['`union_3` has discriminator=1->`x1`(int16), discriminator=2->`x2`(int32); `union_4` has discriminator=1->`x2`(int16), discriminator=2->`x1`(int32). Same discriminator values map to different names but same types.']
    ),
    ('union_5', 'union_6'): (
        'appendable unions with explicit IDs and reordered cases',
        ['Both have members with explicit IDs (id=1,2,3). `union_5` has discriminator order 1,2,3; `union_6` has discriminator order 2,1,3. Explicit IDs ensure correct matching regardless of order.']
    ),
    ('union_int16', 'union_int32'): (
        'unions where one discriminator label selects non-assignable member types',
        ['For discriminator=2: publisher selects `x2` as `int16`, subscriber selects `x2` as `int32`. A label that selects non-assignable types breaks assignability.']
    ),
    ('union_int32', 'union_int16'): (
        'unions where one discriminator label selects non-assignable member types',
        ['For discriminator=2: publisher selects `x2` as `int32`, subscriber selects `x2` as `int16`. A label that selects non-assignable types breaks assignability.']
    ),
    ('union_int32_default', 'union_int32_default'): (
        'identical unions with default discriminator communicate',
        ['Both use `union_int32_default` with a `default` case selecting `int32` member `x2`.']
    ),
    ('union_int16', 'union_int32_default'): (
        'union where subscriber default case selects a non-assignable member type',
        ['Publisher discriminator=2 selects `x2`(`int16`); subscriber `default` case covers discriminator=2 and selects `x2`(`int32`). `int16` is not assignable from `int32`.']
    ),
    ('union_int32', 'union_int32_default'): (
        'union with explicit discriminator=2 vs union with default case',
        ['Publisher has explicit case discriminator=2 selecting `x2`(`int32`); subscriber uses `default` case for `x2`(`int32`). The default case covers discriminator=2.']
    ),
    ('union_int32_default', 'union_int32'): (
        'union with default case vs union with explicit discriminator=2',
        ['Publisher uses `default` case for `x2`(`int32`); subscriber has explicit case discriminator=2 selecting `x2`(`int32`).']
    ),
    ('union_int32_default', 'union_int16'): (
        'union where publisher default case covers labels that select non-assignable types in subscriber',
        ['Publisher `default` case selects `x2`(`int32`); subscriber discriminator=2 selects `x2`(`int16`). `int16` is not assignable from `int32`.']
    ),
    ('union_int32_default', 'union_int16_default'): (
        'unions where both have default cases but with non-assignable member types',
        ['Both have a `default` case: publisher selects `x2`(`int32`), subscriber selects `x2`(`int16`). `int16` is not assignable from `int32`.']
    ),
    ('union_final_5', 'union_final_6'): (
        'final unions with different numbers of cases',
        ['`union_final_5` has 5 cases (discriminator 1-5); `union_final_6` has 6 cases (disc 0-5). Final unions must have the same set of discriminator labels.']
    ),
    ('union_final_6', 'union_final_5'): (
        'final unions with different numbers of cases (reverse direction)',
        ['`union_final_6` has 6 cases (disc 0-5); `union_final_5` has 5 cases (discriminator 1-5). Final unions must have the same set of discriminator labels.']
    ),
    ('union_final_5', 'union_final_5_default'): (
        'final unions where one has a default case',
        ['`union_final_5` has 5 explicit cases (discriminator 1-5); `union_final_5_default` has the same 5 cases plus a `default` case.']
    ),
    ('union_final_5_default', 'union_final_5'): (
        'final unions where publisher has default case but subscriber does not',
        ['Publisher `union_final_5_default` has 5 cases plus `default`; subscriber `union_final_5` has only 5 explicit cases.']
    ),
    ('union_appendable_a', 'union_appendable_b'): (
        'appendable unions with one common discriminator label',
        ['`union_appendable_a` has cases discriminator=1..5; `union_appendable_b` has cases discriminator=10..15. Only discriminator=3 maps to same member `x3`(`int64`) in both.']
    ),
    ('union_appendable_b', 'union_appendable_a'): (
        'appendable unions with one common discriminator label (reverse direction)',
        ['`union_appendable_b` has cases discriminator=10..15; `union_appendable_a` has cases discriminator=1..5. Only discriminator=3 maps to same member `x3`(`int64`) in both.']
    ),
    ('union_appendable_a', 'union_appendable_c'): (
        'appendable unions with no common discriminator labels',
        ['`union_appendable_a` has cases discriminator=1..5; `union_appendable_c` has cases discriminator=10..15. No discriminator value is shared.']
    ),
    ('union_appendable_c', 'union_appendable_a'): (
        'appendable unions with no common discriminator labels (reverse direction)',
        ['`union_appendable_c` has cases discriminator=10..15; `union_appendable_a` has cases discriminator=1..5. No discriminator value is shared.']
    ),
    ('union_appendable_a_default', 'union_appendable_b_default'): (
        'appendable unions with no common explicit discriminator labels are not assignable even when both have a default case',
        ['`union_appendable_a_default` has discriminator=5 + default', '`union_appendable_b_default` has discriminator=15 + default', 'No explicit discriminator value is shared.', 'The default case alone does not satisfy the requirement of at least one member in common.']
    ),
    ('union_mutable_a', 'union_mutable_b'): (
        'mutable unions with one common discriminator label',
        ['`union_mutable_a` has cases discriminator=1..5; `union_mutable_b` has cases discriminator=3,10..15. Only discriminator=3 maps to same member `x3`(`int64`) in both. Mutable extensibility requires at least one member in common for assignability.']
    ),
    ('union_mutable_a', 'union_mutable_c'): (
        'mutable unions with no common discriminator labels are not assignable',
        ['`union_mutable_a` has cases discriminator=1..5', '`union_mutable_c` has cases discriminator=10..15', 'No discriminator value is shared.', 'Mutable extensibility requires at least one member in common.']
    ),
    ('union_mutable_a_default', 'union_mutable_b_default'): (
        'mutable unions with no common explicit discriminator labels are not assignable even when both have a default case',
        ['`union_mutable_a_default` has discriminator=5 + default', '`union_mutable_b_default` has discriminator=15 + default', 'No explicit discriminator value is shared.', 'The default case alone does not satisfy the mutable requirement of at least one member in common.']
    ),

    # === TRY_CONSTRUCT types ===
    ('seq_int32x20', 'seq_int32x10_trim'): (
        'sequence with `@try_construct(trim)` truncates oversized data',
        ['Publisher sequence bound is 20; subscriber bound is 10 with `@try_construct(trim)`. Data exceeding 10 elements is trimmed to fit.']
    ),
    ('seq_int32x20', 'seq_int32x10_discard'): (
        'sequence with `@try_construct(discard)` rejects oversized data',
        ['Publisher sequence bound is 20; subscriber bound is 10 with `@try_construct(discard)`. Data exceeding 10 elements causes the entire sample to be discarded.']
    ),
    ('seq_int32x20', 'seq_int32x10_default'): (
        'sequence with `@try_construct(use_default)` uses default value for oversized data',
        ['Publisher sequence bound is 20; subscriber bound is 10 with `@try_construct(use_default)`. Oversized data is replaced with the default (empty sequence).']
    ),
    ('seq_int32x20', 'seq_int32x10'): (
        'sequence without explicit `@try_construct` and oversized data',
        ['Publisher sequence bound is 20; subscriber bound is 10 with no `@try_construct` annotation. Default behavior (discard) applies to oversized data.']
    ),
    ('string20', 'string10_trim'): (
        'string with `@try_construct(trim)` truncates oversized data',
        ['Publisher string bound is 20; subscriber bound is 10 with `@try_construct(trim)`. Strings longer than 10 characters are trimmed.']
    ),
    ('string20', 'string10_discard'): (
        'string with `@try_construct(discard)` rejects oversized data',
        ['Publisher string bound is 20; subscriber bound is 10 with `@try_construct(discard)`. Strings longer than 10 characters cause the sample to be discarded.']
    ),
    ('string20', 'string10_default'): (
        'string with `@try_construct(use_default)` uses default value for oversized data',
        ['Publisher string bound is 20; subscriber bound is 10 with `@try_construct(use_default)`. Oversized strings are replaced with the default (empty string).']
    ),
    ('string20', 'string10'): (
        'string without explicit `@try_construct` and oversized data',
        ['Publisher string bound is 20; subscriber bound is 10 with no `@try_construct` annotation. Default behavior (discard) applies to oversized strings.']
    ),
    ('struct_enum_1', 'struct_enum_2_discard'): (
        'enum with `@try_construct(discard)` rejects unrepresentable literals',
        ['Publisher uses `E1` (4 literals: VAL0-VAL3); subscriber uses `E2` (3 literals: VAL0-VAL2) with `@try_construct(discard)`. Literal `VAL3` is not in `E2`, so the sample is discarded.']
    ),
    ('struct_enum_1', 'struct_enum_2_default'): (
        'enum with `@try_construct(use_default)` replaces unrepresentable literals with default',
        ['Publisher uses `E1` (4 literals: VAL0-VAL3); subscriber uses `E2` (3 literals: VAL0-VAL2) with `@try_construct(use_default)`. Literal `VAL3` is replaced with `E2`\'s default literal (`VAL1`).']
    ),
    ('struct_enum_1', 'struct_enum_2'): (
        'enum without explicit `@try_construct` receiving unrepresentable literal',
        ['Publisher uses `E1` (4 literals: VAL0-VAL3); subscriber uses `E2` (3 literals: VAL0-VAL2) with no `@try_construct`. Default behavior (discard) applies to unrepresentable literal `VAL3`.']
    ),
    ('union_seq_int32x20', 'union_seq_int32x10_trim'): (
        'union with sequence member using `@try_construct(trim)`',
        ['Publisher union has `sequence<int32, 20>` member; subscriber has `sequence<int32, 10>` with `@try_construct(trim)`. Oversized data is trimmed.']
    ),
    ('union_seq_int32x20', 'union_seq_int32x10_discard'): (
        'union with sequence member using `@try_construct(discard)`',
        ['Publisher union has `sequence<int32, 20>` member; subscriber has `sequence<int32, 10>` with `@try_construct(discard)`. Oversized data causes discard.']
    ),
    ('union_seq_int32x20', 'union_seq_int32x10_default'): (
        'union with sequence member using `@try_construct(use_default)`',
        ['Publisher union has `sequence<int32, 20>` member; subscriber has `sequence<int32, 10>` with `@try_construct(use_default)`. Oversized data replaced with empty sequence.']
    ),
    ('union_seq_int32x20', 'union_seq_int32x10'): (
        'union with sequence member without explicit `@try_construct`',
        ['Publisher union has `sequence<int32, 20>` member; subscriber has `sequence<int32, 10>` with no `@try_construct`. Default behavior (discard) applies.']
    ),
    ('union_string20', 'union_string10_trim'): (
        'union with string member using `@try_construct(trim)`',
        ['Publisher union has `string<20>` member; subscriber has `string<10>` with `@try_construct(trim)`. Oversized strings are trimmed.']
    ),
    ('union_string20', 'union_string10_discard'): (
        'union with string member using `@try_construct(discard)`',
        ['Publisher union has `string<20>` member; subscriber has `string<10>` with `@try_construct(discard)`. Oversized strings cause discard.']
    ),
    ('union_string20', 'union_string10_default'): (
        'union with string member using `@try_construct(use_default)`',
        ['Publisher union has `string<20>` member; subscriber has `string<10>` with `@try_construct(use_default)`. Oversized strings replaced with empty string.']
    ),
    ('union_string20', 'union_string10'): (
        'union with string member without explicit `@try_construct`',
        ['Publisher union has `string<20>` member; subscriber has `string<10>` with no `@try_construct`. Default behavior (discard) applies.']
    ),
    ('union_enum_1', 'union_enum_2_discard'): (
        'union with enum member using `@try_construct(discard)`',
        ['Publisher union uses `E1` (4 literals); subscriber uses `E2` (3 literals) with `@try_construct(discard)`. Unrepresentable literal `VAL3` causes discard.']
    ),
    ('union_enum_1', 'union_enum_2_default'): (
        'union with enum member using `@try_construct(use_default)`',
        ['Publisher union uses `E1` (4 literals); subscriber uses `E2` (3 literals) with `@try_construct(use_default)`. Unrepresentable literal replaced with `E2` default (`VAL1`).']
    ),
    ('union_enum_1', 'union_enum_2'): (
        'union with enum member without explicit `@try_construct`',
        ['Publisher union uses `E1` (4 literals); subscriber uses `E2` (3 literals) with no `@try_construct`. Default behavior (discard) applies.']
    ),
    ('union_disc_enum_1', 'union_disc_enum_2_discard'): (
        'union with enum discriminator using `@try_construct(discard)` on discriminator',
        ['Publisher discriminator is `E1` (4 literals: VAL0-VAL3); subscriber discriminator is `E2` (3 literals: VAL0-VAL2) with `@try_construct(discard)`. Discriminator value `VAL3` is not representable.']
    ),
    ('union_disc_enum_1', 'union_disc_enum_2_default'): (
        'union with enum discriminator using `@try_construct(use_default)` on discriminator',
        ['Publisher discriminator is `E1` (4 literals: VAL0-VAL3); subscriber discriminator is `E2` (3 literals: VAL0-VAL2) with `@try_construct(use_default)`. Discriminator `VAL3` is replaced with `E2` default (`VAL1`).']
    ),
    ('union_disc_enum_1', 'union_disc_enum_2'): (
        'union with enum discriminator without explicit `@try_construct`',
        ['Publisher discriminator is `E1` (4 literals: VAL0-VAL3); subscriber discriminator is `E2` (3 literals: VAL0-VAL2) with no `@try_construct`. Default behavior (discard) applies.']
    ),
}

# Extensibility kinds for types relevant to extensibility tests
TYPE_EXTENSIBILITY = {
    'struct_f1': 'final', 'struct_f2': 'final',
    'struct_a1': 'appendable', 'struct_a2': 'appendable', 'struct_a3': 'appendable',
    'struct_m1': 'mutable', 'struct_m2': 'mutable', 'struct_m3': 'mutable', 'struct_m4': 'mutable',
    'struct_hashid_1': 'final', 'struct_hashid_2': 'final',
    'struct_primitives_final': 'final',
    'struct_primitives_appendable': 'appendable',
    'struct_primitives_mutable': 'mutable',
    'struct_1': 'mutable', 'struct_2': 'mutable',
    'struct_5': 'mutable', 'struct_6': 'mutable',
}

# Flags
FLAG_DESCRIPTIONS = {
    'ignore-member-names': 'ignore_member_names',
    'ignore-seq-bounds': 'ignore_seq_bounds',
    'ignore-str-bounds': 'ignore_str_bounds',
    'prevent-type-widening': 'prevent_type_widening',
    'force-type-validation': 'force_type_validation',
}


def extensibility_relevant(pub_type, sub_type, type_file):
    """Return True if extensibility annotation should be shown."""
    if type_file == 'extensibility':
        return True
    if type_file == 'primitives' and (pub_type in TYPE_EXTENSIBILITY or sub_type in TYPE_EXTENSIBILITY):
        return True
    if type_file == 'struct_names' and (pub_type in TYPE_EXTENSIBILITY or sub_type in TYPE_EXTENSIBILITY):
        return True
    return False


def extract_type_name(app_line):
    m = re.search(r'-y\s+Test::(\S+)', app_line)
    return m.group(1) if m else None


def extract_type_file(app_line, common_args=None):
    m = re.search(r'--type-file\s+(\S+)', app_line)
    if m:
        return m.group(1)
    if common_args:
        for arg in common_args:
            m = re.search(r'--type-file\s+(\S+)', arg)
            if m:
                return m.group(1)
    return None


def extract_flags(app_line):
    flags = {}
    for flag_cli, flag_name in FLAG_DESCRIPTIONS.items():
        m = re.search(rf'--{flag_cli}\s+(\S+)', app_line)
        if m:
            val = m.group(1)
            val_map = {'t': 'true', 'f': 'false', 'd': 'default'}
            flags[flag_cli] = val_map.get(val, val)
    if '--disable-type-info' in app_line:
        flags['disable-type-info'] = 'true'
    return flags


def get_expected_outcome(codes_str):
    if 'INCONSISTENT_TOPIC' in codes_str and 'OK' not in codes_str:
        return 'no_assignability'
    elif 'DATA_NOT_RECEIVED' in codes_str:
        return 'sample_rejected'
    else:
        return 'communication'


def generate_title(pub_type, sub_type, outcome, sub_flags):
    if outcome == 'communication':
        prefix = 'Communication between'
    elif outcome == 'no_assignability':
        prefix = 'No type assignability between'
    else:
        prefix = 'Type assignability between'

    if pub_type == sub_type:
        type_part = f'identical {pub_type}'
    else:
        type_part = f'{pub_type} and {sub_type}'

    if outcome == 'sample_rejected':
        type_part += ' but sample rejected'

    flag_context = []
    for flag_cli, flag_val in sub_flags.items():
        if flag_cli == 'disable-type-info':
            continue
        flag_name = FLAG_DESCRIPTIONS.get(flag_cli, flag_cli)
        flag_context.append(f'{flag_name} {flag_val}')

    if flag_context:
        return f"{prefix} {type_part} (subscriber with {', '.join(flag_context)})"
    return f"{prefix} {type_part}"


def generate_description(pub_type, sub_type, outcome, type_file, sub_flags, pub_flags, test_name):
    # Get knowledge about the type pair
    knowledge = TYPE_KNOWLEDGE.get((pub_type, sub_type))
    
    if knowledge:
        concept, delta_bullets = knowledge
        opening = f'Verifies {concept}:'
    else:
        # Fallback for primitive cross-type tests
        if outcome == 'communication':
            opening = f'Verifies communication between `{pub_type}` and `{sub_type}`:'
        elif outcome == 'no_assignability':
            opening = f'Verifies no type assignability between `{pub_type}` and `{sub_type}`:'
        else:
            opening = f'Verifies type assignability between `{pub_type}` and `{sub_type}` but sample is rejected:'
        delta_bullets = []
    
    # Generate a primitive-type delta if none exists
    if not delta_bullets and pub_type != sub_type:
        # Handle primitives pattern: struct_primitive_X vs struct_primitive_Y
        pub_prim = re.match(r'struct_primitive_(\w+)', pub_type)
        sub_prim = re.match(r'struct_primitive_(\w+)', sub_type)
        if pub_prim and sub_prim:
            pt = pub_prim.group(1)
            st = sub_prim.group(1)
            if pt == st:
                delta_bullets = [f'Both use final structs wrapping a single `{pt}` member `x1`.']
            else:
                delta_bullets = [f'Both are final structs with a single member `x1`, but publisher declares it as `{pt}` and subscriber as `{st}`. Primitive types must match exactly for assignability.']

    # Type bullets
    ext_relevant = extensibility_relevant(pub_type, sub_type, type_file)
    pub_ext = TYPE_EXTENSIBILITY.get(pub_type, '')
    sub_ext = TYPE_EXTENSIBILITY.get(sub_type, '')

    if pub_type == sub_type:
        ext_str = f' ({pub_ext})' if ext_relevant and pub_ext else ''
        type_bullets = [f'Publisher and Subscriber use `{pub_type}`{ext_str} from `{type_file}`.']
    else:
        pub_ext_str = f' ({pub_ext})' if ext_relevant and pub_ext else ''
        sub_ext_str = f' ({sub_ext})' if ext_relevant and sub_ext else ''
        type_bullets = [
            f'Publisher uses `{pub_type}`{pub_ext_str} from `{type_file}`.',
            f'Subscriber uses `{sub_type}`{sub_ext_str} from `{type_file}`.',
        ]

    # Flag bullets
    flag_bullets = []
    for flag_cli, flag_val in sub_flags.items():
        if flag_cli == 'disable-type-info':
            continue
        flag_bullets.append(f'Subscriber sets `--{flag_cli}` to `{flag_val}`.')
    
    pub_disable = pub_flags.get('disable-type-info', '') == 'true'
    sub_disable = sub_flags.get('disable-type-info', '') == 'true'
    if pub_disable and sub_disable:
        flag_bullets.append('Both endpoints set `--disable-type-info`.')

    # Extra context for force_type_validation
    extra_context = ''
    if 'force-type-validation' in sub_flags:
        val = sub_flags['force-type-validation']
        if val == 'true' and pub_disable:
            extra_context = 'With `force_type_validation` enabled and type information disabled, the subscriber cannot confirm type compatibility.'
        elif val in ('false', 'default') and pub_disable:
            extra_context = 'With `force_type_validation` disabled, the subscriber does not require type information for discovery.'

    # Test passes if
    if outcome == 'communication':
        passes = '**Test passes if:** Discovery succeeds and the subscriber receives the sample.'
    elif outcome == 'no_assignability':
        passes = '**Test passes if:** Discovery fails due to type incompatibility.'
    else:
        passes = '**Test passes if:** Discovery succeeds but the sample is not delivered.'

    # Assemble description
    lines = [opening, '']
    for tb in type_bullets:
        lines.append(f' * {tb}')
    for db in delta_bullets:
        lines.append(f' * {db}')
    for fb in flag_bullets:
        lines.append(f' * {fb}')
    if extra_context:
        lines.append(f'{extra_context}')
    lines.append(passes)

    return '\n'.join(lines)


def escape_python(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")


def format_description_multiline(desc, indent):
    desc_lines = desc.split('\n')
    base_indent = ' ' * indent
    cont_indent = ' ' * 24

    parts = []
    for dline in desc_lines:
        escaped = escape_python(dline)
        parts.append(f"'{escaped}\\n'")

    result = f"{base_indent}'description' : {parts[0]}\n"
    for p in parts[1:]:
        result += f"{cont_indent}{p}\n"
    return result.rstrip('\n')


def extract_test_context(lines, target_line_idx):
    test_name = None
    apps = []
    common_args = []
    expected_codes_str = ''

    start = max(0, target_line_idx - 30)
    for j in range(target_line_idx - 1, start - 1, -1):
        l = lines[j].strip()
        m = re.match(r"'([^']+)'\s*:\s*\{", l)
        if m:
            test_name = m.group(1)
            break

    if not test_name:
        return None

    for j in range(max(0, target_line_idx - 20), target_line_idx + 1):
        if j >= len(lines):
            continue
        l = lines[j]

        if "'common_args'" in l:
            m = re.search(r"'common_args'\s*:\s*\[(.+?)\]", l)
            if m:
                common_args = [s.strip().strip("'\"") for s in m.group(1).split(',')]

        if "'apps'" in l:
            apps_text = ''
            for k in range(j, min(j + 5, len(lines))):
                apps_text += lines[k]
                if ']' in lines[k] and k > j:
                    break
            app_matches = re.findall(r"'([^']*exe[^']*)'", apps_text)
            apps = app_matches

        if "'expected_codes'" in l:
            expected_codes_str = l

    if not apps or len(apps) < 2:
        return None

    pub_type = extract_type_name(apps[0])
    sub_type = extract_type_name(apps[1])
    type_file = extract_type_file(apps[0], common_args)

    if not pub_type or not sub_type or not type_file:
        return None

    return {
        'test_name': test_name,
        'pub_type': pub_type,
        'sub_type': sub_type,
        'type_file': type_file,
        'sub_flags': extract_flags(apps[1]),
        'pub_flags': extract_flags(apps[0]),
        'outcome': get_expected_outcome(expected_codes_str),
    }


def process_file():
    with open(FILE, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    output_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if ("'title'" in line) and not line.strip().startswith('#') and (
            "'title' : ''" in line.strip() or "'title': ''" in line.strip() or
            "No communication" in line or "Communication between int32 arrays" in line):
            test_info = extract_test_context(lines, i)
            if test_info:
                title = generate_title(
                    test_info['pub_type'], test_info['sub_type'],
                    test_info['outcome'], test_info['sub_flags']
                )
                indent = len(line) - len(line.lstrip())
                output_lines.append(f"{' ' * indent}'title' : '{escape_python(title)}',")
            else:
                output_lines.append(line)
            i += 1
            continue

        if ("'description'" in line) and not line.strip().startswith('#') and (
            "'description' : ''" in line.strip() or "'description': ''" in line.strip()):
            test_info = extract_test_context(lines, i)
            if test_info:
                desc = generate_description(
                    test_info['pub_type'], test_info['sub_type'],
                    test_info['outcome'], test_info['type_file'],
                    test_info['sub_flags'], test_info['pub_flags'],
                    test_info['test_name']
                )
                indent = len(line) - len(line.lstrip())
                formatted = format_description_multiline(desc, indent)
                output_lines.append(formatted)
            else:
                output_lines.append(line)
            i += 1
            continue

        output_lines.append(line)
        i += 1

    result = '\n'.join(output_lines)

    try:
        compile(result, FILE, 'exec')
    except SyntaxError as e:
        print(f"SYNTAX ERROR: {e}", file=sys.stderr)
        rlines = result.split('\n')
        start = max(0, e.lineno - 5)
        end = min(len(rlines), e.lineno + 5)
        for li in range(start, end):
            marker = ">>>" if li == e.lineno - 1 else "   "
            print(f"{marker} {li+1}: {rlines[li]}", file=sys.stderr)
        sys.exit(1)

    with open(FILE, 'w') as f:
        f.write(result)

    # Stats
    empty_titles = result.count("'title' : ''")
    empty_descs = result.count("'description' : ''")
    print(f"Generated descriptions. Empty titles: {empty_titles}, Empty descs: {empty_descs}")
    
    # Check for tests that got no knowledge
    missing = []
    for line in result.split('\n'):
        if "'description' :" in line and "Verifies communication between" in line:
            # Check if it's a generic fallback
            pass  # Would need more context
    
    print("Done.")


if __name__ == '__main__':
    process_file()
