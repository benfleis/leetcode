#!/usr/bin/env python3

__doc__ = """
# 2336. Smallest Number in Infinite Set

Medium Topics Companies Hint

You have a set which contains all positive integers [1, 2, 3, 4, 5, ...].

Implement the SmallestInfiniteSet class:

SmallestInfiniteSet() Initializes the SmallestInfiniteSet object to contain all positive integers.
int popSmallest() Removes and returns the smallest integer contained in the infinite set.
void addBack(int num) Adds a positive integer num back into the infinite set, if it is not already in the infinite set.
 

## Example 1:

Input
["SmallestInfiniteSet", "addBack", "popSmallest", "popSmallest", "popSmallest", "addBack", "popSmallest", "popSmallest", "popSmallest"]
[[], [2], [], [], [], [1], [], [], []]
Output
[null, null, 1, 2, 3, null, 1, 4, 5]

## Explanation

SmallestInfiniteSet smallestInfiniteSet = new SmallestInfiniteSet();
smallestInfiniteSet.addBack(2);    // 2 is already in the set, so no change is made.
smallestInfiniteSet.popSmallest(); // return 1, since 1 is the smallest number, and remove it from the set.
smallestInfiniteSet.popSmallest(); // return 2, and remove it from the set.
smallestInfiniteSet.popSmallest(); // return 3, and remove it from the set.
smallestInfiniteSet.addBack(1);    // 1 is added back to the set.
smallestInfiniteSet.popSmallest(); // return 1, since 1 was added back to the set and
                                   // is the smallest number, and remove it from the set.
smallestInfiniteSet.popSmallest(); // return 4, and remove it from the set.
smallestInfiniteSet.popSmallest(); // return 5, and remove it from the set.
 

## Constraints:

1 <= num <= 1000
At most 1000 calls will be made in total to popSmallest and addBack.
"""

from heapq import heappop, heappush


class SmallestInfiniteSet:
    def __init__(self):
        # strategy -- keep a frontier to inf set at _next; alongside that a heap of pushbacks
        # within the pushbacks allow duplicates, which we'll delete when performing pops
        # this does lead to a pathological worst case if the same number gets inserted _a lot_
        # fix to that is keeping a parallel set
        # NOTE: the spec doesn't clarify behavior on dup inserts below the frontier,
        # or whether frontier changes at push
        self._next = 1
        self._to_pop = []

    def popSmallest(self) -> int:
        if self._to_pop:
            # pop return value (and any dups)
            rv = heappop(self._to_pop)
            while self._to_pop and self._to_pop[0] == rv:
                heappop(self._to_pop)
            return rv
        else:
            rv = self._next
            self._next += 1
            return rv

    def addBack(self, num: int) -> None:
        if num < self._next:
            heappush(self._to_pop, num)


# Your SmallestInfiniteSet object will be instantiated and called as such:
# obj = SmallestInfiniteSet()
# param_1 = obj.popSmallest()
# obj.addBack(num)

tests = [
    [
        ("SmallestInfiniteSet", [], None),
        ("addBack", [2], None),
        ("popSmallest", [], 1),
        ("popSmallest", [], 2),
        ("popSmallest", [], 3),
        ("addBack", [1], None),
        ("popSmallest", [], 1),
        ("popSmallest", [], 4),
        ("popSmallest", [], 5),
    ],
]


def test_smallest_number():
    for test in tests:
        iset = None
        for op, args, exp in test:
            if op == "SmallestInfiniteSet":
                iset = SmallestInfiniteSet()
                act = None
            elif op == "popSmallest":
                assert iset
                act = iset.popSmallest(*args)
            elif op == "addBack":
                assert iset
                act = iset.addBack(*args)
            else:
                assert False, "invalid op"
            assert act == exp, f"{op}({', '.join(args)}) -> {act} != {exp}"
    print("test_smallest_number: OK")


test_smallest_number()
