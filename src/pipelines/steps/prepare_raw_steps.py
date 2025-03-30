from __future__ import annotations

from src.core.data_handling.lazy_load import LazyLoad
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_registry import StepRegistry

from src.data.process import ProcessDocuments
from src.data.doc_loader import DocumentLoader

@StepRegistry.register(
    category="processing",
    name="process",
    step_class=ProcessDocuments,
    args={"dataset": "raw-docs-all"},
    outputs=[],
)
@StepRegistry.register(
    category="loading",
    name="load",
    step_class=ProcessDocuments,
    args={"dataset": "raw-paths: Paths"},
    outputs=[],
)

def process_documents(modules: dict) -> list[StepDefinition]:
    return [
        StepDefinition(
            name="load",
            step_class=DocumentLoader,
            args={
                "paths": modules.get("raw-paths"),
            },
        ),
        StepDefinition(
            name="process",
            step_class=ProcessDocuments,
            args={
                "dataset": LazyLoad(dm=modules.get("raw-docs")),
            },
        ),
    ]
