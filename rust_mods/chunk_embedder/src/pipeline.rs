use log;
use std::error::Error;
use std::path::Path;

use crate::my_utils::file_access;
use crate::embeddings::embed;
use crate::indexing::build_idx;
use crate::config::DATA_DIR;


pub fn run_pipeline() -> Result<(), Box<dyn Error>>{
    log::info!("Running pipeline...");

    let chunks_path = Path::new(DATA_DIR).join("processed/chunked_docs.json");
    let chunks = file_access::load_json(&chunks_path);
    
    let embeddings_path = Path::new(DATA_DIR).join("processed/embeddings.json");
    let embeddings = embed::run(chunks.unwrap())?;
    file_access::save_json(&embeddings, &embeddings_path)?;

    let index_path = Path::new(DATA_DIR).join("processed/faiss_index.index");
    let index = build_idx::run(embeddings, &index_path)?;
    log::info!("Indexing Complete.\nDimensions: {}\nSize: {}", index.d(), index.ntotal());

    Ok(())
}