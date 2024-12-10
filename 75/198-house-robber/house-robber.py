#!/usr/bin/env python

def rob_houses(houses: list[int]) -> int:
    # strategy - running maxes for "just robbed" and "just waited", iterate forward
    must_wait = can_rob = 0
    for house in houses:
        must_wait, can_rob = can_rob + house, max(can_rob, must_wait)
    return max(must_wait, can_rob)

tests = [
    ([], 0),
    ([2,4,2], 4),
    ([1,2,3,1], 4),
    ([2,7,9,3,1], 12),
    ([1,3,1,3,1], 6),
    ([1,3,1,3,1,1], 7),
    ([1,3,1,3,1,1,3], 9),
    ([1,3,1,3,1,1,3,1], 9),
    ([1,3,1,3,1,1,3,1,3], 12),
]

def test_stuff():
    for houses, exp in tests:
        act = rob_houses(houses)
        assert act == exp, f'Test: {houses} {act} != {exp}'
    else:
        print(f'All tests ({len(tests)}) passed.')


if __name__ == '__main__':
    test_stuff()

