from __future__ import annotations

from src.core.data_handling.lazy_load import LazyLoad
from src.core.data_handling.data_module import DataModule
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepBuilder

from src.models.faiss_store import BuildVectorStore


@StepBuilder.build(
    definition="load-vector-store", 
    order_idx=4,
    order_name="load-store",
    step_class=BuildVectorStore,
    args={"embeddings": "embeddings-docs-all", "index": "faiss-index"},
    outputs=["faiss-store-state"]
)
def load_vector_store_step(modules: dict[str, DataModule], step_kwargs: dict) -> list[StepDefinition]:
    return [
        StepDefinition(
            order_name="load-store",
            step_class=BuildVectorStore,
            args={
                "embeddings": LazyLoad(dm=modules.get("embeddings-docs-all")),
                "index": LazyLoad(dm=modules.get("faiss-index")),
                "embedding_model": step_kwargs.get("embedding_model"),
            },
            method_name="build_faiss_store",
            outputs=["faiss-store-state"],
        ),
    ]
