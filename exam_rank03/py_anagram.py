#!/usr/bin/env python3

def anagram(s1: str, s2: str) -> bool:
    s1 = s1.replace(" ", "")
    s2 = s2.replace(" ", "")
    if len(s1) != len(s2):
        return False
    for char in s1.lower():
        if char not in s2.lower():
            return False
    return True

def new_anagram(s1: str, s2: str) -> bool:
    return sorted(s1.replace(" ", "")) == sorted(s2.replace(" ", ""))

print(anagram("listen", "silent"))
print(anagram("Dormitory", "Dirty Room"))
print(anagram("hello", "world"))
print(anagram("", ""))
print(anagram("abc", "abcc"))
