from __future__ import annotations

import logging
from src.core.data_handling.lazy_load import LazyLoad
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepRegistry

from src.core.step_handling.step_registry import register_step_func

from src.data.chunk import ChunkDocuments
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config.orchestration import STEP_ORCHESTRATION


definition_key = STEP_ORCHESTRATION["step-defs"]["chunk-docs"]
order_key = STEP_ORCHESTRATION["step-order"]

@StepRegistry.register(
    definition=definition_key,
    order_idx=2,
    order_name=order_key["chunk"],
    step_class=ChunkDocuments,
    args={"dataset": "processed-docs-all"},
    outputs=["chunked-docs-all"],
)


@register_step_func(definition_key)
def chunk_documents(modules: dict, text_splitter: RecursiveCharacterTextSplitter) -> list[StepDefinition]:
    logging.warning(f"Registering step - ``{definition_key}: {chunk_documents.__name__}``")
    return [
        StepDefinition(
            order_name=order_key["chunk"],
            step_class=ChunkDocuments,
            args={
                "dataset": LazyLoad(dm=modules.get("processed-docs-all")),
                "text_splitter": text_splitter,
            },
            outputs=["chunked-docs-all"],
        ),
    ]
