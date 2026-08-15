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


MAX_NUMBER_TOKENS = 20
MAX_STRING_TOKENS = 80


class Engine:
    def __init__(
            self,
            model: Small_LLM_Model,
            functions: list[FunctionSpec]) -> None:
        self._model = model
        self._functions = functions
        self._trie = self._build_trie()
        self._vocab = load_vocab(Path(model.get_path_to_vocab_file()))
        self._comma = self._single_token(",")
        self._close = self._single_token("}")
        self._by_name = {f.name: f for f in functions}

    def call(self, prompt: str) -> FunctionCall:
        text = build_prompt(prompt, self._functions)
        ids = self._encode(text)
        self._trie.reset()
        while True:
            allowed = self._trie.allowed()
            if not allowed:
                break
            logits = self._model.get_logits_from_input_ids(ids)
            best = max(allowed, key=lambda t: logits[t])
            ids.append(best)
            self._trie.advance(best)
        name = self._trie.name
        spec = self._by_name[name]
        params = self._generate_parameters(ids, spec)
        return FunctionCall(prompt=prompt, name=name, parameters=params)

    def _single_token(self, text: str) -> int:
        ids = self._encode(text)
        if len(ids) != 1:
            raise CallMeMaybeError(f"expected {text!r} to encode to one "
                                   f"token, got {len(ids)}.")
        return ids[0]

    def _build_trie(self) -> Trie:
        name_tokens: dict[str, list[int]] = {}
        for spec in self._functions:
            name_tokens[spec.name] = self._encode(spec.name)
        return Trie(name_tokens)

    def _encode(self, text: str) -> list[int]:
        return self._model.encode(text)[0].tolist()

    def _generate_number(self, ids: list[int], terminator: int,
                         allow_fraction: bool = True) -> str:
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
