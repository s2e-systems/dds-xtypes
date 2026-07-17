#!/usr/bin/env python3
"""Split bullet points that contain 'A; B. Conclusion' into separate bullets."""

import re
import sys

FILE = '../../../test_suite.py'

def find_conclusion_split(text):
    """Find the period that separates statement B from the conclusion.
    
    Returns index of the period, or -1 if not found.
    We look for '. ' followed by a capital letter or backtick,
    but NOT inside backticks or parentheses.
    """
    # Track backtick depth
    in_backtick = False
    paren_depth = 0
    i = 0
    while i < len(text) - 2:
        ch = text[i]
        if ch == '`':
            in_backtick = not in_backtick
        elif ch == '(' and not in_backtick:
            paren_depth += 1
        elif ch == ')' and not in_backtick:
            paren_depth -= 1
        elif ch == '.' and not in_backtick and paren_depth == 0:
            # Check if followed by space + capital letter or backtick
            if i + 1 < len(text) and text[i+1] == ' ':
                if i + 2 < len(text) and (text[i+2].isupper() or text[i+2] == '`'):
                    return i
        i += 1
    return -1


def find_first_semicolon(text):
    """Find the first '; ' that's not inside backticks or parentheses."""
    in_backtick = False
    paren_depth = 0
    i = 0
    while i < len(text) - 1:
        ch = text[i]
        if ch == '`':
            in_backtick = not in_backtick
        elif ch == '(' and not in_backtick:
            paren_depth += 1
        elif ch == ')' and not in_backtick:
            paren_depth -= 1
        elif ch == ';' and not in_backtick and paren_depth == 0:
            if i + 1 < len(text) and text[i+1] == ' ':
                return i
        i += 1
    return -1


def process_line(line):
    """Process a single bullet line. Returns list of new lines or None if no change."""
    # Match bullet lines: '                        ' * ...\n'
    m = re.match(r"^(\s+)(' \* )(.+\\n')$", line)
    if not m:
        return None
    
    indent = m.group(1)
    bullet_prefix = m.group(2)
    content = m.group(3)  # everything after ' * ' and before the trailing quote
    
    # Remove the trailing \n' to work with raw text
    if content.endswith("\\n'"):
        content = content[:-3]
    else:
        return None
    
    # Find first semicolon
    semi_idx = find_first_semicolon(content)
    if semi_idx == -1:
        return None
    
    part_a = content[:semi_idx]
    rest = content[semi_idx + 2:]  # skip '; '
    
    # Find conclusion split in rest
    conclusion_idx = find_conclusion_split(rest)
    if conclusion_idx == -1:
        # 2-part split: "A; B" with no separate conclusion
        part_b = rest
        # Capitalize first letter of part_b
        if part_b and part_b[0].islower():
            part_b = part_b[0].upper() + part_b[1:]
        
        part_a_end = '.' if not part_a.endswith('.') else ''
        # part_b already ends with period (from original line ending)
        part_b_end = '' if part_b.endswith('.') else '.'
        
        new_lines = [
            f"{indent}' * {part_a}{part_a_end}\\n'\n",
            f"{indent}' * {part_b}{part_b_end}\\n'\n",
        ]
        return new_lines
    
    part_b = rest[:conclusion_idx]
    conclusion = rest[conclusion_idx + 2:]  # skip '. '
    
    # Capitalize first letter of part_b and conclusion
    if part_b and part_b[0].islower():
        part_b = part_b[0].upper() + part_b[1:]
    
    # Build new lines - add period to part_a and part_b if they don't have one
    part_a_end = '.' if not part_a.endswith('.') else ''
    part_b_end = '.' if not part_b.endswith('.') else ''
    # Conclusion already ends with period typically
    conclusion_end = '' if conclusion.endswith('.') else '.'
    
    new_lines = [
        f"{indent}' * {part_a}{part_a_end}\\n'\n",
        f"{indent}' * {part_b}{part_b_end}\\n'\n",
        f"{indent}' * {conclusion}{conclusion_end}\\n'\n",
    ]
    
    return new_lines


def main():
    dry_run = '--dry-run' in sys.argv
    
    with open(FILE, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    changes = 0
    
    for i, line in enumerate(lines):
        # Only process bullet lines in descriptions
        stripped = line.strip()
        if not stripped.startswith("' * "):
            new_lines.append(line)
            continue
        
        # Skip "Publisher and Subscriber use" lines (identical type, single bullet)
        if 'Publisher and Subscriber' in line:
            new_lines.append(line)
            continue
            
        # Check if this line has a semicolon pattern
        if '; ' not in line:
            new_lines.append(line)
            continue
        
        result = process_line(line.rstrip('\n'))
        if result is None:
            new_lines.append(line)
            continue
        
        changes += 1
        if dry_run:
            print(f"Line {i+1}: {line.rstrip()}")
            print(f"  -> Split into {len(result)} bullets:")
            for r in result:
                print(f"     {r.rstrip()}")
            print()
        
        new_lines.extend(result)
    
    if dry_run:
        print(f"\nTotal changes: {changes}")
    else:
        with open(FILE, 'w') as f:
            f.writelines(new_lines)
        print(f"Applied {changes} splits")


if __name__ == '__main__':
    main()
