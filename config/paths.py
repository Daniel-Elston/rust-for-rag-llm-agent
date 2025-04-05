from __future__ import annotations

import logging
from pathlib import Path
from pprint import pformat
from typing import Dict
from typing import Optional
from typing import Union

import attr


paths_store = {
    # Raw
    "raw-p1": Path("data/raw/demonstrating-quantum-error-mitigation-on-logical-qubits-2501.09079v1.pdf"),
    "raw-p2": Path("data/raw/modeling-entanglement-based-quantum-key-distribution-for-the-nasa-quantum-comms-analysis-suite-2501.08476v1.pdf"),
    "raw-t1": Path("data/raw/test-d1.pdf"),
    "raw-t2": Path("data/raw/test-m2.pdf"),
    "raw-x1": "2501.09079",
    "raw-x2": "2501.08476",
    # "raw-docs-all": Path("data/sdo/raw-docs-all.pkl"),
    "raw-docs-all": Path("data/sdo/rs-docs.pkl"),
    "processed-docs-all": Path("data/processed/processed-docs-all.pkl"),
    "chunked-docs-all": Path("data/processed/chunked_docs.json"),
    "embeddings-docs-all": Path("data/embeddings/embeddings.json"),
    # Outputs
    "raw-doc-metadata": Path("reports/outputs/raw-doc-metadata.txt"),
    "sample-chunks": Path("reports/outputs/sample-chunks.txt"),
    "embeddings_sample": Path("reports/outputs/embeddings_sample.txt"),
    "generated-answers": Path("reports/outputs/generated-answers.txt"),
}


@attr.s
class Paths:
    paths: Dict[str, Path] = attr.ib(factory=dict)

    def __attrs_post_init__(self):
        self.paths = {k: Path(v) for k, v in paths_store.items()}
        logging.debug(f"PathsConfig:\n{pformat(self.paths)}\n")

    def get_path(self, key: Optional[Union[str, Path]]) -> Optional[Path]:
        if key is None:
            return None
        if isinstance(key, Path):
            return key
        return self.paths.get(key)
