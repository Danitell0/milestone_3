"""Command-line entry point, run as 'python -m src'.

This module is the boundary between the outside world and the program.
It read arguments, drives the pipeline and turns anticipated failures
into message and an exit code. It catches only CallMeMaybeError, so a
traceback instead of being disguised as a clean error.
"""

import argparse
import sys

from pathlib import Path

from .errors import CallMeMaybeError
from .engine import Engine
from .models import FunctionCall
from .loader import load_prompts, load_functions, save_results
from llm_sdk import Small_LLM_Model


def parse_args() -> argparse.Namespace:
    """Parse the command-line arguments.

    All three paths are optional and default to the layout the subject
    specifies.

    Returns:
        The parsed arguments with each path as a Path object.
    """
    parser = argparse.ArgumentParser(
            description=(
                "Translate natural-language into schema-valid JSON "
                "function calls using constrained decoding."
                ))
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


def main() -> int:
    """Run the pipeline and write the results.

    Exits with status 1 after printing a single line to stderr if any
    anticipated failure occurs.

    Returns:
    0 on success, 1 if an anticipated failure occurred.
    """
    try:
        args = parse_args()
        prompts = load_prompts(args.input)
        functions = load_functions(args.functions_definition)
        # loading costs seconds and over a gigabyte of memory so the model
        # is built once and reused for every prompt
        model = Small_LLM_Model()
        engine = Engine(model=model, functions=functions)

        results: list[FunctionCall] = []
        for p in prompts:
            call = engine.call(p.prompt)
            print(f"{p.prompt} -> {call.name}", file=sys.stderr)
            results.append(call)
            save_results(results, args.output)
    except CallMeMaybeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
