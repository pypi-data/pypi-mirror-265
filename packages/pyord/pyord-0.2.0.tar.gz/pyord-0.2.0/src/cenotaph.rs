use pyo3::prelude::*;

use ordinals::Cenotaph;

use super::flaw::PyFlaw;
use super::rune::PyRune;
use super::rune_id::PyRuneId;

/// Cenotaph
/// :type flaws: list[Flaw]
/// :type etching: typing.Optional[Rune]
/// :type mint: typing.Optional[RuneId]
#[pyclass(name="Cenotaph")]
#[derive(Debug, PartialEq)]
pub struct PyCenotaph(pub Cenotaph);


#[pymethods]
impl PyCenotaph {
    #[new]
    #[pyo3(signature = (flaws, etching=None, mint=None))]
    pub fn new(
        flaws: Vec<PyFlaw>,
        etching: Option<PyRune>,
        mint: Option<PyRuneId>,
    ) -> Self {
        let flaw_bitmask = flaws.iter().fold(0, |acc, f| acc | f.0.flag());
        Self(Cenotaph {
            etching: etching.map(|e| e.0),
            flaws: flaw_bitmask,
            mint: mint.map(|m| m.0),
        })
    }

    pub fn __eq__(&self, other: &PyCenotaph) -> bool {
        self.0 == other.0
    }

    /// :rtype: str
    pub fn __repr__(&self) -> String {
        format!(
            "Cenotaph(flaws={}, etching={}, mint={})",
            self.flaws()
                .iter()
                .map(|f| f.__repr__())
                .collect::<Vec<String>>()
                .join(", "),
            self.etching()
                .map(|e| e.__repr__())
                .unwrap_or_else(|| "None".to_string()),
            self.mint()
                .map(|m| m.__repr__())
                .unwrap_or_else(|| "None".to_string())
        )
    }

    /// :rtype: list[Flaw]
    #[getter]
    pub fn flaws(&self) -> Vec<PyFlaw> {
        self.0.flaws().iter().map(|flaw| PyFlaw(*flaw)).collect()
    }

    /// :rtype: typing.Optional[Rune]
    #[getter]
    pub fn etching(&self) -> Option<PyRune> {
        self.0.etching.map(|e| PyRune(e))
    }

    /// :rtype: typing.Optional[RuneId]
    #[getter]
    pub fn mint(&self) -> Option<PyRuneId> {
        self.0.mint.map(|m| PyRuneId(m))
    }

    /// :rtype: bool
    #[getter]
    pub fn is_cenotaph(&self) -> bool {
        true
    }
}
