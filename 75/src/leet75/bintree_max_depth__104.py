#!/usr/bin/env python3

__doc__ = """
104. Maximum Depth of Binary Tree
Easy
Topics
Companies
Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

 

Example 1:


Input: root = [3,9,20,null,null,15,7]
Output: 3
Example 2:

Input: root = [1,null,2]
Output: 2
 

Constraints:

The number of nodes in the tree is in the range [0, 104].
-100 <= Node.val <= 100
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:
        return max_depth(root) if root else 0


def max_depth(root: TreeNode, cur_depth: int = 1) -> int:
    return max(
        max_depth(root.left, cur_depth + 1) if root.left else cur_depth,
        max_depth(root.right, cur_depth + 1) if root.right else cur_depth,
    )


tests = [
    ([0], 1),
    ([1, 2], 2),
    ([1, 2, 3], 2),
    ([1, 2, 3, 4], 3),
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


def test_max_depth():
    """Traverse recursively and keep max, returning all the way up."""
    for tree_list, exp in tests:
        tree = to_tree(tree_list)
        assert tree
        act = max_depth(tree)
        assert act == exp, f"max_depth({tree_list}) -> {act} != {exp}"
