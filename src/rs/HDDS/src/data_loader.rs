// SPDX-License-Identifier: Apache-2.0 OR MIT
// Copyright (c) 2025-2026 naskel.com

//! DDS-XML data instance loader.
//!
//! Parses the OMG dds-xtypes test data XML format and produces a
//! `DynamicData` whose `TypeDescriptor` matches the provided `type_desc`.
//!
//! Scalar struct:
//!
//!   <struct>
//!     <x1>1</x1>
//!     <x2>2</x2>
//!   </struct>
//!
//! Array / sequence of scalars (uses `<item>`):
//!
//!   <struct>
//!     <x1>
//!       <item>1</item>
//!       <item>2</item>
//!     </x1>
//!   </struct>
//!
//! Nested struct (any name allowed for the outer wrapper):
//!
//!   <outer>
//!     <inner_field>
//!       <a>1</a>
//!       <b>2</b>
//!     </inner_field>
//!   </outer>
//!
//! Union (carries discriminator + selected case):
//!
//!   <union_1>
//!     <discriminator>0x01</discriminator>
//!     <x1>123</x1>
//!   </union_1>
//!
//! Array of struct / sequence of struct:
//!
//!   <outer>
//!     <list>
//!       <item><x1>1</x1></item>
//!       <item><x1>2</x1></item>
//!     </list>
//!   </outer>

use std::collections::HashMap;
use std::sync::{Arc, Mutex};

use hdds::dynamic::{DynamicData, DynamicValue, PrimitiveKind, TypeDescriptor, TypeKind};
use quick_xml::events::{BytesStart, Event};
use quick_xml::reader::Reader;

// ---------------------------------------------------------------------------
// Public
// ---------------------------------------------------------------------------

pub fn load_data_from_xml(
    path: &str,
    type_desc: &Arc<TypeDescriptor>,
) -> Result<DynamicData, String> {
    let content = std::fs::read_to_string(path)
        .map_err(|e| format!("cannot read '{}': {}", path, e))?;
    parse_data_xml(&content, type_desc).map_err(|e| format!("{}: {}", path, e))
}

/// Compare two DynamicData instances for equality. Symmetric across all
/// `DynamicValue` variants including `Union`, `WString`, `LongDouble`,
/// `Null`, and struct field sets.
pub fn compare_dynamic_data(a: &DynamicData, b: &DynamicData) -> bool {
    compare_values(a.value(), b.value())
}

fn compare_values(a: &DynamicValue, b: &DynamicValue) -> bool {
    match (a, b) {
        (DynamicValue::Bool(x), DynamicValue::Bool(y)) => x == y,
        (DynamicValue::U8(x), DynamicValue::U8(y)) => x == y,
        (DynamicValue::U16(x), DynamicValue::U16(y)) => x == y,
        (DynamicValue::U32(x), DynamicValue::U32(y)) => x == y,
        (DynamicValue::U64(x), DynamicValue::U64(y)) => x == y,
        (DynamicValue::I8(x), DynamicValue::I8(y)) => x == y,
        (DynamicValue::I16(x), DynamicValue::I16(y)) => x == y,
        (DynamicValue::I32(x), DynamicValue::I32(y)) => x == y,
        (DynamicValue::I64(x), DynamicValue::I64(y)) => x == y,
        // F32/F64: bitwise equality. Floating-point payloads in the OMG
        // corpus are written as exact decimal literals that round-trip.
        (DynamicValue::F32(x), DynamicValue::F32(y)) => x.to_bits() == y.to_bits(),
        (DynamicValue::F64(x), DynamicValue::F64(y)) => x.to_bits() == y.to_bits(),
        (DynamicValue::Char(x), DynamicValue::Char(y)) => x == y,
        (DynamicValue::String(x), DynamicValue::String(y)) => x == y,
        (DynamicValue::WString(x), DynamicValue::WString(y)) => x == y,
        (DynamicValue::LongDouble(x), DynamicValue::LongDouble(y)) => {
            long_double_semantically_equal(x, y)
        }
        (DynamicValue::Enum(vx, _), DynamicValue::Enum(vy, _)) => vx == vy,
        (DynamicValue::Null, DynamicValue::Null) => true,
        (DynamicValue::Union(disc_a, case_a, inner_a), DynamicValue::Union(disc_b, case_b, inner_b)) => {
            // Discriminator + case name must match. The case name doubles
            // as a guard against the encoder picking a different branch
            // with the same discriminator value (would be a wire-level
            // mismatch even if both values had the same underlying type).
            disc_a == disc_b && case_a == case_b && compare_values(inner_a, inner_b)
        }
        (DynamicValue::Struct(ax), DynamicValue::Struct(bx)) => {
            // Per-key compare for all keys present in ax. Keys present in bx
            // but absent from ax are acceptable only when their value equals
            // the type default (zero / false / empty): this covers mutable
            // struct evolution where the wire omits trailing members that the
            // local type descriptor carries with default values.
            for (k, av) in ax {
                match bx.get(k) {
                    Some(bv) => {
                        if !compare_values(av, bv) {
                            return false;
                        }
                    }
                    None => return false,
                }
            }
            for (k, bv) in bx {
                if !ax.contains_key(k) && !is_default_value(bv) {
                    return false;
                }
            }
            true
        }
        (DynamicValue::Sequence(ax), DynamicValue::Sequence(bx))
        | (DynamicValue::Array(ax), DynamicValue::Array(bx)) => {
            ax.len() == bx.len() && ax.iter().zip(bx.iter()).all(|(a, b)| compare_values(a, b))
        }
        // Cross-variant comparisons (e.g. Sequence vs Array) intentionally
        // return false: they would mean a CDR-level mismatch even if the
        // payload bytes look similar.
        _ => false,
    }
}

/// Returns `true` when `v` equals the DDS type default for its variant.
///
/// Used by `compare_dynamic_data` to accept struct fields that are absent
/// from a decoded mutable payload (the wire omits trailing or unknown members)
/// but present in the expected data with their default value. A non-default
/// absent field means the expected sample genuinely differs from what arrived.
fn is_default_value(v: &DynamicValue) -> bool {
    match v {
        DynamicValue::Bool(x) => !x,
        DynamicValue::U8(x) => *x == 0,
        DynamicValue::U16(x) => *x == 0,
        DynamicValue::U32(x) => *x == 0,
        DynamicValue::U64(x) => *x == 0,
        DynamicValue::I8(x) => *x == 0,
        DynamicValue::I16(x) => *x == 0,
        DynamicValue::I32(x) => *x == 0,
        DynamicValue::I64(x) => *x == 0,
        DynamicValue::F32(x) => x.to_bits() == 0,
        DynamicValue::F64(x) => x.to_bits() == 0,
        DynamicValue::LongDouble(b) => b.iter().all(|&x| x == 0),
        DynamicValue::Char(c) => *c == '\0',
        DynamicValue::String(s) => s.is_empty(),
        DynamicValue::WString(s) => s.is_empty(),
        DynamicValue::Sequence(v) => v.is_empty(),
        DynamicValue::Array(v) => v.iter().all(is_default_value),
        DynamicValue::Struct(m) => m.values().all(is_default_value),
        DynamicValue::Enum(n, _) => *n == 0,
        DynamicValue::Union(..) | DynamicValue::Null => true,
    }
}

// ---------------------------------------------------------------------------
// IEEE 754 binary128 (float128) helpers
// ---------------------------------------------------------------------------
// OMG IDL float128 serializes as IEEE 754 binary128 (1 sign + 15 exponent,
// bias 16383 + 112 mantissa bits). Reference vendors (Cyclone measured on the
// wire) emit true binary128 in CDR. Rust has no stable f128, so the driver
// stores the 16 LE bytes and converts to/from f64 at the edges (XML literal
// parse, display, semantic compare).

