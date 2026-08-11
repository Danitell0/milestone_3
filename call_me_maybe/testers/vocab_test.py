from src.grammar import is_valid_number_prefix, is_whole_number, allowed_number_tokens

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

test_prefix()
test_whole()
test_allowed()
