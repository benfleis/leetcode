#!/usr/bin/env python

__doc__ = """
# 1004. Max Consecutive Ones III

Medium Topics Companies Hint

Given a binary array nums and an integer k, return the maximum number of consecutive 1's in the array if you can flip at most k 0's.

## Example 1:

Input: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
Output: 6
Explanation: [1,1,1,0,0,1,1,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.

## Example 2:

Input: nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
Output: 10
Explanation: [0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.

## Constraints:

1 <= nums.length <= 105
nums[i] is either 0 or 1.
0 <= k <= nums.length

"""


class Solution:
    def longestOnes(self, nums: list[int], k: int) -> int:
        return most_consecutive_ones(nums, k)


def most_consecutive_ones(nums: list[int], k: int) -> int:
    if len(nums) < 1:
        return 0
    if len(nums) <= k:
        return k

    best = 0
    i = j = 0
    end = len(nums)

    # occupy all ks for initial condition
    while j < end and k > 0:
        if nums[j] == 0:
            if k == 0:
                break
            k -= 1
        best += 1
        j += 1

    # now alternate expanding (j) and contracting to keep bests
    cur = best

    # def p(op=None):
    #     if op:
    #         print(f".. {op}")
    #     print(f"SNAP: best={best:2d} i={i:2d} j={j:2d} cur={cur:2d}={nums[i:j]}")

    while j < end:
        # add tail 1s to cur/?best
        while nums[j] == 1:
            cur += 1
            j += 1
            best = max(best, cur)
            if j == end:
                break
        else:
            # drop head 1s; need to drop a 0 to get back a k
            while i < j and nums[i] == 1:
                i += 1
                cur -= 1
            # assert nums[i] == 0 and nums[j] == 0
            i += 1
            j += 1

    # print(f"FINAL: best={best}\n")
    return best


tests = [
    ([], 1, 0),
    ([0], 0, 0),
    ([1], 0, 1),
    ([0], 1, 1),
    ([1], 1, 1),
    ([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2, 6),
    ([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1], 3, 9),
    ([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1], 3, 10),
    ([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0], 3, 10),
    ([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0], 3, 10),
    ([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0], 3, 10),
    ([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1], 3, 10),
    ([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1], 3, 10),
    ([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1], 3, 10),
    ([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3, 10),
]


def test_max_consecutive_ones():
    for seq, k, exp in tests:
        act = most_consecutive_ones(seq, k)
        assert act == exp, f"move_zeroes({seq}, {k}) -> {act} != {exp}"
    print(f"OK: {len(tests)} passed.")


test_max_consecutive_ones()
