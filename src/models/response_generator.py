from __future__ import annotations

import logging

from config.pipeline_context import PipelineContext
from config.settings import Params
from langchain_core.runnables import RunnableLambda


class RAGResponseGenerator:
    """
    Summary:
        Executes queries on the RAG Pipeline and generates responses.
        Uses the retrieval and augmentation system built by the RAGBuilder
        to answer questions with source attribution.\n
    Input: RAG pipeline ``data_state key: rag_pipeline``\n
    Output: LLM generated response\n
    Steps:
        1) Load the RAG pipeline chain from state\n
        2) Execute queries on the RAG pipeline for retrieval and augmentation\n
        3) Generate responses from the LLM\n
        4) Save and log the generated responses for downstream use
    """

    def __init__(
        self, ctx: PipelineContext,
        rag_pipeline: RunnableLambda,
    ):
        self.ctx = ctx
        self.rag_pipeline = rag_pipeline
        self.params: Params = ctx.settings.params
        
    def run(self):
        test_query = self._get_test_query()
        response = self._generate_response(test_query)
        log_response = self._log_generated_response(response)
        return {"generated-answers": log_response}

    def _get_test_query(self):
        """Retrieve a test query."""
        test_query_store = [
            "Give a brief summary of quantum encryption.",
            "Give a summary of challenges in quantum computing.",
        ]
        return test_query_store[0]

    def _generate_response(self, query: str):
        """Generate a response from the QA chain for given query."""
        response = self.rag_pipeline.invoke({"query": query})
        return {
            "query": query,
            "answer": response["result"],
            "metadata": response.get("metadata", [])
        }

    def _log_generated_response(self, response):
        """Log the generated response to a file."""
        log_entry = {
            "response": response,
            "model": self.ctx.settings.params.language_model_name,
            # "sources": response.get("sources", [])
        }
        return log_entry