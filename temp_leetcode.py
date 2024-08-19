class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        if s[0] in t:
            start = t.index(s[0])
            s1 = s[1:]
            if len(s1) == 0:
                return True
            t1 = t[(start+1):]
        else:
            return False
        return self.isSubsequence(s1, t1)


s=''
t = 'abcdefg'
sol = Solution()
print(sol.isSubsequence(s, t))