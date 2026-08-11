from src.trie import Trie
from src.errors import CallMeMaybeError

t = Trie({"fn_greet": [8822, 1889, 3744],
          "fn_add_numbers": [8822, 2891, 32964]})
assert t.allowed() == {8822}
t.advance(8822)
assert t.allowed() == {1889, 2891}
t.advance(1889)
assert t.allowed() == {3744}
t.advance(3744)
assert t.allowed() == set()
assert t.name == "fn_greet"

print("=== All trie tests passed===")

try:
    t.advance(9999)
    print("ERROR - advance accepted an illegal token")
except CallMeMaybeError as e:
    print(e)
