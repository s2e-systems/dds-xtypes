// SPDX-License-Identifier: Apache-2.0 OR MIT
// Copyright (c) 2025-2026 naskel.com

//! DDS-XML type loader.
//!
//! Parses the OMG DDS-XML format used by the dds-xtypes interoperability test
//! suite. The grammar supported is:
//!
//!   <dds><types>
//!     <module name="Test">
//!       <struct name="foo" extensibility="final|appendable|mutable">
//!         <member name="x1" type="int32" [id="N"] [sequenceMaxLength="-1|N"]
//!                 [arrayDimensions="N[,M]"] [stringMaxLength="N"] [optional="true"]/>
//!       </struct>
//!       <enum name="E1" [bitBound="8|16|32"]>
//!         <enumerator name="VAL0" value="0"/>
//!       </enum>
//!       <union name="U1">
//!         <discriminator type="uint8"/>
//!         <case><caseDiscriminator value="1"/><member name="x1" type="int32"/></case>
//!       </union>
//!     </module>
//!   </types></dds>
//!
//! Modules nest: <module name="A"><module name="B">...</module></module> yields
//! qualified names like "A::B::Type". Both the fully qualified and the bare
//! local name resolve to a type, with fully qualified taking priority on
//! collisions.
//!
//! Known unsupported grammar (documented in README.md "Known Blockers"):
//!   - typedef, bitset, annotation, autoid, hashid, mustUnderstand.
//!   - extensibility is parsed and propagated to TypeDescriptor.extensibility
//!     for both struct and union types; the HDDS engine selects the wire
//!     representation identifier (D_CDR2 / PL_CDR2) from it when it prepends
//!     the encapsulation header inside write_raw (the driver sends bare CDR).
//!   - tryConstruct is parsed on struct members and union case members;
//!     defaultLiteral is parsed on enum variants.
//!   - caseDiscriminator value="default" is parsed and marks the case
//!     as the union default (UnionDescriptor::default_case).

use std::collections::HashMap;
use std::sync::Arc;

use hdds::dynamic::{
    ArrayDescriptor, EnumDescriptor, EnumVariant, Extensibility, FieldDescriptor, PrimitiveKind,
    SequenceDescriptor, TryConstructKind, TypeDescriptor, TypeKind, UnionCase, UnionDescriptor,
};
use quick_xml::events::Event;
use quick_xml::reader::Reader;

// ---------------------------------------------------------------------------
// Public entry point
// ---------------------------------------------------------------------------

pub fn load_type_from_xml(path: &str, type_name: &str) -> Result<TypeDescriptor, String> {
    let content = std::fs::read_to_string(path)
        .map_err(|e| format!("cannot read '{}': {}", path, e))?;
    parse_type_xml(&content, type_name)
}

/// Load ALL type descriptors from an XML file.
///
/// Used by the structural-assignability resolver to pre-populate the
/// participant type store with every type defined in the XML file — including
/// types that are not the primary writer/reader type.  This lets the resolver
/// answer hash lookups for nested enum or struct types that appear in the XML
/// but are not the directly-requested type (e.g. E1 in arrays.xml when the
/// driver is running as a subscriber for enum2x10).
///
/// Types that cannot be parsed (e.g. complex recursive aliases) are silently
/// skipped; the returned Vec contains only successfully-built descriptors.
pub fn load_all_types_from_xml(path: &str) -> Result<Vec<TypeDescriptor>, String> {
    let content = std::fs::read_to_string(path)
        .map_err(|e| format!("cannot read '{}': {}", path, e))?;
    let types = collect_raw_types(&content)?;

    let mut by_qualified: std::collections::HashMap<String, usize> =
        std::collections::HashMap::new();
    let mut by_local: std::collections::HashMap<String, usize> =
        std::collections::HashMap::new();
    for (i, t) in types.iter().enumerate() {
        by_qualified.insert(t.qualified_name(), i);
        by_local.entry(t.local_name().to_string()).or_insert(i);
    }

    let mut result = Vec::new();
    for raw in &types {
        if let Ok(td) = raw_to_descriptor(raw, &types, &by_qualified, &by_local) {
            result.push(td);
        }
    }
    Ok(result)
}

// ---------------------------------------------------------------------------
// XML parse
// ---------------------------------------------------------------------------

#[derive(Debug, Clone)]
enum RawTypeDef {
    Struct {
        name: String,
        module: String,
        extensibility: String,
        /// True when the struct carries `autoid="hash"` (DDS-XTypes §7.3.1.2).
        autoid_hash: bool,
        members: Vec<RawMember>,
    },
    Enum {
        name: String,
        module: String,
        bit_bound: u8, // 8 / 16 / 32, defaults to 32 per IDL 4.2
        variants: Vec<EnumVariant>,
    },
    /// Bitmask type: a set of named bit flags each with a bit position.
    /// Represented as an enum where each variant value equals `1 << position`.
    /// The `bit_bound` controls the underlying primitive width (8/16/32/64).
    Bitmask {
        name: String,
        module: String,
        bit_bound: u8,
        /// (flag_name, bit_position)
        flags: Vec<(String, u32)>,
    },
    Union {
        name: String,
        module: String,
        extensibility: String,
        discriminator_type: String,
        /// Try-construct policy on the `<discriminator>` element (not the cases).
        discriminator_try_construct: TryConstructKind,
        /// Whether the discriminator carries `key="true"` (DDS-XML §7.3.4.6).
        discriminator_is_key: bool,
        cases: Vec<RawCase>,
    },
}

impl RawTypeDef {
    fn local_name(&self) -> &str {
        match self {
            Self::Struct { name, .. }
            | Self::Enum { name, .. }
            | Self::Bitmask { name, .. }
            | Self::Union { name, .. } => name,
        }
    }

    fn module(&self) -> &str {
        match self {
            Self::Struct { module, .. }
            | Self::Enum { module, .. }
            | Self::Bitmask { module, .. }
            | Self::Union { module, .. } => module,
        }
    }


    fn qualified_name(&self) -> String {
        let m = self.module();
        if m.is_empty() {
            self.local_name().to_string()
        } else {
            format!("{}::{}", m, self.local_name())
        }
    }
}

#[derive(Debug, Clone)]
struct RawMember {
    name: String,
    type_str: String,
    id: Option<u32>,
    sequence_max: Option<i64>, // -1 = unbounded, else bound
    array_dims: Vec<usize>,
    string_max: Option<usize>,
    optional: bool,
    try_construct: TryConstructKind,
    /// Value of the `hashid="alias"` attribute (DDS-XTypes §7.3.1.2.1.1).
    /// When present, the hash of `alias` is used for the member ID and the
    /// Minimal name_hash instead of the member's own `name`.
    hashid: Option<String>,
    /// `key="true"` — member participates in the DDS instance key.
    is_key: bool,
    /// `mustUnderstand="true"` — reader must understand this member.
    is_must_understand: bool,
}

#[derive(Debug, Clone)]
struct RawCase {
    discriminator_values: Vec<i64>,
    /// Unresolved string labels (enum variant names that could not be parsed
    /// as integers at collection time; resolved in `raw_to_descriptor` once
    /// the discriminator type is known).
    discriminator_name_labels: Vec<String>,
    /// True when one of the caseDiscriminator values was `"default"`.
    is_default: bool,
    member: RawMember,
}

