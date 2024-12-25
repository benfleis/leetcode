#!/usr/bin/env python3

__doc__ = """
216. Combination Sum III
Medium
Topics
Companies
Find all valid combinations of k numbers that sum up to n such that the following conditions are true:

Only numbers 1 through 9 are used.
Each number is used at most once.
Return a list of all possible valid combinations. The list must not contain the same combination twice, and the combinations may be returned in any order.

 

Example 1:

Input: k = 3, n = 7
Output: [[1,2,4]]
Explanation:
1 + 2 + 4 = 7
There are no other valid combinations.
Example 2:

Input: k = 3, n = 9
Output: [[1,2,6],[1,3,5],[2,3,4]]
Explanation:
1 + 2 + 6 = 9
1 + 3 + 5 = 9
2 + 3 + 4 = 9
There are no other valid combinations.
Example 3:

Input: k = 4, n = 1
Output: []
Explanation: There are no valid combinations.
Using 4 different numbers in the range [1,9], the smallest sum we can get is 1+2+3+4 = 10 and since 10 > 1, there are no valid combination.
 

Constraints:

2 <= k <= 9
1 <= n <= 60
"""


from itertools import chain, combinations
from bisect import insort
import typing


class Solution:
    def combinationSum3(self, k: int, n: int) -> list[list[int]]:
        return find_sums(k, n)


type DigitSet = int
DS_ALL: DigitSet = 0x3FE
DS_NONE: DigitSet = 0x0


def ds_off(ds: DigitSet, *digits) -> DigitSet:
    inverse = DS_NONE
    for digit in digits:
        inverse |= 1 << digit
    return ds & ~inverse


def ds_on(ds: DigitSet, *digits) -> DigitSet:
    for digit in digits:
        ds |= 1 << digit
    return ds


def ds_contains(ds: DigitSet, digit: int) -> bool:
    return bool(1 << digit & ds)


def ds_limit_incl(ds: DigitSet, lo=None, hi=None) -> DigitSet:
    for digit in chain(range(1, lo or 0), range(1 + (hi or 10), 10)):
        ds = ds_off(ds, digit)
    return ds


def ds_range(ds: DigitSet, lo=None, hi=None) -> typing.Generator[int, None, None]:
    for digit in range(lo or 1, hi + 1 if hi else 10):
        if (1 << digit) & ds:
            yield digit
    return


def ds_pr(ds: DigitSet) -> None:
    print(list(ds_range(ds)))


def find_sums(k: int, sum: int, available: None | DigitSet = None) -> list[list[int]]:
    if k < 1 or sum < 1:
        return []

    available = DS_ALL if available is None else ds_limit_incl(available, hi=sum)
    if k == 1:
        return [[sum]] if ds_contains(available, sum) else []

    # recurse to find sums of (k, range(1,n))
    combos = []
    for digit in ds_range(available):
        for sub in find_sums(k - 1, sum - digit, available=ds_off(available, digit)):
            insort(sub, digit)
            combos.append(sub)

    # sort and uniquify
    return list(map(list, (sorted(set(map(tuple, combos))))))


def find_sums_choose_k(k: int, n: int):
    return list(
        map(
            list,
            filter(
                lambda x: sum(x) == n,
                # itertools.combinations([1, 2, 3, 4, 5, 6, 7, 8, 9], k),
                choose_k(k, list(range(1, 10))),
            ),
        )
    )


def choose_k[T](k: int, things: list[T]) -> typing.Generator[list[T], None, None]:
    if k > len(things):
        yield []
    elif k == len(things):
        yield things
    elif k == 1:
        for thing in things:
            yield [thing]
    else:  # 1 < k < len(things)
        for i, thing in enumerate(things[: -(k - 1)]):
            rest = things[i + 1 :]
            for chosen in choose_k(k - 1, rest):
                yield [thing] + list(chosen)


choose_tests = [
    ((2, [1, 2, 3]), [[1, 2], [1, 3], [2, 3]]),
    ((1, [1]), [[1]]),
    ((1, [1, 2, 3]), [[1], [2], [3]]),
    ((2, [1, 2]), [[1, 2]]),
    ((2, []), [[]]),
    ((3, list(range(5))), list(map(list, combinations(range(5), 3)))),
]


def test_choose_k():
    for i, ((k, things), exp) in enumerate(choose_tests):
        print(f"test_choose[{i}]: choose_k(k={k}, things={things})")
        act = list(choose_k(k, things))
        assert act == exp, f"choose_k(k={k}, things={things}) -> {act} != {exp}"


tests = [
    ((1, 1), [[1]]),
    ((2, 4), [[1, 3]]),
    ((4, 1), []),
    ((3, 7), [[1, 2, 4]]),
    ((3, 9), [[1, 2, 6], [1, 3, 5], [2, 3, 4]]),
]


def test():
    for (k, sum), exp in tests:
        act = find_sums_choose_k(k, sum)
        assert act == exp, f"find_sums(k={k}, sum={sum}) -> {act} != {exp}"
