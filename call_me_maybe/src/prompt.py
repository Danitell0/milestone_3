"""Prompt construction for the LLM chat format.

The SDK exposes only the raw tokenizer amnd apply_chat_template lives on 
a private attribute, so the chat markup iswritten out literally here.
Each <|im_start|> marker encodes to a single token ID, which is what
makes the modelread these as turn boundaries rather than as text.

The prompt is the only lever on accuracy. Constrained decoding guarantees
the output parses and matches the schema, but nothing in the grammar
makes the model pick the right function or extract the right values.
"""

from .models import FunctionSpec


def format_functions(functions: list[FunctionSpec]) -> str:
    """Render the function catalogue as one line per function.

    Parameter names and values are included so that the model has the
    information needed during argument extraction, not just during selection.
    Return types are ommited, since the model never produces one.

    Args:
        functions: The available function definitions.

    Returns:
        Newline seperated descriptions, one per function.
    """
    lines: list[str] = []
    for func in functions:
        params = ", ".join(
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


def build_prompt(request: str, functions: list[FunctionSpec]) -> str:
    """Build the full token sequence text for one request.

    The assistant turn is opened but left unfinished so the model's most
    likely continuation is a start of an answer.
    the empty <think> block matches what Qwen3 sees when reasoning is
    disabled.

    Args:
        prompt: The user's request.
        functions: The available functions definitions.

    Returns:
        Chat-formatted text ready to be encoded and fed to the model."""
    system = (
            "You are a function calling assistant. Given a user request, "
            "select the single function from the list below that best "
            "fulfills it.\n"
            "String arguments must be copied exactly as they appear in the "
            "user request, including punctuation and quote characters.\n"
            "Example request: Format template: He said \"hi\" to {u}\n"
            "Example answer: fn_example{\"template\": \"He said "
            "\\\"hi\\\" to {u}\"}\n\n"
            f"Available functions:\n{format_functions(functions)}")
    return (
            f"<|im_start|>system\n{system}<|im_end|>\n"
            f"<|im_start|>user\n{request}<|im_end|>\n"
            f"<|im_start|>assistant\n"
            f"<think>\n\n</think>\n\n"
            )
