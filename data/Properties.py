

import os
import numpy as N
from django.db import models
from data.models import *
from django.db.models import Count

class Properties():
    # define class variable shared by all instances
    # tricks = []             # should not be used as a class variable because just a single list would be shared by all Dog instances:
  def __init__(self, p,sisc):
      # define instance variable unique to each instance
      self.property = p
      self.propertydescrition=''
      self.sc = sisc
      self.scdescrition=''
      self.type = ''
      self.typedescrition = ''
      self.title= ''
      self.authors= ''
      self.journal= ''
      self.volume= ''
      self.year= ''
      
      self.puntualgroup= ''
      self.axis= ''
      
      self.error = ""
      self.ShowBtnSend = 0
      self.ShowBtnProcess  = 0
      self.message = ""
      self.questionAxis = ""
      self.questionGp= ""
      self.catalogPropertyDetail = []
      self.puntualGroupsList = []
      self.axisList = []
      self.process=0

      '''self.si=6
      self.sj=6
      self.ci=6
      self.cj=6
      self.di=3
      self.dj=6'''
          
      
      self.results = N.zeros([6,6])
      self.resultc = N.zeros([6,6])
      self.resultd = N.zeros([3,6])
      
      self.printings = 0
      self.printingc = 0
      self.printingd = 0
      
        
      
      
      self.s11= 0
      self.s12= 0
      self.s13= 0
      self.s14= 0
      self.s15= 0
      self.s16= 0
    
      self.s21= 0
      self.s22= 0
      self.s23= 0
      self.s24= 0
      self.s25= 0
      self.s26= 0
     
      self.s31= 0
      self.s32= 0
      self.s33= 0
      self.s34= 0
      self.s35= 0
      self.s36= 0
     
     
      self.s41= 0
      self.s42= 0
      self.s43= 0
      self.s44= 0
      self.s45= 0
      self.s46= 0
     
     
      self.s51= 0
      self.s52= 0
      self.s53= 0
      self.s54= 0
      self.s55= 0
      self.s56= 0
     
      self.s61= 0
      self.s62= 0
      self.s63= 0
      self.s64= 0
      self.s65= 0
      self.s66= 0
      
      self.c11= 0
      self.c12= 0
      self.c13= 0
      self.c14= 0
      self.c15= 0
      self.c16= 0
    
      self.c21= 0
      self.c22= 0
      self.c23= 0
      self.c24= 0
      self.c25= 0
      self.c26= 0
     
      self.c31= 0
      self.c32= 0
      self.c33= 0
      self.c34= 0
      self.c35= 0
      self.c36= 0
     
     
      self.c41= 0
      self.c42= 0
      self.c43= 0
      self.c44= 0
      self.c45= 0
      self.c46= 0
     
     
      self.c51= 0
      self.c52= 0
      self.c53= 0
      self.c54= 0
      self.c55= 0
      self.c56= 0
     
      self.c61= 0
      self.c62= 0
      self.c63= 0
      self.c64= 0
      self.c65= 0
      self.c66= 0
      
      
      
      self.d11= 0
      self.d12= 0
      self.d13= 0
      self.d14= 0
      self.d15= 0
      self.d16= 0
    
      self.d21= 0
      self.d22= 0
      self.d23= 0
      self.d24= 0
      self.d25= 0
      self.d26= 0
     
      self.d31= 0
      self.d32= 0
      self.d33= 0
      self.d34= 0
      self.d35= 0
      self.d36= 0
     
     
      self.d41= 0
      self.d42= 0
      self.d43= 0
      self.d44= 0
      self.d45= 0
      self.d46= 0
     
     
      self.d51= 0
      self.d52= 0
      self.d53= 0
      self.d54= 0
      self.d55= 0
      self.d56= 0
     
      self.d61= 0
      self.d62= 0
      self.d63= 0
      self.d64= 0
      self.d65= 0
      self.d66= 0
  
     
  
      
  def __del__(self):
          print "delete object"
          
  def validate(self,key,value):
        try:
              value =float (value)  
              return True        
        except  Exception, e:
               self.error=key + ": Invalid value"          
               return False
         
      
  def NewProperties(self,typeCS,groupp,axis):
   
    s = N.zeros([6,6])
    c = N.zeros([6,6])
    d = N.zeros([3,6])

    if self.property == 'e':
        self.type = typeCS #Deseas s (compliance) o c (stiffness)?
        if self.sc == 'iso':
            if self.process == 0:          
                objProperty=CatalogProperty.objects.filter(name=self.property) 
                objTypeSelected = Type.objects.filter(catalogproperty=objProperty,name=self.type)                 
                catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name=self.sc,catalogproperty=objProperty)                            
                propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected).order_by('name')
                for obj in propertyDetail:
                      cpd=CatalogPropertyDetail()
                      cpd = obj
                      self.catalogPropertyDetail.append(cpd) 
                      del cpd   
                      
                #self.ShowBtnSend = 1      
                self.ShowBtnSend = 0
                self.ShowBtnProcess = 1                   
                return
                
            if self.type == 's':                   
                if self.validate('s11',self.s11) != True:
                    return
                if self.validate('s12',self.s12) != True:
                    return
                            
                s[0,0] = s[1,1] = s[2,2] =float(self.s11)   
                s[0,1] = s[0,2] = s[1,2] = s[1,0] = s[2,0] = s[2,1] = float(self.s12)  
                s[3,3] = s[4,4] = s[5,5] = 2*(s[0,0] - s[0,1])
                
                self.results=s
                self.printings = 1
              
                #print (s)
            elif self.type == 'c':  
                if self.validate('c11',self.c11) != True:
                    return
                if self.validate('c12',self.c12) != True:
                    return              
                
                c[0,0] = c[1,1] = c[2,2] = float(self.c11)  
                c[0,1] = c[0,2] = c[1,2] = c[1,0] = c[2,0] = c[2,1] =float(self.c12)   
                c[3,3] = c[4,4] = c[5,5] = (c[0,0] - c[0,1])/2

                self.resultc=c
                self.printingc = 1
                #print (c)
            else:
                self.error ='Type not present'
        elif self.sc == 'c':
            self.message= 'All the point groups of this crystal system have the same matrix'
            if self.process == 0:          
                objProperty=CatalogProperty.objects.filter(name=self.property) 
                objTypeSelected = Type.objects.filter(catalogproperty=objProperty,name=self.type)                 
                catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name=self.sc,catalogproperty=objProperty)                            
                propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected).order_by('name')
                for obj in propertyDetail:
                      cpd=CatalogPropertyDetail()
                      cpd = obj
                      self.catalogPropertyDetail.append(cpd) 
                      del cpd       
                
                self.ShowBtnSend = 0
                self.ShowBtnProcess = 1         
                #self.ShowBtnSend = 1                        
                return 
                
            if self.type == 's':     
                if self.validate('s11',self.s11) != True:
                    return
                if self.validate('s12',self.s12) != True:
                    return  
                if self.validate('s44',self.s44) != True:
                    return  
                     
                s[0,0] = s[1,1] = s[2,2] = float (self.s11)
                s[0,1] = s[0,2] = s[1,2] = s[1,0] = s[2,0] = s[2,1] = float (self.s12)
                s[3,3] = s[4,4] = s[5,5] = float (self.s44)
                print (s)
                self.results=s
                self.printings = 1
            elif self.type == 'c':        
                if self.validate('c11',self.c11) != True:
                    return
                if self.validate('c12',self.c12) != True:
                    return                    
                if self.validate('c44',self.c44) != True:
                    return                               
                c[0][0] = c[1][1] = c[2][2] = float (self.c11)
                c[0][1] = c[0][2] = c[1][2] = c[1][0] = c[2][0] = c[2][1] = float (self.c12)
                c[3][3] = c[4][4] = c[5][5] = float (self.c44)
                print (c)
                self.resultc=c
                self.printingc = 1
            else:
                self.error ='Type not present'
        elif self.sc == 'h':
            self.message= 'All the point groups of this crystal system have the same matrix'
            if self.process == 0:          
                objProperty=CatalogProperty.objects.filter(name=self.property) 
                objTypeSelected = Type.objects.filter(catalogproperty=objProperty,name=self.type)                 
                catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name=self.sc,catalogproperty=objProperty)                            
                propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected).order_by('name')
                for obj in propertyDetail:
                      cpd=CatalogPropertyDetail()
                      cpd = obj
                      self.catalogPropertyDetail.append(cpd) 
                      del cpd  
                      
                self.ShowBtnSend = 0
                self.ShowBtnProcess = 1   
                #self.ShowBtnSend = 1                             
                return 
                
            if self.type == 's':            
                if self.validate('s11',self.s11) != True:
                    return
                if self.validate('s12',self.s12) != True:
                    return      
                if self.validate('s13',self.s13) != True:
                    return   
                if self.validate('s33',self.s33) != True:
                    return   
                if self.validate('s44',self.s44) != True:
                    return   
  
                
                
                s[0,0] = s[1,1] = float (self.s11)
                s[0,1] = s[1,0] = float (self.s12)
                s[0,2] = s[1,2] = s[2,0] = s[2,1] = float (self.s13)
                s[2,2] = float (self.s33)
                s[3,3] = s[4,4] = float (self.s44)
                s[5,5] = 2*(s[0,0] - s[0,1])
                print (s)
                self.results=s
                self.printings = 1
            elif self.type == 'c':
                if self.validate('c11',self.c11) != True:
                    return
                if self.validate('c12',self.c12) != True:
                    return      
                if self.validate('c13',self.c13) != True:
                    return   
                if self.validate('c33',self.c33) != True:
                    return   
                if self.validate('c44',self.c44) != True:
                    return   
        
                
                c[0,0] = c[1,1] = float (self.c11)
                c[0,1] = c[1,0] = float (self.c12)
                c[0,2] = c[1,2] = c[2,0] = c[2,1] = float (self.c13)
                c[2,2] = float (self.c33)
                c[3,3] = c[4,4] = float (self.c44)
                c[5,5] = (c[0,0] - c[0,1])/2
                print (c)
                self.resultc=c
                self.printingc = 1
            else:
                self.error ='Type not present'
        elif self.sc == 'o':
            self.message= 'All the point groups of this crystal system have the same matrix'
            if self.process == 0:          
                objProperty=CatalogProperty.objects.filter(name=self.property) 
                objTypeSelected = Type.objects.filter(catalogproperty=objProperty,name=self.type)                 
                catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name=self.sc,catalogproperty=objProperty)                            
                propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected).order_by('name')
                for obj in propertyDetail:
                      cpd=CatalogPropertyDetail()
                      cpd = obj
                      self.catalogPropertyDetail.append(cpd) 
                      del cpd     
                        
                self.ShowBtnSend = 0
                self.ShowBtnProcess = 1        
                #self.ShowBtnSend = 1                        
                return 
            if self.type == 's':
                if self.validate('s11',self.s11) != True:
                    return
                if self.validate('s12',self.s12) != True:
                    return      
                if self.validate('s13',self.s13) != True:
                    return   
                if self.validate('s22',self.s22) != True:
                    return
                if self.validate('s23',self.s23) != True:
                    return      
                if self.validate('s33',self.s33) != True:
                    return   
                if self.validate('s44',self.s44) != True:
                    return                   
                if self.validate('s55',self.s55) != True:
                    return   
                if self.validate('s66',self.s66) != True:
                    return   
                                              
                s[0,0] = float (self.s11)
                s[0,1] = s[1,0] = float (self.s12)
                s[0,2] = s[2,0] = float (self.s13)
                s[1,1] = float (self.s22)
                s[1,2] = s[2,1] = float (self.s23)
                s[2,2] = float (self.s33)
                s[3,3] = float (self.s44)
                s[4,4] = float (self.s55)
                s[5,5] = float (self.s66)
                #print (s)
                self.results=s
                self.printings = 1
            elif self.type == 'c':
                if self.validate('c11',self.c11) != True:
                    return
                if self.validate('c12',self.c12) != True:
                    return      
                if self.validate('c13',self.c13) != True:
                    return   
                if self.validate('c22',self.c22) != True:
                    return
                if self.validate('c23',self.c23) != True:
                    return      
                if self.validate('c33',self.c33) != True:
                    return   
                if self.validate('c44',self.c44) != True:
                    return                   
                if self.validate('c55',self.c55) != True:
                    return   
                if self.validate('c66',self.c66) != True:
                    return 
                c[0,0] = float (self.c11)
                c[0,1] = c[1,0] = float (self.c12)
                c[0,2] = c[2,0] = float (self.c13)
                c[1,1] = float (self.c22)
                c[1,2] = c[2,1] = float (self.c23)
                c[2,2] = float (self.c33)
                c[3,3] = float (self.c44)
                c[4,4] = float (self.c55)
                c[5,5] = float (self.c66)
                #print (c)
                self.resultc=c
                self.printingc = 1
                
            else:
                self.error ='Type not present'
        elif self.sc == 'tc':
            self.message= 'All the point groups of this crystal system have the same matrix'
            if self.process == 0:          
                objProperty=CatalogProperty.objects.filter(name=self.property) 
                objTypeSelected = Type.objects.filter(catalogproperty=objProperty,name=self.type)                 
                catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name=self.sc,catalogproperty=objProperty)                            
                propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected).order_by('name')
                for obj in propertyDetail:
                      cpd=CatalogPropertyDetail()
                      cpd = obj
                      self.catalogPropertyDetail.append(cpd) 
                      del cpd       
                
                self.ShowBtnSend = 0
                self.ShowBtnProcess = 1                    
                #self.ShowBtnSend = 1                        
                return 
                
            if self.type == 's':
                if self.validate('s11',self.s11) != True:
                    return
                if self.validate('s12',self.s12) != True:
                    return      
                if self.validate('s13',self.s13) != True:
                    return   
                if self.validate('s14',self.s14) != True:
                    return
                if self.validate('s15',self.s15) != True:
                    return      
                if self.validate('s16',self.s16) != True:
                    return   
                if self.validate('s22',self.s22) != True:
                    return
                if self.validate('s23',self.s23) != True:
                    return  
                if self.validate('s24',self.s24) != True:
                    return    
                if self.validate('s25',self.s25) != True:
                    return    
                if self.validate('s26',self.s26) != True:
                    return    
                if self.validate('s33',self.s33) != True:
                    return 
                if self.validate('s34',self.s34) != True:
                    return 
                if self.validate('s35',self.s35) != True:
                    return 
                if self.validate('s36',self.s36) != True:
                    return 
                if self.validate('s44',self.s44) != True:
                    return   
                if self.validate('s45',self.s45) != True:
                    return 
                if self.validate('s46',self.s46) != True:
                    return                 
                if self.validate('s55',self.s55) != True:
                    return   
                if self.validate('s56',self.s56) != True:
                    return   
                if self.validate('s66',self.s66) != True:
                    return 
                s[0,0] = float (self.s11)
                s[0,1] = s[1,0] = float (self.s12)
                s[0,2] = s[2,0] = float (self.s13)
                s[0,3] = s[3,0] = float (self.s14)
                s[0,4] = s[4,0] = float (self.s15)
                s[0,5] = s[5,0] = float (self.s16)
                s[1,1] = float (self.s22)
                s[1,2] = s[2,1] = float (self.s23)
                s[1,3] = s[3,1] = float (self.s24)
                s[1,4] = s[4,1] = float (self.s25)
                s[1,5] = s[5,1] = float (self.s26)
                s[2,2] = float (self.s33)
                s[2,3] = s[3,2] = float (self.s34)
                s[2,4] = s[4,2] = float (self.s35)
                s[2,5] = s[5,2] = float (self.s36)
                s[3,3] = float (self.s44)
                s[3,4] = s[4,3] = float (self.s45)
                s[3,5] = s[5,3] = float (self.s46)
                s[4,4] = float (self.s55)
                s[4,5] = s[5,4] = float (self.s56)
                s[5,5] = float (self.s66)
                print (s)
                self.results=s
                self.printings = 1
            elif self.type == 'c':
                if self.validate('c11',self.c11) != True:
                    return
                if self.validate('c12',self.c12) != True:
                    return      
                if self.validate('c13',self.c13) != True:
                    return   
                if self.validate('c14',self.c14) != True:
                    return
                if self.validate('c15',self.c15) != True:
                    return      
                if self.validate('c16',self.c16) != True:
                    return   
                if self.validate('c22',self.c22) != True:
                    return
                if self.validate('c23',self.c23) != True:
                    return  
                if self.validate('c24',self.c24) != True:
                    return    
                if self.validate('c25',self.c25) != True:
                    return    
                if self.validate('c26',self.c26) != True:
                    return    
                if self.validate('c33',self.c33) != True:
                    return 
                if self.validate('c34',self.c34) != True:
                    return 
                if self.validate('c35',self.c35) != True:
                    return 
                if self.validate('c36',self.c36) != True:
                    return 
                if self.validate('c44',self.c44) != True:
                    return   
                if self.validate('c45',self.c45) != True:
                    return 
                if self.validate('c46',self.c46) != True:
                    return                 
                if self.validate('c55',self.c55) != True:
                    return   
                if self.validate('c56',self.c56) != True:
                    return   
                if self.validate('c66',self.c66) != True:
                    return 
                c[0,0] = float (self.c11)
                c[0,1] = c[1,0] = float (self.c12)
                c[0,2] = c[2,0] = float (self.c13)
                c[0,3] = c[3,0] = float (self.c14)
                c[0,4] = c[4,0] = float (self.c15)
                c[0,5] = c[5,0] = float (self.c16)
                c[1,1] = float (self.c22)
                c[1,2] = c[2,1] = float (self.c23)
                c[1,3] = c[3,1] = float (self.c24)
                c[1,4] = c[4,1] = float (self.c25)
                c[1,5] = c[5,1] = float (self.c26)
                c[2,2] = float (self.c33)
                c[2,3] = c[3,2] = float (self.c34)
                c[2,4] = c[4,2] = float (self.c35)
                c[2,5] = c[5,2] = float (self.c36)
                c[3,3] = float (self.c44)
                c[3,4] = c[4,3] = float (self.c45)
                c[3,5] = c[5,3] = float (self.c46)
                c[4,4] = float (self.c55)
                c[4,5] = c[5,4] = float (self.c56)
                c[5,5] = float (self.c66)
                print (c)
                self.resultc=c
                self.printingc = 1
            else:
                self.error ='Type not present'
        elif self.sc == 'te':
            gp = groupp #Cual grupo puntual? (4, -4, 4/m, 422, 4mm, -42m, 4/mmm)
            if  gp == '' or gp not in '4, -4, 4/m, 422, 4mm, -42m, 4/mmm':
               self.questionGp = 'Point Group?'    
               self.ShowBtnSend = 1  
               return
            
            self.questionGp = 'Point Group?'  
            if self.process == 0:
                objProperty=CatalogProperty.objects.filter(name__exact=self.property) 
                objTypeSelected = Type.objects.filter(catalogproperty=objProperty,name__exact=self.type)        
                catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name__exact=self.sc,catalogproperty=objProperty)    
                catalogpointgroupSelected = CatalogPointGroup.objects.filter(name__exact=gp)     
            
                propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,catalogpointgroup=catalogpointgroupSelected).order_by('name')
              
                if not propertyDetail:  
                    #print 'no tiene puntual group'                                                                                                catalopointgroupSelected
                    objPuntualGroupGroups=PuntualGroupGroups.objects.filter(catalogpointgroup=catalogpointgroupSelected)          
                    for obj in objPuntualGroupGroups:
                       pgg=  PuntualGroupGroups()
                       pgg = obj   
                               
                       propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,puntualgroupnames=pgg.puntualgroupnames).order_by('name')
                       if  propertyDetail:
                           for obj in propertyDetail:
                              cpd=CatalogPropertyDetail()
                              cpd = obj
                              self.catalogPropertyDetail.append(cpd) 
                              del cpd 
                              
                    self.ShowBtnSend = 0
                    self.ShowBtnProcess = 1                                 
                    #self.ShowBtnSend = 1
                    return  
                else:                 
                   for obj in propertyDetail:
                      cpd=CatalogPropertyDetail()
                      cpd = obj
                      self.catalogPropertyDetail.append(cpd) 
                      del cpd         
                   self.ShowBtnSend = 1
                   return 
        
            if gp in ('4mm', '-42m', '422', '4/mmm'):
                if self.type == 's':
                    if self.validate('s11',self.s11) != True:
                        return
                    if self.validate('s12',self.s12) != True:
                        return      
                    if self.validate('s13',self.s13) != True:
                        return   
                    if self.validate('s33',self.s33) != True:
                        return
                    if self.validate('s44',self.s44) != True:
                        return      
                    if self.validate('s66',self.s66) != True:
                        return   
                    
                    
                    s[0,0] = s[1,1] = float (self.s11)
                    s[0,1] = s[1,0] = float (self.s12)
                    s[0,2] = s[1,2] = s[2,0] = s[2,1] = float (self.s13)
                    s[2,2] = float (self.s33)
                    s[3,3] = s[4,4] = float (self.s44)
                    s[5,5] = float (self.s66)
                    print (s)
                    self.results=s
                    self.printings = 1
                elif self.type == 'c':  
                    if self.validate('c11',self.c11) != True:
                        return
                    if self.validate('c12',self.c12) != True:
                        return      
                    if self.validate('c13',self.c13) != True:
                        return   
                    if self.validate('c33',self.c33) != True:
                        return
                    if self.validate('c44',self.c44) != True:
                        return      
                    if self.validate('c66',self.c66) != True:
                        return   
                                     
                    c[0,0] = c[1,1] = float (self.c11)
                    c[0,1] = c[1,0] = float (self.c12)
                    c[0,2] = c[1,2] = c[2,0] = c[2,1] = float (self.c13)
                    c[2,2] = float (self.c33)
                    c[3,3] = c[4,4] = float (self.c44)
                    c[5,5] = float (self.c66)
                    print (c)
                    self.resultc=c
                    self.printingc = 1
                else:
                    self.error ='Type not present'
            elif gp in ('4', '-4', '4/m'):
                if self.type == 's':
                    
                    if self.validate('s11',self.s11) != True:
                        return
                    if self.validate('s12',self.s12) != True:
                        return      
                    if self.validate('s13',self.s13) != True:
                        return   
                    if self.validate('s16',self.s16) != True:
                        return
                    if self.validate('s33',self.s33) != True:
                        return      
                    if self.validate('s44',self.s44) != True:
                        return   
                    if self.validate('s66',self.s66) != True:
                        return                   
                    s[0,0] = s[1,1] = float (self.s11)
                    s[0,1] = s[1,0] = float (self.s12)
                    s[0,2] = s[1,2] = s[2,0] = s[2,1] = float (self.s13)
                    s[0,5] = s[5,0] = float (self.s16)
                    s[1,5] = s[5,1] = -s[0,5]
                    s[2,2] = float (self.s33)
                    s[3,3] = s[4,4] = float (self.s44)
                    s[5,5] = float (self.s66)
                    print (s)
                    self.results=s
                    self.printings = 1
                elif self.type == 'c':
                    if self.validate('c11',self.c11) != True:
                        return
                    if self.validate('c12',self.c12) != True:
                        return      
                    if self.validate('c13',self.c13) != True:
                        return   
                    if self.validate('c16',self.c16) != True:
                        return
                    if self.validate('c33',self.c33) != True:
                        return      
                    if self.validate('c44',self.c44) != True:
                        return   
                    if self.validate('c66',self.c66) != True:
                        return 
                    c[0,0] = c[1,1] = float (self.c11)
                    c[0,1] = c[1,0] = float (self.c12)
                    c[0,2] = c[1,2] = c[2,0] = c[2,1] = float (self.c13)
                    c[0,5] = c[5,0] = float (self.c16)
                    c[1,5] = c[5,1] = -c[0,5]
                    c[2,2] = float (self.c33)
                    c[3,3] = c[4,4] = float (self.c44)
                    c[5,5] = float (self.c66)
                    
                    self.resultc=c
                    self.printingc = 1
                else:
                    self.error ='Type not present'
            else:
                self.error ='Non-existent point group'
        elif self.sc == 'm':
            eje = axis # Donde se ubica el eje especial?(x2 o x3)
            if  axis == '' or axis not in 'x2, x3':
               self.questionAxis = 'Where is the special axis1?' 
               self.ShowBtnSend = 1
               return
            if self.process == 0:
                self.questionAxis = 'Where is the special axis?'
                objProperty=CatalogProperty.objects.filter(name__exact=self.property) 
                objTypeSelected = Type.objects.filter(catalogproperty=objProperty,name__exact=self.type)        
                catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name__exact=self.sc,catalogproperty=objProperty)    
                #catalogpuntualgroupSelected = CatalogPuntualGroup.objects.filter(name__exact=gp)   
                axisSelected=CatalogAxis.objects.filter(name__exact=axis)
                  
                propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,catalogaxis=axisSelected).order_by('name')
                
                if self.process == 0:
                    for obj in propertyDetail: 
                      cpd=CatalogPropertyDetail()
                      cpd=obj                
                      self.catalogPropertyDetail.append(cpd)        
                    
                    self.ShowBtnSend = 0
                    self.ShowBtnProcess = 1
                    return 
                  
        
            self.message= 'All the point groups of this crystal system have the same matrix'
            if eje == 'x2':
                if self.type == 's':
                    if self.validate('s11',self.s11) != True:
                        return
                    if self.validate('s12',self.s12) != True:
                        return      
                    if self.validate('s13',self.s13) != True:
                        return   
                    if self.validate('s15',self.s15) != True:
                        return        
                    if self.validate('s22',self.s22) != True:
                        return
                    if self.validate('s23',self.s23) != True:
                        return    
                    if self.validate('s25',self.s25) != True:
                        return    
                    if self.validate('s33',self.s33) != True:
                        return    
                    if self.validate('s35',self.s35) != True:
                        return 
                    if self.validate('s44',self.s44) != True:
                        return
                    if self.validate('s46',self.s46) != True:
                        return
                    if self.validate('s55',self.s55) != True:
                        return
                    if self.validate('s66',self.s66) != True:
                        return   

                    
                    s[0,0] = float (self.s11)
                    s[0,1] = s[1,0] = float (self.s12)
                    s[0,2] = s[2,0] = float (self.s13)
                    s[0,4] = s[4,0] = float (self.s15)
                    s[1,1] = float (self.s22)
                    s[1,2] = s[2,1] = float (self.s23)
                    s[1,4] = s[4,1] = float (self.s25)
                    s[2,2] = float (self.s33)
                    s[2,4] = s[4,2] = float (self.s35)
                    s[3,3] = float (self.s44)
                    s[3,5] = s[5,3] = float (self.s46)
                    s[4,4] = float (self.s55)
                    s[5,5] = float (self.s66)
                    print (s)
                    self.results=s
                    self.printings = 1
                elif self.type == 'c':
                    if self.validate('c11',self.c11) != True:
                        return
                    if self.validate('c12',self.c12) != True:
                        return      
                    if self.validate('c13',self.c13) != True:
                        return   
                    if self.validate('c15',self.c15) != True:
                        return        
                    if self.validate('c22',self.c22) != True:
                        return
                    if self.validate('c23',self.c23) != True:
                        return    
                    if self.validate('c25',self.c25) != True:
                        return    
                    if self.validate('c33',self.c33) != True:
                        return    
                    if self.validate('c35',self.c35) != True:
                        return 
                    if self.validate('c44',self.c44) != True:
                        return
                    if self.validate('c46',self.c46) != True:
                        return
                    if self.validate('c55',self.c55) != True:
                        return
                    if self.validate('c66',self.c66) != True:
                        return    
                                        
                    c[0,0] = float (self.c11)
                    c[0,1] = c[1,0] = float (self.c12)
                    c[0,2] = c[2,0] = float (self.c13)
                    c[0,4] = c[4,0] = float (self.c15)
                    c[1,1] = float (self.c22)
                    c[1,2] = c[2,1] = float (self.c23)
                    c[1,4] = c[4,1] = float (self.c25)
                    c[2,2] = float (self.c33)
                    c[2,4] = c[4,2] = float (self.c35)
                    c[3,3] = float (self.c44)
                    c[3,5] = c[5,3] = float (self.c46)
                    c[4,4] = float (self.c55)
                    c[5,5] = float (self.c66)
                    print (c)
                    self.resultc=c
                    self.printingc = 1
                else:
                    self.error ='Type not present'
            elif eje == 'x3':
                if self.type == 's':
                    if self.validate('s11',self.s11) != True:
                        return
                    if self.validate('s12',self.s12) != True:
                        return      
                    if self.validate('s13',self.s13) != True:
                        return   
                    if self.validate('s16',self.s16) != True:
                        return
                    if self.validate('s22',self.s22) != True:
                        return      
                    if self.validate('s23',self.s23) != True:
                        return   
                    if self.validate('s26',self.s26) != True:
                        return
                    if self.validate('s33',self.s33) != True:
                        return  
                    if self.validate('s36',self.s36) != True:
                        return    
                    if self.validate('s44',self.s44) != True:
                        return    
                    if self.validate('s45',self.s45) != True:
                        return  
                    if self.validate('s55',self.s55) != True:
                        return    
                    if self.validate('s66',self.s66) != True:
                        return     

                    s[0,0] = float (self.s11)
                    s[0,1] = s[1,0] = float (self.s12)
                    s[0,2] = s[2,0] = float (self.s13)
                    s[0,5] = s[5,0] = float (self.s16)
                    s[1,1] = float (self.s22)
                    s[1,2] = s[2,1] = float (self.s23)
                    s[1,5] = s[5,1] = float (self.s26)
                    s[2,2] = float (self.s33)
                    s[2,5] = s[5,2] = float (self.s36)
                    s[3,3] = float (self.s44)
                    s[3,4] = s[4,3] = float (self.s45)
                    s[4,4] = float (self.s55)
                    s[5,5] = float (self.s66)
                    
                    self.results=s
                    self.printings = 1
                elif self.type == 'c':
                    if self.validate('c11',self.c11) != True:
                        return
                    if self.validate('c12',self.c12) != True:
                        return      
                    if self.validate('c13',self.c13) != True:
                        return   
                    if self.validate('c16',self.c16) != True:
                        return
                    if self.validate('c22',self.c22) != True:
                        return      
                    if self.validate('c23',self.c23) != True:
                        return   
                    if self.validate('c26',self.c26) != True:
                        return
                    if self.validate('c33',self.c33) != True:
                        return  
                    if self.validate('c36',self.c36) != True:
                        return    
                    if self.validate('c44',self.c44) != True:
                        return    
                    if self.validate('c45',self.c45) != True:
                        return  
                    if self.validate('c55',self.c55) != True:
                        return    
                    if self.validate('c66',self.c66) != True:
                        return 
                    
                    c[0,0] = float (self.c11)
                    c[0,1] = c[1,0] = float (self.c12)
                    c[0,2] = c[2,0] = float (self.c13)
                    c[0,5] = c[5,0] = float (self.c16)
                    c[1,1] = float (self.c22)
                    c[1,2] = c[2,1] = float (self.c23)
                    c[1,5] = c[5,1] = float (self.c26)
                    c[2,2] = float (self.c33)
                    c[2,5] = c[5,2] = float (self.c36)
                    c[3,3] = float (self.c44)
                    c[3,4] = c[4,3] = float (self.c45)
                    c[4,4] = float (self.c55)
                    c[5,5] = float (self.c66)
                    print (c)
                    self.resultc=c
                    self.printingc = 1
                else:
                    self.error ='Type not present'
            else:
                self.error ='Location of non-existent special axis'
        elif self.sc == 'tg':
            gp = groupp #Cual grupo puntual? (3, -3, 32, 3m, -3m)
            if  gp == '' or gp not in '3, -3, 32, 3m, -3m':
               self.questionGp = 'Point Group:'      
               self.ShowBtnSend = 1                        
               return
            if self.process == 0:
                self.questionGp = 'Point Group:?' 
                objProperty=CatalogProperty.objects.filter(name__exact=self.property) 
                objTypeSelected = Type.objects.filter(catalogproperty=objProperty,name__exact=self.type)        
                catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name__exact=self.sc,catalogproperty=objProperty)    
                catalogpointgroupSelected = CatalogPointGroup.objects.filter(name__exact=gp)     
            
                propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,catalogpointgroup=catalogpointgroupSelected).order_by('name')
              
                if not propertyDetail:  
                    #print 'no tiene puntual group'     
                    objPuntualGroupGroups=PuntualGroupGroups.objects.filter(catalogpointgroup=catalogpointgroupSelected)          
                    for obj in objPuntualGroupGroups:
                       pgg=  PuntualGroupGroups()
                       pgg = obj   
                               
                       propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,puntualgroupnames=pgg.puntualgroupnames).order_by('name')
                       if  propertyDetail:
                           for obj in propertyDetail:
                              cpd=CatalogPropertyDetail()
                              cpd = obj
                              self.catalogPropertyDetail.append(cpd) 
                              del cpd 
                              
                    self.ShowBtnSend = 0
                    self.ShowBtnProcess = 1            
                    #self.ShowBtnSend = 1
                    return  
                else:                 
                   for obj in propertyDetail:
                      cpd=CatalogPropertyDetail()
                      cpd = obj
                      self.catalogPropertyDetail.append(cpd) 
                      del cpd     
                      
                   self.ShowBtnSend = 0
                   self.ShowBtnProcess = 1         
                    #self.ShowBtnSend = 1
                    
                   return 
           
            
            if gp in ('32', '-3m', '3m'):
                if self.type == 's':
                    if self.validate('s11',self.s11) != True:
                        return
                    if self.validate('s12',self.s12) != True:
                        return      
                    if self.validate('s13',self.s13) != True:
                        return   
                    if self.validate('s14',self.s14) != True:
                        return
                    if self.validate('s33',self.s33) != True:
                        return      
                    if self.validate('s44',self.s44) != True:
                        return
                
                    s[0,0] = s[1,1] = float (self.s11)
                    s[0,1] = s[1,0] = float (self.s12)
                    s[0,2] = s[1,2] = s[2,0] = s[2,1] = float (self.s13)
                    s[0,3] = s[3,0] = float (self.s14)
                    s[1,3] = s[3,1] = -s[0,3]
                    s[4,5] = s[5,4] = 2*s[0,3]
                    s[2,2] = float (self.s33)
                    s[3,3] = s[4,4] = float (self.s44)
                    s[5,5] = 2*(s[0,0] - s[0,1])
                    print (s)
                    self.results=s
                    self.printings = 1
                elif self.type == 'c':
                    if self.validate('c11',self.c11) != True:
                        return
                    if self.validate('c12',self.c12) != True:
                        return      
                    if self.validate('c13',self.c13) != True:
                        return   
                    if self.validate('c14',self.c14) != True:
                        return
                    if self.validate('c33',self.c33) != True:
                        return      
                    if self.validate('c44',self.c44) != True:
                        return  
                          
                    c[0,0] = c[1,1] = float (self.c11)
                    c[0,1] = c[1,0] = float (self.c12)
                    c[0,2] = c[1,2] = c[2,0] = c[2,1] = float (self.c13)
                    c[0,3] = c[3,0] = c[4,5] = c[5,4] = float (self.c14)
                    c[1,3] = c[3,1] = -c[0,3]
                    c[2,2] = float (self.c33)
                    c[3,3] = c[4,4] = float (self.c44)
                    c[5,5] = (c[0,0] - c[0,1])/2
                    print (c)
                    self.resultc=c
                    self.printingc = 1
                else:
                    self.error ='Type not present'
            elif gp in ('3', '-3'):
                if self.type == 's':
                    if self.validate('s11',self.s11) != True:
                        return
                    if self.validate('s12',self.s12) != True:
                        return      
                    if self.validate('s13',self.s13) != True:
                        return   
                    if self.validate('s14',self.s14) != True:
                        return
                    if self.validate('s25',self.s25) != True:
                        return  
                    if self.validate('s33',self.s33) != True:
                        return    
                    if self.validate('s44',self.s44) != True:
                        return
                    
                    
                    s[0,0] = s[1,1] = float (self.s11)
                    s[0,1] = s[1,0] = float (self.s12)
                    s[0,2] = s[1,2] = s[2,0] = s[2,1] = float (self.s13)
                    s[0,3] = s[3,0] = float (self.s14)
                    s[1,3] = s[3,1] = -s[0,3]
                    s[4,5] = s[5,4] = 2*s[0,3]
                    s[1,4] = s[4,1] = float (self.s25)
                    s[0,4] = s[4,0] = -s[1,4]
                    s[3,5] = s[5,3] = 2*s[1,4]
                    s[2,2] = float (self.s33)
                    s[3,3] = s[4,4] = float (self.s44)
                    s[5,5] = 2*(s[0,0] - s[0,1])
                    print (s)
                    self.results=s
                    self.printings = 1
                elif self.type == 'c':
                    if self.validate('c11',self.c11) != True:
                        return
                    if self.validate('c12',self.c12) != True:
                        return      
                    if self.validate('c13',self.c13) != True:
                        return   
                    if self.validate('c14',self.c14) != True:
                        return
                    if self.validate('c25',self.c25) != True:
                        return  
                    if self.validate('c33',self.c33) != True:
                        return    
                    if self.validate('c44',self.c44) != True:
                        return    
                    
                    c[0,0] = c[1,1] = float (self.c11)
                    c[0,1] = c[1,0] = float (self.c12)
                    c[0,2] = c[1,2] = c[2,0] = c[2,1] = float (self.c13)
                    c[0,3] = c[3,0] = c[4,5] = c[5,4] = float (self.c14)
                    c[1,3] = c[3,1] = -c[0,3]
                    c[1,4] = c[4,1] = c[3,5] = c[5,3] = float (self.c25)
                    c[0,4] = c[4,0] = -c[1,4]
                    c[2,2] = float (self.c33)
                    c[3,3] = c[4,4] = float (self.c44)
                    c[5,5] = (c[0,0] - c[0,1])/2
                    print (c)
                    self.resultc=c
                    self.printingc = 1
                else:
                    self.error ='Type not present'
                    self.ShowBtnSend = 1
            else:
                self.error ='Non-existent point group'
                self.ShowBtnSend = 1
        else:
            self.ShowBtnSend = 1
            #self.error ='Crystal system '+self.scdescrition+'  does not exist for ' + self.propertydescrition 
            
    elif self.property == 'p':
        if self.sc == 'tc':
            gp = groupp  #Cual grupo puntual? (1, -1)
            if  gp == '' or gp not in '1, -1':
               self.questionGp = 'Point Group:'   
               self.ShowBtnSend = 1            
               return
           
            elif gp == '-1':
                self.error ='This point group does not have priezoelectricity'
                self.ShowBtnSend = 0
                self.ShowBtnProcess = 0 
                return  
 
                
            if self.process == 0:
                self.type = typeCS
                self.questionGp = 'Point Group:'
                objProperty=CatalogProperty.objects.filter(name__exact=self.property) 
                objTypeSelected = Type.objects.filter(catalogproperty=objProperty,name__exact=self.type)        
                catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name__exact=self.sc,catalogproperty=objProperty)    
                catalogpointgroupSelected = CatalogPointGroup.objects.filter(name__exact=gp)     
            
                propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,catalogpointgroup=catalogpointgroupSelected).order_by('name')
              
                if not propertyDetail:  
                    objPuntualGroupGroups=PuntualGroupGroups.objects.filter(catalogpointgroup=catalogpointgroupSelected)          
                    for obj in objPuntualGroupGroups:
                       pgg=  PuntualGroupGroups()
                       pgg = obj   
                               
                       propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,puntualgroupnames=pgg.puntualgroupnames).order_by('name')
                       if  propertyDetail:
                           for obj in propertyDetail:
                              cpd=CatalogPropertyDetail()
                              cpd = obj
                              self.catalogPropertyDetail.append(cpd) 
                              del cpd 
                               
                    self.ShowBtnSend = 0
                    self.ShowBtnProcess = 1                     
                    #self.ShowBtnSend = 1
                    return  
                else:                 
                   for obj in propertyDetail:
                      cpd=CatalogPropertyDetail()
                      cpd = obj
                      self.catalogPropertyDetail.append(cpd) 
                      del cpd      
                      
                   self.ShowBtnSend = 0
                   self.ShowBtnProcess = 1     
                   #self.ShowBtnSend = 1
                   return 
                
            if gp == '1':

                if self.validate('d11',self.d11) != True:
                    return
                if self.validate('d12',self.d12) != True:
                    return      
                if self.validate('d13',self.d13) != True:
                    return   
                if self.validate('d14',self.d14) != True:
                    return
                if self.validate('d15',self.d15) != True:
                    return      
                if self.validate('d16',self.d16) != True:
                    return   
                if self.validate('d21',self.d21) != True:
                    return
                if self.validate('d22',self.d22) != True:
                    return
                if self.validate('d23',self.d23) != True:
                    return  
                if self.validate('d24',self.d24) != True:
                    return    
                if self.validate('d25',self.d25) != True:
                    return    
                if self.validate('d26',self.d26) != True:
                    return    
                if self.validate('d31',self.d31) != True:
                    return 
                if self.validate('d32',self.d32) != True:
                    return 
                if self.validate('d33',self.d33) != True:
                    return 
                if self.validate('d34',self.d34) != True:
                    return 
                if self.validate('d35',self.d35) != True:
                    return 
                if self.validate('d36',self.d36) != True:
                    return 
                
                d[0,0] = float (self.d11)
                d[0,1] = float (self.d12)
                d[0,2] = float (self.d13)
                d[0,3] = float (self.d14)
                d[0,4] = float (self.d15)
                d[0,5] = float (self.d16)                
                d[1,0] = float (self.d21)
                d[1,1] = float (self.d22)
                d[1,2] = float (self.d23)
                d[1,3] = float (self.d24)
                d[1,4] = float (self.d25)
                d[1,5] = float (self.d26)                
                d[2,0] = float (self.d31)
                d[2,1] = float (self.d32)
                d[2,2] = float (self.d33)
                d[2,3] = float (self.d34)
                d[2,4] = float (self.d35)
                d[2,5] = float (self.d36)
                print (d)
                self.resultd=d
                self.printingd= 1

        elif self.sc == 'm':
            eje = axis #Donde se ubica el eje especial?(x2 o x3)
            gp = groupp #Cual grupo puntual? (2, m, 2/m)\n'))
            if  (axis == '' or axis not in 'x2, x3') or (gp == '' or gp not in '2, m, 2 / m'):
               self.questionAxis = 'Where is the special axis?' 
               self.questionGp = 'Point Group:'  
               self.ShowBtnSend = 1
               self.ShowBtnProcess = 0
               return 
           
            if gp == '2/m':
                    self.error ='This point group does not have priezoelectricity'
                    self.ShowBtnSend = 0
                    self.ShowBtnProcess = 0
                    return
   
 
           
           
            self.type = typeCS
            self.questionAxis = 'Where is the special axis?' 
            self.questionGp = 'Point Group:'
            if self.process == 0:
                objProperty=CatalogProperty.objects.filter(name__exact=self.property) 
                objTypeSelected = Type.objects.filter(catalogproperty=objProperty,name__exact=self.type)        
                catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name__exact=self.sc,catalogproperty=objProperty)    
                catalogpointgroupSelected = CatalogPointGroup.objects.filter(name__exact=gp)   
                axisSelected=CatalogAxis.objects.filter(name__exact=axis)
                 
                  
                propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,catalogaxis=axisSelected,catalogpointgroup=catalogpointgroupSelected).order_by('name')

                for obj in propertyDetail: 
                  cpd=CatalogPropertyDetail()
                  cpd=obj                
                  self.catalogPropertyDetail.append(cpd)   
                  self.ShowBtnSend = 0
                  self.ShowBtnProcess = 1     
                  #self.ShowBtnSend = 1           
                return 
            
        

            if eje == 'x2':
                if gp == '2':
                    if self.validate('d14',self.d14) != True:
                       return
                    if self.validate('d16',self.d16) != True:
                        return      
                    if self.validate('d21',self.d21) != True:
                        return   
                    if self.validate('d22',self.d22) != True:
                        return
                    if self.validate('d23',self.d23) != True:
                        return      
                    if self.validate('d25',self.d25) != True:
                        return   
                    if self.validate('d34',self.d34) != True:
                        return
                    if self.validate('d36',self.d36) != True:
                        return
                    
                    d[0,3] = float (self.d14)
                    d[0,5] = float (self.d16)
                    d[1,0] = float (self.d21)
                    d[1,1] = float (self.d22)
                    d[1,2] = float (self.d23)
                    d[1,4] = float (self.d25)
                    d[2,3] = float (self.d34)
                    d[2,5] = float (self.d36)
                    print (d)
                    self.resultd = d
                    self.printingd= 1
                elif gp == 'm':
                    if self.validate('d11',self.d11) != True:
                       return
                    if self.validate('d12',self.d12) != True:
                        return      
                    if self.validate('d13',self.d13) != True:
                        return   
                    if self.validate('d15',self.d15) != True:
                        return
                    if self.validate('d24',self.d24) != True:
                        return      
                    if self.validate('d26',self.d26) != True:
                        return   
                    if self.validate('d31',self.d31) != True:
                        return
                    if self.validate('d32',self.d32) != True:
                        return
                    if self.validate('d33',self.d33) != True:
                        return
                    if self.validate('d35',self.d35) != True:
                        return                    
                    
                    d[0,0] = float (self.d11)
                    d[0,1] = float (self.d12)
                    d[0,2] = float (self.d13)
                    d[0,4] = float (self.d15)
                    d[1,3] = float (self.d24)
                    d[1,5] = float (self.d26)
                    d[2,0] = float (self.d31)
                    d[2,1] = float (self.d32)
                    d[2,2] = float (self.d33)
                    d[2,4] = float (self.d35)
                    print (d)
                    self.resultd=d
                    self.printingd= 1

            elif eje == 'x3':
                if gp == '2':
                    if self.validate('d14',self.d14) != True:
                       return
                    if self.validate('d15',self.d15) != True:
                        return      
                    if self.validate('d24',self.d24) != True:
                        return   
                    if self.validate('d25',self.d25) != True:
                        return
                    if self.validate('d31',self.d31) != True:
                        return      
                    if self.validate('d32',self.d32) != True:
                        return   
                    if self.validate('d31',self.d31) != True:
                        return
                    if self.validate('d32',self.d32) != True:
                        return
                    if self.validate('d33',self.d33) != True:
                        return
                    if self.validate('d36',self.d36) != True:
                        return   
                    
                    
                    d[0,3] = float (self.d14)
                    d[0,4] = float (self.d15)
                    d[1,3] = float (self.d24)
                    d[1,4] = float (self.d25)
                    d[2,0] = float (self.d31)
                    d[2,1] = float (self.d32)
                    d[2,2] = float (self.d33)
                    d[2,5] = float (self.d36)
                    print (d)
                    self.resultd=d
                    self.printingd= 1
                elif gp == 'm':
                    if self.validate('d11',self.d11) != True:
                       return
                    if self.validate('d12',self.d12) != True:
                        return      
                    if self.validate('d13',self.d13) != True:
                        return   
                    if self.validate('d16',self.d16) != True:
                        return
                    if self.validate('d21',self.d21) != True:
                        return      
                    if self.validate('d22',self.d22) != True:
                        return   
                    if self.validate('d23',self.d23) != True:
                        return
                    if self.validate('d26',self.d26) != True:
                        return
                    if self.validate('d34',self.d34) != True:
                        return
                    if self.validate('d35',self.d35) != True:
                        return  
                    
                    d[0,0] = float (self.d11)
                    d[0,1] = float (self.d12)
                    d[0,2] = float (self.d13)
                    d[0,5] = float (self.d16)
                    d[1,0] = float (self.d21)
                    d[1,1] = float (self.d22)
                    d[1,2] = float (self.d23)
                    d[1,5] = float (self.d26)
                    d[2,3] = float (self.d34)
                    d[2,4] = float (self.d35)
                    print (d)
                    self.resultd=d
                    self.printingd= 1

        elif self.sc == 'o':
            gp = groupp #Cual grupo puntual? (222, 2mm, mmm)\n'))        
            if  gp == '' or gp not  in '222, 2mm, mmm' :
               self.questionGp = 'Point Group:'        
               self.ShowBtnSend = 1       
               self.ShowBtnProcess = 0   
               return
           
            if gp == 'mmm':
                self.error ='This point group does not have priezoelectricity'
                self.ShowBtnSend = 0
                self.ShowBtnProcess = 0   
                return
 
                
            if self.process == 0:
                self.type = typeCS
                self.questionGp = 'Point Group:'  
                objProperty=CatalogProperty.objects.filter(name__exact=self.property) 
                objTypeSelected = Type.objects.filter(catalogproperty=objProperty,name__exact=self.type)        
                catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name__exact=self.sc,catalogproperty=objProperty)    
                catalogpointgroupSelected = CatalogPointGroup.objects.filter(name__exact=gp)     
            
                propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,catalogpointgroup=catalogpointgroupSelected).order_by('name')
              
                if not propertyDetail:  
                    objPuntualGroupGroups=PuntualGroupGroups.objects.filter(catalogpointgroup=catalogpointgroupSelected)          
                    for obj in objPuntualGroupGroups:
                       pgg=  PuntualGroupGroups()
                       pgg = obj   
                               
                       propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,puntualgroupnames=pgg.puntualgroupnames).order_by('name')
                       if  propertyDetail:
                           for obj in propertyDetail:
                              cpd=CatalogPropertyDetail()
                              cpd = obj
                              self.catalogPropertyDetail.append(cpd) 
                              del cpd 
                              
                    self.ShowBtnSend = 0
                    self.ShowBtnProcess = 1   
                    
                    #self.ShowBtnSend = 1
                
                else:                 
                   for obj in propertyDetail:
                      cpd=CatalogPropertyDetail()
                      cpd = obj
                      self.catalogPropertyDetail.append(cpd) 
                      del cpd     
                          
                   self.ShowBtnSend = 0
                   self.ShowBtnProcess = 1   
                       
                return 
           
           
            if gp == '222':
                if self.validate('d14',self.d14) != True:
                   return
                if self.validate('d25',self.d25) != True:
                    return      
                if self.validate('d36',self.d36) != True:
                    return   

                d[0,3] = float (self.d14)
                d[1,4] = float (self.d25)
                d[2,5] = float (self.d36)
                print (d)
                self.resultd=d
                self.printingd= 1
            elif gp == '2mm':
               
                if self.validate('d15',self.d15) != True:
                    return      
                if self.validate('d24',self.d24) != True:
                    return   
                if self.validate('d31',self.d31) != True:
                    return
                if self.validate('d32',self.d32) != True:
                    return
                if self.validate('d33',self.d33) != True:
                    return
              
                    
                d[0,4] = float (self.d15)
                d[1,3] = float (self.d24)
                d[2,0] = float (self.d31)
                d[2,1] = float (self.d32)
                d[2,2] = float (self.d33)
                print (d)
                self.resultd=d
                self.printingd= 1

        elif self.sc == 'te':
            gp = groupp #Cual grupo puntual? (4, -4, 4/m, 422, 4mm, -42m, 4/mmm)\n'))
            if  gp == '' or gp not in '4, -4, 4/m, 422, 4mm, -42m, 4/mmm':
                self.questionGp = 'Point Group:'    
                self.ShowBtnSend = 1
                self.ShowBtnProcess = 0             
                return
           
            if gp in ('4/m', '4/mmm'):
                self.error ='This point group does not have priezoelectricity'
                self.ShowBtnSend = 0
                self.ShowBtnProcess = 0   
                return
        
            self.type = typeCS
            self.questionGp = 'Point Group:'  
            if self.process == 0:
                objProperty=CatalogProperty.objects.filter(name__exact=self.property) 
                objTypeSelected = Type.objects.filter(catalogproperty=objProperty,name__exact=self.type)        
                catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name__exact=self.sc,catalogproperty=objProperty)    
                catalogpointgroupSelected = CatalogPointGroup.objects.filter(name__exact=gp)     
            
                propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,catalogpointgroup=catalogpointgroupSelected).order_by('name')
              
                if not propertyDetail:  
                    objPuntualGroupGroups=PuntualGroupGroups.objects.filter(catalogpointgroup=catalogpointgroupSelected)          
                    for obj in objPuntualGroupGroups:
                       pgg=  PuntualGroupGroups()
                       pgg = obj   
                               
                       propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,puntualgroupnames=pgg.puntualgroupnames).order_by('name')
                       if  propertyDetail:
                           for obj in propertyDetail:
                              cpd=CatalogPropertyDetail()
                              cpd = obj
                              self.catalogPropertyDetail.append(cpd) 
                              del cpd 
                              
                    self.ShowBtnSend = 0
                    self.ShowBtnProcess = 1   
                    return  
                else:                 
                   for obj in propertyDetail:
                      cpd=CatalogPropertyDetail()
                      cpd = obj
                      self.catalogPropertyDetail.append(cpd) 
                      del cpd         
                   self.ShowBtnSend = 0
                   self.ShowBtnProcess = 1   
                   #self.ShowBtnSend = 1
                   return 
        
            if gp == '4':
                if self.validate('d14',self.d14) != True:
                    return      
                if self.validate('d15',self.d15) != True:
                    return   
                if self.validate('d31',self.d31) != True:
                    return
                if self.validate('d33',self.d33) != True:
                    return
   
                
                d[0,3] = float (self.d14)
                d[1,4] = -d[0,3]
                d[0,4] = d[1,3] = float (self.d15)
                d[2,0] = d[2,1] = float (self.d31)
                d[2,2] = float (self.d33)
                print (d)
                self.resultd=d
                self.printingd= 1
            elif gp == '-4':
                if self.validate('d14',self.d14) != True:
                    return      
                if self.validate('d15',self.d15) != True:
                    return   
                if self.validate('d31',self.d31) != True:
                    return
                if self.validate('d36',self.d36) != True:
                    return
                
                d[0,3] = d[1,4] = float (self.d14)
                d[0,4] = float (self.d15)
                d[1,3] = -d[0,4]
                d[2,0] = float (self.d31)
                d[2,1] = -d[2,0]
                d[2,5] = float (self.d36)
                print (d)
                self.resultd=d
                self.printingd= 1

            elif gp == '422':
                if self.validate('d14',self.d14) != True:
                    return      
                
                d[0,3] = float (self.d14)
                d[1,4] = -d[0,3]
                print (d)
                self.resultd=d
                self.printingd= 1
            elif gp == '4mm':
                if self.validate('d15',self.d15) != True:
                    return      
                if self.validate('d31',self.d31) != True:
                    return    
                if self.validate('d33',self.d33) != True:
                    return  
                
                d[0,4] = d[1,3] = float (self.d15)
                d[2,0] = d[2,1] = float (self.d31)
                d[2,2] = float (self.d33)
                
                self.resultd=d
                self.printingd= 1
            elif gp == '-42m':
                if self.validate('d14',self.d14) != True:
                    return      
                if self.validate('d36',self.d36) != True:
                    return 
                
                d[0,3] = d[1,4] = float (self.d14)
                d[2,5] = d36 = float (self.d36)
                
                self.resultd=d
                self.printingd= 1

        elif self.sc == 'c':
            gp = groupp # Cual grupo puntual? (23, m3, 432, -43m, m3m)\n'))
            if  gp == ''  or gp not in '23, m3, 432, -43m, m3m':
                self.questionGp = 'Point Group:'         
                self.ShowBtnSend = 1
                self.ShowBtnProcess = 0       
                return
           
            if gp in ('m3', '432', 'm3m'):
                self.error ='This point group does not have priezoelectricity'
                self.ShowBtnSend = 0
                self.ShowBtnProcess = 0   
                return
   
                
            self.type = typeCS
            self.questionGp = 'Point Group:' 
            if self.process == 0:
                objProperty=CatalogProperty.objects.filter(name__exact=self.property) 
                objTypeSelected = Type.objects.filter(catalogproperty=objProperty,name__exact=self.type)        
                catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name__exact=self.sc,catalogproperty=objProperty)    
                catalogpointgroupSelected = CatalogPointGroup.objects.filter(name__exact=gp)     
            
                propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,catalogpointgroup=catalogpointgroupSelected).order_by('name')
              
                if not propertyDetail:  
                    objPuntualGroupGroups=PuntualGroupGroups.objects.filter(catalogpointgroup=catalogpointgroupSelected)          
                    for obj in objPuntualGroupGroups:
                       pgg=  PuntualGroupGroups()
                       pgg = obj   
                               
                       propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,puntualgroupnames=pgg.puntualgroupnames).order_by('name')
                       if  propertyDetail:
                           for obj in propertyDetail:
                              cpd=CatalogPropertyDetail()
                              cpd = obj
                              self.catalogPropertyDetail.append(cpd) 
                              del cpd 
                    self.ShowBtnSend = 0
                    self.ShowBtnProcess = 1   
                    return  
                else:                 
                   for obj in propertyDetail:
                      cpd=CatalogPropertyDetail()
                      cpd = obj
                      self.catalogPropertyDetail.append(cpd) 
                      del cpd         
                   self.ShowBtnSend = 0
                   self.ShowBtnProcess = 1   
                   return   
             
            if gp in ('23', '-43m'):
                if self.validate('d14',self.d14) != True:
                    return 
                
                d[0,3] = d[1,4] = d[2,5] = float (self.d14)
               
                self.resultd=d
                self.printingd= 1

        elif self.sc == 'tg':
            gp = groupp #Cual grupo puntual? (3, -3, 32, 3m, -3m)\n'))
            if  gp == '' or gp not in '3, -3, 32, 3m, -3m':
               self.questionGp = 'Point Group:'       
               self.ShowBtnSend = 1
               self.ShowBtnProcess = 0        
               return
           
            if gp in ('-3', '-3m'):
                self.error ='This point group does not have priezoelectricity'
                self.ShowBtnSend = 0
                self.ShowBtnProcess = 0
                return 
          
        
            self.type = typeCS
            self.questionGp = 'Point Group:'    
            if self.process == 0:
                objProperty=CatalogProperty.objects.filter(name__exact=self.property) 
                objTypeSelected = Type.objects.filter(catalogproperty=objProperty,name__exact=self.type)        
                catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name__exact=self.sc,catalogproperty=objProperty)    
                catalogpointgroupSelected = CatalogPointGroup.objects.filter(name__exact=gp)     
                
                if gp == '3m':
                    if  axis == '' or axis not in 'x1, x2':
                      self.questionAxis = 'Where is the special axis?' 
                      self.ShowBtnSend = 1
                      self.ShowBtnProcess = 0                 
                      return               
                     
                    self.questionAxis = 'Where is the special axis?'                    
                        
                    axisSelected=CatalogAxis.objects.filter(name__exact=axis)                          
                    propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,catalogpointgroup=catalogpointgroupSelected,catalogaxis=axisSelected).order_by('name')

                    for obj in propertyDetail: 
                      cpd=CatalogPropertyDetail()
                      cpd=obj                
                      self.catalogPropertyDetail.append(cpd)              
                      
                    self.ShowBtnSend = 0
                    self.ShowBtnProcess = 1  
                    return 
                     
                else:
                    propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,catalogpointgroup=catalogpointgroupSelected).order_by('name')
              
                    if not propertyDetail:  
                        objPuntualGroupGroups=PuntualGroupGroups.objects.filter(catalogpointgroup=catalogpointgroupSelected)          
                        for obj in objPuntualGroupGroups:
                           pgg=  PuntualGroupGroups()
                           pgg = obj   
                                   
                           propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,puntualgroupnames=pgg.puntualgroupnames).order_by('name')
                           if  propertyDetail:
                               for obj in propertyDetail:
                                  cpd=CatalogPropertyDetail()
                                  cpd = obj
                                  self.catalogPropertyDetail.append(cpd) 
                                  del cpd 
                        self.ShowBtnSend = 0
                        self.ShowBtnProcess = 1  
                        return  
                    else:                 
                       for obj in propertyDetail:
                          cpd=CatalogPropertyDetail()
                          cpd = obj
                          self.catalogPropertyDetail.append(cpd) 
                          del cpd         
                       self.ShowBtnSend = 0
                       self.ShowBtnProcess = 1  
                       return 
               
               
               
               
            
           
            if gp == '3':
                if self.validate('d11',self.d11) != True:
                    return
                if self.validate('d14',self.d14) != True:
                    return      
                if self.validate('d15',self.d15) != True:
                    return   
                if self.validate('d22',self.d22) != True:
                    return
                if self.validate('d31',self.d31) != True:
                    return      
                if self.validate('d33',self.d33) != True:
                    return   
 
                
                
                d[0,0] = float (self.d11)
                d[0,1] = -d[0,0]
                d[1,5] = -2*d[0,0]
                d[0,3] = float (self.d14)
                d[1,4] = -d[0,3]
                d[0,4] = d[1][3] = float (self.d15)
                d[1,1] = float (self.d22)
                d[1,0] = -d[1,1]
                d[0,5] = -2*d[1,1]
                d[2,0] = d[2][1] = float (self.d31)
                d[2,2] = float (self.d33)
                print (d)
                self.resultd=d
                self.printingd= 1
            elif gp == '32':
                if self.validate('d11',self.d11) != True:
                    return
                if self.validate('d14',self.d14) != True:
                    return   
                
                d[0,0] = float (self.d11)
                d[0,1] = -d[0,0]
                d[1,5] = -2*d[0,0]
                d[0,3] = float (self.d14)
                d[1,4] = -d[0,3]
                
                self.resultd=d
                self.printingd= 1
            elif gp == '3m':
                eje = axis #Donde se ubica el eje especial?(x1 o x2)\n'))       
                if eje == 'x1':
                    if self.validate('d14',self.d14) != True:
                      return
                    if self.validate('d15',self.d15) != True:
                      return  
                    if self.validate('d22',self.d22) != True:
                      return
                    if self.validate('d31',self.d31) != True:
                      return                     
                    if self.validate('d33',self.d33) != True:
                      return
 
                   
                  
                    d[0,3] = float (self.d14)
                    d[1,4] = -d[0,3]
                    d[0,4] = d[1,3] = float (self.d15)
                    d[1,1] = float (self.d22)
                    d[1,0] = -d[1,1]
                    d[0,5] = -2*d[1,1]
                    d[2,0] = d[2][1] = float (self.d31)
                    d[2,2] = float (self.d33)
                  
                    self.resultd=d
                    self.printingd= 1
                elif eje == 'x2':
                    if self.validate('d11',self.d11) != True:
                      return
                    if self.validate('d14',self.d14) != True:
                      return  
                    if self.validate('d15',self.d15) != True:
                      return
                    if self.validate('d31',self.d31) != True:
                      return                     
                    if self.validate('d33',self.d33) != True:
                      return
                  
                    d[0,0] = float (self.d11)
                    d[0,1] = -d[0,0]
                    d[1,5] = -2*d[0,0]
                    d[0,3] = float (self.d14)
                    d[1,4] = -d[0,3]
                    d[0,4] = d[1,3] = float (self.d15)
                    d[2,0] = d[2,1] = float (self.d31)
                    d[2,2] = float (self.d33)
                    print (d)
                    self.resultd=d
                    self.printingd= 1
                else:
                    self.error ='Location of non-existent special axis'

        elif self.sc == 'h':
            gp = groupp #Cual grupo puntual? (6, -6, 6/m, 6mm, 622, -6m2, 6/mmm)\n'))
            if  gp == '' or gp not in '6, -6, 6/m, 6mm, 622, -6m2, 6/mmm' :
               self.questionGp = 'Point Group:'      
               self.ShowBtnSend =1
               self.ShowBtnProcess = 0           
               return
               
            if gp in ('6/m', '6/mmm'):
                 self.error ='This point group does not have priezoelectricity' 
                 self.ShowBtnSend = 0
                 self.ShowBtnProcess = 0  
                 return
             
        
            self.type = typeCS
            self.questionGp = 'Point Group:'  
            if self.process == 0:   
                objProperty=CatalogProperty.objects.filter(name__exact=self.property) 
                objTypeSelected = Type.objects.filter(catalogproperty=objProperty,name__exact=self.type)        
                catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name__exact=self.sc,catalogproperty=objProperty)    
                catalogpointgroupSelected = CatalogPointGroup.objects.filter(name__exact=gp)     
            
            
                if gp == '-6m2':
                    if  axis == '' or axis not in 'x1, x2':
                      self.questionAxis = 'Where is the special axis?'    
                      self.ShowBtnSend = 1
                      self.ShowBtnProcess = 0            
                      return
                  
                    self.questionAxis = 'Where is the special axis?'                       
                    axisSelected=CatalogAxis.objects.filter(name__exact=axis)                          
                    propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,catalogpointgroup=catalogpointgroupSelected,catalogaxis=axisSelected).order_by('name')

                    for obj in propertyDetail: 
                      cpd=CatalogPropertyDetail()
                      cpd=obj                
                      self.catalogPropertyDetail.append(cpd)             
                       
                    self.ShowBtnSend = 0
                    self.ShowBtnProcess = 1  
                    return 
            
                else:
                    propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,catalogpointgroup=catalogpointgroupSelected).order_by('name')
                  
                    if not propertyDetail:  
                        objPuntualGroupGroups=PuntualGroupGroups.objects.filter(catalogpointgroup=catalogpointgroupSelected)          
                        for obj in objPuntualGroupGroups:
                           pgg=  PuntualGroupGroups()
                           pgg = obj   
                                   
                           propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected,puntualgroupnames=pgg.puntualgroupnames).order_by('name')
                           if  propertyDetail:
                               for obj in propertyDetail:
                                  cpd=CatalogPropertyDetail()
                                  cpd = obj
                                  self.catalogPropertyDetail.append(cpd) 
                                  del cpd 
                                  
                        self.ShowBtnSend = 0
                        self.ShowBtnProcess = 1  
                        return  
                    else:                 
                       for obj in propertyDetail:
                          cpd=CatalogPropertyDetail()
                          cpd = obj
                          self.catalogPropertyDetail.append(cpd) 
                          del cpd         
                          
                       self.ShowBtnSend = 0
                       self.ShowBtnProcess = 1  
                       return 
           
            if gp == '6':
                if self.validate('d14',self.d14) != True:
                  return
                if self.validate('d15',self.d15) != True:
                  return  
                if self.validate('d31',self.d31) != True:
                  return
                if self.validate('d33',self.d33) != True:
                  return                     
   
              
                d[0,3] = float (self.d14)
                d[1,4] = -d[0,3]
                d[0,4] = d[1,3] = float (self.d15)
                d[2,0] = d[2,1] = float (self.d31)
                d[2,2] = float (self.d33)
                print (d)
                self.resultd=d
                self.printingd= 1
            elif gp == '6mm':
                if self.validate('d15',self.d15) != True:
                  return
                if self.validate('d31',self.d31) != True:
                  return  
                if self.validate('d33',self.d33) != True:
                  return
          
              
                d[0,4] = d[1,3] = float (self.d15)
                d[2,0] = d[2,1] = float (self.d31)
                d[2,2] = float (self.d33)
                print (d)
                self.resultd=d
                self.printingd= 1
            elif gp == '622':
                    
                if self.validate('d14',self.d14) != True:
                  return  
        
                d[0,3] = float (self.d14)
                d[1,4] = -d[0,3]
                print (d)
                self.resultd=d
                self.printingd= 1
            elif gp == '-6':
                if self.validate('d11',self.d11) != True:
                  return  
                if self.validate('d22',self.d22) != True:
                  return  
              
                d[0,0] = float (self.d11)
                d[0,1] = -d[0,0]
                d[1,5] = -2*d[0,0]
                d[1,1] = float (self.d22)
                d[1,0] = -d[1,1]
                d[0,5] = -2*d[1,1]
                print (d)
                self.resultd=d
                self.printingd= 1
            elif gp == '-6m2':
                eje = axis #Donde se ubica el eje especial?(x1 o x2)\n'))           
                if eje == 'x1':
           
                    if self.validate('d22',self.d22) != True:
                      return  
                  
                    d[1,1] = float (self.d22)
                    d[1,0] = -d[1,1]
                    d[0,5] = -2*d[1,1] 
                    print (d)
                    self.resultd=d
                    self.printingd= 1
                elif eje == 'x2':
                    if self.validate('d11',self.d11) != True:
                      return  
                  
                    d[0,0] = float (self.d11)
                    d[0,1] = -d[0,0]
                    d[1,5] = -2*d[0,0]
                    print (d)
                    self.resultd=d
                    self.printingd= 1
                else:
                    #print ('Ubicacion del eje especial inexistente')
                    self.error ='Location of non-existent special axis'
                    self.ShowBtnSend = 1

        else:
            self.ShowBtnSend = 1
            
            
             
            #self.error ='Crystal system ('+self.scdescrition+')  does not exist for ' + self.propertydescrition 
    else:
        self.error ='Nonexistent property'
        self.ShowBtnSend = 1
    
 
     
     