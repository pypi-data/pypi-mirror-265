use crate::{
    extrapolation::TimeExtrapolation,
    model::{Model, State, StateViewMut},
    num::{half, two},
};

pub struct RungeKutta4;

impl<L: ?Sized + Model> TimeExtrapolation<L> for RungeKutta4 {
    fn step(&mut self, model: &mut L, ext: &mut L::Ext, dt: L::Dtype) {
        // model.state = X_n

        // k1 = X'(X_n)
        let k1 = model.tendencies(ext);

        // k2 = X'(X_n + k1 * dt/2)
        let k2 = {
            let mut k1_dt = k1.clone();
            k1_dt.mul_assign(dt * half::<L::Dtype>());
            k1_dt.add_assign(model.state());
            model.tendencies_for_state(k1_dt.view(), ext)
        };

        // k3 = X'(X_n + k2 * dt/2)
        let k3 = {
            let mut k2_dt = k2.clone();
            k2_dt.mul_assign(dt * half::<L::Dtype>());
            k2_dt.add_assign(model.state());
            model.tendencies_for_state(k2_dt.view(), ext)
        };

        // k4 = X'(X_n + k3 * dt)
        let k4 = {
            let mut k3_dt = k3.clone();
            k3_dt.mul_assign(dt);
            k3_dt.add_assign(model.state());
            model.tendencies_for_state(k3_dt.view(), ext)
        };

        // k_sum = (k1 + 2*k2 + 2*k3 + k4)
        let mut k_sum = {
            let mut k_sum = k1;

            let mut k2_2 = k2;
            k2_2.mul_assign(two());
            k_sum.add_assign(k2_2.view());

            let mut k3_2 = k3;
            k3_2.mul_assign(two());
            k_sum.add_assign(k3_2.view());

            k_sum.add_assign(k4.view());

            k_sum
        };
        let six = two::<L::Dtype>() + two::<L::Dtype>() + two::<L::Dtype>();
        k_sum.mul_assign(dt / six);

        // X_(n+1) = X_n + (k1 + 2*k2 + 2*k3 + k4) * dt/6
        model.state_mut().add_assign(k_sum.view());
    }
}
