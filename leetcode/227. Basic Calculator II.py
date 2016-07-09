'''
Implement a basic calculator to evaluate a simple expression string.

The expression string contains only non-negative integers, +, -, *, / operators and empty spaces . The integer division should truncate toward zero.

You may assume that the given expression is always valid.

Some examples:
"3+2*2" = 7
" 3/2 " = 1
" 3+5 / 2 " = 5
Note: Do not use the eval built-in library function.
'''
import re
class Solution(object):
    def calculate(self, s):
        """
        :type s: str
        :rtype: int
        """
        list = ''.join(s.split())
        list = re.split('[+-///*]', list)
        print list


s = Solution()
s.calculate(" 3+5 / 2-5*3 ")