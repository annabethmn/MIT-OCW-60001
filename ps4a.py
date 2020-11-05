# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 15:38:29 2020

@author: annab
"""
def get_permutations (string):
    permutations=[]
    if len(string)==1:
        permutations.append(string)
    else: 
        newstring1=string[0:1]
        newstring2=string[1:len(string)]
        permutations_newstring=get_permutations(newstring2)
        for i in range (0, len(permutations_newstring)):
            permutation=permutations_newstring[i]
            for i in range (0, len(permutation)+1):
                newstring3=permutation[0:i]
                newstring4=permutation[i:len(permutation)]
                newpermutation=newstring3+newstring1+newstring4
                permutations.append(newpermutation)
    return permutations
print(get_permutations("aeiou"))
            
            
        
