use ndarray::{Axis, RemoveAxis};
use num_traits::Zero;

use crate::{
    boundary::BoundaryCondition,
    model::{Model, StateViewMut},
};

pub struct ZeroBoundary<const N: usize>;

impl<L: ?Sized + Model, const N: usize> BoundaryCondition<L> for ZeroBoundary<N>
where
    L::Dimension: RemoveAxis,
{
    fn apply(&mut self, model: &mut L) {
        for mut state in model.state_mut().iter_mut() {
            let shape = state.shape().to_vec();

            for (i, len) in shape.iter().copied().enumerate() {
                for j in 0..N.min(len) {
                    for x in &mut state.index_axis_mut(Axis(i), j) {
                        *x = L::Dtype::zero();
                    }
                }

                for j in len.saturating_sub(N)..len {
                    for x in &mut state.index_axis_mut(Axis(i), j) {
                        *x = L::Dtype::zero();
                    }
                }
            }
        }
    }
}
