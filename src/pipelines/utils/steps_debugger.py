from __future__ import annotations

import json
import logging
from pathlib import Path

from config.settings import Config
from src.core.step_handling.step_registry import StepRegistry
from utils.file_access import FileAccess

from config.orchestration import STEP_ORCHESTRATION
from pprint import pprint


def debug_init_components():
    init_metadata = StepRegistry.list_init_components()
    json_output = json.dumps(init_metadata, indent=4)
    path = Path("src/pipelines/utils/comps_metadata.json")
    FileAccess.save_json(init_metadata, path, overwrite=True)
    if Config().output_helpers is True:
        logging.info(f"Initialised Components:\n{"=" * 125}\n{json_output}\nOutput Saved: ``{path}``\n{"=" * 125}\n")
    
def debug_steps():
    steps_metadata = StepRegistry.list_all_steps()

    ordered_steps = []
    for idx, step in enumerate(STEP_ORCHESTRATION["step-defs"], start=0):
        step_metadata = steps_metadata.get(step, [])

        for entry in step_metadata:
            if "step_class" in entry and isinstance(entry["step_class"], type):
                entry["step_class"] = f"{entry['step_class'].__module__}.{entry['step_class'].__qualname__}"
            if "func" in entry:
                entry["func"] = f"{entry['func'].__module__}.{entry['func'].__qualname__}"
            if "definition" or "is_definition" in entry:
                entry.pop("definition", None) and entry.pop("is_definition", None)
                
                
        ordered_steps.append({
            "step": step,
            "step_n": idx,
            "metadata": step_metadata,
        })

    json_output = json.dumps(ordered_steps, indent=4)
    path = Path("src/pipelines/utils/steps_metadata.json")
    FileAccess.save_json(ordered_steps, path, overwrite=True)
    if Config().output_helpers is True:
        logging.info(f"Workflow Steps:\n{"=" * 125}\n{json_output}\nOutput Saved: ``{path}``\n{"=" * 125}\n")
