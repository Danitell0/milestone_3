import pytest

from src.errors import CallMeMaybeError
from src.trie import Trie


def _two_names() -> Trie:
    return Trie.from_names({
        "fn_greet": [8822, 1889, 3744],
        "fn_add_numbers": [8822, 2891, 32964],
    })


def test_first_step_is_forced() -> None:
    trie = _two_names()
    assert trie.allowed() == {8822}


def test_branch_point_offers_every_option() -> None:
    trie = _two_names()
    trie.advance(8822)
    assert trie.allowed() == {1889, 2891}


def test_traversal_reaches_a_complete_name() -> None:
    trie = _two_names()
    for token in (8822, 1889, 3744):
        trie.advance(token)
    assert trie.allowed() == set()
    assert trie.name == "fn_greet"


def test_reset_returns_to_the_root() -> None:
    trie = _two_names()
    for token in (8822, 1889, 3744):
        trie.advance(token)
    trie.reset()
    assert trie.allowed() == {8822}


def test_advance_rejects_an_illegal_token() -> None:
    trie = _two_names()
    with pytest.raises(CallMeMaybeError):
        trie.advance(9999)


def test_name_before_a_leaf_is_an_error() -> None:
    trie = _two_names()
    trie.advance(8822)
    with pytest.raises(CallMeMaybeError):
        trie.name


def test_empty_catalogue_offers_nothing() -> None:
    trie = Trie.from_names({})
    assert trie.allowed() == set()


def test_prefixing_names_are_rejected() -> None:
    with pytest.raises(CallMeMaybeError):
        Trie.from_names({
            "fn_add": [8822, 2891],
            "fn_add_numbers": [8822, 2891, 32964],
        })


def test_shared_prefix_without_collision_is_fine() -> None:
    trie = Trie.from_names({
        "fn_greet": [8822, 1889, 3744],
        "fn_add_numbers": [8822, 2891, 32964],
    })
    assert trie.allowed() == {8822}
