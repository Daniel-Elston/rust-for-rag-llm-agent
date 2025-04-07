use log;
use std::error::Error;
use std::path::PathBuf;
use faiss::{index_factory, MetricType, Index, write_index};

use crate::embeddings::data_structures::DocumentEmbedding;


pub fn run(records: Vec<DocumentEmbedding>, output_path: &PathBuf) -> Result<Box<dyn Index>, Box<dyn Error>> {
    log::info!("Building index...");

    let dim = records[0].embedding.len();
    let index_description = "Flat";
    let metric = MetricType::L2;

    let mut index = index_factory(dim as u32, index_description, metric)?;
    for rec in &records {
        index.add(&rec.embedding)?;
    }
    
    write_index(&index, output_path.to_str().unwrap())?;
    log::info!("Saved FAISS index to {:?}", output_path.display());

    Ok(Box::new(index))
}
