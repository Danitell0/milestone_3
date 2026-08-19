"""Reading and validating every file the program loads from disk.

All file I/O and schema validation lives here, so the rest of the program
works with typed objects and never touches raw JSON. Each loader translates
its underlying failures into CallMeMaybeError.
"""

import json

from pathlib import Path
from typing import Any
from pydantic import TypeAdapter, ValidationError

from .errors import CallMeMaybeError
from .models import TestPrompt, FunctionSpec, FunctionCall


def _load_json(path: Path) -> Any:
    """Read and parse a JSON file.

    Args:
        path: The file to read.
    Returns:
        The parsed document of whatever shape the file contained.
    Raises:
        CallMeMaybeError: If the file is missing, unreadable or not
            valid JSON.
    """
    try:
        with open(path) as file:
            return json.load(file)
    except FileNotFoundError:
        raise CallMeMaybeError(f"{path}: file not found") from None
    except OSError as e:
        # catches the cases a specific handler would miss like a directory
        # in place of a file, permission denied, a broken symlink
        raise CallMeMaybeError(f"{path}: {e.strerror}") from e
    except json.JSONDecodeError as e:
        raise CallMeMaybeError(f"{path}: invalid JSON at line {e.lineno},"
                               f" column {e.colno}") from e


def _bytes_to_unicode() -> dict[int, str]:
    """Map each byte to the printable char byte-level BPE stores it as.

    Byte-level BPE has to keep arbitrary bytes inside a JSON text file,
    so every byte gets a printable stand-in. Printable ASCII and most of
    Latin-1 represent themselves. The remaining 68 bytes are pushed into the
    range starting at U+0100. This is why a space appears as "Ġ" and
    a newline as "Ċ" in vocab.json.
    
    Returns:
        All 256 byte values mapped to distinct characters.
    """
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

# Built once at import, inverts the table above for decoding
_BYTE_DECODER = {c: b for b, c in _bytes_to_unicode().items()}


def _decode_token(token: str) -> str:
    """Turn a raw vocab key such as "Ġhello" into the text " hello".

    Args:
        token: A key from vocab.json, in its byte-encoded form.

    Returns:
        The text the token represents. A token holding only part of a
        multi-byte character decodes to U+FFFD, which the string grammar
        rejects so such tokens are never selected alone.
    """
    try:
        raw = bytes(_BYTE_DECODER[ch] for ch in token)
    except KeyError:
        # added tokens are stored literally rather than byte-enocded, so
        # they contain characters outside the table, pass them through
        return token
    return raw.decode("utf-8", errors="replace")


def load_prompts(path: Path) -> list[TestPrompt]:
    """Load and validate the natural-language requests.

    Args:
        path: Path to function_calling_tests.json.
    Returns:
        The requests, in file order.
    Raises:
        CallMeMaybeError: If the file cannot be read, is not valid JSON or
            does not match the expected schema."""
    try:
        raw = _load_json(path)
        result: list[TestPrompt] = TypeAdapter(
                list[TestPrompt]).validate_python(raw)
        return result
    except ValidationError as e:
        # Pydantic own message is verbose and cites internal URLs
        # the first error's location and reason are what a user can act on
        first = e.errors()[0]
        where = " -> ".join(str(x) for x in first['loc'])
        raise CallMeMaybeError(f"{path}: {where}: {first['msg']}") from e


def load_functions(path: Path) -> list[FunctionSpec]:
    """Load the catalogue of callable functions.

    Args:
        path: Path to functions_definition.json.
    Returns:
        The function definitions, in file order.
    Raises:
        CallMeMaybeError: If the file is unreadable, malformed or any entry
            has a missing field or an unrecognised parameter type.
    """
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
    """Load the tokenizer vocabulary, keyed by token ID.

    The file maps text to ID, the decoder needs the reverse and the stored
    text is byte-encoded rather than literal.

    Args:
        path: Path to vocab.json, obtained from SDK.
    Returns:
        Token IDs mapped to the text they represent. Special and padding
        token IDs are absent from the file and therefore from this map, which
        is what keeps the grammar from ever selecting one.
    Raises:
        CallMeMaybeError: If the is unreadable or malformed.
    """
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


def save_results(results: list[FunctionCall], path: Path) -> None:
    """Write the function calls to path as JSON.

    Args:
        results: The calls to serialise.
        path: Destination file. Parent directories are created.
    Raises:
        CallMeMaybeError: If the file cannot be written.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as file:
            json.dump([r.model_dump() for r in results], file,
                      indent=2, ensure_ascii=False)
    except OSError as e:
        raise CallMeMaybeError(f"{path}: {e.strerror}") from e
