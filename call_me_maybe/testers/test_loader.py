import json
from pathlib import Path

import pytest

from src.errors import CallMeMaybeError
from src.loader import load_functions, load_prompts
from src.models import JsonType


def _write(tmp_path: Path, name: str, content: str) -> Path:
    path = tmp_path / name
    path.write_text(content)
    return path


_FUNCTIONS = [
    {
        "name": "fn_add_numbers",
        "description": "Add two numbers together and return their sum.",
        "parameters": {"a": {"type": "number"}, "b": {"type": "number"}},
        "returns": {"type": "number"},
    }
]


# --- prompts ---------------------------------------------------------


def test_prompts_load(tmp_path: Path) -> None:
    path = _write(tmp_path, "p.json", json.dumps([
        {"prompt": "What is the sum of 2 and 3?"},
        {"prompt": "Greet shrek"},
    ]))
    prompts = load_prompts(path)
    assert len(prompts) == 2
    assert prompts[0].prompt == "What is the sum of 2 and 3?"


def test_missing_file_is_reported(tmp_path: Path) -> None:
    with pytest.raises(CallMeMaybeError):
        load_prompts(tmp_path / "nope.json")


def test_directory_instead_of_file_is_reported(tmp_path: Path) -> None:
    with pytest.raises(CallMeMaybeError):
        load_prompts(tmp_path)


def test_truncated_json_is_reported(tmp_path: Path) -> None:
    path = _write(tmp_path, "p.json", '[{"prompt": "hello"')
    with pytest.raises(CallMeMaybeError):
        load_prompts(path)


def test_empty_file_is_reported(tmp_path: Path) -> None:
    path = _write(tmp_path, "p.json", "")
    with pytest.raises(CallMeMaybeError):
        load_prompts(path)


def test_valid_json_of_the_wrong_shape_is_reported(tmp_path: Path) -> None:
    path = _write(tmp_path, "p.json", '{"not": "a list"}')
    with pytest.raises(CallMeMaybeError):
        load_prompts(path)


def test_missing_field_is_reported(tmp_path: Path) -> None:
    path = _write(tmp_path, "p.json", '[{"question": "hello"}]')
    with pytest.raises(CallMeMaybeError):
        load_prompts(path)


# --- functions -------------------------------------------------------


def test_functions_load_with_typed_parameters(tmp_path: Path) -> None:
    path = _write(tmp_path, "f.json", json.dumps(_FUNCTIONS))
    functions = load_functions(path)
    assert len(functions) == 1
    spec = functions[0]
    assert spec.name == "fn_add_numbers"
    assert list(spec.parameters) == ["a", "b"]
    assert spec.parameters["a"].type is JsonType.NUMBER


def test_parameter_order_follows_the_file(tmp_path: Path) -> None:
    path = _write(tmp_path, "f.json", json.dumps([{
        "name": "fn_three",
        "description": "Three parameters in a deliberate order.",
        "parameters": {
            "third": {"type": "string"},
            "first": {"type": "number"},
            "second": {"type": "boolean"},
        },
        "returns": {"type": "string"},
    }]))
    spec = load_functions(path)[0]
    assert list(spec.parameters) == ["third", "first", "second"]


def test_unknown_parameter_type_is_reported(tmp_path: Path) -> None:
    path = _write(tmp_path, "f.json", json.dumps([{
        "name": "fn_odd",
        "description": "Takes something this program cannot generate.",
        "parameters": {"items": {"type": "array"}},
        "returns": {"type": "string"},
    }]))
    with pytest.raises(CallMeMaybeError):
        load_functions(path)


def test_every_supported_type_loads(tmp_path: Path) -> None:
    path = _write(tmp_path, "f.json", json.dumps([{
        "name": "fn_all",
        "description": "One parameter of each supported type.",
        "parameters": {
            "n": {"type": "number"},
            "i": {"type": "integer"},
            "s": {"type": "string"},
            "b": {"type": "boolean"},
        },
        "returns": {"type": "string"},
    }]))
    spec = load_functions(path)[0]
    assert spec.parameters["i"].type is JsonType.INTEGER
    assert spec.parameters["b"].type is JsonType.BOOLEAN
