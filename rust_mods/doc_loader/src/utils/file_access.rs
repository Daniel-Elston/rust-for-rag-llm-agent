use std::fs::File;
use std::error::Error;
use serde::{Deserialize, Serialize};
use serde_pickle;
use std::path::Path;
use log;
use std::collections::HashMap;

use crate::config::DATA_DIR;
use crate::data::load_docs::LoadedDoc;



#[derive(Serialize, Deserialize, Debug)]
struct SerializableDoc {
    page_content: String,
    metadata: HashMap<String, String>,
}


fn save_to_pickle<T: Serialize>(
    data: &T, output_path: &Path
) -> Result<(), Box<dyn Error>> {
    let mut file = File::create(output_path)?;
    serde_pickle::to_writer(&mut file, data, Default::default())?;
    Ok(())
}


pub fn run_persist(
    docs: Vec<LoadedDoc>
) -> Result<(), Box<dyn Error>> {
    let ser_docs: Vec<SerializableDoc> = docs.into_iter().map(|loaded_doc| {
        SerializableDoc {
            page_content: loaded_doc.page_content,
            metadata: loaded_doc.metadata
        }
    }).collect();

    let output_path = Path::new(DATA_DIR).join("sdo/rs-docs.pkl");
    log::info!("Sample document:\n{}", ser_docs[0].page_content.chars().take(500).collect::<String>().replace("\n", " ").replace("\r", " "));
    log::info!("Saving documents to:\n{}", output_path.display());
    save_to_pickle(&ser_docs, &output_path)?;
    log::info!("Documents have been serialized and saved to\n{:?}", output_path);
    Ok(())
}
