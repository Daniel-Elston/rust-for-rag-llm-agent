from __future__ import annotations

from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepBuilder

from src.models.retrieval_builder import RAGRetrievalBuilder


@StepBuilder.build(
    definition="RAG", 
    order_idx=5,
    order_name="retrieval",
    step_class="RAGRetrievalBuilder",
    args={"faiss_store": "FAISS", "language_pipeline": "HuggingFacePipeline"},
    outputs=["rag-pipeline"]
)
def retrieval_step(_, step_kwargs: dict) -> list[StepDefinition]:
    return [
        StepDefinition(
            order_name="retrieval",
            step_class=RAGRetrievalBuilder,
            args={
                "faiss_store": step_kwargs.get("faiss_store"),
                "language_pipeline": step_kwargs.get("language_pipeline"),
            },
            outputs=["rag-pipeline"],
        ),
    ]