fn parse_type_xml(xml: &str, type_name: &str) -> Result<TypeDescriptor, String> {
    let types = collect_raw_types(xml)?;

    // Build lookup: qualified takes priority; fall back to local but warn
    // when a local-name collision exists across modules (last write wins is
    // unsafe - we keep the *first* occurrence so the message stays
    // deterministic and lookup by the unqualified name does not silently
    // pick the wrong module's type).
    let mut by_qualified: HashMap<String, usize> = HashMap::new();
    let mut by_local: HashMap<String, usize> = HashMap::new();
    for (i, t) in types.iter().enumerate() {
        by_qualified.insert(t.qualified_name(), i);
        // First-write-wins on the local index so a deterministic name
        // collision still has a stable answer.
        by_local.entry(t.local_name().to_string()).or_insert(i);
    }

    // Resolve the requested type
    let idx = by_qualified
        .get(type_name)
        .or_else(|| by_local.get(type_name))
        .copied()
        .ok_or_else(|| {
            let available: Vec<_> = types.iter().map(|t| t.qualified_name()).collect();
            format!(
                "type '{}' not found in XML; available: {}",
                type_name,
                available.join(", ")
            )
        })?;

    raw_to_descriptor(&types[idx], &types, &by_qualified, &by_local)
}

// ---------------------------------------------------------------------------
// Collect all raw type definitions
// ---------------------------------------------------------------------------

fn collect_raw_types(xml: &str) -> Result<Vec<RawTypeDef>, String> {
    let mut reader = Reader::from_str(xml);
    reader.config_mut().trim_text(true);

    let mut types: Vec<RawTypeDef> = Vec::new();

    // Parsing state
    let mut module_stack: Vec<String> = Vec::new();
    let mut current_struct: Option<(String, String, bool, Vec<RawMember>)> = None; // (name, ext, autoid_hash, members)
    let mut current_enum: Option<(String, u8, Vec<EnumVariant>)> = None; // (name, bit_bound, variants)
    // (name, bit_bound, flags: Vec<(flag_name, bit_position)>)
    let mut current_bitmask: Option<(String, u8, Vec<(String, u32)>)> = None;
    // (name, ext, disc_type, disc_try_construct, disc_is_key, cases)
    let mut current_union: Option<(String, String, String, TryConstructKind, bool, Vec<RawCase>)> = None;
    // (int_labels, name_labels, is_default, member)
    let mut current_case: Option<(Vec<i64>, Vec<String>, bool, Option<RawMember>)> = None;
    let mut buf = Vec::new();

    loop {
        match reader.read_event_into(&mut buf) {
            Ok(Event::Start(ref e)) => {
                let tag = std::str::from_utf8(e.name().as_ref())
                    .unwrap_or("")
                    .to_lowercase();
                let attrs = parse_attrs(e);

                handle_open_tag(
                    &tag,
                    &attrs,
                    &mut module_stack,
                    &mut current_struct,
                    &mut current_enum,
                    &mut current_bitmask,
                    &mut current_union,
                    &mut current_case,
                );
            }
            Ok(Event::Empty(ref e)) => {
                let tag = std::str::from_utf8(e.name().as_ref())
                    .unwrap_or("")
                    .to_lowercase();
                let attrs = parse_attrs(e);

                // An empty element has no End event. Handle it like
                // Start+End for child-data containers (member, enumerator,
                // discriminator, caseDiscriminator). Container-style
                // elements (module, struct, enum, union, case) cannot be
                // empty - if encountered, push+immediate-pop so we do not
                // leak the module stack (F-module-stack from the panel).
                match tag.as_str() {
                    "module" => {
                        // <module/> opens and closes immediately. The OMG
                        // corpus never uses this form but the spec allows
                        // it, and the previous code leaked module_stack
                        // here. We push and pop to keep the qualified-name
                        // join() stable across nesting.
                        let name = attrs.get("name").cloned().unwrap_or_default();
                        module_stack.push(name);
                        module_stack.pop();
                    }
                    "struct" | "enum" | "union" | "case" => {
                        // Genuinely empty type/case definitions are
                        // malformed input but the parser previously dropped
                        // them silently. Surface as a hard error.
                        return Err(format!(
                            "<{}/> empty element is not allowed (need child elements)",
                            tag
                        ));
                    }
                    _ => {
                        handle_open_tag(
                            &tag,
                            &attrs,
                            &mut module_stack,
                            &mut current_struct,
                            &mut current_enum,
                            &mut current_bitmask,
                            &mut current_union,
                            &mut current_case,
                        );
                    }
                }
            }
            Ok(Event::End(ref e)) => {
                let tag = std::str::from_utf8(e.name().as_ref())
                    .unwrap_or("")
                    .to_lowercase();

                match tag.as_str() {
                    "module" => {
                        module_stack.pop();
                    }
                    "struct" => {
                        if let Some((name, ext, autoid_hash, members)) = current_struct.take() {
                            // Fully qualified module path: A::B::C, not just C.
                            let module = module_stack.join("::");
                            types.push(RawTypeDef::Struct {
                                name,
                                module,
                                extensibility: ext,
                                autoid_hash,
                                members,
                            });
                        }
                    }
                    "enum" => {
                        if let Some((name, bit_bound, variants)) = current_enum.take() {
                            let module = module_stack.join("::");
                            types.push(RawTypeDef::Enum {
                                name,
                                module,
                                bit_bound,
                                variants,
                            });
                        }
                    }
                    "bitmask" => {
                        if let Some((name, bit_bound, flags)) = current_bitmask.take() {
                            let module = module_stack.join("::");
                            types.push(RawTypeDef::Bitmask {
                                name,
                                module,
                                bit_bound,
                                flags,
                            });
                        }
                    }
                    "union" => {
                        if let Some((name, ext, disc_type, disc_try_construct, disc_is_key, cases)) = current_union.take() {
                            let module = module_stack.join("::");
                            types.push(RawTypeDef::Union {
                                name,
                                module,
                                extensibility: ext,
                                discriminator_type: disc_type,
                                discriminator_try_construct: disc_try_construct,
                                discriminator_is_key: disc_is_key,
                                cases,
                            });
                        }
                    }
                    "case" => {
                        if let Some((int_labels, name_labels, is_default, Some(member))) = current_case.take() {
                            if let Some((_, _, _, _, _, ref mut cases)) = current_union {
                                cases.push(RawCase {
                                    discriminator_values: int_labels,
                                    discriminator_name_labels: name_labels,
                                    is_default,
                                    member,
                                });
                            }
                        }
                    }
                    _ => {}
                }
            }
            Ok(Event::Eof) => break,
            Err(e) => return Err(format!("XML parse error: {}", e)),
            _ => {}
        }
        buf.clear();
    }

    Ok(types)
}

