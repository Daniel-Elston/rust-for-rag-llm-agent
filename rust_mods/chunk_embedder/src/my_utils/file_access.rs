use log;
use std::error::Error;
use std::fs::File;
use std::io::BufReader;
use std::path::PathBuf;
use serde_pickle::Value;

use crate::embeddings::data_structures::{SerializableDoc, DocumentEmbedding};


pub fn load_json(input_path: &PathBuf) -> Result<Vec<SerializableDoc>, Box<dyn Error>> {
    let file = File::open(input_path)?;
    let reader = BufReader::new(file);
    let data: Vec<SerializableDoc> = serde_json::from_reader(reader)?;
    // for doc in &data[0..3] {
    //     log::info!("Document chunk: {:?}", doc);
    // }
    log::info!("Loaded {} chunks from {}.", data.len(), input_path.display());
    Ok(data)
}

pub fn save_json(embeddings: &Vec<DocumentEmbedding>, output_path: &PathBuf) -> Result<(), Box<dyn Error>> {
    let file = File::create(output_path)?;
    serde_json::to_writer_pretty(file, &embeddings)?;
    log::info!("Saved {} embeddings to: {:?}", embeddings.len(), output_path);
    Ok(())
}

fn _inspect_file(file_path: &str) -> Result<(), Box<dyn Error>> {
    let file = File::open(file_path)?;
    let reader = BufReader::new(file);
    let _raw_data: Value = serde_json::from_reader(reader)?;
    // log::info!("{:?}", _raw_data);
    Ok(())
}
    // // Inspect the file
    // _inspect_file(input_path.to_str().unwrap())?;
