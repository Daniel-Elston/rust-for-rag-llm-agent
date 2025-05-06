from __future__ import annotations

import logging
from operator import itemgetter
from typing import Dict, Any

from config.pipeline_context import PipelineContext
from config.settings import Params
from src.core.data_handling.lazy_load import LazyLoad
from src.core.data_handling.data_module_handler import DataModuleHandler

from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnableMap
from langchain_huggingface import HuggingFacePipeline


class ResponseGenerator:
    def __init__(
        self, ctx: PipelineContext,
        language_pipeline: HuggingFacePipeline,
        prompt_template: LazyLoad
    ):
        self.ctx = ctx
        self.dm_handler = DataModuleHandler(ctx)
        self.language_pipeline = language_pipeline
        self.params: Params = ctx.settings.params
        self.prompt_template = ChatPromptTemplate.from_template(prompt_template.load(self.dm_handler))
    
    def as_runnable(self) -> RunnableMap:
        input_mapping = {
            "context": itemgetter("context"),
            "question": itemgetter("question"),
            "sources": itemgetter("sources"),
        }
        
        return RunnableMap({
            "response": (
                input_mapping 
                | RunnableLambda(lambda x: logging.debug(f"Final Prompt:\n{self.prompt_template.format(**x)}") or x)
                | self.prompt_template 
                | self.language_pipeline
            ),
            "source_docs": itemgetter("source_docs")
        })


class ResponseFormatter:
    @staticmethod
    def format_output(generation_output: Dict[str, Any]) -> Dict[str, Any]:
        response = generation_output.get("response", "")
        source_docs = generation_output.get("source_docs", [])
        
        metadata = []
        for i, doc in enumerate(source_docs):
            meta_entry = {
                "index": i,
                "source": doc.metadata.get("source_file", "Unknown"),
                "page_count": doc.metadata.get("page_count", "Unknown"),
                "object_count": doc.metadata.get("object_count", "Unknown"),
                "page_content": doc.page_content,
            }
            metadata.append(meta_entry)
        
        return {
            "result": response,
            "source_documents": source_docs,
            "metadata": metadata
        }
    
    def as_runnable(self) -> RunnableLambda:
        return RunnableLambda(self.format_output, name="output_formatter")
