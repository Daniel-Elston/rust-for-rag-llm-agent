from __future__ import annotations

from config.pipeline_context import PipelineContext
from src.core.data_handling.data_module import DataModule
from src.core.data_handling.data_module_handler import DataModuleHandler

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain.schema import Document


class BuildVectorStore:
    def __init__(
        self, ctx: PipelineContext,
        embeddings: DataModule,
        index: DataModule,
        embedding_model: HuggingFaceEmbeddings
    ):
        self.ctx = ctx
        self.dm_handler = DataModuleHandler(ctx)
        self.embeddings = embeddings.load(self.dm_handler)
        self.index = index.load(self.dm_handler)
        self.embedding_model = embedding_model
    
    def build(self):
        docs = [Document(**doc) for doc in self.embeddings]
        
        assert len(docs) == self.index.ntotal, \
            f"Document count ({len(docs)}) doesn't match index size ({self.index.ntotal})"
        assert self.index.d == 384, "Dimension mismatch between index and embeddings!"

        return FAISS(
            embedding_function=self.embedding_model.embed_query,
            index=self.index,
            docstore=InMemoryDocstore({i: doc for i, doc in enumerate(docs)}),
            index_to_docstore_id={i: i for i in range(len(docs))},
            # distance_strategy=DistanceStrategy.COSINE
        )
