use log;
use std::error::Error;
use std::fs::File;
use std::io::BufReader;
use std::path::Path;
use serde_pickle::Value;

use crate::config::DATA_DIR;
use crate::embeddings::data_structures::{SerializableDoc, DocumentEmbedding};


fn load_chunked_documents(file_path: &str) -> Result<Vec<SerializableDoc>, Box<dyn Error>> {
    let file = File::open(file_path)?;
    let reader = BufReader::new(file);
    let docs: Vec<SerializableDoc> = serde_json::from_reader(reader)?;
    // for doc in &docs[0..3] {
    //     log::info!("Document chunk: {:?}", doc);
    // }
    Ok(docs)
}

fn _inspect_file(file_path: &str) -> Result<(), Box<dyn Error>> {
    let file = File::open(file_path)?;
    let reader = BufReader::new(file);
    let _raw_data: Value = serde_json::from_reader(reader)?;
    // log::info!("{:?}", _raw_data);
    Ok(())
}
    // // Inspect the file
    // inspect_file(input_path.to_str().unwrap())?;

fn save_embeddings(embeddings: Vec<DocumentEmbedding>, file_path: &str) -> Result<(), Box<dyn Error>> {
    let file = File::create(file_path)?;
    serde_json::to_writer_pretty(file, &embeddings)?;
    Ok(())
}

pub fn load() -> Result<Vec<SerializableDoc>, Box<dyn Error>> {
    let input_path = Path::new(DATA_DIR).join("processed/chunked_docs.json");
    let docs = load_chunked_documents(input_path.to_str().unwrap()).expect("Failed to load chunked documents");
    log::info!("Loaded {} chunks from {}.", docs.len(), input_path.display());
    Ok(docs)
}

pub fn save(embeddings: Vec<DocumentEmbedding>) -> Result<(), Box<dyn Error>> {
    let output_path = Path::new(DATA_DIR).join("embeddings/embeddings.json");
    log::info!("Saving {} embeddings to: {:?}", embeddings.len(), output_path);
    save_embeddings(embeddings, output_path.to_str().unwrap())?;
    Ok(())
}