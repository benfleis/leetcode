#!/usr/bin/env python3

__doc__ = """
437. Path Sum III
Medium
Topics
Companies
Given the root of a binary tree and an integer targetSum, return the number of paths where the sum of the values along the path equals targetSum.

The path does not need to start or end at the root or a leaf, but it must go downwards (i.e., traveling only from parent nodes to child nodes).

Example 1:


Input: root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
Output: 3
Explanation: The paths that sum to 8 are shown.

Example 2:

Input: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
Output: 3
 

Constraints:

The number of nodes in the tree is in the range [0, 1000].
-109 <= Node.val <= 109
-1000 <= targetSum <= 1000
"""


# Definition for a binary tree node.
import collections
import typing


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"N({self.val})"

    __str__ = __repr__


class Solution:
    def pathSum(self, root: TreeNode | None, targetSum: int) -> int:
        if not root:
            return 0
        return count_path_sums(root, targetSum)


def count_path_sums(
    node: TreeNode | None,
    target_sum: int,
    partial_sum: int = 0,
    partial_counts: typing.MutableMapping[int, int] = {},
) -> int:
    # strategy: traverse (DFS) nodes; target_diff is the value required to count, and
    # target_diff_count tells us how many to count if `node.val` == `target_diff`;
    # traverse left and right, updating target_diff appropriately; any path zeroes along the
    # way cause target_diff_count to incr, thus e.g. [2, None, 1, None, -1, None, -2] carries
    # with starting sum = 0 carries these values into each node/RHS:
    # [(0, 1), (-2, 1), ]
    if not node:
        return 0

    if not partial_counts:
        partial_counts = collections.defaultdict[int, int](int)
        partial_counts[0] = 1

    partial_sum += node.val
    node_cnt = partial_counts[partial_sum - target_sum]

    partial_counts[partial_sum] += 1
    left_cnt = count_path_sums(node.left, target_sum, partial_sum, partial_counts)
    right_cnt = count_path_sums(node.right, target_sum, partial_sum, partial_counts)
    partial_counts[partial_sum] -= 1

    return node_cnt + left_cnt + right_cnt


tests = [
    ([1], 0, 0),
    ([2], 1, 0),
    ([2], 2, 1),
    ([2, None, -1], 1, 1),
    ([2, None, -1, None, 1], 1, 2),
    ([2, None, -1, None, 1, None, -1], 1, 3),
    ([2, None, -1, None, 1, None, -1, None, 2], 1, 5),
    ([-1, None, 1, None, 2, None, 3], 5, 2),
    ([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1], 8, 3),
    ([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], 22, 3),
]


def to_tree(tree_list: list[int]) -> TreeNode:
    # make nodes, then link them up
    nodes = [TreeNode(v) if isinstance(v, int) else None for v in tree_list]
    node_cnt: int = len(nodes)
    if node_cnt == 1:
        assert nodes[0]
        return nodes[0]

    # linkage was not what I thought -- it worked for examples but not actual test code
    # [2, None, 4, 10, 8, None, None, 4] -- in this example, 10 and 8 are children of 4
    # so we must iterate through active nodes alongside all nodes to combine
    child_iter = iter(nodes[1:])
    for parent in filter(None, nodes):
        try:
            left = next(child_iter)
            parent.left = left
            right = next(child_iter)
            parent.right = right
        except StopIteration:
            break

    assert nodes[0]
    return nodes[0]


def test_path_sum():
    for tree_list, target_sum, exp in tests:
        tree = to_tree(tree_list)
        assert tree
        act = count_path_sums(tree, target_sum)
        assert act == exp, f"count_path_sums({tree_list}) -> {act} != {exp}"
