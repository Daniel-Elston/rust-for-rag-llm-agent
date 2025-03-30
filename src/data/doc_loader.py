from __future__ import annotations

from langchain_community.document_loaders import ArxivLoader, PyPDFLoader

from config.paths import Paths
from config.pipeline_context import PipelineContext
from config.settings import Config


class DocumentLoader:
    """
    Summary: Load all raw documents from local dir or arxiv
    """

    def __init__(
        self, ctx: PipelineContext,
        paths: Paths,
    ):
        self.ctx = ctx
        self.paths = paths
        
        self.config: Config = ctx.settings.config
        self.paths: Paths = ctx.paths
        self.all_docs = []

    def run(self):
        self.load_pdfs()
        self.load_arxiv()
        meta_log = self._log_doc_metadata()
        return {
            "raw-docs-all": self.all_docs,
            "raw-doc-metadata": meta_log
        }

    def load_pdfs(self):
        for idx in ["raw-p1", "raw-p2"]:
            pdf_path = self.paths.get_path(idx)
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            for doc in docs:
                doc.metadata["source_file"] = pdf_path
            self.all_docs.extend(docs)

    def load_arxiv(self):
        for idx in ["raw-x1", "raw-x2"]:
            arx_path = self.paths.get_path(idx)
            loader = ArxivLoader(query=str(arx_path))
            docs = loader.load()
            for doc in docs:
                doc.metadata["source_file"] = f"https://arxiv.org/abs/{arx_path}"
            self.all_docs.extend(docs)

    def _log_doc_metadata(self):
        for i, doc in enumerate(self.all_docs):
            return (
                f"Document {i + 1}:\n"
                f"Metadata:\n{doc.metadata}\n"
                f"Page Content (Sample):\n{doc.page_content[250:1000]}\n\n"
            )
