from __future__ import annotations

from operator import itemgetter

from config.pipeline_context import PipelineContext

from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnableMap
from langchain_huggingface import HuggingFacePipeline
from langchain_community.vectorstores import FAISS


class RAGRetrievalBuilder:
    """
    Summary:
        Builds the retrieval system and augments retrieved documents into RAG pipeline
        for later generation. Utilises FAISS for retrieval and a Hugging Face LLM for
        local text generation.\n
    Input: FAISS vector store ``data_state key: faiss_store``\n
    Output: RAG Pipeline ``data_state key: rag_pipeline``\n
    Steps:
        1) Load FAISS store from state\n
        2) Initialise the retriever from the FAISS store\n
        3) Build the RAG Pipeline chain by combining retrieval and augmentation steps\n
        4) Save RAG Pipeline chain to state
    """

    def __init__(
        self, ctx: PipelineContext,
        faiss_store: FAISS,
        language_pipeline: HuggingFacePipeline,
    ):
        self.ctx = ctx
        self.faiss_store = faiss_store.as_retriever()
        self.language_pipeline = language_pipeline

    def run(self):
        """Initialize the RAG pipeline components and save to state."""
        retrieval_step = self.make_retrieval_step(self.faiss_store)
        first_map_step = self._first_map_step()
        second_map_step = self._second_map_step()
        prompt_step = self.make_prompt_template()
        
        rag_pipeline = (
            retrieval_step
            | first_map_step
            | second_map_step
            | self.build_generation_step()
            | self.build_output()
        )
        return rag_pipeline

    def build_output(self):
        return RunnableLambda(self.process_output, name="output_finaliser")
    
    def build_generation_step(self):
        """Build the LLM generation step."""
        # Create the response and source_docs dict
        return RunnableMap({
            "response": self._create_generation_chain(),
            "source_docs": itemgetter("source_docs"),
        })
    
    def _create_generation_chain(self):
        """Create response gen chain from the LLM."""
        input_mapping = {
            "context": itemgetter("context"),
            "question": itemgetter("question"),
            "sources": itemgetter("sources"),
        }
        prompt = self.make_prompt_template()
        return input_mapping | prompt | self.language_pipeline
        
    @staticmethod
    def make_retrieval_step(retriever):
        """
        INPUT: {"query": ...}
        OUTPUT: {"docs", "question"}.
        """
        return RunnableLambda(
            lambda inputs: {
                "docs": retriever.invoke(inputs["query"]),
                "question": inputs["query"],
            },
            name="retrieval",
        )

    @staticmethod
    def _first_map_step():
        """
        Maps the initial retrieval results to maintain "docs" and "question".
        INPUT: {"docs", "question"}
        OUTPUT: {"docs", "question"}
        """
        return RunnableMap(
            {
                "docs": itemgetter("docs"),
                "question": itemgetter("question"),
            }
        )

    @staticmethod
    def make_docs_to_str_step():
        """Convert the list of docs to a single string."""
        return RunnableLambda(
            lambda docs: "\n\n".join(doc.page_content for doc in docs), name="docs_to_str"
        )

    @staticmethod
    def format_source_metadata(docs):
        """Format metadata from source documents into a readable format."""
        sources = []
        for i, doc in enumerate(docs):
            source = f"[{i+1}] "
            if "source_file" in doc.metadata:
                source += f"File: {doc.metadata['source_file']} "
            if "page_count" in doc.metadata:
                source += f"Pages: {doc.metadata['page_count']} "
            sources.append(source)
        return "\n".join(sources)

    @staticmethod
    def _second_map_step():
        """
        Maps "docs" to "context" by converting docs to a string and formats metadata.
        INPUT: {"docs", "question"}
        OUTPUT: {"context", "question", "source_docs", "sources"}
        """
        docs_to_str_step = RAGRetrievalBuilder.make_docs_to_str_step()
        return RunnableMap(
            {
                "context": (itemgetter("docs") | docs_to_str_step),
                "question": itemgetter("question"),
                "source_docs": itemgetter("docs"),
                "sources": (itemgetter("docs") | RunnableLambda(RAGRetrievalBuilder.format_source_metadata))
            }
        )
    
    @staticmethod
    def make_prompt_template():
        """Prompt expects {"context", "question", "source_docs"} as input"""
        template = """
            Context information:
            {context}
            
            Sources:
            {sources}
            
            User Question: {question}
            
            Provide a concise summary based on the context above. Include relevant source information in your response.
        """
        return ChatPromptTemplate.from_template(template)

    def process_output(self, inputs):
        """Merge LLM response with source doc metadata"""
        response = inputs.get("response", "")
        source_docs = inputs.get("source_docs", [])
        
        metadata = []
        for i, doc in enumerate(source_docs):
            meta_entry = {
                "index": i,
                "source": doc.metadata.get("source_file", "Unknown"),
                "page_count": doc.metadata.get("page_count", "Unknown"),
                "object_count": doc.metadata.get("object_count", "Unknown"),
            }
            metadata.append(meta_entry)
        
        return {
            "result": response,
            "source_documents": source_docs,
            "metadata": metadata
        }
