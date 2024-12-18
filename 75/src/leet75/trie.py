#!/usr/bin/env python3

__doc__ = """
208. Implement Trie (Prefix Tree)
Medium
Topics
Companies
A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker.

Implement the Trie class:

Trie() Initializes the trie object.
void insert(String word) Inserts the string word into the trie.
boolean search(String word) Returns true if the string word is in the trie (i.e., was inserted before), and false otherwise.
boolean startsWith(String prefix) Returns true if there is a previously inserted string word that has the prefix prefix, and false otherwise.
 

Example 1:

Input
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
Output
[null, null, true, false, true, null, true]

Explanation
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple");   // return True
trie.search("app");     // return False
trie.startsWith("app"); // return True
trie.insert("app");
trie.search("app");     // return True
 

Constraints:

1 <= word.length, prefix.length <= 2000
word and prefix consist only of lowercase English letters.
At most 3 * 104 calls in total will be made to insert, search, and startsWith.
"""


# Definition:
# Node is a list of children; each child is a tuple(prefix (of length N), next Node)
# Invariants:
# - For any Node, the number of children will not exceed 26 (alphabet)
# - For any Node, each child has a unique prefix
# - For any prefix Node, the children must all prefixes length N=[0,1]
# - For any prefix Node, the children are sorted by prefix
# - For any leaf Node, "prefix" length is unlimited, next Node is None
# NOTE: given the limited length of children, perform simple insertion sort for now, can move to binary search later
# NOTE: evt relax the condition prefix node prefix N=0,1 to allow for long common substrings

import bisect
from typing import Self


class _Node:
    def __init__(self, prefix: str = "", children=None):
        self.prefix: str = prefix
        self.children: list[Self] = children or []

    def __lt__(self, other) -> bool:  # for bisect
        return self.prefix < other.prefix

    def __eq__(self, other) -> bool:  # for testing
        return self.prefix == other.prefix and self.children == other.children

    def __repr__(self) -> str:
        return f"{{prefix={self.prefix} children={repr(self.children)}}}"

    def is_leaf(self) -> bool:
        return bool(self.children)


# split node[pos] and word on common prefix, replacing node[pos] with new branching node
def _split_on_prefix(parent: _Node, pos: int, word: str) -> None:
    # NOTE: this is where the magic happens for prefix N > 1
    # common prefix leaf node, split
    present = parent.children[pos]
    assert not present.children, "invalid assumption: current child is leaf node"
    assert present.prefix[0] == word[0], "invalid assumption: common prefix"

    # split prefixes
    prefix = word[0]
    present = _Node(present.prefix[1:])
    other = _Node(word[1:])
    split_children = (
        [present, other] if present.prefix < other.prefix else [other, present]
    )

    split_node = _Node(prefix, split_children)
    parent.children[pos] = split_node


def _insert(node: _Node, word: str) -> None:
    # TODO: is there a sneaky case word="" and children=[] here? cuz my recursive _insert may be in danger
    import pdb

    pdb.set_trace()

    if node.prefix == word:
        return

    word_node = _Node(word)
    if not node.children or not word:
        node.children.insert(0, word_node)
        return

    prefix = word[0]
    pos = bisect.bisect_left(node.children, word_node)

    lhs = node.children[pos - 1] if pos else None
    if lhs and prefix <= lhs.prefix[0]:
        # LHS is present and prefix match or proceding, meaning we'll never consider RHS and return
        if prefix < lhs.prefix[0]:
            node.children.insert(pos - 1, _Node(word))
        else:  # prefix == lhs.prefix[0]
            if lhs.is_leaf():
                if word != lhs.prefix:  # o/w dup
                    _split_on_prefix(node, pos - 1, word)
            else:  # non leaf + prefix branch
                _insert(lhs, word[1:])
        return

    rhs = node.children[pos] if pos < len(node.children) else None
    if not rhs or prefix < rhs.prefix[0]:  # no match to rhs, insert as-is
        node.children.insert(pos, word_node)
    elif rhs.prefix == prefix:  # prefix subtree exists
        _insert(rhs, word[1:])
    else:  # rhs.prefix[0] == prefix: # make prefix subtree
        _split_on_prefix(node, pos, word)


