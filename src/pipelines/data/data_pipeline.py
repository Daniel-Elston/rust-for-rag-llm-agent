from __future__ import annotations

from config.pipeline_context import PipelineContext
from src.core.base_pipeline import BasePipeline
from src.core.types import DataPipelineModules
from src.pipelines.data.dependencies import DataPipelineDependencies

# Ensure to import step_*.py:
from src.pipelines.data import step_process_docs
from src.pipelines.data import step_chunk_docs



class DataPipeline(BasePipeline):
    modules: DataPipelineModules
    
    def __init__(self, ctx: PipelineContext):
        super().__init__(ctx)
        self.modules = DataPipelineModules(
            raw_paths=self.paths,
            raw_docs_all=self.dm_handler.get_dm('raw-docs-all'),
            processed_docs_all=self.dm_handler.get_dm('processed-docs-all'),
        )
        self.text_splitter = DataPipelineDependencies.load_text_splitter(self.params)

    def load_process_raw_docs(self):
        self.build_pipeline(
            def_key="process-raw-docs",
            modules=self.modules,
            step_order=[
                "load-raw",
                "process"
            ],
            checkpoints=["process"],
        )

    def chunk_docs(self):
        self.build_pipeline(
            def_key="chunk-docs",
            modules=self.modules,
            step_order=["chunk"],
            checkpoints=["chunk"],
            step_kwargs={"text_splitter": self.text_splitter},
        )
