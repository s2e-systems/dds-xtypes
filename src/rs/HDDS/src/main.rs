// SPDX-License-Identifier: Apache-2.0 OR MIT
// Copyright (c) 2025-2026 naskel.com

//! HDDS OMG DDS-XTypes interoperability test application.
//!
//! Implements the OMG dds-xtypes interoperability test driver protocol:
//!   - Publisher (-P): load type from XML, load data from XML, publish on loop
//!   - Subscriber (-S): receive, decode with type from XML, compare to expected data
//!
//! Arg conventions match the OMG test_suite.py expectations:
//!   -d <domain>  -t <topic>  -y <type_name>
//!   --type-folder <dir>  --type-file <file>
//!   --data-folder <dir>  --data-file <file>
//!   -P / -S
//!   -r <reliability>  -D <durability>  -x <xcdr_version>
//!
//! Behavior flags propagated by the OMG test_suite.py (each takes t/f/d for
//! true / false / default - "default" leaves the implementation's native
//! behavior in place):
//!   --ignore-member-names <t|f|d>
//!   --ignore-seq-bounds   <t|f|d>
//!   --ignore-str-bounds   <t|f|d>
//!   --prevent-type-widening <t|f|d>
//!   --check-member-names  <t|f|d>
//!   --check-seq-bounds    <t|f|d>
//!   --check-str-bounds    <t|f|d>
//!   --force-type-validation <t|f|d>
//!   --disable-type-info       (bare flag)

mod cdr_compat;
mod data_loader;
mod xml_loader;

use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::time::Duration;

use hdds::dynamic::{
    decode_dynamic_with_version, encode_dynamic_with_version, type_descriptor_to_xtypes,
    type_descriptor_to_xtypes_complete, DynamicData, Extensibility,
};
use hdds::CdrVersion;
use hdds::dds::listener::{
    DataReaderListener, DataWriterListener, InconsistentTopicStatus, PublicationMatchedStatus,
    RequestedIncompatibleQosStatus, SubscriptionMatchedStatus,
};
use hdds::{DdsTrait, Participant, QoS, TransportMode, TypeConsistencyEnforcement};

// ---------------------------------------------------------------------------
// OMG harness listener strings (verbatim from interoperability_report.py)
//
// Publisher step 4 (pexpect.expect list):
//   index 0: 'on_publication_matched()'      -> READER_MATCHED (success)
//   index 1: 'on_offered_incompatible_qos'   -> INCOMPATIBLE_QOS  (no parens)
//   index 2: 'on_inconsistent_topic'         -> INCONSISTENT_TOPIC
//
// Subscriber step 4 (pexpect.expect list):
//   index 0: r'\[[0-9]+\]'                   -> success (sample or matched line)
//   index 1: 'on_requested_incompatible_qos()' -> INCOMPATIBLE_QOS
//   index 2: 'on_requested_deadline_missed()' -> DEADLINE_MISSED
//   index 3: 'sample_received()'             -> success (handled by existing code)
//   index 4: 'on_inconsistent_topic'         -> INCONSISTENT_TOPIC
// ---------------------------------------------------------------------------

/// Writer-side OMG listener: prints strings the harness regex matches on stdout.
struct XtypesWriterListener;

impl XtypesWriterListener {
    fn new() -> Self {
        XtypesWriterListener
    }
}

impl<T: DdsTrait> DataWriterListener<T> for XtypesWriterListener {
    // Called when a DataReader with compatible QoS is found.
    // Harness pattern (pub step 4, index 0): 'on_publication_matched()'
    fn on_publication_matched(&self, status: PublicationMatchedStatus) {
        println!(
            "on_publication_matched() current_count={}",
            status.current_count
        );
    }

    // Called when a DataReader with incompatible QoS is found.
    // Harness pattern (pub step 4, index 1): 'on_offered_incompatible_qos'
    // Note: the harness substring has no trailing '()' — the longer form still
    // satisfies a substring match.
    fn on_offered_incompatible_qos(&self, policy_id: u32, policy_name: &str) {
        println!(
            "on_offered_incompatible_qos() policy_id={} policy={}",
            policy_id, policy_name
        );
    }

    // Called when a remote DataReader on the same topic announces a type that
    // is structurally incompatible with the local writer's type.
    // Harness pattern (pub step 4, index 2): 'on_inconsistent_topic'
    fn on_inconsistent_topic(&self, status: InconsistentTopicStatus) {
        println!("on_inconsistent_topic total_count={}", status.total_count);
    }
}

/// Reader-side OMG listener: prints strings the harness regex matches on stdout.
struct XtypesReaderListener;

impl XtypesReaderListener {
    fn new() -> Self {
        XtypesReaderListener
    }
}

impl<T: DdsTrait> DataReaderListener<T> for XtypesReaderListener {
    // Called when a DataWriter with compatible QoS is found.
    // Harness does not key on 'on_subscription_matched()' for the success path
    // (it keys on sample data '[N]'), but printing it aids debugging and may
    // satisfy future harness versions that reference the DDS-RTPS spec string.
    fn on_subscription_matched(&self, status: SubscriptionMatchedStatus) {
        println!(
            "on_subscription_matched() current_count={}",
            status.current_count
        );
    }

    // Called when a DataWriter with incompatible QoS is found.
    // Harness pattern (sub step 4, index 1): 'on_requested_incompatible_qos()'
    fn on_requested_incompatible_qos(&self, status: RequestedIncompatibleQosStatus) {
        println!(
            "on_requested_incompatible_qos() total_count={} last_policy_id={}",
            status.total_count, status.last_policy_id
        );
    }

    // Called when a remote DataWriter on the same topic announces a type that
    // is structurally incompatible with the local reader's type.
    // Harness pattern (sub step 4, index 4): 'on_inconsistent_topic'
    fn on_inconsistent_topic(&self, status: InconsistentTopicStatus) {
        println!("on_inconsistent_topic total_count={}", status.total_count);
    }
}

use data_loader::{compare_dynamic_data, load_data_from_xml};
use xml_loader::load_type_from_xml;

// ---------------------------------------------------------------------------
// Exit codes
// ---------------------------------------------------------------------------

const EXIT_OK: i32 = 0;
const EXIT_USAGE: i32 = 1;
const EXIT_PARTICIPANT: i32 = 2;
const EXIT_DATA: i32 = 3;
const EXIT_UNSUPPORTED: i32 = 4;

// ---------------------------------------------------------------------------
// Signal handling (async-signal-safe via signal-hook)
// ---------------------------------------------------------------------------

static ALL_DONE: AtomicBool = AtomicBool::new(false);

