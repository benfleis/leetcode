#!/usr/bin/env python

__doc__ = """
# 215. Kth Largest Element in an Array

Medium Topics Companies

Given an integer array nums and an integer k, return the kth largest element in the array.

Note that it is the kth largest element in the sorted order, not the kth distinct element.

Can you solve it without sorting?

## Example 1:

Input: nums = [3,2,1,5,6,4], k = 2
Output: 5


## Example 2:

Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4
 

## Constraints:

1 <= k <= nums.length <= 105
-104 <= nums[i] <= 104
"""

import heapq


class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        return find_kth_largest(nums, k)


def find_kth_largest(nums: list[int], k: int) -> int:
    heap = []
    for num in nums:
        heapq.heappush(heap, -num)
    for _ in range(k - 1):
        heapq.heappop(heap)
    return -heapq.heappop(heap)


tests = [
    ([3, 2, 1, 5, 6, 4], 2, 5),
    ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
]


def test_find_kth_largest():
    for input, k, exp in tests:
        act = find_kth_largest(input, k)
        assert act == exp, f"find_kth_largest({input}) -> {act} != {exp}"
    print("test_find_kth_largest: OK")


test_find_kth_largest()
