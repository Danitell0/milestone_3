from enum import Enum, auto

from .loader import load_vocab


class NumState(Enum):
    START = auto()
    AFTER_MINUS = auto()
    AFTER_DOT = auto()
    INT_DIGITS = auto()
    FRAC_DIGITS = auto()


def _number_state(text: str) -> NumState | None:
    state = NumState.START
    for ch in text:
        if state is NumState.START:
            if ch == "-":
                state = NumState.AFTER_MINUS
            elif ch.isdigit():
                state = NumState.INT_DIGITS
            else:
                return None
        elif state is NumState.AFTER_MINUS:
            if ch.isdigit():
                state = NumState.INT_DIGITS
            else:
                return None
        elif state is NumState.INT_DIGITS:
            if ch.isdigit():
                pass
            elif ch == ".":
                state = NumState.AFTER_DOT
            else:
                return None
        elif state is NumState.AFTER_DOT:
            if not ch.isdigit():
                return None
            state = NumState.FRAC_DIGITS
        elif state is NumState.FRAC_DIGITS:
            if not ch.isdigit():
                return None
    return state


def is_valid_number_prefix(text: str) -> bool:
    return _number_state(text) is not None


def is_whole_number(text: str) -> bool:
    return _number_state(text) in (NumState.INT_DIGITS, NumState.FRAC_DIGITS)

def allowed_number_tokens(vocab: dict[int, str], text: str) -> set[int]:
    allowed_tokens: set[int] = set()
    for token_id, token_text in vocab.items():
        if is_valid_number_prefix(text + token_text):
            allowed_tokens.add(token_id)
    return allowed_tokens
