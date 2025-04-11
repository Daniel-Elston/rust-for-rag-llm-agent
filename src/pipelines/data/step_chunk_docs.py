from __future__ import annotations

from src.core.types import DataPipelineModules
from src.core.data_handling.lazy_load import LazyLoad
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepBuilder

from src.data.chunk import ChunkDocuments


@StepBuilder.build(
    definition="chunk-docs", 
    order_idx=2,
    order_name="chunk",
    step_class=ChunkDocuments,
    args={"dataset": "processed_docs_all", "text_splitter": "RecursiveCharacterTextSplitter"},
    outputs=["chunked_docs_all"]
)
def chunk_docs_steps(modules: DataPipelineModules, step_kwargs: dict) -> list[StepDefinition]:
    return [
        StepDefinition(
            order_name="chunk",
            step_class=ChunkDocuments,
            args={
                "dataset": LazyLoad(dm=modules["processed_docs_all"]),
                "text_splitter": step_kwargs.get("text_splitter"),
            },
            outputs=["chunked_docs_all"],
        ),
    ]
