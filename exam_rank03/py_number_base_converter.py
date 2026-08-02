#!/usr/bin/env python3

def number_base_converter(number: str, from_base: int, to_base: int) -> str:
    if not number:
        return "ERROR"
    if not (2 <= from_base <= 36 and 2 <= to_base <= 36):
        return "ERROR"

    try:
        decimal = int(number, from_base)
    except:
        return "ERROR"
    if decimal == 0:
        return "0"
    
    result = []
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
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
