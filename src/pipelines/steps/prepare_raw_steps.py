from __future__ import annotations

import logging
from src.core.data_handling.lazy_load import LazyLoad
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepRegistry

from src.core.step_handling.step_registry import register_step_func

from src.data.process import ProcessDocuments
from src.data.doc_loader import DocumentLoader

from config.orchestration import STEP_ORCHESTRATION


definition_key = STEP_ORCHESTRATION["step-defs"]["process-docs"]
order_key = STEP_ORCHESTRATION["step-order"]

@StepRegistry.register(
    definition=definition_key,
    order_idx=1,
    order_name=order_key["process"],
    step_class=ProcessDocuments,
    args={"dataset": "raw-docs-all"},
    outputs=["processed-docs-all"],
)
@StepRegistry.register(
    definition=definition_key,
    order_idx=0,
    order_name=order_key["load"],
    step_class=DocumentLoader,
    args={"dataset": "Paths[raw-paths]"},
    outputs=["raw-docs-all"],
)

@register_step_func(definition_key)
def process_documents(modules: dict) -> list[StepDefinition]:
    logging.warning(f"Registering step - ``{definition_key}: {process_documents.__name__}``")
    return [
        StepDefinition(
            order_name=order_key["load"],
            step_class=DocumentLoader,
            args={
                "paths": modules.get("raw-paths"),
            },
            outputs=["raw-docs-all"],
        ),
        StepDefinition(
            order_name=order_key["process"],
            step_class=ProcessDocuments,
            args={
                "dataset": LazyLoad(dm=modules.get("raw-docs-all")),
            },
            outputs=["processed-docs-all"],
        ),
    ]
