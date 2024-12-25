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

from itertools import chain, takewhile
import copy
import typing

from hypothesis import example, given, note, settings, strategies as st


def _c2i(char: str) -> int:
    return ord(char) - ord("a")


def _common_prefix_len(s0: str, s1: str, s0_start: int = 0, s1_start: int = 0) -> int:
    i = 0
    for _ in takewhile(lambda x: x[0] == x[1], zip(s0[s0_start:], s1[s1_start:])):
        i += 1
    return i


class TrieNode:
    def __init__(
        self,
        prefix: str = "",
        is_leaf: bool = False,
        suffixes: None | list[None | typing.Self] = None,
    ):
        assert len(prefix) in [0, 1]  # root allows 0
        self.prefix: str = prefix
        self.is_leaf: bool = is_leaf
        self._suffixes: list[None | typing.Self] = suffixes or [None] * 26

    def insert(self, word: str) -> None:
        cur = self
        for char in word:
            assert cur
            idx = _c2i(char)
            if cur._suffixes[idx] is None:
                cur._suffixes[idx] = TrieNode(char)
            cur = cur._suffixes[idx]
        cur.is_leaf = True

    _LOC_NONE = "none"
    _LOC_PREFIX = "prefix"
    _LOC_EXACT = "exact"

    def _locate(self, word: str) -> str:
        cur = self
        for char in word:
            next = cur._suffixes[_c2i(char)]
            if next is None:
                return TrieNode._LOC_NONE
            cur = next
        return TrieNode._LOC_EXACT if cur.is_leaf else TrieNode._LOC_PREFIX

    def search(self, word: str) -> bool:
        return self._locate(word) == TrieNode._LOC_EXACT

    def startsWith(self, prefix: str) -> bool:
        return self._locate(prefix) in [
            TrieNode._LOC_EXACT,
            TrieNode._LOC_PREFIX,
        ]


class RadixTrieNode:
    def __init__(
        self,
        prefix: str = "",
        is_leaf: bool = False,
        suffixes: None | list[None | typing.Self] = None,
    ):
        self.prefix: str = prefix
        self.is_leaf: bool = is_leaf
        self._suffixes: list[None | typing.Self] = suffixes or [None] * 26

    def __repr__(self):
        suffixes = ",".join(map(lambda x: x.prefix, filter(None, self._suffixes)))
        return f'RadixNode{{p="{self.prefix}" l={self.is_leaf} s=[{suffixes}]}}'

    __str__ = __repr__

    def _get_suffix(self, prefix: str) -> None | typing.Self:
        assert prefix
        return self._suffixes[_c2i(prefix[0])]

    def _set_suffix(self, item: typing.Self) -> None:
        assert item.prefix
        i = _c2i(item.prefix[0])
        self._suffixes[i] = item

    # returned match node is last_node which contains deepest (partial) match node,
    # number of consumed chars prior to that node, and number of matched characters in that node.
    # Example: _match(trie="a"->"b"->"cd", "abc") -> (@"cd", 2, 1)
    # - @"cd" points to deepest match node
    # - 2 = len("a") + len("b") = length of prefixes prior to match node
    # - 1 = common prefix in remainder: "cd" and "c"
    #
    # More Examples (assume "b" and "cd" are marked LEAF nodes, thus "ab" and "abcd" present):
    # - _match(trie="a"->"b"->"cd", "ab") -> (@"b", 1, 1)
    # - _match(trie="a"->"b"->"cd", "abcd") -> (@"cd", 2, 2)
    # - _match(trie="a"->"b"->"cd", "abcde") -> (@"cd", 2, 2)
    #
    # From this info caller can determine none/exact/partial matches with arithmetic,
    # which is why this is internal only. Final semantic interpretation done in parent caller,
    # e.g. search and startsWith.
    def _match(self, prefix: str) -> tuple[typing.Self, int, int]:
        path_len = common_len = 0
        cur = self
        while path_len + common_len < len(prefix):
            next = cur._get_suffix(prefix[path_len + common_len])
            if next is None:
                break

            # march on - returns next (or deeper)
            assert len(cur.prefix) == common_len
            path_len += common_len
            cur = next

            # finish here or deeper?
            common_len = _common_prefix_len(prefix[path_len:], next.prefix)
            if common_len < len(next.prefix):
                break

        return (cur, path_len, common_len)

    def insert(self: typing.Self, word: str) -> None:
        (match, path_len, common_len) = self._match(word)
        # simplify comparisons below and avoid confusion; use word_suffix_len instead of word_len
        word_suffix_len = len(word) - path_len
        word_suffix_common = word[path_len + common_len :]

        match_prefix_len = len(match.prefix)
        if common_len == match_prefix_len == word_suffix_len:
            match.is_leaf = True
        elif common_len == match_prefix_len < word_suffix_len:
            match._set_suffix(RadixTrieNode(word_suffix_common, is_leaf=True))
        else:
            # merge/rotate, either node.prefix.startswith(word) or common prefix, diff tails
            # approach: create suffixes, update existing node to point to them
            # TODO: split to _merge
            assert common_len != match_prefix_len
            # split at `common_len` between match & match_child
            match_child = copy.copy(match)
            match_child.prefix = match.prefix[common_len:]
            match.prefix = match.prefix[:common_len]
            match.is_leaf = False  # reset, can be set below
            match._suffixes = [None for _ in match._suffixes]
            match._set_suffix(match_child)
            if common_len == word_suffix_len:
                match.is_leaf = True  # full word match at split; just flag leaf
            else:
                match._set_suffix(RadixTrieNode(word_suffix_common, is_leaf=True))

    def search(self, word: str) -> bool:
        (node, path_common, node_common) = self._match(word)
        return (
            node.is_leaf
            and node_common == len(node.prefix)
            and path_common + node_common == len(word)
        )

    def startsWith(self, prefix: str) -> bool:
        (_, path_common, node_common) = self._match(prefix)
        return len(prefix) == path_common + node_common


