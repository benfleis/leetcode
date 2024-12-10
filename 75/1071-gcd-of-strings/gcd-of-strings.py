#!/usr/bin/env python3

import math

class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        return gcd_of_strings(str1, str2)

def gcd_of_strings(s1, s2):
    if not s1 or not s2:
        return ''

    s1_len = len(s1)
    s2_len = len(s2)
    if s1_len > s2_len:
        s1, s2 = s2, s1

    gcd = math.gcd(s1_len, s2_len)
    sub = s1[:gcd]

    def grouper(s: str, n: int):
        return zip(*[iter(s)] * n, strict=True)

    #import pdb; pdb.set_trace()
    return sub if (
        gcd > 0 and
        all(map(lambda s: ''.join(s) == sub, grouper(s1, gcd))) and
        all(map(lambda s: ''.join(s) == sub, grouper(s2, gcd)))
    ) else ''


tests = [
    ('', '', ''),
    ('a', 'a', 'a'),
    ('a', 'b', ''),
    ('a', '', ''),
    ('', 'b', ''),
    ("LEET", "CODE", ""),
    ("ABCABC", "ABC", "ABC"),
    ("ABABAB", "ABAB", "AB"),
]

def test():
    for (s1, s2, exp) in tests:
        act = gcd_of_strings(s1, s2)
        assert act == exp
