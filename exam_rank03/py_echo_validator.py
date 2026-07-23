#!/usr/bin/env python3

def echo_validator(text: str) -> bool:
    text = text.lower().replace(" ", "")
    return True if text == text[::-1] else False

print(echo_validator("racecar"))
print(echo_validator("race a car"))
print(echo_validator("Was it a car or a cat I saw"))
print(echo_validator("A man a plan a canal Panama"))
