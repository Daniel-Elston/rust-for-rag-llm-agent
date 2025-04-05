use pyo3::prelude::*;
use env_logger::{Builder, Env};

mod config;
mod embeddings;
mod my_utils;
mod pipeline;

fn init_logging() -> PyResult<()> {
    let env = Env::default().default_filter_or("info");
    let mut builder = Builder::from_env(env);
    
    builder.filter_module("cached_path", log::LevelFilter::Error);
    builder.filter(None, log::LevelFilter::Info);
    builder.init();
    
    Ok(())
}

#[pyfunction]
fn run_embedding_pipeline() -> PyResult<()> {
    let _ =init_logging();
    
    pipeline::run_pipeline()
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(
            format!("Embedding pipeline failed: {}", e)
        )
    )?;
    
    Ok(())
}

#[pymodule]
fn rust_chunk_embedder(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(run_embedding_pipeline, m)?)?;
    Ok(())
}