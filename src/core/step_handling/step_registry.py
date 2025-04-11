from __future__ import annotations

import logging

from collections import defaultdict
from functools import wraps

from typing import Any, Callable, Dict, List, Type

from config.orchestration import STEP_ORCHESTRATION


class StepRegistry:
    """
    Summary
    ----------
    Central catalog for pipeline step configurations.
    Maintains import-time metadata about pipeline steps using class decorators.
    Enables discovery of available steps and their configurations.

    Extended Summary
    ----------
    - Uses decorator-based registration at module import time
    - Organizes steps by definition (e.g., 'preprocessing', 'modeling')
    - Stores metadata including arguments, outputs, and execution order
    - Provides complete registry inspection via list_all_steps()

    Returns
    -------
    Dict[str, List[Dict[str, Any]]]
        Definition-keyed dictionary of step metadata when using list_all_steps()
    """
    _metadata = defaultdict(list)
    _definitions: Dict[str, Callable] = {}

    @classmethod
    def register(cls, is_definition: bool = False, **kwargs):
        def decorator(fn):
            if is_definition:
                cls._definitions[kwargs['definition']] = fn
            cls._metadata[kwargs['definition']].append(kwargs)
            return fn
        return decorator

    @classmethod
    def get_definition_func(cls, defs_key: str, *args, **kwargs) -> Callable:
        try:
            func = cls._definitions[defs_key]
            logging.info(f"Registering orchestration step: ``{defs_key}``, for func: ``{func.__name__}``")
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error: {e}", exc_info=True)

    @classmethod
    def list_all_steps(cls) -> Dict[str, List[Dict[str, Any]]]:
        return dict(cls._metadata)

class StepBuilder:
    """
    Summary
    ----------
    Simplified step registration
    """
    @classmethod
    def build(
        cls, definition: str,
        order_idx: int,
        order_name: str,
        step_class: Type,
        args: Dict[str, Any],
        outputs: List[str]
    ):
        def decorator(fn):
            @StepRegistry.register(
                definition=STEP_ORCHESTRATION["step-defs"][definition],
                order_idx=order_idx,
                order_name=STEP_ORCHESTRATION["step-order"][order_name],
                step_class=step_class,
                args=args,
                outputs=outputs,
                is_definition=True
            )
            @wraps(fn)
            def wrapped(*args, **kwargs):
                return fn(*args, **kwargs)
            return wrapped
        return decorator