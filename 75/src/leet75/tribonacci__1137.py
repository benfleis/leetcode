#!/usr/bin/env python3

__doc__ = """
1137. N-th Tribonacci Number
Easy
Topics
Companies
Hint
The Tribonacci sequence Tn is defined as follows: 

T0 = 0, T1 = 1, T2 = 1, and Tn+3 = Tn + Tn+1 + Tn+2 for n >= 0.

Given n, return the value of Tn.

 

Example 1:

Input: n = 4
Output: 4
Explanation:
T_3 = 0 + 1 + 1 = 2
T_4 = 1 + 1 + 2 = 4
Example 2:

Input: n = 25
Output: 1389537
 

Constraints:

0 <= n <= 37
The answer is guaranteed to fit within a 32-bit integer, ie. answer <= 2^31 - 1.
"""


class Solution:
    def tribonacci(self, n: int) -> int:
        return tribonacci(n)


def tribonacci(n: int) -> int:
    if n in [0, 1]:
        return n

    # simple sliding window of 3
    n0, n1, n2 = 0, 1, 1
    for _ in range(n - 2):
        next = n0 + n1 + n2
        n0 = n1
        n1 = n2
        n2 = next

    return n2


tests = [
    (0, 0),
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 4),
    (25, 1389537),
]


def test_tribonacci():
    for n, exp in tests:
        act = tribonacci(n)
        assert act == exp, f"tribonacci({n}) -> {act} != {exp}"
