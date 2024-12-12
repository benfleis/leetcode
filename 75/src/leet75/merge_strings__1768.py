#!/usr/bin/env python3

"""
# 1768. Merge Strings Alternately
Tags: Easy Topics Companies Hint

You are given two strings word1 and word2. Merge the strings by adding letters in alternating order, starting with word1. If a string is longer than the other, append the additional letters onto the end of the merged string.

Return the merged string.

 

### Example 1:

Input: word1 = "abc", word2 = "pqr"
Output: "apbqcr"
Explanation: The merged string will be merged as so:
word1:  a   b   c
word2:    p   q   r
merged: a p b q c r

### Example 2:

Input: word1 = "ab", word2 = "pqrs"
Output: "apbqrs"
Explanation: Notice that as word2 is longer, "rs" is appended to the end.
word1:  a   b 
word2:    p   q   r   s
merged: a p b q   r   s

### Example 3:

Input: word1 = "abcd", word2 = "pq"
Output: "apbqcd"
Explanation: Notice that as word1 is longer, "cd" is appended to the end.
word1:  a   b   c   d
word2:    p   q 
merged: a p b q c   d
 

### Constraints:

1 <= word1.length, word2.length <= 100
word1 and word2 consist of lowercase English letters.
"""

# %%
from itertools import zip_longest


def merge_strings_per_char(a, b):
    return "".join([(x + y if x and y else x or y) for (x, y) in zip_longest(a, b)])


tests = [
    ("", "", ""),
    ("asdf", "", "asdf"),
    ("", "qqq", "qqq"),
    ("a", "b", "ab"),
    ("aa", "b", "aba"),
    ("a", "bb", "abb"),
    ("aa", "bb", "abab"),
    ("abc", "pqr", "apbqcr"),
    ("ab", "pqrs", "apbqrs"),
    ("abcd", "pq", "apbqcd"),
]


def test():
    for w1, w2, exp in tests:
        act = merge_strings_per_char(w1, w2)
        assert act == exp
