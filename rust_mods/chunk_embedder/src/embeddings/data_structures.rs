
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Serialize, Deserialize, Debug)]
pub struct SerializableDoc {
    // pub page_content: Option<String>,
    pub page_content: String,
    pub source_file: Option<String>,
    pub object_count: Option<usize>,
    pub metadata: Option<HashMap<String, String>>,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct DocumentEmbedding {
    pub doc_id: u32,
    pub embedding: Vec<f32>,
}
