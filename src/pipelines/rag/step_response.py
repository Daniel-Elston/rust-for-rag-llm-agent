from __future__ import annotations

from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepBuilder

from src.models.response_generator import RAGResponseGenerator


@StepBuilder.build(
    definition="RAG-response", 
    order_idx=6,
    order_name="response",
    step_class="RAGResponseGenerator",
    args={"rag_pipeline": "RunnableLambda"},
    outputs=["generated-answers"]
)
def response_step(modules: dict, step_kwargs: dict) -> list[StepDefinition]:
    return [
        StepDefinition(
            order_name="response",
            step_class=RAGResponseGenerator,
            args={
                "rag_pipeline": step_kwargs.get("rag_pipeline"),
            },
            outputs=["generated-answers"],
        ),
    ]
