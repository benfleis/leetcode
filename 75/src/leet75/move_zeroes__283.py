#!/usr/bin/env python

__doc__ = """
# 283. Move Zeroes

Easy Topics Companies Hint

Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.
Note that you must do this in-place without making a copy of the array.

## Example 1:

Input: nums = [0,1,0,3,12]
Output: [1,3,12,0,0]

## Example 2:

Input: nums = [0]
Output: [0]

## Constraints:

1 <= nums.length <= 104
-231 <= nums[i] <= 231 - 1

## Follow up
Could you minimize the total number of operations done?
"""


class Solution:
    def moveZeroes(self, nums: list[int]) -> None:
        return move_zeroes_gen(nums)


def move_zeroes_gen(nums: list[int]) -> None:
    if len(nums) <= 1:
        return

    i = 0
    for i, n in enumerate(filter(None, nums)):
        nums[i] = n
    else:
        for i in range(i + 1, len(nums)):
            nums[i] = 0


tests = [
    ([], []),
    ([0], [0]),
    ([1], [1]),
    ([0, 1], [1, 0]),
    ([1, 0], [1, 0]),
    ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
]


def test_move_zeroes():
    for input, exp in tests:
        act = input[:]
        move_zeroes_gen(act)
        assert act == exp, f"move_zeroes({input}) -> {act} != {exp}"
    print("test_move_zeroes: OK")


test_move_zeroes()
