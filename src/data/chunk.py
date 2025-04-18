from __future__ import annotations

import logging
import attr

from config.pipeline_context import PipelineContext
from src.core.data_handling.data_module import DataModule

from langchain.text_splitter import RecursiveCharacterTextSplitter

@attr.s
class Document:
    page_content: str = attr.ib()
    metadata: dict = attr.ib()


class ChunkDocuments:
    """
    Summary: Splits documents into chunks, based on text splitter
    Brief:
        - Splits documents into chunks using text splitter and data config params
        - Filters out chunks with mostly numerical data
    """

    def __init__(
        self, ctx: PipelineContext,
        dataset: DataModule,
        text_splitter: RecursiveCharacterTextSplitter
    ):
        self.ctx = ctx
        self.dataset = dataset
        self.text_splitter = text_splitter

    def run(self):
        chunks = self.text_splitter.split_documents(self.dataset)
        
        custom_chunks = self.form_custom_chunks(chunks)
        
        chunks_filtered = [doc for doc in custom_chunks if self.filter_junk_chunks(doc)]
        self._log_doc_chunks(chunks_filtered)
        
        chunks_dict = [attr.asdict(chunk) for chunk in chunks_filtered]
        return {"chunked-docs-all": chunks_dict}
    
    
    def form_custom_chunks(self, chunks):
        """Convert chunks to custom Document format"""
        return [
            Document(page_content=doc.page_content, metadata=doc.metadata)
            for doc in chunks
        ]

    def filter_junk_chunks(self, doc):
        """If chunk will is mostly useless numerical data, filter out"""
        content = doc.page_content
        alpha_chars = sum(char.isalpha() for char in content)
        return alpha_chars >= len(content) // 2

    def _log_doc_chunks(self, chunks_filtered):
        """Logs and saves specific chunks of documents to a file"""
        log_entries = []
        for i in (0, 1, 2, 15, -1):
            if i < len(chunks_filtered):  # Avoid out-of-range errors
                log_entries.append(
                    f"[Document {i} of {len(chunks_filtered)}]\n"
                    f"Chunk:\n{chunks_filtered[i].page_content}\n\n"
                    f"{'=' * 125}\n"
                )
        combined_log = "\n".join(log_entries)
        logging.debug(f"Sample chunks:\n{combined_log}")

