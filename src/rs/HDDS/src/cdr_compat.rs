// SPDX-License-Identifier: Apache-2.0 OR MIT
// Copyright (c) 2025-2026 naskel.com

//! CDR encapsulation header helpers.
//!
//! RTPS DATA submessages carry a 4-byte encapsulation header before the
//! serialized payload (DDS-XTypes v1.3 section 7.6.3.1.2):
//!
//!   Byte 0: 0x00 (reserved)
//!   Byte 1: representation identifier (table below)
//!   Bytes 2-3: options (usually 0x00 0x00)
//!
//! Representation IDs used in the OMG test suite:
//!
//!   | Repr ID | Name                  | Notes                                |
//!   |---------|-----------------------|--------------------------------------|
//!   | 0x00    | CDR_BE                | XCDR1 big-endian                     |
//!   | 0x01    | CDR_LE                | XCDR1 little-endian                  |
//!   | 0x02    | PL_CDR_BE             | XCDR1 with parameter list (mutable)  |
//!   | 0x03    | PL_CDR_LE             | XCDR1 with parameter list (mutable)  |
//!   | 0x06    | CDR2_BE               | XCDR2 plain big-endian               |
//!   | 0x07    | CDR2_LE               | XCDR2 plain little-endian            |
//!   | 0x08    | D_CDR2_BE             | XCDR2 delimited (appendable)         |
//!   | 0x09    | D_CDR2_LE             | XCDR2 delimited (appendable)         |
//!   | 0x0A    | PL_CDR2_BE            | XCDR2 with EMHEADER (mutable)        |
//!   | 0x0B    | PL_CDR2_LE            | XCDR2 with EMHEADER (mutable)        |
//!
//! Extensibility rules (DDS-XTypes v1.3 §7.4.3 Table 12):
//!   - FINAL      → CDR_LE (0x01) or CDR2_LE (0x07) per xcdr_version flag
//!   - APPENDABLE → D_CDR2_LE (0x09) — always XCDR2 delimited, xcdr_version ignored
//!   - MUTABLE    → PL_CDR2_LE (0x0B) — always XCDR2 with EMHEADER, xcdr_version ignored
//!
//! Use `prepend_encapsulation_with_ext` when the type descriptor's extensibility
//! is available (preferred). `prepend_encapsulation` is kept for call-sites that
//! have not yet been updated to thread the extensibility through.

use hdds::dynamic::Extensibility;

/// Prepend DDS CDR encapsulation header, selecting the representation
/// identifier from both the xcdr_version preference AND the type extensibility.
///
/// Extensibility overrides xcdr_version for APPENDABLE and MUTABLE types:
///
/// - `Final`      → CDR_LE (0x01) when xcdr_version == 1, else CDR2_LE (0x07)
/// - `Appendable` → D_CDR2_LE (0x09) regardless of xcdr_version
/// - `Mutable`    → PL_CDR2_LE (0x0B) regardless of xcdr_version
///
/// DDS-XTypes v1.3 §7.4.3 Table 12.
pub fn prepend_encapsulation_with_ext(
    cdr: &[u8],
    xcdr_version: u8,
    ext: Extensibility,
) -> Vec<u8> {
    let repr_id: u8 = match ext {
        Extensibility::Final => {
            if xcdr_version == 1 {
                0x01 // CDR_LE
            } else {
                0x07 // CDR2_LE
            }
        }
        Extensibility::Appendable => 0x09, // D_CDR2_LE
        Extensibility::Mutable => 0x0B,    // PL_CDR2_LE
    };
    build_encapsulation_frame(cdr, repr_id)
}

/// Prepend DDS CDR encapsulation header without extensibility context.
///
/// xcdr_version: 1 selects XCDR1 little-endian (`CDR_LE`, 0x01); any other
/// value selects XCDR2 plain little-endian (`CDR2_LE`, 0x07).
///
/// Callers that know the type descriptor's extensibility should prefer
/// [`prepend_encapsulation_with_ext`] so that APPENDABLE / MUTABLE types
/// emit the correct delimited or EMHEADER representation ID.
pub fn prepend_encapsulation(cdr: &[u8], xcdr_version: u8) -> Vec<u8> {
    let repr_id: u8 = match xcdr_version {
        1 => 0x01, // CDR_LE
        _ => 0x07, // CDR2_LE plain
    };
    build_encapsulation_frame(cdr, repr_id)
}

