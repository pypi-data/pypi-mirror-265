use pyo3::prelude::*;
use pyo3::types::*;

mod trie;
mod flashtext;

use trie::Span;

impl IntoPy<PyObject> for Span<usize, String> {
    fn into_py(self, py: Python) -> PyObject {
        let span = PyDict::new(py);
        span.set_item("start", self.start).unwrap();
        span.set_item("end", self.end).unwrap();
        span.set_item("value", self.value).unwrap();
        span.into()
    }
}

#[pyclass]
struct KeywordProcessor {
    core: flashtext::KeywordProcessor,
}

#[pymethods]
impl KeywordProcessor {
    #[getter]
    fn case_sensitive(&self) -> bool {
        self.core.case_sensitive
    }

    #[getter]
    fn boundary(&self) -> String {
        match self.core.boundary {
            Some(ref b) => Vec::from_iter(b.clone()).iter().collect(),
            None => "".to_string(),
        }
    }

    #[setter]
    fn set_boundary(&mut self, boundary: &str) {
        self.core.boundary = match boundary {
            "" => None,
            _ => Some(boundary.chars().collect()),
        };
    }

    #[new]
    fn new(case_sensitive: bool) -> Self {
        KeywordProcessor {
            core: flashtext::KeywordProcessor::new(case_sensitive, " \t\n\r,.;:!?"),
        }
    }

    fn put(&mut self, keyword: &str) {
        self.core.put(keyword);
    }

    fn pop(&mut self, keyword: &str) {
        self.core.pop(keyword);
    }

    fn extract(&self, text: &str) -> Vec<Span<usize, String>> {
        self.core.extract(text)
    }
}


/// A Python module implemented in Rust.
#[pymodule]
fn krabby(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<KeywordProcessor>()?;
    Ok(())
}
