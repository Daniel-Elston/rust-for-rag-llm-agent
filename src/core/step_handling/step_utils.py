from __future__ import annotations

from typing import List

from src.core.step_handling.step_definition import StepDefinition
from src.core.data_handling.lazy_load import LazyLoad
from src.core.data_handling.data_module_handler import DataModuleHandler

class StepUtils:
    """
    Summary
    ----------
    Utility class for pipeline step management.
    Handles step registration, argument resolution, and dependency management.
    
    Extended Summary
    ----------
    - Maintains a registry of step configurations
    - Resolves lazy-loaded arguments through DataModuleHandler
    - Provides utility functions for step configuration
    
    Parameters
    ----------
    ctx : PipelineContext
        Container for paths, settings, and pipeline states
    """
    
    def __init__(self, ctx):
        self.ctx = ctx
        self.dm_handler = DataModuleHandler(ctx)
        self._step_map = {}
    
    def configure_steps(self, definitions: List[StepDefinition]) -> None:
        """Stores step definitions in the step map"""
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
    
    def get_step_map(self):
        """Returns the step map for use by ExecutorStep"""
        return self._step_map
