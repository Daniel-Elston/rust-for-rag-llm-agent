from __future__ import annotations

from typing import TypedDict
from config.paths import Paths
from src.core.data_handling.data_module import DataModule


class DataPipelineModules(TypedDict):
    raw_paths: Paths
    raw_docs_all: DataModule
    processed_docs_all: DataModule

class VectorPipelineModules(TypedDict):
    chunked_docs_all: DataModule

class RAGPipelineModules(TypedDict):
    embeddings_docs_all: DataModule
    faiss_index: DataModule
    input_prompts: DataModule
    prompt_template: DataModule
