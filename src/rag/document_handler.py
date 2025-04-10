from __future__ import annotations

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
        vector_store: FAISS
    ):
        self.ctx = ctx
        self.params: Params = ctx.settings.params
        self.retriever: VectorStoreRetriever = vector_store.as_retriever(
            search_kwargs={"k": self.params.retriever_k}
        )
    
    def retrieve(self, query: str) -> Dict[str, Any]:
        documents = self.retriever.invoke(query)
        return {
            "docs": documents,
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