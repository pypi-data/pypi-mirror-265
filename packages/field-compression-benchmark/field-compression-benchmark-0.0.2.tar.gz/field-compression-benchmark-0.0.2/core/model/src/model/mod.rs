use ndarray::{Array, ArrayView, ArrayViewMut, Dimension, NdFloat};

pub mod any;
pub mod linadv;
pub mod lorenz_63;
pub mod lorenz_96;
pub mod onedsw;
pub mod twodsw;

pub trait Model {
    type Dtype: NdFloat;
    type Dimension: Dimension;
    type State: State<Dtype = Self::Dtype, Dimension = Self::Dimension>;
    type Ext;

    fn variables(&self) -> impl Iterator<Item = &'static str>;

    fn state(&self) -> <Self::State as State>::View<'_>;
    fn state_mut(&mut self) -> <Self::State as State>::ViewMut<'_>;

    #[must_use]
    fn tendencies(&self, ext: &mut Self::Ext) -> Self::State {
        self.tendencies_for_state(self.state(), ext)
    }

    #[must_use]
    fn tendencies_for_state(
        &self,
        state: <Self::State as State>::View<'_>,
        ext: &mut Self::Ext,
    ) -> Self::State;

    #[must_use]
    fn with_state(&self, state: Self::State) -> Self
    where
        Self: Sized;
}

pub trait State: Clone {
    type Dtype: NdFloat;
    type Dimension: Dimension;

    type View<'a>: StateView<'a, Dtype = Self::Dtype, Dimension = Self::Dimension, State = Self>
    where
        Self: 'a;
    type ViewMut<'a>: StateViewMut<
        'a,
        Dtype = Self::Dtype,
        Dimension = Self::Dimension,
        State = Self,
    >
    where
        Self: 'a;

    fn view(&self) -> Self::View<'_>;
    fn view_mut(&mut self) -> Self::ViewMut<'_>;

    fn assign(&mut self, rhs: Self::View<'_>) {
        self.view_mut().assign(rhs);
    }

    fn add_assign(&mut self, rhs: Self::View<'_>) {
        self.view_mut().add_assign(rhs);
    }

    fn mul_assign(&mut self, rhs: Self::Dtype) {
        self.view_mut().mul_assign(rhs);
    }
}

pub trait StateView<'s> {
    type Dtype: NdFloat;
    type Dimension: Dimension;

    type State: State<Dtype = Self::Dtype, Dimension = Self::Dimension>;

    fn to_owned(&self) -> Self::State;

    fn iter<'a>(&'a self)
        -> impl Iterator<Item = ArrayView<'a, Self::Dtype, Self::Dimension>> + 'a;
}

pub trait StateViewMut<'s> {
    type Dtype: NdFloat;
    type Dimension: Dimension;

    type State: State<Dtype = Self::Dtype, Dimension = Self::Dimension>;

    fn to_owned(&self) -> Self::State;

    fn iter<'a>(&'a self)
        -> impl Iterator<Item = ArrayView<'a, Self::Dtype, Self::Dimension>> + 'a;
    fn iter_mut<'a>(
        &'a mut self,
    ) -> impl Iterator<Item = ArrayViewMut<'a, Self::Dtype, Self::Dimension>> + 'a;

    fn assign(&mut self, rhs: <Self::State as State>::View<'_>) {
        self.iter_mut()
            .zip(rhs.iter())
            .for_each(|(mut x, rhs)| x.assign(&rhs));
    }

    fn add_assign(&mut self, rhs: <Self::State as State>::View<'_>) {
        self.iter_mut()
            .zip(rhs.iter())
            .for_each(|(mut x, rhs)| x += &rhs);
    }

    fn mul_assign(&mut self, rhs: Self::Dtype) {
        self.iter_mut().for_each(|mut x| x *= rhs);
    }
}

impl<F: NdFloat, D: Dimension> State for Array<F, D> {
    type Dimension = D;
    type Dtype = F;
    type View<'a> = ArrayView<'a, Self::Dtype, Self::Dimension> where Self: 'a;
    type ViewMut<'a> = ArrayViewMut<'a, Self::Dtype, Self::Dimension> where Self: 'a;

    fn view(&self) -> Self::View<'_> {
        self.view()
    }

    fn view_mut(&mut self) -> Self::ViewMut<'_> {
        self.view_mut()
    }
}

impl<'s, F: NdFloat, D: Dimension> StateView<'s> for ArrayView<'s, F, D> {
    type Dimension = D;
    type Dtype = F;
    type State = Array<F, D>;

    fn to_owned(&self) -> Self::State {
        self.to_owned()
    }

    fn iter<'a>(
        &'a self,
    ) -> impl Iterator<Item = ArrayView<'a, Self::Dtype, Self::Dimension>> + 'a {
        std::iter::once(self.view())
    }
}

impl<'s, F: NdFloat, D: Dimension> StateViewMut<'s> for ArrayViewMut<'s, F, D> {
    type Dimension = D;
    type Dtype = F;
    type State = Array<F, D>;

    fn to_owned(&self) -> Self::State {
        self.to_owned()
    }

    fn iter<'a>(
        &'a self,
    ) -> impl Iterator<Item = ArrayView<'a, Self::Dtype, Self::Dimension>> + 'a {
        std::iter::once(self.view())
    }

    fn iter_mut<'a>(
        &'a mut self,
    ) -> impl Iterator<Item = ArrayViewMut<'a, Self::Dtype, Self::Dimension>> + 'a {
        std::iter::once(self.view_mut())
    }
}
