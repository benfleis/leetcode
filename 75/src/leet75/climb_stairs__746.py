#!/usr/bin/env python3

__doc__ = """
746. Min Cost Climbing Stairs
Easy
Topics
Companies
Hint

You are given an integer array cost where cost[i] is the cost of ith step on a staircase. Once you pay the cost, you can either climb one or two steps.

You can either start from the step with index 0, or the step with index 1.

Return the minimum cost to reach the top of the floor.

 

Example 1:

Input: cost = [10,15,20]
Output: 15
Explanation: You will start at index 1.
- Pay 15 and climb two steps to reach the top.
The total cost is 15.
Example 2:

Input: cost = [1,100,1,1,1,100,1,1,100,1]
Output: 6
Explanation: You will start at index 0.
- Pay 1 and climb two steps to reach index 2.
- Pay 1 and climb two steps to reach index 4.
- Pay 1 and climb two steps to reach index 6.
- Pay 1 and climb one step to reach index 7.
- Pay 1 and climb two steps to reach index 9.
- Pay 1 and climb one step to reach the top.
The total cost is 6.
 

Constraints:

2 <= cost.length <= 1000
0 <= cost[i] <= 999
"""


class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        return climb_stairs(cost)


def climb_stairs(costs: list[int]) -> int:
    if len(costs) <= 1:
        return 0

    # NOTE: we track cheapest way to arrive at any stair by checking -1, and -2 stairs.
    thru_0 = costs[0]
    thru_1 = costs[1]
    for i in range(2, len(costs)):
        thru_1, thru_0 = costs[i] + min(thru_0, thru_1), thru_1

    return min(thru_0, thru_1)


tests = [
    ([1, 100, 1, 1, 1, 100, 1, 1, 100, 1], 6),
    ([1, 0, 1], 0),
    ([0, 1], 0),
    ([1, 0], 0),
    ([10, 15, 20], 15),
    ([1, 100, 1, 1, 1, 100, 1, 1, 100, 1], 6),
]


def test_climb_stairs():
    for costs, exp in tests:
        act = climb_stairs(costs)
        assert act == exp, f"climb_stairs({costs}) -> {act} != {exp}"
