import re

with open('../../../test_suite.py', 'r') as f:
    lines = f.readlines()

new_lines = []
count = 0
i = 0
while i < len(lines):
    # Check if this line is a standalone '\n' continuation
    stripped = lines[i].rstrip('\n')
    if stripped == "                        '\\n'":
        # Merge with previous line: previous line should end with \n'
        # Replace the trailing \n' with \n\n' and skip this line
        if new_lines:
            prev = new_lines[-1].rstrip('\n')
            if prev.endswith("\\n'"):
                # Replace trailing \n' with \n\n'
                new_lines[-1] = prev[:-3] + "\\n\\n'\n"
                count += 1
                i += 1
                continue
    new_lines.append(lines[i])
    i += 1

with open('../../../test_suite.py', 'w') as f:
    f.writelines(new_lines)

print(f"Merged {count} standalone '\\n' lines")
