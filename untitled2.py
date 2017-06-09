# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 13:30:51 2017

@author: Snok
"""

class a():
    
    def __init__(self):
        self.x = 1
        
        
        
        
class b(object):
    
    def __init__(self):
        self.x = 2
        
    def f(self, c):
        print(self.x)
        print(c.x)
        
        
q = a()
w = b()

w.f(q)