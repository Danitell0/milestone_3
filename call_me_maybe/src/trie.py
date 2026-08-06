from dataclasses import dataclass, field
from .errors import CallMeMaybeError

@dataclass
class TrieNode:
    name: str | None = None
    children: dict[int, "TrieNode"] = field(default_factory=dict)

class Trie:
    def __init__(self, names: dict[str, list[int]]) -> None:
        self._root = TrieNode()
        self._cursor = self._root

        for name, ids in names.items():
            node = self._root
            for token_id in ids:
                node = node.children.setdefault(token_id, TrieNode())
            node.name = name

    @property
    def name(self) -> str:
        return self._cursor.name

    def reset(self) -> None:
        self._cursor = self._root

    def allowed(self) -> set[int]:
        return set(self._cursor.children)

    def advance(self, token: int) -> None:
        if token not in self._cursor.children:
            raise CallMeMaybeError(f"{token} is not an available token.")
        self._cursor = self._cursor.children[token]
