from __future__ import annotations

from config.pipeline_context import PipelineContext
from src.core.base_pipeline import BasePipeline

# Ensure to import src/pipeline/steps/*_steps.py at top of *_pipeline.py:
from src.pipelines.steps import embed_doc_steps
from src.pipelines.steps import store_embeddings_steps



class EmbeddingPipeline(BasePipeline):
    def __init__(self, ctx: PipelineContext):
        super().__init__(ctx)
        self.modules = {
            'chunked-docs-all': self.dm_handler.get_dm('chunked-docs-all'),
            'embeddings-docs-all': self.dm_handler.get_dm('embeddings-docs-all'),
            'faiss-index': self.dm_handler.get_dm('faiss-index'),
        }

    def embed_docs(self):
        self.build_pipeline(
            def_key="embed-docs",
            modules=self.modules,
            step_order=[
                self.order.get("embed"),
            ],
            checkpoints=[],
        )
    
    def store_embeddings(self):
        self.build_pipeline(
            def_key="store-embeddings",
            modules=self.modules,
            step_order=[
                self.order.get("faiss-store")
            ],
            checkpoints=[],
        )
