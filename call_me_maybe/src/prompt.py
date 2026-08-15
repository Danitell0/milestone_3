from .models import FunctionSpec


def format_functions(functions: list[FunctionSpec]) -> str:
    lines: list[str] = []
    for func in functions:
        params = " ,".join(
                f"{name} ({spec.type.value})"
                for name, spec in func.parameters.items()
                )
        if params:
            lines.append(
                    f"-> {func.name}: {func.description} "
                    f"Parameters: {params}")
        else:
            lines.append(
                    f"-> {func.name}: {func.description} (no parameters)")
    return "\n".join(lines)


def build_prompt(prompt: str, functions: list[FunctionSpec]) -> str:
    system = (
            "You are a function calling assistant, Given a user request, "
            "select the single function from the list below that best "
            "fulfills it.\n"
            "String arguments must be copied exactly as they appear in the "
            "user request, including punctuation and quote characters.\n"
            "Example request: Format template: He said \"hi\" to {u}\n"
            "Example answer: fn_example{\"template\": \"He said "
            "\\\"hi\\\" to {u}\"}\n\n"
            f"Available functions\n{format_functions(functions)}")
    return (
            f"<|im_start|>system\n{system}<|im_end|>\n"
            f"<|im_start|>user\n{prompt}<|im_end|>\n"
            f"<|im_start|>assistant\n"
            f"<think>\n\n</think>\n\n"
            )
