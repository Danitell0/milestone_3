#!/usr/bin/env python3

def number_base_converter(number: str, from_base: int, to_base: int) -> str:
    if not number:
        return "ERROR"
    if not (2 <= from_base <= 36 and 2 <= to_base <= 36):
        return "ERROR"

    number = number.upper()

    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    decimal = 0
    for char in number:
        if char not in digits:
            return "ERROR"

        value = digits.index(char)

        if value >= from_base:
            return "ERROR"

        decimal = decimal * from_base + value

    if decimal == 0:
        return "0"

    result = []
    while decimal > 0:
        decimal, remainder = divmod(decimal, to_base)
        result.append(digits[remainder])

    return "".join(reversed(result))

print(number_base_converter("101010", 2, 10))
print(number_base_converter("FF", 16, 10))
print(number_base_converter("255", 10, 16))
print(number_base_converter("123", 10, 2))
print(number_base_converter("35", 10, 36))
print(number_base_converter("Z", 36, 10))
print(number_base_converter("123", 1, 10))
print(number_base_converter("G", 16, 10))