

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
            self.puntualgroup = None
            self.propertyList=[]
            self.headerBlockValues = None
            
            
 
        
    def __del__(self):
        print "delete object"