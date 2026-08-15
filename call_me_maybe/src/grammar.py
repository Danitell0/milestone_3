from enum import Enum, auto


class NumState(Enum):
    START = auto()
    AFTER_MINUS = auto()
    AFTER_DOT = auto()
    INT_DIGITS = auto()
    FRAC_DIGITS = auto()


class StrState(Enum):
    NORMAL = auto()
    AFTER_BACKSLASH = auto()
    CLOSED = auto()
    DONE = auto()


def _string_state(text: str, suffix: str = "") -> StrState | None:
    """Walk *text* as the body of a JSON string.

    The closing quote is part of the grammar, so a token that fuses it to
    preceding characters (``}"``) can end the string. *suffix* is the single
    character the caller expects after that quote -- ``,`` between parameters
    or ``}`` after the last one -- so a token that fuses that too (``",``)
    ends it as well.
    """
    state = StrState.NORMAL
    for ch in text:
        if state is StrState.DONE:
            return None
        elif state is StrState.CLOSED:
            if ch != suffix:
                return None
            state = StrState.DONE
        elif state is StrState.NORMAL:
            if ch == "\\":
                state = StrState.AFTER_BACKSLASH
            elif ch == '"':
                state = StrState.CLOSED
            elif ord(ch) < 0x20 or ord(ch) > 0x7E:
                return None
        elif state is StrState.AFTER_BACKSLASH:
            if ch in ('"', '\\', '/', 'b', 'f', 'n', 'r', 't'):
                state = StrState.NORMAL
            else:
                return None
    return state


def is_valid_string_prefix(text: str, suffix: str = "") -> bool:
    return _string_state(text, suffix) is not None


def is_whole_string(text: str, suffix: str = "") -> bool:
    return _string_state(text, suffix) is StrState.NORMAL


def is_string_closed(text: str, suffix: str = "") -> bool:
    """True once the closing quote has been written."""
    return _string_state(text, suffix) in (StrState.CLOSED, StrState.DONE)


def is_string_done(text: str, suffix: str = "") -> bool:
    """True when the closing quote *and* the suffix have been written."""
    return _string_state(text, suffix) is StrState.DONE


def _number_state(text: str, allow_fration: bool = True) -> NumState | None:
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
            elif ch == "." and allow_fration:
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


def is_valid_number_prefix(text: str, allow_fration: bool = True) -> bool:
    return _number_state(text, allow_fration) is not None


def is_whole_number(text: str, allow_fration: bool = True) -> bool:
    return _number_state(text, allow_fration) in (NumState.INT_DIGITS,
                                                  NumState.FRAC_DIGITS)


def allowed_number_tokens(vocab: dict[int, str],
                          text: str,
                          allow_fration: bool = True) -> set[int]:
    allowed_tokens: set[int] = set()
    for token_id, token_text in vocab.items():
        if is_valid_number_prefix(text + token_text, allow_fration):
            allowed_tokens.add(token_id)
    return allowed_tokens


def allowed_string_tokens(vocab: dict[int, str], text: str,
                          suffix: str = "") -> set[int]:
    allowed_tokens: set[int] = set()
    for token_id, token_text in vocab.items():
        if is_valid_string_prefix(text + token_text, suffix):
            allowed_tokens.add(token_id)
    return allowed_tokens
