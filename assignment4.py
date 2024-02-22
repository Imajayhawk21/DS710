#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 22:52:34 2024

@author: rajeshgogineni
"""

first_name = "Rajesh" # put your first name here, inside the ""
last_name  = "Gogineni" # put your last name here, inside the ""

#%%
#Max tuple check

def maximums(tuple_list):
    max_nums = max(tuple_list)
    return max_nums

#%%

maximums([(1,2,3),(4,5,6)])


#%%

maximums([(1,2,3),(4,5,6)]) == [3, 6]
maximums([(4.1, -3, 6), (-6, 2.0001, 10), (9/5, -5, 8/9), (-2, -7, 2, 7, 8, 2)]) == [6, 10, 1.8, 8]
maximums([(1.1,1.2,-1.3)]) == [1.2]
maximums([(0,)]) == [0] # it's not a tuple without the comma