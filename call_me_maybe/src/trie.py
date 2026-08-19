"""Token-level prefix tree for constraining function-name generation.

The model emits function names one token at a time, never as a single
choice. This module stores every allowed name as a path through a tree
keyed by tokens ID, so that at each generation step the set of tokens
that could still complete a valid name can be read directly off the
current node.
"""

from pydantic import BaseModel, Field

from .errors import CallMeMaybeError


class TrieNode(BaseModel):
    """A single position in the tree.

    Attributes:
        name: The complete function name ending at this node, or None if
            this node is only a waypoint along a longer name.
        children: Token IDs that may follow, mapped to the nodes they
            lead to.
    """
    name: str | None = None
    children: dict[int, "TrieNode"] = Field(default_factory=dict)


class Trie(BaseModel):
    """A traversable prefix tree over tokenized function names.

    The tree is built once and then walked repeatedly. A cursor tracks the
    current position, so callers must call reset() before each traversal.
    """
    root: TrieNode
    cursor: TrieNode

    @classmethod
    def from_names(cls, names: dict[str, list[int]]) -> "Trie":
        """Build the tree from tokenized names.

        Args:
            names: Function names mapped to their token ID sequences.
        Returns:
            A Trie positioned at the root.
        """
        root = TrieNode()
        for name, ids in names.items():
            node = root
            for token_id in ids:
                # setdefault reuses the branch when names share a prefix
                # all five example names begin with the token for "fn"
                node = node.children.setdefault(token_id, TrieNode())
            # Only the final node carries the name, marking it as complete
            node.name = name
        return cls(root=root, cursor=root)

    @property
    def name(self) -> str:
        """The complete function name at the current position.

        Returns:
            The name ending at the cursor.

        Raises:
            CallMeMaybeError: If the cursor has not reached a complete name.
                This indicates a bug in the caller, not invalid input.
        """
        if self.cursor.name is None:
            raise CallMeMaybeError(
                    "internal error: name requested before reaching a "
                    "complete function name."
                    )
        return self.cursor.name

    def reset(self) -> None:
        """Return the cursor to the root, ready for a new traversal."""
        self.cursor = self.root

    def allowed(self) -> set[int]:
        """Token IDs that may legally follow the current position.

        Returns:
            The permitted token IDs. Empty when no name can continue from
            here, which signals that generation is finished.
        """
        return set(self.cursor.children)

    def advance(self, token: int) -> None:
        """Move the cursor along the branch for the given token.

        Args:
            token: A token ID, which must come from allowed().

        Raises:
            CallMeMaybeError: If the token is not a valid continuation.
                Since callers select only from allowed(), this indicates
                a bug in the masking logic rather than bad input.
        """
        if token not in self.cursor.children:
            raise CallMeMaybeError(
                    f"internal error: token {token} is not valid continuation"
                    f" (allowed: {sorted(self.cursor.children)})"
                    )
        self.cursor = self.cursor.children[token]
