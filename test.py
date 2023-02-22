class Solution(object):
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        chars = [s[0]]
        for c in s[1:]:
            if c in chars[-1]:
                chars[-1] += c
            else:
                chars.append(c)

        i = 0 #character in pattern
        j = 0 #string set in string
        k = 0 #character in string set
        star_power = False
        while i < len(p):
            c = p[i]
            if c != ".":
                star_power = False
            if (i+1 < len(p) and p[i+1] == "*") and c == ".":
                star_power = True
            if c in [".",s[i][k]] or star_power: # found character
                if (i+1 < len(p) and p[i+1] == "*"): # if the character can match the complete set
                    j += 1 #next set
                    k = 0 #first char in set
                    i += 1 #must skip 2 parts of pattern
                elif k == (len(s[i]) - 1):
                    j += 1 #next set
                    k = 0 #first char in set
                else:
                    k += 1
            elif i+1 < len(p) and p[i+1] == "*": #if the character doesnt exist but doesnt need to
                i += 1
            i += 1 # increment the character in the pattern
        print(i,j,k)
            

                
        print(chars)