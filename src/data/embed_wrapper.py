from __future__ import annotations

import rust_chunk_embedder


class EmbedWrapper:
    """Wrapper class for embedding documents using Rust."""
    @staticmethod
    def run():
        rust_chunk_embedder.run_embedding_pipeline()