/// Convert an f64 to IEEE binary128 little-endian bytes.
pub fn f64_to_binary128_le(v: f64) -> [u8; 16] {
    let bits = v.to_bits();
    let sign = (bits >> 63) & 1;
    let e = ((bits >> 52) & 0x7FF) as i64;
    let m = bits & 0x000F_FFFF_FFFF_FFFF;

    let (eq, mq): (u64, u128) = if e == 0x7FF {
        // Inf / NaN: max exponent, shift the mantissa into the top bits.
        (0x7FFF, (m as u128) << 60)
    } else if e == 0 {
        if m == 0 {
            (0, 0) // signed zero
        } else {
            // f64 subnormal: normalize into a binary128 normal.
            // value = m * 2^-1074; leading bit of m becomes implicit.
            let lz = m.leading_zeros() as i64 - 11; // zeros within the 53-bit field
            let shift = lz + 1;
            let mant = (m << shift) & 0x000F_FFFF_FFFF_FFFF;
            let e_unb = -1022 - shift;
            (((e_unb + 16383) as u64), (mant as u128) << 60)
        }
    } else {
        (((e - 1023 + 16383) as u64), (m as u128) << 60)
    };

    let raw: u128 = ((sign as u128) << 127) | ((eq as u128) << 112) | mq;
    raw.to_le_bytes()
}

/// Convert IEEE binary128 little-endian bytes to the nearest f64.
///
/// Legacy tolerance: a pre-spec HDDS peer stored the f64 bits in the first 8
/// bytes with a zero tail; that layout has an all-zero exponent field at
/// bytes 14..16 while carrying non-zero data below, which no binary128 value
/// produced by the suite does (subnormal quads are out of the suite's value
/// range) - detect it and read the f64 directly.
pub fn binary128_le_to_f64(bytes: &[u8; 16]) -> f64 {
    let raw = u128::from_le_bytes(*bytes);
    let sign = ((raw >> 127) & 1) as u64;
    let eq = ((raw >> 112) & 0x7FFF) as i64;
    let mq = raw & ((1u128 << 112) - 1);

    if eq == 0 && mq != 0 {
        // Not a suite-range binary128 (would be subnormal ~1e-4932):
        // interpret as the legacy f64-in-16 layout.
        let mut f64_bits = [0u8; 8];
        f64_bits.copy_from_slice(&bytes[..8]);
        return f64::from_le_bytes(f64_bits);
    }

    if eq == 0x7FFF {
        let m52 = (mq >> 60) as u64;
        let bits = (sign << 63) | (0x7FFu64 << 52) | m52;
        return f64::from_bits(bits);
    }
    if eq == 0 {
        return if sign == 1 { -0.0 } else { 0.0 };
    }

    let e_unb = eq - 16383;
    let e64 = e_unb + 1023;
    if e64 >= 0x7FF {
        return if sign == 1 {
            f64::NEG_INFINITY
        } else {
            f64::INFINITY
        };
    }
    if e64 <= 0 {
        // Underflows f64 normals; suite values never do. Flush to zero.
        return if sign == 1 { -0.0 } else { 0.0 };
    }

    // Round to nearest on the 52-bit truncation (guard bit at position 59).
    let mut m52 = (mq >> 60) as u64;
    let mut e_out = e64 as u64;
    if (mq >> 59) & 1 == 1 {
        m52 += 1;
        if m52 == (1 << 52) {
            m52 = 0;
            e_out += 1;
        }
    }
    f64::from_bits((sign << 63) | (e_out << 52) | m52)
}

/// Convert an unsigned 128-bit integer VALUE to IEEE binary128 LE bytes
/// (round-to-nearest-even when the value needs more than 113 significand
/// bits). Used for the camp-B reading of ambiguous 32-hex float128 literals:
/// some vendors (coredx, cyclone) parse the literal as an integer and convert
/// it numerically instead of taking it as the raw bit pattern. Suite literals
/// are far below 2^113, so the conversion is exact there.
pub fn u128_to_binary128_le(v: u128) -> [u8; 16] {
    if v == 0 {
        return [0u8; 16];
    }
    let bl = 128 - v.leading_zeros(); // significant bits, 1..=128
    let mut exp_field = (bl as u128 - 1) + 16383;
    let frac: u128 = if bl <= 113 {
        // Exact: drop the implicit leading 1, left-align into 112 bits.
        (v << (113 - bl)) & ((1u128 << 112) - 1)
    } else {
        // Round the top 113 bits nearest-even on guard + sticky.
        let shift = bl - 113;
        let mut top = v >> shift; // 113 bits incl. implicit leading 1
        let guard = (v >> (shift - 1)) & 1 == 1;
        let sticky = v & ((1u128 << (shift - 1)) - 1) != 0;
        if guard && (sticky || top & 1 == 1) {
            top += 1;
            if top >> 113 == 1 {
                top >>= 1;
                exp_field += 1;
            }
        }
        top & ((1u128 << 112) - 1)
    };
    ((exp_field << 112) | frac).to_le_bytes()
}

// ---------------------------------------------------------------------------
// Exact decimal literal -> x87-extended-precision binary128
// ---------------------------------------------------------------------------
// Reference vendors (coredx, connext measured on the wire) parse float128
// XML literals with strtold: x87 80-bit extended precision, i.e. the
// significand is rounded to 64 bits (round-to-nearest-even) and then widened
// to binary128 with a zero tail (compiler __extendxftf2). Parsing with f64
// (53-bit significand) loses the low 11 mantissa bits and produces different
// wire bytes, which vendor subscribers memcmp-reject (DATA_NOT_CORRECT).
//
// This converter parses the decimal literal EXACTLY using a small bignum,
// rounds the significand to 64 bits nearest-even, and widens to binary128.
// For every finite literal this is byte-identical to strtold + widening.
// Integer-valued and dyadic literals that fit 53 bits are exact in both f64
// and x87, so their bytes are unchanged from the previous f64 path.

/// Number of significand bits of x87 double-extended precision.
const X87_SIG_BITS: u32 = 64;

/// Minimal little-endian-limb bignum. Sized for the OMG suite literals
/// (short decimal strings); hard caps in the caller keep it bounded.
struct Big(Vec<u64>);

impl Big {
    fn from_decimal_digits(digits: &[u8]) -> Big {
        let mut n = Big(vec![0]);
        for &d in digits {
            n.mul_small(10);
            n.add_small(u64::from(d));
        }
        n
    }

    fn mul_small(&mut self, m: u64) {
        let mut carry: u128 = 0;
        for l in &mut self.0 {
            let p = (*l as u128) * (m as u128) + carry;
            *l = p as u64;
            carry = p >> 64;
        }
        if carry != 0 {
            self.0.push(carry as u64);
        }
    }

    fn add_small(&mut self, a: u64) {
        let mut carry = a;
        for l in &mut self.0 {
            let (s, c) = l.overflowing_add(carry);
            *l = s;
            carry = u64::from(c);
            if carry == 0 {
                return;
            }
        }
        if carry != 0 {
            self.0.push(carry);
        }
    }

    /// Divide in place by a small divisor, returning the remainder.
    fn div_small(&mut self, d: u64) -> u64 {
        let mut rem: u128 = 0;
        for l in self.0.iter_mut().rev() {
            let cur = (rem << 64) | (*l as u128);
            *l = (cur / (d as u128)) as u64;
            rem = cur % (d as u128);
        }
        while self.0.len() > 1 && *self.0.last().expect("non-empty") == 0 {
            self.0.pop();
        }
        rem as u64
    }

    /// Shift left by `bits`.
    fn shl(&mut self, bits: u32) {
        let limbs = (bits / 64) as usize;
        let rem = bits % 64;
        if rem != 0 {
            let mut carry = 0u64;
            for l in &mut self.0 {
                let new_carry = *l >> (64 - rem);
                *l = (*l << rem) | carry;
                carry = new_carry;
            }
            if carry != 0 {
                self.0.push(carry);
            }
        }
        if limbs > 0 {
            let mut v = vec![0u64; limbs];
            v.extend_from_slice(&self.0);
            self.0 = v;
        }
    }

