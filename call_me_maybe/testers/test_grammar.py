from src.grammar import (
    is_valid_boolean_prefix,
    is_valid_number_prefix,
    is_valid_string_prefix,
    is_whole_number,
    is_whole_string,
)

# --- numbers ---------------------------------------------------------


def test_number_prefix_accepts_incomplete_values() -> None:
    assert is_valid_number_prefix("") is True
    assert is_valid_number_prefix("-") is True
    assert is_valid_number_prefix("2") is True
    assert is_valid_number_prefix("2.") is True
    assert is_valid_number_prefix("2.5") is True
    assert is_valid_number_prefix("-2.5") is True


def test_number_prefix_rejects_malformed() -> None:
    assert is_valid_number_prefix("--") is False
    assert is_valid_number_prefix("5-") is False
    assert is_valid_number_prefix("5x") is False
    assert is_valid_number_prefix("2.5.1") is False
    assert is_valid_number_prefix(".5") is False


def test_number_completeness_differs_from_prefix() -> None:
    assert is_whole_number("2") is True
    assert is_whole_number("2.5") is True
    assert is_whole_number("-2.5") is True
    assert is_whole_number("") is False
    assert is_whole_number("-") is False
    assert is_whole_number("2.") is False


# --- strings ---------------------------------------------------------


def test_string_prefix_accepts_ordinary_content() -> None:
    assert is_valid_string_prefix("") is True
    assert is_valid_string_prefix("hello") is True
    assert is_valid_string_prefix("The cat sat") is True


def test_string_prefix_handles_escapes() -> None:
    assert is_valid_string_prefix("C:\\\\Users") is True
    assert is_valid_string_prefix('say \\"hi') is True
    assert is_valid_string_prefix('say "hi"') is False


def test_string_prefix_rejects_illegal_characters() -> None:
    assert is_valid_string_prefix("a\nb") is False
    assert is_valid_string_prefix("a\tb") is False
    assert is_valid_string_prefix("caf\u00e9") is False
    assert is_valid_string_prefix("a\ufffd") is False


def test_dangling_backslash_is_a_prefix_but_not_complete() -> None:
    assert is_valid_string_prefix("a\\") is True
    assert is_whole_string("a\\") is False
    assert is_whole_string("a") is True


# --- booleans --------------------------------------------------------


def test_boolean_prefix_tracks_both_literals() -> None:
    assert is_valid_boolean_prefix("") is True
    assert is_valid_boolean_prefix("t") is True
    assert is_valid_boolean_prefix("tr") is True
    assert is_valid_boolean_prefix("fa") is True
    assert is_valid_boolean_prefix("true") is True
    assert is_valid_boolean_prefix("false") is True


def test_boolean_prefix_rejects_anything_else() -> None:
    assert is_valid_boolean_prefix("tx") is False
    assert is_valid_boolean_prefix("truex") is False
    assert is_valid_boolean_prefix("True") is False
