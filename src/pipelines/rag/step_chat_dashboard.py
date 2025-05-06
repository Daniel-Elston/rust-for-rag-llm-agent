from __future__ import annotations

from src.core.types import RAGPipelineModules
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepBuilder

from src.rag.dashboard import RAGChatDashboard


@StepBuilder.build(
    definition="RAG-chat", 
    order_idx=8,
    order_name="chat",
    step_class=RAGChatDashboard,
    args={},
    outputs=[]
)
def chat_dashboard_step(modules: RAGPipelineModules, step_kwargs: dict) -> list[StepDefinition]:
    return [
        StepDefinition(
            order_name="chat",
            step_class=RAGChatDashboard,
            args={
                "convo_chain": step_kwargs.get("convo_chain"),
            },
            outputs=["faiss_store_state"],
        ),
    ]
