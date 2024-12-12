#!/usr/bin/env python3

from leet75.place_flowers__605 import place_flowers

# %% Cell 1

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