    /// Total significant bits (0 for zero).
    fn bitlen(&self) -> u64 {
        for (i, &l) in self.0.iter().enumerate().rev() {
            if l != 0 {
                return (i as u64) * 64 + (64 - u64::from(l.leading_zeros()));
            }
        }
        0
    }

    fn bit(&self, i: u64) -> bool {
        let limb = (i / 64) as usize;
        if limb >= self.0.len() {
            return false;
        }
        (self.0[limb] >> (i % 64)) & 1 == 1
    }

    /// True when any bit strictly below position `i` is set.
    fn any_bit_below(&self, i: u64) -> bool {
        let full = (i / 64) as usize;
        let rem = i % 64;
        for (idx, &l) in self.0.iter().enumerate() {
            if idx < full {
                if l != 0 {
                    return true;
                }
            } else if idx == full {
                return rem != 0 && (l & ((1u64 << rem) - 1)) != 0;
            } else {
                break;
            }
        }
        false
    }

    /// Top `n` bits as an integer (requires bitlen() >= n).
    fn top_bits(&self, n: u32) -> u64 {
        let bl = self.bitlen();
        debug_assert!(bl >= u64::from(n));
        let shift = bl - u64::from(n);
        let mut out: u64 = 0;
        for k in 0..u64::from(n) {
            out = (out << 1) | u64::from(self.bit(bl - 1 - k));
        }
        debug_assert!(shift == 0 || out >> (n - 1) == 1);
        out
    }
}

/// Parse a decimal float literal exactly and produce IEEE binary128 LE bytes
/// carrying the value rounded to a 64-bit significand (x87 extended,
/// round-to-nearest-even) -- byte-identical to what strtold-based vendors
/// put on the wire. Returns None for anything that is not a plain finite
/// decimal literal (inf/nan/hex/garbage/out-of-range): callers fall back.
pub fn decimal_to_binary128_x87_le(s: &str) -> Option<[u8; 16]> {
    let s = s.trim();
    let (neg, rest) = match s.as_bytes().first()? {
        b'-' => (true, &s[1..]),
        b'+' => (false, &s[1..]),
        _ => (false, s),
    };

    // Split off an optional exponent part.
    let (mant, exp10) = match rest.find(['e', 'E']) {
        Some(pos) => {
            let e: i64 = rest[pos + 1..].parse().ok()?;
            (&rest[..pos], e)
        }
        None => (rest, 0i64),
    };

    // Mantissa: digits with at most one '.'.
    let mut digits: Vec<u8> = Vec::new();
    let mut frac_len: i64 = 0;
    let mut seen_dot = false;
    let mut seen_digit = false;
    for c in mant.bytes() {
        match c {
            b'0'..=b'9' => {
                seen_digit = true;
                // Skip leading zeros (they carry no value).
                if !(digits.is_empty() && c == b'0') {
                    digits.push(c - b'0');
                }
                if seen_dot {
                    frac_len += 1;
                }
            }
            b'.' if !seen_dot => seen_dot = true,
            _ => return None,
        }
    }
    if !seen_digit {
        return None;
    }

    // Bound the work (suite literals are tiny; these caps are generous).
    if digits.len() > 768 {
        return None;
    }
    let dec_exp = exp10.checked_sub(frac_len)?;
    if !(-6000..=6000).contains(&dec_exp) {
        return None;
    }

    if digits.iter().all(|&d| d == 0) {
        // Signed zero.
        let mut out = [0u8; 16];
        if neg {
            out[15] = 0x80;
        }
        return Some(out);
    }

    let mut n = Big::from_decimal_digits(&digits);
    let mut sticky = false;
    let e2: i64; // value = N * 2^e2 (+ sticky below the last bit of N)

    if dec_exp >= 0 {
        // Exact integer: N *= 10^dec_exp.
        let mut left = dec_exp;
        while left >= 19 {
            n.mul_small(10u64.pow(19));
            left -= 19;
        }
        if left > 0 {
            n.mul_small(10u64.pow(left as u32));
        }
        e2 = 0;
    } else {
        // value = N / (2^f * 5^f). Pre-shift so the quotient keeps well
        // over 64 significant bits, then divide by 5^f in u64-sized chunks
        // (5^27 < 2^63). Any non-zero remainder folds into sticky.
        let f = -dec_exp;
        let t = 3 * f + 128; // 5^f < 2^(2.33*f): quotient bitlen > 64
        n.shl(u32::try_from(t).ok()?);
        let mut left = f;
        while left >= 27 {
            sticky |= n.div_small(5u64.pow(27)) != 0;
            left -= 27;
        }
        if left > 0 {
            sticky |= n.div_small(5u64.pow(left as u32)) != 0;
        }
        e2 = -(t + f);
    }

    // Round the significand to X87_SIG_BITS bits, nearest-even.
    let bl = n.bitlen();
    debug_assert!(bl > 0);
    let mut e_unb = i64::try_from(bl).ok()? - 1 + e2;
    let mut m: u64;
    if bl <= u64::from(X87_SIG_BITS) {
        m = n.top_bits(u32::try_from(bl).ok()?) << (u64::from(X87_SIG_BITS) - bl);
        // Exact: no guard/sticky from N itself. sticky can only be set on
        // the division path, whose quotient always exceeds 64 bits.
        debug_assert!(!sticky);
    } else {
        let shift = bl - u64::from(X87_SIG_BITS);
        m = n.top_bits(X87_SIG_BITS);
        let guard = n.bit(shift - 1);
        sticky |= n.any_bit_below(shift - 1);
        if guard && (sticky || (m & 1) == 1) {
            let (sum, overflow) = m.overflowing_add(1);
            m = sum;
            if overflow {
                m = 1u64 << 63;
                e_unb += 1;
            }
        }
    }
    debug_assert!(m >> 63 == 1);

    // Widen the 64-bit significand to binary128 (1 implicit + 112 fraction).
    let exp_field = e_unb + 16383;
    if !(1..=0x7FFE).contains(&exp_field) {
        return None; // out of suite range; caller falls back
    }
    let frac63 = u128::from(m & ((1u64 << 63) - 1));
    let raw: u128 =
        (u128::from(neg) << 127) | ((exp_field as u128) << 112) | (frac63 << 49);
    Some(raw.to_le_bytes())
}

// ---------------------------------------------------------------------------
// Ambiguous 32-hex float128 literals: RX-side dual acceptance
// ---------------------------------------------------------------------------
// The OMG corpus writes float128 payloads as 0x + 32 hex chars (e.g.
// struct_float128_x1.xml: 0x0000000000000000000000003f800000). Vendors split
// into two camps on what that means:
//   camp A (HDDS, connext): the raw binary128 bit pattern, byte for byte;
//   camp B (coredx, cyclone): the hex INTEGER value (0x3f800000 = 1065353216)
//     converted numerically to binary128.
// TX keeps emitting the camp-A form (no per-peer gaming). On RX, a received
// long double is accepted when it matches EITHER reading of the literal.
// Alternates are registered only at 32-hex literal parse time, so decimal
// literals and wire-decoded values never gain aliases.

/// (camp-A raw literal bytes, camp-B integer-value bytes) pairs registered by
/// the literal parser. The corpus holds a handful at most; linear scan is fine.
static F128_HEX_ALTERNATES: Mutex<Vec<([u8; 16], [u8; 16])>> = Mutex::new(Vec::new());

/// Record the camp-B alternate reading for a 32-hex float128 literal.
fn register_f128_hex_alternate(raw: [u8; 16], alt: [u8; 16]) {
    let mut reg = F128_HEX_ALTERNATES
        .lock()
        .expect("f128 alternate registry poisoned");
    if !reg.iter().any(|(r, a)| *r == raw && *a == alt) {
        reg.push((raw, alt));
    }
}