/// Shared handler for both Start and (non-container) Empty events.
fn handle_open_tag(
    tag: &str,
    attrs: &HashMap<String, String>,
    module_stack: &mut Vec<String>,
    current_struct: &mut Option<(String, String, bool, Vec<RawMember>)>,
    current_enum: &mut Option<(String, u8, Vec<EnumVariant>)>,
    current_bitmask: &mut Option<(String, u8, Vec<(String, u32)>)>,
    current_union: &mut Option<(String, String, String, TryConstructKind, bool, Vec<RawCase>)>,
    current_case: &mut Option<(Vec<i64>, Vec<String>, bool, Option<RawMember>)>,
) {
    match tag {
        "module" => {
            let name = attrs.get("name").cloned().unwrap_or_default();
            module_stack.push(name);
        }
        "struct" => {
            let name = attrs.get("name").cloned().unwrap_or_default();
            // IDL 4.2 / DDS-XTypes v1.3 (7.3.1.2.1.6): a constructed type
            // with no explicit extensibility annotation is APPENDABLE, not
            // final. Reference vendors (coredx/cyclone/connext) apply this
            // default, so a "final" fallback here breaks TypeObject hashes
            // and assignability for every type file omitting the attribute.
            let ext = attrs
                .get("extensibility")
                .cloned()
                .unwrap_or_else(|| "appendable".to_string());
            // autoid="hash" enables IS_AUTOID_HASH on the emitted StructTypeFlag
            // (DDS-XTypes v1.3 §7.3.1.2).  Any other autoid value is ignored.
            let autoid_hash = attrs
                .get("autoid")
                .map(|v| v.trim().to_lowercase() == "hash")
                .unwrap_or(false);
            *current_struct = Some((name, ext, autoid_hash, Vec::new()));
        }
        "enum" => {
            let name = attrs.get("name").cloned().unwrap_or_default();
            let bit_bound = attrs
                .get("bitbound")
                .and_then(|v| v.parse::<u8>().ok())
                .unwrap_or(32);
            *current_enum = Some((name, bit_bound, Vec::new()));
        }
        "bitmask" => {
            let name = attrs.get("name").cloned().unwrap_or_default();
            let bit_bound = attrs
                .get("bitbound")
                .and_then(|v| v.parse::<u8>().ok())
                .unwrap_or(32);
            *current_bitmask = Some((name, bit_bound, Vec::new()));
        }
        "flag" => {
            // <flag name="FLAG_N" value="N"/> where value is the bit position.
            if let Some((_, _, ref mut flags)) = current_bitmask {
                let fname = attrs.get("name").cloned().unwrap_or_default();
                let position = attrs
                    .get("value")
                    .and_then(|v| v.parse::<u32>().ok())
                    .unwrap_or(flags.len() as u32);
                flags.push((fname, position));
            }
        }
        "union" => {
            let name = attrs.get("name").cloned().unwrap_or_default();
            // Same spec default as struct: absent extensibility attribute
            // means APPENDABLE (IDL 4.2 / DDS-XTypes v1.3 7.3.1.2.1.6).
            let ext = attrs
                .get("extensibility")
                .cloned()
                .unwrap_or_else(|| "appendable".to_string());
            *current_union = Some((name, ext, "int32".to_string(), TryConstructKind::Discard, false, Vec::new()));
        }
        "discriminator" => {
            if let Some((_, _, ref mut disc_type, ref mut disc_tc, ref mut disc_is_key, _)) = current_union {
                if let Some(t) = attrs.get("type") {
                    if t == "nonBasic" || t == "nonbasic" {
                        // Use the referenced type name as the discriminator type string.
                        if let Some(n) = attrs.get("nonbasictypename") {
                            *disc_type = n.clone();
                        }
                    } else {
                        *disc_type = t.clone();
                    }
                }
                if let Some(tc) = attrs.get("tryconstruct") {
                    *disc_tc = try_construct_from_str(tc);
                }
                if attrs.get("key").map(|v| v.trim().eq_ignore_ascii_case("true")).unwrap_or(false) {
                    *disc_is_key = true;
                }
            }
        }
        "case" => {
            *current_case = Some((Vec::new(), Vec::new(), false, None));
        }
        "casediscriminator" => {
            if let Some((ref mut int_labels, ref mut name_labels, ref mut is_default, _)) = current_case {
                if let Some(v) = attrs.get("value") {
                    if v.trim().eq_ignore_ascii_case("default") {
                        *is_default = true;
                    } else if let Ok(parsed) = parse_int_literal(v) {
                        int_labels.push(parsed);
                    } else {
                        // Enum variant name — resolved to an integer value once
                        // the discriminator type is known in raw_to_descriptor.
                        name_labels.push(v.trim().to_string());
                    }
                }
            }
        }
        "member" => {
            let member = build_raw_member(attrs);
            // Precedence: a union case `member` populates the case payload;
            // otherwise it is appended to the current struct.
            if let Some((_, _, _, ref mut opt_member)) = current_case {
                *opt_member = Some(member);
            } else if let Some((_, _, _, ref mut members)) = current_struct {
                members.push(member);
            }
        }
        "enumerator" => {
            if let Some((_, _, ref mut variants)) = current_enum {
                let name = attrs.get("name").cloned().unwrap_or_default();
                let value = attrs
                    .get("value")
                    .and_then(|v| parse_int_literal(v).ok())
                    .unwrap_or(variants.len() as i64);
                let default_literal = attrs
                    .get("defaultliteral")
                    .map(|v| v.eq_ignore_ascii_case("true"))
                    .unwrap_or(false);
                let mut variant = EnumVariant::new(name, value);
                if default_literal {
                    variant = variant.with_default_literal();
                }
                variants.push(variant);
            }
        }
        _ => {}
    }
}

// ---------------------------------------------------------------------------
// Attribute helpers
// ---------------------------------------------------------------------------

fn parse_attrs(e: &quick_xml::events::BytesStart) -> HashMap<String, String> {
    let mut map = HashMap::new();
    for attr in e.attributes().flatten() {
        let key = std::str::from_utf8(attr.key.as_ref())
            .unwrap_or("")
            .to_lowercase();
        // Unescape XML entities in attribute values so `type="string&lt;64&gt;"`
        // round-trips to `string<64>`. Without this the inline-bound syntax
        // never matches because the entity stays literal.
        let val = attr
            .unescape_value()
            .map(|cow| cow.into_owned())
            .unwrap_or_else(|_| String::from_utf8(attr.value.to_vec()).unwrap_or_default());
        map.insert(key, val);
    }
    map
}

fn build_raw_member(attrs: &HashMap<String, String>) -> RawMember {
    let name = attrs.get("name").cloned().unwrap_or_default();
    // DDS-XML uses type="nonBasic" + nonBasicTypeName="ActualType" when the
    // member type is a user-defined type (enum, struct, union). Resolve to the
    // actual type name so prim_from_str_or_nested_with_bound can look it up.
    let raw_type = attrs.get("type").map(|s| s.as_str()).unwrap_or("int32");
    let type_str = if raw_type.eq_ignore_ascii_case("nonBasic") {
        attrs
            .get("nonbasictypename")
            .cloned()
            .unwrap_or_else(|| "int32".to_string())
    } else {
        raw_type.to_string()
    };
    let id = attrs.get("id").and_then(|v| v.parse::<u32>().ok());

    // sequenceMaxLength: present means it is a sequence
    let sequence_max = attrs
        .get("sequencemaxlength")
        .and_then(|v| parse_int_literal(v).ok());

    // arrayDimensions: comma-separated list e.g. "10" or "10,2"
    let array_dims: Vec<usize> = attrs
        .get("arraydimensions")
        .map(|v| {
            v.split(',')
                .filter_map(|s| s.trim().parse::<usize>().ok())
                .collect()
        })
        .unwrap_or_default();

    let string_max = attrs
        .get("stringmaxlength")
        .and_then(|v| v.parse::<usize>().ok());

    let optional = attrs.get("optional").map(|v| v == "true").unwrap_or(false);

    // tryConstruct attribute (DDS-XML: case-insensitive).
    // Per DDS-XTypes v1.3 §7.2.2.4.1.2 Table 9, absent TryConstruct flags
    // (both TC1 and TC2 = 0) encode DISCARD, not USE_DEFAULT. The XML
    // attribute is absent when neither publisher nor subscriber specified a
    // policy; the absence means the subscriber cannot accommodate a bound
    // mismatch and must reject the sample.
    let try_construct = attrs
        .get("tryconstruct")
        .map(|v| try_construct_from_str(v))
        .unwrap_or(TryConstructKind::Discard);

    // hashid="alias" overrides the name used for hash-based member ID
    // computation (DDS-XTypes §7.3.1.2.1.1). The attribute value is the
    // canonical name whose FNV-1a hash becomes the member ID.
    let hashid = attrs.get("hashid").cloned();

    // key="true" marks the member as participating in the DDS instance key
    // (DDS-XTypes §7.5.1.3). The IS_KEY MemberFlag is set in the emitted
    // TypeObject so that the key-compatibility check fires during type matching.
    let is_key = attrs
        .get("key")
        .map(|v| v.trim().eq_ignore_ascii_case("true"))
        .unwrap_or(false);

    // mustUnderstand="true" marks the member as @must_understand
    // (DDS-XTypes §7.6.3.3). IS_MUST_UNDERSTAND is set in the emitted
    // TypeObject; if a writer sends this member and the reader's type lacks a
    // member with the same ID, the type pair is structurally incompatible.
    let is_must_understand = attrs
        .get("mustunderstand")
        .map(|v| v.trim().eq_ignore_ascii_case("true"))
        .unwrap_or(false);

    RawMember {
        name,
        type_str,
        id,
        sequence_max,
        array_dims,
        string_max,
        optional,
        try_construct,
        hashid,
        is_key,
        is_must_understand,
    }
}

