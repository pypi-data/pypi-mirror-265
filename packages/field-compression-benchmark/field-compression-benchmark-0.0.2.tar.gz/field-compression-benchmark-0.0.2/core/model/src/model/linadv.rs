use ndarray::{s, Array, Array1, ArrayView, ArrayViewMut, Ix1, NdFloat};

use crate::{model::Model, num::two};

pub struct Linadv<F: NdFloat> {
    parameters: LinadvParameters<F>,
    h_m: Array1<F>,
}

impl<F: NdFloat> Linadv<F> {
    #[must_use]
    pub fn new(parameters: LinadvParameters<F>) -> Self {
        Self {
            parameters,
            h_m: Array1::zeros((parameters.x_dim,)),
        }
    }

    #[must_use]
    pub const fn parameters(&self) -> &LinadvParameters<F> {
        &self.parameters
    }
}

impl<F: NdFloat> Model for Linadv<F> {
    type Dimension = Ix1;
    type Dtype = F;
    type Ext = ();
    type State = Array<F, Ix1>;

    fn variables(&self) -> impl Iterator<Item = &'static str> {
        ["h_m"].into_iter()
    }

    fn state(&self) -> ArrayView<Self::Dtype, Self::Dimension> {
        self.h_m.view()
    }

    fn state_mut(&mut self) -> ArrayViewMut<Self::Dtype, Self::Dimension> {
        self.h_m.view_mut()
    }

    fn tendencies_for_state(
        &self,
        state: ArrayView<Self::Dtype, Self::Dimension>,
        _ext: &mut Self::Ext,
    ) -> Array<Self::Dtype, Self::Dimension> {
        let LinadvParameters {
            x_dim: _,
            dx_m,
            U_const_m_s,
        } = self.parameters;

        let h_m = state;

        // Calculate the initial tendency of the height variable
        let mut h_tend_m_s = Array1::zeros(state.dim());
        #[allow(clippy::reversed_empty_ranges)]
        h_tend_m_s.slice_mut(s![1..-1]).assign(
            &-((h_m.slice(s![2..]).to_owned() - h_m.slice(s![..-2])) * U_const_m_s
                / (dx_m * two())),
        );

        h_tend_m_s
    }

    fn with_state(&self, h_m: Array<Self::Dtype, Self::Dimension>) -> Self {
        let mut model = Self::new(self.parameters);
        model.h_m.view_mut().assign(&h_m);
        model
    }
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
#[allow(non_snake_case)]
pub struct LinadvParameters<F: NdFloat> {
    pub x_dim: usize,
    pub dx_m: F,
    pub U_const_m_s: F,
}
