'''
Given two arrays, write a function to compute their intersection.

Example:
Given nums1 = [1, 2, 2, 1], nums2 = [2, 2], return [2].
'''
class Solution(object):
    def intersection(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        list = []
        if len(nums1) == 0 or len(nums2) == 0:
            return list
        s = set(nums1) & set(nums2)

        for i in s:
            list.append(i)
        return list

s = Solution()
print (s.intersection([1,2], [1]))