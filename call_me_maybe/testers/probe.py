from llm_sdk import Small_LLM_Model
from src.prompt import build_prompt
from pathlib import Path
from src.loader import load_prompts, load_functions


potato = Small_LLM_Model()
prompts = load_prompts(Path("data/input/function_calling_tests.json"))
functions = load_functions(Path("data/input/functions_definition.json"))

text = build_prompt(prompts[0].prompt, functions)
print(text)
print("---")

ids = potato.encode(text)[0].tolist()
print(len(ids), "tokens")
print("first 5 ids:", ids[:5])

print("----")

logits = potato.get_logits_from_input_ids(ids)
best = max(range(len(logits)), key=lambda i: logits[i])
print("model wants:", repr(potato.decode([best])), best)

for fun in functions:
    print(fun.name, potato.encode(fun.name)[0].tolist())
