#![allow(dead_code)]
use crate::trie::*;

use std::collections::HashSet;

#[derive(Debug)]
pub struct KeywordProcessor {
    trie: Trie<char, bool>,

    pub case_sensitive: bool,

    pub boundary: Option<HashSet<char>>,
}

impl KeywordProcessor {
    pub fn new(case_sensitive: bool, boundary: &str) -> Self {
        KeywordProcessor {
            trie: Trie::new(),
            case_sensitive: case_sensitive,
            boundary: match boundary {
                "" => None,
                _ => Some(boundary.chars().collect()),
            },
        }
    }

    pub fn put(&mut self, keyword: &str) {
        let mut key = keyword.chars().collect::<Vec<char>>();
        if !self.case_sensitive {
            key = key.iter().map(|c| c.to_ascii_lowercase()).collect();
        }
        self.trie.put(&key, true);
    }

    pub fn pop(&mut self, keyword: &str) {
        let mut key = keyword.chars().collect::<Vec<char>>();
        if !self.case_sensitive {
            key = key.iter().map(|c| c.to_ascii_lowercase()).collect();
        }
        self.trie.pop(&key, true);
    }

    pub fn extract(&self, text: &str) -> Vec<Span<usize, String>> {
        let spans: Vec<Span<usize, Vec<char>>>;
        let mut target = text.chars().collect::<Vec<char>>();
        if !self.case_sensitive {
            target = target.iter().map(|c| c.to_ascii_lowercase()).collect();
        }

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
}
