#!/usr/bin/env python3

# %%
from itertools import zip_longest

def merge_strings_per_char(a, b):
    return ''.join([(x + y if x and y else x or y) for (x, y) in zip_longest(a, b)])

tests = [
    ('', '', ''),
    ('asdf', '', 'asdf'),
    ('', 'qqq', 'qqq'),
    ('a', 'b', 'ab'),
    ('aa', 'b', 'aba'),
    ('a', 'bb', 'abb'),
    ('aa', 'bb', 'abab'),
    ('abc', 'pqr', 'apbqcr'),
    ("ab", "pqrs", "apbqrs"),
    ("abcd", "pq", "apbqcd"),
]

def test():
    for (w1, w2, exp) in tests:
        act = merge_strings_per_char(w1, w2)
        assert act == exp
