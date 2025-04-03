from __future__ import annotations

import logging
from collections import defaultdict
from functools import wraps
from typing import Any
from typing import Dict
from typing import List

from typing import Callable, Dict, Any
from src.core.step_handling.step_definition import StepDefinition


STEP_FUNC_REGISTRY: Dict[str, Callable[..., list[StepDefinition]]] = {}

def register_step_func(definition: str) -> Callable:
    """Decorator to register a step function under a given definition."""
    def decorator(fn: Callable[..., list[StepDefinition]]) -> Callable[..., list[StepDefinition]]:
        STEP_FUNC_REGISTRY[definition] = fn
        return fn
    return decorator


class StepRegistry:
    """
    Summary
    ----------
    Central catalog for pipeline step configurations
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
    _registry: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    @classmethod
    def register(
        cls,
        definition: str,
        order_idx: int,
        order_name: str,
        step_class: Any,
        args: Dict[str, Any],
        outputs: List[str],
    ):
        """
        Registers step metadata in the global registry
        Decorator that records step configuration during module import.
        """
        def decorator(fn):
            # Record the metadata at import time
            metadata = {
                "order_name": order_name,
                "order_idx": order_idx,
                "substep_n": len(cls._registry[definition]),
                "step_class": step_class.__name__,
                "args": args,
                "outputs": outputs,
            }
            cls._registry[definition].append(metadata)

            # Return the original function unmodified
            @wraps(fn)
            def wrapper(*inner_args, **inner_kwargs):
                return fn(*inner_args, **inner_kwargs)
            return wrapper
        return decorator

    @classmethod
    def list_all_steps(cls) -> Dict[str, List[Dict[str, Any]]]:
        """
        Retrieves complete step registry at import time
        Provides snapshot of all registered steps organized by definition.
        """
        return dict(cls._registry)
