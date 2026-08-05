#!/usr/bin/env python3

import time
from llm_sdk import Small_LLM_Model

potato = Small_LLM_Model()

reverse_string = potato.encode("fn_reverse_string")[0].tolist()
for i in reverse_string:
    print(i, repr(potato.decode(i)))

add_numbers = potato.encode("fn_add_numbers")[0].tolist()
for i in add_numbers:
    print(i, repr(potato.decode(i)))

greet = potato.encode("fn_greet")[0].tolist()
for i in greet:
    print(i, repr(potato.decode(i)))

square_root = potato.encode("fn_get_square_root")[0].tolist()
for i in square_root:
    print(i, repr(potato.decode(i)))

regex = potato.encode("fn_substitute_string_with_regex")[0].tolist()
for i in regex:
    print(i, repr(potato.decode(i)))

for i in ["<|im_end|>", "<think>", "</think>", "<|endoftext|>"]:
    print(repr(i), potato.encode(i)[0].tolist())

t = time.perf_counter()
logits = potato.get_logits_from_input_ids(reverse_string)
print(len(logits), (time.perf_counter() - t) * 1000, "ms")
