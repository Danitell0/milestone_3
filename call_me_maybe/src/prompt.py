from .models import FunctionSpec


def format_functions(functions: list[FunctionSpec]) -> str:
    lines = []
    for func in functions:
        lines.append(f"-> {func.name}: {func.description}")
    return "\n".join(lines)

def build_prompt(prompt: str, functions: list[FunctionSpec]) -> str:
    system = f"Available functions\n{format_functions(functions)}"
    return (
            f"<|im_start|>system\n{system}<|im_end|>\n"
            f"<|im_start|>user\n{prompt}<|im_end|>\n"
            f"<|im_start|>assistant\n"
            f"<think>\n\n</think>\n\n"
            )
