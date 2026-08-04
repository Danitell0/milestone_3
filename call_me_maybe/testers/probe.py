#!/usr/bin/env python3

from llm_sdk import Small_LLM_Model

potato = Small_LLM_Model()

reverse_string = potato.encode("fn_reverse_string")[0].tolist()
for i in reverse_string:
    print(potato.decode(i))

add_numbers = potato.encode("fn_add_numbers")[0].tolist()
for i in add_numbers:
    print(potato.decode(i))

greet = potato.encode("fn_greet")[0].tolist()
for i in greet:
    print(potato.decode(i))

square_root = potato.encode("fn_get_square_root")[0].tolist()
for i in square_root:
    print(potato.decode(i))


regex = potato.encode("fn_substitute_string_with_regex")[0].tolist()
for i in regex:
    print(potato.decode(i))

