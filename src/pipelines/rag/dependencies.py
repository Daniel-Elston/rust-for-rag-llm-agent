from __future__ import annotations

from config.settings import Params

from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class RAGPipelineDependencies:
    @staticmethod
    def load_embedding_model(params: Params) -> HuggingFaceEmbeddings:
        return HuggingFaceEmbeddings(
            model_name=params.embedding_model_name,
            model_kwargs={'device': params.device},
            encode_kwargs={'normalize_embeddings': True}
        )

    @staticmethod
    def load_tokenizer(params: Params) -> AutoTokenizer:
        return AutoTokenizer.from_pretrained(
            params.language_model_name,
            truncation=params.truncation,
            model_max_length=params.max_input_seq_length,
        )

    @staticmethod
    def load_llm(params: Params) -> AutoModelForSeq2SeqLM:
        return AutoModelForSeq2SeqLM.from_pretrained(
            params.language_model_name
        )
