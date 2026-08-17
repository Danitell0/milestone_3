"""Character-level grammars for JSON scalar values.

Constrained decoding needs to answer one question at every generation
step: which tokens could continue the value without breaking JSON? Each
grammar here is a small finite state machine walked one character at a time.
Because the model emits multi-character tokens, a candidate token is legal
only if every one of its characters survives the walk.

A prefix check asks whether the text could still grow into something valid.
A completness check asks whether it is valid right now. The first decides
what the model may emit, the second decides whether generation may stop.
"""

from enum import Enum, auto


class NumState(Enum):
    """Position within a JSON number.

    INT_DIGITS and FRAC_DIGITS are the accepting states. The other 3 mean a
    number has been started but not finished.
    """
    START = auto()
    AFTER_MINUS = auto()
    AFTER_DOT = auto()
    INT_DIGITS = auto()
    FRAC_DIGITS = auto()


class StrState(Enum):
    """Position within a JSON string value and its trailling seperator.

    The walk covers the string body, its closing quote and whatever
    punctuation follows it, so that all three can be constrained together.
    """
    NORMAL = auto()
    AFTER_BACKSLASH = auto()
    CLOSED = auto()
    DONE = auto()


def _string_state(text: str, suffix: str = "") -> StrState | None:
    """Walk test through the string automaton.

    Args:
        text: Characters generated so far, excluding the opening quote.
        suffix: The single character expected after the closing quote,
        typically "," or "}". """
    state = StrState.NORMAL
    for ch in text:
        if state is StrState.DONE:
            # nothing may follow the seperator
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
                # control characters are illegal
                return None
        elif state is StrState.AFTER_BACKSLASH:
            if ch in ('"', '\\', '/', 'b', 'f', 'n', 'r', 't'):
                state = StrState.NORMAL
            else:
                return None
    return state


def is_valid_string_prefix(text: str, suffix: str = "") -> bool:
    """Whether text could still grow into a valid string value."""
    return _string_state(text, suffix) is not None


def is_whole_string(text: str, suffix: str = "") -> bool:
    """whether the closing quote could legally be written next.

    False after a lone backslash since the escape is incomplete."""
    return _string_state(text, suffix) is StrState.NORMAL


def is_string_closed(text: str, suffix: str = "") -> bool:
    """True once the closing quote has been written."""
    return _string_state(text, suffix) in (StrState.CLOSED, StrState.DONE)


def is_string_done(text: str, suffix: str = "") -> bool:
    """True when the closing quote and the suffix have been written."""
    return _string_state(text, suffix) is StrState.DONE


def _number_state(text: str, allow_fration: bool = True) -> NumState | None:
    """Walk text through the number automaton.

    Args:
        text: Characters generated so far.
        allow_fration: Whether a decimal point is permitted. False for
            parameters typed "integer", which keeps int() from failing on
            the result.

    Returns:
        The state reached or None if the text can never become a valid JSON
        number.
    """
    state = NumState.START
    for ch in text:
        if state is NumState.START:
            if ch == "-":
                state = NumState.AFTER_MINUS
            elif ch.isdigit():
                state = NumState.INT_DIGITS
            else:
                # JSON requires a leading digit
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
            # JSON forbids a trailing point, so a digit must follow
            if not ch.isdigit():
                return None
            state = NumState.FRAC_DIGITS
        elif state is NumState.FRAC_DIGITS:
            if not ch.isdigit():
                # a second point will also be rejected
                return None
    return state


def is_valid_number_prefix(text: str, allow_fration: bool = True) -> bool:
    """Whether text coult still grow into a valid number."""
    return _number_state(text, allow_fration) is not None


def is_whole_number(text: str, allow_fration: bool = True) -> bool:
    """Whether text is a complete number that generation may stop on."""
    return _number_state(text, allow_fration) in (NumState.INT_DIGITS,
                                                  NumState.FRAC_DIGITS)


def allowed_number_tokens(vocab: dict[int, str],
                          text: str,
                          allow_fration: bool = True) -> set[int]:
    """Token IDs that may legally continue a number.

    Args:
        vocab: Token IDs mapped to the text they represent.
        text: The number generated so far.
        allow_fration: Whether a decimal point is permitted.

    Returns:
        Every token whose characters keep the number valid. Token IDs
        absent from the vocabulary, including special and padding tokens
        are excluded by construction.
    """
    allowed_tokens: set[int] = set()
    for token_id, token_text in vocab.items():
        if is_valid_number_prefix(text + token_text, allow_fration):
            allowed_tokens.add(token_id)
    return allowed_tokens


def allowed_string_tokens(vocab: dict[int, str], text: str,
                          suffix: str = "") -> set[int]:
    """Token IDs that may legally continue a string value.

    Args:
        vocab: Token IDs mapped to the text they represent.
        text: The value generated so far, excluding the opening quote.
        suffix: The character expected after the closing quote.

    Returns:
        Every token whose character keep the string valid. Tokens carrying
        the closing quote and seperator are included once the body may end
        which lets the model choose merged tokens such as '",' rather than
        being forced onto a rarer path.
    """
    allowed_tokens: set[int] = set()
    for token_id, token_text in vocab.items():
        if is_valid_string_prefix(text + token_text, suffix):
            allowed_tokens.add(token_id)
    return allowed_tokens
