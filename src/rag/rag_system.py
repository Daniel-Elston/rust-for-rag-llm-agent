from __future__ import annotations

from typing import Dict, Any

from config.settings import Params
from config.pipeline_context import PipelineContext

from src.rag.document_handler import DocumentRetriever, DocumentProcessor
from src.rag.response_handler import ResponseGenerator, ResponseFormatter
from src.rag.rag_invoke import InvokeRAG

from langchain_huggingface import HuggingFacePipeline
from langchain_community.vectorstores import FAISS


class RAGSystem:
    """
    Summary:
        Builds the retrieval system and augments retrieved documents into RAG pipeline
        for later generation. Utilises FAISS for retrieval and a Hugging Face LLM for
        local text generation.\n
    Input: FAISS vector store ``data_state key: faiss_store``\n
    Output: RAG Pipeline ``data_state key: rag_pipeline``\n
    Steps:
        1) Load FAISS store from state\n
        2) Initialise the retriever from the FAISS store\n
        3) Build the RAG Pipeline chain by combining retrieval and augmentation steps\n
        4) Save RAG Pipeline chain to state
    """
    def __init__(
        self, ctx: PipelineContext,
        faiss_store: FAISS,
        hf_pipeline: HuggingFacePipeline,
        prompt_template: str,
        input_prompts: list,
    ):
        self.ctx = ctx
        self.params: Params = ctx.settings.params
        self.prompt_template = prompt_template
        self.input_prompts: str = input_prompts[self.params.prompt_key]
        
        self.retriever = DocumentRetriever(ctx, faiss_store)
        self.processor = DocumentProcessor()
        self.generator = ResponseGenerator(ctx, hf_pipeline, prompt_template)
        self.formatter = ResponseFormatter()
        
    def run(self):
        rag_pipeline = self.build_rag_system()
        response = InvokeRAG(self.ctx, rag_pipeline).invoke_response(self.input_prompts)
        return {"generated-answers": response}
        
    def build_rag_system(self):
        retrieval_step = self.retriever.as_runnable()
        processing_step = self.processor.as_runnable()
        generation_step = self.generator.as_runnable()
        output_step = self.formatter.as_runnable()
        return (
            retrieval_step
            | processing_step
            | generation_step
            | output_step
        )
