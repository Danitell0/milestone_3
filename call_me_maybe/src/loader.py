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


def _bytes_to_unicode() -> dict[int, str]:
    """Map each byte to the printable char byte-level BPE stores it as."""
    bs = (list(range(ord("!"), ord("~") + 1))
          + list(range(ord("¡"), ord("¬") + 1))
          + list(range(ord("®"), ord("ÿ") + 1)))
    cs = bs[:]
    n = 0
    for b in range(256):
        if b not in bs:
            bs.append(b)
            cs.append(256 + n)
            n += 1
    return dict(zip(bs, (chr(c) for c in cs)))


_BYTE_DECODER = {c: b for b, c in _bytes_to_unicode().items()}


def _decode_token(token: str) -> str:
    """Turn a raw vocab key such as "Ġhello" into the text " hello"."""
    try:
        raw = bytes(_BYTE_DECODER[ch] for ch in token)
    except KeyError:
        return token
    return raw.decode("utf-8", errors="replace")


def load_prompts(path: Path) -> list[TestPrompt]:
    try:
        raw = _load_json(path)
        result: list[TestPrompt] = TypeAdapter(
                list[TestPrompt]).validate_python(raw)
        return result
    except ValidationError as e:
        first = e.errors()[0]
        where = " -> ".join(str(x) for x in first["loc"])
        raise CallMeMaybeError(f"{path}: {where}: {first['msg']}") from e


def load_functions(path: Path) -> list[FunctionSpec]:
    try:
        raw = _load_json(path)
        result: list[FunctionSpec] = TypeAdapter(
                list[FunctionSpec]).validate_python(raw)
        return result
    except ValidationError as e:
        first = e.errors()[0]
        where = " -> ".join(str(x) for x in first['loc'])
        raise CallMeMaybeError(f"{path}: {where}: {first['msg']}") from e


def load_vocab(path: Path) -> dict[int, str]:
    try:
        raw = _load_json(path)
        result: dict[str, int] = TypeAdapter(
                dict[str, int]).validate_python(raw)
        invert = {i: _decode_token(token) for token, i in result.items()}
        return invert
    except ValidationError as e:
        first = e.errors()[0]
        where = " -> ".join(str(x) for x in first['loc'])
        raise CallMeMaybeError(f"{path}: {where}: {first['msg']}") from e
