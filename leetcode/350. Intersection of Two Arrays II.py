'''
Given two arrays, write a function to compute their intersection.

Example:
Given nums1 = [1, 2, 2, 1], nums2 = [2, 2], return [2, 2].

Note:
Each element in the result should appear as many times as it shows in both arrays.
The result can be in any order.
Follow up:
What if the given array is already sorted? How would you optimize your algorithm?
What if nums1's size is small compared to nums2's size? Which algorithm is better?
What if elements of nums2 are stored on disk, and the memory is limited such that you cannot load all elements into the memory at once?
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
        s = set(nums1) & set(nums2)#get the hashSet

        #traverse the s
        for i in s:
            flag1 = 0 #the num exist in nums1
            flag2 = 0 #the num exist in nums2
            for j in nums1:
                if i == j:
                    flag1 += 1
            for j in nums2:
                if i == j:
                    flag2 += 1
            for k in range(min(flag1, flag2)):#put i for min(flag1, flag2) times to list
                list.append(i)
        return list


s = Solution()
print (s.intersection([43,85,49,2,83,2,39,99,15,70,39,27,71,3,88,5,19,5,68,34,7,41,84,2,13,85,12,54,7,9,13,19,92], [10,8,53,63,58,83,26,10,58,3,61,56,55,38,81,29,69,55,86,23,91,44,9,98,41,48,41,16,42,72,6,4,2,81,42,84,4,13]))

