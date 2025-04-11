from __future__ import annotations

from config.settings import Params

from langchain.text_splitter import RecursiveCharacterTextSplitter

class DataPipelineDependencies:
    @staticmethod
    def load_text_splitter(params: Params) -> RecursiveCharacterTextSplitter:
        return RecursiveCharacterTextSplitter(
            chunk_size=params.chunk_size,
            chunk_overlap=params.chunk_overlap,
            separators=params.separators,
        )