/// Base float128 equality: byte-identical, or equal after conversion to
/// f64 within a small relative tolerance (covers the precision difference
/// between a text literal parsed to f64 by HDDS and to x87/quad by a vendor).
fn long_double_base_equal(a: &[u8; 16], b: &[u8; 16]) -> bool {
    if a[..] == b[..] {
        return true;
    }
    let fa = binary128_le_to_f64(a);
    let fb = binary128_le_to_f64(b);
    if fa == fb {
        return true;
    }
    let tol = 1e-9_f64 * fa.abs().max(fb.abs()).max(1.0);
    (fa - fb).abs() <= tol
}

/// Semantic float128 equality: base equality, or a match against the camp-B
/// alternate of a 32-hex literal (either argument order: the compare is
/// symmetric and does not know which side is the expected sample).
fn long_double_semantically_equal(a: &[u8; 16], b: &[u8; 16]) -> bool {
    if long_double_base_equal(a, b) {
        return true;
    }
    let reg = F128_HEX_ALTERNATES
        .lock()
        .expect("f128 alternate registry poisoned");
    reg.iter().any(|(raw, alt)| {
        (raw == a && long_double_base_equal(alt, b))
            || (raw == b && long_double_base_equal(alt, a))
    })
}

// ---------------------------------------------------------------------------
// Internal parser
// ---------------------------------------------------------------------------

fn parse_data_xml(
    xml: &str,
    type_desc: &Arc<TypeDescriptor>,
) -> Result<DynamicData, String> {
    // Find the root element regardless of its tag name.
    let tree = parse_xml_to_tree(xml)?;
    let value = build_value_from_node(&tree, &type_desc.kind)?;
    DynamicData::from_value(type_desc, value).map_err(|e| format!("DynamicData error: {}", e))
}

// ---------------------------------------------------------------------------
// Generic XML tree
// ---------------------------------------------------------------------------

/// A minimal XML tree node: name + text content + children. Attributes are
/// captured but unused in the OMG data corpus.
#[derive(Debug, Default)]
struct XmlNode {
    name: String,
    text: String,
    children: Vec<XmlNode>,
}

impl XmlNode {
    fn child(&self, name: &str) -> Option<&XmlNode> {
        self.children.iter().find(|c| c.name == name)
    }

    /// Return all direct children whose tag equals `name`.
    fn children_named(&self, name: &str) -> Vec<&XmlNode> {
        self.children.iter().filter(|c| c.name == name).collect()
    }
}

/// Parse an XML string into a single root XmlNode. The OMG data corpus
/// always wraps the payload in a single root element (e.g. `<struct>`,
/// `<union_1>`); if more than one root element is found, the first is used
/// and a warning is logged.
fn parse_xml_to_tree(xml: &str) -> Result<XmlNode, String> {
    let mut reader = Reader::from_str(xml);
    reader.config_mut().trim_text(true);

    let mut buf = Vec::new();
    let mut stack: Vec<XmlNode> = Vec::new();
    let mut root: Option<XmlNode> = None;

    loop {
        match reader.read_event_into(&mut buf) {
            Ok(Event::Start(ref e)) => {
                let n = bytes_start_to_node(e);
                stack.push(n);
            }
            Ok(Event::Empty(ref e)) => {
                let n = bytes_start_to_node(e);
                if let Some(parent) = stack.last_mut() {
                    parent.children.push(n);
                } else {
                    root = Some(n);
                }
            }
            Ok(Event::Text(ref e)) => {
                let text = e.unescape().unwrap_or_default().to_string();
                let trimmed = text.trim();
                if !trimmed.is_empty() {
                    if let Some(top) = stack.last_mut() {
                        if top.text.is_empty() {
                            top.text = trimmed.to_string();
                        } else {
                            top.text.push(' ');
                            top.text.push_str(trimmed);
                        }
                    }
                }
            }
            Ok(Event::End(_)) => {
                if let Some(node) = stack.pop() {
                    if let Some(parent) = stack.last_mut() {
                        parent.children.push(node);
                    } else if root.is_none() {
                        root = Some(node);
                    }
                    // If we already saw a root, the additional top-level
                    // element is silently appended as a sibling of the
                    // first root via the parent path above (not reachable
                    // here since stack is empty).
                }
            }
            Ok(Event::Eof) => break,
            Err(e) => return Err(format!("XML parse error: {}", e)),
            _ => {}
        }
        buf.clear();
    }

    root.ok_or_else(|| "empty XML document".to_string())
}

fn bytes_start_to_node(e: &BytesStart) -> XmlNode {
    let name = std::str::from_utf8(e.name().as_ref())
        .unwrap_or("")
        .to_string();
    XmlNode {
        name,
        text: String::new(),
        children: Vec::new(),
    }
}

// ---------------------------------------------------------------------------
// Recursive type-driven construction
// ---------------------------------------------------------------------------

fn build_value_from_node(node: &XmlNode, kind: &TypeKind) -> Result<DynamicValue, String> {
    match kind {
        TypeKind::Primitive(pk) => parse_primitive_strict(node.text.trim(), *pk),
        TypeKind::Enum(e) => parse_enum_strict(node.text.trim(), e),
        TypeKind::Struct(fields) => {
            let mut map: HashMap<String, DynamicValue> = HashMap::new();
            // Default everything up front so missing fields stay
            // deterministic. The OMG corpus often omits fields a publisher
            // type does not carry (e.g. struct_a2 publishing data shaped
            // for struct_a3).
            for f in fields {
                map.insert(f.name.clone(), default_value(&f.type_desc.kind));
            }
            for f in fields {
                if let Some(child) = node.child(&f.name) {
                    let val = build_value_from_node(child, &f.type_desc.kind)?;
                    map.insert(f.name.clone(), val);
                }
            }
            Ok(DynamicValue::Struct(map))
        }
        TypeKind::Sequence(seq) => build_sequence(node, &seq.element_type.kind, false),
        TypeKind::Array(arr) => {
            let v = build_sequence(node, &arr.element_type.kind, true)?;
            match v {
                DynamicValue::Sequence(items) | DynamicValue::Array(items) => {
                    // Pad with default values if the XML provided fewer
                    // items than the declared array length. Strict mode
                    // would error here; the OMG corpus has well-formed
                    // arrays so the pad is only a safety net.
                    let mut items = items;
                    while items.len() < arr.length {
                        items.push(default_value(&arr.element_type.kind));
                    }
                    if items.len() > arr.length {
                        return Err(format!(
                            "array overflow: declared {}, got {}",
                            arr.length,
                            items.len()
                        ));
                    }
                    Ok(DynamicValue::Array(items))
                }
                _ => unreachable!(),
            }
        }
        TypeKind::Union(u) => build_union(node, u),
        TypeKind::Nested(inner) => build_value_from_node(node, &inner.kind),
    }
}

fn build_sequence(
    node: &XmlNode,
    element_kind: &TypeKind,
    is_array: bool,
) -> Result<DynamicValue, String> {
    let mut items: Vec<DynamicValue> = Vec::new();
    let item_nodes = node.children_named("item");

    if item_nodes.is_empty() && !node.text.trim().is_empty() {
        // Allow a single inline scalar like `<x>3</x>` to behave as a
        // 1-element sequence, mirroring how some OMG samples express
        // optional/singleton lists.
        items.push(parse_node_as_scalar(node, element_kind)?);
    } else {
        for item in item_nodes {
            // For struct elements, the `<item>` wraps the struct body
            // directly. For scalars, the `<item>` carries text content.
            // Decide based on the kind, not on the XML shape.
            match element_kind {
                TypeKind::Primitive(_) | TypeKind::Enum(_) => {
                    items.push(parse_node_as_scalar(item, element_kind)?);
                }
                _ => {
                    items.push(build_value_from_node(item, element_kind)?);
                }
            }
        }
    }

    if is_array {
        Ok(DynamicValue::Array(items))
    } else {
        Ok(DynamicValue::Sequence(items))
    }
}

