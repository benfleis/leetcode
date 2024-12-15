#!/usr/bin/env python

"""
# 345. Reverse Vowels of a String

Easy Topics Companies

Given a string s, reverse only all the vowels in the string and return it.

The vowels are 'a', 'e', 'i', 'o', and 'u', and they can appear in both lower and upper cases, more than once.



## Example 1:

Input: s = "IceCreAm"
Output: "AceCreIm"

Explanation:

The vowels in s are ['I', 'e', 'e', 'A']. On reversing the vowels, s becomes "AceCreIm".

## Example 2:

Input: s = "leetcode"
Output: "leotcede"



## Constraints:

1 <= s.length <= 3 * 105
s consist of printable ASCII characters.
"""


class Solution:
    def reverseVowels(self, s: str) -> str:
        return reverse_vowels_array(s)


vowels = "aeiouAEIOU"  # set("aeiouAEIOU")


def reverse_vowels_array(s: str) -> str:
    if len(s) <= 1:
        return s

    arr = list(s)
    i = 0
    j = len(s) - 1
    while i < j:
        if s[i] not in vowels:
            i += 1
        elif s[j] not in vowels:
            j -= 1
        else:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1

    return "".join(arr)


def reverse_vowels_iterative(s: str) -> str:
    if len(s) <= 1:
        return s

    swaps = []
    i = 0
    j = len(s) - 1
    while i < j:
        if s[i] not in vowels:
            i += 1
        elif s[j] not in vowels:
            j -= 1
        else:
            swaps.append((i, j))
            i += 1
            j -= 1

    def gen_swapped():
        cur = 0
        for pos0, pos1 in swaps:
            yield s[cur:pos0]
            yield s[pos1]
            cur = pos0 + 1
        for pos1, pos0 in reversed(swaps):
            yield s[cur:pos0]
            yield s[pos1]
            cur = pos0 + 1
        yield s[cur:]
        return

    return "".join(gen_swapped())


tests = [
    ("", ""),
    ("a", "a"),
    ("b", "b"),
    ("eba", "abe"),
    ("IceCreAm", "AceCreIm"),
    ("leetcode", "leotcede"),
]


def test_reverse_vowels_array():
    for input, exp in tests:
        act = reverse_vowels_array(input)
        assert act == exp, f"reverse_vowels_array({input}) -> {act} != {exp}"
    print("test_reverse_vowels_array: OK")


def test_reverse_vowels_iterative():
    for input, exp in tests:
        act = reverse_vowels_iterative(input)
        assert act == exp, f"reverse_vowels_iterative({input}) -> {act} != {exp}"
    print("test_reverse_vowels_iterative: OK")


test_reverse_vowels_array()
test_reverse_vowels_iterative()
