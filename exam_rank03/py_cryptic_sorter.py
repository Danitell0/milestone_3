#!/usr/bin/env python3

def count_vowels(s: str) -> int:
    vowels = "aeiou"
    counter = 0

    for char in s:
        if char in vowels:
            counter += 1
    return counter

def check_swap(s1: str, s2: str) -> bool:
    s1_l = s1.lower()
    s2_l = s2.lower()

    if len(s1) > len(s2):
        return True
    elif len(s1) == len(s2):
        if s1_l > s2_l:
            return True
        elif count_vowels(s1_l) > count_vowels(s2_l):
            return True
    return False

def cryptic_sorter(strings: list[str]) -> list[str]:
    limit = len(strings)

    for i in range(limit):
        swapped = False
        for j in range(0, limit - i - 1):
            if check_swap(strings[j], strings[j + 1]):
                strings[j], strings[j + 1] = strings[j + 1], strings[j]
                swapped = True
        if not swapped:
            break
    return strings

if __name__ == "__main__":
    list_1 = ["apple","cat","banana","dog","elephant"]
    list_2 = ["aaa","bbb","AAA","BBB"]
    list_3 = ["hello","world","hi","test"]

    print(cryptic_sorter(list_1))
    print(cryptic_sorter(list_2))
    print(cryptic_sorter(list_3))
    
