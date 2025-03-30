from __future__ import annotations

import logging

from config.pipeline_context import PipelineContext
from src.core.step_handling.step_factory import StepFactory

from src.pipelines.data_pipeline import DataPipeline

from src.pipelines.steps.steps_debugger import debug_steps
from utils.project_setup import initialise_project_configs


class MainPipeline:
    def __init__(self, ctx: PipelineContext):
        self.ctx = ctx

    def run(self):
        """ETL pipeline main entry point."""
        steps = [
            DataPipeline(self.ctx).process_docs,
        ]
        StepFactory(self.ctx).run_main(steps)


if __name__ == "__main__":
    ctx = initialise_project_configs()
    debug_steps()
    try:
        logging.info(f"Beginning Top-Level Pipeline from ``main.py``...\n{"=" * 125}")
        MainPipeline(ctx).run()
    except Exception as e:
        logging.error(f"{e}", exc_info=True)
