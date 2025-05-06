from __future__ import annotations

import logging
import json

from collections import defaultdict
from functools import wraps

from typing import Any, Callable, Dict, List, Type

from config.orchestration import STEP_ORCHESTRATION
from src.core.step_handling.step_definition import StepDefinition
from pprint import pprint

class StepRegistry:
    """Central registry for steps and components."""
    _metadata = defaultdict(list)  # For step definitions
    _init_components = defaultdict(list)  # For component initialisations
    _definitions: Dict[str, Callable] = {}  # For step definition functions

    @classmethod
    def register(cls, registry_type: str, data: dict) -> None:
        """Register entries into the appropriate registry."""
        if registry_type == 'step_definition':
            definition = data['definition']
            cls._metadata[definition].append(data)
            if data.get('is_definition', False):
                cls._definitions[definition] = data['func']
        elif registry_type == 'component_init':
            def_key = data['def_key']
            data.pop('def_key', None)
            cls._init_components[def_key].append(data)
        else:
            raise ValueError(f"Unknown registry type: {registry_type}")

    @classmethod
    def get_definition_func(cls, defs_key: str, *args, **kwargs) -> Callable:
        try:
            func = cls._definitions[defs_key]
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error: {e}", exc_info=True)

    @classmethod
    def list_all_steps(cls) -> Dict[str, List[Dict[str, Any]]]:
        return dict(cls._metadata)
    
    @classmethod
    def list_init_components(cls) -> Dict[str, List[Dict[str, Any]]]:
        return dict(cls._init_components)


class StepBuilder:
    """Registration with unified decorators."""
    @classmethod
    def build(
        cls, definition: str,
        order_idx: int,
        order_name: str,
        step_class: Type,
        args: Dict[str, Any],
        outputs: List[str]
    ) -> Callable:
        def decorator(fn):
            step_data = {
                'definition': STEP_ORCHESTRATION["step-defs"][definition],
                'sub_step_n': order_idx,
                'order_name': STEP_ORCHESTRATION["step-order"][order_name],
                'step_class': step_class,
                'func': fn,
                'args': args,
                'outputs': outputs,
                'is_definition': True,
            }
            StepRegistry.register('step_definition', step_data)
            
            @wraps(fn)
            def wrapped(*args, **kwargs) -> List[StepDefinition]:
                return fn(*args, **kwargs)
            return wrapped
        return decorator

    @classmethod
    def initialise(cls, def_key: str) -> Callable:
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs) -> Any:
                component = func(self, *args, **kwargs)
                logged_kwargs = {k: str(v.__class__.__name__) for k, v in kwargs.items()}
                init_data = {
                    'def_key': def_key,
                    'pipeline_stage': self.__class__.__name__,
                    'component': f"{component.__class__.__module__}.{component.__class__.__qualname__}",
                    'deps': logged_kwargs,
                }
                # logging.info(f"Initialised Component: {init_data.get('def_key')}")
                StepRegistry.register('component_init', init_data)
                return component
            return wrapper
        return decorator
