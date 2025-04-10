from __future__ import annotations

from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepBuilder

from src.models.llm import BuildLanguageModel


@StepBuilder.build(
    definition="load-llm", 
    order_idx=5,
    order_name="load-model",
    step_class=BuildLanguageModel,
    args={},
    outputs=["hf_pipeline: HuggingFacePipeline"],
)
def build_language_model_step(_, step_kwargs: dict) -> list[StepDefinition]:
    return [
        StepDefinition(
            order_name="load-model",
            step_class=BuildLanguageModel,
            args={
                "llm": step_kwargs.get("llm"),
                "tokenizer": step_kwargs.get("tokenizer"),
            },
            method_name="build",
            outputs=["hf_pipeline: HuggingFacePipeline"],
        ),
    ]
