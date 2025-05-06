from __future__ import annotations

from src.core.types import RAGPipelineModules
from src.core.data_handling.lazy_load import LazyLoad
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepBuilder

from src.rag.memory_retrieval import RAGConversationalBuilder


@StepBuilder.build(
    definition="RAG-memory", 
    order_idx=7,
    order_name="build-memory",
    step_class=RAGConversationalBuilder,
    args={"faiss_store": "FAISS", "hf_pipeline": "HuggingFacePipeline"},
    outputs=["convo_chain"]
)
def build_rag_system_memory_step(modules: RAGPipelineModules, step_kwargs: dict) -> list[StepDefinition]:
    return [
        StepDefinition(
            order_name="build-memory",
            step_class=RAGConversationalBuilder,
            args={
                "rag_system": step_kwargs.get("rag_system"),
                "invoker": step_kwargs.get("invoker"),
            },
            method_name="run",
            outputs=["convo_chain"],
        ),
    ]
