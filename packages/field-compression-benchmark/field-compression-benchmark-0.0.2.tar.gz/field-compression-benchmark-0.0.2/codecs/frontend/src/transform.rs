pub struct InstructionCounterInjecter {
    instruction_counter: walrus::GlobalId,
}

impl InstructionCounterInjecter {
    pub fn inject_into_module(module: &mut walrus::Module) -> walrus::GlobalId {
        let (instruction_counter, _import) =
            module.add_import_global("fcbench", "instruction-counter", walrus::ValType::I64, true);

        for (_, func) in module.funcs.iter_local_mut() {
            let entry = func.entry_block();

            walrus::ir::dfs_pre_order_mut(
                &mut Self {
                    instruction_counter,
                },
                func,
                entry,
            );
        }

        instruction_counter
    }

    const fn instruction_needs_counter_update(instr: &walrus::ir::Instr) -> bool {
        #[allow(clippy::match_same_arms)]
        match instr {
            walrus::ir::Instr::Block(_)
            | walrus::ir::Instr::Loop(_)
            | walrus::ir::Instr::Br(_)
            | walrus::ir::Instr::BrIf(_)
            | walrus::ir::Instr::IfElse(_)
            | walrus::ir::Instr::BrTable(_)
            | walrus::ir::Instr::Return(_) => true,
            // calls must return control flow to continue,
            //  so no counter-saving is necessary
            walrus::ir::Instr::Call(_) | walrus::ir::Instr::CallIndirect(_) => false,
            // unreachable control flow doesn't need to care
            //  about instruction counting
            walrus::ir::Instr::Unreachable(_) => false,
            // no control flow occurs
            walrus::ir::Instr::LocalGet(_)
            | walrus::ir::Instr::LocalSet(_)
            | walrus::ir::Instr::LocalTee(_)
            | walrus::ir::Instr::GlobalGet(_)
            | walrus::ir::Instr::GlobalSet(_)
            | walrus::ir::Instr::Const(_)
            | walrus::ir::Instr::Binop(_)
            | walrus::ir::Instr::Unop(_)
            | walrus::ir::Instr::Select(_)
            | walrus::ir::Instr::Drop(_)
            | walrus::ir::Instr::MemorySize(_)
            | walrus::ir::Instr::MemoryGrow(_)
            | walrus::ir::Instr::MemoryInit(_)
            | walrus::ir::Instr::DataDrop(_)
            | walrus::ir::Instr::MemoryCopy(_)
            | walrus::ir::Instr::MemoryFill(_)
            | walrus::ir::Instr::Load(_)
            | walrus::ir::Instr::Store(_)
            | walrus::ir::Instr::AtomicRmw(_)
            | walrus::ir::Instr::Cmpxchg(_)
            | walrus::ir::Instr::AtomicNotify(_)
            | walrus::ir::Instr::AtomicWait(_)
            | walrus::ir::Instr::AtomicFence(..)
            | walrus::ir::Instr::TableGet(_)
            | walrus::ir::Instr::TableSet(_)
            | walrus::ir::Instr::TableGrow(_)
            | walrus::ir::Instr::TableSize(_)
            | walrus::ir::Instr::TableFill(_)
            | walrus::ir::Instr::RefNull(_)
            | walrus::ir::Instr::RefIsNull(_)
            | walrus::ir::Instr::RefFunc(_)
            | walrus::ir::Instr::V128Bitselect(_)
            | walrus::ir::Instr::I8x16Swizzle(_)
            | walrus::ir::Instr::I8x16Shuffle(_)
            | walrus::ir::Instr::LoadSimd(_)
            | walrus::ir::Instr::TableInit(_)
            | walrus::ir::Instr::ElemDrop(_)
            | walrus::ir::Instr::TableCopy(_) => false,
        }
    }

    fn generate_instruction_counter_update(
        &self,
        delta: i64,
    ) -> impl IntoIterator<Item = (walrus::ir::Instr, walrus::ir::InstrLocId)> {
        [
            (
                walrus::ir::Instr::GlobalGet(walrus::ir::GlobalGet {
                    global: self.instruction_counter,
                }),
                walrus::ir::InstrLocId::default(),
            ),
            (
                walrus::ir::Instr::Const(walrus::ir::Const {
                    value: walrus::ir::Value::I64(delta),
                }),
                walrus::ir::InstrLocId::default(),
            ),
            (
                walrus::ir::Instr::Binop(walrus::ir::Binop {
                    op: walrus::ir::BinaryOp::I64Add,
                }),
                walrus::ir::InstrLocId::default(),
            ),
            (
                walrus::ir::Instr::GlobalSet(walrus::ir::GlobalSet {
                    global: self.instruction_counter,
                }),
                walrus::ir::InstrLocId::default(),
            ),
        ]
    }
}

impl walrus::ir::VisitorMut for InstructionCounterInjecter {
    fn start_instr_seq_mut(&mut self, instr_seq: &mut walrus::ir::InstrSeq) {
        let mut i = 0;

        let mut counter: i64 = 0;

        while let Some((instr, _)) = instr_seq.get(i) {
            counter += 1;

            if Self::instruction_needs_counter_update(instr) {
                for new_instr in self.generate_instruction_counter_update(counter) {
                    instr_seq.insert(i, new_instr);
                    i += 1;
                }

                counter = 0;
            }

            i += 1;
        }

        if counter > 0 {
            instr_seq.extend(self.generate_instruction_counter_update(counter));
        }
    }
}

/// Adapted from cranelift's NaN canonicalisation codegen pass
/// <https://github.com/bytecodealliance/wasmtime/blob/ead6c7cc5dbb876437acbdf429a9190f25b96755/cranelift/codegen/src/nan_canonicalization.rs>
/// Released under the Apache-2.0 WITH LLVM-exception License
///
/// Implementation written referencing:
/// - WebAssembly Core Specification v2 <https://www.w3.org/TR/2024/WD-wasm-core-2-20240219>
/// - The "WebAssembly 128-bit packed SIMD Extension" Specification: <https://github.com/WebAssembly/spec/blob/f8114686035f6ffc358771c822ede3c96bf54cd9/proposals/simd/SIMD.md>
/// - The "Non-trapping Float-to-int Conversions" Extension Specification: <https://github.com/WebAssembly/spec/blob/f8114686035f6ffc358771c822ede3c96bf54cd9/proposals/nontrapping-float-to-int-conversion/Overview.md>
#[allow(clippy::struct_field_names)]
pub struct NaNCanonicaliser {
    stash_f32: walrus::LocalId,
    stash_f64: walrus::LocalId,
    stash_v128: walrus::LocalId,
    result: Result<(), NaNCanonicaliserError>,
}

#[derive(Debug, thiserror::Error)]
pub enum NaNCanonicaliserError {
    #[error("module contains non-deterministic relaxed-simd instructions")]
    RelaxedSimd,
}

impl NaNCanonicaliser {
    // Canonical 32-bit and 64-bit NaN values
    const CANON_NAN_B32: u32 = 0x7FC0_0000;
    const CANON_NAN_B32X4: u128 = 0x7FC0_0000_7FC0_0000_7FC0_0000_7FC0_0000;
    const CANON_NAN_B64: u64 = 0x7FF8_0000_0000_0000;
    const CANON_NAN_B64X2: u128 = 0x7FF8_0000_0000_0000_7FF8_0000_0000_0000;

    pub fn apply_to_module(module: &mut walrus::Module) -> Result<(), NaNCanonicaliserError> {
        let mut visitor = Self {
            stash_f32: module.locals.add(walrus::ValType::F32),
            stash_f64: module.locals.add(walrus::ValType::F64),
            stash_v128: module.locals.add(walrus::ValType::V128),
            result: Ok(()),
        };

        for (_, func) in module.funcs.iter_local_mut() {
            let entry = func.entry_block();

            walrus::ir::dfs_pre_order_mut(&mut visitor, func, entry);

            std::mem::replace(&mut visitor.result, Ok(()))?;
        }

        Ok(())
    }

    const fn may_produce_non_deterministic_nan(
        instr: &walrus::ir::Instr,
    ) -> Result<Option<MaybeNaNKind>, NaNCanonicaliserError> {
        #[allow(clippy::match_same_arms)]
        match instr {
            walrus::ir::Instr::Block(_)
            | walrus::ir::Instr::Loop(_)
            | walrus::ir::Instr::Br(_)
            | walrus::ir::Instr::BrIf(_)
            | walrus::ir::Instr::IfElse(_)
            | walrus::ir::Instr::BrTable(_)
            | walrus::ir::Instr::Return(_)
            | walrus::ir::Instr::Call(_)
            | walrus::ir::Instr::CallIndirect(_)
            | walrus::ir::Instr::Unreachable(_)
            | walrus::ir::Instr::LocalGet(_)
            | walrus::ir::Instr::LocalSet(_)
            | walrus::ir::Instr::LocalTee(_)
            | walrus::ir::Instr::GlobalGet(_)
            | walrus::ir::Instr::GlobalSet(_)
            | walrus::ir::Instr::Const(_) => Ok(None),
            walrus::ir::Instr::Binop(walrus::ir::Binop { op }) => {
                Self::binop_may_produce_non_deterministic_nan(*op)
            },
            walrus::ir::Instr::Unop(walrus::ir::Unop { op }) => {
                Self::unop_may_produce_non_deterministic_nan(*op)
            },
            walrus::ir::Instr::Select(_)
            | walrus::ir::Instr::Drop(_)
            | walrus::ir::Instr::MemorySize(_)
            | walrus::ir::Instr::MemoryGrow(_)
            | walrus::ir::Instr::MemoryInit(_)
            | walrus::ir::Instr::DataDrop(_)
            | walrus::ir::Instr::MemoryCopy(_)
            | walrus::ir::Instr::MemoryFill(_)
            | walrus::ir::Instr::Load(_)
            | walrus::ir::Instr::Store(_)
            | walrus::ir::Instr::AtomicRmw(_)
            | walrus::ir::Instr::Cmpxchg(_)
            | walrus::ir::Instr::AtomicNotify(_)
            | walrus::ir::Instr::AtomicWait(_)
            | walrus::ir::Instr::AtomicFence(..)
            | walrus::ir::Instr::TableGet(_)
            | walrus::ir::Instr::TableSet(_)
            | walrus::ir::Instr::TableGrow(_)
            | walrus::ir::Instr::TableSize(_)
            | walrus::ir::Instr::TableFill(_)
            | walrus::ir::Instr::RefNull(_)
            | walrus::ir::Instr::RefIsNull(_)
            | walrus::ir::Instr::RefFunc(_)
            | walrus::ir::Instr::V128Bitselect(_)
            | walrus::ir::Instr::I8x16Swizzle(_)
            | walrus::ir::Instr::I8x16Shuffle(_)
            | walrus::ir::Instr::LoadSimd(_)
            | walrus::ir::Instr::TableInit(_)
            | walrus::ir::Instr::ElemDrop(_)
            | walrus::ir::Instr::TableCopy(_) => Ok(None),
        }
    }