/// Map an XML `tryConstruct` attribute value to [`TryConstructKind`].
///
/// Accepted values (case-insensitive, leading/trailing whitespace stripped):
///   `discard`     → [`TryConstructKind::Discard`]
///   `trim`        → [`TryConstructKind::Trim`]
///   `use_default` → [`TryConstructKind::UseDefault`]
///
/// Any other value (including absent attribute) falls back to `UseDefault`
/// per DDS-XTypes v1.3 §7.5.1.4.
fn try_construct_from_str(s: &str) -> TryConstructKind {
    match s.trim().to_lowercase().as_str() {
        "discard" => TryConstructKind::Discard,
        "trim" => TryConstructKind::Trim,
        "use_default" | "usedefault" => TryConstructKind::UseDefault,
        _ => TryConstructKind::UseDefault,
    }
}

fn parse_int_literal(s: &str) -> Result<i64, String> {
    let s = s.trim();
    if let Some(hex) = s.strip_prefix("0x").or_else(|| s.strip_prefix("0X")) {
        i64::from_str_radix(hex, 16).map_err(|e| e.to_string())
    } else {
        s.parse::<i64>().map_err(|e| e.to_string())
    }
}

/// Map a DDS-XML extensibility attribute value to `Extensibility`.
///
/// Per OMG DDS-XML specification and IDL 4.2 the recognized values are
/// "final", "appendable", and "mutable" (case-insensitive). Any other value
/// falls back to `Appendable` -- the IDL 4.2 / DDS-XTypes v1.3 (7.3.1.2.1.6)
/// default for constructed types without an explicit annotation.
fn extensibility_from_str(s: &str) -> Extensibility {
    match s.to_lowercase().as_str() {
        "final" => Extensibility::Final,
        "mutable" => Extensibility::Mutable,
        _ => Extensibility::Appendable,
    }
}

/// Map an `bitBound` (8/16/32) to a HDDS `PrimitiveKind`. Anything outside
/// the spec range falls back to U32 (the IDL 4.2 default).
fn bit_bound_to_primitive(bit_bound: u8) -> PrimitiveKind {
    match bit_bound {
        8 => PrimitiveKind::U8,
        16 => PrimitiveKind::U16,
        _ => PrimitiveKind::U32,
    }
}

// ---------------------------------------------------------------------------
// Convert raw type to TypeDescriptor
// ---------------------------------------------------------------------------

fn raw_to_descriptor(
    raw: &RawTypeDef,
    all_types: &[RawTypeDef],
    by_qualified: &HashMap<String, usize>,
    by_local: &HashMap<String, usize>,
) -> Result<TypeDescriptor, String> {
    match raw {
        RawTypeDef::Struct {
            name,
            module,
            extensibility,
            autoid_hash,
            members,
        } => {
            let qualified = if module.is_empty() {
                name.clone()
            } else {
                format!("{}::{}", module, name)
            };
            let fields: Result<Vec<FieldDescriptor>, String> = members
                .iter()
                .map(|m| {
                    let td = Arc::new(member_to_type_descriptor(
                        m,
                        all_types,
                        by_qualified,
                        by_local,
                    )?);
                    let mut fd = FieldDescriptor::new(m.name.clone(), td);
                    if let Some(id) = m.id {
                        fd = fd.with_id(id);
                    }
                    if m.optional {
                        fd = fd.optional();
                    }
                    fd = fd.with_try_construct(m.try_construct);
                    if let Some(ref alias) = m.hashid {
                        fd = fd.with_hashid_name(alias.clone());
                    }
                    if m.is_key {
                        fd = fd.with_key();
                    }
                    if m.is_must_understand {
                        fd = fd.with_must_understand();
                    }
                    Ok(fd)
                })
                .collect();
            // Map the XML extensibility attribute to the TypeDescriptor enum.
            // Absent attributes were already defaulted to "appendable" at
            // parse time (IDL 4.2 / DDS-XTypes v1.3 spec default).
            let ext = extensibility_from_str(extensibility);
            let mut td = TypeDescriptor::struct_type(qualified, fields?).with_extensibility(ext);
            if *autoid_hash {
                td = td.with_autoid_hash();
            }
            Ok(td)
        }
        RawTypeDef::Enum {
            name,
            module,
            bit_bound,
            variants,
        } => {
            let qualified = if module.is_empty() {
                name.clone()
            } else {
                format!("{}::{}", module, name)
            };
            // Propagate the bit_bound to the underlying CDR width
            // (F-bitBound). Otherwise vendors which respect a 1-byte
            // encoding will see 3 bytes of misalignment on every following
            // field.
            let enum_desc = EnumDescriptor::new(variants.clone())
                .with_underlying(bit_bound_to_primitive(*bit_bound));
            Ok(TypeDescriptor::new(qualified, TypeKind::Enum(enum_desc)))
        }
        RawTypeDef::Bitmask {
            name,
            module,
            bit_bound,
            flags,
        } => {
            let qualified = if module.is_empty() {
                name.clone()
            } else {
                format!("{}::{}", module, name)
            };
            // Bitmask: each flag at bit position N has value `1 << N`.
            // Represented as an enum so union discriminator resolution and
            // type assignability use the same enum path.
            let variants: Vec<EnumVariant> = flags
                .iter()
                .map(|(flag_name, position)| {
                    EnumVariant::new(flag_name.clone(), 1_i64 << position)
                })
                .collect();
            let enum_desc = EnumDescriptor::new_bitmask(variants)
                .with_underlying(bit_bound_to_primitive(*bit_bound));
            Ok(TypeDescriptor::new(qualified, TypeKind::Enum(enum_desc)))
        }
        RawTypeDef::Union {
            name,
            module,
            extensibility,
            discriminator_type,
            discriminator_try_construct,
            discriminator_is_key,
            cases,
        } => {
            let qualified = if module.is_empty() {
                name.clone()
            } else {
                format!("{}::{}", module, name)
            };
            // Resolve discriminator type — may be a primitive or a defined
            // type such as an enum (DDS-XML `nonBasic`).
            let disc_td = Arc::new(prim_from_str_or_nested_with_bound(
                discriminator_type,
                None,
                all_types,
                by_qualified,
                by_local,
            )?);
            // Separate default case from labeled cases, recording the
            // default's declaration index among ALL cases so the TypeObject
            // emission can keep it at its declared slot with its sequential
            // member id (reference vendors number union members by
            // declaration order, default case included).
            let mut default_case: Option<UnionCase> = None;
            let mut default_case_index: Option<usize> = None;
            let mut regular_cases: Vec<UnionCase> = Vec::new();
            for (decl_idx, c) in cases.iter().enumerate() {
                let case_td = Arc::new(member_to_type_descriptor(
                    &c.member,
                    all_types,
                    by_qualified,
                    by_local,
                )?);
                // Resolve any string-valued caseDiscriminator labels (enum
                // variant names) to their integer values using the
                // discriminator enum type.
                let mut int_labels = c.discriminator_values.clone();
                if !c.discriminator_name_labels.is_empty() {
                    if let TypeKind::Enum(ref e) = disc_td.kind {
                        for label in &c.discriminator_name_labels {
                            if let Some(v) = e.variant(label) {
                                int_labels.push(v.value);
                            }
                            // Unknown name silently skipped; case will only
                            // match if other integer labels are provided.
                        }
                    }
                }
                let mut uc = UnionCase::new(
                    c.member.name.clone(),
                    int_labels,
                    case_td,
                )
                .with_try_construct(c.member.try_construct);
                // Propagate explicit @id(N) / `id` attribute when present so
                // the TypeObject member_id matches the declared annotation, not
                // the declaration-order positional index.
                if let Some(explicit_id) = c.member.id {
                    uc = uc.with_member_id(explicit_id);
                }
                if c.is_default {
                    default_case = Some(uc);
                    default_case_index = Some(decl_idx);
                } else {
                    regular_cases.push(uc);
                }
            }
            let mut union_desc = UnionDescriptor::new(disc_td, regular_cases)
                .with_discriminator_try_construct(*discriminator_try_construct);
            if *discriminator_is_key {
                union_desc = union_desc.with_discriminator_key();
            }
            if let (Some(dc), Some(idx)) = (default_case, default_case_index) {
                union_desc = union_desc.with_default_at(dc, idx);
            }
            let ext = extensibility_from_str(extensibility);
            Ok(TypeDescriptor::new(qualified, TypeKind::Union(union_desc))
                .with_extensibility(ext))
        }
    }
}