fn install_signal_handlers() -> Result<(), String> {
    // signal-hook installs an async-signal-safe handler. The store on
    // ALL_DONE is the only thing executed on the signal path. We register
    // the same callback for SIGINT and SIGTERM so the binary exits cleanly
    // under `pkill` / Ctrl-C from the OMG harness.
    unsafe {
        register_signal(signal_hook::consts::SIGINT)?;
        register_signal(signal_hook::consts::SIGTERM)?;
    }
    Ok(())
}

unsafe fn register_signal(sig: i32) -> Result<(), String> {
    signal_hook::low_level::register(sig, || {
        ALL_DONE.store(true, Ordering::SeqCst);
    })
    .map(|_| ())
    .map_err(|e| format!("low_level register({}) failed: {}", sig, e))
}

// ---------------------------------------------------------------------------
// CLI args
// ---------------------------------------------------------------------------

/// Tri-state for OMG t/f/d flags.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum TriState {
    /// Vendor implementation default - we don't change behavior.
    Default,
    True,
    False,
}

impl TriState {
    fn parse(s: &str) -> Result<Self, String> {
        match s.to_lowercase().as_str() {
            "t" | "true" | "1" => Ok(TriState::True),
            "f" | "false" | "0" => Ok(TriState::False),
            "d" | "default" => Ok(TriState::Default),
            _ => Err(format!("expected t/f/d, got '{}'", s)),
        }
    }
}

#[derive(Debug)]
struct Options {
    domain_id: u32,
    domain_id_from_cli: bool,
    topic_name: String,
    type_name: String,
    type_folder: Option<String>,
    type_file: Option<String>,
    data_folder: Option<String>,
    data_file: Option<String>,
    publish: bool,
    subscribe: bool,
    reliability: String,
    durability: String,
    xcdr_version: u8,
    print_writer_samples: bool,
    verbose: bool,
    // OMG behavior switches - currently captured for diagnostics only.
    // None of these change HDDS wire behavior yet; binary fails hard when a
    // test asks for behavior we don't implement (see `enforce_unsupported`).
    //
    // explicit_ignore_member_names: set when --ignore-member-names is present on
    // the command line even if the value is 'd' (Default). This lets
    // build_type_consistency() distinguish "user said d = spec default
    // = ignore_member_names=false" from "user never mentioned the flag = use
    // the permissive implementation default = ignore_member_names=true".
    explicit_ignore_member_names: bool,
    ignore_member_names: TriState,
    ignore_seq_bounds: TriState,
    ignore_str_bounds: TriState,
    prevent_type_widening: TriState,
    check_member_names: TriState,
    check_seq_bounds: TriState,
    check_str_bounds: TriState,
    force_type_validation: TriState,
    disable_type_info: bool,
    type_object_version: u8,
    // When set, print the TypeObject equivalence hash(es) to stdout and exit
    // without creating a Participant (OMG dds-xtypes "typeid" test mode).
    print_typeid: bool,
}

impl Default for Options {
    fn default() -> Self {
        Self {
            domain_id: 0,
            domain_id_from_cli: false,
            topic_name: String::new(),
            type_name: String::new(),
            type_folder: None,
            type_file: None,
            data_folder: None,
            data_file: None,
            publish: false,
            subscribe: false,
            reliability: "reliable".to_string(),
            durability: "volatile".to_string(),
            xcdr_version: 2,
            print_writer_samples: false,
            verbose: false,
            explicit_ignore_member_names: false,
            ignore_member_names: TriState::Default,
            ignore_seq_bounds: TriState::Default,
            ignore_str_bounds: TriState::Default,
            prevent_type_widening: TriState::Default,
            check_member_names: TriState::Default,
            check_seq_bounds: TriState::Default,
            check_str_bounds: TriState::Default,
            force_type_validation: TriState::Default,
            disable_type_info: false,
            type_object_version: 2,
            print_typeid: false,
        }
    }
}

/// Helper: fetch the next argv and advance index. Reports a clear usage
/// error if the value is missing.
fn next_arg(args: &[String], i: &mut usize, flag: &str) -> Result<String, String> {
    *i += 1;
    args.get(*i)
        .cloned()
        .ok_or_else(|| format!("missing value for {}", flag))
}

fn parse_args(args: &[String]) -> Result<Options, String> {
    let mut opts = Options::default();
    let mut i = 1usize;
    while i < args.len() {
        let arg = args[i].as_str();
        match arg {
            "-d" => {
                let v = next_arg(args, &mut i, "-d")?;
                opts.domain_id = v.parse::<u32>().map_err(|e| format!("-d: {}", e))?;
                opts.domain_id_from_cli = true;
            }
            "-t" => opts.topic_name = next_arg(args, &mut i, "-t")?,
            "-y" => opts.type_name = next_arg(args, &mut i, "-y")?,
            "--type-folder" => opts.type_folder = Some(next_arg(args, &mut i, "--type-folder")?),
            "--type-file" => opts.type_file = Some(next_arg(args, &mut i, "--type-file")?),
            "--data-folder" => opts.data_folder = Some(next_arg(args, &mut i, "--data-folder")?),
            "--data-file" => opts.data_file = Some(next_arg(args, &mut i, "--data-file")?),
            "-P" => opts.publish = true,
            "-S" => opts.subscribe = true,
            "-r" => opts.reliability = next_arg(args, &mut i, "-r")?.to_lowercase(),
            "-D" => opts.durability = next_arg(args, &mut i, "-D")?.to_lowercase(),
            "-x" => {
                let v = next_arg(args, &mut i, "-x")?;
                opts.xcdr_version = v.parse::<u8>().map_err(|e| format!("-x: {}", e))?;
            }
            "-w" => opts.print_writer_samples = true,
            "-v" => opts.verbose = true,
            // OMG tri-state behavior flags.
            "--ignore-member-names" => {
                opts.ignore_member_names = TriState::parse(&next_arg(args, &mut i, arg)?)?;
                opts.explicit_ignore_member_names = true;
            }
            "--ignore-seq-bounds" => {
                opts.ignore_seq_bounds = TriState::parse(&next_arg(args, &mut i, arg)?)?;
            }
            "--ignore-str-bounds" => {
                opts.ignore_str_bounds = TriState::parse(&next_arg(args, &mut i, arg)?)?;
            }
            "--prevent-type-widening" => {
                opts.prevent_type_widening = TriState::parse(&next_arg(args, &mut i, arg)?)?;
            }
            "--check-member-names" => {
                opts.check_member_names = TriState::parse(&next_arg(args, &mut i, arg)?)?;
            }
            "--check-seq-bounds" => {
                opts.check_seq_bounds = TriState::parse(&next_arg(args, &mut i, arg)?)?;
            }
            "--check-str-bounds" => {
                opts.check_str_bounds = TriState::parse(&next_arg(args, &mut i, arg)?)?;
            }
            "--force-type-validation" => {
                opts.force_type_validation = TriState::parse(&next_arg(args, &mut i, arg)?)?;
            }
            "--disable-type-info" => opts.disable_type_info = true,
            "--print-typeid" => opts.print_typeid = true,
            "--type-object-version" => {
                let v = next_arg(args, &mut i, "--type-object-version")?;
                opts.type_object_version = v
                    .parse::<u8>()
                    .map_err(|e| format!("--type-object-version: {}", e))?;
            }
            "-h" | "--help" => {
                print_help();
                std::process::exit(EXIT_OK);
            }
            s => {
                return Err(format!(
                    "unknown argument '{}' (use --help to list supported flags)",
                    s
                ));
            }
        }
        i += 1;
    }
    Ok(opts)
}

