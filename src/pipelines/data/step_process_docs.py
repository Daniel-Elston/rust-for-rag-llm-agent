from __future__ import annotations

from src.core.data_handling.lazy_load import LazyLoad
from src.core.data_handling.data_module import DataModule
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepBuilder

from src.data.process import ProcessDocuments
from src.data.doc_loader import DocumentLoader


@StepBuilder.build(
    definition="process-raw-docs", 
    order_idx=1,
    order_name="process",
    step_class=ProcessDocuments,
    args={"dataset": "raw-docs-all"},
    outputs=["processed-docs-all"]
)
@StepBuilder.build(
    definition="process-raw-docs",
    order_idx=0,
    order_name="load-raw",
    step_class=DocumentLoader,
    args={"paths": "raw-paths"},
    outputs=["raw-docs-all"]
)
def load_process_raw_docs_step(modules: dict[str, DataModule]) -> list[StepDefinition]:
    return [
        StepDefinition(
            order_name="load-raw",
            step_class=DocumentLoader,
            args={"paths": modules["raw-paths"]},
            outputs=["raw-docs-all"]
        ),
        StepDefinition(
            order_name="process",
            step_class=ProcessDocuments,
            args={"dataset": LazyLoad(modules["raw-docs-all"])},
            outputs=["processed-docs-all"]
        )
    ]