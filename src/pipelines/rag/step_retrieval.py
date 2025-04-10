from __future__ import annotations

from src.core.data_handling.lazy_load import LazyLoad
from src.core.data_handling.data_module import DataModule
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepBuilder

from src.rag.rag_system import RAGSystem


@StepBuilder.build(
    definition="RAG", 
    order_idx=6,
    order_name="retrieval",
    step_class=RAGSystem,
    args={"faiss_store": "FAISS", "language_pipeline": "HuggingFacePipeline"},
    outputs=["rag-pipeline"]
)
def retrieval_step(modules: dict[str, DataModule], step_kwargs: dict) -> list[StepDefinition]:
    return [
        StepDefinition(
            order_name="retrieval",
            step_class=RAGSystem,
            args={
                "faiss_store": step_kwargs.get("faiss_store"),
                "hf_pipeline": step_kwargs.get("hf_pipeline"),
                "prompt_template": LazyLoad(dm=modules.get("prompt-template")),
                "input_prompts": LazyLoad(dm=modules.get("input-prompts")),
            },
            outputs=["rag-pipeline"],
        ),
    ]
