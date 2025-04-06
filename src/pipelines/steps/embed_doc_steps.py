from __future__ import annotations

from src.core.step_handling.step_registry import StepBuilder


@StepBuilder.build(
    definition="embed-docs", 
    order_idx=2,
    order_name="embed",
    step_class="rust_chunk_embedder",
    args={"dataset": "chunked-docs-all"},
    outputs=["embeddings-docs-all"]
)
def embed_docs():
    pass
