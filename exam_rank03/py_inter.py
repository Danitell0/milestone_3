#!/usr/bin/env python3

def inter(s1: str, s2: str) -> str:
    result = ""
    for char in s1:
        if char in s2:
            if char in result:
                continue
            result += char
    return result

print(inter("hello", "world"))
print(inter("banana", "band"))
print(inter("abcabc", "bc"))
print(inter("abc", "xyz"))
print(inter("", "abc"))