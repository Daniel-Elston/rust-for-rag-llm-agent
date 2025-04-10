from __future__ import annotations

from src.core.data_handling.lazy_load import LazyLoad
from src.core.data_handling.data_module import DataModule
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepBuilder

from src.data.chunk import ChunkDocuments


@StepBuilder.build(
    definition="chunk-docs", 
    order_idx=2,
    order_name="chunk",
    step_class=ChunkDocuments,
    args={"dataset": "processed-docs-all", "text_splitter": "RecursiveCharacterTextSplitter"},
    outputs=["chunked-docs-all"]
)
def chunk_docs_steps(modules: dict[str, DataModule], step_kwargs: dict) -> list[StepDefinition]:
    return [
        StepDefinition(
            order_name="chunk",
            step_class=ChunkDocuments,
            args={
                "dataset": LazyLoad(dm=modules.get("processed-docs-all")),
                "text_splitter": step_kwargs.get("text_splitter"),
            },
            outputs=["chunked-docs-all"],
        ),
    ]
