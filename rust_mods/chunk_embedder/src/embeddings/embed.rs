use log;
use std::error::Error;
use rust_bert::pipelines::sentence_embeddings::{
    SentenceEmbeddingsBuilder, SentenceEmbeddingsModelType
};

use crate::embeddings::data_structures::{SerializableDoc, DocumentEmbedding};


pub fn run(chunks: Vec<SerializableDoc>) -> Result<Vec<DocumentEmbedding>, Box<dyn Error>> {
    let model = SentenceEmbeddingsBuilder::remote(SentenceEmbeddingsModelType::AllMiniLmL6V2)
        .with_device(tch::Device::Cpu)
        .create_model()?;
    
    let mut embedding_entries = Vec::new();
    
    for (doc_id, doc) in chunks.into_iter().enumerate() {
        let embedding_results = model.encode(&[doc.page_content.as_str()])?;
        
        if let Some(embedding_vector) = embedding_results.first() {
            embedding_entries.push(DocumentEmbedding {
                doc_id: doc_id as u32,
                page_content: doc.page_content.clone(),
                metadata: doc.metadata.unwrap_or_default(),
                embedding: embedding_vector.clone(),
            });
        }
    }
    log::info!("Generated {} embeddings", embedding_entries.len());
    Ok(embedding_entries)
}
