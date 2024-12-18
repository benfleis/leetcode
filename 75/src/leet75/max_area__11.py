#!/usr/bin/env python3

"""
# 11. Container With Most Water

Medium Topics Companies Hint

You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

## Example 1:

Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.

## Example 2:

Input: height = [1,1]
Output: 1


## Constraints:

n == height.length
2 <= n <= 105
0 <= height[i] <= 104
"""


class Solution:
    def maxArea(self, heights: list[int]) -> int:
        return max_area(heights)


def max_area(heights: list[int]) -> int:
    if len(heights) < 2:
        return 0

    lhs = 0
    rhs = len(heights) - 1
    best = 0

    while lhs < rhs:
        area = (rhs - lhs) * min(heights[lhs], heights[rhs])
        best = area if area > best else best
        if heights[lhs] < heights[rhs]:
            lhs += 1
        else:
            rhs -= 1

    return best


tests = [
    ([1, 2, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1], 11),
    ([1, 2, 1, 1, 1, 3, 1, 1, 1, 1, 1, 2], 20),
    ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
    ([1, 1], 1),
]


def test_max_area():
    for heights, exp in tests:
        act = max_area(heights)
        assert act == exp, f"max_area({heights}) -> {act} != {exp}"
        act_rev = max_area(list(reversed(heights)))
        assert act_rev == exp, f"max_area({reversed(heights)}) -> {act} != {exp}"
    else:
        print(f"OK: {len(tests)} tests passed.")


test_max_area()
