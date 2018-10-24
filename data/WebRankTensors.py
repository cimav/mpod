'''
Created on Dec 1, 2014

@author: admin
'''

from time import gmtime, strftime
#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.pyplot as plt
import plotly.plotly as py
from plotly.graph_objs import *
import numpy as np
#from pylab import *
import sys
from smtpd import parseargs
from stlwrite import *
import os.path
import math
import time
import threading


 
class RankTensors():
   def __init__(self):
    self.A = 1
    self.color = None 
    self.dataS = None
    self.layoutS = None
    self.stringValsOfXEC = ''
    self.stringValsOfYEC = ''
    self.stringValsOfZEC = ''
    self.stringValsOfXEC2 = ''
    self.stringValsOfYEC2 = ''
    self.stringValsOfZEC2 = ''
    self.colorscale = ""
    self.surfacecolorSecondRankTensor=''
    self.surfacecolorSecondRankTensorRotated =""
    self.surfacecolorThirdRankTensor=''
    self.surfacecolorThirdRankTensorRotated=''
    self.surfacecolorFourthRankTensor=''
    self.lock = threading.Lock()    
       
   def dist_origin(self,x, y, z):
        return math.sqrt((1.0 * x)**2 + (1.0 * y)**2 + (1.0 * z)**2)
     
     
   def stlCreator(self,createstl,filename,stldir,XEC,YEC,ZEC):
        start = int(time.time())
        self.lock.acquire()  
        
        scale = 100
        if createstl == 1: 
            fl= filename 
            #stl_dir = ".\\media\\stlfiles\\"      
            filepath=os.path.join(stldir, fl)
            stlw = STLUtil()
            tri = stlw.stlwrite(filepath,XEC,YEC,ZEC,scale)
            stlw
          
        self.lock.release()  
        end = str(int(time.time()) - start)
        print filename + " created in "+ end + " seconds"
                                           
   def SecondRankTensor(self,d11, d12, d13, d21, d22, d23, d31, d32, d33, Color,filename,res,stl_dir,createstl,createdata):
        filename= filename
        #self.Res = res
        stldir=stl_dir
        createstl= createstl
        createdata = createdata
        color = Color 
        phi=None
        beta=None
        if res == 1:
              phi, beta = np.mgrid[0:np.pi:45j,0:2*np.pi:90j]
        elif res == 2:
              phi, beta = np.mgrid[0:np.pi:90j,0:2*np.pi:180j] 
        elif res == 3:
              phi, beta = np.mgrid[0:np.pi:180j,0:2*np.pi:360j]
    
        x= np.sin(phi) * np.cos(beta)
        y= np.sin(phi) * np.sin(beta)
        z= np.cos(phi) * np.ones((np.shape(beta)))
         
        E=d11*(x**2) + d22*(y**2) + d33*(z**2) + (x*y)*(d12+d21) + (x*z)*(d13+d31) + (y*z)*(d23+d32)
    
        XEC=E*x
        YEC=E*y
        ZEC=E*z
    
        """scale = 100
        if createstl == 1: 
              fl= filename 
              #stl_dir = ".\\media\\stlfiles\\"      
              filepath=os.path.join(stldir, fl)
              stlw = STLUtil()
              tri = stlw.stlwrite(filepath,XEC,YEC,ZEC,scale)
              del stlw"""
              
        t = threading.Thread(target=self.stlCreator,args=(createstl,filename,stldir,XEC,YEC,ZEC))
        t.start()
          
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
          if "magnetoelectric" in filename or 'thermalexpansion' in filename:
             SC = []
             SC= E
             b = 0
             
             for itemSC in SC:                      
                b = b + 1   
                t = len(E)    
                if  b ==  len(E):      
                  c = 0 
                  self.surfacecolorSecondRankTensor =  self.surfacecolorSecondRankTensor + '['                 
                  for val in itemSC:  
                    c = c + 1               
                    if c == len(itemSC):                
                          self.surfacecolorSecondRankTensor =   self.surfacecolorSecondRankTensor + str(val) +']'       
                    else:    
                          self.surfacecolorSecondRankTensor =  self.surfacecolorSecondRankTensor + str(val) + ','       
                else:
                  c = 0 
                  self.surfacecolorSecondRankTensor =  self.surfacecolorSecondRankTensor + '['                           
                  for val in itemSC: 
                    c = c + 1
                    if c == len(itemSC):                
                          self.surfacecolorSecondRankTensor =   self.surfacecolorSecondRankTensor + str(val) +'],'       
                    else:    
                          self.surfacecolorSecondRankTensor =  self.surfacecolorSecondRankTensor + str(val) + ','   
             
             self.surfacecolorSecondRankTensor =  '['  + self.surfacecolorSecondRankTensor + ']' 
             
             
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
              self.surfacecolorSecondRankTensor =sc 
              
   def SecondRankTensorRotated(self,valuearrayrotated, Color,filename,res,stl_dir,createstl,createdata):
        d11=float(valuearrayrotated[0])
        d12=float(valuearrayrotated[1])
        d13=float(valuearrayrotated[2])
        d21=float(valuearrayrotated[3])
        d22=float(valuearrayrotated[4])
        d23=float(valuearrayrotated[5])
        d31=float(valuearrayrotated[6])
        d32=float(valuearrayrotated[7])
        d33=float(valuearrayrotated[8])
        self.surfacecolorSecondRankTensor =""
        
        filename= filename
        #self.Res = res
        stldir=stl_dir
        createstl= createstl
        createdata = createdata
        color = Color 
        phi=None
        beta=None
        if res == 1:
            phi, beta = np.mgrid[0:np.pi:45j,0:2*np.pi:90j]
        elif res == 2:
            phi, beta = np.mgrid[0:np.pi:90j,0:2*np.pi:180j] 
        elif res == 3:
            phi, beta = np.mgrid[0:np.pi:180j,0:2*np.pi:360j]
    
        x= np.sin(phi) * np.cos(beta)
        y= np.sin(phi) * np.sin(beta)
        z= np.cos(phi) * np.ones((np.shape(beta)))
         
        E=d11*(x**2) + d22*(y**2) + d33*(z**2) + (x*y)*(d12+d21) + (x*z)*(d13+d31) + (y*z)*(d23+d32)
    
        XEC=E*x
        YEC=E*y
        ZEC=E*z
    
        """scale = 100
        if createstl == 1: 
              fl= filename 
              #stl_dir = ".\\media\\stlfiles\\"      
              filepath=os.path.join(stldir, fl)
              stlw = STLUtil()
              tri = stlw.stlwrite(filepath,XEC,YEC,ZEC,scale)
              del stlw"""
              
        t = threading.Thread(target=self.stlCreator,args=(createstl,filename,stldir,XEC,YEC,ZEC))
        t.start()
          
        if createdata == 1:
              b=0
              for itemX in XEC:                      
                b = b + 1  
                if  b ==  len(XEC):                
                  c = 0 
                  self.stringValsOfXEC2 =  self.stringValsOfXEC2 + '['                 
                  for val in itemX:  
                    c = c + 1               
                    if c == len(itemX):                
                          self.stringValsOfXEC2 =   self.stringValsOfXEC2 + str(val) +']'       
                    else:    
                          self.stringValsOfXEC2 =  self.stringValsOfXEC2 + str(val) + ','       
                          
                else:
                  c = 0 
                  self.stringValsOfXEC2 =  self.stringValsOfXEC2 + '['                           
                  for val in itemX: 
                    c = c + 1
                    if c == len(itemX):                
                          self.stringValsOfXEC2 =   self.stringValsOfXEC2 + str(val) +'],'       
                    else:    
                          self.stringValsOfXEC2 =  self.stringValsOfXEC2 + str(val) + ',' 
              
              b=0            
              for itemY in YEC:                      
                b = b + 1  
                if  b ==  len(YEC):                 
                  c = 0 
                  self.stringValsOfYEC2 =  self.stringValsOfYEC2 + '['                 
                  for val in itemY:  
                    c = c + 1               
                    if c == len(itemY):                
                          self.stringValsOfYEC2 =   self.stringValsOfYEC2 + str(val) +']'       
                    else:    
                          self.stringValsOfYEC2 =  self.stringValsOfYEC2 + str(val) + ','       
                          
                else:
                  c = 0 
                  self.stringValsOfYEC2 =  self.stringValsOfYEC2 + '['                           
                  for val in itemY: 
                    c = c + 1
                    if c == len(itemY):                
                          self.stringValsOfYEC2 =   self.stringValsOfYEC2 + str(val) +'],'       
                    else:    
                          self.stringValsOfYEC2 =  self.stringValsOfYEC2 + str(val) + ','             
                          
              b = 0
              for itemZ in ZEC:                      
               # if (itemZ ==  ZEC[-1:]).all():   
                b = b + 1   
                t = len(ZEC)    
                if  b ==  len(ZEC):      
                  c = 0 
                  self.stringValsOfZEC2 =  self.stringValsOfZEC2 + '['                 
                  for val in itemZ:  
                    c = c + 1               
                    if c == len(itemZ):                
                          self.stringValsOfZEC2 =   self.stringValsOfZEC2 + str(val) +']'       
                    else:    
                          self.stringValsOfZEC2 =  self.stringValsOfZEC2 + str(val) + ','       
                          
                else:
                  c = 0 
                  self.stringValsOfZEC2 =  self.stringValsOfZEC2 + '['                           
                  for val in itemZ: 
                    c = c + 1
                    if c == len(itemZ):                
                          self.stringValsOfZEC2 =   self.stringValsOfZEC2 + str(val) +'],'       
                    else:    
                          self.stringValsOfZEC2 =  self.stringValsOfZEC2 + str(val) + ','                    
     
        
        if createdata == 1:
          if "magnetoelectric" in filename or 'thermalexpansion' in filename:
             SC = []
             SC= E
             b = 0
             
             for itemSC in SC:                      
                b = b + 1   
                t = len(E)    
                if  b ==  len(E):      
                  c = 0 
                  self.surfacecolorSecondRankTensor =  self.surfacecolorSecondRankTensor + '['                 
                  for val in itemSC:  
                    c = c + 1               
                    if c == len(itemSC):                
                          self.surfacecolorSecondRankTensor =   self.surfacecolorSecondRankTensor + str(val) +']'       
                    else:    
                          self.surfacecolorSecondRankTensor =  self.surfacecolorSecondRankTensor + str(val) + ','       
                else:
                  c = 0 
                  self.surfacecolorSecondRankTensor =  self.surfacecolorSecondRankTensor + '['                           
                  for val in itemSC: 
                    c = c + 1
                    if c == len(itemSC):                
                          self.surfacecolorSecondRankTensor =   self.surfacecolorSecondRankTensor + str(val) +'],'       
                    else:    
                          self.surfacecolorSecondRankTensor =  self.surfacecolorSecondRankTensor + str(val) + ','   
             
             self.surfacecolorSecondRankTensorRotated =  '['  + self.surfacecolorSecondRankTensor + ']' 
             
             
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
              self.surfacecolorSecondRankTensorRotated =sc
     
   def ThirdRankTensordg (self,d11,d12,d13,d14,d15,d16,d21,d22,d23,d24,d25,d26,d31,d32,d33,d34,d35,d36,Color,filename,res,stl_dir,createstl,createdata):
        filename= filename
        #self.Res = res
        stldir=stl_dir
        createstl= createstl
        createdata = createdata
        color = Color 
        
        phi=None
        beta=None
        if res == 1:
          phi, beta = np.mgrid[0:np.pi:45j,0:np.pi:90j]
        elif res == 2:
          phi, beta = np.mgrid[0:np.pi:90j,0:np.pi:180j] 
        elif res == 3:
          phi, beta = np.mgrid[0:np.pi:180j,0:np.pi:360j]
              
              
    
        x = np.sin(phi)*np.cos(beta)
        y = np.sin(phi)*np.sin(beta)
        z = np.cos(phi)
    
        E1=d11*x*x*x + (d12+d26)*x*y*y + (d13+d35)*x*z*z + (d14+d25+d36)*x*y*z + (d15+d31)*x*x*z + (d16+d21)*x*x*y
        E2=d22*y*y*y + (d23+d34)*y*z*z + (d24+d32)*y*y*z
        E3=d33*z*z*z 
    
        E=E1+E2+E3
    
        XEC=E*x
        YEC=E*y
        ZEC=E*z
    
        """scale = 100
        if createstl == 1: 
          fl= filename 
          #stl_dir = ".\\media\\stlfiles\\"      
          filepath=os.path.join(stldir, fl)
          stlw = STLUtil()
          tri = stlw.stlwrite(filepath,XEC,YEC,ZEC,scale)
          del stlw"""
          
        t = threading.Thread(target=self.stlCreator,args=(createstl,filename,stldir,XEC,YEC,ZEC))
        t.start()
      
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
          self.surfacecolorThirdRankTensor =sc 

   def ThirdRankTensoreh (self,d11,d12,d13,d14,d15,d16,d21,d22,d23,d24,d25,d26,d31,d32,d33,d34,d35,d36,Color,filename,res,stl_dir,createstl,createdata):
        filename= filename
        #self.Res = res
        stldir=stl_dir
        createstl= createstl
        createdata = createdata
        color = Color 
        
        phi=None
        beta=None
        if res == 1:
          phi, beta = np.mgrid[0:np.pi:45j,0:np.pi:90j]
        elif res == 2:
          phi, beta = np.mgrid[0:np.pi:90j,0:np.pi:180j] 
        elif res == 3:
          phi, beta = np.mgrid[0:np.pi:180j,0:np.pi:360j]
              
              
    
        x = np.sin(phi)*np.cos(beta)
        y = np.sin(phi)*np.sin(beta)
        z = np.cos(phi)
    
        E1=d11*x*x*x + (d12+d26)*x*y*y + (d13+d35)*x*z*z + (d14+d25+d36)*x*y*z + (d15+d31)*x*x*z + (d16+d21)*x*x*y
        E2=d22*y*y*y + (d23+d34)*y*z*z + (d24+d32)*y*y*z
        E3=d33*z*z*z 
    
        E=E1+E2+E3
    
        XEC=E*x
        YEC=E*y
        ZEC=E*z
    
        """scale = 100
        if createstl == 1: 
          fl= filename 
          #stl_dir = ".\\media\\stlfiles\\"      
          filepath=os.path.join(stldir, fl)
          stlw = STLUtil()
          tri = stlw.stlwrite(filepath,XEC,YEC,ZEC,scale)
          del stlw"""
          
        t = threading.Thread(target=self.stlCreator,args=(createstl,filename,stldir,XEC,YEC,ZEC))
        t.start()
      
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
          self.surfacecolorThirdRankTensor =sc 
          
                                 
   def FourthRankTensor (self,s11, s12, s13, s14, s15, s16, s21, s22, s23, s24, s25, s26, s31, s32, s33, s34, s35, s36, s41, s42, s43, s44, s45, s46, s51, s52, s53, s54, s55, s56, s61, s62, s63, s64, s65, s66, Color,filename,res,stl_dir,createstl,createdata):
    
        filename= filename
          #self.Res = res
        stldir=stl_dir
        createstl= createstl
        createdata = createdata
        color = Color
        #phi, beta = np.mgrid[0:np.pi:180j,0:2*np.pi:360j]
        
        
        phi=None
        beta=None
        if res == 1:
              phi, beta = np.mgrid[0:np.pi:45j,0:2*np.pi:90j]
        elif res == 2:
              phi, beta = np.mgrid[0:np.pi:90j,0:2*np.pi:180j] 
        elif res == 3:
              phi, beta = np.mgrid[0:np.pi:180j,0:2*np.pi:360j]
              
              
        x = np.sin(phi)*np.cos(beta)
        y = np.sin(phi)*np.sin(beta)
        z = np.cos(phi)
    
        if s21==0 and s31==0 and s32==0 and s41==0 and s42==0 and s43==0 and s51==0 and s52==0 and s53==0 and s54==0 and s61==0 and s62==0 and s63==0 and s64==0 and s65==0:
            S1=s11*(x**4) + 2*s12*(x**2)*(y**2) + 2*s13*(x**2)*(z**2) + 2*s14*(x**2)*y*z + 2*s15*(x**3)*z + 2*s16*(x**3)*y
            S2=s22*(y**4) + 2*s23*(y**2)*(z**2) + 2*s24*(y**3)*z + 2*s25*x*(y**2)*z + 2*s26*x*(y**3)
            S3=s33*(z**4) + 2*s34*y*(z**3) + 2*s35*x*(z**3) + 2*s36*x*y*(z**2)
            S4=s44*(y**2)*(z**2) + 2*s45*x*y*(z**2) + 2*s46*x*(y**2)*z
            S5=s55*(x**2)*(z**2) + 2*s56*(x**2)*y*z + s66*(x**2)*(y**2)
            
        else:
            S1=s11*(x**4) + (x**2)*(y**2)*(s12+s21) + (x**2)*(z**2)*(s13+s31) + (x**2)*y*z*(s14+s41) + (x**3)*z*(s15+s51) + (x**3)*y*(s16+s61)
            S2=s22*(y**4) + (y**2)*(z**2)*(s23+s32) + (y**3)*z *(s24+s42) + x*(y**2)*z*(s25+s52) + x*(y**3)*(s26+s62)
            S3=s33*(z**4) + y*(z**3)*(s34+s43) + x*(z**3)*(s35+s53) + x*y*(z**2)*(s36+s63)
            S4=s44*(y**2)*(z**2) + x*y*(z**2)*(s45+s54) + x*(y**2)*z*(s46+s64)
            S5=s55*(x**2)*(z**2) + (x**2)*y*z*(s56+s65) + s66*(x**2)*(y**2)
    
        S=S1+S2+S3+S4+S5
    
        XEC=S*x
        YEC=S*y
        ZEC=S*z
        
        
    
        """scale = 100
        if createstl == 1: 
              fl= filename 
              #stl_dir = ".\\media\\stlfiles\\"      
              filepath=os.path.join(stldir, fl)
              stlw = STLUtil()
              tri = stlw.stlwrite(filepath,XEC,YEC,ZEC,scale)
              del stlw"""
              
        t = threading.Thread(target=self.stlCreator,args=(createstl,filename,stldir,XEC,YEC,ZEC))
        t.start()
              
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
          self.surfacecolorFourthRankTensor =sc     
                  
  
       