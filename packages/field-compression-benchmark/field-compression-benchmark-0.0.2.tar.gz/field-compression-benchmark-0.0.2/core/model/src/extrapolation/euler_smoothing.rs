use crate::{
    extrapolation::TimeExtrapolation,
    model::{Model, State, StateView, StateViewMut},
    num::half,
};

pub struct EulerSmoothing;

impl<L: ?Sized + Model> TimeExtrapolation<L> for EulerSmoothing {
    fn step(&mut self, model: &mut L, ext: &mut L::Ext, dt: L::Dtype) {
        // X_n
        let x_n = model.state().to_owned();
        // model.state = X_n

        // X_(n+1) = X_n + X'_n * dt
        let mut x_np1 = model.tendencies(ext);
        x_np1.mul_assign(dt);
        model.state_mut().add_assign(x_np1.view());
        // model.state = X_(n+1)

        // X_(n+2) = X_(n+1) + X'(n+1) * dt
        let mut x_np2 = model.tendencies(ext);
        x_np2.mul_assign(dt);
        model.state_mut().add_assign(x_np2.view());
        // model.state = X_(n+2)

        // X_(n+1) = (X_n + X_(n+2)) * 0.5
        model.state_mut().add_assign(x_n.view());
        model.state_mut().mul_assign(half::<L::Dtype>());
    }
}
