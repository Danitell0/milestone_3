#!/usr/bin/env python3

def string_sculptor(text: str) -> str:
    result = ""
    alter = True
    for char in text:
        if char.isalpha():
            if alter:
                result += char.lower()
                alter = False
            else:
                result += char.upper()
                alter = True
        elif char == " ":
            alter = True
            result += char
        else:
            result += char

    return result

print(string_sculptor("hello"))
print(string_sculptor("hello world"))
print(string_sculptor("abc123def"))
print(string_sculptor("Python3.9!"))
print(string_sculptor(""))