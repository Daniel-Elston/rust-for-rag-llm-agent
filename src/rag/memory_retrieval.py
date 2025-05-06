from __future__ import annotations

from config.pipeline_context import PipelineContext
from src.rag.rag_system import RAGSystem
from src.rag.rag_invoke import InvokeRAG
from src.rag.rag_system import RAGSystem

from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage


class RAGConversationalBuilder:
    """
    Wraps your existing RAGSystem with conversation memory
    while preserving its document processing logic.
    """
    def __init__(
        self, ctx: PipelineContext,
        rag_system: RAGSystem,
        invoker: InvokeRAG
    ):
        self.ctx = ctx
        self.rag_system = rag_system
        self.invoker = invoker
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history",
            max_token_limit=1000
        )

    def _format_chat_history(self, chat_history: list) -> str:
        """Convert LangChain message objects to text"""
        formatted = []
        for msg in chat_history:
            if isinstance(msg, HumanMessage):
                formatted.append(f"Human: {msg.content}")
            elif isinstance(msg, AIMessage):
                formatted.append(f"Assistant: {msg.content}")
        return "\n".join(formatted)
    
    def invoke(self, query: str) -> dict:
        history = self.memory.load_memory_variables({})["chat_history"]
        # augmented_query = f"""
        # Chat History:
        # {self._format_chat_history(history)}
        
        # New Question: {query}
        # """
        augmented_query = self.prompt_template.format(
            context="",  # Add context if needed
            question=f"Chat History: {history}\nNew Question: {query}"
        )
        augmented_query = augmented_query[:self.ctx.settings.params.max_input_seq_length]
        # response = InvokeRAG(self.ctx, self.rag_system).invoke_response(augmented_query)
        response = self.invoker.invoke_response(query=augmented_query, save=False)
        
        self.memory.chat_memory.add_user_message(query)
        self.memory.chat_memory.add_ai_message(response["answer"])
        
        return response
    
    def run(self):
        pass