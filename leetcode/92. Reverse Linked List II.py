'''
everse a linked list from position m to n. Do it in-place and in one-pass.

For example:
Given 1->2->3->4->5->NULL, m = 2 and n = 4,

return 1->4->3->2->5->NULL.

Note:
Given m, n satisfy the following condition:
1 ≤ m ≤ n ≤ length of list.
'''

# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

import copy

# class Solution(object):
#     def reverseBetween(self, head, m, n):
#         pre = head
#         headt = None
#         for i in range(m - 1):
#             headt = pre
#             pre = pre.next
#         for i in range(n - m):
#             cur = pre.next
#             pre.next = cur.next
#             if headt != None:
#                 cur.next = headt.next
#                 headt.next = cur
#             else:
#                 cur.next = head
#                 head = cur
#         return head
class Solution(object):
    def reverseBetween(self, head, m, n):
        if m == n:
            return head

        pre = head
        headp = None
        for i in range(m - 1):
            headp = pre
            pre = pre.next

        heads = None
        suf = pre
        for i in range(n - m):
            heads = suf
            suf = suf.next


        if heads == pre:
            pre.next = suf.next
            suf.next = pre
            return suf
        elif headp == None:
            headp = pre
            headp.next = suf
            suf.next = pre.next

        else:
            headp.next = suf
            suft = suf.next
            suf.next = pre.next
            pre.next = suft
            heads.next = pre
        return headp





