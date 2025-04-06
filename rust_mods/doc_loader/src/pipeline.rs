use std::error::Error;


pub fn run_pipeline() -> Result<(), Box<dyn Error>> {
    let docs = crate::data::load_docs::run()?;
    crate::utils::file_access::run_persist(docs)?;
    Ok(())
}
