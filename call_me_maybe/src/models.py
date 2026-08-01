from pydantic import BaseModel, ValidationError
from enum import Enum

class JsonType(str, Enum):
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"

class TestPrompt(BaseModel):
    prompt: str

class ParameterSpec(BaseModel):
    type: JsonType

class FunctionSpec(BaseModel):
    name: str
    description: str
    parameters: ...
    returns: ...
