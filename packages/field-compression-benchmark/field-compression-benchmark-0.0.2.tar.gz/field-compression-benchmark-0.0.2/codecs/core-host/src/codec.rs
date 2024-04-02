use std::{borrow::BorrowMut, marker::PhantomData};

use wasm_component_layer::{
    List, ListType, RecordType, ResourceOwn, Value, ValueType, Variant, VariantCase, VariantType,
};
use wasm_runtime_layer::backend::WasmEngine;

use codecs_core::{casts::u32_as_usize, BufferSlice, ShapedBuffer, VecBuffer};
use core_error::LocationError;

use crate::{plugin::CodecPlugin, Error};

#[allow(clippy::module_name_repetitions)]
pub struct WasmCodec<E: WasmEngine, P: BorrowMut<CodecPlugin<E>>> {
    pub(crate) resource: ResourceOwn,
    pub(crate) plugin: P,
    pub(crate) instruction_counter: u64,
    pub(crate) _marker: PhantomData<E>,
}

impl<E: WasmEngine, P: BorrowMut<CodecPlugin<E>>> WasmCodec<E, P> {
    #[must_use]
    pub const fn instruction_counter(&self) -> u64 {
        self.instruction_counter
    }

    #[allow(clippy::type_complexity, clippy::too_many_lines)]
    fn process(
        &mut self,
        buf: BufferSlice,
        shape: &[usize],
        process: impl FnOnce(&mut CodecPlugin<E>, &[Value], &mut [Value]) -> anyhow::Result<()>,
    ) -> Result<Result<ShapedBuffer<VecBuffer>, String>, LocationError<Error>> {
        let plugin: &mut CodecPlugin<E> = self.plugin.borrow_mut();

        let resource = self
            .resource
            .borrow(&mut plugin.ctx)
            .map_err(LocationError::from2)?;

        let buffer_ty = VariantType::new(
            None,
            [
                VariantCase::new("u8", Some(ValueType::List(ListType::new(ValueType::U8)))),
                VariantCase::new("u16", Some(ValueType::List(ListType::new(ValueType::U16)))),
                VariantCase::new("u32", Some(ValueType::List(ListType::new(ValueType::U32)))),
                VariantCase::new("u64", Some(ValueType::List(ListType::new(ValueType::U64)))),
                VariantCase::new("i8", Some(ValueType::List(ListType::new(ValueType::S8)))),
                VariantCase::new("i16", Some(ValueType::List(ListType::new(ValueType::S16)))),
                VariantCase::new("i32", Some(ValueType::List(ListType::new(ValueType::S32)))),
                VariantCase::new("i64", Some(ValueType::List(ListType::new(ValueType::S64)))),
                VariantCase::new("f32", Some(ValueType::List(ListType::new(ValueType::F32)))),
                VariantCase::new("f64", Some(ValueType::List(ListType::new(ValueType::F64)))),
            ],
        )
        .map_err(LocationError::from2)?;

        let shaped_buffer_ty = RecordType::new(
            None,
            [
                ("buffer", ValueType::Variant(buffer_ty.clone())),
                ("shape", ValueType::List(ListType::new(ValueType::U32))),
            ],
        )
        .map_err(LocationError::from2)?;

        let buffer = match buf {
            BufferSlice::U8(buf) => Variant::new(buffer_ty, 0, Some(Value::List(List::from(buf)))),
            BufferSlice::U16(buf) => Variant::new(buffer_ty, 1, Some(Value::List(List::from(buf)))),
            BufferSlice::U32(buf) => Variant::new(buffer_ty, 2, Some(Value::List(List::from(buf)))),
            BufferSlice::U64(buf) => Variant::new(buffer_ty, 3, Some(Value::List(List::from(buf)))),
            BufferSlice::I8(buf) => Variant::new(buffer_ty, 4, Some(Value::List(List::from(buf)))),
            BufferSlice::I16(buf) => Variant::new(buffer_ty, 5, Some(Value::List(List::from(buf)))),
            BufferSlice::I32(buf) => Variant::new(buffer_ty, 6, Some(Value::List(List::from(buf)))),
            BufferSlice::I64(buf) => Variant::new(buffer_ty, 7, Some(Value::List(List::from(buf)))),
            BufferSlice::F32(buf) => Variant::new(buffer_ty, 8, Some(Value::List(List::from(buf)))),
            BufferSlice::F64(buf) => Variant::new(buffer_ty, 9, Some(Value::List(List::from(buf)))),
            buf => Err(anyhow::Error::msg(format!(
                "unknown buffer type {}",
                buf.ty()
            ))),
        }
        .map_err(LocationError::from2)?;

        let shape = shape
            .iter()
            .map(|s| u32::try_from(*s).map_err(anyhow::Error::new))
            .collect::<Result<Vec<_>, _>>()
            .map_err(LocationError::from2)?;

        let instruction_counter_pre = plugin
            .instruction_counter
            .call(&mut plugin.ctx, ())
            .map_err(LocationError::from2)?;

        let args = [
            Value::Borrow(resource),
            Value::Variant(buffer),
            Value::List(List::from(shape.as_slice())),
        ];
        let mut result = Value::U8(0);

        process(plugin, &args, std::slice::from_mut(&mut result)).map_err(LocationError::from2)?;

        let instruction_counter_post = plugin
            .instruction_counter
            .call(&mut plugin.ctx, ())
            .map_err(LocationError::from2)?;

        self.instruction_counter += instruction_counter_post - instruction_counter_pre;

        match result {
            Value::Result(result) => match &*result {
                Ok(Some(Value::Record(record))) if record.ty() == shaped_buffer_ty => {
                    let Some(Value::Variant(variant)) = record.field("buffer") else {
                        return Err(LocationError::from2(anyhow::Error::msg(format!(
                            "process result record {record:?} is missing buffer field"
                        ))));
                    };
                    let buffer = match (variant.discriminant(), variant.value()) {
                        (0, Some(Value::List(list))) => {
                            BufferSlice::from(list.typed::<u8>().map_err(LocationError::from2)?)
                                .to_vec()
                        },
                        (1, Some(Value::List(list))) => {
                            BufferSlice::from(list.typed::<u16>().map_err(LocationError::from2)?)
                                .to_vec()
                        },
                        (2, Some(Value::List(list))) => {
                            BufferSlice::from(list.typed::<u32>().map_err(LocationError::from2)?)
                                .to_vec()
                        },
                        (3, Some(Value::List(list))) => {
                            BufferSlice::from(list.typed::<u64>().map_err(LocationError::from2)?)
                                .to_vec()
                        },
                        (4, Some(Value::List(list))) => {
                            BufferSlice::from(list.typed::<i8>().map_err(LocationError::from2)?)
                                .to_vec()
                        },
                        (5, Some(Value::List(list))) => {
                            BufferSlice::from(list.typed::<i16>().map_err(LocationError::from2)?)
                                .to_vec()
                        },
                        (6, Some(Value::List(list))) => {
                            BufferSlice::from(list.typed::<i32>().map_err(LocationError::from2)?)
                                .to_vec()
                        },
                        (7, Some(Value::List(list))) => {
                            BufferSlice::from(list.typed::<i64>().map_err(LocationError::from2)?)
                                .to_vec()
                        },
                        (8, Some(Value::List(list))) => {
                            BufferSlice::from(list.typed::<f32>().map_err(LocationError::from2)?)
                                .to_vec()
                        },
                        (9, Some(Value::List(list))) => {
                            BufferSlice::from(list.typed::<f64>().map_err(LocationError::from2)?)
                                .to_vec()
                        },
                        (discriminant, value) => {
                            return Err(LocationError::from2(anyhow::Error::msg(format!(
                                "process result buffer has an invalid variant \
                                 [{discriminant}]:{value:?}"
                            ))))
                        },
                    };

                    let Some(Value::List(shape)) = record.field("shape") else {
                        return Err(LocationError::from2(anyhow::Error::msg(format!(
                            "process result record {record:?} is missing shape field"
                        ))));
                    };
                    let shape = shape
                        .typed::<u32>()
                        .map_err(LocationError::from2)?
                        .iter()
                        .copied()
                        .map(u32_as_usize)
                        .collect();

                    Ok(Ok(ShapedBuffer { buffer, shape }))
                },
                Err(Some(Value::String(err))) => Ok(Err(String::from(&**err))),
                result => Err(LocationError::from2(anyhow::Error::msg(format!(
                    "unexpected process result value {result:?}"
                )))),
            },
            value => Err(LocationError::from2(anyhow::Error::msg(format!(
                "unexpected process result value {value:?}"
            )))),
        }
    }

