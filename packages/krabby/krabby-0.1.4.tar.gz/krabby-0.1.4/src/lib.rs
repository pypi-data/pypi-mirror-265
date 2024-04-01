#![allow(dead_code)]

use std::collections::HashMap;

use pyo3::{prelude::*, types::PyDict};

mod flashtext;
mod trie;

#[pyclass]
struct Span {
    #[pyo3(get)]
    start: usize,

    #[pyo3(get)]
    end: usize,

    #[pyo3(get)]
    value: String,
}

#[pymethods]
impl Span {
    fn __repr__(&self) -> PyResult<String> {
        Ok(format!(
            "Span(start={}, end={}, value=\"{}\")",
            self.start, self.end, self.value
        ))
    }

    fn dict(&self, py: Python) -> PyResult<PyObject> {
        let dict = PyDict::new(py);
        dict.set_item("start", self.start).unwrap();
        dict.set_item("end", self.end).unwrap();
        dict.set_item("value", self.value.clone()).unwrap();
        Ok(dict.into())
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

    fn set_boundary(&mut self, boundary: &str) {
        self.core.boundary = match boundary {
            "" => None,
            _ => Some(boundary.chars().collect()),
        };
    }

    fn add_boundary(&mut self, boundary: &str) {
        match &mut self.core.boundary {
            Some(b) => {
                for c in boundary.chars() {
                    b.insert(c);
                }
            }
            None => {
                self.core.boundary = Some(boundary.chars().collect());
            }
        }
    }

    fn del_boundary(&mut self, boundary: &str) {
        match &mut self.core.boundary {
            Some(b) => {
                for c in boundary.chars() {
                    b.remove(&c);
                }
            }
            None => {}
        }
    }

    #[new]
    fn new(case_sensitive: bool) -> Self {
        KeywordProcessor {
            core: flashtext::KeywordProcessor::new(
                case_sensitive,
                " \t\n\r,.;:!?{}[]()<>+-*/=|\\\"'`~@#$%^&*",
            ),
        }
    }

    fn put(&mut self, keyword: &str) {
        self.core.put(keyword);
    }

    fn pop(&mut self, keyword: &str) {
        self.core.pop(keyword);
    }

    fn extract(&self, text: &str) -> Vec<Span> {
        let spans = self.core.extract(text);
        spans
            .iter()
            .map(|t| Span {
                start: t.start,
                end: t.end,
                value: match &t.value {
                    Some(v) => v.chars().collect(),
                    None => "".to_string(),
                },
            })
            .collect()
    }

    fn replace(&self, text: &str, repl: HashMap<&str, &str>, default: Option<&str>) -> String {
        self.core.replace(text, &repl, default)
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn krabby(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<KeywordProcessor>()?;
    Ok(())
}
