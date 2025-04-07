from __future__ import annotations

import logging
from typing import Callable
from typing import List

from utils.logging_utils import log_step
from src.core.data_handling.data_module_handler import DataModuleHandler
from src.core.step_handling.step_definition import StepDefinition
from src.core.step_handling.step_utils import StepUtils


class StepExecutor:
    """
    Summary
    ----------
    Executes pipeline steps according to defined configurations.
    Manages argument resolution, method dispatch, and checkpoint logging.

    Extended Summary
    ----------
    - Maintains a registry of step configurations (classes, arguments, and methods)
    - Handles lazy-loaded argument resolution through DataModuleHandler
    - Supports runtime argument injection via **runtime_extra

    Outputs
    ----------
    - Initialized StepFactory instance ready to execute pipeline steps

    Parameters
    ----------
    ctx : PipelineContext
        Container for paths, settings, and pipeline states
    step_map : dict, optional
        Preconfigured step definitions mapping step names to
        (StepClass, base_args, method_name) tuples
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.dm_handler = DataModuleHandler(ctx)
        self.step_utils = StepUtils(ctx)
    
    def add_steps(self, definitions: List[StepDefinition]) -> None:
        """Adds step definitions to be executed. Delegates to StepUtils"""
        self.step_utils.configure_steps(definitions)

    def run_step(self, step_name: str, **runtime_extra):
        StepClass, method, args = self.step_utils.resolve_args(step_name, **runtime_extra)
        try:
            instance = StepClass(ctx=self.ctx, **args)
        except TypeError:
            instance = StepClass
        method = getattr(instance, method)
        return log_step()(method)()

    def run_pipeline(self, step_order: List[str], checkpoints: List[str] = None) -> None:
        """
        Executes pipeline steps in specified order, saving intermediate 
        results at designated checkpoints using DataModuleHandler.
        """
        checkpoints = checkpoints or []
        for step_name in step_order:
            result = self.run_step(step_name)
            if step_name in checkpoints:
                logging.info(f"SAVING at checkpoint: ``{step_name}``")
                self.dm_handler.save_data(result)

    def run_main(self, steps: List[Callable]):
        """Applies log_step decorator to each step and executes in sequence."""
        for step in steps:
            log_step()(step)()