/// Build the 4-byte encapsulation frame followed by the CDR payload.
fn build_encapsulation_frame(cdr: &[u8], repr_id: u8) -> Vec<u8> {
    let mut out = Vec::with_capacity(4 + cdr.len());
    out.push(0x00);
    out.push(repr_id);
    out.push(0x00);
    out.push(0x00);
    out.extend_from_slice(cdr);
    out
}

/// Strip DDS CDR encapsulation header if present (4 bytes). Returns the
/// payload unchanged if no recognized representation ID is found in
/// byte 1, so callers that receive raw CDR without a header still decode.
pub fn strip_encapsulation(data: &[u8]) -> &[u8] {
    if data.len() >= 4 && data[0] == 0x00 {
        let repr_id = data[1];
        // All representation IDs from the DDS-XTypes v1.3 table.
        if matches!(
            repr_id,
            0x00 | 0x01 | 0x02 | 0x03 | 0x06 | 0x07 | 0x08 | 0x09 | 0x0A | 0x0B
        ) {
            return &data[4..];
        }
    }
    data
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn prepend_xcdr1_le() {
        let p = prepend_encapsulation(&[0xAA, 0xBB], 1);
        assert_eq!(&p[..4], &[0x00, 0x01, 0x00, 0x00]);
        assert_eq!(&p[4..], &[0xAA, 0xBB]);
    }

    #[test]
    fn prepend_xcdr2_le() {
        let p = prepend_encapsulation(&[0xCC], 2);
        assert_eq!(&p[..4], &[0x00, 0x07, 0x00, 0x00]);
    }

    #[test]
    fn strip_passes_through_when_no_header() {
        let raw = [0x42, 0x43, 0x44];
        assert_eq!(strip_encapsulation(&raw), &[0x42, 0x43, 0x44]);
    }

    #[test]
    fn strip_recognizes_all_known_repr_ids() {
        for rid in [0x00, 0x01, 0x02, 0x03, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B] {
            let buf = [0x00, rid, 0x00, 0x00, 0x42];
            let stripped = strip_encapsulation(&buf);
            assert_eq!(stripped, &[0x42], "repr_id 0x{:02X}", rid);
        }
    }

    // -- prepend_encapsulation_with_ext tests ---------------------------------

    #[test]
    fn with_ext_final_xcdr1_emits_cdr_le() {
        // FINAL + xcdr_version=1 → CDR_LE (0x01)
        let p = prepend_encapsulation_with_ext(&[0x01], 1, Extensibility::Final);
        assert_eq!(p[1], 0x01, "expected CDR_LE repr_id");
    }

    #[test]
    fn with_ext_final_xcdr2_emits_cdr2_le() {
        // FINAL + xcdr_version=2 → CDR2_LE (0x07)
        let p = prepend_encapsulation_with_ext(&[0x01], 2, Extensibility::Final);
        assert_eq!(p[1], 0x07, "expected CDR2_LE repr_id");
    }

    #[test]
    fn with_ext_appendable_always_emits_d_cdr2_le() {
        // APPENDABLE must always emit D_CDR2_LE (0x09) per XTypes §7.4.3 Table 12,
        // regardless of the xcdr_version flag.
        for xcdr in [1u8, 2, 3] {
            let p = prepend_encapsulation_with_ext(&[0x01], xcdr, Extensibility::Appendable);
            assert_eq!(
                p[1], 0x09,
                "APPENDABLE must emit D_CDR2_LE (0x09) for xcdr_version={}",
                xcdr
            );
        }
    }

    #[test]
    fn with_ext_mutable_always_emits_pl_cdr2_le() {
        // MUTABLE must always emit PL_CDR2_LE (0x0B) per XTypes §7.4.3 Table 12,
        // regardless of the xcdr_version flag.
        for xcdr in [1u8, 2, 3] {
            let p = prepend_encapsulation_with_ext(&[0x01], xcdr, Extensibility::Mutable);
            assert_eq!(
                p[1], 0x0B,
                "MUTABLE must emit PL_CDR2_LE (0x0B) for xcdr_version={}",
                xcdr
            );
        }
    }
}
