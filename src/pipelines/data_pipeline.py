from __future__ import annotations

from config.pipeline_context import PipelineContext
from src.core.base_pipeline import BasePipeline
from src.core.step_handling.step_factory import StepFactory
from src.core.step_handling.step_handler import StepHandler

from langchain.text_splitter import RecursiveCharacterTextSplitter


class DataPipeline(BasePipeline):
    def __init__(self, ctx: PipelineContext):
        super().__init__(ctx)
        self.modules = {
            'raw-paths': self.paths,
            'raw-docs': self.dm_handler.get_dm('raw-docs-all'),
        }
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.params.chunk_size,
            chunk_overlap=self.params.chunk_overlap,
            separators=self.params.separators,
        )

    def process_docs(self):
        step_defs = StepHandler.get_step_defs(self.defs[0], self.modules)
        step_map = StepHandler.create_step_map(step_defs)
        step_order = [self.order[0], self.order[1]]
        save_points = [self.saves[0], self.saves[1]]
        factory = StepFactory(ctx=self.ctx, step_map=step_map)
        factory.run_pipeline(step_order, save_points)
