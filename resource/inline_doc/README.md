# Documentation Generation Scripts

These scripts generate the `title` and `description` fields for all tests in
`dds-xtypes/test_suite.py`. They are meant to be run on a file with empty
`'title': ''` and `'description': ''` fields.

## Rules

All generated documentation follows the rules in `ai_doc_rules.md`.

## Scripts (run in order)

| Script | Purpose |
|--------|---------|
| `01_generate_descriptions.py` | Fill empty title/description from type knowledge base |
| `02_fix_union_ext.py` | Add `(final)`/`(appendable)`/`(mutable)` to union type refs |
| `03_merge_newlines.py` | Merge standalone `'\n'` continuation lines into `\n\n` |
| `04_replace_disc.py` | Replace `disc` abbreviation with `discriminator` in prose |
| `05_split_semicolons.py` | Split `A; B. Conclusion` into separate bullet points |

## Usage

The scripts must be run **from within the `doc_scripts/` folder**. They target
`../../../test_suite.py` (i.e. `dds-xtypes/test_suite.py`).

```bash
cd dds-xtypes/resource/inline_doc/doc_scripts
./run.sh
```

Or with a specific Python:
```bash
cd dds-xtypes/resource/inline_doc/doc_scripts
PYTHON=/path/to/python3 ./run.sh
```
