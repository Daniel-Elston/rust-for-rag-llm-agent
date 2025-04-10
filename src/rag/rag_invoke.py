from __future__ import annotations

import logging
from typing import Dict, Any

from config.settings import Params
from config.pipeline_context import PipelineContext

from langchain_core.runnables.base import RunnableSequence


class InvokeRAG:
    """
    Summary:
        Executes queries on the RAG Pipeline and generates responses.
        Uses the retrieval and augmentation system built by the RAGBuilder
        to answer questions with source attribution.
    """

    def __init__(
        self, ctx: PipelineContext,
        rag_pipeline: RunnableSequence,
    ):
        self.ctx = ctx
        self.rag_pipeline = rag_pipeline
        self.params: Params = ctx.settings.params

    def invoke_response(self, query: str) -> Dict[str, Any]:
        """Generate a response from the RAG pipeline for a given query."""
        try:
            response = self.rag_pipeline.invoke({"query": query})
            logging.error(f"Answer: {response['result']}")
            return {
                "query": query,
                "answer": response["result"],
                "metadata": response.get("metadata", []),
                "model": self.params.language_model_name,
            }
        except Exception as e:
            logging.error(f"Error generating response: {e}", exc_info=True)
