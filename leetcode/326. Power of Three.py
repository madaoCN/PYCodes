#!/usr/bin/env python
#coding=utf8
'''
Given an integer, write a function to determine if it is a power of three.
'''
import math

class Solution(object):
    def isPowerOfThree(self, n):
        """
        :type n: int
        :rtype: bool
        """
        if n <= 0:
            return False
        temp = math.log10(n) / math.log10(3)
        if temp.is_integer():
            return True
        return False





s = Solution()
print(s.isPowerOfThree(243))
