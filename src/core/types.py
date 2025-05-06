from __future__ import annotations

from typing import TypedDict
from config.paths import Paths
from src.core.data_handling.data_module import DataModule

from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFacePipeline
from src.rag.document_handler import DocumentRetriever, DocumentProcessor
from src.rag.response_handler import ResponseGenerator, ResponseFormatter
from src.rag.rag_system import RAGSystem


class DataPipelineModules(TypedDict):
    raw_paths: Paths
    raw_docs_all: DataModule
    processed_docs_all: DataModule

class VectorPipelineModules(TypedDict):
    chunked_docs_all: DataModule

class RAGPipelineModules(TypedDict):
    embeddings_docs_all: DataModule
    faiss_index: DataModule
    input_prompts: DataModule
    prompt_template: DataModule

class RAGSystemComponents(TypedDict):
    retriever: DocumentRetriever
    processor: DocumentProcessor
    generator: ResponseGenerator
    formatter: ResponseFormatter

class RAGComponents(TypedDict):
    embedding_model: HuggingFaceEmbeddings
    tokenizer: AutoTokenizer
    llm: AutoModelForSeq2SeqLM
    faiss_store: FAISS
    hf_pipeline: HuggingFacePipeline
    rag_components: RAGSystemComponents
    rag_system: RAGSystem