#!/usr/bin/env python3

from typing import List
import sys

##
# approach:
# - sort by istart
# - iterate forward -- if adjacents do not overlap, drop first, else drop interval that ends first
#
# I didn't think this greedy form through, perhaps shortcoming at tail end?
#

def erase_overlap_intervals(intervals: List[List[int]]) -> int:
    if not intervals or len(intervals) == 1:
        return 0

    drops = 0
    cur = None
    for next in sorted(intervals):
        if cur is None or cur[1] <= next[0]:
            cur = next
        else:
            drops += 1
            if cur[1] >= next[1]:
                cur = next

    return drops

class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        return erase_overlap_intervals(intervals)


def test():
    tests = [
        ([], 0),
        ([[1, 2]], 0),
        ([[1,2],[2,3],[3,4],[1,3]], 1),
        ([[1,2],[1,2],[1,2]], 2),
        ([[1,2],[2,3]], 0),
    ]

    for intervals, exp in tests:
        print(intervals)
        act = erase_overlap_intervals(intervals)
        assert act == exp, f"erase_overlap_intervals(...) -> {act} != {exp}"


def main(args):
    test()

if __name__ == '__main__':
    main(sys.argv[:])
