from __future__ import annotations

from config.settings import Params
from config.pipeline_context import PipelineContext

from src.rag.document_handler import DocumentRetriever, DocumentProcessor
from src.rag.response_handler import ResponseGenerator, ResponseFormatter


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
        retriever: DocumentRetriever,
        processor: DocumentProcessor,
        generator: ResponseGenerator,
        formatter: ResponseFormatter,
    ):
        self.ctx = ctx
        self.params: Params = ctx.settings.params
        self.retriever = retriever
        self.processor = processor
        self.generator = generator
        self.formatter = formatter

    def build(self):
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
