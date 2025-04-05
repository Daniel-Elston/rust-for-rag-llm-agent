use log;
use std::error::Error;


pub fn run_pipeline() -> Result<(), Box<dyn Error>>{
    log::info!("Running pipeline...");
    let chunks = crate::my_utils::file_access::load();
    // log::info!("Pipeline completed with {} chunks.", &chunks?.len());
    let embeddings = crate::embeddings::embed::run(chunks.unwrap())?;
    crate::my_utils::file_access::save(embeddings)?;
    Ok(())
}