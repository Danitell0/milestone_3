from .models import FunctionSpec, FunctionCall
from llm_sdk import Small_LLM_Model
from .prompt import build_prompt
from .trie import Trie
from .loader import load_vocab
from .grammar import allowed_number_tokens, is_whole_number
from .errors import CallMeMaybeError

from pathlib import Path


MAX_NUMBER_TOKENS = 20


class Engine:
    def __init__(
            self,
            model: Small_LLM_Model,
            functions: list[FunctionSpec]) -> None:
        self._model = model
        self._functions = functions
        self._trie = self._build_trie()
        self._vocab = load_vocab(Path(model.get_path_to_vocab_file()))

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
        return FunctionCall(prompt=prompt, name=name, parameters={})

    def _build_trie(self) -> Trie:
        name_tokens: dict[str, list[int]] = {}
        for spec in self._functions:
            name_tokens[spec.name] = self._encode(spec.name)
        return Trie(name_tokens)

    def _encode(self, text: str) -> list[int]:
        return self._model.encode(text)[0].tolist()

    def _generate_number(self, ids: list[int], terminator: int) -> str:
        text = ""
        for _ in range(MAX_NUMBER_TOKENS):
            allowed = allowed_number_tokens(self._vocab, text)
            if is_whole_number(text):
                allowed = allowed | {terminator}
            logits = self._model.get_logits_from_input_ids(ids)
            best = max(allowed, key=lambda t: logits[t])
            if best == terminator:
                break
            ids.append(best)
            text += self._vocab[best]
        else:
            raise CallMeMaybeError("internal error: number generator "
                                   "exceeded token list.")
        return text

    def _generate_parameters(self, ids: list[int], spec: FunctionSpec) -> str:
        values = {}

        params =list(spec.parameters.items())
        if not params:
            values.append(self._model.encode('{}'))
            return {}
        values.append(self._model.encode('{'))
        for i, (param_name, type_spec) in enumerate(params):

