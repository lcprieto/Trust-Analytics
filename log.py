# -*- coding: utf-8 -*-
"""
Created on Wed May  3 12:03:18 2017

@author: Luis Carlos Prieto
luisc.prieto@gmail.com
"""

import sys
    
class Log(object):
     

    
    def Salida (self, Texto):
        try:
            print(Texto, end="")  
            sys.stdout.flush()
        except Exception as e:
            print(" - ERROR -")
            sys.stdout.flush()
            pass
    

    
    def Salidaln (self, Texto):
        try:
            print( Texto)  
            sys.stdout.flush()
        except Exception as e:
            print(" - ERROR -")
            sys.stdout.flush()
            pass