from __future__ import annotations

from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

from config.pipeline_context import PipelineContext
from config.settings import Params


class BuildHFPipeline:
    """
    Summary:
        Generates text using a Hugging Face LLM.\n
    Input: Hugging Face LLM\n
    Output: Generated text\n
    Steps:
        1) Load the Hugging Face model and tokenizer\n
        2) Create a Hugging Face pipeline for text generation\n
        3) Save the pipeline to state
    """

    def __init__(
        self, ctx: PipelineContext,
    ):
        self.ctx = ctx
        self.params: Params = ctx.settings.params

    def build(self):
        language_model_name = self.params.language_model_name
        tokenizer = AutoTokenizer.from_pretrained(
            language_model_name,
            truncation=self.params.truncation,
            model_max_length=self.params.max_input_seq_length,
        )
        model = AutoModelForSeq2SeqLM.from_pretrained(language_model_name)
        hf_pipeline = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=self.params.max_output_seq_length,
        )
        return HuggingFacePipeline(pipeline=hf_pipeline)
