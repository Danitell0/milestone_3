#!/usr/bin/env python3

def hidenp(small: str, big: str) -> bool:
    s = 0
    for char in big:
        if s < len(small) and char == small[s]:
            s += 1
    return s == len(small)

print("True: ", hidenp("abc", "a1b2c3"))
print("False: ", hidenp("aec", "abcde"))
print("True: ",hidenp("ace", "abcde"))
print("True: ", hidenp("", "abc"))
print("False: ", hidenp("abc", "ab"))
print("False: ", hidenp("aaaa", "aaa"))
print("True: ", hidenp("sing","subsequence testing"))