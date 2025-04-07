from __future__ import annotations

import logging
import time

from config.pipeline_context import PipelineContext
from src.core.step_handling.step_executor import StepExecutor

from src.pipelines.data_pipeline import DataPipeline
from src.pipelines.vector_pipeline import EmbeddingPipeline

from src.pipelines.steps.steps_debugger import debug_steps
from utils.project_setup import initialise_project_configs


class MainPipeline:
    def __init__(self, ctx: PipelineContext):
        self.ctx = ctx

    def run(self):
        """ETL pipeline main entry point."""
        steps = [
            DataPipeline(self.ctx).process_docs,
            DataPipeline(self.ctx).chunk_docs,
            EmbeddingPipeline(self.ctx).embed_docs,
            EmbeddingPipeline(self.ctx).store_embeddings,
            
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
        logging.error(f"{e}", exc_info=True)
