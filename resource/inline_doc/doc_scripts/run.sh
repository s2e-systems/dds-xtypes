#!/bin/bash
# Regenerate all test documentation in dds-xtypes/test_suite.py
#
# This script runs all documentation generation steps in order to produce
# the final documented test_suite.py from one with empty title/description fields.
#
# Prerequisites:
#   - Python 3 available
#   - Run from within dds-xtypes/doc_scripts/
#
# Steps:
#   1. Generate titles and descriptions from type knowledge base
#   2. Add extensibility annotations to union type references
#   3. Merge standalone '\n' lines into previous line as \n\n
#   4. Replace 'disc' abbreviation with 'discriminator' in prose
#   5. Split semicolon-joined sentences into separate bullet points
#
# Usage:
#   cd dds-xtypes/doc_scripts && ./run.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON="${PYTHON:-python3}"

echo "=== Step 1: Generate descriptions ==="
$PYTHON 01_generate_descriptions.py

echo ""
echo "=== Step 2: Add union extensibility annotations ==="
$PYTHON 02_fix_union_ext.py

echo ""
echo "=== Step 3: Merge standalone newline lines ==="
$PYTHON 03_merge_newlines.py

echo ""
echo "=== Step 4: Replace 'disc' with 'discriminator' ==="
$PYTHON 04_replace_disc.py

echo ""
echo "=== Step 5: Split semicolon-joined sentences ==="
$PYTHON 05_split_semicolons.py

echo ""
echo "=== Validating Python syntax ==="
$PYTHON -c "import ast; ast.parse(open('../../../test_suite.py').read()); print('OK: test_suite.py is valid Python')"

echo ""
echo "=== Done ==="
