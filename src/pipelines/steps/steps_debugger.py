from __future__ import annotations

import json
import logging
from pathlib import Path

from src.core.step_handling.step_registry import StepRegistry
from utils.file_access import FileAccess

from config.pipeline_context import PipelineContext
from src.core.base_pipeline import BasePipeline


definition_sequence = BasePipeline(PipelineContext()).defs

def debug_steps():
    steps_metadata = StepRegistry.list_all_steps()

    ordered_steps = []
    for idx, step in enumerate(definition_sequence, start=1):
        step_metadata = steps_metadata.get(step, [])
        ordered_steps.append({
            "step": step,
            "step_n": idx,
            "metadata": step_metadata,
        })

    json_output = json.dumps(ordered_steps, indent=4)
    path = Path("src/pipelines/steps/steps_metadata.json")
    logging.warning(f"\n{json_output}\nSaving Output File: ``{path}``")
    FileAccess.save_json(ordered_steps, path, overwrite=True)