class Trie:
    def __init__(self) -> None:
        self.root = _Node()

    def insert(self, word: str) -> None:
        _insert(self.root, word)

    def search(self, word: str) -> bool:
        if not word:
            return True
        return False

    def starts_with(self, prefix: str) -> bool:
        if not prefix:
            return True
        return False


def _n(prefix, children=None):
    if not children:
        return _Node(prefix)
    assert not isinstance(children, _Node)
    if isinstance(children[0], str):
        return _Node(prefix, list(map(_Node, children)))
    assert isinstance(children[0], _Node)
    return _Node(prefix, list(children))


def _r(children=None):
    return _n("", children=children)


def _pr(node: _Node, depth: int = 0):
    import pdb

    # pdb.set_trace()
    prefix = ("    " * (depth - 1)) + "  + " if depth > 0 else ""
    print(prefix, end="")
    print(f"'{node.prefix}'")
    for child in node.children:
        _pr(child, depth + 1)


split_tests = [
    ((["ab"], 0, "az"), [_n("a", ["b", "z"])]),
    ((["az"], 0, "ab"), [_n("a", ["b", "z"])]),
    ((["az"], 0, "a"), [_n("a", ["", "z"])]),
    ((["azzz"], 0, "a"), [_n("a", ["", "zzz"])]),
    ((["a"], 0, "azzz"), [_n("a", ["", "zzz"])]),
]


def test_split():
    for (trie, pos, word), exp in split_tests:
        trie, exp = _r(trie), _r(exp)
        _split_on_prefix(trie, pos, word)
        assert trie == exp, "split no workie"
    print("test_split_on_prefix: OK")


insert_tests = [
    # (in_trie, word, out_trie); if in_trie == None, make new; == "->", use previous out_trie
    # (None, "ab", _r([_n("ab")])),
    (_r([_n("a")]), "a", _r([_n("a")])),
    (_r([_n("a")]), "ab", _r([_n("a", ["", "b"])])),
    (_r([_n("ab")]), "az", _r([_n("a", ["b", "z"])])),
    (_r([_n("az")]), "ab", _r([_n("a", ["b", "z"])])),
    (_r([_n("a")]), "ab", _r([_n("a", ["", "b"])])),
    (_r([_n("a")]), "ab", _r([_n("a", ["", "b"])])),
    # (None, "aab", ("aab", None)),
    # ("->", "aaz", ("a", [("a", [("b", None), ("z", None)])])),
]


def test_insert():
    trie = None  # bump scope
    for trie, word, exp in insert_tests:
        trie = trie or _r()
        _insert(trie, word)
        _pr(trie)
        assert trie == exp, f"_insert({trie}, {word}) -> {trie} != {exp}"
    print("test_insert: OK")


tests = [
    [
        ("Trie", [], None),
        ("insert", ["apple"], None),
        ("search", ["apple"], True),
        ("startsWith", ["app"], True),
        ("insert", ["apped"], False),
        ("search", ["apple"], True),
        ("search", ["appld"], True),
        ("startsWith", ["app"], True),
        ("insert", ["app"], False),
        ("search", ["apple"], True),
        ("search", ["appld"], True),
        ("startsWith", ["app"], True),
    ],
    [
        ("Trie", [], None),
        ("insert", ["apple"], None),
        ("search", ["apple"], True),
        ("search", ["app"], False),
        ("startsWith", ["app"], True),
    ],
    [
        ("Trie", [], None),
        ("insert", ["apple"], None),
        ("search", ["apple"], True),
        ("search", ["app"], False),
        ("startsWith", ["app"], True),
        ("insert", ["app"], None),
        ("search", ["app"], True),
        ("search", ["apple"], True),
        ("startsWith", ["a"], True),
        ("startsWith", ["ap"], True),
        ("startsWith", ["app"], True),
        ("startsWith", ["appl"], True),
        ("startsWith", ["apple"], True),
    ],
]


def test_trie():
    for test in tests:
        trie = None
        for op, args, exp in test:
            if op == "Trie":
                trie = Trie()
                act = None
            elif op == "insert":
                assert trie
                act = trie.insert(*args)
            elif op == "search":
                assert trie
                act = trie.search(*args)
            elif op == "startsWith":
                assert trie
                act = trie.starts_with(*args)
            else:
                assert False, "invalid op"
            assert act == exp, f"{op}({', '.join(args)}) -> {act} != {exp}"
    print("test_trie: OK")


if __name__ == "__main__":
    test_split()
    test_insert()
    # test_trie()
