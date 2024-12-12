#!/usr/bin/env python3

"""
# 605. Can Place Flowers
Easy Topics Companies

You have a long flowerbed in which some of the plots are planted, and some are
not. However, flowers cannot be planted in adjacent plots.

Given an integer array flowerbed containing 0's and 1's, where 0 means empty
and 1 means not empty, and an integer n, return true if n new flowers can be
planted in the flowerbed without violating the no-adjacent-flowers rule and
false otherwise.


## Example 1:

Input: flowerbed = [1,0,0,0,1], n = 1
Output: true

## Example 2:

Input: flowerbed = [1,0,0,0,1], n = 2
Output: false


## Constraints:

1 <= flowerbed.length <= 2 * 104
flowerbed[i] is 0 or 1.
There are no two adjacent flowers in flowerbed.
0 <= n <= flowerbed.length
"""

# %% Cell 1


class Solution:
    def canPlaceFlowers(self, flowerbed: list[int], n: int) -> bool:
        return place_flowers(flowerbed, n)


def place_flowers(flowerbed: list[int], n: int) -> bool:
    # strategy - mark previous state (full, space), initial state = space
    # iterate plots, plant greedily. If we hit a 1 and previous state == full (after planting), incr
    # n and carry on

    prev = 0  # states: None (beginning), 'f'ull, 's'pace
    # import pdb; pdb.set_trace()  # fmt: skip
    for plot in flowerbed:
        if plot == 0:
            if prev == 0:
                prev = 1  # plant
                n -= 1
            else:  # prev == 1:
                prev = 0
        else:  # plot == 1
            if prev == 1:
                n += 1  # roll back aggressive planting
            prev = 1
    return n <= 0
