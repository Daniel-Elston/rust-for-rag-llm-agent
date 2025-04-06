from __future__ import annotations

import json
import logging
from pathlib import Path

from src.core.step_handling.step_registry import StepRegistry
from utils.file_access import FileAccess

from config.orchestration import STEP_ORCHESTRATION


def debug_steps():
    steps_metadata = StepRegistry.list_all_steps()

    ordered_steps = []
    for idx, step in enumerate(STEP_ORCHESTRATION["step-defs"], start=0):
        step_metadata = steps_metadata.get(step, [])
        
        for entry in step_metadata:
            if "step_class" in entry and isinstance(entry["step_class"], type):
                entry["step_class"] = f"{entry['step_class'].__module__}.{entry['step_class'].__qualname__}"
                
        ordered_steps.append({
            "step": step,
            "step_n": idx,
            "metadata": step_metadata,
        })

    json_output = json.dumps(ordered_steps, indent=4)
    path = Path("src/pipelines/steps/steps_metadata.json")
    FileAccess.save_json(ordered_steps, path, overwrite=True)
    logging.warning(f"Workflow Steps:\n{"=" * 125}\n{json_output}\nOutput Saved: ``{path}``\n{"=" * 125}\n")
