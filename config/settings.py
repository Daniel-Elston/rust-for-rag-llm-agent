from __future__ import annotations

import logging
from pprint import pformat

import attr


@attr.s
class Config:
    write_output: bool = attr.ib(default=True)
    overwrite: bool = attr.ib(default=True)
    save_fig: bool = attr.ib(default=True)


@attr.s
class Params:
    device: str = attr.ib(default="cpu")
    chunk_size: int = attr.ib(default=1000)
    chunk_overlap: int = attr.ib(default=50)
    truncation: bool = attr.ib(default=True)
    max_input_seq_length: int = attr.ib(default=512)
    max_output_seq_length: int = attr.ib(default=512)
    separators: list = attr.ib(default=["\n\n", "\n", ".", ";", ",", " ", ""])
    embedding_model_name: str = attr.ib(default="sentence-transformers/all-MiniLM-L6-v2")
    language_model_name: str = attr.ib(default="google/flan-t5-base")
    
    prompt_key: int = attr.ib(default=0)
    retriever_k: int = attr.ib(default=2)

@attr.s
class HyperParams:
    pass


@attr.s
class Settings:
    """config, params, hyper_params"""

    config: Config = attr.ib(factory=Config)
    params: Params = attr.ib(factory=Params)
    hyperparams: HyperParams = attr.ib(factory=HyperParams)

    def __attrs_post_init__(self):
        attr_dict = attr.asdict(self)
        logging.debug(f"{self.__class__.__name__}:\n{pformat(attr_dict)}\n")