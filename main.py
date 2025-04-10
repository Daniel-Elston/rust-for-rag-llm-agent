from __future__ import annotations

import logging
import time

from config.pipeline_context import PipelineContext
from src.core.step_handling.step_executor import StepExecutor

from src.pipelines.data.data_pipeline import DataPipeline
from src.pipelines.vector.vector_pipeline import VectorPipeline
from src.pipelines.rag.rag_pipeline import RAGPipeline

from src.pipelines.utils.steps_debugger import debug_steps
from utils.project_setup import initialise_project_configs
import rust_chunk_embedder

class MainPipeline:
    def __init__(self, ctx: PipelineContext):
        self.ctx = ctx

    def run(self):
        """ETL pipeline main entry point."""
        steps = [
            # DataPipeline(self.ctx).load_process_raw_docs,
            # DataPipeline(self.ctx).chunk_docs,
            # VectorPipeline(self.ctx).embed_index_chunked_docs,
            RAGPipeline(self.ctx).retrieval,
            # RAGPipeline(self.ctx).response,
        ]
        StepExecutor(self.ctx).run_main(steps)


if __name__ == "__main__":
    ctx = initialise_project_configs()
    debug_steps()
    try:
        logging.info(f"Beginning Top-Level Pipeline from ``main.py``...\n{"=" * 125}")
        start_t = time.perf_counter()
        MainPipeline(ctx).run()
        end_t = time.perf_counter()
        logging.warning(f"Pipeline executed in {(end_t - start_t):.3f} seconds.")
    except Exception as e:
        logging.error(f"{e}", exc_info=False)
