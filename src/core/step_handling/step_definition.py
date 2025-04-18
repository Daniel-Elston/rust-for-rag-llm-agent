from __future__ import annotations

from typing import Type

import attrs


@attrs.define
class StepDefinition:
    order_name: str
    step_class: Type
    args: dict
    method_name: str = "run"
    outputs: list[str] = attrs.field(factory=list)
