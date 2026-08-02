from pydantic import BaseModel
from enum import Enum


class JsonType(str, Enum):
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"


class TestPrompt(BaseModel):
    prompt: str


class TypeSpec(BaseModel):
    type: JsonType


class FunctionSpec(BaseModel):
    name: str
    description: str
    parameters: dict[str, TypeSpec]
    returns: TypeSpec
