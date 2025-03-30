from __future__ import annotations

import logging
from src.core.data_handling.lazy_load import LazyLoad
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepRegistry

from src.data.process import ProcessDocuments
from src.data.doc_loader import DocumentLoader

from src.core.step_handling.step_registry import register_step_func
# from config.orchestration import PipelineOrchestration
from config.pipeline_context import PipelineContext
from src.core.base_pipeline import BasePipeline


DEFINITION_KEY = "process-docs"
step_order = BasePipeline(PipelineContext()).order


@StepRegistry.register(
    definition=DEFINITION_KEY,
    order_name="process",
    step_class=ProcessDocuments,
    args={"dataset": "raw-docs-all"},
    outputs=["processed-docs-all"],
)
@StepRegistry.register(
    definition=DEFINITION_KEY,
    order_name="load",
    step_class=DocumentLoader,
    args={"dataset": "Paths[raw-paths]"},
    outputs=["raw-docs-all"],
)

@register_step_func(DEFINITION_KEY)
def process_documents(modules: dict) -> list[StepDefinition]:
    logging.warning(f"Registering step - ``{DEFINITION_KEY}: {process_documents.__name__}``")
    return [
        StepDefinition(
            order_name=step_order[0],
            step_class=DocumentLoader,
            args={
                "paths": modules.get("raw-paths"),
            },
            outputs=["raw-docs-all"],
        ),
        StepDefinition(
            order_name=step_order[1],
            step_class=ProcessDocuments,
            args={
                "dataset": LazyLoad(dm=modules.get("raw-docs")),
            },
            outputs=["processed-docs-all"],
        ),
    ]
