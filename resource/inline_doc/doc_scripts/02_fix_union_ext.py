import re

# Map union names to extensibility from the XML
# Default extensibility in DDS is APPENDABLE when not specified
UNION_EXT = {
    'union_primitives_final': 'final',
    'union_primitives_appendable': 'appendable',
    'union_primitives_mutable': 'mutable',
    'union_uint32': 'appendable',
    'union_1': 'appendable',
    'union_2': 'appendable',
    'union_3': 'appendable',
    'union_4': 'appendable',
    'union_5': 'appendable',
    'union_6': 'appendable',
    'union_int16': 'appendable',
    'union_int32': 'appendable',
    'union_int32_default': 'appendable',
    'union_int16_default': 'appendable',
    'union_final_5': 'final',
    'union_final_5_default': 'final',
    'union_final_6': 'final',
    'union_appendable_a': 'appendable',
    'union_appendable_b': 'appendable',
    'union_appendable_c': 'appendable',
    'union_appendable_a_default': 'appendable',
    'union_appendable_b_default': 'appendable',
    'union_mutable_a': 'mutable',
    'union_mutable_b': 'mutable',
    'union_mutable_c': 'mutable',
    'union_mutable_a_default': 'mutable',
    'union_mutable_b_default': 'mutable',
    'union_bitmask32': 'appendable',
    'union_bitmask16': 'appendable',
    'union_uint32_key': 'appendable',
}

with open('../../../test_suite.py', 'r') as f:
    content = f.read()

count = 0
# Sort by longest name first to avoid partial matches (e.g. union_int32 matching inside union_int32_default)
for name in sorted(UNION_EXT.keys(), key=len, reverse=True):
    ext = UNION_EXT[name]
    # Match `union_NAME` from `unions` but NOT already followed by (ext)
    # Use word boundary after the name to avoid partial matches
    old_pattern = '`' + name + '` from `unions'
    already_done = '`' + name + '` (' + ext + ') from `unions'
    
    if already_done in content:
        continue
    
    if old_pattern in content:
        new_text = '`' + name + '` (' + ext + ') from `unions'
        replacements = content.count(old_pattern)
        content = content.replace(old_pattern, new_text)
        count += replacements
        print(f"  {name}: +{replacements} annotations")

with open('../../../test_suite.py', 'w') as f:
    f.write(content)

print(f"\nTotal: Added extensibility to {count} union type references")
