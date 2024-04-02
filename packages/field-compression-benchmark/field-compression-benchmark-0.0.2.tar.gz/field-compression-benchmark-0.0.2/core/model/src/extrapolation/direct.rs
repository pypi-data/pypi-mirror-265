use crate::{
    extrapolation::TimeExtrapolation,
    model::{Model, State, StateViewMut},
};

pub struct Direct;

impl<L: ?Sized + Model> TimeExtrapolation<L> for Direct {
    fn step(&mut self, model: &mut L, ext: &mut L::Ext, dt: L::Dtype) {
        // model.state = X_n

        // X_(n+1) = X_n + X'_n * dt
        let mut x_np1 = model.tendencies(ext);
        x_np1.mul_assign(dt);
        model.state_mut().add_assign(x_np1.view());
    }
}
