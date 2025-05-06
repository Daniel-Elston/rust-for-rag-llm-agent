from __future__ import annotations

import logging

from operator import itemgetter
from typing import List, Dict, Any

from config.pipeline_context import PipelineContext
from config.settings import Params

from langchain.schema import Document
from langchain.schema.runnable import RunnableLambda, RunnableMap
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores.base import VectorStoreRetriever


class DocumentRetriever:
    def __init__(
        self, ctx: PipelineContext,
        vector_store: FAISS,
    ):
        self.ctx = ctx
        self.params: Params = ctx.settings.params
        self.vector_store = vector_store
            

    def retrieve(self, query: str) -> Dict[str, Any]:
        docs_with_scores = self.vector_store.similarity_search_with_score(query, k=120, sort=True)
        docs_list = list(docs_with_scores)        
        # docs_list.sort(key=lambda x: x[1], reverse=False)
        filtered_docs = [doc for doc, score in docs_list[:self.params.retriever_k]]
        
        # Debug
        for i, (doc, score) in enumerate(docs_list[:self.params.retriever_k]):
            logging.debug(f"Rank {i+1} (Distance={score:.6f}): {doc.page_content}\n")
            
        return {
            "docs": filtered_docs,
            "question": query
        }
        
    def as_runnable(self) -> RunnableLambda:
        return RunnableLambda(
            lambda inputs: self.retrieve(inputs["query"]),
            name="retrieval"
        )


class DocumentProcessor:
    @staticmethod
    def extract_content(docs: List[Document]) -> str:
        return "\n\n".join(doc.page_content for doc in docs)
    
    @staticmethod
    def format_sources(docs: List[Document]) -> str:
        sources = [
            f"[{i+1}] \
            File: {doc.metadata['source_file']} \
            Pages: {doc.metadata['page_count']} \
            Objects: {doc.metadata['object_count']}"
            for i, doc in enumerate(docs)
        ]
        return "\n".join(sources)
    
    def process(self, retrieval_output: Dict[str, Any]) -> Dict[str, Any]:
        docs = retrieval_output["docs"]
        return {
            "context": self.extract_content(docs),
            "question": retrieval_output["question"],
            "source_docs": docs,
            "sources": self.format_sources(docs)
        }
    
    def as_runnable(self) -> RunnableMap:
        return RunnableMap({
            "context": itemgetter("docs") | RunnableLambda(self.extract_content),
            "question": itemgetter("question"),
            "source_docs": itemgetter("docs"),
            "sources": itemgetter("docs") | RunnableLambda(self.format_sources)
        })