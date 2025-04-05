from __future__ import annotations

from src.core.data_handling.lazy_load import LazyLoad
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepBuilder

import rust_chunk_embedder


# @StepBuilder.build(
#     definition="embed-docs", 
#     order_idx=2,
#     order_name="embed",
#     step_class=rust_chunk_embedder,
#     args={"dataset": "chunked-docs-all"},
#     outputs=["embeddings-docs-all"]
# )
# def embed_documents(modules: dict) -> list[StepDefinition]:
    # return [
    #     StepDefinition(
    #         order_name="embed",
    #         step_class=rust_chunk_embedder,
    #         args={
    #             "dataset": LazyLoad(dm=modules.get("chunked-docs-all")),
    #         },
    #         outputs=["embeddings-docs-all"],
    #     ),
    # ]
    # return [
    #     StepDefinition(
    #         order_name="embed",
    #         step_class=rust_chunk_embedder.run_embedding_pipeline,
    #         args={
    #             "dataset": LazyLoad(dm=modules.get("chunked-docs-all")),
    #         },
    #         outputs=["embeddings-docs-all"],
    #     ),
    # ]