Trie = RadixTrieNode
Node = Trie


def _pr(node: RadixTrieNode, depth: int = 0):
    prefix = ("    " * (depth - 1)) + "  + " if depth > 0 else ""
    print(prefix, end="")
    print(f"'{node.prefix}'")
    for child in filter(None, node._suffixes or []):
        _pr(child, depth + 1)


class _n(RadixTrieNode):
    def __init__(
        self, prefix: str, is_leaf: bool = False, suffixes: None | list[str] = None
    ):
        super().__init__(prefix, is_leaf=is_leaf)
        for suffix in suffixes or []:
            if isinstance(suffix, str):
                suffix_is_leaf = suffix[0].isupper()
                suffix = RadixTrieNode(suffix.lower(), is_leaf=suffix_is_leaf)
            self._set_suffix(suffix)


_appled_sub = _n("app", False, ["ed", "le"])
_appled_trie = _n("", False, [_appled_sub])
_one_apple = _n("", False, [_n("apple", True)])

match_tests = [
    (_one_apple, "app", (["a"], 0, 3)),
    (_appled_trie, "a", (["a"], 0, 1)),
    (_appled_trie, "ap", (["a"], 0, 2)),
    (_appled_trie, "app", (["a"], 0, 3)),
    (_appled_trie, "appe", (["a", "e"], 3, 1)),
    (_appled_trie, "apped", (["a", "e"], 3, 2)),
    (_appled_trie, "appl", (["a", "l"], 3, 1)),
    (_appled_trie, "apple", (["a", "l"], 3, 2)),
    (_appled_trie, "applez", (["a", "l"], 3, 2)),
    (_appled_trie, "b", ([], 0, 0)),
]


def test_this():
    t = Trie()
    t.insert("apple")
    t.insert("app")
    res = t.search("app")
    assert res


def test_match():
    for trie, prefix, (path, pre_len, node_len) in match_tests:
        act = trie._match(prefix)
        exp_node = trie
        for edge in path:
            assert exp_node
            exp_node = exp_node._get_suffix(edge)
        exp = (exp_node, pre_len, node_len)
        assert act == exp, f"trie._match({prefix}) -> {act} != {exp}"


tests = [
    [
        ("T", [], None),
        ("I", ["apple"], None),
        ("s", ["apple"], True),
        ("s", ["app"], False),
        ("p", ["app"], True),
    ],
    [
        ("T", [], None),
        ("I", ["apple"], None),
        ("s", ["apple"], True),
        ("p", ["app"], True),
        ("I", ["apped"], None),
        ("s", ["apple"], True),
        ("s", ["apped"], True),
        ("p", ["app"], True),
        ("I", ["app"], None),
        ("s", ["apple"], True),
        ("s", ["apped"], True),
        ("p", ["app"], True),
    ],
    [
        ("T", [], None),
        ("I", ["apple"], None),
        ("s", ["apple"], True),
        ("s", ["app"], False),
        ("p", ["app"], True),
        ("I", ["app"], None),
        ("s", ["app"], True),
        ("s", ["apple"], True),
        ("I", ["apped"], None),
        ("p", ["a"], True),
        ("p", ["ap"], True),
        ("p", ["app"], True),
        ("p", ["appl"], True),
        ("p", ["apple"], True),
        ("p", ["applez"], False),
        ("p", ["appe"], True),
        ("p", ["apped"], True),
        ("p", ["appedz"], False),
        ("p", ["b"], False),
        ("s", ["a"], False),
        ("s", ["ap"], False),
        ("s", ["app"], True),
        ("s", ["appl"], False),
        ("s", ["apple"], True),
    ],
    # failed test case
    [
        ("T", [], None),
        ("I", ["p"], None),
        ("p", ["pr"], False),
        ("s", ["p"], True),
        ("I", ["pr"], None),
        ("p", ["pre"], False),
        ("s", ["pr"], True),
        ("I", ["pre"], None),
        ("p", ["pre"], True),
        ("s", ["pre"], True),
        ("I", ["pref"], None),
        ("p", ["pref"], True),
        ("s", ["pref"], True),
        ("I", ["prefi"], None),
        ("p", ["pref"], True),
        ("s", ["prefi"], True),
        ("I", ["prefix"], None),
        ("p", ["prefi"], True),
        ("s", ["prefix"], True),
    ],
    # failed test case
    [
        ("Trie", [], None),
        ("insert", ["app"], None),
        ("insert", ["apple"], None),
        ("insert", ["beer"], None),
        ("insert", ["add"], None),
        ("insert", ["jam"], None),
        ("insert", ["rental"], None),
        ("search", ["apps"], False),
        ("search", ["app"], True),
        ("search", ["ad"], False),
        ("search", ["applepie"], False),
        ("search", ["rest"], False),
        ("search", ["jan"], False),
        ("search", ["rent"], False),
        ("search", ["beer"], True),
        ("search", ["jam"], True),
        ("startsWith", ["apps"], False),
        ("startsWith", ["app"], True),
        ("startsWith", ["ad"], True),
        ("startsWith", ["applepie"], False),
        ("startsWith", ["rest"], False),
        ("startsWith", ["jan"], False),
        ("startsWith", ["rent"], True),
        ("startsWith", ["beer"], True),
        ("startsWith", ["jam"], True),
    ],
]


