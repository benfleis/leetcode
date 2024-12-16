#!/usr/bin/env python

__doc__ = """
# 443. String Compression

Medium Topics Companies Hint

Given an array of characters chars, compress it using the following algorithm:

Begin with an empty string s. For each group of consecutive repeating characters in chars:

If the group's length is 1, append the character to s.
Otherwise, append the character followed by the group's length.
The compressed string s should not be returned separately, but instead, be stored in the input character array chars. Note that group lengths that are 10 or longer will be split into multiple characters in chars.

After you are done modifying the input array, return the new length of the array.

You must write an algorithm that uses only constant extra space.

----

## Example 1:

Input: chars = ["a","a","b","b","c","c","c"]
Output: Return 6, and the first 6 characters of the input array should be: ["a","2","b","2","c","3"]
Explanation: The groups are "aa", "bb", and "ccc". This compresses to "a2b2c3".

## Example 2:

Input: chars = ["a"]
Output: Return 1, and the first character of the input array should be: ["a"]
Explanation: The only group is "a", which remains uncompressed since it's a single character.

## Example 3:

Input: chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]
Output: Return 4, and the first 4 characters of the input array should be: ["a","b","1","2"].
Explanation: The groups are "a" and "bbbbbbbbbbbb". This compresses to "ab12".
 

## Constraints:

1 <= chars.length <= 2000
chars[i] is a lowercase English letter, uppercase English letter, digit, or symbol.
"""


class Solution:
    def compress(self, chars: list[str]) -> int:
        return compress_string_gen(chars)


def compress_string_gen(chars: list[str]) -> int:
    if len(chars) <= 1:
        return len(chars)

    def gen():
        cur = ""
        count = 0
        for char in chars:
            if cur == char:
                count += 1
            else:
                if cur:
                    yield cur
                    if count > 1:
                        yield str(count)
                cur = char
                count = 1
        yield cur
        if count > 1:
            yield str(count)

    for i, c in enumerate([c for chunk in gen() for c in chunk]):
        chars[i] = c
    else:
        return i + 1


def compress_string_inline(chars: list[str]) -> int:
    if len(chars) <= 1:
        return len(chars)

    write_pos = count = 0
    cur = ""

    for char in chars:
        if cur == char:
            count += 1
        else:
            if cur:
                compressed = cur + (str(count) if count > 1 else "")
                chars[write_pos : write_pos + len(compressed)] = compressed
                write_pos += len(compressed)
            cur = char
            count = 1
    else:
        compressed = cur + (str(count) if count > 1 else "")
        chars[write_pos : write_pos + len(compressed)] = compressed
        write_pos += len(compressed)

    return write_pos


tests = [
    ("", ""),
    ("a", "a"),
    ("b", "b"),
    ("aa", "a2"),
    ("aabcc", "a2bc2"),
    ("baaaaaaaaaaaaaaaaaaaaaa", "ba22"),
    ("aabbccc", "a2b2c3"),
    ("a", "a"),
    ("abbbbbbbbbbbb", "ab12"),
]


def test_compress_string_gen():
    for input, exp in tests:
        input_arr = list(input)
        act_count = compress_string_gen(input_arr)
        act = "".join(input_arr[:act_count])

        assert act == exp, f"compress_string_gen({input}) ~> {act} != {exp}"
        assert act_count == len(
            exp
        ), f"compress_string_gen({input}) -> {act_count} != {len(exp)}"
    print("test_compress_string_gen: OK")


def test_compress_string_inline():
    for input, exp in tests:
        input_arr = list(input)
        act_count = compress_string_inline(input_arr)
        act = "".join(input_arr[:act_count])

        assert act == exp, f"compress_string_inline({input}) ~> {act} != {exp}"
        assert act_count == len(
            exp
        ), f"compress_string_inline({input}) -> {act_count} != {len(exp)}"
    print("test_compress_string_inline: OK")


test_compress_string_gen()
test_compress_string_inline()
