from __future__ import annotations

from abc import ABC
from typing import List, Dict

from config.paths import Paths
from config.pipeline_context import PipelineContext
from config.settings import Config
from config.settings import HyperParams
from config.settings import Params
from config.states import DataState
from config.states import ModelState
from config.states import States
from src.core.data_handling.data_module_handler import DataModuleHandler

from src.core.step_handling.step_executor import StepExecutor
from src.core.step_handling.step_registry import StepRegistry

from config.orchestration import STEP_ORCHESTRATION


class BasePipeline(ABC):
    """
    Summary
    ----------
    Abstract base class for pipeline components
    Provides common infrastructure and accessors for pipeline elements.
    Centralizes access to context, settings, and state management.

    Extended Summary
    ----------
    - Initialises core pipeline components from context
    - Provides type access to:
        - Path configurations
        - Application settings/parameters
        - Pipeline state containers
        - Data module handler

    Outputs
    ----------
    - Initialized base class providing common pipeline infrastructure

    Parameters
    ----------
    ctx : PipelineContext
        Contains all pipeline runtime configurations and state trackers
    """

    def __init__(self, ctx: PipelineContext):
        self.ctx = ctx
        self.paths: Paths = ctx.paths
        self.config: Config = ctx.settings.config
        self.params: Params = ctx.settings.params
        self.hyperparams: HyperParams = ctx.settings.hyperparams
        self.states: States = ctx.states
        self.data_state: DataState = ctx.states.data
        self.model_state: ModelState = ctx.states.model
        self.dm_handler = DataModuleHandler(ctx)
        
        self.defs = STEP_ORCHESTRATION["step-defs"]
        self.order = STEP_ORCHESTRATION["step-order"]
    
    def build_pipeline(
        self, def_key:str,
        modules: Dict,
        step_order: List[str],
        checkpoints: List[str] = None,
        **step_kwargs
    ):
        """
        Template method for standard pipeline construction
        
        Args:
            definition_key: Key from STEP_ORCHESTRATION['step-defs']
            modules: Dictionary of module imports
            step_order: Key from STEP_ORCHESTRATION['step-order']
            checkpoints: Steps where data should be persisted
            step_kwargs: Additional arguments for step definitions
        """
        checkpoints = checkpoints or []
        step_defs = StepRegistry.get_definition_func(
            self.defs.get(def_key),
            modules,
            **step_kwargs
        )
        executor = StepExecutor(self.ctx)
        executor.add_steps(step_defs)
        return executor.run_pipeline(step_order, checkpoints)
