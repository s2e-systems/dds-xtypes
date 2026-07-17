#!/usr/bin/env python3
"""Replace 'disc' abbreviation with 'discriminator' in description prose.

Only replaces in description bullet text (not in type names like union_disc_enum_1).
Targets patterns like: disc=, disc , disc/, (disc
"""

import re

FILE = '../../../test_suite.py'

with open(FILE, 'r') as f:
    content = f.read()

# Replace disc= with discriminator= in description strings only
# But NOT in type names (e.g., union_disc_enum_1)
# Target: "disc=" "disc " "disc/" "(disc" patterns inside quoted description strings

count = 0

def replace_disc(match):
    global count
    line = match.group(0)
    # Only process lines that are part of descriptions (contain ' * ' or 'description')
    if "' * " not in line and "'description'" not in line:
        return line
    # Replace disc= disc  disc/ (disc but NOT _disc (which is in type names)
    # Also keep "disc " when followed by a digit (e.g., "disc 0-5" as shorthand)
    original = line
    line = re.sub(r'(?<![_a-zA-Z])disc(?==|/|\)|\(|,)', 'discriminator', line)
    # disc followed by space + non-digit (e.g., "disc values" "disc order")
    line = re.sub(r'(?<![_a-zA-Z])disc(?=\s+[^0-9])', 'discriminator', line)
    if line != original:
        count += 1
    return line

result = re.sub(r'^.*$', replace_disc, content, flags=re.MULTILINE)

with open(FILE, 'w') as f:
    f.write(result)

print(f"Replaced 'disc' with 'discriminator' in {count} lines")
