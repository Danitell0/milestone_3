#!/usr/bin/env python3

def echo_validator(text: str) -> bool:
    # The line below doesn't take care of all spaces or other characters; what if there's a number or tabs?
    # text = text.lower().replace(" ", "") 
    # to fix this:
    for character in text:
        if character.isalpha():
            just_alphabetical += character.lower()

    if just_alphabetical == "":
        return False
    # you also need to check if the 
    return True if just_alphabetical == just_alphabetical[::-1] else False

print(echo_validator("racecar"))
print(echo_validator("race a car"))
print(echo_validator("Was it a car or a cat I saw"))
print(echo_validator("A man a plan a canal Panama"))