fn print_help() {
    println!(
        "Usage: hdds_xtypes_shape_main_linux [OPTIONS] -P|-S\n\
\n\
Required:\n\
  -P                          Publisher mode\n\
  -S                          Subscriber mode\n\
  -t <topic>                  DDS topic name\n\
  -y <type>                   Fully qualified type name (e.g. Test::struct_f1)\n\
  --type-folder <dir>         Folder containing types/xml/<name>.xml\n\
  --type-file <name>          Type XML file basename (without .xml)\n\
\n\
Optional:\n\
  -d <id>                     DDS domain id (default 0)\n\
  -r <reliable|best_effort>   Reliability QoS (default reliable)\n\
  -D <volatile|transient_local|persistent>   Durability QoS (default volatile)\n\
  -x <1|2>                    XCDR version (default 2)\n\
  -w                          Print sample on every write\n\
  -v                          Verbose logging\n\
  --data-folder <dir>         Folder containing data/xml/<name>.xml\n\
  --data-file <name>          Data XML file basename (without .xml)\n\
\n\
OMG behavior flags (t=true, f=false, d=vendor default):\n\
  --ignore-member-names <t|f|d>\n\
  --ignore-seq-bounds   <t|f|d>\n\
  --ignore-str-bounds   <t|f|d>\n\
  --prevent-type-widening <t|f|d>\n\
  --check-member-names  <t|f|d>\n\
  --check-seq-bounds    <t|f|d>\n\
  --check-str-bounds    <t|f|d>\n\
  --force-type-validation <t|f|d>\n\
  --disable-type-info\n\
\n\
TypeObject hash mode:\n\
  --print-typeid              Print TypeObject equivalence hash(es) and exit\n\
  --type-object-version <1|2> Hash version (default 2; V1 vendor-specific)\n\
\n\
Environment:\n\
  HDDS_DOMAIN_ID              Override domain id (only when -d is not given)\n"
    );
}

/// Warn when the OMG harness passes behavior switches that are only partially
/// implemented. The switches are now wired into `TypeConsistencyEnforcement`
/// and propagated via SEDP `PID_TYPE_CONSISTENCY_ENFORCEMENT` (0x0074) so
/// that remote endpoints receive the declared coercion policy. However, the
/// local assignability checks in `is_assignable_to` / `is_type_compatible`
/// do not yet branch on these flags at match time — tests that depend on
/// HDDS changing its own local matching behavior based on the flags may still
/// fail. Tests where the flag value matches the spec default (no-op) should
/// pass. `--disable-type-info` is not yet plumbed at all.
fn enforce_unsupported(opts: &Options) {
    // Only flag switches whose local-matching semantics are unimplemented.
    // The SEDP wire emission is handled via build_type_consistency(); the
    // remaining gap is that HDDS does not alter its own matcher decisions
    // based on the received/local TypeConsistencyEnforcement policy.
    let partial_wire_only: &[&str] = &[
        // Wire-emitted correctly but local matcher ignores:
    ];
    let _ = partial_wire_only; // for future use

    // disable-type-info: suppresses TypeObject emission in SEDP; now implemented.
    // No warning needed — run_publisher/run_subscriber pass None for type_object.
}

// ---------------------------------------------------------------------------
// QoS mapping
// ---------------------------------------------------------------------------

/// Derive a `TypeConsistencyEnforcement` policy from the OMG harness CLI flags.
///
/// Maps `TriState` values to the DDS-XTypes §7.6.3.4 fields.
///
/// Distinction between "no flag" and "--ignore-member-names d":
///   - No flag at all: use HDDS permissive default (ignore_member_names=true).
///     Returns None; the SEDP builder emits the wire default bytes
///     (ignore_member_names=true). Peer sees permissive behavior.
///   - "--ignore-member-names d" (opts.explicit_ignore_member_names=true,
///     value=Default): user requested the spec strict default
///     (ignore_member_names=false per XTypes §7.6.3.4). Emits a PID with
///     ignore_member_names=false so peers correctly apply name enforcement.
///
/// This distinction is why opts.explicit_ignore_member_names is checked
/// separately from opts.ignore_member_names != TriState::Default.
fn build_type_consistency(opts: &Options) -> Option<TypeConsistencyEnforcement> {
    // Resolve each flag: Default -> spec default, True/False -> override.
    let ignore_sequence_bounds = match opts.ignore_seq_bounds {
        TriState::True => true,
        TriState::False => false,
        TriState::Default => true, // spec default
    };
    let ignore_string_bounds = match opts.ignore_str_bounds {
        TriState::True => true,
        TriState::False => false,
        TriState::Default => true, // spec default
    };
    let ignore_member_names = match opts.ignore_member_names {
        TriState::True => true,
        TriState::False => false,
        TriState::Default => false, // spec default per XTypes §7.6.3.4
    };
    let prevent_type_widening = match opts.prevent_type_widening {
        TriState::True => true,
        TriState::False => false,
        TriState::Default => false, // spec default
    };
    let force_type_validation = match opts.force_type_validation {
        TriState::True => true,
        TriState::False => false,
        TriState::Default => false, // spec default
    };

    // Check flags are non-default; also honour check_* flags which are the
    // inverse semantics of ignore_*: check_seq_bounds=true <-> ignore_seq_bounds=false.
    // explicit_ignore_member_names triggers policy emission even when the value
    // is Default, so peers receive ignore_member_names=false (spec strict default).
    let any_explicit = opts.explicit_ignore_member_names
        || opts.ignore_seq_bounds != TriState::Default
        || opts.ignore_str_bounds != TriState::Default
        || opts.ignore_member_names != TriState::Default
        || opts.prevent_type_widening != TriState::Default
        || opts.force_type_validation != TriState::Default
        || opts.check_seq_bounds != TriState::Default
        || opts.check_str_bounds != TriState::Default
        || opts.check_member_names != TriState::Default;

    if !any_explicit {
        return None;
    }

    // Resolve --check-* flags: check_seq_bounds=t -> ignore_sequence_bounds=false.
    let ignore_sequence_bounds = if opts.check_seq_bounds == TriState::True {
        false
    } else {
        ignore_sequence_bounds
    };
    let ignore_string_bounds = if opts.check_str_bounds == TriState::True {
        false
    } else {
        ignore_string_bounds
    };
    let ignore_member_names = if opts.check_member_names == TriState::True {
        false
    } else {
        ignore_member_names
    };

    // kind: DISALLOW_TYPE_COERCION when ignore_seq+str are both false AND
    // prevent_type_widening is true; otherwise ALLOW_TYPE_COERCION.
    let kind: u16 = if !ignore_sequence_bounds && !ignore_string_bounds && !ignore_member_names
        && prevent_type_widening
    {
        0 // DISALLOW_TYPE_COERCION
    } else {
        1 // ALLOW_TYPE_COERCION
    };

    Some(TypeConsistencyEnforcement {
        kind,
        ignore_sequence_bounds,
        ignore_string_bounds,
        ignore_member_names,
        prevent_type_widening,
        force_type_validation,
    })
}

