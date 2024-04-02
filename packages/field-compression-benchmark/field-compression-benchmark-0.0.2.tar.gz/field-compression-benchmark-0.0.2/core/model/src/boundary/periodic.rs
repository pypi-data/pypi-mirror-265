use ndarray::{SliceArg, SliceInfo, SliceInfoElem};

use crate::{
    boundary::BoundaryCondition,
    model::{Model, StateViewMut},
};

pub struct PeriodicBoundary<const N: usize>;

impl<L: ?Sized + Model, const N: usize> BoundaryCondition<L> for PeriodicBoundary<N>
where
    for<'a> SliceInfo<&'a [SliceInfoElem], L::Dimension, L::Dimension>: SliceArg<L::Dimension>,
{
    fn apply(&mut self, model: &mut L) {
        for mut state in model.state_mut().iter_mut() {
            let shape = state.shape().to_vec();

            let mut left_slice = shape
                .iter()
                .map(|_| SliceInfoElem::from(..))
                .collect::<Vec<_>>();
            let mut right_slice = shape
                .iter()
                .map(|_| SliceInfoElem::from(..))
                .collect::<Vec<_>>();

            #[allow(clippy::indexing_slicing, clippy::unwrap_used)] // FIXME
            for (i, len) in shape.iter().copied().enumerate() {
                left_slice[i] = SliceInfoElem::from(0..N);
                right_slice[i] = SliceInfoElem::from((len - 2 * N)..(len - N));

                let left = SliceInfo::try_from(&left_slice[..]).unwrap();
                let right = SliceInfo::try_from(&right_slice[..]).unwrap();

                let (mut left_to, right_from) = state.multi_slice_mut((left, right));
                left_to.assign(&right_from);
                std::mem::drop((left_to, right_from));

                left_slice[i] = SliceInfoElem::from(N..(2 * N));
                right_slice[i] = SliceInfoElem::from((len - N)..);

                let left = SliceInfo::try_from(&left_slice[..]).unwrap();
                let right = SliceInfo::try_from(&right_slice[..]).unwrap();

                let (left_from, mut right_to) = state.multi_slice_mut((left, right));
                right_to.assign(&left_from);
                std::mem::drop((left_from, right_to));

                left_slice[i] = SliceInfoElem::from(..);
                right_slice[i] = SliceInfoElem::from(..);
            }
        }
    }
}
