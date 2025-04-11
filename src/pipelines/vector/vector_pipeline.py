from __future__ import annotations

from config.pipeline_context import PipelineContext
from src.core.base_pipeline import BasePipeline
from src.core.types import VectorPipelineModules

# Ensure to import step_*.py:
from src.pipelines.vector import step_embed_doc


class VectorPipeline(BasePipeline):
    modules: VectorPipelineModules
    
    def __init__(self, ctx: PipelineContext):
        super().__init__(ctx)
        self.modules = VectorPipelineModules(
            chunked_docs_all=self.dm_handler.get_dm('chunked-docs-all'),
        )
    
    def embed_index_chunked_docs(self):
        self.build_pipeline(
            def_key="embed-index-docs",
            step_order=["embed-index"],
            checkpoints=[],
        )
