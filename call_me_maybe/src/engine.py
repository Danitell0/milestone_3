from .models import FunctionSpec, FunctionCall
from llm_sdk import Small_LLM_Model
from .prompt import build_prompt
from .trie import Trie
from .loader import load_vocab

from pathlib import Path


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
