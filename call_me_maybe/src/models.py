"""Pydantic schemas for every JSON document the program reads or writes.

Validation happens once, at the boundary: raw dicts from json.load are
turned into these and everything downstream works with objects that
cannot be malformed. A file that parses as JSON but has the wrong shape.
An object where a list is expected, a missing field or an unknown type name.
Fails with a clear messagerather than surfacing as a confusing error later.
"""

from pydantic import BaseModel
from enum import Enum


class JsonType(str, Enum):
    """Parameter types recognised in function_definition.json.

    Inheriting from str keeps the members euqal to their JSON spellings,
    so they serialise back unchanged. Each member maps to a grammar in
    grammar.py. A type outside this set is rejected at loat time rather
    than reaching the decoder.
    """

    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    INTEGER = "integer"


# a value the model may produce for a parameter. a bool comes first
# because it is a subclass of int and a union tried left to right would
# otherwise coerce True into 1
ParamValue = bool | int | float | str


class TestPrompt(BaseModel):
    """One entry from function_calling_tests.json."""
    prompt: str


class TypeSpec(BaseModel):
    """A declared type, used for both parameters and return values."""
    type: JsonType


class FunctionSpec(BaseModel):
    """One entry from functions_definition.json.

    Attributes:
        name: The function's name, tokenized into the selection trie.
        description: Shown to the model to guide which function it picks.
        parameters: Parameter names mapped to their declared types. The keys
            vary per function, so this is a mapping rather than a fixed set of
            fields. Insertion order is preserved from the file and determines
            generation order.
        returns: Declared return type. Parsed for completeness. The program
            will produce calls, never their results."""
    name: str
    description: str
    parameters: dict[str, TypeSpec]
    returns: TypeSpec


class FunctionCall(BaseModel):
    """One entry written to the output file.

    Attributes:
        name: The selected function, guaranteed by the trie to be one of
            the defined names.
        prompt: The original request, echoed back unchanged.
        parameters: Extracted argument values, keyes by parameter name.
    """
    prompt: str
    name: str
    parameters: dict[str, ParamValue]