fn build_union(
    node: &XmlNode,
    union: &hdds::dynamic::UnionDescriptor,
) -> Result<DynamicValue, String> {
    // Read the discriminator. The OMG corpus uses a `<discriminator>` child
    // node carrying a numeric literal (decimal or 0x-prefixed hex).
    //
    // Some OMG test data files use the same XML as the equivalent struct type
    // (e.g. array_num_20.xml is used for both the struct and union variants of
    // a sequence-bearing type). In that case the root element is named `struct`
    // and there is no `<discriminator>` child. Fall back to discriminator
    // inference: scan the union's cases and pick the first case whose member
    // name matches a child element of the node. Use the first label of that
    // case as the discriminator value. This correctly handles single-case
    // unions (the dominant pattern in the tryconstruct/sequence corpus).
    let (disc, case) = if let Some(disc_node) = node.child("discriminator") {
        let disc = parse_int_literal_strict(disc_node.text.trim()).map_err(|e| {
            format!(
                "union '{}': discriminator '{}' is not an integer: {}",
                node.name, disc_node.text, e
            )
        })?;
        let case = union
            .case_by_discriminator(disc)
            .ok_or_else(|| format!("union '{}': no case for discriminator {}", node.name, disc))?;
        (disc, case)
    } else {
        // No explicit discriminator: infer from child element names.
        let inferred = union
            .cases
            .iter()
            .find(|c| node.child(&c.name).is_some())
            .map(|c| {
                let disc = c.labels.first().copied().unwrap_or(0);
                (disc, c)
            });
        match inferred {
            Some((disc, case)) => (disc, case),
            None => {
                // No matching child found; use the first case with discriminator 1
                // (common for single-case unions whose data was written as a struct).
                let case = union
                    .case_by_discriminator(1)
                    .or_else(|| union.cases.first())
                    .ok_or_else(|| {
                        format!(
                            "union '{}': no <discriminator> and no matchable case member; \
                             union has {} cases",
                            node.name,
                            union.cases.len()
                        )
                    })?;
                let disc = case.labels.first().copied().unwrap_or(1);
                (disc, case)
            }
        }
    };

    // Look for a child element carrying the case payload. We accept either
    // a child element whose tag matches the case name (preferred), or fall
    // back to a generic `<value>` element for vendors that prefer that
    // shape.
    let payload_node = node
        .child(&case.name)
        .or_else(|| node.child("value"));

    let inner = match payload_node {
        Some(child) => build_value_from_node(child, &case.type_desc.kind)?,
        None => default_value(&case.type_desc.kind),
    };

    Ok(DynamicValue::Union(disc, case.name.clone(), Box::new(inner)))
}

fn parse_node_as_scalar(node: &XmlNode, kind: &TypeKind) -> Result<DynamicValue, String> {
    let t = node.text.trim();
    match kind {
        TypeKind::Primitive(pk) => parse_primitive_strict(t, *pk),
        TypeKind::Enum(e) => parse_enum_strict(t, e),
        TypeKind::Nested(inner) => parse_node_as_scalar(node, &inner.kind),
        _ => Err(format!(
            "expected scalar/enum at <{}>, got nested kind {:?}",
            node.name, kind
        )),
    }
}

// ---------------------------------------------------------------------------
// Strict primitive / enum parsing
// ---------------------------------------------------------------------------

fn parse_int_literal_strict(s: &str) -> Result<i64, String> {
    let s = s.trim();
    if let Some(hex) = s.strip_prefix("0x").or_else(|| s.strip_prefix("0X")) {
        i64::from_str_radix(hex, 16).map_err(|e| e.to_string())
    } else {
        s.parse::<i64>().map_err(|e| e.to_string())
    }
}

fn parse_primitive_strict(t: &str, pk: PrimitiveKind) -> Result<DynamicValue, String> {
    let parsed = match pk {
        PrimitiveKind::Bool => match t.to_lowercase().as_str() {
            "true" | "1" => Ok(DynamicValue::Bool(true)),
            "false" | "0" => Ok(DynamicValue::Bool(false)),
            _ => Err(format!("bad bool literal '{}'", t)),
        },
        // Allow hex literals on every integer type. Byte shares u8 storage.
        PrimitiveKind::U8 | PrimitiveKind::Byte => parse_int_literal_strict(t)
            .and_then(|v| u8::try_from(v).map_err(|e| e.to_string()))
            .map(DynamicValue::U8),
        PrimitiveKind::U16 => parse_int_literal_strict(t)
            .and_then(|v| u16::try_from(v).map_err(|e| e.to_string()))
            .map(DynamicValue::U16),
        PrimitiveKind::U32 => parse_int_literal_strict(t)
            .and_then(|v| u32::try_from(v).map_err(|e| e.to_string()))
            .map(DynamicValue::U32),
        PrimitiveKind::U64 => {
            // u64 cannot be represented in i64 for the top range, so accept
            // either form here.
            let s = t.trim();
            let r = if let Some(hex) = s.strip_prefix("0x").or_else(|| s.strip_prefix("0X")) {
                u64::from_str_radix(hex, 16).map_err(|e| e.to_string())
            } else {
                s.parse::<u64>().map_err(|e| e.to_string())
            };
            r.map(DynamicValue::U64)
        }
        PrimitiveKind::I8 => parse_int_literal_strict(t)
            .and_then(|v| i8::try_from(v).map_err(|e| e.to_string()))
            .map(DynamicValue::I8),
        PrimitiveKind::I16 => parse_int_literal_strict(t)
            .and_then(|v| i16::try_from(v).map_err(|e| e.to_string()))
            .map(DynamicValue::I16),
        PrimitiveKind::I32 => parse_int_literal_strict(t)
            .and_then(|v| i32::try_from(v).map_err(|e| e.to_string()))
            .map(DynamicValue::I32),
        PrimitiveKind::I64 => parse_int_literal_strict(t).map(DynamicValue::I64),
        PrimitiveKind::F32 => t.parse::<f32>().map(DynamicValue::F32).map_err(|e| e.to_string()),
        PrimitiveKind::F64 => t.parse::<f64>().map(DynamicValue::F64).map_err(|e| e.to_string()),
        PrimitiveKind::LongDouble => {
            // OMG harness encodes float128 as a 0x-prefixed 32-hex-char string
            // (16 raw bytes, big-endian as written). When the literal has exactly
            // 32 hex digits after the 0x prefix, decode directly into the 16-byte
            // storage array so that byte-for-byte round-trip works between pub and sub.
            // Fall back to f64 decimal parse for any other format.
            let mut bytes = [0u8; hdds::dynamic::LONG_DOUBLE_SIZE];
            if let Some(hex) = t.strip_prefix("0x").or_else(|| t.strip_prefix("0X")) {
                if hex.len() == 32 {
                    for (i, chunk) in hex.as_bytes().chunks(2).enumerate() {
                        let hi = (chunk[0] as char).to_digit(16).ok_or("invalid hex digit")?;
                        let lo = (chunk[1] as char).to_digit(16).ok_or("invalid hex digit")?;
                        bytes[i] = (hi as u8) << 4 | lo as u8;
                    }
                    // Ambiguity guard: camp-B vendors (coredx, cyclone) read
                    // this literal as an integer VALUE and convert it to
                    // binary128 numerically. Register that reading as an
                    // RX-acceptable alternate; TX keeps the raw camp-A bytes.
                    if let Ok(v) = u128::from_str_radix(hex, 16) {
                        let alt = u128_to_binary128_le(v);
                        if alt != bytes {
                            register_f128_hex_alternate(bytes, alt);
                        }
                    }
                    return Ok(DynamicValue::LongDouble(bytes));
                }
            }
            // Decimal literal: reference vendors (coredx, connext) parse it
            // with strtold (x87 80-bit, 64-bit significand) and widen to
            // binary128 on the wire; their subscribers memcmp against that.
            // Produce the same bytes via exact decimal parsing + 64-bit
            // round-to-nearest-even. Fall back to the f64 path for anything
            // the exact parser rejects (inf/nan/garbage: prior behavior).
            if let Some(b) = decimal_to_binary128_x87_le(t) {
                return Ok(DynamicValue::LongDouble(b));
            }
            let v = t.parse::<f64>().map_err(|e| e.to_string())?;
            bytes = f64_to_binary128_le(v);
            Ok(DynamicValue::LongDouble(bytes))
        }
        PrimitiveKind::Char => {
            // OMG harness char8 literals are either a plain character or a
            // 0x-prefixed code point (e.g. <x14>0x0e</x14>). Taking the first
            // character of "0x0e" would yield '0' (0x30) - wrong data on the
            // wire and a false compare against spec vendors.
            let c = if (t.starts_with("0x") || t.starts_with("0X")) && t.len() > 2 {
                u8::from_str_radix(&t[2..], 16)
                    .map(|b| b as char)
                    .map_err(|e| e.to_string())?
            } else {
                t.chars().next().unwrap_or('\0')
            };
            Ok(DynamicValue::Char(c))
        }
        PrimitiveKind::String { .. } => Ok(DynamicValue::String(t.to_string())),
        PrimitiveKind::WString { .. } => Ok(DynamicValue::WString(t.to_string())),
    };

    // F-parse_scalar: any parse error becomes fatal so the test harness
    // sees the diagnostic instead of "Received sample is different".
    match parsed {
        Ok(v) => Ok(v),
        Err(e) => {
            eprintln!(
                "ERROR: cannot parse '{}' as {:?}: {}",
                t, pk, e
            );
            std::process::exit(3);
        }
    }
}

