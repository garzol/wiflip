#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 4 déc. 2023

@author: garzol
'''

class Fletcher:
    C0_initial = 0
    C1_initial = 0
    def __init__(self, bn):
        self.C0 = self.C0_initial
        self.C1 = self.C1_initial
        
        for b in bn:
            self.C0 = ( (self.C0+b) % 255 )
            self.C1 = ( (self.C0+self.C1) % 255 )
    
    @property
    def crc(self):
        return(f"0X{self.C1:02X}{self.C0:02X}")
