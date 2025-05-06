from __future__ import annotations

import logging
from typing import Self, Any

from config.pipeline_context import PipelineContext
from src.core.data_handling.data_module_handler import DataModuleHandler
from src.core.data_handling.lazy_load import LazyLoad
from src.pipelines.rag.dependencies import RAGPipelineDependencies
from src.core.types import RAGPipelineModules, RAGComponents


class RAGPipelineBuilder:
    def __init__(self, ctx: PipelineContext):
        self.ctx = ctx
        self.dm_handler = DataModuleHandler(ctx)
        self.di = RAGPipelineDependencies(ctx)
        self.comps: dict[str, Any] = {}
        self._modules: RAGPipelineModules = None
        self._components: RAGComponents = None
    
    @property
    def modules(self) -> RAGPipelineModules:
        if self._modules is None:
            self._modules = self._initialise_modules()
        return self._modules
    
    @property
    def components(self) -> RAGComponents:
        if self._components is None:
            self._components = self._build_components()
        return self._components
        
    def _initialise_modules(self) -> RAGPipelineModules:
        return RAGPipelineModules(
            embeddings_docs_all=LazyLoad(self.dm_handler.get_dm('embeddings-docs-all')),
            faiss_index=LazyLoad(self.dm_handler.get_dm('faiss-index')),
            input_prompts=LazyLoad(self.dm_handler.get_dm('input-prompts')),
            prompt_template=LazyLoad(self.dm_handler.get_dm('prompt-template')),
        )
        
    def _build_components(self) -> RAGPipelineModules:
        (
            self.build_core_models()
            .build_vector_store()
            .build_hf_pipeline()
            .build_rag_components()
            .build_rag_system()
        )
        logging.info(f"[INIT] RAG Pipeline Components: {self.comps.keys()}")
        return self.comps

    def build_core_models(self) -> Self:
        self.comps['embedding_model'] = self.di.load_embedding_model()
        self.comps['tokenizer'] = self.di.load_tokenizer()
        self.comps['llm'] = self.di.load_llm()
        return self
    
    def build_vector_store(self) -> Self:
        self.comps['faiss_store'] = self.di.load_vector_store(
            self.modules['embeddings_docs_all'],
            self.modules['faiss_index'],
            self.comps['embedding_model']
        )
        return self
    
    def build_hf_pipeline(self) -> Self:
        self.comps['hf_pipeline'] = self.di.load_llm_pipeline(
            self.comps['llm'],
            self.comps['tokenizer']
        )
        return self
    
    def build_rag_components(self) -> Self:
        self.comps['rag_components'] = self.di.load_rag_components(
            self.comps['faiss_store'],
            self.comps['hf_pipeline'],
            self.modules['prompt_template'],
        )
        return self
    
    def build_rag_system(self) -> Self:
        self.comps['rag_system'] = self.di.load_rag_system(
            **self.comps['rag_components']
        )
        return self
