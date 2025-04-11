from __future__ import annotations

from config.pipeline_context import PipelineContext
from src.core.base_pipeline import BasePipeline
from src.core.types import RAGPipelineModules
from src.pipelines.rag.dependencies import RAGPipelineDependencies

from langchain_huggingface import HuggingFacePipeline
from langchain_community.vectorstores import FAISS

# Ensure to import step_*.py:
from src.pipelines.rag import step_vector_store
from src.pipelines.rag import step_hf_pipeline
from src.pipelines.rag import step_retrieval


class RAGPipeline(BasePipeline):
    modules: RAGPipelineModules
    
    def __init__(self, ctx: PipelineContext):
        super().__init__(ctx)
        self.modules = RAGPipelineModules(
            embeddings_docs_all=self.dm_handler.get_dm('embeddings-docs-all'),
            faiss_index=self.dm_handler.get_dm('faiss-index'),
            input_prompts=self.dm_handler.get_dm('input-prompts'),
            prompt_template=self.dm_handler.get_dm('prompt-template'),
        )
        self.embedding_model = RAGPipelineDependencies.load_embedding_model(self.params)
        self.tokenizer = RAGPipelineDependencies.load_tokenizer(self.params)
        self.llm = RAGPipelineDependencies.load_llm(self.params)
        
        self.faiss_store: FAISS = self.load_vector_store()
        self.hf_pipeline: HuggingFacePipeline = self.build_language_model()

    def load_vector_store(self):
        return self.build_pipeline(
            def_key="load-vector-store",
            modules=self.modules,
            step_order=["load-store"],
            checkpoints=[],
            step_kwargs={
                "embedding_model": self.embedding_model,
            }
        )
        
    def build_language_model(self):
        return self.build_pipeline(
            def_key="load-llm",
            step_order=["load-model"],
            checkpoints=[],
            step_kwargs={
                "llm": self.llm,
                "tokenizer": self.tokenizer,
            }
        )

    def retrieval(self):
        return self.build_pipeline(
            def_key="RAG",
            modules=self.modules,
            step_order=["retrieval"],
            checkpoints=["retrieval"],
            step_kwargs={
                "faiss_store": self.faiss_store,
                "hf_pipeline": self.hf_pipeline,
            }
        )

