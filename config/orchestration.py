# step-defs must be unique per *_steps.py script.
# step-order must be unique per StepDefinition object.
STEP_ORCHESTRATION = {
    "step-defs": {
        "process-raw-docs": "process-raw-docs", # includes loading step
        "chunk-docs": "chunk-docs",
        "embed-index-docs": "embed-index-docs",
        "load-vector-store": "load-vector-store",
        "RAG": "RAG",
        "RAG-response": "RAG-response",
    },
    "step-order": {
        "load-raw": "load-raw",
        "process": "process",
        "chunk": "chunk",
        "embed-index": "embed-index",
        "load-store": "load-store",
        "retrieval": "retrieval",
        "response": "response",
    }
}
