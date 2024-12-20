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


# simple trie -- fixed size branch blocks, no tunneling

import typing


def _c2i(char: str) -> int:
    return ord(char) - ord("a")


class Node:
    def __init__(
        self,
        prefix: str = "",
        suffixes: None | list[None | typing.Self] = None,
        is_leaf: bool = False,
    ):
        assert len(prefix) in [0, 1]  # root allows 0
        self.prefix: str = prefix
        self.suffixes: list[None | typing.Self] = suffixes or [None] * 26
        self.is_leaf: bool = is_leaf

    def insert(self, word: str) -> None:
        if word == "apped":
            breakpoint()
        cur = self
        for char in word:
            assert cur
            idx = _c2i(char)
            if cur.suffixes[idx] is None:
                cur.suffixes[idx] = Node(char)
            cur = cur.suffixes[idx]
        cur.is_leaf = True

    _MATCH_NONE = "none"
    _MATCH_PREFIX = "prefix"
    _MATCH_EXACT = "exact"

    def _match(self, word: str) -> str:
        cur = self
        for char in word:
            next = cur.suffixes[_c2i(char)]
            if next is None:
                return Node._MATCH_NONE
            cur = next
        return Node._MATCH_EXACT if cur.is_leaf else Node._MATCH_PREFIX

    def search(self, word: str) -> bool:
        return self._match(word) == Node._MATCH_EXACT

    def startsWith(self, prefix: str) -> bool:
        return self._match(prefix) in [Node._MATCH_EXACT, Node._MATCH_PREFIX]


Trie = Node


def _pr(node: Node, depth: int = 0):
    prefix = ("    " * (depth - 1)) + "  + " if depth > 0 else ""
    print(prefix, end="")
    print(f"'{node.prefix}'")
    for child in filter(None, node.suffixes or []):
        _pr(child, depth + 1)


tests = [
    [
        ("Trie", [], None),
        ("insert", ["apple"], None),
        ("search", ["apple"], True),
        ("startsWith", ["app"], True),
        ("insert", ["apped"], None),
        ("search", ["apple"], True),
        ("search", ["apped"], True),
        ("startsWith", ["app"], True),
        ("insert", ["app"], None),
        ("search", ["apple"], True),
        ("search", ["apped"], True),
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
    for i, test in enumerate(tests):
        trie = None
        for j, (op, args, exp) in enumerate(test):
            print(f"[{i}:{j:2d}] op={op} args={args}")
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
                act = trie.startsWith(*args)
            else:
                assert False, "ERROR test: invalid op"
            assert act == exp, f"{op}({', '.join(args)}) -> {act} != {exp}"
        print()
    print("test_trie: OK")


if __name__ == "__main__":
    test_trie()
