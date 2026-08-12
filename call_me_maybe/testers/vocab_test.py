from src.grammar import (is_valid_number_prefix,
                         is_whole_number,
                         allowed_number_tokens,
                         is_valid_string_prefix,
                         is_whole_string)

def test_prefix() -> None:
    assert is_valid_number_prefix("")     is True
    assert is_valid_number_prefix("2")    is True
    assert is_valid_number_prefix("-")    is True
    assert is_valid_number_prefix("-5")   is True
    assert is_valid_number_prefix("--")   is False
    assert is_valid_number_prefix("5-")   is False
    assert is_valid_number_prefix("2.")    is True
    assert is_valid_number_prefix("2.5")   is True
    assert is_valid_number_prefix("2.5.1") is False
    assert is_valid_number_prefix(".5")    is False
    assert is_valid_number_prefix("-2.5")  is True
    print("Tests passed successfully!")

def test_whole() -> None:
    assert is_whole_number("2")     is True
    assert is_whole_number("2.5")   is True
    assert is_whole_number("-2.5")  is True
    assert is_whole_number("")      is False
    assert is_whole_number("-")     is False
    assert is_whole_number("2.")    is False
    assert is_whole_number("2.5.1") is False
    print("Tests passed successfully!")

def test_allowed() -> None:
    vocab = {15: "0", 13: ".", 220: "Ġ", 99: "123", 100: "x"}
    assert allowed_number_tokens(vocab, "") == {15, 99}
    allowed = allowed_number_tokens(vocab, "")
    assert 15 in allowed        # '0'
    assert 13 not in allowed    # '.'
    assert 220 not in allowed   # 'Ġ' (space)
    print("Tests passed successfully!")

def test_string() -> None:
    assert is_valid_string_prefix("hello") is True
    assert is_valid_string_prefix('say "hi"') is False
    assert is_valid_string_prefix('say \\"hi') is True
    assert is_valid_string_prefix("a\nb") is False
    assert is_valid_string_prefix("a\\") is True
    assert is_whole_string("a\\") is False
    print("String tests passed successfully!")

test_prefix()
test_whole()
test_allowed()
test_string()
