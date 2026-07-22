#!/usr/bin/env python3

def bracket_validator(s: str) -> bool:
    opener = "([{"
    closer = ")]}"
    waiting = ""

    for char in s:
        if char in opener:
            waiting += char
        elif char in closer:
            if char in closer and waiting and opener[
                    closer.index(char)] == waiting[-1]:
                waiting = waiting[:-1]
            else:
                return False

    if len(waiting) > 0:
        return False
    return True


print("() expecting true: ", bracket_validator("()"))
print("()[]{} expecting true : ", bracket_validator("()[]{}"))
print("(] expecting false: ", bracket_validator("(]"))
print("([)] expecting false: ", bracket_validator("([)]"))
print("{[]} expecting true: ", bracket_validator("{[]}"))
print("hello(world) expecting true: ", bracket_validator("hello(world)"))
print("((()) expecting false: ", bracket_validator("((())"))
print('"" expecting true: ', bracket_validator(""))
print(") expecting false: ", bracket_validator(")"))
