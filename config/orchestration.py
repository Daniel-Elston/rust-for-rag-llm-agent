from __future__ import annotations

import logging
from pprint import pformat

import attr
from typing import List


@attr.s(frozen=True)
class PipelineOrchestration:
    step_definitions: List[str] = attr.ib(default=[  # Ensure match with *_steps.py decorator fn
        "process-docs"
    ])
    step_order: List[str] = attr.ib(default=[
        "load", 
        "process"
    ])
    save_points: List[str] = attr.ib(default=[
        "load", 
        "process"
    ])

    def __attrs_post_init__(self):
        attr_dict = attr.asdict(self)
        logging.debug(f"{self.__class__.__name__}:\n{pformat(attr_dict)}\n")