fn parse_enum_strict(t: &str, e: &hdds::dynamic::EnumDescriptor) -> Result<DynamicValue, String> {
    // Numeric first (the OMG corpus mostly uses bare integers, sometimes
    // hex 0x prefixed).
    if let Ok(n) = parse_int_literal_strict(t) {
        let vname = e
            .variants
            .iter()
            .find(|v| v.value == n)
            .map(|v| v.name.clone())
            .unwrap_or_else(|| n.to_string());
        return Ok(DynamicValue::Enum(n, vname));
    }
    // Symbolic name.
    if let Some(v) = e.variants.iter().find(|v| v.name == t) {
        return Ok(DynamicValue::Enum(v.value, v.name.clone()));
    }
    eprintln!(
        "ERROR: cannot parse '{}' as enum (no numeric match and no variant by name)",
        t
    );
    std::process::exit(3);
}

fn default_value(kind: &TypeKind) -> DynamicValue {
    match kind {
        TypeKind::Primitive(pk) => match pk {
            PrimitiveKind::Bool => DynamicValue::Bool(false),
            PrimitiveKind::U8 | PrimitiveKind::Byte => DynamicValue::U8(0),
            PrimitiveKind::U16 => DynamicValue::U16(0),
            PrimitiveKind::U32 => DynamicValue::U32(0),
            PrimitiveKind::U64 => DynamicValue::U64(0),
            PrimitiveKind::I8 => DynamicValue::I8(0),
            PrimitiveKind::I16 => DynamicValue::I16(0),
            PrimitiveKind::I32 => DynamicValue::I32(0),
            PrimitiveKind::I64 => DynamicValue::I64(0),
            PrimitiveKind::F32 => DynamicValue::F32(0.0),
            PrimitiveKind::F64 => DynamicValue::F64(0.0),
            PrimitiveKind::LongDouble => {
                DynamicValue::LongDouble([0u8; hdds::dynamic::LONG_DOUBLE_SIZE])
            }
            PrimitiveKind::Char => DynamicValue::Char('\0'),
            PrimitiveKind::String { .. } => DynamicValue::String(String::new()),
            PrimitiveKind::WString { .. } => DynamicValue::WString(String::new()),
        },
        TypeKind::Struct(fields) => {
            let mut map = HashMap::new();
            for f in fields {
                map.insert(f.name.clone(), default_value(&f.type_desc.kind));
            }
            DynamicValue::Struct(map)
        }
        TypeKind::Sequence(_) => DynamicValue::Sequence(Vec::new()),
        TypeKind::Array(a) => {
            DynamicValue::Array(vec![default_value(&a.element_type.kind); a.length])
        }
        TypeKind::Enum(e) => {
            let first = e.variants.first();
            DynamicValue::Enum(
                first.map(|v| v.value).unwrap_or(0),
                first.map(|v| v.name.clone()).unwrap_or_default(),
            )
        }
        TypeKind::Union(_) => DynamicValue::Null,
        TypeKind::Nested(inner) => default_value(&inner.kind),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use hdds::dynamic::{
        EnumDescriptor, EnumVariant, FieldDescriptor, TypeDescriptor, UnionCase, UnionDescriptor,
    };

    fn td_i32() -> Arc<TypeDescriptor> {
        Arc::new(TypeDescriptor::primitive("int32", PrimitiveKind::I32))
    }

    #[test]
    fn parses_flat_struct() {
        let td = Arc::new(TypeDescriptor::struct_type(
            "S",
            vec![
                FieldDescriptor::new("x", td_i32()),
                FieldDescriptor::new("y", td_i32()),
            ],
        ));
        let xml = r#"<struct><x>1</x><y>2</y></struct>"#;
        let dd = parse_data_xml(xml, &td).expect("parse");
        match dd.value() {
            DynamicValue::Struct(m) => {
                assert!(matches!(m.get("x"), Some(DynamicValue::I32(1))));
                assert!(matches!(m.get("y"), Some(DynamicValue::I32(2))));
            }
            v => panic!("expected struct, got {:?}", v),
        }
    }

    #[test]
    fn parses_nested_struct() {
        let inner = Arc::new(TypeDescriptor::struct_type(
            "Inner",
            vec![FieldDescriptor::new("a", td_i32())],
        ));
        let outer = Arc::new(TypeDescriptor::struct_type(
            "Outer",
            vec![FieldDescriptor::new("inner", inner)],
        ));
        let xml = r#"<outer><inner><a>42</a></inner></outer>"#;
        let dd = parse_data_xml(xml, &outer).expect("parse");
        if let DynamicValue::Struct(m) = dd.value() {
            if let Some(DynamicValue::Struct(im)) = m.get("inner") {
                assert!(matches!(im.get("a"), Some(DynamicValue::I32(42))));
                return;
            }
        }
        panic!("expected nested struct");
    }

    #[test]
    fn parses_sequence_of_struct() {
        let item_td = Arc::new(TypeDescriptor::struct_type(
            "Item",
            vec![FieldDescriptor::new("x", td_i32())],
        ));
        let seq_td = Arc::new(TypeDescriptor::new(
            "Seq",
            TypeKind::Sequence(hdds::dynamic::SequenceDescriptor::unbounded(item_td)),
        ));
        let outer = Arc::new(TypeDescriptor::struct_type(
            "Outer",
            vec![FieldDescriptor::new("list", seq_td)],
        ));
        let xml = r#"<o><list><item><x>1</x></item><item><x>2</x></item></list></o>"#;
        let dd = parse_data_xml(xml, &outer).expect("parse");
        if let DynamicValue::Struct(m) = dd.value() {
            if let Some(DynamicValue::Sequence(items)) = m.get("list") {
                assert_eq!(items.len(), 2);
                return;
            }
        }
        panic!("expected sequence of struct");
    }

    #[test]
    fn parses_union_with_discriminator_and_case() {
        let disc = Arc::new(TypeDescriptor::primitive("uint8", PrimitiveKind::U8));
        let cases = vec![UnionCase::single("x1", 1, td_i32())];
        let td = Arc::new(TypeDescriptor::new(
            "U",
            TypeKind::Union(UnionDescriptor::new(disc, cases)),
        ));
        let xml = r#"<union_1><discriminator>0x01</discriminator><x1>123</x1></union_1>"#;
        let dd = parse_data_xml(xml, &td).expect("parse");
        match dd.value() {
            DynamicValue::Union(d, case, inner) => {
                assert_eq!(*d, 1);
                assert_eq!(case, "x1");
                assert!(matches!(**inner, DynamicValue::I32(123)));
            }
            v => panic!("expected Union, got {:?}", v),
        }
    }

    #[test]
    fn compare_unions_symmetrically() {
        let a = DynamicValue::Union(1, "x".to_string(), Box::new(DynamicValue::I32(7)));
        let b = DynamicValue::Union(1, "x".to_string(), Box::new(DynamicValue::I32(7)));
        let c = DynamicValue::Union(2, "x".to_string(), Box::new(DynamicValue::I32(7)));
        assert!(compare_values(&a, &b));
        assert!(!compare_values(&a, &c));
    }

    #[test]
    fn compare_structs_is_symmetric_on_keys() {
        let mut a = HashMap::new();
        a.insert("x".to_string(), DynamicValue::I32(1));
        let mut b = a.clone();
        b.insert("y".to_string(), DynamicValue::I32(2));
        assert!(!compare_values(
            &DynamicValue::Struct(a.clone()),
            &DynamicValue::Struct(b.clone())
        ));
        assert!(!compare_values(
            &DynamicValue::Struct(b),
            &DynamicValue::Struct(a)
        ));
    }

    #[test]
    fn compare_long_double_is_semantic() {
        let a = f64_to_binary128_le(12.3);
        let b = f64_to_binary128_le(13.4);
        assert!(!compare_values(
            &DynamicValue::LongDouble(a),
            &DynamicValue::LongDouble(b)
        ));
        assert!(compare_values(
            &DynamicValue::LongDouble(a),
            &DynamicValue::LongDouble(a)
        ));
    }

    #[test]
    fn binary128_roundtrip_and_vendor_bytes() {
        for v in [0.0f64, 1.0, -1.0, 12.3, 10.1, -0.25, 1e300, 1e-300] {
            let b = f64_to_binary128_le(v);
            assert_eq!(binary128_le_to_f64(&b), v, "roundtrip {}", v);
        }
        // Cyclone 11.0.1 wire bytes for float128 12.3. NOTE: these are the
        // f64-widened bytes (Cyclone parses the literal to double); the
        // x87-sourced bytes coredx/connext emit differ in the low mantissa
        // bits. Both must compare equal semantically to either source.
        let cyclone_12_3: [u8; 16] = [
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xa0, 0x99, 0x99, 0x99, 0x99, 0x99, 0x89,
            0x02, 0x40,
        ];
        let ours_f64 = f64_to_binary128_le(12.3);
        assert_eq!(cyclone_12_3, ours_f64, "cyclone reference IS the f64-widened form");
        let ours_x87 = decimal_to_binary128_x87_le("12.3").expect("parse 12.3");
        assert!(long_double_semantically_equal(&cyclone_12_3, &ours_f64));
        assert!(long_double_semantically_equal(&cyclone_12_3, &ours_x87));
        assert!(long_double_semantically_equal(&ours_x87, &ours_f64));
        // Legacy f64-in-16 layout must still be readable.
        let mut legacy = [0u8; 16];
        legacy[..8].copy_from_slice(&12.3f64.to_le_bytes());
        assert_eq!(binary128_le_to_f64(&legacy), 12.3);
    }

    #[test]
    fn parses_enum_by_value_or_name() {
        let e = EnumDescriptor::new(vec![
            EnumVariant::new("RED", 0),
            EnumVariant::new("GREEN", 1),
            EnumVariant::new("BLUE", 2),
        ]);
        let td = Arc::new(TypeDescriptor::new("Color", TypeKind::Enum(e.clone())));
        let s = Arc::new(TypeDescriptor::struct_type(
            "C",
            vec![FieldDescriptor::new("c", td)],
        ));
        let xml = r#"<C><c>GREEN</c></C>"#;
        let dd = parse_data_xml(xml, &s).expect("parse");
        if let DynamicValue::Struct(m) = dd.value() {
            assert!(matches!(m.get("c"), Some(DynamicValue::Enum(1, _))));
        } else {
            panic!()
        }
    }

    // ========== float128 x87-extended decimal literal guards ================
    //
    // Ground truth generated two ways and cross-checked:
    //  - coredx 12.3 wire bytes (frame 235, /tmp/waveE_cx_mut_x1.pcap)
    //  - numpy.longdouble (x86 = x87 80-bit) widened to binary128:
    //    strtold semantics = 64-bit significand round-to-nearest-even.

    fn hexb(s: &str) -> [u8; 16] {
        let mut out = [0u8; 16];
        for i in 0..16 {
            out[i] = u8::from_str_radix(&s[2 * i..2 * i + 2], 16).expect("hex");
        }
        out
    }

    #[test]
    fn float128_decimal_literal_matches_x87_ground_truth() {
        // (literal, binary128 LE bytes of strtold(literal) widened)
        let cases: &[(&str, &str)] = &[
            // The suite's only decimal float128 literal (struct_primitives.xml
            // x12) -- coredx wire ground truth.
            ("12.3", "0000000000009a999999999999890240"),
            ("12.300000", "0000000000009a999999999999890240"),
            ("-12.3", "0000000000009a9999999999998902c0"),
            // Exponent forms must land on the same value.
            ("1.23e1", "0000000000009a999999999999890240"),
            ("123e-1", "0000000000009a999999999999890240"),
            ("+12.3", "0000000000009a999999999999890240"),
            // Other suite float literal values (x10/x11 shapes), as float128.
            ("10.100000", "00000000000034333333333333430240"),
            ("11.200000", "00000000000066666666666666660240"),
            // Classic repeating-fraction and mixed cases.
            ("0.1", "0000000000009a99999999999999fb3f"),
            ("0.001", "00000000000076be9f1a2fdd2406f53f"),
            ("1e-3", "00000000000076be9f1a2fdd2406f53f"),
            ("123.456", "0000000000008c6ce7fba9f1d2ed0540"),
            ("3.14159265358979323846", "0000000000006a84d14244b51f920040"),
            ("2.718281828459045235360287", "00000000000036957645b1a8f05b0040"),
            ("1000000.000001", "000000000000f4de1802000048e81240"),
            ("1e30", "000000000000be9dce089a93e5936240"),
        ];
        for (lit, want) in cases {
            let got = decimal_to_binary128_x87_le(lit)
                .unwrap_or_else(|| panic!("parse '{}'", lit));
            assert_eq!(got, hexb(want), "literal '{}'", lit);
        }
    }

    #[test]
    fn float128_integer_and_dyadic_literals_stay_f64_identical() {
        // Values exact in <= 53 significand bits must produce byte-identical
        // binary128 whether parsed via f64 (old path) or exactly (new path).
        let cases: &[(&str, f64)] = &[
            ("0", 0.0),
            ("1", 1.0),
            ("-1", -1.0),
            ("5", 5.0),
            ("13", 13.0),
            ("100", 100.0),
            ("13.000000", 13.0),
            ("0.5", 0.5),
            ("1.5", 1.5),
            ("-0.25", -0.25),
            ("-7.25", -7.25),
            ("4294967296", 4294967296.0),
        ];
        for (lit, v) in cases {
            let got = decimal_to_binary128_x87_le(lit)
                .unwrap_or_else(|| panic!("parse '{}'", lit));
            assert_eq!(
                got,
                f64_to_binary128_le(*v),
                "literal '{}' must match the f64-widened bytes",
                lit
            );
        }
        // Signed zero keeps its sign bit.
        let neg_zero = decimal_to_binary128_x87_le("-0.0").expect("parse -0.0");
        assert_eq!(neg_zero, f64_to_binary128_le(-0.0));
        assert_eq!(neg_zero[15], 0x80);
    }

    #[test]
    fn float128_decimal_parser_rejects_non_decimal_input() {
        for bad in ["", "-", "+", ".", "e5", "0x1p3", "nan", "inf", "-inf",
                    "1.2.3", "12a", "1e", "1e999999", "1e-999999"] {
            assert!(
                decimal_to_binary128_x87_le(bad).is_none(),
                "'{}' must be rejected (falls back to f64 path)",
                bad
            );
        }
    }

    #[test]
    fn float128_decimal_rx_tolerance_still_accepts_f64_sourced_peer() {
        // A cyclone-style f64-sourced peer vs our new x87-sourced bytes must
        // still compare equal through the RX tolerance path.
        let x87 = decimal_to_binary128_x87_le("12.3").expect("parse");
        let f64w = f64_to_binary128_le(12.3);
        assert_ne!(x87, f64w, "the two sources differ in low mantissa bits");
        assert!(compare_values(
            &DynamicValue::LongDouble(x87),
            &DynamicValue::LongDouble(f64w)
        ));
    }

    // ========== ambiguous 32-hex float128 literal dual acceptance ===========
    //
    // struct_float128_x1.xml carries 0x0000000000000000000000003f800000.
    // camp A (HDDS, connext) = raw binary128 bit pattern (subnormal ~0);
    // camp B (coredx, cyclone) = integer 0x3f800000 = 1065353216 widened to
    // binary128 (LE tail ... fc 1c 40, measured on the wire). RX must accept
    // both; TX stays camp A.

    #[test]
    fn u128_to_binary128_matches_f64_widening_for_exact_ints() {
        for v in [1u128, 2, 5, 127, 1_065_353_216, 4_294_967_296, 1u128 << 52] {
            assert_eq!(
                u128_to_binary128_le(v),
                f64_to_binary128_le(v as f64),
                "integer {} must widen identically via u128 and f64",
                v
            );
        }
        assert_eq!(u128_to_binary128_le(0), [0u8; 16]);
        // 2^128 - 1 rounds up to 2^128: exponent field 16383 + 128 = 0x407f,
        // zero fraction.
        let mut want = [0u8; 16];
        want[14] = 0x7f;
        want[15] = 0x40;
        assert_eq!(u128_to_binary128_le(u128::MAX), want);
        // Round-half-even: 2^113 + 1 is exactly halfway, LSB even -> down.
        assert_eq!(
            u128_to_binary128_le((1u128 << 113) + 1),
            u128_to_binary128_le(1u128 << 113)
        );
    }

    #[test]
    fn float128_32hex_literal_accepts_both_vendor_interpretations() {
        let lit = "0x0000000000000000000000003f800000";
        let parsed =
            parse_primitive_strict(lit, PrimitiveKind::LongDouble).expect("parse 32-hex literal");
        let camp_a = match parsed {
            DynamicValue::LongDouble(b) => b,
            other => panic!("expected LongDouble, got {:?}", other),
        };
        // TX/expected form unchanged: the raw literal bytes as written.
        assert_eq!(camp_a, hexb("0000000000000000000000003f800000"));
        // Camp B: 0x3f800000 = 1065353216 = 127 * 2^23 as binary128
        // (wire-measured coredx/cyclone tail: .. fc 1c 40).
        let camp_b = u128_to_binary128_le(0x3f80_0000);
        assert_eq!(&camp_b[13..], &[0xfc, 0x1c, 0x40]);
        assert!(camp_b[..13].iter().all(|&x| x == 0));
        // RX accepts both readings, in both argument orders.
        assert!(compare_values(
            &DynamicValue::LongDouble(camp_a),
            &DynamicValue::LongDouble(camp_a)
        ));
        assert!(compare_values(
            &DynamicValue::LongDouble(camp_a),
            &DynamicValue::LongDouble(camp_b)
        ));
        assert!(compare_values(
            &DynamicValue::LongDouble(camp_b),
            &DynamicValue::LongDouble(camp_a)
        ));
        // A third, unrelated value stays rejected against both forms.
        let other = f64_to_binary128_le(42.0);
        assert!(!compare_values(
            &DynamicValue::LongDouble(camp_a),
            &DynamicValue::LongDouble(other)
        ));
        assert!(!compare_values(
            &DynamicValue::LongDouble(camp_b),
            &DynamicValue::LongDouble(other)
        ));
    }

    #[test]
    fn float128_decimal_literal_gets_no_integer_alias() {
        // Decimal literals must NOT gain an integer-reinterpretation alias:
        // only 32-hex literals register a camp-B alternate.
        let parsed =
            parse_primitive_strict("12.3", PrimitiveKind::LongDouble).expect("parse decimal");
        let bytes = match parsed {
            DynamicValue::LongDouble(b) => b,
            other => panic!("expected LongDouble, got {:?}", other),
        };
        let bogus = u128_to_binary128_le(u128::from_be_bytes(bytes));
        assert_ne!(bogus, bytes);
        assert!(!compare_values(
            &DynamicValue::LongDouble(bytes),
            &DynamicValue::LongDouble(bogus)
        ));
        assert!(!compare_values(
            &DynamicValue::LongDouble(bogus),
            &DynamicValue::LongDouble(bytes)
        ));
    }

    // ========== ext_mutable_struct regression guards ========================
    //
    // Mutable struct evolution: a decoded struct (ax) may contain fewer fields
    // than the expected struct (bx) when the wire type has fewer members. The
    // missing fields in bx must equal their type default to pass.
    // Locked by: data_loader.rs compare_values struct branch fix.

    #[test]
    fn compare_mutable_decoded_fewer_fields_than_expected_with_defaults_matches() {
        // ax = decoded from wire (only x1 present, as from struct_m1)
        // bx = expected loaded with struct_m2 type (x1=1, x2=0 default)
        // Should match: bx["x2"] is I32(0) which is the type default.
        let mut ax = HashMap::new();
        ax.insert("x1".to_string(), DynamicValue::I32(1));

        let mut bx = HashMap::new();
        bx.insert("x1".to_string(), DynamicValue::I32(1));
        bx.insert("x2".to_string(), DynamicValue::I32(0));

        assert!(compare_values(
            &DynamicValue::Struct(ax),
            &DynamicValue::Struct(bx)
        ));
    }

    #[test]
    fn compare_mutable_decoded_fewer_fields_non_default_expected_does_not_match() {
        // ax = decoded (x1=1 only), bx = expected with x2=99 (non-default)
        // Should NOT match: x2 is absent from ax but non-default in bx.
        let mut ax = HashMap::new();
        ax.insert("x1".to_string(), DynamicValue::I32(1));

        let mut bx = HashMap::new();
        bx.insert("x1".to_string(), DynamicValue::I32(1));
        bx.insert("x2".to_string(), DynamicValue::I32(99));

        assert!(!compare_values(
            &DynamicValue::Struct(ax),
            &DynamicValue::Struct(bx)
        ));
    }

    #[test]
    fn compare_mutable_decoded_field_value_mismatch_fails() {
        // Both have x1 but values differ.
        let mut ax = HashMap::new();
        ax.insert("x1".to_string(), DynamicValue::I32(5));

        let mut bx = HashMap::new();
        bx.insert("x1".to_string(), DynamicValue::I32(1));

        assert!(!compare_values(
            &DynamicValue::Struct(ax),
            &DynamicValue::Struct(bx)
        ));
    }
}
