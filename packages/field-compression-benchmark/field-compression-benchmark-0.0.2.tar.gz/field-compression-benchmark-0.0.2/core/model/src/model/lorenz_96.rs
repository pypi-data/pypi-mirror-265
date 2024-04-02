use std::marker::PhantomData;

use ndarray::{Array, Array1, ArrayView, ArrayViewMut, Ix1, NdFloat};
use rand::RngCore;
use rand_distr::Distribution;

use crate::model::Model;

pub struct Lorenz96<F: NdFloat, S: ForcingSampler<Dtype = F>> {
    parameters: Lorenz96Parameters<F, S>,
    state: Array1<F>,
}

impl<F: NdFloat, S: ForcingSampler<Dtype = F>> Lorenz96<F, S> {
    #[must_use]
    pub fn new(parameters: Lorenz96Parameters<F, S>) -> Self {
        let k = parameters.k;
        Self {
            parameters,
            state: Array1::zeros((k.get(),)),
        }
    }

    #[must_use]
    pub const fn parameters(&self) -> &Lorenz96Parameters<F, S> {
        &self.parameters
    }
}

impl<F: NdFloat, S: ForcingSampler<Dtype = F>> Model for Lorenz96<F, S> {
    type Dimension = Ix1;
    type Dtype = F;
    type Ext = S::Ext;
    type State = Array<F, Ix1>;

    fn variables(&self) -> impl Iterator<Item = &'static str> {
        ["X_k"].into_iter()
    }

    fn state(&self) -> ArrayView<Self::Dtype, Self::Dimension> {
        self.state.view()
    }

    fn state_mut(&mut self) -> ArrayViewMut<Self::Dtype, Self::Dimension> {
        self.state.view_mut()
    }

    fn tendencies_for_state(
        &self,
        state: ArrayView<Self::Dtype, Self::Dimension>,
        ext: &mut Self::Ext,
    ) -> Array<Self::Dtype, Self::Dimension> {
        let Lorenz96Parameters { k: _, forcing } = &self.parameters;

        let mut tendencies = Array1::zeros(state.dim());

        for (((x_k, &x_kp1), &x_km1), &x_km2) in tendencies
            .iter_mut()
            .zip(state.iter().cycle().skip(1))
            .zip(state.iter().cycle().skip(state.len() - 1))
            .zip(state.iter().cycle().skip(state.len() - 2))
        {
            *x_k = -x_km2 * x_km1 + x_km1 * x_kp1 - (*x_k) + forcing.sample(ext);
        }

        tendencies
    }

    fn with_state(&self, state: Array<Self::Dtype, Self::Dimension>) -> Self {
        let mut model = Self::new(self.parameters.clone());
        model.state.view_mut().assign(&state);
        model
    }
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
pub struct Lorenz96Parameters<F: NdFloat, S: ForcingSampler<Dtype = F>> {
    pub k: K,
    pub forcing: S,
}

#[derive(
    Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, serde::Serialize, serde::Deserialize,
)]
#[serde(try_from = "usize", into = "usize")]
pub struct K(usize);

impl K {
    pub const MIN: Self = Self(4);

    #[must_use]
    pub const fn new(x: usize) -> Option<Self> {
        if x >= 4 {
            Some(Self(x))
        } else {
            None
        }
    }

    #[must_use]
    pub const fn get(&self) -> usize {
        self.0
    }
}

impl From<K> for usize {
    fn from(value: K) -> Self {
        value.get()
    }
}

impl TryFrom<usize> for K {
    type Error = &'static str;

    fn try_from(value: usize) -> Result<Self, Self::Error> {
        Self::new(value).ok_or("k must be >= 4")
    }
}

pub trait ForcingSampler: Clone {
    type Dtype: NdFloat;
    type Ext;

    fn sample(&self, ext: &mut Self::Ext) -> Self::Dtype;
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
pub struct Const<F: NdFloat> {
    r#const: F,
}

impl<F: NdFloat> Const<F> {
    #[must_use]
    pub const fn new(r#const: F) -> Self {
        Self { r#const }
    }
}

impl<F: NdFloat> ForcingSampler for Const<F> {
    type Dtype = F;
    type Ext = ();

    fn sample(&self, _ext: &mut Self::Ext) -> Self::Dtype {
        self.r#const
    }
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
pub struct Distr<F: NdFloat, D: Distribution<F> + Clone> {
    distr: D,
    #[serde(skip)]
    _marker: PhantomData<F>,
}

impl<F: NdFloat, D: Distribution<F> + Clone> Distr<F, D> {
    #[must_use]
    pub const fn new(distr: D) -> Self {
        Self {
            distr,
            _marker: PhantomData::<F>,
        }
    }
}

impl<F: NdFloat, D: Distribution<F> + Clone> ForcingSampler for Distr<F, D> {
    type Dtype = F;
    type Ext = Box<dyn 'static + RngCore + Send + Sync>;

    fn sample(&self, ext: &mut Self::Ext) -> Self::Dtype {
        self.distr.sample(&mut **ext)
    }
}
