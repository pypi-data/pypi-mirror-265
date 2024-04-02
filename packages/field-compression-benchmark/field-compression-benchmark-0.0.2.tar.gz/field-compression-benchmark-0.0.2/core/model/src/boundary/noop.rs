use crate::{boundary::BoundaryCondition, model::Model};

pub struct NoopBoundary;

impl<L: ?Sized + Model> BoundaryCondition<L> for NoopBoundary {
    fn apply(&mut self, _model: &mut L) {
        // no-op
    }
}
