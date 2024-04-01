#![allow(dead_code)]

use crate::trie::*;

use std::collections::{HashMap, HashSet};
use std::{hash::Hash, result};

#[derive(Debug)]
pub struct KeywordProcessor {
    trie: Trie<char, bool>,
    keywords: HashMap<String, String>,

    pub case_sensitive: bool,

    pub boundary: Option<HashSet<char>>,
}

impl KeywordProcessor {
    pub fn new(case_sensitive: bool, boundary: &str) -> Self {
        KeywordProcessor {
            trie: Trie::new(),
            keywords: HashMap::new(),
            case_sensitive: case_sensitive,
            boundary: match boundary {
                "" => None,
                _ => Some(boundary.chars().collect()),
            },
        }
    }

    pub fn put(&mut self, keyword: &str) {
        let key = if !self.case_sensitive {
            keyword.to_lowercase()
        } else {
            keyword.to_string()
        };
        // let mut key: Vec<char> = keyword.chars().collect();
        // if !self.case_sensitive {
        //     key = key.iter().map(|c| c.to_lowercase()).collect();
        // }

        // let key_str: String = key.iter().collect();
        if self.keywords.contains_key(&key) {
            return;
        }

        self.trie.put(&key.chars().collect(), true);
        self.keywords.insert(key, keyword.to_string());
    }

    pub fn pop(&mut self, keyword: &str) {
        let key = if !self.case_sensitive {
            keyword.to_lowercase()
        } else {
            keyword.to_string()
        };

        if !self.keywords.contains_key(&key) {
            return;
        }

        self.keywords.remove(&key);
        self.trie.pop(&key.chars().collect(), true);
    }

    pub fn get_keywords(&self) -> Vec<String> {
        self.keywords.values().map(|v| v.clone()).collect()
    }

    pub fn extract(&self, text: &str) -> Vec<Span<usize, String>> {
        let spans: Vec<Span<usize, Vec<char>>>;
        let target: Vec<char> = if !self.case_sensitive {
            text.to_lowercase().chars().collect()
        } else {
            text.chars().collect()
        };

        match self.boundary {
            Some(ref b) => {
                spans = self.trie.extract(&target, true, Some(b));
            }
            None => {
                spans = self.trie.extract(&target, true, None);
            }
        };

        return spans
            .iter()
            .map(|t| Span {
                start: t.start,
                end: t.end,
                value: match &t.value {
                    Some(v) => Some(v.iter().collect()),
                    None => None,
                },
            })
            .collect();
    }

    pub fn replace(&self, text: &str, repl: &HashMap<&str, &str>, default: Option<&str>) -> String {
        let repl: HashMap<String, String> = {
            let mut r = HashMap::new();
            for (k, v) in repl.iter() {
                let k: String = if !self.case_sensitive {
                    k.to_lowercase()
                } else {
                    k.to_string()
                };
                r.insert(k, v.to_string());
            }
            r
        };
        
        let spans = self.extract(text);
        let mut result = String::new();
        let mut last_end = 0;
        let indices: Vec<usize> = text.char_indices().map(|(i, _)| i).collect();

        for span in spans {
            let start = indices[span.start];
            let end = if span.end < indices.len() {
                indices[span.end]
            } else {
                text.len()
            };
            if last_end < start {
                result.push_str(&text[last_end..start]);
            }
            let orginal = &text[start..end];

            let replacement = match span.value {
                Some(v) => {
                    // let key = v.as_str();
                    match repl.get(&v) {
                        Some(value) => value.as_str(),
                        None => match default {
                            Some(value) => value,
                            None => orginal,
                        },
                    }
                }
                None => orginal,
            };
            result.push_str(replacement);
            last_end = end;
        }

        if last_end < text.len() {
            result.push_str(&text[last_end..]);
        }

        return result;
    }

    pub fn has(&self, keyword: &str) -> bool {
        let target: String = if !self.case_sensitive {
            keyword.to_lowercase()
        } else {
            keyword.to_string()
        };

        self.keywords.contains_key(&target)
    }
}
