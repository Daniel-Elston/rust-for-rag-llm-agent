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
        input_prompts: list,
        rag_system: RunnableSequence
    ):
        self.ctx = ctx
        self.params: Params = ctx.settings.params
        self.input_prompts: str = input_prompts[self.params.prompt_key]
        self.rag_system = rag_system
        
    def invoke_response(self, query: str = None, save: bool = True) -> Dict[str, Any]:
        """Generate a response from the RAG pipeline for a given query."""
        if query is None:
            query = self.input_prompts
        try:
            enhanced_query = query#.split('?')[0]
            response = self.rag_system.invoke({"query": enhanced_query})
            logging.error(f"Answer: {response['result']}")
            response = {
                "query": query,
                "answer": response["result"],
                "metadata": response.get("metadata", []),
                "model": self.params.language_model_name,
            }
            if save:
                return {"generated-answers": response}
            else:
                return response
        except Exception as e:
            logging.error(f"Error generating response: {e}", exc_info=True)
