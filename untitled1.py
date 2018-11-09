# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 20:40:44 2018

@author: Sophia
"""

def join(l, sep):
    out_str = ''
    for i, el in enumerate(l):
        out_str += '{}{}'.format(el, sep)
    return out_str[:-len(sep)]


print (join([1,2,3,4,5,6] , '+' ))