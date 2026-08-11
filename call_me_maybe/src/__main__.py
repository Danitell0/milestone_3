import argparse
import sys
import json

from pathlib import Path

from .errors import CallMeMaybeError
from .engine import Engine
from .models import FunctionCall
from .loader import load_prompts, load_functions
from llm_sdk import Small_LLM_Model


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


def main() -> None:
    try:
        args = parse_args()
        prompts = load_prompts(args.input)
        functions = load_functions(args.functions_definition)

        potato = Small_LLM_Model()
        potato_engine = Engine(potato, functions)

        results: list[FunctionCall] = []
        for p in prompts:
            call = potato_engine.call(p.prompt)
            print(f"{p.prompt} -> {call.name}")
            results.append(call)

        args.output.parent.mkdir(parents=True, exist_ok=True)
        data = [r.model_dump() for r in results]
        with open(args.output, "w") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    except CallMeMaybeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