fn member_to_type_descriptor(
    m: &RawMember,
    all_types: &[RawTypeDef],
    by_qualified: &HashMap<String, usize>,
    by_local: &HashMap<String, usize>,
) -> Result<TypeDescriptor, String> {
    // Array takes priority over sequence
    if !m.array_dims.is_empty() {
        let elem_kind = prim_from_str_or_nested_with_bound(
            &m.type_str,
            m.string_max,
            all_types,
            by_qualified,
            by_local,
        )?;
        // Struct/union elements must be wrapped in Nested so that
        // descriptor_to_type_identifier_impl can lower them to a Minimal
        // EquivalenceHash TypeIdentifier (XTypes v1.3 §7.3.4.7).
        let elem_kind = match &elem_kind.kind {
            TypeKind::Struct(_) | TypeKind::Union(_) => {
                TypeDescriptor::new("", TypeKind::Nested(Arc::new(elem_kind)))
            }
            _ => elem_kind,
        };
        // Build a single flat ArrayDescriptor with all dimensions stored in
        // `dims` (DDS-XTypes §7.2.2.4.3 array_bound_seq carries all dims).
        // This replaces the previous nested-Array approach which prevented the
        // XTypes bridge from emitting a correct multi-dim TypeIdentifier.
        let dims: Vec<u32> = m.array_dims.iter().map(|&d| d as u32).collect();
        let arr = ArrayDescriptor::multi_dim(Arc::new(elem_kind), dims);
        return Ok(TypeDescriptor::new("", TypeKind::Array(arr)));
    }

    if let Some(seq_max) = m.sequence_max {
        let elem_kind = prim_from_str_or_nested_with_bound(
            &m.type_str,
            m.string_max,
            all_types,
            by_qualified,
            by_local,
        )?;
        // Struct/union elements must be wrapped in Nested so that
        // descriptor_to_type_identifier_impl can lower them to a Minimal
        // EquivalenceHash TypeIdentifier (XTypes v1.3 §7.3.4.7).  Without
        // this the outer sequence TypeObject is None and discovery skips the
        // structural assignability check, causing false OK results.
        let elem_kind = match &elem_kind.kind {
            TypeKind::Struct(_) | TypeKind::Union(_) => {
                TypeDescriptor::new("", TypeKind::Nested(Arc::new(elem_kind)))
            }
            _ => elem_kind,
        };
        let elem_td = Arc::new(elem_kind);
        let seq = if seq_max < 0 {
            SequenceDescriptor::unbounded(elem_td)
        } else {
            SequenceDescriptor::bounded(elem_td, seq_max as usize)
        };
        return Ok(TypeDescriptor::new("", TypeKind::Sequence(seq)));
    }

    // Plain scalar or nested user-defined type
    let td = prim_from_str_or_nested_with_bound(
        &m.type_str,
        m.string_max,
        all_types,
        by_qualified,
        by_local,
    )?;
    // Struct/union members must be wrapped in Nested so that
    // descriptor_to_type_identifier_impl can lower them to a Minimal
    // EquivalenceHash TypeIdentifier (XTypes v1.3 clause 7.3.4.7), exactly
    // like the sequence/array element paths above. Without this the outer
    // type's TypeObject is None and NO TypeInformation is announced at all
    // (driver prints "ERROR: cannot build CompleteTypeObject").
    let td = match &td.kind {
        TypeKind::Struct(_) | TypeKind::Union(_) => {
            TypeDescriptor::new("", TypeKind::Nested(Arc::new(td)))
        }
        _ => td,
    };
    Ok(td)
}

fn prim_from_str_or_nested_with_bound(
    s: &str,
    string_max: Option<usize>,
    all_types: &[RawTypeDef],
    by_qualified: &HashMap<String, usize>,
    by_local: &HashMap<String, usize>,
) -> Result<TypeDescriptor, String> {
    // Strings come with an optional bound (`string<128>` or
    // `stringMaxLength="128"`). Propagate it (F-string_max) so HDDS can
    // enforce the bound on the wire instead of silently emitting an
    // unbounded length.
    let lower = s.to_lowercase();
    if lower == "string" || lower.starts_with("string<") {
        // Inline `string<N>` syntax takes priority if present.
        let inline_max = parse_bounded_string_inline(s);
        let max_length = inline_max.or(string_max);
        return Ok(TypeDescriptor::primitive(
            "",
            PrimitiveKind::String { max_length },
        ));
    }
    if lower == "wstring" || lower.starts_with("wstring<") {
        let inline_max = parse_bounded_wstring_inline(s);
        let max_length = inline_max.or(string_max);
        return Ok(TypeDescriptor::primitive(
            "",
            PrimitiveKind::WString { max_length },
        ));
    }

    // Try primitive
    if let Ok(pk) = prim_from_str(s) {
        return Ok(TypeDescriptor::primitive("", pk));
    }

    // Try looking up as a defined type (enum, struct, union). The qualified
    // map takes priority; the local map is a fallback for IDL files that
    // reference types by their bare name. Lookup also normalizes the
    // module-stripped form so `Test::E1` matches the `E1` we registered
    // when the type lives in module Test.
    if let Some(&idx) = by_qualified
        .get(s)
        .or_else(|| by_local.get(s))
        .or_else(|| {
            // Strip a leading "Test::" / "Foo::" before falling back to the
            // local map: in DDS-XML the user often writes the unqualified
            // name but the type was defined inside a module.
            s.rsplit("::").next().and_then(|tail| by_local.get(tail))
        })
    {
        return raw_to_descriptor(&all_types[idx], all_types, by_qualified, by_local);
    }

    Err(format!(
        "unknown type '{}'; available: {}",
        s,
        all_types
            .iter()
            .map(|t| t.qualified_name())
            .collect::<Vec<_>>()
            .join(", ")
    ))
}