/// Build the DDS QoS used by writer and reader.
///
/// Defaults (matching the OMG reference C++ binary `test_main.cxx`
/// `TestOptions()` constructor at /tmp/dds-xtypes-recon/src/cxx/test_main.cxx
/// lines 290-294):
///
/// - Reliability = RELIABLE  (overridable via `-r best_effort`)
/// - Durability  = VOLATILE  (overridable via `-D transient_local|...`)
/// - DataRepresentation explicit list derived from `-x`. The OMG harness
///   `interoperability_report.py` always injects `-x <1|2>` (default "2",
///   line 778) when the test case does not set it, so this field is
///   effectively never empty in a harness run. Setting it explicitly here
///   makes HDDS' SEDP `PID_DATA_REPRESENTATION` carry the exact list every
///   peer expects.
/// Map the harness `-x` flag to the CDR version used by the dynamic codec.
/// The harness always injects `-x <1|2>` (default 2); both peers of a test
/// case get the same value, so encode and decode agree.
fn cdr_version_of(opts: &Options) -> CdrVersion {
    if opts.xcdr_version == 1 {
        CdrVersion::Xcdr1
    } else {
        CdrVersion::Xcdr2
    }
}

fn build_qos(opts: &Options) -> QoS {
    let base = match opts.reliability.as_str() {
        "best_effort" | "besteffort" | "be" => QoS::best_effort(),
        _ => QoS::reliable(),
    };

    let with_durability = match opts.durability.as_str() {
        "transient_local" | "transientlocal" | "tl" => base.transient_local(),
        "transient" => base.transient_local(),
        "persistent" => base.transient_local(),
        _ => base.volatile(),
    };

    // Pin DataRepresentation so the SEDP PID matches the encapsulation byte
    // the ENGINE prepends inside write_raw (the driver passes bare CDR).
    // Without this, HDDS' RTI dialect emits PID_DATA_REPRESENTATION =
    // [XCDR2] only (see hdds protocol/dialect/rti/sedp/metadata.rs
    // write_data_representation) regardless of `-x 1`, which would silently
    // disagree with the wire encapsulation when the user asks for XCDR1.
    let with_repr = match opts.xcdr_version {
        1 => with_durability.data_representation_xcdr1(),
        _ => with_durability.data_representation_xcdr2(),
    };

    // Wire the TypeConsistencyEnforcementQosPolicy derived from the OMG
    // harness CLI flags into the QoS so SEDP propagates the caller's intent.
    let mut qos = with_repr;
    qos.type_consistency = build_type_consistency(opts);
    qos
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

/// Print the TypeObject equivalence hash(es) for a type and exit (OMG
/// dds-xtypes "typeid" test mode).
///
/// V2 prints the Minimal and Complete TypeObject equivalence hashes (MD5 of the
/// CDR2-serialised TypeObject truncated to 14 bytes, per XTypes v1.3 §7.3.4.8),
/// lowercase hex, matching the reference vendor output format exactly:
///   `Minimal Type Object V2 - Equivalence Hash: <28 hex>`
///   `Complete Type Object V2 - Equivalence Hash: <28 hex>`
///
/// V1 TypeIdentifiers are vendor-specific (different vendors emit different
/// uint64 for the same type) and are manifest-excluded for HDDS, so V1 prints a
/// single placeholder line and is documented as unsupported.
fn print_typeid_and_exit(type_desc: &Arc<hdds::dynamic::TypeDescriptor>, version: u8) -> ! {
    let cto = match type_descriptor_to_xtypes(type_desc) {
        Some(c) => c,
        None => {
            eprintln!("ERROR: cannot build CompleteTypeObject");
            std::process::exit(EXIT_DATA);
        }
    };
    if version == 1 {
        // V1 Type ID is vendor-specific and manifest-excluded for HDDS.
        println!("Type Object V1 - Type ID: 0");
        std::process::exit(EXIT_OK);
    }
    // DEBUG-ONLY falsification path: when HDDS_TYPEID_DEBUG is set, dump the raw
    // inner CDR2-LE bytes (no outer TypeObject union wrapper) so candidate
    // wrappings can be MD5-tested against reference hashes offline.
    if std::env::var_os("HDDS_TYPEID_DEBUG").is_some() {
        if let Some((c_bytes, m_bytes)) = hdds::dynamic::debug_type_object_inner_cdr2(&cto) {
            let hex = |b: &[u8]| b.iter().map(|x| format!("{:02x}", x)).collect::<String>();
            eprintln!("DEBUG inner CDR2 complete len={} hex={}", c_bytes.len(), hex(&c_bytes));
            eprintln!("DEBUG inner CDR2 minimal  len={} hex={}", m_bytes.len(), hex(&m_bytes));
        } else {
            eprintln!("DEBUG inner CDR2: unavailable for this type variant");
        }
    }
    // Minimal hash is derived from the Minimal-reference CompleteTypeObject
    // (`cto`). The Complete hash must come from a CompleteTypeObject whose
    // hash-based members (enums, nested-struct collection elements) are
    // referenced by their Complete equivalence hash, per DDS-XTypes v1.3
    // §7.3.4.5 / §7.3.4.8.
    let cto_complete = match type_descriptor_to_xtypes_complete(type_desc) {
        Some(c) => c,
        None => {
            eprintln!("ERROR: cannot build Complete CompleteTypeObject");
            std::process::exit(EXIT_DATA);
        }
    };
    let complete = cto_complete.compute_equivalence_hash();
    let minimal = hdds::dynamic::complete_type_object_minimal_hash(&cto);
    match (minimal, complete) {
        (Some(m), Ok(c)) => {
            println!("Minimal Type Object V2 - Equivalence Hash: {}", m);
            println!("Complete Type Object V2 - Equivalence Hash: {}", c);
            std::process::exit(EXIT_OK);
        }
        _ => {
            eprintln!("ERROR: cannot compute equivalence hash");
            std::process::exit(EXIT_DATA);
        }
    }
}

fn main() {
    let _ = env_logger::try_init();
    if let Err(e) = install_signal_handlers() {
        eprintln!("ERROR: {}", e);
        std::process::exit(EXIT_PARTICIPANT);
    }

    let args: Vec<String> = std::env::args().collect();
    let opts = match parse_args(&args) {
        Ok(o) => o,
        Err(e) => {
            eprintln!("ERROR: {}", e);
            std::process::exit(EXIT_USAGE);
        }
    };

    // OMG dds-xtypes "typeid" test mode: print the TypeObject equivalence
    // hash(es) for the requested type and exit. This path does NOT require -t
    // (topic) nor -P/-S (role) and never creates a Participant; it only needs
    // the type loaded from XML (-y plus --type-folder/--type-file).
    if opts.print_typeid {
        if opts.type_name.is_empty() {
            eprintln!("ERROR: type name (-y) required for --print-typeid");
            std::process::exit(EXIT_USAGE);
        }
        let type_xml_path = match (&opts.type_folder, &opts.type_file) {
            (Some(folder), Some(file)) => format!("{}/xml/{}.xml", folder, file),
            _ => {
                eprintln!("ERROR: --type-folder and --type-file are required");
                std::process::exit(EXIT_USAGE);
            }
        };
        let type_desc = match load_type_from_xml(&type_xml_path, &opts.type_name) {
            Ok(td) => Arc::new(td),
            Err(e) => {
                eprintln!(
                    "ERROR loading type '{}' from '{}': {}",
                    opts.type_name, type_xml_path, e
                );
                std::process::exit(EXIT_DATA);
            }
        };
        print_typeid_and_exit(&type_desc, opts.type_object_version);
    }

    if opts.topic_name.is_empty() {
        eprintln!("ERROR: topic name (-t) required");
        std::process::exit(EXIT_USAGE);
    }
    if opts.type_name.is_empty() {
        eprintln!("ERROR: type name (-y) required");
        std::process::exit(EXIT_USAGE);
    }
    if !opts.publish && !opts.subscribe {
        eprintln!("ERROR: must specify -P (publish) or -S (subscribe)");
        std::process::exit(EXIT_USAGE);
    }

    enforce_unsupported(&opts);

    // Resolve type XML path
    let type_xml_path = match (&opts.type_folder, &opts.type_file) {
        (Some(folder), Some(file)) => Some(format!("{}/xml/{}.xml", folder, file)),
        _ => None,
    };

    // Load type descriptor
    let type_desc = match &type_xml_path {
        Some(path) => match load_type_from_xml(path, &opts.type_name) {
            Ok(td) => Arc::new(td),
            Err(e) => {
                eprintln!(
                    "ERROR loading type '{}' from '{}': {}",
                    opts.type_name, path, e
                );
                std::process::exit(EXIT_DATA);
            }
        },
        None => {
            eprintln!("ERROR: --type-folder and --type-file are required");
            std::process::exit(EXIT_USAGE);
        }
    };

    if opts.verbose {
        println!("Loaded type: {}", type_desc.name);
    }

    // Build participant.
    // Precedence: -d on the CLI wins. Only fall back to HDDS_DOMAIN_ID if
    // -d was not passed. Log the source so a stale env var cannot silently
    // change the domain (F-HDDS_DOMAIN_ID).
    let (domain_id, domain_source) = if opts.domain_id_from_cli {
        (opts.domain_id, "cli")
    } else if let Some(env_val) = std::env::var("HDDS_DOMAIN_ID")
        .ok()
        .and_then(|v| v.parse::<u32>().ok())
    {
        (env_val, "env")
    } else {
        (opts.domain_id, "default")
    };
    if opts.verbose {
        println!("Domain id {} (source: {})", domain_id, domain_source);
    }

    let participant = match Participant::builder("hdds-xtypes-interop")
        .domain_id(domain_id)
        .with_transport(TransportMode::UdpMulticast)
        .build()
    {
        Ok(p) => Arc::new(p),
        Err(e) => {
            eprintln!("ERROR creating participant: {}", e);
            std::process::exit(EXIT_PARTICIPANT);
        }
    };

    // Pre-populate the participant type store with ALL types from the XML file
    // so the structural-assignability resolver can look up nested complex types
    // (e.g. E1 enum when the local type is E2-based) at match time.
    //
    // This is feature-gated behind "xtypes-structural-assignability": when the
    // feature is OFF the block compiles away and the participant type store is
    // never touched, preserving byte-identical behavior with the baseline binary.
    #[cfg(feature = "xtypes-structural-assignability")]
    if let Some(ref path) = type_xml_path {
        use std::collections::hash_map::Entry;
        let mut nested: std::collections::HashMap<
            hdds::xtypes::EquivalenceHash,
            hdds::xtypes::CompleteTypeObject,
        > = std::collections::HashMap::new();
        // Qualified type name -> Minimal hash of the structure that OWNS the
        // name in the store. Guards name-recourse soundness across files.
        let mut known_names: std::collections::HashMap<String, hdds::xtypes::EquivalenceHash> =
            std::collections::HashMap::new();

        // The app's own type file is loaded FIRST (its types always win name
        // conflicts), then every sibling XML type file from the same folder
        // in sorted (deterministic) order. Reference vendor test binaries
        // compile the ENTIRE suite's types in, so any announced peer type
        // name is resolvable on their side; loading the sibling files gives
        // the HDDS structural-assignability resolver the same local type
        // knowledge (e.g. union_uint32_key from unions_key_discriminator.xml
        // when the app itself runs with --type-file unions).
        let mut files: Vec<std::path::PathBuf> = vec![std::path::PathBuf::from(path)];
        if let Some(dir) = std::path::Path::new(path.as_str()).parent() {
            if let Ok(rd) = std::fs::read_dir(dir) {
                let mut siblings: Vec<std::path::PathBuf> = rd
                    .filter_map(|e| e.ok())
                    .map(|e| e.path())
                    .filter(|p| p.extension().map(|x| x == "xml").unwrap_or(false))
                    .filter(|p| p != &files[0])
                    .collect();
                siblings.sort();
                files.extend(siblings);
            }
        }

        for file in &files {
            let Some(file_str) = file.to_str() else {
                continue;
            };
            let Ok(all_types) = xml_loader::load_all_types_from_xml(file_str) else {
                // Sibling file the loader cannot parse: skip it entirely;
                // resolution for its types keeps the absent -> allow behavior.
                continue;
            };
            for td in &all_types {
                let td_arc = Arc::new(td.clone());
                // Collect nested enums/structs/bitmasks keyed by Minimal hash.
                hdds::dynamic::collect_nested_type_objects(&td_arc, &mut nested);
                // Also register the top-level type itself.
                let Some(to) = type_descriptor_to_xtypes(&td_arc) else {
                    continue;
                };
                let Some(hash) = hdds::dynamic::complete_type_object_minimal_hash(&to) else {
                    continue;
                };
                if let Some(name) = to.type_name() {
                    match known_names.entry(name.to_string()) {
                        Entry::Occupied(owner) => {
                            // Name already owned by an earlier file. Same hash
                            // means an identical structure (harmless duplicate,
                            // already resolvable). A DIFFERENT hash means two
                            // files declare conflicting shapes under one name:
                            // skip this one (first/primary file wins) so
                            // name-recourse resolution can never hand the
                            // matcher a wrong structure.
                            let _ = owner;
                            continue;
                        }
                        Entry::Vacant(slot) => {
                            slot.insert(hash);
                        }
                    }
                }
                match nested.entry(hash) {
                    Entry::Vacant(slot) => {
                        slot.insert(to);
                    }
                    Entry::Occupied(slot) => {
                        // Same Minimal hash under a DIFFERENT type name:
                        // structurally identical types (Minimal hashes exclude
                        // the type name, e.g. union_1 == union_3 == union_int32
                        // in unions.xml). The first entry keeps the
                        // Minimal-hash key; park each alias under its COMPLETE
                        // equivalence hash (which includes the type name, so
                        // aliases never collide) so the engine's SEDP
                        // name-recourse resolution (resolve_type_by_name scans
                        // store VALUES) still finds every announced type name.
                        // Without this, a vendor announcing 'Test::union_int32'
                        // missed resolution entirely (union_1 had evicted it)
                        // and the matcher fell back to absent-TypeObject ->
                        // allow, producing OK where INCONSISTENT_TOPIC is
                        // expected.
                        if slot.get().type_name() != to.type_name() {
                            if let Ok(chash) = to.compute_equivalence_hash() {
                                nested.entry(chash).or_insert(to);
                            }
                        }
                    }
                }
            }
        }
        participant.register_nested_type_objects(nested);
    }

    println!("Create topic: {}", opts.topic_name);

    let qos = build_qos(&opts);

    if opts.publish {
        run_publisher(&participant, &opts, &type_desc, qos);
    } else {
        run_subscriber(&participant, &opts, &type_desc, qos);
    }
}

// ---------------------------------------------------------------------------
// Publisher
// ---------------------------------------------------------------------------

fn run_publisher(
    participant: &Arc<Participant>,
    opts: &Options,
    type_desc: &Arc<hdds::dynamic::TypeDescriptor>,
    qos: QoS,
) {
    // Load data
    let data_xml_path = match (&opts.data_folder, &opts.data_file) {
        (Some(folder), Some(file)) => format!("{}/xml/{}.xml", folder, file),
        _ => {
            eprintln!("ERROR: --data-folder and --data-file required for publisher");
            std::process::exit(EXIT_USAGE);
        }
    };

    let data = match load_data_from_xml(&data_xml_path, type_desc) {
        Ok(d) => d,
        Err(e) => {
            eprintln!("ERROR loading data from '{}': {}", data_xml_path, e);
            std::process::exit(EXIT_DATA);
        }
    };

    // Encode to CDR at the negotiated representation. The `-x` flag drives
    // both the SEDP DataRepresentation PID and the encapsulation the engine
    // prepends; the body alignment must match (XCDR2 caps primitive
    // alignment at 4, DDS-XTypes v1.3 section 7.4.3.3).
    let cdr_bytes = match encode_dynamic_with_version(&data, cdr_version_of(opts)) {
        Ok(b) => b,
        Err(e) => {
            eprintln!("ERROR encoding CDR: {}", e);
            std::process::exit(EXIT_DATA);
        }
    };

    // Do NOT prepend an encapsulation header here. HDDS `write_raw` takes
    // raw serialized CDR: the engine prepends the 4-byte header itself
    // (derived from the type extensibility + the writer DataRepresentation,
    // see hdds protocol/builder/packet.rs `encap_kind_for_version`) and the
    // receiving router strips it before delivery. Prepending here doubles
    // the header on the wire; peers then decode the second header as data
    // (CoreDX/Cyclone read x1 = 0x0700 for struct_primitive_uint32). The
    // read path keeps `strip_encapsulation` as an if-present no-op.
    let payload = cdr_bytes;

    // Create writer with type name override.
    // When --disable-type-info is set, suppress the TypeObject from SEDP so the
    // remote peer falls back to topic-name-only type matching (DDS-XTypes v1.3
    // §7.6.3.4 force_type_validation semantics: without a TypeObject, structural
    // assignability cannot be enforced and matching proceeds by name).
    let type_object = if opts.disable_type_info {
        None
    } else {
        type_descriptor_to_xtypes(type_desc)
    };

    // When the TypeObject is suppressed (--disable-type-info) the engine
    // cannot derive the canonical XCDR2 encapsulation from extensibility
    // flags and would default to PLAIN_CDR2 (0x0007) even though the body
    // we encode above is DHEADER/EMHEADER-framed for appendable/mutable
    // types. Steer the encapsulation explicitly from the local descriptor
    // (DDS-XTypes v1.3 section 7.6.3.1.2: appendable -> D_CDR2 0x0009,
    // mutable -> PL_CDR2 0x000B; final keeps the engine default). The
    // engine still degrades to the XCDR1 codes when x1 is negotiated.
    let encapsulation_kind = if opts.disable_type_info {
        match type_desc.extensibility {
            Extensibility::Appendable => Some(0x0009u16),
            Extensibility::Mutable => Some(0x000Bu16),
            Extensibility::Final => None,
        }
    } else {
        None
    };
    println!(
        "Create writer for topic: {} type: {}",
        opts.topic_name, opts.type_name
    );

    let writer_listener = Arc::new(XtypesWriterListener::new());
    let writer = match participant.create_raw_writer_with_type_and_encapsulation(
        &opts.topic_name,
        &opts.type_name,
        Some(qos),
        type_object,
        encapsulation_kind,
        Some(writer_listener),
    ) {
        Ok(w) => w,
        Err(e) => {
            eprintln!("ERROR creating writer: {}", e);
            std::process::exit(EXIT_PARTICIPANT);
        }
    };

    // Wait briefly for discovery
    std::thread::sleep(Duration::from_millis(500));

    while !ALL_DONE.load(Ordering::SeqCst) {
        if let Err(e) = writer.write_raw(&payload) {
            eprintln!("WARN write error: {}", e);
        }
        if opts.print_writer_samples {
            println!("Wrote:");
            print_dynamic_data(&data);
        }
        std::thread::sleep(Duration::from_secs(1));
    }
}

// ---------------------------------------------------------------------------
// Subscriber
// ---------------------------------------------------------------------------

fn run_subscriber(
    participant: &Arc<Participant>,
    opts: &Options,
    type_desc: &Arc<hdds::dynamic::TypeDescriptor>,
    qos: QoS,
) {
    // When --disable-type-info is set, suppress the TypeObject from SEDP so the
    // remote peer falls back to topic-name-only type matching. Mirrors the
    // publisher-side suppression; both sides must agree on omitting the TypeObject
    // for the force_type_validation=false case to yield a successful match.
    let type_object = if opts.disable_type_info {
        None
    } else {
        type_descriptor_to_xtypes(type_desc)
    };
    println!(
        "Create reader for topic: {} type: {}",
        opts.topic_name, opts.type_name
    );

    let reader_listener = Arc::new(XtypesReaderListener::new());
    let reader = match participant.create_raw_reader_with_type(
        &opts.topic_name,
        &opts.type_name,
        Some(qos),
        type_object,
        Some(reader_listener),
    ) {
        Ok(r) => r,
        Err(e) => {
            eprintln!("ERROR creating reader: {}", e);
            std::process::exit(EXIT_PARTICIPANT);
        }
    };

    // Expected data for check
    let expected_data = match (&opts.data_folder, &opts.data_file) {
        (Some(folder), Some(file)) => {
            let path = format!("{}/xml/{}.xml", folder, file);
            match load_data_from_xml(&path, type_desc) {
                Ok(d) => Some(d),
                Err(e) => {
                    eprintln!("WARN could not load expected data: {}", e);
                    None
                }
            }
        }
        _ => None,
    };

    let mut received_ok = false;

    while !ALL_DONE.load(Ordering::SeqCst) {
        match reader.try_take_raw() {
            Ok(samples) => {
                for raw in samples {
                    // The HDDS router already strips the 4-byte encapsulation
                    // header before delivery (route_data_packet /
                    // route_reassembled_data), so `raw.payload` is bare CDR.
                    // Do NOT run strip_encapsulation here: its if-present
                    // heuristic corrupts samples whose first bytes mimic a
                    // header (e.g. a union discriminant 0 -> `00 00` reads
                    // as CDR_BE and 4 data bytes get eaten).
                    let payload = raw.payload.as_slice();
                    match decode_dynamic_with_version(payload, type_desc, cdr_version_of(opts)) {
                        Ok(decoded) => {
                            // Print after successful decode: harness uses this
                            // line to determine the subscriber received a sample.
                            // Emitting it before decode would cause DATA_NOT_CORRECT
                            // for tryConstruct=Discard samples that are silently
                            // dropped (DDS-XTypes v1.3 §7.5.1.4).
                            println!("sample_received()");
                            print_dynamic_data(&decoded);
                            if let Some(ref expected) = expected_data {
                                if compare_dynamic_data(&decoded, expected) {
                                    println!("Received sample is the same as loaded");
                                    received_ok = true;
                                } else {
                                    println!("Received sample is not the same as loaded");
                                }
                            }
                        }
                        Err(e) => {
                            // Decode failed: policy (Discard) or corrupt wire data.
                            // Do not announce sample_received() so the harness
                            // observes DATA_NOT_RECEIVED instead of DATA_NOT_CORRECT.
                            eprintln!("WARN CDR decode error: {}", e);
                        }
                    }
                }
            }
            Err(e) => {
                eprintln!("WARN read error: {}", e);
            }
        }
        std::thread::sleep(Duration::from_millis(100));
    }

    let _ = received_ok;
}

// ---------------------------------------------------------------------------
// Print helper
// ---------------------------------------------------------------------------

fn print_dynamic_data(data: &DynamicData) {
    use hdds::dynamic::DynamicValue;

    fn print_value(indent: usize, name: &str, val: &DynamicValue) {
        let pad = " ".repeat(indent * 2);
        match val {
            DynamicValue::Struct(fields) => {
                println!("{}{} {{", pad, name);
                for (k, v) in fields {
                    print_value(indent + 1, k, v);
                }
                println!("{}}}", pad);
            }
            DynamicValue::Sequence(elems) | DynamicValue::Array(elems) => {
                println!("{}{} [", pad, name);
                for (i, v) in elems.iter().enumerate() {
                    print_value(indent + 1, &i.to_string(), v);
                }
                println!("{}]", pad);
            }
            DynamicValue::Bool(v) => println!("{}{}: {}", pad, name, v),
            DynamicValue::U8(v) => println!("{}{}: {}", pad, name, v),
            DynamicValue::U16(v) => println!("{}{}: {}", pad, name, v),
            DynamicValue::U32(v) => println!("{}{}: {}", pad, name, v),
            DynamicValue::U64(v) => println!("{}{}: {}", pad, name, v),
            DynamicValue::I8(v) => println!("{}{}: {}", pad, name, v),
            DynamicValue::I16(v) => println!("{}{}: {}", pad, name, v),
            DynamicValue::I32(v) => println!("{}{}: {}", pad, name, v),
            DynamicValue::I64(v) => println!("{}{}: {}", pad, name, v),
            DynamicValue::F32(v) => println!("{}{}: {}", pad, name, v),
            DynamicValue::F64(v) => println!("{}{}: {}", pad, name, v),
            DynamicValue::LongDouble(v) => println!(
                "{}{}: {}",
                pad,
                name,
                crate::data_loader::binary128_le_to_f64(v)
            ),
            // escape_default() keeps control bytes (e.g. char8 value 0x01 from
            // struct_char_x1) out of stdout: a raw control char captured into the
            // OMG harness junit makes junitparser/lxml reject the whole report
            // ("no control characters") and HDDS would score zero on the CI.
            DynamicValue::Char(v) => println!("{}{}: '{}'", pad, name, v.escape_default()),
            DynamicValue::String(v) | DynamicValue::WString(v) => {
                println!("{}{}: \"{}\"", pad, name, v.escape_default())
            }
            DynamicValue::Enum(val, name2) => println!("{}{}: {}({})", pad, name, name2, val),
            DynamicValue::Union(disc, case, inner) => {
                println!("{}{}: union[disc={}][{}]", pad, name, disc, case);
                print_value(indent + 1, case, inner);
            }
            DynamicValue::Null => println!("{}{}: null", pad, name),
        }
    }

    print_value(0, data.type_name(), data.value());
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    fn args(input: &[&str]) -> Vec<String> {
        std::iter::once("hdds_xtypes_shape_main_linux".to_string())
            .chain(input.iter().map(|s| s.to_string()))
            .collect()
    }

    #[test]
    fn parses_basic_publisher_args() {
        let v = args(&[
            "-P",
            "-d",
            "42",
            "-t",
            "Test",
            "-y",
            "Test::struct_f1",
            "--type-folder",
            "/tmp/types",
            "--type-file",
            "extensibility",
        ]);
        let o = parse_args(&v).expect("parse");
        assert!(o.publish);
        assert!(!o.subscribe);
        assert_eq!(o.domain_id, 42);
        assert!(o.domain_id_from_cli);
        assert_eq!(o.topic_name, "Test");
        assert_eq!(o.type_name, "Test::struct_f1");
        assert_eq!(o.type_folder.as_deref(), Some("/tmp/types"));
    }

    #[test]
    fn tri_state_parsing() {
        assert_eq!(TriState::parse("t").unwrap(), TriState::True);
        assert_eq!(TriState::parse("T").unwrap(), TriState::True);
        assert_eq!(TriState::parse("true").unwrap(), TriState::True);
        assert_eq!(TriState::parse("f").unwrap(), TriState::False);
        assert_eq!(TriState::parse("0").unwrap(), TriState::False);
        assert_eq!(TriState::parse("d").unwrap(), TriState::Default);
        assert!(TriState::parse("xyz").is_err());
    }

    #[test]
    fn unknown_arg_is_error_not_silent() {
        let v = args(&["-P", "-t", "T", "-y", "Y", "--bogus-flag", "value"]);
        let err = parse_args(&v).unwrap_err();
        assert!(err.contains("--bogus-flag"));
    }

    #[test]
    fn missing_value_is_error() {
        let v = args(&["-P", "-t"]);
        let err = parse_args(&v).unwrap_err();
        assert!(err.contains("missing value"));
    }

    #[test]
    fn captures_omg_behavior_flags() {
        let v = args(&[
            "-S",
            "-t",
            "T",
            "-y",
            "Y",
            "--ignore-member-names",
            "t",
            "--ignore-seq-bounds",
            "f",
            "--ignore-str-bounds",
            "d",
            "--force-type-validation",
            "t",
            "--disable-type-info",
        ]);
        let o = parse_args(&v).expect("parse");
        assert_eq!(o.ignore_member_names, TriState::True);
        assert_eq!(o.ignore_seq_bounds, TriState::False);
        assert_eq!(o.ignore_str_bounds, TriState::Default);
        assert_eq!(o.force_type_validation, TriState::True);
        assert!(o.disable_type_info);
    }

    #[test]
    fn domain_id_default_is_not_from_cli() {
        let v = args(&["-P", "-t", "T", "-y", "Y"]);
        let o = parse_args(&v).expect("parse");
        assert_eq!(o.domain_id, 0);
        assert!(!o.domain_id_from_cli);
    }

    // Verify that decode_dynamic returns Err for an enum value absent from the
    // local type when the field carries TryConstructKind::Discard (the default
    // per DDS-XTypes v1.3 §7.2.2.4.1.2 Table 9).  This is the precondition for
    // the subscriber loop to suppress sample_received() and let the harness
    // observe DATA_NOT_RECEIVED instead of DATA_NOT_CORRECT.
    //
    // E2 (local): VAL0=0, VAL1=1(default), VAL2=2
    // Wire enum value: 3 (VAL3) -- present in E1 but not in E2.
    #[test]
    fn decode_unknown_enum_discard_returns_err() {
        use hdds::dynamic::{
            decode_dynamic, EnumDescriptor, EnumVariant, Extensibility, FieldDescriptor,
            TryConstructKind, TypeDescriptor, TypeKind,
        };
        use std::sync::Arc;

        // Build E2: three variants, VAL1 is the defaultLiteral.
        let e2 = Arc::new(TypeDescriptor::new(
            "E2",
            TypeKind::Enum(EnumDescriptor::new(vec![
                EnumVariant::new("VAL0", 0),
                EnumVariant::new("VAL1", 1).with_default_literal(),
                EnumVariant::new("VAL2", 2),
            ])),
        ));

        // Struct with one E2 field, TryConstruct=Discard (default).
        let discard_desc = Arc::new(
            TypeDescriptor::struct_type(
                "struct_enum_2_discard",
                vec![FieldDescriptor::new("x1", e2.clone())],
            )
            .with_extensibility(Extensibility::Mutable),
        );

        // Wire: mutable struct -- EMHEADER(x1, LC=2, id=0) + enum value=3 (unknown in E2).
        // EMHEADER: LC=2 -> (2<<28) | member_id=0 = 0x2000_0000
        // Enum: 4 bytes little-endian = 3u32
        let mut wire: Vec<u8> = Vec::new();
        wire.extend(&0x2000_0000u32.to_le_bytes()); // EMHEADER
        wire.extend(&3u32.to_le_bytes()); // enum value VAL3, not in E2
        wire.extend(&0x3FFF_FFFFu32.to_le_bytes()); // sentinel

        // Discard policy: decode must fail.
        assert!(
            decode_dynamic(&wire, &discard_desc).is_err(),
            "Discard policy: unknown enum value must produce Err"
        );

        // UseDefault policy: decode must succeed and return the defaultLiteral (VAL1=1).
        let use_default_desc = Arc::new(
            TypeDescriptor::struct_type(
                "struct_enum_2_default",
                vec![FieldDescriptor::new("x1", e2.clone())
                    .with_try_construct(TryConstructKind::UseDefault)],
            )
            .with_extensibility(Extensibility::Mutable),
        );

        let decoded = decode_dynamic(&wire, &use_default_desc)
            .expect("UseDefault policy: unknown enum value must produce Ok with default variant");
        // The default variant is VAL1 (value=1).
        match decoded.get_field("x1").expect("x1 field present") {
            hdds::dynamic::DynamicValue::Enum(v, _) => {
                assert_eq!(*v, 1, "UseDefault must map unknown enum to defaultLiteral (VAL1=1)");
            }
            other => panic!("expected Enum variant, got {:?}", other),
        }
    }
}
