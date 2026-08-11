from pydantic import BaseModel
from enum import Enum


class JsonType(str, Enum):
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    INTEGER = "integer"


class TestPrompt(BaseModel):
    prompt: str


class TypeSpec(BaseModel):
    type: JsonType


class FunctionSpec(BaseModel):
    name: str
    description: str
    parameters: dict[str, TypeSpec]
    returns: TypeSpec


class FunctionCall(BaseModel):
    name: str
    prompt: str
    parameters: dict[str, bool | int | float | str]
