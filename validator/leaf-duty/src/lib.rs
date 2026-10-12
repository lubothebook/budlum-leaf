//! # budlum-leaf-duty: research order RG-18
//!
//! The validator Leaf duty of FINAL Part 21, Section 21.5: validators run the
//! Leaf as they run Budlum. Session state is chain state, frames are rendered
//! by a deterministic fixed-point rasteriser, each frame is committed in a
//! hash chain with a signed Merkle root per second, a second validator
//! re-executes a sample bit for bit, a forged frame yields slashing evidence,
//! the re-executor doubles as a hot shadow for a zero-frame handover, and the
//! Leaf countersigns receipts.
//!
//! Types copied from the Budlum tree live in [`mirror`] and [`crypto`].

pub mod app;
pub mod chain;
pub mod crypto;
pub mod device;
pub mod evidence;
pub mod fixed;
pub mod frame;
pub mod mirror;
pub mod raster;
pub mod receipt;
pub mod scene;
pub mod session;
pub mod validator;
