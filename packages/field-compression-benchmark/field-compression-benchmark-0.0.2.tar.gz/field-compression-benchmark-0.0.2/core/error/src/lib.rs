use std::{borrow::Cow, error::Error, fmt};

use serde_name::{DeserializeNameAdapter, SerializeNameAdapter};

#[derive(
    Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash, serde::Serialize, serde::Deserialize,
)]
pub struct Location {
    file: Cow<'static, str>,
    line: u32,
    column: u32,
}

impl Location {
    #[must_use]
    #[track_caller]
    pub fn caller() -> Self {
        let location = std::panic::Location::caller();

        // Ideally, the location would also store the function name, see
        //  https://github.com/rust-lang/rust/issues/95529

        Self {
            file: Cow::Borrowed(location.file()),
            line: location.line(),
            column: location.column(),
        }
    }
}

impl fmt::Display for Location {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        write!(fmt, "{}:{}:{}", self.file, self.line, self.column)
    }
}

#[derive(Clone, PartialEq, Eq, PartialOrd, Ord, Hash, serde::Serialize, serde::Deserialize)]
#[serde(transparent)]
pub struct LocationError<E: Error> {
    inner: Box<LocationErrorInner<E>>,
}

impl<E: Error> LocationError<E> {
    #[must_use]
    #[track_caller]
    pub fn new(error: E) -> Self {
        Self {
            inner: Box::new(LocationErrorInner {
                error,
                location: Location::caller(),
            }),
        }
    }

    #[must_use]
    #[track_caller]
    pub fn from2<E2: Into<E>>(error: E2) -> Self {
        Self::new(error.into())
    }
}

impl<E: Error> LocationError<E> {
    #[must_use]
    pub const fn error(&self) -> &E {
        &self.inner.error
    }

    #[must_use]
    pub fn error_mut(&mut self) -> &mut E {
        &mut self.inner.error
    }

    #[must_use]
    pub fn into_error(self) -> E {
        self.inner.error
    }

    #[must_use]
    pub const fn location(&self) -> &Location {
        &self.inner.location
    }

    #[must_use]
    pub fn map<F: Error>(self, map: impl FnOnce(E) -> F) -> LocationError<F> {
        LocationError {
            inner: Box::new(LocationErrorInner {
                error: map(self.inner.error),
                location: self.inner.location,
            }),
        }
    }
}

impl<E: Error + Into<std::convert::Infallible>> LocationError<E> {
    pub fn infallible(self) -> ! {
        #[allow(unreachable_code)]
        match self.into_error().into() {}
    }
}

impl<E: Error> From<E> for LocationError<E> {
    #[track_caller]
    fn from(error: E) -> Self {
        Self::new(error)
    }
}

impl<E: Error> fmt::Display for LocationError<E> {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.write_fmt(format_args!("{}", self.inner.error))?;

        if !fmt.alternate() {
            return Ok(());
        }

        // TODO: allow pretty-printing with colours and indentation
        if let Some(cause) = self.inner.error.source() {
            fmt.write_fmt(format_args!("\n ├╴at {}", self.inner.location))?;

            fmt.write_fmt(format_args!("\n │\n{cause:#}"))
        } else {
            fmt.write_fmt(format_args!("\n └╴at {}", self.inner.location))
        }
    }
}

impl<E: Error> fmt::Debug for LocationError<E> {
    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        write!(fmt, "{self:#}")
    }
}

impl<E: Error> Error for LocationError<E> {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        self.inner.error.source()
    }
}

#[derive(Clone, PartialEq, Eq, PartialOrd, Ord, Hash, serde::Serialize, serde::Deserialize)]
#[serde(rename = "LocationError")]
#[serde(remote = "LocationErrorInner")]
struct LocationErrorInner<E: Error> {
    error: E,
    location: Location,
}

// FIXME: don't generate overly specific names
impl<E: Error + serde::Serialize> serde::Serialize for LocationErrorInner<E> {
    fn serialize<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        Self::serialize(
            self,
            SerializeNameAdapter::new(serializer, std::any::type_name::<Self>()),
        )
    }
}

impl<'de, E: Error + serde::Deserialize<'de>> serde::Deserialize<'de> for LocationErrorInner<E> {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        Self::deserialize(DeserializeNameAdapter::new(
            deserializer,
            std::any::type_name::<Self>(),
        ))
    }
}
