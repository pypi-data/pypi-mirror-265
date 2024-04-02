use crate::{
    extrapolation::TimeExtrapolation,
    model::{Model, State, StateViewMut},
    num::two,
};

pub struct LeapFrog<L: ?Sized + Model> {
    state_prev: L::State,
}

impl<L: ?Sized + Model> LeapFrog<L> {
    #[must_use]
    pub const fn new(state_prev: L::State) -> Self {
        Self { state_prev }
    }
}

impl<L: ?Sized + Model> TimeExtrapolation<L> for LeapFrog<L> {
    fn step(&mut self, model: &mut L, ext: &mut L::Ext, dt: L::Dtype) {
        // model.state = X_n
        // self.state_prev = X_(n-1)

        // X_(n+1) = X_(n-1) + 2 * X'_n * dt
        let mut x_np1 = model.tendencies(ext);
        x_np1.mul_assign(dt * two());
        x_np1.add_assign(self.state_prev.view());

        // self.state_prev = X_n
        self.state_prev.assign(model.state());

        // model.state = X_(n+1)
        model.state_mut().assign(x_np1.view());
    }
}
