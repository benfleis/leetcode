#!/usr/bin/env python3

import sys

##
# concept notes:
# - end state must be all things on LHS flying left (up to 0) and all things on RHS flying right
# - start on LHS, keep seeking/executing collisions until we can assert the above end state
#
# simplest: walk array, executing all neighbor collisions. Repeat until no collisions occur.
# possible better -- forward, backward?
# better: some fancy index stuff :)
# now: output as stack, works the LHS, input as stack, works as RHS
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


# pay the abstraction tax
def collide_field_v1(roids: list[int]) -> list[int]:
    if len(roids) <= 1:
        return roids

    rhs = roids[:]
    rhs.reverse()
    lhs = [rhs.pop()]

    while rhs:
        l = lhs.pop()
        r = rhs.pop()
        banged = collide_neighbors(l, r)
        if len(banged) == 2:
            lhs.extend(banged)
        elif len(banged) == 1: # goes to RHS because it gets a round against next LHS
            rhs.append(banged[0])
        if rhs and not lhs: # refill LHS
            lhs.append(rhs.pop())

    return lhs


def collide_field_v2(roids: list[int]) -> list[int]:
    if len(roids) <= 1:
        return roids

    lhs = []
    for roid in roids:
        print(f"lhs: {lhs}, roid: {roid}")
        while lhs and roid < 0 < lhs[-1]: # <- push roid into LHS blowing up as far as it can
            if -roid > lhs[-1]: # roid wins, blow up LHS challenger
                lhs.pop()
                continue
            if -roid == lhs[-1]: # everybody loses
                lhs.pop()
            # else: skip this roid, it lost
            break
        else:
            lhs.append(roid)
    return lhs


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
        act = collide_field_v2(field)
        assert act == exp, f"collide_field(...) -> {act} != {exp}"


def main(args):
    test()

if __name__ == '__main__':
    main(sys.argv[:])

