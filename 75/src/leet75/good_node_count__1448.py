#!/usr/bin/env python3

__doc__ = """
1448. Count Good Nodes in Binary Tree
Medium
Topics
Companies
Hint
Given a binary tree root, a node X in the tree is named good if in the path from root to X there are no nodes with a value greater than X.

Return the number of good nodes in the binary tree.

Example 1:

Input: root = [3,1,4,3,null,1,5]
Output: 4

Explanation: Nodes in blue are good.
Root Node (3) is always a good node.
Node 4 -> (3,4) is the maximum value in the path starting from the root.
Node 5 -> (3,4,5) is the maximum value in the path
Node 3 -> (3,1,3) is the maximum value in the path.


Example 2:

Input: root = [3,3,null,4,2]
Output: 3

Explanation: Node 2 -> (3, 3, 2) is not good, because "3" is higher than it.
Example 3:

Input: root = [1]
Output: 1
Explanation: Root is considered as good.
 

Constraints:

The number of nodes in the binary tree is in the range [1, 10^5].
Each node's value is between [-10^4, 10^4].
"""


# | None = None Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"N({self.val})"

    __str__ = __repr__


class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        return count_good_nodes(root)


def count_good_nodes(node: TreeNode, max_ancestor_value: int | None = None) -> int:
    anc_max: int = max_ancestor_value if max_ancestor_value is not None else node.val
    node_good: int = node.val >= anc_max
    node_max: int = max(anc_max, node.val)
    return (
        (1 if node_good else 0)
        + (count_good_nodes(node.left, node_max) if node.left else 0)
        + (count_good_nodes(node.right, node_max) if node.right else 0)
    )


tests = [
    ([2, None, 4, 10, 8, None, None, 4], 4),
    ([0], 1),
    ([3, 1, 4, 3, None, 1, 5], 4),
    ([3, 3, None, 4, 2], 3),
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


def test_good_node_count():
    """Traverse recursively and keep max, returning all the way up."""
    for tree_list, exp in tests:
        tree = to_tree(tree_list)
        assert tree
        act = count_good_nodes(tree)
        assert act == exp, f"count_good_nodes({tree_list}) -> {act} != {exp}"
