mod config;
mod data;
mod pipeline;
mod utils;
use env_logger::{Builder, Env};

use pyo3::prelude::*;


fn init_logging() {
    let env = Env::default().default_filter_or("info");
    let mut builder = Builder::from_env(env);

    builder.filter_module("lopdf", log::LevelFilter::Error);
    builder.filter(None, log::LevelFilter::Info);
    builder.init();
}

#[pyfunction] // Expose to Python
fn run_document_pipeline() -> PyResult<()> {
    init_logging();

    match pipeline::run_pipeline() {
        Ok(_) => Ok(()),
        Err(e) => Err(pyo3::exceptions::PyRuntimeError::new_err(
            format!("Pipeline failed: {}",
            e
        ))),
    }
}

#[pymodule]
fn rust_doc_loader(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(run_document_pipeline, m)?)?;
    Ok(())
}
