from __future__ import annotations

import re
import unicodedata

from config.pipeline_context import PipelineContext
from src.core.data_handling.data_module import DataModule
from dataclasses import dataclass


@dataclass
class Document:
    page_content: str
    object_count: int
    source_file: str
    metadata: dict


class ProcessDocuments:
    """
    Summary: Light NLP cleaning for document text
    Brief:
        - Standardise special characters if complex fonts
        - Remove excessive whitespace
        - Fix repeated punctuation (e.g. ". ." -> ".")
    """

    def __init__(
        self, ctx: PipelineContext,
        dataset: DataModule,
    ):
        self.ctx = ctx
        self.dataset = dataset

    def run(self):
        self.format_document_text()
        for doc in self.dataset:
            doc.page_content = self.clean_document_text(doc.page_content)
        return {"processed-docs-all": self.dataset}

    def format_document_text(self):
        if isinstance(self.dataset[0], dict):
            self.dataset = [Document(**doc) for doc in self.dataset]
        
    def clean_document_text(self, text: str) -> str:
        text = unicodedata.normalize('NFKC', text)
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"\.\s*\.", ".", text)
        # Remove reference bracket [1], [2]...? Could be useful
        # text = re.sub(r"\[\d+\]", "", text)
        return text