use std::os;
use std::fs::read_dir;
use std::io::Read;
use std::path::Path;
use md5::{Md5, Digest};

pub fn md5sum(path: &str, batch_size: usize) -> String {
    let mut files: Vec<String> = Vec::new();
    let mut dirs: Vec<String> = Vec::new();

    // Check if path exists
    if Path::new(path).exists() {
        // Check if path is a file
        if Path::new(path).is_file() {
            files.push(path.to_string());
        } else {
            dirs.push(path.to_string());
        }
    }

    loop {
        if dirs.is_empty() {
            break;
        }

        let dir = dirs.pop().unwrap();
        let entries = match read_dir(&dir) {
            Ok(entries) => entries,
            Err(_) => continue,
        };

        for entry in entries {
            let entry = match entry {
                Ok(entry) => entry,
                Err(_) => continue,
            };

            let path = entry.path();
            if path.is_file() {
                files.push(path.to_string_lossy().to_string());
            } else {
                dirs.push(path.to_string_lossy().to_string());
            }
        }
    }

    // Sort files
    files.sort();

    // Initialize hash data
    let mut md5 = Md5::new();
    
    for file in &files {
        let filename = Path::new(file).file_name().unwrap().to_str().unwrap();
        md5.update(filename.as_bytes());

        let mut file = match std::fs::File::open(file) {
            Ok(file) => file,
            Err(_) => continue,
        };

        loop {
            let mut buf = vec![0; batch_size];
            let n = match file.read(&mut buf) {
                Ok(n) => n,
                Err(_) => break,
            };

            if n == 0 {
                break;
            }

            md5.update(&buf[..n]);
        }
    }

    format!("{:x}", md5.finalize())
}