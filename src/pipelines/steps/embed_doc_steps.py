from __future__ import annotations

from src.core.data_handling.lazy_load import LazyLoad
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepBuilder

from src.data.embed_wrapper import EmbedWrapper

@StepBuilder.build(
    definition="embed-docs", 
    order_idx=3,
    order_name="embed",
    step_class="FAISSLoader -> rust_chunk_embedder",
    args={"dataset": "chunked-docs-all"},
    outputs=["embeddings-docs-all", "faiss-index"]
)
def embed_docs(modules: dict) -> list[StepDefinition]:
    return [
        StepDefinition(
            order_name="embed",
            step_class=EmbedWrapper,
            args={}, # args called from rust scripts
            outputs=["embeddings-docs-all", "faiss-index"],
        ),
    ]

