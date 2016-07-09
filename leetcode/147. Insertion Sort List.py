'''
Sort a linked list using insertion sort.

Subscribe to see which companies asked this question
'''

# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def insertionSortList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        if head is None:
            return head
        pre = head.next
        cur = pre
        while cur != None:
            cur = cur.next

