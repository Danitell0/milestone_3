#!/usr/bin/env python3

def string_permutation_checker(s1: str, s2: str) -> bool:
    for char in s1:
        if char not in s2:
            return False
    for char in s2:
        if char not in s1:
            return False
    return True

print(string_permutation_checker("abc", "bca"))
print(string_permutation_checker("abc", "def"))
print(string_permutation_checker("listen", "silent"))
print(string_permutation_checker("hello", "bello"))
print(string_permutation_checker("", ""))
print(string_permutation_checker("a", ""))
print(string_permutation_checker("Abc", "abc"))
print(string_permutation_checker("a gentleman", "elegant man"))