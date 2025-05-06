from __future__ import annotations

from config.pipeline_context import PipelineContext
from src.core.base_pipeline import BasePipeline
from src.pipelines.rag.builder import RAGPipelineBuilder
from src.core.types import RAGPipelineModules, RAGComponents
from langchain_core.runnables.base import RunnableSequence

from src.pipelines.rag import step_invoke


class RAGPipeline(BasePipeline):
    def __init__(self, ctx: PipelineContext):
        super().__init__(ctx)
        self.builder = RAGPipelineBuilder(ctx)
    
    @property
    def modules(self) -> RAGPipelineModules:
        return self.builder.modules
    
    @property
    def components(self) -> RAGComponents:
        return self.builder.components
    
    def invoke_rag_system(self) -> RunnableSequence:
        # print(self.components["rag_system"].__repr__())
        return self.build_pipeline(
            def_key="RAG-invoke",
            modules={"input_prompts": self.modules["input_prompts"]},
            step_order=["invoke"],
            checkpoints=["invoke"],
            step_kwargs={"rag_system": self.components["rag_system"]}
        )
        
    # def build_rag_system_memory(self):
    #     return self.build_pipeline(
    #         def_key="RAG-memory",
    #         modules=self.modules,
    #         step_order=["build-memory"],
    #         checkpoints=[],
    #         step_kwargs={
    #             "rag_system": self.rag_system,
    #             "invoker": self.invoker
    #         }
    #     )

    # def build_chat_dashboard(self):
    #     return self.build_pipeline(
    #         def_key="RAG-chat",
    #         modules=self.modules,
    #         step_order=["chat"],
    #         checkpoints=[],
    #         step_kwargs={
    #             "convo_chain": RAGConversationalBuilder(self.ctx, self.rag_system, self.invoker),
    #             # "convo_chain": self.convo_chain,
    #         }
    #     )
