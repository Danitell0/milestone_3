from .models import FunctionSpec
from llm_sdk import Small_LLM_Model


class Engine:
    def __init__(
            self,
            model: Small_LLM_Model,
            functions: list[FunctionSpec]) -> None:
