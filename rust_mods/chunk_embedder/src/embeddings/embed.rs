use log;
use std::error::Error;
use candle_core::{Tensor, Device, DType};
use candle_nn::VarBuilder;
use hf_hub::api::sync::Api;
use candle_transformers::models::bert::{BertModel, Config};
use tokenizers::Tokenizer;
use rayon::prelude::*;
use anyhow::Result;

use crate::embeddings::data_structures::{SerializableDoc, DocumentEmbedding};


pub struct SentenceModel {
    model: BertModel,
    tokenizer: Tokenizer,
    device: Device,
}

impl SentenceModel {
    // Model Initialization
    pub fn new(model_name: &str) -> Result<Self, Box<dyn Error>> {
        let device = Device::Cpu;
        let api = Api::new()?;
        let api_repo = api.model(model_name.to_string());

        // // Download the model files
        // let model_path = api_repo.download("model.safetensors")?;
        // let config_path = api_repo.download("config.json")?;
        // let tokenizer_path = api_repo.download("tokenizer.json")?;
        // log::info!("Model files downloaded successfully.");

        let model_path = api_repo.get("model.safetensors")?;
        let config_path = api_repo.get("config.json")?;
        let tokenizer_path = api_repo.get("tokenizer.json")?;

        // Load config
        let config: Config = serde_json::from_slice(&std::fs::read(config_path)?)?;
        
        // Initialize model and tokenizer
        let vb = unsafe {VarBuilder::from_mmaped_safetensors(&[model_path], DType::F32, &device)? };
        let model = BertModel::load(vb, &config)?;
        let tokenizer = Tokenizer::from_file(tokenizer_path).map_err(|e| e.to_string())?;
        log::info!(
            "Model, Config and Tokenizer initialized successfully.
            \nModel name: {}\nModel hidden size: {}\nModel num layers: {}",
            model_name, config.hidden_size, config.num_hidden_layers
        );

        Ok(Self { model, tokenizer, device })
    }


    // Embedding Generation
    pub fn embed(&self, text: &str) -> Result<Vec<f32>, Box<dyn Error>> {
        // 1. Tokenization
        let tokens = self.tokenizer.encode(text, true).map_err(|e| e.to_string())?;
        let token_ids = Tensor::new(tokens.get_ids(), &self.device)?.unsqueeze(0)?;
        let token_type_ids = token_ids.zeros_like()?;
        let attention_mask = token_ids.ones_like()?;

        // 2. Forward pass, explicit execution
        let embeddings = self.model.forward(
            &token_ids,
            &token_type_ids,
            Some(&attention_mask)
        )?;

        // 3. mean pooling with tensor ops
        let pooled = {
            // Convert attention mask to weights
            let weights = attention_mask
                .to_dtype(DType::F32)?
                .sum_keepdim(1)?
                .recip()?;  // 1/seq_len for mean

            embeddings
                .sum_keepdim(1)?
                .broadcast_mul(&weights)?
        };

        let result = pooled.flatten_all()?.to_vec1()?;

        Ok(result)
    }
}


pub fn run(chunks: Vec<SerializableDoc>) -> Result<Vec<DocumentEmbedding>, Box<dyn Error>> {
    let model = SentenceModel::new("sentence-transformers/all-MiniLM-L6-v2")?;
    
    // Create thread-safe reference counter for the model
    let model_arc = std::sync::Arc::new(model);
    
    // Process chunks in parallel
    let embedding_entries: Vec<_> = chunks
        .into_par_iter()
        .enumerate()
        .map(|(doc_id, doc)| {
            let model = model_arc.clone();
            log::info!("Processing chunk {}", doc_id + 1);
            
            model.embed(&doc.page_content)
                .map(|embedding| DocumentEmbedding {
                    doc_id: doc_id as u32,
                    page_content: doc.page_content.clone(),
                    metadata: doc.metadata.unwrap_or_default(),
                    embedding,
                })
                .map_err(|e| anyhow::anyhow!("Error embedding chunk {}: {}", doc_id, e))
        })
        .collect::<Result<Vec<_>, _>>()?;

    log::info!("Generated {} embeddings", embedding_entries.len());
    Ok(embedding_entries)
}