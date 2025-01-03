#!/usr/bin/env python3

__doc__ = """
2095. Delete the Middle Node of a Linked List
Medium
Topics
Companies
Hint
You are given the head of a linked list. Delete the middle node, and return the head of the modified linked list.

The middle node of a linked list of size n is the ⌊n / 2⌋th node from the start using 0-based indexing, where ⌊x⌋ denotes the largest integer less than or equal to x.

For n = 1, 2, 3, 4, and 5, the middle nodes are 0, 1, 1, 2, and 2, respectively.
 

Example 1:


Input: head = [1,3,4,7,1,2,6]
Output: [1,3,4,1,2,6]
Explanation:
The above figure represents the given linked list. The indices of the nodes are written below.
Since n = 7, node 3 with value 7 is the middle node, which is marked in red.
We return the new list after removing this node. 
Example 2:


Input: head = [1,2,3,4]
Output: [1,2,4]
Explanation:
The above figure represents the given linked list.
For n = 4, node 2 with value 3 is the middle node, which is marked in red.
Example 3:


Input: head = [2,1]
Output: [2]
Explanation:
The above figure represents the given linked list.
For n = 2, node 1 with value 1 is the middle node, which is marked in red.
Node 0 with value 2 is the only node remaining after removing node 1.
 

Constraints:

The number of nodes in the list is in the range [1, 105].
1 <= Node.val <= 105
"""

from itertools import islice
import typing


class ListNode:
    def __init__(self, value: int, next: None | typing.Self = None) -> None:
        self.value = value
        self.next = next

    def iter_nodes(self) -> typing.Generator[typing.Self, None, None]:
        cur = self
        while cur is not None:
            yield cur
            cur = cur.next

    def delete_next(self):
        if self.next:
            self.next = self.next.next


class Solution:
    def deleteMiddle(self, head: None | ListNode) -> None | ListNode:
        return delete_middle_zippy(head)


def delete_middle(head: None | ListNode) -> None | ListNode:
    # len 0 or 1
    if head is None or head.next is None:
        return None

    prev = single = double = head
    assert prev and single and double and head
    while double is not None:
        double = double.next
        if double is None:
            break
        prev = single
        single = single.next
        double = double.next

    prev.delete_next()
    return head


def delete_middle_zippy(head: None | ListNode) -> None | ListNode:
    if not head or head.next is None:
        return None

    # iterate through single speed, and double speed; double is offset +1 so that we del from prev
    # node
    prev = head
    for prev, _ in zip(head.iter_nodes(), islice(head.iter_nodes(), 1, None, 2)):
        pass  # ignore until list consumed
    else:
        prev.delete_next()
        return head


tests = [
    ([], []),
    ([1], []),
    ([2, 1], [2]),
    ([2, 1, 0], [2, 0]),
    ([1, 2, 3, 4], [1, 2, 4]),
    ([1, 3, 4, 7, 1, 2, 6], [1, 3, 4, 1, 2, 6]),
]


def list_to_linked(nums: list[int]) -> None | ListNode:
    if not nums:
        return None

    head = ListNode(nums[0])
    cur = head
    for elt in nums[1:]:
        cur.next = ListNode(elt)
        cur = cur.next
    return head


def linked_to_list(head: None | ListNode) -> list[int]:
    rv = []
    while head:
        rv.append(head.value)
        head = head.next
    return rv


def test_delete_middle():
    for input, exp in tests:
        act = linked_to_list(delete_middle_zippy(list_to_linked(input)))
        assert act == exp, f"delete_middle_zippy({input}) -> {act} != {exp}"
