use crate::model::Model;

mod direct;
mod euler_smoothing;
mod leapfrog;
mod runge_kutta;

pub use direct::Direct;
pub use euler_smoothing::EulerSmoothing;
pub use leapfrog::LeapFrog;
pub use runge_kutta::RungeKutta4;

pub trait TimeExtrapolation<L: ?Sized + Model> {
    fn step(&mut self, model: &mut L, ext: &mut L::Ext, dt: L::Dtype);
}