    #[allow(clippy::too_many_lines)]
    const fn unop_may_produce_non_deterministic_nan(
        unop: walrus::ir::UnaryOp,
    ) -> Result<Option<MaybeNaNKind>, NaNCanonicaliserError> {
        #[allow(clippy::match_same_arms)]
        match unop {
            // integer operations never produce NaNs
            walrus::ir::UnaryOp::I32Eqz
            | walrus::ir::UnaryOp::I32Clz
            | walrus::ir::UnaryOp::I32Ctz
            | walrus::ir::UnaryOp::I32Popcnt
            | walrus::ir::UnaryOp::I64Eqz
            | walrus::ir::UnaryOp::I64Clz
            | walrus::ir::UnaryOp::I64Ctz
            | walrus::ir::UnaryOp::I64Popcnt => Ok(None),
            // fabs and fneg only change the sign bit
            walrus::ir::UnaryOp::F32Abs | walrus::ir::UnaryOp::F32Neg => Ok(None),
            // ceil, floor, trunc, nearest, and sqrt may produce NaNs
            walrus::ir::UnaryOp::F32Ceil
            | walrus::ir::UnaryOp::F32Floor
            | walrus::ir::UnaryOp::F32Trunc
            | walrus::ir::UnaryOp::F32Nearest
            | walrus::ir::UnaryOp::F32Sqrt => Ok(Some(MaybeNaNKind::F32)),
            // fabs and fneg only change the sign bit
            walrus::ir::UnaryOp::F64Abs | walrus::ir::UnaryOp::F64Neg => Ok(None),
            // ceil, floor, trunc, nearest, and sqrt may produce NaNs
            walrus::ir::UnaryOp::F64Ceil
            | walrus::ir::UnaryOp::F64Floor
            | walrus::ir::UnaryOp::F64Trunc
            | walrus::ir::UnaryOp::F64Nearest
            | walrus::ir::UnaryOp::F64Sqrt => Ok(Some(MaybeNaNKind::F64)),
            // integer operations never produce NaNs
            walrus::ir::UnaryOp::I32WrapI64 => Ok(None),
            // f2i truncation operations trap on NaNs and never produce NaNs
            walrus::ir::UnaryOp::I32TruncSF32
            | walrus::ir::UnaryOp::I32TruncUF32
            | walrus::ir::UnaryOp::I32TruncSF64
            | walrus::ir::UnaryOp::I32TruncUF64 => Ok(None),
            // integer operations never produce NaNs
            walrus::ir::UnaryOp::I64ExtendSI32 | walrus::ir::UnaryOp::I64ExtendUI32 => Ok(None),
            // f2i truncation operations trap on NaNs and never produce NaNs
            walrus::ir::UnaryOp::I64TruncSF32
            | walrus::ir::UnaryOp::I64TruncUF32
            | walrus::ir::UnaryOp::I64TruncSF64
            | walrus::ir::UnaryOp::I64TruncUF64 => Ok(None),
            // i2f conversion operations never produce NaNs
            walrus::ir::UnaryOp::F32ConvertSI32
            | walrus::ir::UnaryOp::F32ConvertUI32
            | walrus::ir::UnaryOp::F32ConvertSI64
            | walrus::ir::UnaryOp::F32ConvertUI64 => Ok(None),
            // floating point demotion operations may demote NaNs
            walrus::ir::UnaryOp::F32DemoteF64 => Ok(Some(MaybeNaNKind::F32)),
            // i2f conversion operations never produce NaNs
            walrus::ir::UnaryOp::F64ConvertSI32
            | walrus::ir::UnaryOp::F64ConvertUI32
            | walrus::ir::UnaryOp::F64ConvertSI64
            | walrus::ir::UnaryOp::F64ConvertUI64 => Ok(None),
            // floating point promotion operations may promote NaNs
            walrus::ir::UnaryOp::F64PromoteF32 => Ok(Some(MaybeNaNKind::F64)),
            // reinterpret operations may produce NaNs but they are fully deterministic
            walrus::ir::UnaryOp::I32ReinterpretF32
            | walrus::ir::UnaryOp::I64ReinterpretF64
            | walrus::ir::UnaryOp::F32ReinterpretI32
            | walrus::ir::UnaryOp::F64ReinterpretI64 => Ok(None),
            // integer operations never produce NaNs
            walrus::ir::UnaryOp::I32Extend8S
            | walrus::ir::UnaryOp::I32Extend16S
            | walrus::ir::UnaryOp::I64Extend8S
            | walrus::ir::UnaryOp::I64Extend16S
            | walrus::ir::UnaryOp::I64Extend32S
            | walrus::ir::UnaryOp::I8x16Splat
            | walrus::ir::UnaryOp::I8x16ExtractLaneS { .. }
            | walrus::ir::UnaryOp::I8x16ExtractLaneU { .. }
            | walrus::ir::UnaryOp::I16x8Splat
            | walrus::ir::UnaryOp::I16x8ExtractLaneS { .. }
            | walrus::ir::UnaryOp::I16x8ExtractLaneU { .. }
            | walrus::ir::UnaryOp::I32x4Splat
            | walrus::ir::UnaryOp::I32x4ExtractLane { .. }
            | walrus::ir::UnaryOp::I64x2Splat
            | walrus::ir::UnaryOp::I64x2ExtractLane { .. } => Ok(None),
            // floating point splat and extract only duplicate values
            //  and are thus fully deterministic
            walrus::ir::UnaryOp::F32x4Splat
            | walrus::ir::UnaryOp::F32x4ExtractLane { .. }
            | walrus::ir::UnaryOp::F64x2Splat
            | walrus::ir::UnaryOp::F64x2ExtractLane { .. } => Ok(None),
            // integer operations never produce NaNs
            walrus::ir::UnaryOp::V128Not
            | walrus::ir::UnaryOp::V128AnyTrue
            | walrus::ir::UnaryOp::I8x16Abs
            | walrus::ir::UnaryOp::I8x16Popcnt
            | walrus::ir::UnaryOp::I8x16Neg
            | walrus::ir::UnaryOp::I8x16AllTrue
            | walrus::ir::UnaryOp::I8x16Bitmask
            | walrus::ir::UnaryOp::I16x8Abs
            | walrus::ir::UnaryOp::I16x8Neg
            | walrus::ir::UnaryOp::I16x8AllTrue
            | walrus::ir::UnaryOp::I16x8Bitmask
            | walrus::ir::UnaryOp::I32x4Abs
            | walrus::ir::UnaryOp::I32x4Neg
            | walrus::ir::UnaryOp::I32x4AllTrue
            | walrus::ir::UnaryOp::I32x4Bitmask
            | walrus::ir::UnaryOp::I64x2Abs
            | walrus::ir::UnaryOp::I64x2Neg
            | walrus::ir::UnaryOp::I64x2AllTrue
            | walrus::ir::UnaryOp::I64x2Bitmask => Ok(None),
            // fabs and fneg only change the sign bit
            walrus::ir::UnaryOp::F32x4Abs | walrus::ir::UnaryOp::F32x4Neg => Ok(None),
            // ceil, floor, trunc, nearest, and sqrt may produce NaNs
            walrus::ir::UnaryOp::F32x4Sqrt
            | walrus::ir::UnaryOp::F32x4Ceil
            | walrus::ir::UnaryOp::F32x4Floor
            | walrus::ir::UnaryOp::F32x4Trunc
            | walrus::ir::UnaryOp::F32x4Nearest => Ok(Some(MaybeNaNKind::F32x4)),
            // relaxed fma is non-deterministic in its precision
            walrus::ir::UnaryOp::F32x4FmaRelaxed | walrus::ir::UnaryOp::F32x4FmsRelaxed => {
                Err(NaNCanonicaliserError::RelaxedSimd)
            },
            // relaxed min and max are non-deterministic if inputs are NaN, -0.0, or +0.0
            walrus::ir::UnaryOp::F32x4MinRelaxed | walrus::ir::UnaryOp::F32x4MaxRelaxed => {
                Err(NaNCanonicaliserError::RelaxedSimd)
            },
            // fabs and fneg only change the sign bit
            walrus::ir::UnaryOp::F64x2Abs | walrus::ir::UnaryOp::F64x2Neg => Ok(None),
            // ceil, floor, trunc, nearest, and sqrt may produce NaNs
            walrus::ir::UnaryOp::F64x2Sqrt
            | walrus::ir::UnaryOp::F64x2Ceil
            | walrus::ir::UnaryOp::F64x2Floor
            | walrus::ir::UnaryOp::F64x2Trunc
            | walrus::ir::UnaryOp::F64x2Nearest => Ok(Some(MaybeNaNKind::F64x2)),
            // integer operations never produce NaNs
            walrus::ir::UnaryOp::I16x8ExtAddPairwiseI8x16S
            | walrus::ir::UnaryOp::I16x8ExtAddPairwiseI8x16U
            | walrus::ir::UnaryOp::I32x4ExtAddPairwiseI16x8S
            | walrus::ir::UnaryOp::I32x4ExtAddPairwiseI16x8U => Ok(None),
            // relaxted saturating f2i conversions are non-deterministic if the values are
            //  NaN or outside the integer type bounds
            walrus::ir::UnaryOp::I32x4TruncSatF32x4SRelaxed
            | walrus::ir::UnaryOp::I32x4TruncSatF32x4URelaxed
            | walrus::ir::UnaryOp::I32x4TruncSatF64x2SZeroRelaxed
            | walrus::ir::UnaryOp::I32x4TruncSatF64x2UZeroRelaxed => {
                Err(NaNCanonicaliserError::RelaxedSimd)
            },
            // integer operations never produce NaNs
            walrus::ir::UnaryOp::I64x2ExtendLowI32x4S
            | walrus::ir::UnaryOp::I64x2ExtendHighI32x4S
            | walrus::ir::UnaryOp::I64x2ExtendLowI32x4U
            | walrus::ir::UnaryOp::I64x2ExtendHighI32x4U => Ok(None),
            // saturating f2i truncation operations saturate on NaNs and never produce NaNs
            walrus::ir::UnaryOp::I32x4TruncSatF64x2SZero
            | walrus::ir::UnaryOp::I32x4TruncSatF64x2UZero => Ok(None),
            // i2f conversion operations never produce NaNs
            walrus::ir::UnaryOp::F64x2ConvertLowI32x4S
            | walrus::ir::UnaryOp::F64x2ConvertLowI32x4U => Ok(None),
            // floating point demotion operations may demote NaNs
            walrus::ir::UnaryOp::F32x4DemoteF64x2Zero => Ok(Some(MaybeNaNKind::F32x4)),
            // floating point promotion operations may promote NaNs
            walrus::ir::UnaryOp::F64x2PromoteLowF32x4 => Ok(Some(MaybeNaNKind::F64x2)),
            // saturating f2i truncation operations saturate on NaNs and never produce NaNs
            walrus::ir::UnaryOp::I32x4TruncSatF32x4S | walrus::ir::UnaryOp::I32x4TruncSatF32x4U => {
                Ok(None)
            },
            // i2f conversion operations never produce NaNs
            walrus::ir::UnaryOp::F32x4ConvertI32x4S | walrus::ir::UnaryOp::F32x4ConvertI32x4U => {
                Ok(None)
            },
            // saturating f2i truncation operations saturate on NaNs and never produce NaNs
            walrus::ir::UnaryOp::I32TruncSSatF32
            | walrus::ir::UnaryOp::I32TruncUSatF32
            | walrus::ir::UnaryOp::I32TruncSSatF64
            | walrus::ir::UnaryOp::I32TruncUSatF64
            | walrus::ir::UnaryOp::I64TruncSSatF32
            | walrus::ir::UnaryOp::I64TruncUSatF32
            | walrus::ir::UnaryOp::I64TruncSSatF64
            | walrus::ir::UnaryOp::I64TruncUSatF64 => Ok(None),
            // integer operations never produce NaNs
            walrus::ir::UnaryOp::I16x8WidenLowI8x16S
            | walrus::ir::UnaryOp::I16x8WidenLowI8x16U
            | walrus::ir::UnaryOp::I16x8WidenHighI8x16S
            | walrus::ir::UnaryOp::I16x8WidenHighI8x16U
            | walrus::ir::UnaryOp::I32x4WidenLowI16x8S
            | walrus::ir::UnaryOp::I32x4WidenLowI16x8U
            | walrus::ir::UnaryOp::I32x4WidenHighI16x8S
            | walrus::ir::UnaryOp::I32x4WidenHighI16x8U => Ok(None),
        }
    }

