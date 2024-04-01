#![allow(dead_code)]

use pyo3::prelude::*;

mod trie;
mod flashtext;

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
        Ok(format!("Span(start={}, end={}, value=\"{}\")", self.start, self.end, self.value))
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

    fn extract(&self, text: &str) -> Vec<Span> {
        let spans = self.core.extract(text);
        spans.iter().map(|t| Span {
            start: t.start,
            end: t.end,
            value: match &t.value {
                Some(v) => v.chars().collect(),
                None => "".to_string(),
            },
        }).collect()
    }
}


/// A Python module implemented in Rust.
#[pymodule]
fn krabby(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<KeywordProcessor>()?;
    Ok(())
}
