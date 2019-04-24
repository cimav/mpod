'''
Created on Marzo 07, 2019

@author: Jorge Alberto Torres Acosta
'''

import os
import re
import string

from django.db import models
from django.db.models import Q
from django.db.models import Count
from data.models import *
from parse_files_2 import *
from django.core.exceptions import ObjectDoesNotExist
from data.Utils import *




class PropertiesKeyNotation (object):
    def __init__(self):
        self.value = None
        
    def tow_x__subtraction__s11_s12(self,nonzerocomponent_s11,nonzerocomponent_s12):
        result = None 
        try:
                result = 2  * (float(nonzerocomponent_s11) -float (nonzerocomponent_s12) )
        except ValueError:
            return result
        
        return result
    
    
    def a_medium_x__subtraction__c11_c12(self,nonzerocomponent_c11,nonzerocomponent_c12):
        result = None 
        try:
                result = 0.5  * (float(nonzerocomponent_c11) -float (nonzerocomponent_c12) )
        except ValueError:
            return result
        
        return result
    
    def nonzero(self,nonzerocomponent):
        result = None 
        try:
                result = float(nonzerocomponent)
        except ValueError:
            return result
        
        return result
    
    def equalcomponents(self,nonzerocomponent, *args):
        result = None 
        try:
                
                result = float(nonzerocomponent)
                for key, value in args[0].items():
                        args[0][key] = result
                        
                        
                        
        except ValueError:
            return result
        
        return args
    
    
    
        
            
            
