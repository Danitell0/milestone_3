import argparse
import json
import sys

from pathlib import Path
from typing import Any

from .errors import CallMeMaybeError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
            description="Parsing arguments to get PATH")
    parser.add_argument("--input",
                        default=Path(
                            "data/input/function_calling_tests.json"),
                        type=Path,
                        help="The path for the input")
    parser.add_argument("--output",
                        default=Path(
                            "data/output/function_calling_results.json"),
                        type=Path,
                        help="The path for the output")
    parser.add_argument("--functions_definition",
                        default=Path(
                            "data/input/functions_definition.json"),
                        type=Path,
                        help="The path to the functions definitions")
    args = parser.parse_args()

    return args


def load_json(path: Path) -> Any:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise CallMeMaybeError(f"{path}: file not found")
    except json.JSONDecodeError as e:
        raise CallMeMaybeError(f"{path}: invalid JSON at line {e.lineno},"
                               f" column {e.colno}") from e


def main() -> None:
    try:
        args = parse_args()
        prompts = load_json(args.input)
        functions = load_json(args.functions_definition)
        print(len(prompts), len(functions))
    except CallMeMaybeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
