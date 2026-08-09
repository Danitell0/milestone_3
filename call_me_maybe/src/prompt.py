from .models import FunctionSpec


def format_functions(functions: list[FunctionSpec]) -> str:
    lines: list[str] = []
    for func in functions:
        lines.append(f"-> {func.name}: {func.description}")
    return "\n".join(lines)

def build_prompt(prompt: str, functions: list[FunctionSpec]) -> str:
    system = (
            "You are a function calling assistant, Given a user request, "
            "select the single function from the list below that best "
            "fulfills it.\n\n"
            f"Available functions\n{format_functions(functions)}")
    return (
            f"<|im_start|>system\n{system}<|im_end|>\n"
            f"<|im_start|>user\n{prompt}<|im_end|>\n"
            f"<|im_start|>assistant\n"
            f"<think>\n\n</think>\n\n"
            )
