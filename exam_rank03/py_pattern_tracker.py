#!/usr/bin/env python3

def pattern_tracker(text: str) -> int:
    tracker = 0
    prev = None

    for char in text:
        if char.isdigit():
            digit = int(char)
            if prev is not None and digit == prev + 1:
                tracker += 1
            prev = digit
        else:
            prev = None

    return tracker

print(pattern_tracker("123"))
print(pattern_tracker("12a34"))
print(pattern_tracker("987654321"))
print(pattern_tracker("01234567"))
print(pattern_tracker("abc"))
print(pattern_tracker("1a2b3c4"))
print(pattern_tracker("112233"))