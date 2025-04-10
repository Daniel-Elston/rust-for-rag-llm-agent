from __future__ import annotations

from config.pipeline_context import PipelineContext
from src.core.base_pipeline import BasePipeline

from src.models.llm import BuildHFPipeline

from langchain_huggingface import HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableLambda
from langchain_community.embeddings import HuggingFaceEmbeddings

# Ensure to import src/pipeline/steps/*_steps.py in *_pipeline.py:
from src.pipelines.rag import step_vector_store
from src.pipelines.rag import step_retrieval
from src.pipelines.rag import step_response


class RAGPipeline(BasePipeline):
    def __init__(self, ctx: PipelineContext):
        super().__init__(ctx)
        self.modules = {
            'embeddings-docs-all': self.dm_handler.get_dm('embeddings-docs-all'),
            'faiss-index': self.dm_handler.get_dm('faiss-index'),
        }
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},  # Match Rust CPU usage
            encode_kwargs={'normalize_embeddings': True}
        )
        self.faiss_store: FAISS = self.load_vector_store()
        self.language_pipeline: HuggingFacePipeline = BuildHFPipeline(ctx).build()
        self.rag_pipeline: RunnableLambda = self.retrieval()

    def load_vector_store(self):
        return self.build_pipeline(
            def_key="load-vector-store",
            modules=self.modules,
            step_order=[
                self.order.get("load-store")
            ],
            checkpoints=[],
            step_kwargs={
                "embedding_model": self.embedding_model,
            }
        )

    def retrieval(self):
        return self.build_pipeline(
            def_key="RAG",
            modules=self.modules,
            step_order=[
                self.order.get("retrieval"),
            ],
            checkpoints=[],
            step_kwargs={
                "faiss_store": self.faiss_store,
                "language_pipeline": self.language_pipeline,
            }
        )

    def response(self):
        self.build_pipeline(
            def_key="RAG-response",
            modules=self.modules,
            step_order=[
                self.order.get("response"),
            ],
            checkpoints=[self.order.get("response")],
            step_kwargs={
                "rag_pipeline": self.rag_pipeline,
            }
        )