    #[allow(clippy::too_many_lines)]
    const fn binop_may_produce_non_deterministic_nan(
        binop: walrus::ir::BinaryOp,
    ) -> Result<Option<MaybeNaNKind>, NaNCanonicaliserError> {
        #[allow(clippy::match_same_arms)]
        match binop {
            // integer operations never produce NaNs
            walrus::ir::BinaryOp::I32Eq
            | walrus::ir::BinaryOp::I32Ne
            | walrus::ir::BinaryOp::I32LtS
            | walrus::ir::BinaryOp::I32LtU
            | walrus::ir::BinaryOp::I32GtS
            | walrus::ir::BinaryOp::I32GtU
            | walrus::ir::BinaryOp::I32LeS
            | walrus::ir::BinaryOp::I32LeU
            | walrus::ir::BinaryOp::I32GeS
            | walrus::ir::BinaryOp::I32GeU
            | walrus::ir::BinaryOp::I64Eq
            | walrus::ir::BinaryOp::I64Ne
            | walrus::ir::BinaryOp::I64LtS
            | walrus::ir::BinaryOp::I64LtU
            | walrus::ir::BinaryOp::I64GtS
            | walrus::ir::BinaryOp::I64GtU
            | walrus::ir::BinaryOp::I64LeS
            | walrus::ir::BinaryOp::I64LeU
            | walrus::ir::BinaryOp::I64GeS
            | walrus::ir::BinaryOp::I64GeU => Ok(None),
            // floating point comparison operations never produce NaNs
            walrus::ir::BinaryOp::F32Eq
            | walrus::ir::BinaryOp::F32Ne
            | walrus::ir::BinaryOp::F32Lt
            | walrus::ir::BinaryOp::F32Gt
            | walrus::ir::BinaryOp::F32Le
            | walrus::ir::BinaryOp::F32Ge
            | walrus::ir::BinaryOp::F64Eq
            | walrus::ir::BinaryOp::F64Ne
            | walrus::ir::BinaryOp::F64Lt
            | walrus::ir::BinaryOp::F64Gt
            | walrus::ir::BinaryOp::F64Le
            | walrus::ir::BinaryOp::F64Ge => Ok(None),
            // integer operations never produce NaNs
            walrus::ir::BinaryOp::I32Add
            | walrus::ir::BinaryOp::I32Sub
            | walrus::ir::BinaryOp::I32Mul
            | walrus::ir::BinaryOp::I32DivS
            | walrus::ir::BinaryOp::I32DivU
            | walrus::ir::BinaryOp::I32RemS
            | walrus::ir::BinaryOp::I32RemU
            | walrus::ir::BinaryOp::I32And
            | walrus::ir::BinaryOp::I32Or
            | walrus::ir::BinaryOp::I32Xor
            | walrus::ir::BinaryOp::I32Shl
            | walrus::ir::BinaryOp::I32ShrS
            | walrus::ir::BinaryOp::I32ShrU
            | walrus::ir::BinaryOp::I32Rotl
            | walrus::ir::BinaryOp::I32Rotr
            | walrus::ir::BinaryOp::I64Add
            | walrus::ir::BinaryOp::I64Sub
            | walrus::ir::BinaryOp::I64Mul
            | walrus::ir::BinaryOp::I64DivS
            | walrus::ir::BinaryOp::I64DivU
            | walrus::ir::BinaryOp::I64RemS
            | walrus::ir::BinaryOp::I64RemU
            | walrus::ir::BinaryOp::I64And
            | walrus::ir::BinaryOp::I64Or
            | walrus::ir::BinaryOp::I64Xor
            | walrus::ir::BinaryOp::I64Shl
            | walrus::ir::BinaryOp::I64ShrS
            | walrus::ir::BinaryOp::I64ShrU
            | walrus::ir::BinaryOp::I64Rotl
            | walrus::ir::BinaryOp::I64Rotr => Ok(None),
            // fadd, fsub, fmul, fdiv, fmin, and fmax may produce NaNs
            walrus::ir::BinaryOp::F32Add
            | walrus::ir::BinaryOp::F32Sub
            | walrus::ir::BinaryOp::F32Mul
            | walrus::ir::BinaryOp::F32Div
            | walrus::ir::BinaryOp::F32Min
            | walrus::ir::BinaryOp::F32Max => Ok(Some(MaybeNaNKind::F32)),
            // copysign only changes the sign bit
            walrus::ir::BinaryOp::F32Copysign => Ok(None),
            // fadd, fsub, fmul, fdiv, fmin, and fmax may produce NaNs
            walrus::ir::BinaryOp::F64Add
            | walrus::ir::BinaryOp::F64Sub
            | walrus::ir::BinaryOp::F64Mul
            | walrus::ir::BinaryOp::F64Div
            | walrus::ir::BinaryOp::F64Min
            | walrus::ir::BinaryOp::F64Max => Ok(Some(MaybeNaNKind::F64)),
            // copysign only changes the sign bit
            walrus::ir::BinaryOp::F64Copysign => Ok(None),
            // integer operations never produce NaNs
            walrus::ir::BinaryOp::I8x16ReplaceLane { .. }
            | walrus::ir::BinaryOp::I16x8ReplaceLane { .. }
            | walrus::ir::BinaryOp::I32x4ReplaceLane { .. }
            | walrus::ir::BinaryOp::I64x2ReplaceLane { .. } => Ok(None),
            // floating point replace only duplicates a value
            //  and is thus fully deterministic
            walrus::ir::BinaryOp::F32x4ReplaceLane { .. }
            | walrus::ir::BinaryOp::F64x2ReplaceLane { .. } => Ok(None),
            // relaxed lane selection is non-deterministic if the mask is not
            //  all ones or all zeros per lane
            walrus::ir::BinaryOp::I8x16RelaxedLaneselect
            | walrus::ir::BinaryOp::I16x8RelaxedLaneselect
            | walrus::ir::BinaryOp::I32x4RelaxedLaneselect
            | walrus::ir::BinaryOp::I64x2RelaxedLaneselect => {
                Err(NaNCanonicaliserError::RelaxedSimd)
            },
            // integer operations never produce NaNs
            walrus::ir::BinaryOp::I8x16Eq
            | walrus::ir::BinaryOp::I8x16Ne
            | walrus::ir::BinaryOp::I8x16LtS
            | walrus::ir::BinaryOp::I8x16LtU
            | walrus::ir::BinaryOp::I8x16GtS
            | walrus::ir::BinaryOp::I8x16GtU
            | walrus::ir::BinaryOp::I8x16LeS
            | walrus::ir::BinaryOp::I8x16LeU
            | walrus::ir::BinaryOp::I8x16GeS
            | walrus::ir::BinaryOp::I8x16GeU
            | walrus::ir::BinaryOp::I16x8Eq
            | walrus::ir::BinaryOp::I16x8Ne
            | walrus::ir::BinaryOp::I16x8LtS
            | walrus::ir::BinaryOp::I16x8LtU
            | walrus::ir::BinaryOp::I16x8GtS
            | walrus::ir::BinaryOp::I16x8GtU
            | walrus::ir::BinaryOp::I16x8LeS
            | walrus::ir::BinaryOp::I16x8LeU
            | walrus::ir::BinaryOp::I16x8GeS
            | walrus::ir::BinaryOp::I16x8GeU
            | walrus::ir::BinaryOp::I32x4Eq
            | walrus::ir::BinaryOp::I32x4Ne
            | walrus::ir::BinaryOp::I32x4LtS
            | walrus::ir::BinaryOp::I32x4LtU
            | walrus::ir::BinaryOp::I32x4GtS
            | walrus::ir::BinaryOp::I32x4GtU
            | walrus::ir::BinaryOp::I32x4LeS
            | walrus::ir::BinaryOp::I32x4LeU
            | walrus::ir::BinaryOp::I32x4GeS
            | walrus::ir::BinaryOp::I32x4GeU
            | walrus::ir::BinaryOp::I64x2Eq
            | walrus::ir::BinaryOp::I64x2Ne
            | walrus::ir::BinaryOp::I64x2LtS
            | walrus::ir::BinaryOp::I64x2GtS
            | walrus::ir::BinaryOp::I64x2LeS
            | walrus::ir::BinaryOp::I64x2GeS => Ok(None),
            // floating point comparison operations never produce NaNs
            walrus::ir::BinaryOp::F32x4Eq
            | walrus::ir::BinaryOp::F32x4Ne
            | walrus::ir::BinaryOp::F32x4Lt
            | walrus::ir::BinaryOp::F32x4Gt
            | walrus::ir::BinaryOp::F32x4Le
            | walrus::ir::BinaryOp::F32x4Ge
            | walrus::ir::BinaryOp::F64x2Eq
            | walrus::ir::BinaryOp::F64x2Ne
            | walrus::ir::BinaryOp::F64x2Lt
            | walrus::ir::BinaryOp::F64x2Gt
            | walrus::ir::BinaryOp::F64x2Le
            | walrus::ir::BinaryOp::F64x2Ge => Ok(None),
            // integer operations never produce NaNs
            walrus::ir::BinaryOp::V128And
            | walrus::ir::BinaryOp::V128Or
            | walrus::ir::BinaryOp::V128Xor
            | walrus::ir::BinaryOp::V128AndNot
            | walrus::ir::BinaryOp::I8x16Shl
            | walrus::ir::BinaryOp::I8x16ShrS
            | walrus::ir::BinaryOp::I8x16ShrU
            | walrus::ir::BinaryOp::I8x16Add
            | walrus::ir::BinaryOp::I8x16AddSatS
            | walrus::ir::BinaryOp::I8x16AddSatU
            | walrus::ir::BinaryOp::I8x16Sub
            | walrus::ir::BinaryOp::I8x16SubSatS
            | walrus::ir::BinaryOp::I8x16SubSatU
            | walrus::ir::BinaryOp::I16x8Shl
            | walrus::ir::BinaryOp::I16x8ShrS
            | walrus::ir::BinaryOp::I16x8ShrU
            | walrus::ir::BinaryOp::I16x8Add
            | walrus::ir::BinaryOp::I16x8AddSatS
            | walrus::ir::BinaryOp::I16x8AddSatU
            | walrus::ir::BinaryOp::I16x8Sub
            | walrus::ir::BinaryOp::I16x8SubSatS
            | walrus::ir::BinaryOp::I16x8SubSatU
            | walrus::ir::BinaryOp::I16x8Mul
            | walrus::ir::BinaryOp::I32x4Shl
            | walrus::ir::BinaryOp::I32x4ShrS
            | walrus::ir::BinaryOp::I32x4ShrU
            | walrus::ir::BinaryOp::I32x4Add
            | walrus::ir::BinaryOp::I32x4Sub
            | walrus::ir::BinaryOp::I32x4Mul
            | walrus::ir::BinaryOp::I64x2Shl
            | walrus::ir::BinaryOp::I64x2ShrS
            | walrus::ir::BinaryOp::I64x2ShrU
            | walrus::ir::BinaryOp::I64x2Add
            | walrus::ir::BinaryOp::I64x2Sub
            | walrus::ir::BinaryOp::I64x2Mul => Ok(None),
            // fadd, fsub, fmul, fdiv, fmin, and fmax may produce NaNs
            walrus::ir::BinaryOp::F32x4Add
            | walrus::ir::BinaryOp::F32x4Sub
            | walrus::ir::BinaryOp::F32x4Mul
            | walrus::ir::BinaryOp::F32x4Div
            | walrus::ir::BinaryOp::F32x4Min
            | walrus::ir::BinaryOp::F32x4Max => Ok(Some(MaybeNaNKind::F32x4)),
            // fpmin and fpmax deterministically propagate inputs
            walrus::ir::BinaryOp::F32x4PMin | walrus::ir::BinaryOp::F32x4PMax => Ok(None),
            // relaxed fma is non-deterministic in its precision
            walrus::ir::BinaryOp::F32x4RelaxedFma | walrus::ir::BinaryOp::F32x4RelaxedFnma => {
                Err(NaNCanonicaliserError::RelaxedSimd)
            },
            // fadd, fsub, fmul, fdiv, fmin, and fmax may produce NaNs
            walrus::ir::BinaryOp::F64x2Add
            | walrus::ir::BinaryOp::F64x2Sub
            | walrus::ir::BinaryOp::F64x2Mul
            | walrus::ir::BinaryOp::F64x2Div
            | walrus::ir::BinaryOp::F64x2Min
            | walrus::ir::BinaryOp::F64x2Max => Ok(Some(MaybeNaNKind::F64x2)),
            // fpmin and fpmax deterministically propagate inputs
            walrus::ir::BinaryOp::F64x2PMin | walrus::ir::BinaryOp::F64x2PMax => Ok(None),
            // relaxed fma is non-deterministic in its precision
            walrus::ir::BinaryOp::F64x2RelaxedFma | walrus::ir::BinaryOp::F64x2RelaxedFnma => {
                Err(NaNCanonicaliserError::RelaxedSimd)
            },
            // relaxed min and max are non-deterministic if inputs are NaN, -0.0, or +0.0
            walrus::ir::BinaryOp::F64x2MinRelaxed | walrus::ir::BinaryOp::F64x2MaxRelaxed => {
                Err(NaNCanonicaliserError::RelaxedSimd)
            },
            // relaxed swizzle is non-deterministic if lane is out of range
            walrus::ir::BinaryOp::I8x16RelaxedSwizzle => Err(NaNCanonicaliserError::RelaxedSimd),
            // integer operations never produce NaNs
            walrus::ir::BinaryOp::I8x16NarrowI16x8S
            | walrus::ir::BinaryOp::I8x16NarrowI16x8U
            | walrus::ir::BinaryOp::I16x8NarrowI32x4S
            | walrus::ir::BinaryOp::I16x8NarrowI32x4U
            | walrus::ir::BinaryOp::I8x16AvgrU
            | walrus::ir::BinaryOp::I16x8AvgrU
            | walrus::ir::BinaryOp::I8x16MinS
            | walrus::ir::BinaryOp::I8x16MinU
            | walrus::ir::BinaryOp::I8x16MaxS
            | walrus::ir::BinaryOp::I8x16MaxU
            | walrus::ir::BinaryOp::I16x8MinS
            | walrus::ir::BinaryOp::I16x8MinU
            | walrus::ir::BinaryOp::I16x8MaxS
            | walrus::ir::BinaryOp::I16x8MaxU
            | walrus::ir::BinaryOp::I32x4MinS
            | walrus::ir::BinaryOp::I32x4MinU
            | walrus::ir::BinaryOp::I32x4MaxS
            | walrus::ir::BinaryOp::I32x4MaxU
            | walrus::ir::BinaryOp::I32x4DotI16x8S
            | walrus::ir::BinaryOp::I16x8Q15MulrSatS
            | walrus::ir::BinaryOp::I16x8ExtMulLowI8x16S
            | walrus::ir::BinaryOp::I16x8ExtMulHighI8x16S
            | walrus::ir::BinaryOp::I16x8ExtMulLowI8x16U
            | walrus::ir::BinaryOp::I16x8ExtMulHighI8x16U
            | walrus::ir::BinaryOp::I32x4ExtMulLowI16x8S
            | walrus::ir::BinaryOp::I32x4ExtMulHighI16x8S
            | walrus::ir::BinaryOp::I32x4ExtMulLowI16x8U
            | walrus::ir::BinaryOp::I32x4ExtMulHighI16x8U
            | walrus::ir::BinaryOp::I64x2ExtMulLowI32x4S
            | walrus::ir::BinaryOp::I64x2ExtMulHighI32x4S
            | walrus::ir::BinaryOp::I64x2ExtMulLowI32x4U
            | walrus::ir::BinaryOp::I64x2ExtMulHighI32x4U => Ok(None),
        }
    }

