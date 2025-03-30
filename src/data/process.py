from __future__ import annotations

import re
import unicodedata

from config.pipeline_context import PipelineContext
from config.states import DataState
from src.core.data_handling.data_module import DataModule


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
        self.data_state: DataState = ctx.states.data

    def run(self):
        for doc in self.dataset:
            doc.page_content = self.clean_document_text(doc.page_content)
        return {"processed-docs-all": self.dataset}

    def clean_document_text(self, text: str) -> str:
        text = unicodedata.normalize('NFKC', text)
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"\.\s*\.", ".", text)
        # Remove reference bracket [1], [2]...? Could be useful
        # text = re.sub(r"\[\d+\]", "", text)
        return text