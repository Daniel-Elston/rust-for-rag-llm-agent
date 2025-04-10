from __future__ import annotations

from config.pipeline_context import PipelineContext
from src.core.base_pipeline import BasePipeline

# Ensure to import src/pipeline/steps/*_steps.py in *_pipeline.py:
from src.pipelines.vector import step_embed_doc


class VectorPipeline(BasePipeline):
    def __init__(self, ctx: PipelineContext):
        super().__init__(ctx)
        self.modules = {
            'chunked-docs-all': self.dm_handler.get_dm('chunked-docs-all'),
            'embeddings-docs-all': self.dm_handler.get_dm('embeddings-docs-all'),
            'faiss-index': self.dm_handler.get_dm('faiss-index'),
        }

    def embed_index_chunked_docs(self):
        self.build_pipeline(
            def_key="embed-index-docs",
            modules=self.modules,
            step_order=[
                self.order.get("embed-index"),
            ],
            checkpoints=[],
        )
