"""Turns one natural-laguage request into one function call.

Generation happens in two constrained passes over a single token sequence.
The first walks a trie of tokenized function names, so the model chooses among
the defined functions and cannot invent one. Once the name is known, its
schema is known too.

That second point is what keeps this tractable. Constraining a whole
JsonTypeonject would need a parser that can answer "what may come next?" at
every position, constraining one scalar at a time needs only the small
auto in grammar.py. Prefilled structure also costs nothing, since appending
known token IDs requires no forwart pass.
"""

from .models import (FunctionSpec, FunctionCall, JsonType,
                     ParamValue)
from llm_sdk import Small_LLM_Model
from .prompt import build_prompt
from .trie import Trie
from .loader import load_vocab
from .grammar import (allowed_number_tokens, is_whole_number,
                      allowed_string_tokens, is_string_closed,
                      is_string_done)
from .errors import CallMeMaybeError

from pathlib import Path
import json

# caps on generated tokens per value
MAX_NUMBER_TOKENS = 20
MAX_STRING_TOKENS = 80


class Engine:
    """Holds the model and the per-run state needed to decode calls."""

    def __init__(
            self,
            model: Small_LLM_Model,
            functions: list[FunctionSpec]) -> None:
        """Prepare everything that can be computed once.

        The vocabulary, the name trie and the seperator token IDs are all
        fixed for a run, so they are built here rather than per request.

        Args:
            model: The loaded language model.
            functions: The available function definitions.
        Raises:
            CallMeMaybeError: If the vocabulary cannot be read or if a
            seperator does not encode to a single token, which would mean
            this tokenizer needs different handling.
        """
        self._model = model
        self._functions = functions
        self._trie = self._build_trie()
        self._vocab = load_vocab(Path(model.get_path_to_vocab_file()))
        self._comma = self._single_token(",")
        self._close = self._single_token("}")
        self._by_name = {f.name: f for f in functions}

    def call(self, prompt: str) -> FunctionCall:
        """Decode one request into a schema-valid function call.

        Args:
            prompt: The user's natural-language requests.
        Returns:
            The selected function and its extracted arguments.
        Raises:
            CallMeMaybeError: If generation exceeds a token limit or the
                schema declares a type without a grammar.
        """
        text = build_prompt(prompt, self._functions)
        ids = self._encode(text)
        # the cursor is instance state, so each call must claim it afresh.
        # Without this every request after the first would find the trie
        # already at a leaf
        self._trie.reset()
        while True:
            allowed = self._trie.allowed()
            # empty only at a leaf, which means a complete name
            if not allowed:
                break
            logits = self._model.get_logits_from_input_ids(ids)
            # equivalent to setting every other logit to -inf and taking
            # the argmax, but over a handful of tokens rather than 151936
            best = max(allowed, key=lambda t: logits[t])
            ids.append(best)
            self._trie.advance(best)
        name = self._trie.name
        spec = self._by_name[name]
        params = self._generate_parameters(ids, spec)
        return FunctionCall(prompt=prompt, name=name, parameters=params)

    def _single_token(self, text: str) -> int:
        """Encode text that is expected to be exactly one token.

        Args:
            text: The literal to encode.
        Returns:
            Its token ID.
        Raises:
            CallMeMaybeError: If it encodes to any other number of tokens.
        """
        ids = self._encode(text)
        if len(ids) != 1:
            raise CallMeMaybeError(f"expected {text!r} to encode to one "
                                   f"token, got {len(ids)}.")
        return ids[0]

    def _build_trie(self) -> Trie:
        """Tokenize every function name into a prefix tree."""
        name_tokens: dict[str, list[int]] = {}
        for spec in self._functions:
            name_tokens[spec.name] = self._encode(spec.name)
        return Trie(name_tokens)

    def _encode(self, text: str) -> list[int]:
        """Encode text to a flat list of token IDs.

        The SDK returns a two-dimensional tensor while
        get_logits_from_input_ids expects a list, so the conversion is
        kept in one place.
        """
        return self._model.encode(text)[0].tolist()

    def _generate_number(self, ids: list[int], terminator: int,
                         allow_fraction: bool = True) -> str:
        """Generate one number, stopping when the model closes the value.

        Args:
            ids: The token sequence, extended in place with each choice.
            terminator"""
        text = ""
        for _ in range(MAX_NUMBER_TOKENS):
            allowed = allowed_number_tokens(self._vocab, text, allow_fraction)
            if is_whole_number(text, allow_fraction):
                allowed = allowed | {terminator}
            logits = self._model.get_logits_from_input_ids(ids)
            best = max(allowed, key=lambda t: logits[t])
            if best == terminator:
                break
            ids.append(best)
            text += self._vocab[best]
        else:
            raise CallMeMaybeError("internal error: number generator "
                                   "exceeded token limit.")
        return text

    def _generate_string(self, ids: list[int],
                         suffix: str) -> tuple[str, bool]:
        """Generate a string body, returning it with the closing quote (and
        *suffix*) stripped, plus whether the suffix was already emitted."""
        text = ""
        for _ in range(MAX_STRING_TOKENS):
            allowed = allowed_string_tokens(self._vocab, text, suffix)
            logits = self._model.get_logits_from_input_ids(ids)
            best = max(allowed, key=lambda t: logits[t])
            ids.append(best)
            text += self._vocab[best]
            if is_string_done(text, suffix):
                return text[:-2], True
            if is_string_closed(text, suffix):
                return text[:-1], False
        raise CallMeMaybeError("internal error: string generator "
                               "exceeded token limit.")

    def _generate_parameters(self, ids: list[int],
                             spec: FunctionSpec) -> dict[str, ParamValue]:
        values: dict[str, ParamValue] = {}

        params = list(spec.parameters.items())
        if not params:
            ids.extend(self._encode('{}'))
            return {}
        ids.extend(self._encode('{'))
        for i, (param_name, type_spec) in enumerate(params):
            last = (i == len(params) - 1)
            suffix = "}" if last else ","
            terminator = self._close if last else self._comma
            if type_spec.type in (JsonType.NUMBER, JsonType.INTEGER):
                is_int = type_spec.type is JsonType.INTEGER
                ids.extend(self._encode(f'"{param_name}": '))
                text = self._generate_number(ids,
                                             terminator,
                                             allow_fraction=not is_int)
                values[param_name] = int(text) if is_int else float(text)
                ids.append(terminator)
            elif type_spec.type is JsonType.STRING:
                ids.extend(self._encode(f'"{param_name}": "'))
                text, emitted = self._generate_string(ids, suffix)
                values[param_name] = json.loads(f'"{text}"')
                if not emitted:
                    ids.append(terminator)
            else:
                raise CallMeMaybeError(
                        f"unsupported type {type_spec.type.value}")
        return values
