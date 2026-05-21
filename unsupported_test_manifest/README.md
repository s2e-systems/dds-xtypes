# Unsupported-test manifests

This folder contains plain-text manifest files that list test IDs which a
specific DDS implementation does not support. `interoperability_report.py`
automatically looks up a manifest for each executable — no command-line flag
is needed.

## Auto-detection

The script derives the product name from the executable path using the same
logic that produces the report name (everything before `_test`, `_shape`, etc.,
keeping only the last path component). It then looks for:

```
unsupported_test_manifest/<product_name>.txt
```

If a manifest file is not found, the product is assumed to support all tests
and the file is silently ignored.

Example: for `--pub-exe ./executables/connext_dds-7.7.0_test_main_linux`
the script looks for `unsupported_test_manifest/connext_dds-7.7.0.txt`.

## File format

* One test ID per line.
* A test ID is `<dict_name>_<test_case_name>`, matching the name in the JUnit
  XML report. Example: `xtypes_v2_extensibility_test_suite_ext_final_struct_1`
* Blank lines and lines beginning with `#` are ignored.

## Naming convention

```
unsupported_test_manifest/
    connext_dds-7.7.0.txt
    opendds-3.28.txt
    fastdds-3.1.txt
```

## Usage example

```bash
python interoperability_report.py \
    --pub-exe ./executables/connext_dds-7.7.0_test_main_linux \
    --sub-exe ./executables/toc_coredx_dds-6.14.0_test_main_linux
# manifests connext_dds-7.7.0.txt and toc_coredx_dds-6.14.0.txt
# are picked up automatically if they exist.
```

Tests listed in a manifest are added to the report as **NOT SUPPORTED** (with
`PUB_UNSUPPORTED_FEATURE` or `SUB_UNSUPPORTED_FEATURE` in the failure message)
without running the actual test application.
