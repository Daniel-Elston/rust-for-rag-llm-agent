from __future__ import annotations

from src.core.data_handling.lazy_load import LazyLoad
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepBuilder

from src.models.faiss_store import FAISSLoader


@StepBuilder.build(
    definition="store-embeddings", 
    order_idx=4,
    order_name="faiss-store",
    step_class="FAISSLoader",
    args={"dataset": "embeddings-docs-all"},
    outputs=["faiss-store-state"]
)
def store_embeds(modules: dict) -> list[StepDefinition]:
    return [
        StepDefinition(
            order_name="faiss-store",
            step_class=FAISSLoader,
            args={
                "embeddings": LazyLoad(dm=modules.get("embeddings-docs-all")),
                "index": LazyLoad(dm=modules.get("faiss-index")),
            },
            method_name="load_faiss_store",
            outputs=["faiss-store-state"],
        ),
    ]