from __future__ import annotations

from operator import itemgetter
from typing import Dict, Any

from config.pipeline_context import PipelineContext
from config.settings import Params

from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnableMap
from langchain_huggingface import HuggingFacePipeline



class ResponseGenerator:
    def __init__(
        self, ctx: PipelineContext,
        language_pipeline: HuggingFacePipeline,
        prompt_template: str
    ):
        self.ctx = ctx
        self.language_pipeline = language_pipeline
        self.params: Params = ctx.settings.params
        self.prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_template(prompt_template)
    
    def generate(self, processed_doc: Dict[str, Any]) -> Dict[str, Any]:
        context = processed_doc["context"]
        question = processed_doc["question"]
        sources = processed_doc["sources"]
        source_docs = processed_doc["source_docs"]
        
        prompt_args = {
            "context": context,
            "question": question,
            "sources": sources
        }
        
        prompt = self.prompt_template.format_prompt(**prompt_args).text
        response = self.language_pipeline.invoke(prompt)
        return {
            "response": response,
            "source_docs": source_docs
        }
    
    def as_runnable(self) -> RunnableMap:
        input_mapping = {
            "context": itemgetter("context"),
            "question": itemgetter("question"),
            "sources": itemgetter("sources"),
        }
        return RunnableMap({
            "response": input_mapping | self.prompt_template | self.language_pipeline,
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
            }
            metadata.append(meta_entry)
        
        return {
            "result": response,
            "source_documents": source_docs,
            "metadata": metadata
        }
    
    def as_runnable(self) -> RunnableLambda:
        return RunnableLambda(self.format_output, name="output_formatter")
