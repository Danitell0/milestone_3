#!/usr/bin/env python3

import json

from pathlib import Path
from typing import Any
from pydantic import TypeAdapter, ValidationError

from .errors import CallMeMaybeError
from .models import TestPrompt, FunctionSpec


def _load_json(path: Path) -> Any:
    try:
        with open(path) as file:
            return json.load(file)
    except FileNotFoundError:
        raise CallMeMaybeError(f"{path}: file not found") from None
    except OSError as e:
        raise CallMeMaybeError(f"{path}: {e.strerror}") from e
    except json.JSONDecodeError as e:
        raise CallMeMaybeError(f"{path}: invalid JSON at line {e.lineno},"
                               f" column {e.colno}") from e


def load_prompts(path: Path) -> list[TestPrompt]:
    raw = _load_json(path)
    try:
        result: list[TestPrompt] = TypeAdapter(
                list[TestPrompt]).validate_python(raw)
        return result
    except ValidationError as e:
        first = e.errors()[0]
        where = " -> ".join(str(x) for x in first["loc"])
        raise CallMeMaybeError(f"{path}: {where}: {first['msg']}") from e


def load_functions(path: Path) -> list[FunctionSpec]:
    raw = _load_json(path)
    try:
        result: list[FunctionSpec] = TypeAdapter(
                list[FunctionSpec]).validate_python(raw)
        return result
    except ValidationError as e:
        first = e.errors()[0]
        where = " -> ".join(str(x) for x in first['loc'])
        raise CallMeMaybeError(f"{path}: {where}: {first['msg']}") from e
