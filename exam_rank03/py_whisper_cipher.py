#!/usr/bin/env python3

def whisper_cipher(text: str, shift: int) -> str:
    result = ""
    for char in text:
        if char.islower():
            offset = ord('a')
            result += chr((ord(char) - offset + shift) % 26 + offset)
        elif char.isupper():
            offset = ord('A')
            result += chr((ord(char) - offset + shift) % 26 + offset)
        else:
            result += char
    return result

print(whisper_cipher("hello", 3))
print(whisper_cipher("Hello World!", 1))
print(whisper_cipher("xyz", 3))
print(whisper_cipher("ABC123def", 5))
print(whisper_cipher("", 10))
print(whisper_cipher("abc", -3))