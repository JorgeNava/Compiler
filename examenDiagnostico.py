# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 22:31:49 2022

@author: Jorge Nava
"""

vocals = ['A','E','I','O']
nums = [4,3,1,0]

opt = input("Change vocals for numbers? (S/N)\nR: ").upper()

if opt == "S":
  print(vocals)
elif opt == "N":
  print(nums)
  
