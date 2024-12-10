#!/usr/bin/env python3

from functools import reduce
from itertools import batched, chain
import sys

##
# concept notes:
# - end state must be all things on LHS flying left (up to 0) and all things on RHS flying right
# - start on LHS, keep seeking/executing collisions until we can assert the above end state
#
# simplest: walk array, executing all neighbor collisions. Repeat until no collisions occur.
# possible better -- forward, backward?
# better: some fancy index stuff :)
#

def collide_neighbors(a0: int, a1: int) -> list[int]:
    # checks for collision -- if none, return [a0, a1]; if one, return remaining/victor or []
    if a0 > 0 and a1 < 0:
        m0, m1 = abs(a0), abs(a1)
        if m0 == m1:
            return []
        if m0 > m1:
            return [a0]
        else: # m0 < m1
            return [a1]
    return [a0, a1]


def collide_field_once(roids: list[int]) -> list[int]:
    # single pass collision run
    if len(roids) <= 1:
        return roids

    # out stack, think of deepest as LHS in above metaphor
    out = [roids[0]]
    i = 1
    while True:
        banged = collide_neighbors(out.pop(), roids[i])
        out.extend(banged)
        i += 1
        if i == len(roids):
            return out
        if not out:
            out.append(roids[i])


    #lhs, rhs = [], []
    #i, j = 0, len(roids) - 1
    #while i < len(roids) and j >= 0:

def collide_field(roids: list[int]) -> list[int]:
    prev = roids
    print(prev)
    while True:
        cur = collide_field_once(prev)
        print(cur)
        #print('#', end='')
        if cur == prev:
            print()
            return cur
        prev = cur


def test():
    tests = [
        ([], []),
        ([1], [1]),
        ([-1, 1], [-1, 1]),
        ([1, -1], []),
        ([5, 10, -5], [5, 10]),
        ([10, 2, -5], [10]),
    ]

    for field, exp in tests:
        print(field)
        act = collide_field(field)
        assert act == exp, f"collide_field(...) -> {act} != {exp}"


def main(args):
    test()

if __name__ == '__main__':
    main(sys.argv[:])

