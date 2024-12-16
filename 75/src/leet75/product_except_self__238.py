#!/usr/bin/env python

__doc__ = """
# 238. Product of Array Except Self
Medium Topics Companies Hint

Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.


## Example 1:

Input: nums = [1,2,3,4]
Output: [24,12,8,6]

## Example 2:

Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]


## Constraints:

2 <= nums.length <= 105
-30 <= nums[i] <= 30
The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
 

## Follow up
Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space for space complexity analysis.)
"""


class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        return product_except_self(nums)


def product_except_self(nums: list[int]) -> list[int]:
    acc_for = [1]
    product = 1
    for num in nums[:-1]:
        product = product * num
        acc_for.append(product)

    acc_rev = [1]
    product = 1
    for num in reversed(nums[1:]):
        product = product * num
        acc_rev.append(product)

    ### [2, 4, 6]
    # print(nums)
    ###
    ### [x, 2, 8]
    # print(acc_for)
    ### [24, 6, x]
    # print(acc_rev)
    ###
    ###
    ### [24, 12, 8]

    return [f * r for (f, r) in zip(acc_for, reversed(acc_rev))]


tests = [
    ([2, 4, 6], [24, 12, 8]),
    ([1, 2, 3, 4], [24, 12, 8, 6]),
    ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),
]


def test_product_except_self():
    for input, exp in tests:
        act = product_except_self(input)
        assert act == exp, f"product_except_self({input}) -> {act} != {exp}"


test_product_except_self()
