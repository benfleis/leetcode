#!/usr/bin/env python3

__doc__ = """
# 394. Decode String

Medium Topics Companies

Given an encoded string, return its decoded string.

The encoding rule is: k[encoded_string], where the encoded_string inside the square brackets is being repeated exactly k times. Note that k is guaranteed to be a positive integer.

You may assume that the input string is always valid; there are no extra white spaces, square brackets are well-formed, etc. Furthermore, you may assume that the original data does not contain any digits and that digits are only for those repeat numbers, k. For example, there will not be input like 3a or 2[4].

The test cases are generated so that the length of the output will never exceed 105.

 
## Example 1:

Input: s = "3[a]2[bc]"
Output: "aaabcbc"

## Example 2:

Input: s = "3[a2[c]]"
Output: "accaccacc"

## Example 3:

Input: s = "2[abc]3[cd]ef"
Output: "abcabccdcdcdef"

## Constraints:

1 <= s.length <= 30
s consists of lowercase English letters, digits, and square brackets '[]'.
s is guaranteed to be a valid input.
All the integers in s are in the range [1, 300].
"""

from itertools import takewhile


class Solution:
    def decodeString(self, s: str) -> str:
        return "".join(decode_substring(s)[0])


def decode_substring(encoded: str, i: int = 0) -> tuple[list[str], int]:
    end = len(encoded)
    subs: list[str] = []
    while i < end:
        # print(f"encoded={encoded[:i]}_{encoded[i:]}")
        char = encoded[i]
        if char.isdigit():
            count_str = "".join(takewhile(str.isdigit, encoded[i:]))
            i += len(count_str)
            assert encoded[i] == "["
            sub, i = decode_substring(encoded, i + 1)
            subs.extend(sub * int(count_str))
        elif char.isalpha():
            sub = "".join(takewhile(str.isalpha, encoded[i:]))
            subs.append(sub)
            i += len(sub)
        elif char == "]":
            i += 1
            return (subs, i)
        else:
            assert False, "ERROR: invalid token"

    return (subs, end)


tests = [
    ("", ""),
    ("a", "a"),
    ("1[a]", "a"),
    ("a2[b]c", "abbc"),
    ("3[a]2[bc]", "aaabcbc"),
    ("3[a2[c]]", "accaccacc"),
    ("2[abc]3[cd]ef", "abcabccdcdcdef"),
]


def test():
    for encoded, exp in tests:
        act = "".join(decode_substring(encoded)[0])
        assert act == exp, f"decode_string({encoded}) -> {act} != {exp}"
