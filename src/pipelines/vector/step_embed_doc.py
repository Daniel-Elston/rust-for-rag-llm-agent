from __future__ import annotations

from src.core.types import VectorPipelineModules
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepBuilder

from src.data.embed_wrapper import EmbedWrapper


@StepBuilder.build(
    definition="embed-index-docs", 
    order_idx=3,
    order_name="embed-index",
    step_class="FAISSLoader -> rust_chunk_embedder",
    args={"dataset": "chunked_docs_all"},
    outputs=["embeddings_docs_all", "faiss_index"]
)
def embed_index_chunked_docs_step(modules: VectorPipelineModules) -> list[StepDefinition]:
    return [
        StepDefinition(
            order_name="embed-index",
            step_class=EmbedWrapper,
            args={}, # args called from rust scripts
            outputs=["embeddings_docs_all", "faiss_index"],
        ),
    ]
