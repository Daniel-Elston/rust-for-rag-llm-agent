from __future__ import annotations

from src.core.types import RAGPipelineModules
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepBuilder

from src.rag.rag_invoke import InvokeRAG


@StepBuilder.build(
    definition="RAG-invoke", 
    order_idx=7,
    order_name="invoke",
    step_class=InvokeRAG,
    args={"faiss_store": "FAISS", "hf_pipeline": "HuggingFacePipeline"},
    outputs=["response"]
)
def invoke_rag_system_step(modules: RAGPipelineModules, step_kwargs: dict) -> list[StepDefinition]:
    return [
        StepDefinition(
            order_name="invoke",
            step_class=InvokeRAG,
            args={
                "input_prompts": modules.get("input_prompts"),
                "rag_system": step_kwargs.get("rag_system"),
            },
            method_name="invoke_response",
            outputs=["response"],
        ),
    ]
