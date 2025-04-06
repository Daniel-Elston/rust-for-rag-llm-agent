use std::fs;
use std::path::{Path, PathBuf};
use std::error::Error;
use lopdf::Document;
use std::collections::HashMap;

use log;

use crate::config::DATA_DIR;

#[derive(Debug)]
pub struct LoadedDoc {
    pub page_content: String,
    pub metadata: HashMap<String, String>,
}

fn extract_text_from_document(doc: &Document) -> Result<String, Box<dyn Error>> {
    let mut text = String::new();
    
    // Get document pages: keys are page numbers
    let pages = doc.get_pages();
    for (page_num, _) in pages.iter() {
        // Pass the page number to extract_text
        if let Ok(content) = doc.extract_text(&[*page_num]) {
            text.push_str(&content);
            text.push_str("\n\n");
        }
    }
    Ok(text)
}


fn load_pdfs_from_dir(
    dir_path: &Path
) -> Result<Vec<LoadedDoc>, Box<dyn Error>> {
    let mut docs = Vec::new();

    for entry in fs::read_dir(dir_path)? {
        let entry = entry?;
        let path = entry.path();

        if path.extension().map_or(false, |ext| ext == "pdf") {
            let doc = Document::load(&path)?;
            let page_content = extract_text_from_document(&doc)?;
            log::info!("Loaded document: {}", path.display());

            let mut metadata = HashMap::new();
            metadata.insert("source_file".to_string(), path.to_string_lossy().to_string());
            metadata.insert("object_count".to_string(), doc.objects.len().to_string());
            metadata.insert("page_count".to_string(), doc.get_pages().len().to_string());

            docs.push(LoadedDoc {
                page_content,
                metadata
            });
        }
    }
    Ok(docs)
}

pub fn run() -> Result<Vec<LoadedDoc>, Box<dyn Error>> {
    log::info!("Loading documents...");

    let raw_path: PathBuf = Path::new(DATA_DIR).join("raw/");
    log::info!("Loading documents from: {}", raw_path.display());

    let docs = load_pdfs_from_dir(&raw_path)?;
    log::info!("Loaded {} documents", docs.len());

    for (i, loaded_doc) in docs.iter().enumerate() {
        log::info!(
            "Document {} has {} pages\nPath: {}\n",
            i,
            loaded_doc.metadata.get("page_count").unwrap(),
            loaded_doc.metadata.get("source_file").unwrap(),
        );
    }
    Ok(docs)
}