from __future__ import annotations

from config.pipeline_context import PipelineContext
from config.settings import Params
from src.core.data_handling.data_module import DataModule
from src.core.step_handling.step_registry import StepBuilder

from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFacePipeline

from src.models.faiss_store import BuildVectorStore
from src.rag.document_handler import DocumentRetriever, DocumentProcessor
from src.rag.response_handler import ResponseGenerator, ResponseFormatter
from src.rag.rag_system import RAGSystem


class RAGPipelineDependencies:
    def __init__(self, ctx: PipelineContext):
        self.ctx = ctx
        self.params: Params = ctx.settings.params

    @StepBuilder.initialise(def_key="embedding-model")
    def load_embedding_model(self) -> HuggingFaceEmbeddings:
        return HuggingFaceEmbeddings(
            model_name=self.params.embedding_model_name,
            model_kwargs={'device': self.params.device},
            encode_kwargs={'normalize_embeddings': self.params.normalise_embeddings},
        )

    @StepBuilder.initialise(def_key="tokenizer")
    def load_tokenizer(self) -> AutoTokenizer:
        return AutoTokenizer.from_pretrained(
            self.params.language_model_name,
            truncation=self.params.truncation,
            model_max_length=self.params.max_input_seq_length,
        )

    @StepBuilder.initialise(def_key="llm")
    def load_llm(self) -> AutoModelForSeq2SeqLM:
        return AutoModelForSeq2SeqLM.from_pretrained(
            self.params.language_model_name,
            device_map="auto"
        )

    @StepBuilder.initialise(def_key="vector-store")
    def load_vector_store(self, embeddings, index, embedding_model) -> FAISS:
        return BuildVectorStore(self.ctx, embeddings, index, embedding_model).build()

    @StepBuilder.initialise(def_key="llm-pipeline")
    def load_llm_pipeline(self, llm, tokenizer) -> HuggingFacePipeline:
        return HuggingFacePipeline(pipeline=pipeline(
            "text2text-generation",
            model=llm,
            tokenizer=tokenizer,
            max_length=self.params.max_output_seq_length,
        ))
    
    @StepBuilder.initialise(def_key="RAG-components")
    def load_rag_components(
        self, faiss_store: FAISS,
        hf_pipeline: HuggingFacePipeline,
        prompt_template: DataModule,
    ):
        retriever = DocumentRetriever(self.ctx, faiss_store)
        processor = DocumentProcessor()
        generator = ResponseGenerator(self.ctx, hf_pipeline, prompt_template)
        formatter = ResponseFormatter()
        return {
            "retriever": retriever,
            "processor": processor,
            "generator": generator,
            "formatter": formatter
        }

    @StepBuilder.initialise(def_key="rag-system")
    def load_rag_system(self, retriever, processor, generator, formatter) -> RAGSystem:
        return RAGSystem(self.ctx, retriever, processor, generator, formatter).build()