def test_trie():
    for i, test in enumerate(tests):
        trie = None
        for j, (op, args, exp) in enumerate(test):
            print(repr(trie))
            print(f"[{i}:{j:2d}] op={op} args={args}")
            if op in ["T", "Trie"]:
                trie = Trie()
                act = None
            elif op in ["I", "insert"]:
                assert trie
                act = trie.insert(*args)
            elif op in ["s", "search"]:
                assert trie
                act = trie.search(*args)
            elif op in ["p", "startsWith"]:
                assert trie
                act = trie.startsWith(*args)
            else:
                assert False, "ERROR test: invalid op"
            assert act == exp, f"{op}({', '.join(args)}) -> {act} != {exp}"
        print()
    print("test_trie: OK")


def mutate_word(word: str, op: int, pos: int, arg: int) -> str:
    op = op % 3
    pos = pos % len(word)
    char = chr(arg % 26 + ord("a"))

    if op == 0:  # INSERT CHAR
        return word[:pos] + char + word[pos:]
    elif op == 1:  # DELETE CHAR
        return word[:pos] + (word[pos + 1 :] if pos + 1 < len(word) else "")
    else:  # if op == 2:  # REPLACE CHAR
        return word[:pos] + char + (word[pos + 1 :] if pos + 1 < len(word) else "")


@settings(max_examples=1000)
@given(
    st.lists(
        st.text(
            st.characters(min_codepoint=ord("a"), max_codepoint=ord("z")),
            min_size=1,
            max_size=2000,
        ),
        min_size=1,
        max_size=2000,
    ),
    st.lists(
        st.tuples(
            st.integers(),
            st.integers(),
            st.integers(),
        ),
    ),
)
@example(["pa", "paa", "p"], [])
def test_trie_qt(words: list[str], mutations: list[tuple[int, int, int]]):
    # insert strings in order, generate all known exact and prefix match tests, and
    # accompanying mutation (non match) tests

    NONE = 0
    PREFIX = 1
    EXACT = 2

    # map str -> {PREFIX, EXACT, NONE} for all -- both known words & generated tests
    exacts: set[str] = set()
    prefixes: set[str] = set()
    nones: set[str] = set()

    trie = Trie()
    assert not trie.is_leaf

    # generate all matches
    for word in words:
        trie.insert(word)
        exacts.add(word)

        # add all valid prefixes/prefix tests
        for prefix in (word[:i] for i in range(1, len(word))):
            prefixes.add(prefix)
            for mutation in mutations:
                nones.add(mutate_word(prefix, *mutation))

    print({"nones": sorted(nones)})
    note({"nones": sorted(nones)})

    # keep all non-empty strings that aren't already found in a higher match level
    # this is cleaner than doing inline filtering during gen above
    tests = filter(
        lambda pair: pair[0] and pair,
        chain(
            ((w, EXACT) for w in exacts),
            ((w, PREFIX) for w in prefixes if w not in exacts),
            ((w, NONE) for w in nones if w not in exacts and w not in prefixes),
        ),
    )

    for prefix, match in tests:
        # prefix test
        exp = match in [PREFIX, EXACT]
        act = trie.startsWith(prefix)
        assert act == exp, prefix
        # exact test
        exp = match == EXACT
        act = trie.search(prefix)
        assert act == exp, prefix