fn parse_bounded_string_inline(s: &str) -> Option<usize> {
    let lower = s.to_lowercase();
    if let Some(rest) = lower.strip_prefix("string<") {
        rest.trim_end_matches('>').parse::<usize>().ok()
    } else {
        None
    }
}

fn parse_bounded_wstring_inline(s: &str) -> Option<usize> {
    let lower = s.to_lowercase();
    if let Some(rest) = lower.strip_prefix("wstring<") {
        rest.trim_end_matches('>').parse::<usize>().ok()
    } else {
        None
    }
}

fn prim_from_str(s: &str) -> Result<PrimitiveKind, String> {
    match s.to_lowercase().as_str() {
        "boolean" | "bool" => Ok(PrimitiveKind::Bool),
        "uint8" | "octet" => Ok(PrimitiveKind::U8),
        "uint16" | "unsigned short" => Ok(PrimitiveKind::U16),
        "uint32" | "unsigned long" => Ok(PrimitiveKind::U32),
        "uint64" | "unsigned long long" => Ok(PrimitiveKind::U64),
        "int8" => Ok(PrimitiveKind::I8),
        "int16" | "short" => Ok(PrimitiveKind::I16),
        "int32" | "long" => Ok(PrimitiveKind::I32),
        "int64" | "long long" => Ok(PrimitiveKind::I64),
        "float32" | "float" => Ok(PrimitiveKind::F32),
        "float64" | "double" => Ok(PrimitiveKind::F64),
        "float128" | "long double" => Ok(PrimitiveKind::LongDouble),
        "char8" | "char" => Ok(PrimitiveKind::Char),
        // IDL 4.2 `byte` is an opaque octet, semantically distinct from `uint8`.
        // DDS-XTypes v1.3 §7.5.1.3 Table 3: TK_BYTE is NOT assignable to TK_UINT8.
        "byte" => Ok(PrimitiveKind::Byte),
        "string" => Ok(PrimitiveKind::String { max_length: None }),
        "wstring" => Ok(PrimitiveKind::WString { max_length: None }),
        _ => Err(format!("not a primitive: '{}'", s)),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn nested_modules_qualify_correctly() {
        let xml = r#"
            <dds><types>
              <module name="A">
                <module name="B">
                  <struct name="T" extensibility="final">
                    <member name="x" type="int32"/>
                  </struct>
                </module>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "A::B::T").expect("nested resolve");
        assert_eq!(td.name, "A::B::T");
    }

    #[test]
    fn bit_bound_propagates_to_enum_underlying() {
        let xml = r#"
            <dds><types>
              <module name="Test">
                <enum name="Small" bitBound="8">
                  <enumerator name="A" value="0"/>
                  <enumerator name="B" value="1"/>
                </enum>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::Small").expect("parse enum");
        match &td.kind {
            TypeKind::Enum(e) => assert_eq!(e.underlying, PrimitiveKind::U8),
            k => panic!("expected Enum, got {:?}", k),
        }
    }

    #[test]
    fn bit_bound_defaults_to_u32() {
        let xml = r#"
            <dds><types>
              <module name="Test">
                <enum name="Color">
                  <enumerator name="R" value="0"/>
                </enum>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::Color").expect("parse");
        match &td.kind {
            TypeKind::Enum(e) => assert_eq!(e.underlying, PrimitiveKind::U32),
            k => panic!("expected Enum, got {:?}", k),
        }
    }

    #[test]
    fn string_max_propagates_via_attribute() {
        let xml = r#"
            <dds><types>
              <module name="Test">
                <struct name="S" extensibility="final">
                  <member name="x" type="string" stringMaxLength="128"/>
                </struct>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::S").expect("parse");
        let f = td.fields().expect("struct")[0].clone();
        match &f.type_desc.kind {
            TypeKind::Primitive(PrimitiveKind::String { max_length }) => {
                assert_eq!(*max_length, Some(128));
            }
            k => panic!("expected bounded String, got {:?}", k),
        }
    }

    #[test]
    fn string_max_propagates_via_inline_syntax() {
        let xml = r#"
            <dds><types>
              <module name="Test">
                <struct name="S" extensibility="final">
                  <member name="x" type="string&lt;64&gt;"/>
                </struct>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::S").expect("parse");
        let f = td.fields().expect("struct")[0].clone();
        match &f.type_desc.kind {
            TypeKind::Primitive(PrimitiveKind::String { max_length }) => {
                assert_eq!(*max_length, Some(64));
            }
            k => panic!("expected bounded String, got {:?}", k),
        }
    }

    #[test]
    fn empty_module_does_not_leak_stack() {
        // A <module name="X"/> by itself used to push and never pop. With
        // the fix it should round-trip cleanly: a later <struct/> stays at
        // top level.
        let xml = r#"
            <dds><types>
              <module name="Empty"/>
              <module name="Real">
                <struct name="S" extensibility="final">
                  <member name="x" type="int32"/>
                </struct>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Real::S").expect("parse");
        assert_eq!(td.name, "Real::S");
    }

    #[test]
    fn local_lookup_first_write_wins() {
        // Two structs with the same local name in different modules. The
        // unqualified lookup should return the first one deterministically.
        let xml = r#"
            <dds><types>
              <module name="A">
                <struct name="T" extensibility="final">
                  <member name="x" type="int32"/>
                </struct>
              </module>
              <module name="B">
                <struct name="T" extensibility="final">
                  <member name="y" type="int32"/>
                </struct>
              </module>
            </types></dds>
        "#;
        // Qualified resolution works for both.
        assert_eq!(parse_type_xml(xml, "A::T").unwrap().name, "A::T");
        assert_eq!(parse_type_xml(xml, "B::T").unwrap().name, "B::T");
        // Unqualified picks A (declared first).
        let td = parse_type_xml(xml, "T").unwrap();
        assert_eq!(td.name, "A::T");
    }

    #[test]
    fn extensibility_attribute_propagates_to_type_descriptor() {
        // The XML extensibility attribute must flow through into
        // TypeDescriptor.extensibility so the bridge and CDR layer can
        // select the correct StructTypeFlag and representation ID.
        use hdds::dynamic::Extensibility;

        let xml = r#"
            <dds><types>
              <module name="Test">
                <struct name="Final" extensibility="final">
                  <member name="x" type="int32"/>
                </struct>
                <struct name="App" extensibility="appendable">
                  <member name="x" type="int32"/>
                </struct>
                <struct name="Mut" extensibility="mutable">
                  <member name="x" type="int32"/>
                </struct>
              </module>
            </types></dds>
        "#;

        let final_td = parse_type_xml(xml, "Test::Final").expect("parse final");
        assert_eq!(final_td.extensibility, Extensibility::Final);

        let app_td = parse_type_xml(xml, "Test::App").expect("parse appendable");
        assert_eq!(app_td.extensibility, Extensibility::Appendable);

        let mut_td = parse_type_xml(xml, "Test::Mut").expect("parse mutable");
        assert_eq!(mut_td.extensibility, Extensibility::Mutable);
    }

    #[test]
    fn extensibility_defaults_to_appendable_when_absent() {
        // IDL 4.2 / DDS-XTypes v1.3 (7.3.1.2.1.6): constructed types with no
        // explicit extensibility annotation are APPENDABLE. This test used to
        // pin the (wrong) "final" default, which diverged from the reference
        // vendors and broke TypeObject hash equivalence.
        use hdds::dynamic::Extensibility;

        let xml = r#"
            <dds><types>
              <module name="Test">
                <struct name="NoExt">
                  <member name="x" type="int32"/>
                </struct>
                <union name="NoExtU">
                  <discriminator type="int32"/>
                  <case><caseDiscriminator value="1"/><member name="x1" type="int32"/></case>
                </union>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::NoExt").expect("parse");
        assert_eq!(td.extensibility, Extensibility::Appendable);
        let ud = parse_type_xml(xml, "Test::NoExtU").expect("parse union");
        assert_eq!(ud.extensibility, Extensibility::Appendable);
    }

    #[test]
    fn union_extensibility_propagates() {
        use hdds::dynamic::{Extensibility, TypeKind};

        let xml = r#"
            <dds><types>
              <module name="Test">
                <union name="U1" extensibility="appendable">
                  <discriminator type="uint32"/>
                  <case><caseDiscriminator value="1"/><member name="x1" type="int32"/></case>
                </union>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::U1").expect("parse union");
        assert_eq!(td.extensibility, Extensibility::Appendable);
        match &td.kind {
            TypeKind::Union(u) => {
                assert_eq!(u.cases.len(), 1);
                assert_eq!(u.cases[0].name, "x1");
                assert_eq!(u.cases[0].labels, vec![1]);
            }
            k => panic!("expected Union, got {:?}", k),
        }
    }

    #[test]
    fn union_default_case_parsed_and_separated() {
        use hdds::dynamic::TypeKind;

        let xml = r#"
            <dds><types>
              <module name="Test">
                <union name="U2" extensibility="appendable">
                  <discriminator type="uint32"/>
                  <case><caseDiscriminator value="5"/><member name="x5" type="uint32"/></case>
                  <case><caseDiscriminator value="default"/><member name="xd" type="uint32"/></case>
                </union>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::U2").expect("parse union with default");
        match &td.kind {
            TypeKind::Union(u) => {
                // The labeled case goes into cases; the default goes into default_case.
                assert_eq!(u.cases.len(), 1, "expected 1 labeled case");
                assert_eq!(u.cases[0].name, "x5");
                assert!(u.default_case.is_some(), "expected a default case");
                assert_eq!(u.default_case.as_ref().unwrap().name, "xd");
            }
            k => panic!("expected Union, got {:?}", k),
        }
    }

    #[test]
    fn nonbasic_member_resolves_to_enum_type() {
        // type="nonBasic" nonBasicTypeName="E1" in a struct member must resolve
        // to the enum type rather than failing with "unknown type 'nonBasic'".
        let xml = r#"
            <dds><types>
              <module name="Test">
                <enum name="E1" bitBound="32" extensibility="appendable">
                  <enumerator name="VAL0" value="0"/>
                  <enumerator name="VAL1" value="1"/>
                </enum>
                <struct name="struct_enum_1" extensibility="mutable">
                  <member name="x1" type="nonBasic" nonBasicTypeName="E1"/>
                </struct>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::struct_enum_1").expect("nonBasic member resolve");
        let fields = td.fields().expect("struct fields");
        assert_eq!(fields.len(), 1);
        match &fields[0].type_desc.kind {
            TypeKind::Enum(e) => assert_eq!(e.variants.len(), 2),
            k => panic!("expected Enum field, got {:?}", k),
        }
    }

    #[test]
    fn nonbasic_member_try_construct_propagates() {
        // tryConstruct on a nonBasic member must reach the FieldDescriptor.
        let xml = r#"
            <dds><types>
              <module name="Test">
                <enum name="E2" bitBound="32" extensibility="appendable">
                  <enumerator name="VAL0" value="0"/>
                  <enumerator name="VAL1" value="1" defaultLiteral="true"/>
                  <enumerator name="VAL2" value="2"/>
                </enum>
                <struct name="struct_enum_2_discard" extensibility="mutable">
                  <member name="x1" type="nonBasic" nonBasicTypeName="E2" tryConstruct="discard"/>
                </struct>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::struct_enum_2_discard").expect("nonBasic tryConstruct");
        let fields = td.fields().expect("struct fields");
        assert_eq!(fields[0].try_construct, TryConstructKind::Discard);
    }

    #[test]
    fn nonbasic_union_case_member_resolves() {
        // type="nonBasic" nonBasicTypeName="E1" in a union case member.
        let xml = r#"
            <dds><types>
              <module name="Test">
                <enum name="E1" bitBound="32" extensibility="appendable">
                  <enumerator name="VAL0" value="0"/>
                  <enumerator name="VAL1" value="1"/>
                </enum>
                <union name="union_enum_1">
                  <discriminator type="uint32"/>
                  <case>
                    <caseDiscriminator value="1"/>
                    <member name="x1" type="nonBasic" nonBasicTypeName="E1"/>
                  </case>
                </union>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::union_enum_1").expect("nonBasic union case");
        match &td.kind {
            TypeKind::Union(u) => {
                assert_eq!(u.cases.len(), 1);
                match &u.cases[0].type_desc.kind {
                    TypeKind::Enum(e) => assert_eq!(e.variants.len(), 2),
                    k => panic!("expected Enum case type, got {:?}", k),
                }
            }
            k => panic!("expected Union, got {:?}", k),
        }
    }

    #[test]
    fn nonbasic_discriminator_with_enum_labels_resolve() {
        // <discriminator type="nonBasic" nonBasicTypeName="E1"/> with
        // caseDiscriminator values as enum variant names.
        let xml = r#"
            <dds><types>
              <module name="Test">
                <enum name="E1" bitBound="32" extensibility="appendable">
                  <enumerator name="VAL0" value="0"/>
                  <enumerator name="VAL1" value="1"/>
                  <enumerator name="VAL2" value="2"/>
                </enum>
                <union name="union_disc_enum_1">
                  <discriminator type="nonBasic" nonBasicTypeName="E1"/>
                  <case><caseDiscriminator value="VAL0"/><member name="x0" type="int32"/></case>
                  <case><caseDiscriminator value="VAL1"/><member name="x1" type="int32"/></case>
                  <case><caseDiscriminator value="VAL2"/><member name="x2" type="int32"/></case>
                </union>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::union_disc_enum_1").expect("enum-disc union resolve");
        match &td.kind {
            TypeKind::Union(u) => {
                assert_eq!(u.cases.len(), 3);
                // Enum variant names must be resolved to integer labels.
                assert_eq!(u.cases[0].labels, vec![0_i64]);
                assert_eq!(u.cases[1].labels, vec![1_i64]);
                assert_eq!(u.cases[2].labels, vec![2_i64]);
            }
            k => panic!("expected Union, got {:?}", k),
        }
    }

    #[test]
    fn autoid_hash_attribute_sets_autoid_hash_on_descriptor() {
        // `autoid="hash"` on a struct element must propagate TypeDescriptor.autoid_hash=true.
        let xml = r#"
            <dds><types>
              <module name="Test">
                <struct name="struct_hashid_1" extensibility="final" autoid="hash">
                  <member name="x1" type="int32"/>
                </struct>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::struct_hashid_1").expect("autoid hash parse");
        assert!(td.autoid_hash, "autoid_hash must be true for autoid='hash'");
    }

    #[test]
    fn autoid_absent_leaves_autoid_hash_false() {
        // Struct without autoid attribute must have autoid_hash=false.
        let xml = r#"
            <dds><types>
              <module name="Test">
                <struct name="S" extensibility="final">
                  <member name="x1" type="int32"/>
                </struct>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::S").expect("parse");
        assert!(!td.autoid_hash, "autoid_hash must be false when autoid is absent");
    }

    #[test]
    fn hashid_attribute_propagates_to_field_descriptor() {
        // `hashid="x1"` on member x2 must propagate to FieldDescriptor.hashid_name="x1".
        // This is the key XML attribute for ext_autoid_1 (struct_hashid_2.x2 gets
        // the same hash-ID as struct_hashid_1.x1 via hashid="x1").
        let xml = r#"
            <dds><types>
              <module name="Test">
                <struct name="struct_hashid_2" extensibility="final" autoid="hash">
                  <member name="x2" type="int32" hashid="x1"/>
                </struct>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::struct_hashid_2").expect("parse hashid");
        assert!(td.autoid_hash, "autoid_hash must be true");
        let fields = td.fields().expect("struct fields");
        assert_eq!(fields.len(), 1);
        assert_eq!(fields[0].name, "x2", "field name must stay x2");
        assert_eq!(
            fields[0].hashid_name.as_deref(),
            Some("x1"),
            "hashid_name must be 'x1'"
        );
    }

    #[test]
    fn hashid_absent_leaves_hashid_name_none() {
        // Member without hashid attribute must have hashid_name=None.
        let xml = r#"
            <dds><types>
              <module name="Test">
                <struct name="S" extensibility="final" autoid="hash">
                  <member name="x1" type="int32"/>
                </struct>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::S").expect("parse");
        let fields = td.fields().expect("struct fields");
        assert!(fields[0].hashid_name.is_none(), "no hashid attr -> hashid_name must be None");
    }

    #[test]
    fn multidim_array_parsed_with_flat_dims() {
        // arrayDimensions="10,2" must produce a single ArrayDescriptor with
        // dims=[10, 2] and length=20, not a nested Array-of-Array structure.
        // This allows the XTypes bridge to emit array_bound_seq=[10,2] directly.
        let xml = r#"
            <dds><types>
              <module name="Test">
                <struct name="int32x10x2" extensibility="final">
                  <member name="x1" type="int32" arrayDimensions="10,2"/>
                </struct>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::int32x10x2").expect("parse multidim");
        let fields = td.fields().expect("struct fields");
        assert_eq!(fields.len(), 1);
        match &fields[0].type_desc.kind {
            TypeKind::Array(arr) => {
                assert_eq!(arr.dims, vec![10u32, 2u32], "dims must be [10, 2]");
                assert_eq!(arr.length, 20, "length must be product 10*2=20");
                // Element must be a plain i32 primitive, not a nested Array.
                assert!(
                    matches!(&arr.element_type.kind, TypeKind::Primitive(PrimitiveKind::I32)),
                    "element type must be i32, not a nested array"
                );
            }
            k => panic!("expected Array, got {:?}", k),
        }
    }

    #[test]
    fn bitmask_parsed_as_enum_with_power_of_two_values() {
        // <bitmask name="B_32" bitBound="32"> with two flags at positions 0 and 1.
        // Must be registered so that a union using it as discriminator can resolve it.
        let xml = r#"
            <dds><types>
              <module name="Test">
                <bitmask name="B_32" bitBound="32">
                    <flag name="B_FLAG_1" value="0"/>
                    <flag name="B_FLAG_2" value="1"/>
                    <flag name="B_FLAG_3" value="2"/>
                </bitmask>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::B_32").expect("bitmask parse");
        match &td.kind {
            TypeKind::Enum(e) => {
                assert_eq!(e.variants.len(), 3, "expected 3 flags");
                assert_eq!(e.variants[0].name, "B_FLAG_1");
                assert_eq!(e.variants[0].value, 1); // 1 << 0
                assert_eq!(e.variants[1].name, "B_FLAG_2");
                assert_eq!(e.variants[1].value, 2); // 1 << 1
                assert_eq!(e.variants[2].name, "B_FLAG_3");
                assert_eq!(e.variants[2].value, 4); // 1 << 2
            }
            k => panic!("expected Enum for bitmask, got {:?}", k),
        }
    }

    #[test]
    fn bitmask_discriminator_union_resolves() {
        // A union with a bitmask discriminator must load successfully.
        // Reproduces the OMG xtypes union_uint32_bitmask32 failure pattern.
        let xml = r#"
            <dds><types>
              <module name="Test">
                <bitmask name="B_16" bitBound="16">
                    <flag name="B_FLAG_1" value="0"/>
                    <flag name="B_FLAG_2" value="1"/>
                </bitmask>
                <union name="union_bitmask16">
                  <discriminator type="nonBasic" nonBasicTypeName="B_16"/>
                  <case><caseDiscriminator value="2"/><member name="x1" type="int16"/></case>
                  <case><caseDiscriminator value="1"/><member name="x2" type="int32"/></case>
                </union>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::union_bitmask16").expect("bitmask discriminator union");
        match &td.kind {
            TypeKind::Union(u) => {
                assert_eq!(u.cases.len(), 2, "expected 2 cases");
                // Discriminator must be an enum (bitmask).
                assert!(
                    matches!(&u.discriminator.kind, TypeKind::Enum(_)),
                    "discriminator must be Enum (bitmask)"
                );
            }
            k => panic!("expected Union, got {:?}", k),
        }
    }

    #[test]
    fn discriminator_key_parsed() {
        // A union with `key="true"` on the discriminator element must set
        // discriminator_is_key=true in the UnionDescriptor.
        // Reproduces the OMG xtypes union_uint32_one_key failure pattern.
        let xml = r#"
            <dds><types>
              <module name="Test">
                <union name="union_uint32_key">
                  <discriminator type="uint32" key="true"/>
                  <case><caseDiscriminator value="2"/><member name="x1" type="int16"/></case>
                  <case><caseDiscriminator value="1"/><member name="x2" type="int32"/></case>
                </union>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::union_uint32_key").expect("key discriminator union");
        match &td.kind {
            TypeKind::Union(u) => {
                assert!(u.discriminator_is_key, "discriminator_is_key must be true");
            }
            k => panic!("expected Union, got {:?}", k),
        }
    }

    #[test]
    fn discriminator_key_absent_defaults_false() {
        // A union without key="true" on the discriminator must have
        // discriminator_is_key=false (the default).
        let xml = r#"
            <dds><types>
              <module name="Test">
                <union name="union_uint32">
                  <discriminator type="uint32"/>
                  <case><caseDiscriminator value="2"/><member name="x1" type="int16"/></case>
                  <case><caseDiscriminator value="1"/><member name="x2" type="int32"/></case>
                </union>
              </module>
            </types></dds>
        "#;
        let td = parse_type_xml(xml, "Test::union_uint32").expect("non-key discriminator union");
        match &td.kind {
            TypeKind::Union(u) => {
                assert!(!u.discriminator_is_key, "discriminator_is_key must be false");
            }
            k => panic!("expected Union, got {:?}", k),
        }
    }
}
