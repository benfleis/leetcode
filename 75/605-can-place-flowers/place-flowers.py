#!/usr/bin/env python3


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
                n += 1  # correct aggressive planting
            prev = 1
    return n <= 0


tests: list[tuple[list[int], int, bool]] = [
    ([], 0, True),
    ([], 1, False),
    ([0], 1, True),
    ([0], 2, False),
    ([1, 0, 0, 1], 0, True),
    ([1, 0, 0, 1], 1, False),
    ([1, 0, 0, 0, 1], 2, False),
    ([1, 0, 0, 0, 1], 1, True),
    ([1, 0, 0, 0, 1], 2, False),
    ([1, 0, 0, 0, 0, 1], 1, True),
    ([1, 0, 0, 0, 0, 1], 2, False),
    ([1, 0, 0, 0, 0, 0, 1], 2, True),
    ([1, 0, 0, 0, 0, 0, 1], 3, False),
]


def test():
    for flowerbed, n, exp in tests:
        # import pdb; pdb.set_trace()  # fmt: skip
        act = place_flowers(flowerbed, n)
        assert act == exp, f"{flowerbed} {n} {act} != {exp}"
