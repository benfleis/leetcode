#!/usr/bin/env python3

__doc__ = """
328. Odd Even Linked List
Medium
Topics
Companies
Given the head of a singly linked list, group all the nodes with odd indices together followed by the nodes with even indices, and return the reordered list.

The first node is considered odd, and the second node is even, and so on.

Note that the relative order inside both the even and odd groups should remain as it was in the input.

You must solve the problem in O(1) extra space complexity and O(n) time complexity.

 

Example 1:


Input: head = [1,2,3,4,5]
Output: [1,3,5,2,4]
Example 2:


Input: head = [2,1,3,5,6,4,7]
Output: [2,3,6,7,1,5,4]
 

Constraints:

The number of nodes in the linked list is in the range [0, 104].
-106 <= Node.val <= 106
"""

from itertools import islice, chain
import typing


class ListNode:
    def __init__(self, val: int = 0, next: typing.Self | None = None):
        self.val = val
        self.next = next


def delete_next(node):
    if node.next:
        node.next = node.next.next


def node_to_list(node) -> list[int]:
    return [x.val for x in iter_nodes(node)]


def build_linked(iterable: typing.Iterable[int]) -> None | ListNode:
    head = prev = None
    for val in iterable:
        cur = ListNode(val)
        if not prev:
            head = prev = cur
        else:
            prev.next = cur
        prev = cur
    return head


def iter_nodes(head) -> typing.Generator[ListNode, None, None]:
    cur = head
    while cur is not None:
        yield cur
        cur = cur.next


def reweave_list(head: None | ListNode) -> None | ListNode:
    if not head:
        return None

    odds = islice(iter_nodes(head), 0, None, 2)
    evens = islice(iter_nodes(head), 1, None, 2)
    return build_linked(map(lambda x: x.val, chain(odds, evens)))


class Solution:
    def oddEvenList(self, head: None | ListNode) -> None | ListNode:
        return reweave_list(head)


tests = [
    ([], []),
    ([1], [1]),
    ([1, 2], [1, 2]),
    ([1, 2, 3], [1, 3, 2]),
    ([1, 2, 3, 4, 5], [1, 3, 5, 2, 4]),
    ([2, 1, 3, 5, 6, 4, 7], [2, 3, 6, 7, 1, 5, 4]),
]


def test_reweave():
    for input, exp in tests:
        linked_act = reweave_list(build_linked(input))
        act = node_to_list(linked_act) if linked_act else []
        assert act == exp, f"reweave_list({input}) -> {act} != {exp}"
