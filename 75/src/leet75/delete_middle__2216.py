#!/usr/bin/env python3

import collections
from itertools import islice
from typing import Optional
import sys


# from itertools recipes
def consume(iterator, n=None):
    "Advance the iterator n-steps ahead. If n is None, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        collections.deque(iterator, maxlen=0)
    else:
        next(islice(iterator, n, n), None)

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __iter__(self):
        return self

    def __next__(self):
        return self.next


def delete_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    # handle 0, 1, 2 cases
    if head is None or head.next is None:
        return None
    if head.next.next is None:
        head.next = None
        return head


    # otherwise measure, then do it
    n = 1
    cur = head.next
    while cur:
        n += 1
        cur = cur.next
    
    prev_n = (n // 2) - 1
    prev = head
    for _ in range(prev_n):
        prev = prev.next

    prev.next = prev.next.next
    return head


class Solution:
    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        return delete_middle(head)


def to_linked(from_list):
    if not from_list: return None
    head = ListNode(from_list[0])
    cur = head
    for i in from_list[1:]:
       cur.next = ListNode(i)
       cur = cur.next
    return head

def iter_linked(linked):
    while linked:
        next = linked.next
        yield linked.val
        linked = next

def test():
    tests = [
        ([], []),
        ([1], []),
        ([2, 1], [2]),
        ([3, 2, 1], [3, 1]),
        ([4, 3, 2, 1], [4, 3, 1]),
        ([5, 4, 3, 2, 1], [5, 4, 2, 1]),
    ]

    for seq, exp in tests:
        print(seq)
        act_seq = delete_middle(to_linked(seq))
        act = [x for x in iter_linked(act_seq)]
        assert act == exp, f"collide_field(...) -> {act} != {exp}"


def main(args):
    test()

if __name__ == '__main__':
    main(sys.argv[:])

