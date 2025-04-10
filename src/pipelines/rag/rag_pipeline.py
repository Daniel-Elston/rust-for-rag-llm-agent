from __future__ import annotations

from config.pipeline_context import PipelineContext
from src.core.base_pipeline import BasePipeline

from langchain_huggingface import HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

# Ensure to import src/pipeline/steps/*_steps.py in *_pipeline.py:
from src.pipelines.rag import step_vector_store
from src.pipelines.rag import step_hf_pipeline
from src.pipelines.rag import step_retrieval


class RAGPipeline(BasePipeline):
    def __init__(self, ctx: PipelineContext):
        super().__init__(ctx)
        self.modules = {
            'embeddings-docs-all': self.dm_handler.get_dm('embeddings-docs-all'),
            'faiss-index': self.dm_handler.get_dm('faiss-index'),
            'input-prompts': self.dm_handler.get_dm('input-prompts'),
            'prompt-template': self.dm_handler.get_dm('prompt-template'),
        }
        
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=self.params.embedding_model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.params.language_model_name,
            truncation=self.params.truncation,
            model_max_length=self.params.max_input_seq_length,
        )
        self.llm = AutoModelForSeq2SeqLM.from_pretrained(
            self.params.language_model_name
        )
        
        self.faiss_store: FAISS = self.load_vector_store()
        self.hf_pipeline: HuggingFacePipeline = self.build_language_model()

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
        
    def build_language_model(self):
        return self.build_pipeline(
            def_key="load-llm",
            modules=self.modules,
            step_order=[
                self.order.get("load-model")
            ],
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
            step_order=[
                self.order.get("retrieval"),
            ],
            checkpoints=[self.order.get("retrieval")],
            step_kwargs={
                "faiss_store": self.faiss_store,
                "hf_pipeline": self.hf_pipeline,
            }
        )

