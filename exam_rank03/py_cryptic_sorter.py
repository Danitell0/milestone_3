#!/usr/bin/env python3

def swap_check(a: str, b: str) -> bool:
    if len(a) != len(b):
        return len(a) < len(b)
    for ch1, ch2 in zip(a, b):
        if ch1.lower() != ch2.lower():
            return ch1.lower() < ch2.lower()

    vowels = "aeiouAEIOU"

    count_a = sum(ch in vowels for ch in a)
    count_b = sum(ch in vowels for ch in b)
    if count_a != count_b:
        return count_a < count_b

def cryptic_sorter(strings: list[str]) -> list[str]:
    for i in range(1, len(strings)):
        current = strings[i]
        j = i - 1

        while j >= 0 and swap_check(current, strings[j]):
            strings[j + 1] = strings[j]
            j -= 1

        strings[j + 1] = current
    return strings

if __name__ == "__main__":
    list_1 = ["apple","cat","banana","dog","elephant"]
    list_2 = ["aaa","bbb","AAA","BBB"]
    list_3 = ["hello","world","hi","test"]

    print(cryptic_sorter(list_1))
    print(cryptic_sorter(list_2))
    print(cryptic_sorter(list_3))
    print(cryptic_sorter([]))
    print(cryptic_sorter([""]))

