
import logging
from langchain_core.runnables import RunnableLambda

class DebugRunnable(RunnableLambda):
    def __init__(self, name="DebugRunnable"):
        super().__init__(self._log_input, name=name)

    def _log_input(self, inputs):
        logging.debug(f"{self.name} received inputs: {inputs}")
        return inputs