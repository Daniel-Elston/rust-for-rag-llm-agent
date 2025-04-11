from __future__ import annotations

from src.core.types import DataPipelineModules
from src.core.data_handling.lazy_load import LazyLoad
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepBuilder

from src.data.process import ProcessDocuments
from src.data.doc_loader import DocumentLoader


@StepBuilder.build(
    definition="process-raw-docs", 
    order_idx=1,
    order_name="process",
    step_class=ProcessDocuments,
    args={"dataset": "raw_docs_all"},
    outputs=["processed_docs_all"]
)
@StepBuilder.build(
    definition="process-raw-docs",
    order_idx=0,
    order_name="load-raw",
    step_class=DocumentLoader,
    args={"paths": "raw_paths"},
    outputs=["raw_docs_all"]
)
def load_process_raw_docs_step(modules: DataPipelineModules) -> list[StepDefinition]:
    return [
        StepDefinition(
            order_name="load-raw",
            step_class=DocumentLoader,
            args={"paths": modules["raw_paths"]},
            outputs=["raw_docs_all"]
        ),
        StepDefinition(
            order_name="process",
            step_class=ProcessDocuments,
            args={"dataset": LazyLoad(dm=modules["raw_docs_all"])},
            outputs=["processed_docs_all"]
        )
    ]