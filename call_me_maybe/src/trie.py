"""Token-level prefix tree for constraining function-name generation.

The model emits function names one token at a time, never as a single
choice. This module stores every allowed name as a path through a tree
keyed by tokens ID, so that at each generation step the set of tokens
that could still complete a valid name can be read directly off the
current node.
"""

from dataclasses import dataclass, field

from .errors import CallMeMaybeError


@dataclass
class TrieNode:
    """A single position in the tree.

    Attributes:
        name: The complete function name ending at this node, or None if
            this node is only a waypoint along a longer name.
        children: Token IDs that may follow, mapped to the nodes they
            lead to.
    """
    name: str | None = None
    children: dict[int, "TrieNode"] = field(default_factory=dict)


class Trie:
    """A traversable prefix tree over tokenized function names.

    The tree is built once and then walked repeatedly, A cursor tracks the
    current position, so callers must call reset() before each traversal.
    """
    def __init__(self, names: dict[str, list[int]]) -> None:
        """Build the tree from tokenized names.

        Args:
            names: Function names mapped to their token ID sequences.
        """
        self._root = TrieNode()
        self._cursor = self._root

        for name, ids in names.items():
            node = self._root
            for token_id in ids:
                # setdefault reuses the branch when names share a prefix
                # all five examole names begin with the token for "fn"
                node = node.children.setdefault(token_id, TrieNode())
            # Only the final node carried the name, marking it as complete
            node.name = name

    @property
    def name(self) -> str:
        """The complete function name at the current position.

        Returns:
            The name ending at the cursor.

        Raises:
            CallMeMaybeError: If the cursor has not reached a complete name.
                This indicates a bug in the caller, not invalid input.
        """
        if self._cursor.name is None:
            raise CallMeMaybeError(
                    "internal error: name requested before reaching a "
                    "complete function name."
                    )
        return self._cursor.name

    def reset(self) -> None:
        """Return the cursor tp the root, ready for a new traversal."""
        self._cursor = self._root

    def allowed(self) -> set[int]:
        """Token IDs that may legally follow the current position.

        Returns:
            The permitted token IDs. Empty when no name can continue from
            here, which is signals that generation is finished.
        """
        return set(self._cursor.children)

    def advance(self, token: int) -> None:
        """Move the cursor along the branch for the given token.

        Args:
            token: A token ID, which must come from allowed().

        Raises:
            CallMeMaybeError: If the token is not a valid continuation.
                Since the callers select only from allowed(), this indicates
                a bug in the masking logic rather than bad input.
        """
        if token not in self._cursor.children:
            raise CallMeMaybeError(
                    f"internal error: token {token} is not valid continuation"
                    f" (allowed: {sorted(self._cursor.children)})"
                    )
        self._cursor = self._cursor.children[token]
