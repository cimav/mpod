'''
Created on Jun 18, 2016

@author: alfredo
'''

#import matplotlib.pyplot as plt
import plotly.plotly as py
from plotly.graph_objs import *
import numpy as np
from numpy import sin,cos,pi,abs
#from pylab import *
import sys
from smtpd import parseargs
from stlwrite import *
import os.path
import math



class Magneto():
  def __init__(self):
      self.A = 1
      self.stringValsOfXEC = ''
      self.stringValsOfYEC = ''
      self.stringValsOfZEC = ''
      self.surfacecolorMagneticAnisotropy=''
      self.surfacecolorMagnetostriction=''
      
  def dist_origin(self,x, y, z):
         return math.sqrt((1.0 * x)**2 + (1.0 * y)**2 + (1.0 * z)**2)
         
  def MagnetocrystallineAnisotropy(self,k1,k2, Color,filename,res,stl_dir,createstl,createdata):     
        filename= filename
          #self.Res = res
        stldir=stl_dir
        createstl= createstl
        createdata = createdata
        color = Color
        
        if res == 1:
              phi, beta = np.mgrid[0:np.pi:45j,0:2*np.pi:90j]
        elif res == 2:
              phi, beta = np.mgrid[0:np.pi:90j,0:2*np.pi:180j] 
        elif res == 3:
              phi, beta = np.mgrid[0:np.pi:180j,0:2*np.pi:360j] 
        
        
        x = sin(phi)*cos(beta)
        y = sin(phi)*sin(beta)
        z = cos(phi)

        S1=k1*((x**2)*(y**2) + (x**2)*(z**2) + (y**2)*(z**2))
        S2=k2*((x**2)*(y**2)*(z**2))
        S=S1+S2
        XEC = S*sin(phi)*cos(beta)
        YEC = S*sin(phi)*sin(beta)
        ZEC = S*cos(phi)

        scale = 100
        if createstl == 1: 
              fl= filename 
              #stl_dir = ".\\media\\stlfiles\\"      
            
              
              filepath=os.path.join(stldir, fl)
              print 'RUTA:' + filepath
              stlw = STLUtil()
              tri = stlw.stlwrite(filepath,XEC,YEC,ZEC,scale)
              del stlw
 
   
        if createdata == 1:  
            b=0
            for itemX in XEC:                      
                b = b + 1  
                if  b ==  len(XEC):                
                  c = 0 
                  self.stringValsOfXEC =  self.stringValsOfXEC + '['                 
                  for val in itemX:  
                    c = c + 1               
                    if c == len(itemX):                
                          self.stringValsOfXEC =   self.stringValsOfXEC + str(val) +']'       
                    else:    
                          self.stringValsOfXEC =  self.stringValsOfXEC + str(val) + ','       
                          
                else:
                  c = 0 
                  self.stringValsOfXEC =  self.stringValsOfXEC + '['                           
                  for val in itemX: 
                    c = c + 1
                    if c == len(itemX):                
                          self.stringValsOfXEC =   self.stringValsOfXEC + str(val) +'],'       
                    else:    
                          self.stringValsOfXEC =  self.stringValsOfXEC + str(val) + ',' 
              
            b=0            
            for itemY in YEC:                      
                b = b + 1  
                if  b ==  len(YEC):                 
                  c = 0 
                  self.stringValsOfYEC =  self.stringValsOfYEC + '['                 
                  for val in itemY:  
                    c = c + 1               
                    if c == len(itemY):                
                          self.stringValsOfYEC =   self.stringValsOfYEC + str(val) +']'       
                    else:    
                          self.stringValsOfYEC =  self.stringValsOfYEC + str(val) + ','       
                          
                else:
                  c = 0 
                  self.stringValsOfYEC =  self.stringValsOfYEC + '['                           
                  for val in itemY: 
                    c = c + 1
                    if c == len(itemY):                
                          self.stringValsOfYEC =   self.stringValsOfYEC + str(val) +'],'       
                    else:    
                          self.stringValsOfYEC =  self.stringValsOfYEC + str(val) + ','             
                          
            b = 0
            for itemZ in ZEC:                      
               # if (itemZ ==  ZEC[-1:]).all():   
                b = b + 1   
                t = len(ZEC)    
                if  b ==  len(ZEC):      
                  c = 0 
                  self.stringValsOfZEC =  self.stringValsOfZEC + '['                 
                  for val in itemZ:  
                    c = c + 1               
                    if c == len(itemZ):                
                          self.stringValsOfZEC =   self.stringValsOfZEC + str(val) +']'       
                    else:    
                          self.stringValsOfZEC =  self.stringValsOfZEC + str(val) + ','       
                          
                else:
                  c = 0 
                  self.stringValsOfZEC =  self.stringValsOfZEC + '['                           
                  for val in itemZ: 
                    c = c + 1
                    if c == len(itemZ):                
                          self.stringValsOfZEC =   self.stringValsOfZEC + str(val) +'],'       
                    else:    
                          self.stringValsOfZEC =  self.stringValsOfZEC + str(val) + ',' 
      
      
        if createdata == 1:
            if "anisotropy" in filename:
                 SC = []
                 SC= S
                 b = 0
                 
                 for itemSC in SC:                      
                    b = b + 1   
                    t = len(S)    
                    if  b ==  len(S):      
                      c = 0 
                      self.surfacecolorMagneticAnisotropy =  self.surfacecolorMagneticAnisotropy + '['                 
                      for val in itemSC:  
                        c = c + 1               
                        if c == len(itemSC):                
                              self.surfacecolorMagneticAnisotropy =   self.surfacecolorMagneticAnisotropy + str(val) +']'       
                        else:    
                              self.surfacecolorMagneticAnisotropy =  self.surfacecolorMagneticAnisotropy + str(val) + ','       
                    else:
                      c = 0 
                      self.surfacecolorMagneticAnisotropy =  self.surfacecolorMagneticAnisotropy + '['                           
                      for val in itemSC: 
                        c = c + 1
                        if c == len(itemSC):                
                              self.surfacecolorMagneticAnisotropy =   self.surfacecolorMagneticAnisotropy + str(val) +'],'       
                        else:    
                              self.surfacecolorMagneticAnisotropy =  self.surfacecolorMagneticAnisotropy + str(val) + ','   
                 
                 self.surfacecolorMagneticAnisotropy =  '['  + self.surfacecolorMagneticAnisotropy + ']' 
            else: 
            
              lx=len(ZEC)
              ly=len(ZEC[0])
              sc='['
              out=[]
              for i in xrange(lx):
                    temp = []
                    sc= sc + '['
                    for j in xrange( ly):
                        res= self.dist_origin(XEC[i][j], YEC[i][j], ZEC[i][j])
                        #print res
                        if j ==( ly -1): 
                            if i == ( lx -1): 
                                sc= sc + str(res) + ']'  
                            else:
                                sc= sc + str(res) + '],'  
                            #print sc
                        else:
                              sc= sc + str(res) + ','  
        
               
              sc= sc + ']'     
              self.surfacecolorMagneticAnisotropy =sc  
          
  def MagnetoStriction(self,k1,k2, Color,filename,res,stl_dir,createstl,createdata):     
        filename= filename
          #self.Res = res
        stldir=stl_dir
        createstl= createstl
        createdata = createdata
        color = Color
        #L100=318*2/3; L111=-20*2/3
        L100=k1*2/3; L111=k2*2/3
        
        if res == 1:
              phi, beta = np.mgrid[0:np.pi:45j,0:2*np.pi:90j]
        elif res == 2:
              phi, beta = np.mgrid[0:np.pi:90j,0:2*np.pi:180j] 
        elif res == 3:
              phi, beta = np.mgrid[0:np.pi:180j,0:2*np.pi:360j] 

        
        #phi, beta = np.mgrid[0:np.pi:180j,0:2*np.pi:360j]
        x = sin(phi)*cos(beta)
        y = sin(phi)*sin(beta)
        z = cos(phi)
        S0=L100
        S1=3*(L111-L100)*((x**2)*(y**2) + (x**2)*(z**2) + (y**2)*(z**2))
        S=S0+S1
        XEC = S*sin(phi)*cos(beta)
        YEC = S*sin(phi)*sin(beta)
        ZEC = S*cos(phi)
        
        scale = 100
        if createstl == 1: 
              fl= filename 

              filepath=os.path.join(stldir, fl)
              stlw = STLUtil()
              tri = stlw.stlwrite(filepath,XEC,YEC,ZEC,scale)
              del stlw
 
   
        if createdata == 1:  
            b=0
            for itemX in XEC:                      
                b = b + 1  
                if  b ==  len(XEC):                
                  c = 0 
                  self.stringValsOfXEC =  self.stringValsOfXEC + '['                 
                  for val in itemX:  
                    c = c + 1               
                    if c == len(itemX):                
                          self.stringValsOfXEC =   self.stringValsOfXEC + str(val) +']'       
                    else:    
                          self.stringValsOfXEC =  self.stringValsOfXEC + str(val) + ','       
                          
                else:
                  c = 0 
                  self.stringValsOfXEC =  self.stringValsOfXEC + '['                           
                  for val in itemX: 
                    c = c + 1
                    if c == len(itemX):                
                          self.stringValsOfXEC =   self.stringValsOfXEC + str(val) +'],'       
                    else:    
                          self.stringValsOfXEC =  self.stringValsOfXEC + str(val) + ',' 
              
            b=0            
            for itemY in YEC:                      
                b = b + 1  
                if  b ==  len(YEC):                 
                  c = 0 
                  self.stringValsOfYEC =  self.stringValsOfYEC + '['                 
                  for val in itemY:  
                    c = c + 1               
                    if c == len(itemY):                
                          self.stringValsOfYEC =   self.stringValsOfYEC + str(val) +']'       
                    else:    
                          self.stringValsOfYEC =  self.stringValsOfYEC + str(val) + ','       
                          
                else:
                  c = 0 
                  self.stringValsOfYEC =  self.stringValsOfYEC + '['                           
                  for val in itemY: 
                    c = c + 1
                    if c == len(itemY):                
                          self.stringValsOfYEC =   self.stringValsOfYEC + str(val) +'],'       
                    else:    
                          self.stringValsOfYEC =  self.stringValsOfYEC + str(val) + ','             
                          
            b = 0
            for itemZ in ZEC:                      
               # if (itemZ ==  ZEC[-1:]).all():   
                b = b + 1   
                t = len(ZEC)    
                if  b ==  len(ZEC):      
                  c = 0 
                  self.stringValsOfZEC =  self.stringValsOfZEC + '['                 
                  for val in itemZ:  
                    c = c + 1               
                    if c == len(itemZ):                
                          self.stringValsOfZEC =   self.stringValsOfZEC + str(val) +']'       
                    else:    
                          self.stringValsOfZEC =  self.stringValsOfZEC + str(val) + ','       
                          
                else:
                  c = 0 
                  self.stringValsOfZEC =  self.stringValsOfZEC + '['                           
                  for val in itemZ: 
                    c = c + 1
                    if c == len(itemZ):                
                          self.stringValsOfZEC =   self.stringValsOfZEC + str(val) +'],'       
                    else:    
                          self.stringValsOfZEC =  self.stringValsOfZEC + str(val) + ',' 
      
      
        if createdata == 1:
            if "magnetostriction" in filename:
                 SC = []
                 SC= S
                 b = 0
                 
                 for itemSC in SC:                      
                    b = b + 1   
                    t = len(S)    
                    if  b ==  len(S):      
                      c = 0 
                      self.surfacecolorMagnetostriction =  self.surfacecolorMagnetostriction + '['                 
                      for val in itemSC:  
                        c = c + 1               
                        if c == len(itemSC):                
                              self.surfacecolorMagnetostriction =   self.surfacecolorMagnetostriction + str(val) +']'       
                        else:    
                              self.surfacecolorMagnetostriction =  self.surfacecolorMagnetostriction + str(val) + ','       
                    else:
                      c = 0 
                      self.surfacecolorMagnetostriction =  self.surfacecolorMagnetostriction + '['                           
                      for val in itemSC: 
                        c = c + 1
                        if c == len(itemSC):                
                              self.surfacecolorMagnetostriction =   self.surfacecolorMagnetostriction + str(val) +'],'       
                        else:    
                              self.surfacecolorMagnetostriction =  self.surfacecolorMagnetostriction + str(val) + ','   
                 
                 self.surfacecolorMagnetostriction =  '['  + self.surfacecolorMagnetostriction + ']' 
            else: 
                  lx=len(ZEC)
                  ly=len(ZEC[0])
                  sc='['
                  out=[]
                  for i in xrange(lx):
                        temp = []
                        sc= sc + '['
                        for j in xrange( ly):
                            res= self.dist_origin(XEC[i][j], YEC[i][j], ZEC[i][j])
                            #print res
                            if j ==( ly -1): 
                                if i == ( lx -1): 
                                    sc= sc + str(res) + ']'  
                                else:
                                    sc= sc + str(res) + '],'  
                                #print sc
                            else:
                                  sc= sc + str(res) + ','  
            
                   
                  sc= sc + ']'     
                  self.surfacecolorMagnetostriction =sc  
              
      