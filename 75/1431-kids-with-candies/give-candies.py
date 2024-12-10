#!/usr/bin/env python3

class Solution:
    def kidsWithCandies(self, candies: list[int], extraCandies: int) -> list[bool]:
        return kids_with_candies(candies, extraCandies)


def kids_with_candies(candies: list[int], extra_candies: int) -> list[bool]:
    lucky_kid_candies = max(*candies)
    return list(map(lambda x: x + extra_candies >= lucky_kid_candies, candies))

tests = [
    ([2,3,5,1,3], 3, [True,True,True,False,True]),
    ([4,2,1,1,2], 1, [True,False,False,False,False]),
    ([12,1,12], 10, [True,False,True]),
]

def test():
    for (dist, extra, exp) in tests:
        act = kids_with_candies(dist, extra)
        assert act == exp

