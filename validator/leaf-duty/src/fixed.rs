//! Q16.16 fixed point. No floating point reaches the session state or a
//! pixel, which is what makes two validators produce the same bytes on any
//! CPU. Budlum made the same rule for its consensus constants
//! (`src/consensus/pos.rs`, F-184/185/186).

use std::ops::{Add, Neg, Sub};

pub const FRAC_BITS: u32 = 16;
pub const ONE: i32 = 1 << FRAC_BITS;

/// A signed Q16.16 number. The range is about ±32 768, ten times the panel.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Default)]
pub struct Fx(pub i32);

impl Fx {
    pub const ZERO: Fx = Fx(0);
    pub const ONE: Fx = Fx(ONE);

    pub const fn int(v: i32) -> Fx {
        Fx(v << FRAC_BITS)
    }
    /// `num / den`, rounded toward negative infinity.
    pub fn ratio(num: i64, den: i64) -> Fx {
        Fx(((num << FRAC_BITS).div_euclid(den)) as i32)
    }
    pub fn mul(self, o: Fx) -> Fx {
        Fx(((self.0 as i64 * o.0 as i64) >> FRAC_BITS) as i32)
    }
    pub fn mul_int(self, k: i32) -> Fx {
        Fx(self.0.wrapping_mul(k))
    }
    /// Multiply by `num / 256`, the damping step of a fling.
    pub fn scale256(self, num: i32) -> Fx {
        Fx(((self.0 as i64 * num as i64) >> 8) as i32)
    }
    pub fn floor(self) -> i32 {
        self.0 >> FRAC_BITS
    }
    pub fn ceil(self) -> i32 {
        (self.0 + ONE - 1) >> FRAC_BITS
    }
    pub fn round(self) -> i32 {
        (self.0 + (ONE >> 1)) >> FRAC_BITS
    }
    pub fn clamp(self, lo: Fx, hi: Fx) -> Fx {
        if self < lo {
            lo
        } else if self > hi {
            hi
        } else {
            self
        }
    }
    pub fn to_le_bytes(self) -> [u8; 4] {
        self.0.to_le_bytes()
    }
}

impl Add for Fx {
    type Output = Fx;
    fn add(self, o: Fx) -> Fx {
        Fx(self.0.wrapping_add(o.0))
    }
}
impl Sub for Fx {
    type Output = Fx;
    fn sub(self, o: Fx) -> Fx {
        Fx(self.0.wrapping_sub(o.0))
    }
}
impl Neg for Fx {
    type Output = Fx;
    fn neg(self) -> Fx {
        Fx(self.0.wrapping_neg())
    }
}

/// Exact `round(x / 255)` for `x` in `0..=255*255`, integer only.
#[inline(always)]
pub fn div255(x: u32) -> u32 {
    let x = x + 128;
    (x + (x >> 8)) >> 8
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn div255_is_exact_rounding() {
        for x in 0..=255u32 * 255 {
            let want = (x * 2 + 255) / 510;
            assert_eq!(div255(x), want, "x={x}");
        }
    }

    #[test]
    fn floor_ceil_round() {
        let v = Fx::ratio(5, 2);
        assert_eq!((v.floor(), v.ceil(), v.round()), (2, 3, 3));
        let n = -v;
        assert_eq!((n.floor(), n.ceil()), (-3, -2));
    }
}
