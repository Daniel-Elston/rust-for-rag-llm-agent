mod config;
mod utils;
mod pipeline;
mod data;
use env_logger::{Builder, Env};


fn init_logging() {
    let env = Env::default().default_filter_or("info");
    let mut builder = Builder::from_env(env);

    builder.filter_module("lopdf", log::LevelFilter::Error);
    builder.filter(None, log::LevelFilter::Info);
    builder.init();
}

fn main() {
    init_logging();
    let _ = pipeline::run_pipeline();
}
