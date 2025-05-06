# from __future__ import annotations

# from langchain_huggingface import HuggingFacePipeline
# from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

# from config.pipeline_context import PipelineContext
# from config.settings import Params


# class BuildLanguageModel:
#     """
#     Summary:
#         Generates text using a Hugging Face LLM.\n
#     Input: Hugging Face LLM\n
#     Output: Generated text\n
#     Steps:
#         1) Load the Hugging Face model and tokenizer\n
#         2) Create a Hugging Face pipeline for text generation\n
#         3) Save the pipeline to state
#     """

#     def __init__(
#         self, ctx: PipelineContext,
#         llm: AutoModelForSeq2SeqLM,
#         tokenizer: AutoTokenizer,
#     ):
#         self.ctx = ctx
#         self.params: Params = ctx.settings.params
#         self.llm = llm
#         self.tokenizer = tokenizer

#     def build(self):
#         pipe = pipeline(
#             "text2text-generation",
#             model=self.llm,
#             tokenizer=self.tokenizer,
#             max_length=self.params.max_output_seq_length,
#         )
#         return HuggingFacePipeline(pipeline=pipe)
