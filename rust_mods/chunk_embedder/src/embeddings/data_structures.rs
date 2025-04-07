
use std::collections::HashMap;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct SerializableDoc {
    pub page_content: String,
    pub source_file: Option<String>,
    pub object_count: Option<usize>,
    pub metadata: Option<HashMap<String, String>>,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct DocumentEmbedding {
    pub doc_id: u32,
    pub page_content: String,
    pub metadata: HashMap<String, String>,
    pub embedding: Vec<f32>,
}
