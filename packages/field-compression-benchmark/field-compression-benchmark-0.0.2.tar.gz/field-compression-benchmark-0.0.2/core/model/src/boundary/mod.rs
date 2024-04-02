use crate::model::Model;

mod noop;
mod periodic;
mod zero;

pub use noop::NoopBoundary;
pub use periodic::PeriodicBoundary;
pub use zero::ZeroBoundary;

pub trait BoundaryCondition<L: ?Sized + Model> {
    fn apply(&mut self, model: &mut L);
}
