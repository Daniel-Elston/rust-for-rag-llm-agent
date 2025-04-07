
STEP_ORCHESTRATION = {
    "step-defs": {
        "process-docs": "process-docs", # includes loading step
        "chunk-docs": "chunk-docs",
        "embed-docs": "embed-docs",
        "store-embeddings": "store-embeddings",
    },
    "step-order": {
        "load": "load",
        "process": "process",
        "chunk": "chunk",
        "embed": "embed",
        "faiss-store": "faiss-store",
    }
}
