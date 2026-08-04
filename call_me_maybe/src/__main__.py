import argparse
import sys

from pathlib import Path

from .errors import CallMeMaybeError
from .loader import load_prompts, load_functions


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
        print(len(prompts), len(functions))
    except CallMeMaybeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
