#!/usr/bin/env python

__doc__ = """ 
# 334. Increasing Triplet Subsequence

Medium Topics Companies

Given an integer array nums, return true if there exists a triple of indices (i, j, k) such that i < j < k and nums[i] < nums[j] < nums[k]. If no such indices exists, return false.

## Example 1:

Input: nums = [1,2,3,4,5]
Output: true
Explanation: Any triplet where i < j < k is valid.

## Example 2:

Input: nums = [5,4,3,2,1]
Output: false
Explanation: No triplet exists.

## Example 3:

Input: nums = [2,1,5,0,4,6]
Output: true
Explanation: The triplet (3, 4, 5) is valid because nums[3] == 0 < nums[4] == 4 < nums[5] == 6.

## Constraints:

1 <= nums.length <= 5 * 105
-231 <= nums[i] <= 231 - 1

## Follow up

Could you implement a solution that runs in O(n) time complexity and O(1) space complexity?
"""


class Solution:
    def increasingTriplet(self, nums: list[int]) -> bool:
        return find_increasing_triplet(nums)


def find_increasing_triplet(nums: list[int]) -> bool:
    # approach:
    # don't need to know the triplet, only whether it exists. for it to exist, there must be two increases (non consecutive)
    # we can run the range, keeping the lowest 2nd number (thus second number of first increasing pair), and improve/update
    # elements as we walk, while noting whether a 3rd in sequence in found.
    if len(nums) < 3:
        return False

    # def p(a, b, c):
    #     print(f"[{a},{b},{c}]")

    a, b = None, None
    # p(a, b, c)
    for x in nums:
        if (a is None) or (x <= a):
            a = x
            # p(a, b, c)

        elif (b is None) or (b is not None and a < x <= b):
            b = x
            # p(a, b, c)
        elif b < x:
            # p(a, b, x)
            # print()
            return True  # c = x

    # print()
    return False


tests = [
    ([20, 100, 10, 12, 5, 13], True),
    ([], False),
    ([1], False),
    ([1, 2], False),
    ([1, 2, 3], True),
    ([1, 1, 1], False),
    ([1, 2, 2], False),
    ([1, 1, 2], False),
    ([3, 1, 4, 1], False),
    ([3, 1, 4, 1, 2], False),  # tests intermediate value bug: [1, 1, 2]
    ([3, 1, 4, 1, 5], True),
    ([1, 2, 3, 4, 5], True),
    ([5, 4, 3, 2, 1], False),
    ([2, 1, 5, 0, 4, 6], True),
]


def test_find_increasing_triplet():
    for input, exp in tests:
        act = find_increasing_triplet(input)
        assert act == exp, f"find_increasing_triplet({input}) -> {act} != {exp}"
    print("test_find_increasing_triplet: OK")


test_find_increasing_triplet()