    #[allow(clippy::too_many_lines)]
    fn generate_nan_canonicalisation(
        &self,
        kind: MaybeNaNKind,
    ) -> impl IntoIterator<Item = (walrus::ir::Instr, walrus::ir::InstrLocId)> {
        match kind {
            MaybeNaNKind::F32 => [
                // stack: [x, ...]; stash: ??
                (
                    walrus::ir::Instr::LocalSet(walrus::ir::LocalSet {
                        local: self.stash_f32,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [...]; stash: x
                (
                    // canonical NaN
                    walrus::ir::Instr::Const(walrus::ir::Const {
                        value: walrus::ir::Value::F32(f32::from_bits(Self::CANON_NAN_B32)),
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [canon(NaN), ...]; stash: x
                (
                    walrus::ir::Instr::LocalGet(walrus::ir::LocalGet {
                        local: self.stash_f32,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [x, canon(NaN), ...]; stash: x
                (
                    walrus::ir::Instr::LocalGet(walrus::ir::LocalGet {
                        local: self.stash_f32,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [x, x, canon(NaN), ...]; stash: x
                (
                    walrus::ir::Instr::LocalGet(walrus::ir::LocalGet {
                        local: self.stash_f32,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [x, x, x, canon(NaN), ...]; stash: x
                (
                    // isNaN: x != x
                    walrus::ir::Instr::Binop(walrus::ir::Binop {
                        op: walrus::ir::BinaryOp::F32Ne,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [isNaN, x, canon(NaN), ...]; stash: x
                (
                    // select expects the stack [c: isNaN, val2: x, val1: canon(NaN), ...]
                    // select returns if c == 0 { val2 } else { val1 }
                    // here if isNaN  then c = 1 and val1 = canon(NaN) is returned
                    //      if !isNaN then c = 0 and val2 = x is returned
                    walrus::ir::Instr::Select(walrus::ir::Select {
                        // explicit typing requires refrence types
                        ty: None, // Some(walrus::ValType::F32),
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [canon(x), ...]; stash: x
            ],
            MaybeNaNKind::F64 => [
                // stack: [x, ...]; stash: ??
                (
                    walrus::ir::Instr::LocalSet(walrus::ir::LocalSet {
                        local: self.stash_f64,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [...]; stash: x
                (
                    // canonical NaN
                    walrus::ir::Instr::Const(walrus::ir::Const {
                        value: walrus::ir::Value::F64(f64::from_bits(Self::CANON_NAN_B64)),
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [canon(NaN), ...]; stash: x
                (
                    walrus::ir::Instr::LocalGet(walrus::ir::LocalGet {
                        local: self.stash_f64,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [x, canon(NaN), ...]; stash: x
                (
                    walrus::ir::Instr::LocalGet(walrus::ir::LocalGet {
                        local: self.stash_f64,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [x, x, canon(NaN), ...]; stash: x
                (
                    walrus::ir::Instr::LocalGet(walrus::ir::LocalGet {
                        local: self.stash_f64,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [x, x, x, canon(NaN), ...]; stash: x
                (
                    // isNaN: x != x
                    walrus::ir::Instr::Binop(walrus::ir::Binop {
                        op: walrus::ir::BinaryOp::F64Ne,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [isNaN, x, canon(NaN), ...]; stash: x
                (
                    // select expects the stack [c: isNaN, val2: x, val1: canon(NaN), ...]
                    // select returns if c == 0 { val2 } else { val1 }
                    // here if isNaN  then c = 1 and val1 = canon(NaN) is returned
                    //      if !isNaN then c = 0 and val2 = x is returned
                    walrus::ir::Instr::Select(walrus::ir::Select {
                        // explicit typing requires refrence types
                        ty: None, // Some(walrus::ValType::F64),
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [canon(x), ...]; stash: x
            ],
            MaybeNaNKind::F32x4 => [
                // stack: [x, ...]; stash: ??
                (
                    walrus::ir::Instr::LocalSet(walrus::ir::LocalSet {
                        local: self.stash_v128,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [...]; stash: x
                (
                    // canonical NaN
                    walrus::ir::Instr::Const(walrus::ir::Const {
                        value: walrus::ir::Value::V128(Self::CANON_NAN_B32X4),
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [canon(NaN), ...]; stash: x
                (
                    walrus::ir::Instr::LocalGet(walrus::ir::LocalGet {
                        local: self.stash_v128,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [x, canon(NaN), ...]; stash: x
                (
                    walrus::ir::Instr::LocalGet(walrus::ir::LocalGet {
                        local: self.stash_v128,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [x, x, canon(NaN), ...]; stash: x
                (
                    walrus::ir::Instr::LocalGet(walrus::ir::LocalGet {
                        local: self.stash_v128,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [x, x, x, canon(NaN), ...]; stash: x
                (
                    // isNaN: x != x
                    walrus::ir::Instr::Binop(walrus::ir::Binop {
                        op: walrus::ir::BinaryOp::F32x4Ne,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [isNaN, x, canon(NaN), ...]; stash: x
                (
                    // bitselect expects the stack [c: isNaN, val2: x, val1: canon(NaN), ...]
                    // bitselect returns if c[i] == 0 { val2[i] } else { val1[i] }
                    // here if per-lane isNaN  then c = 1 and val1 = canon(NaN) is returned
                    //      if per-lane !isNaN then c = 0 and val2 = x is returned
                    walrus::ir::Instr::V128Bitselect(walrus::ir::V128Bitselect {}),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [canon(x), ...]; stash: x
            ],
            MaybeNaNKind::F64x2 => [
                // stack: [x, ...]; stash: ??
                (
                    walrus::ir::Instr::LocalSet(walrus::ir::LocalSet {
                        local: self.stash_v128,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [...]; stash: x
                (
                    // canonical NaN
                    walrus::ir::Instr::Const(walrus::ir::Const {
                        value: walrus::ir::Value::V128(Self::CANON_NAN_B64X2),
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [canon(NaN), ...]; stash: x
                (
                    walrus::ir::Instr::LocalGet(walrus::ir::LocalGet {
                        local: self.stash_v128,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [x, canon(NaN), ...]; stash: x
                (
                    walrus::ir::Instr::LocalGet(walrus::ir::LocalGet {
                        local: self.stash_v128,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [x, x, canon(NaN), ...]; stash: x
                (
                    walrus::ir::Instr::LocalGet(walrus::ir::LocalGet {
                        local: self.stash_v128,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [x, x, x, canon(NaN), ...]; stash: x
                (
                    // isNaN: x != x
                    walrus::ir::Instr::Binop(walrus::ir::Binop {
                        op: walrus::ir::BinaryOp::F64x2Ne,
                    }),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [isNaN, x, canon(NaN), ...]; stash: x
                (
                    // bitselect expects the stack [c: isNaN, val2: x, val1: canon(NaN), ...]
                    // bitselect returns if c[i] == 0 { val2[i] } else { val1[i] }
                    // here if per-lane isNaN  then c = 1 and val1 = canon(NaN) is returned
                    //      if per-lane !isNaN then c = 0 and val2 = x is returned
                    walrus::ir::Instr::V128Bitselect(walrus::ir::V128Bitselect {}),
                    walrus::ir::InstrLocId::default(),
                ),
                // stack: [canon(x), ...]; stash: x
            ],
        }
    }
}

impl walrus::ir::VisitorMut for NaNCanonicaliser {
    fn start_instr_seq_mut(&mut self, instr_seq: &mut walrus::ir::InstrSeq) {
        if self.result.is_err() {
            return;
        }

        let mut i = 0;

        while let Some((instr, _)) = instr_seq.get(i) {
            match Self::may_produce_non_deterministic_nan(instr) {
                Ok(Some(kind)) => {
                    for new_instr in self.generate_nan_canonicalisation(kind) {
                        i += 1;
                        instr_seq.insert(i, new_instr);
                    }
                },
                Ok(None) => (),
                Err(err) => {
                    self.result = Err(err);
                    return;
                },
            }

            i += 1;
        }
    }
}

#[derive(Copy, Clone)]
enum MaybeNaNKind {
    F32,
    F64,
    F32x4,
    F64x2,
}
