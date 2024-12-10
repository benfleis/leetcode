#!/usr/bin/env python3

class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        return gcd_of_strings(str1, str2)


def gcd(a, b):
    if a == 0 and b == 0:
        return 0
    if a > b: # from now on a <= b
        a, b = b, a
    while a and b:
        a, b = b % a, a
    return b


def gcd_of_strings(s1, s2):
    if not s1 or not s2:
        return ''

    s1_len = len(s1)
    s2_len = len(s2)
    if s1_len > s2_len:
        s1, s2 = s2, s1

    # much faster with math.gcd :)
    gos_len = gcd(s1_len, s2_len)
    gos = s1[:gos_len]

    def grouper(s: str, n: int):
        return zip(*[iter(s)] * n, strict=True)

    #import pdb; pdb.set_trace()
    return gos if (
        gos_len > 0 and
        all(map(lambda s: ''.join(s) == gos, grouper(s1, gos_len))) and
        all(map(lambda s: ''.join(s) == gos, grouper(s2, gos_len)))
    ) else ''


gcd_tests = [
    (0, 0, 0),
    (1, 2, 1),
    (0, 3, 3),
    (3, 3, 3),
    (3, 6, 3),
    (25, 36, 1),
    (75, 35, 5),
    (75, 25595, 5),
]

def test_gcd():
    for (a, b, exp) in gcd_tests:
        act = gcd(a, b)
        assert act == exp
        act_swap = gcd(b, a)
        assert act_swap == exp

str_tests = [
    ('', '', ''),
    ('a', 'a', 'a'),
    ('a', 'b', ''),
    ('a', '', ''),
    ('', 'b', ''),
    ("LEET", "CODE", ""),
    ("ABCABC", "ABC", "ABC"),
    ("ABABAB", "ABAB", "AB"),
]

def test_str():
    for (s1, s2, exp) in str_tests:
        act = gcd_of_strings(s1, s2)
        assert act == exp
