#!/usr/bin/env python3

from pathlib import Path

from .errors import CallMeMaybeError

def _load_json(path: Path) -> Any:
    try:
        with open(path) as file:
            return json.load(file)
    except FileNotFoundError:
        raise CallMeMaybeError()
