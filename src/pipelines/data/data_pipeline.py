from __future__ import annotations

from config.pipeline_context import PipelineContext
from src.core.base_pipeline import BasePipeline

from langchain.text_splitter import RecursiveCharacterTextSplitter

# Ensure to import src/pipeline/steps/*_steps.py in *_pipeline.py:
from src.pipelines.data import step_process_docs
from src.pipelines.data import step_chunk_docs



class DataPipeline(BasePipeline):
    def __init__(self, ctx: PipelineContext):
        super().__init__(ctx)
        self.modules = {
            'raw-paths': self.paths,
            'raw-docs-all': self.dm_handler.get_dm('raw-docs-all'),
            'processed-docs-all': self.dm_handler.get_dm('processed-docs-all'),
            'chunked-docs-all': self.dm_handler.get_dm('chunked-docs-all'),
            'embeddings-docs-all': self.dm_handler.get_dm('embeddings-docs-all'),
            'faiss-index': self.dm_handler.get_dm('faiss-index'),
        }
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.params.chunk_size,
            chunk_overlap=self.params.chunk_overlap,
            separators=self.params.separators,
        )

    def load_process_raw_docs(self):
        self.build_pipeline(
            def_key="process-raw-docs",
            modules=self.modules,
            step_order=[
                self.order.get("load-raw"),
                self.order.get("process")
            ],
            checkpoints=[self.order.get("process")],
        )

    def chunk_docs(self):
        self.build_pipeline(
            def_key="chunk-docs",
            modules=self.modules,
            step_order=[self.order.get("chunk")],
            checkpoints=[self.order.get("chunk")],
            step_kwargs={
                "text_splitter": self.text_splitter,
            },
        )
