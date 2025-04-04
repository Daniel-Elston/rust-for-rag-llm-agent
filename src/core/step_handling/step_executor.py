from __future__ import annotations

import logging
from typing import Callable
from typing import List

from utils.logging_utils import log_step
from src.core.data_handling.data_module_handler import DataModuleHandler
from src.core.step_handling.step_definition import StepDefinition
from src.core.data_handling.lazy_load import LazyLoad


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
        self._step_map = {}
    
    def register_steps(self, definitions: List[StepDefinition]) -> None:
        """Stores step definitions"""
        self._step_map.update({
            step_def.order_name: (
                step_def.step_class,
                step_def.args,
                step_def.method_name
            )
            for step_def in definitions
        })

    def resolve_args(self, step_name: str, **runtime_extra):
        """Handles argument resolution for a step, including lazy-loaded dependencies."""
        try:
            StepClass, base_args, method_name = self._step_map[step_name]
        except KeyError:
            available = list(self._step_map.keys())
            raise KeyError(f"Unknown key input for step. Registered steps: {available}")

        resolved_args = {}
        for k, v in base_args.items():
            if isinstance(v, LazyLoad):
                resolved_args[k] = v.load(self.dm_handler)
            else:
                resolved_args[k] = v
                
        return StepClass, method_name, {**resolved_args, **runtime_extra}

    def run_step(self, step_name: str, **runtime_extra):
        StepClass, method, args = self.resolve_args(step_name, **runtime_extra)
        instance = StepClass(ctx=self.ctx, **args)
        method = getattr(instance, method)
        return log_step()(method)()

    def run_pipeline(self, step_order: List[str], checkpoints: List[str] = None) -> None:
        """
        Executes a sequence of pipeline steps with checkpoint support
        Processes steps in specified order, saving intermediate results
        at designated checkpoints using DataModuleHandler.
        """
        checkpoints = checkpoints or []
        for step_name in step_order:
            result = self.run_step(step_name)
            if step_name in checkpoints:
                logging.info(f"SAVING at checkpoint: {step_name}")
                self.dm_handler.save_data(result)

    def run_main(self, steps: List[Callable]):
        """Applies log_step decorator to each step and executes in sequence."""
        for step in steps:
            log_step()(step)()
