'''
Created on Feb 10, 2019

@author: Jorge Alberto Torres Acosta
'''

import os
 
 

class PropertyMaster(object):
    
    
    def __init__(self):
        
            self.title =  ""
            self.authors =  ""
            self.journal =  ""
            self.volume =  ""
            self.year = ""
            self.page_first =  ""
            self.page_last = ""
            self.pointgroup = None
            self.propertyList=[]
            self.headerBlockValues = None
            
            
 
        
    def __del__(self):
        print "delete object"