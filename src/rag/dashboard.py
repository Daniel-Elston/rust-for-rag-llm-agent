from __future__ import annotations

import gradio as gr

from config.pipeline_context import PipelineContext
from config.settings import Params
from src.rag.memory_retrieval import RAGConversationalBuilder


class RAGChatDashboard:
    """
    Summary:
        Provides a Gradio-based user interface for multi-turn conversations using
        the RAG conversational pipeline. Integrates retrieval, augmentation, and generation
        for a seamless conversational experience.\n
    Input: Conversational chain ``data_state key: convo_chain``\n
    Output: Real-time chat interface for interacting with the RAG pipeline\n
    Steps:
        1) Load the conversational chain from state\n
        2) Accept user input and process it using the conversational chain for retrieval and augmentation\n
        3) Generate LLM responses and update chat history\n
        4) Launch the Gradio chat interface for real-time user interaction
    """
    def __init__(
        self, ctx: PipelineContext,
        convo_chain: RAGConversationalBuilder,
    ):
        self.params: Params = ctx.settings.params
        self.convo_chain = convo_chain

    def run(self):
        """Build and launch the Gradio interface."""
        with gr.Blocks() as demo:
            chatbot = gr.Chatbot(
                label="RAG-based Conversational Agent",
                type="messages"
            )

            # Define input box for user
            user_input = gr.Textbox(
                placeholder="Ask a question...",
                show_label=False
            )

            # Store convo in Gradio state
            conversation_state = gr.State([])

            # Callback to process each user message
            def respond(user_message, chat_history):
                """
                :param user_message: str from the user
                :param chat_history: list of [user_msg, bot_msg] pairs so far
                :return: updated chat_history, plus an empty string to reset user textbox
                """
                # if not self.convo_chain:
                #     bot_msg = "No conversation chain found. Did you run RAGSystem?"
                #     chat_history.append([user_message, bot_msg])
                #     chat_history.append({"role": "assistant", "content": bot_msg})
                #     return chat_history, ""
                if not self.convo_chain:
                    bot_msg = "No conversation chain found. Did you run RAGBuilder?"
                    chat_history.append({"role": "user", "content": user_message})
                    chat_history.append({"role": "assistant", "content": bot_msg})
                    return chat_history, ""

                user_message = user_message[:self.params.max_input_seq_length]

                chat_history.append({
                    "role": "user",
                    "content": user_message
                })

                result = self.convo_chain.invoke(user_message)
                bot_msg = result["answer"]

                chat_history.append({
                    "role": "assistant",
                    "content": bot_msg
                })
                return chat_history, ""

            # Link the input + chatbot to the callback
            user_input.submit(
                fn=respond,
                inputs=[user_input, conversation_state],
                outputs=[chatbot, user_input],
            )

        demo.launch()