    #[allow(clippy::type_complexity)]
    pub fn encode(
        &mut self,
        buf: BufferSlice,
        shape: &[usize],
    ) -> Result<Result<ShapedBuffer<VecBuffer>, String>, LocationError<Error>> {
        self.process(buf, shape, |plugin, arguments, results| {
            plugin.encode.call(&mut plugin.ctx, arguments, results)
        })
    }

    #[allow(clippy::type_complexity)]
    pub fn decode(
        &mut self,
        buf: BufferSlice,
        shape: &[usize],
    ) -> Result<Result<ShapedBuffer<VecBuffer>, String>, LocationError<Error>> {
        self.process(buf, shape, |plugin, arguments, results| {
            plugin.decode.call(&mut plugin.ctx, arguments, results)
        })
    }

    pub fn get_config(&mut self) -> Result<Result<String, String>, LocationError<Error>> {
        let plugin: &mut CodecPlugin<E> = self.plugin.borrow_mut();

        let resource = self
            .resource
            .borrow(&mut plugin.ctx)
            .map_err(LocationError::from2)?;

        let arg = Value::Borrow(resource);
        let mut result = Value::U8(0);

        plugin
            .get_config
            .call(
                &mut plugin.ctx,
                std::slice::from_ref(&arg),
                std::slice::from_mut(&mut result),
            )
            .map_err(LocationError::from2)?;

        match result {
            Value::Result(result) => match &*result {
                Ok(Some(Value::String(config))) => Ok(Ok(String::from(&**config))),
                Err(Some(Value::String(err))) => Ok(Err(String::from(&**err))),
                result => Err(LocationError::from2(anyhow::Error::msg(format!(
                    "unexpected get-config result value {result:?}"
                )))),
            },
            value => Err(LocationError::from2(anyhow::Error::msg(format!(
                "unexpected get-config result value {value:?}"
            )))),
        }
    }

    pub fn drop(mut self) -> Result<(), LocationError<Error>> {
        let plugin: &mut CodecPlugin<E> = self.plugin.borrow_mut();

        let result = self
            .resource
            .drop(&mut plugin.ctx)
            .map_err(LocationError::from2);

        // We need to forget here instead of using ManuallyDrop since we need
        //  both a mutable borrow to self.plugin and an immutable borrow to
        //  self.resource at the same time
        std::mem::forget(self);

        result
    }
}

impl<E: WasmEngine, P: BorrowMut<CodecPlugin<E>>> Drop for WasmCodec<E, P> {
    fn drop(&mut self) {
        let plugin: &mut CodecPlugin<E> = self.plugin.borrow_mut();

        std::mem::drop(self.resource.drop(&mut plugin.ctx));
    }
}
