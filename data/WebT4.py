'''
Created on Dec 1, 2014

@author: admin
'''

#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.pyplot as plt
import plotly.plotly as py
from plotly.graph_objs import *
import numpy as np
#from pylab import *
import sys
from stlwrite import *
import os.path
import math
import threading
from django.utils.text import force_unicode
import time

 

 

class ComplianceT4():
   def __init__(self):
   
       
      self.A = 1
      self.matrixS=None
      self.dataS = None
      self.layoutS = None
      self.stringValsOfXEC = ''
      self.stringValsOfYEC = ''
      self.stringValsOfZEC = ''
      
      self.stringValsOfXEC2 = ''
      self.stringValsOfYEC2 = ''
      self.stringValsOfZEC2 = ''
      self.youngXEC=None
      self.youngYEC=None
      self.youngZEC=None
      #self.Res=None;   'resolucion de la superficie'
      
      self.colorscale = ""
      self.surfacecolorcompliance=''
      self.surfacecolorYoungModulus=''
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
    
      
   def Compliance(self,s11, s12, s13, s14, s15, s16, s21, s22, s23, s24, s25, s26, s31, s32, s33, s34, s35, s36, s41, s42, s43, s44, s45, s46, s51, s52, s53, s54, s55, s56, s61, s62, s63, s64, s65, s66,Color,filename,res,stl_dir,createstl,createdata):
      self.matrixS=np.matrix([[s11,s12,s13,s14,s15,s16],[s21,s22,s23,s24,s25,s26],[s31,s32,s33,s34,s35,s36],[s41,s42,s43,s44,s45,s46],[s51,s52,s53,s54,s55,s56],[s61,s62,s63,s64,s65,s66]])

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
      
      
      x = np.sin(phi)*np.cos(beta)
      y = np.sin(phi)*np.sin(beta)
      z = np.cos(phi)

      S1=s11*(x**4) + 2*s12*(x**2)*(y**2) + 2*s13*(x**2)*(z**2) + 2*s14*(x**2)*y*z + 2*s15*(x**3)*z + 2*s16*(x**3)*y
      S2=s22*(y**4) + 2*s23*(y**2)*(z**2) + 2*s24*(y**3)*z + 2*s25*x*(y**2)*z + 2*s26*x*(y**3)
      S3=s33*(z**4) + 2*s34*y*(z**3) + 2*s35*x*(z**3) + 2*s36*x*y*(z**2)
      S4=s44*(y**2)*(z**2) + 2*s45*x*y*(z**2) + 2*s46*x*(y**2)*z
      S5=s55*(x**2)*(z**2) + 2*s56*(x**2)*y*z + s66*(x**2)*(y**2)

      S=S1+S2+S3+S4+S5

      #compliance
      XEC=S*x
      YEC=S*y
      ZEC=S*z

      


      
      t = threading.Thread(target=self.stlCreator,args=(createstl,filename,stldir,XEC,YEC,ZEC))
      t.start()
    
      """scale = 100
      if createstl == 1: 
          fl= filename 
          #stl_dir = ".\\media\\stlfiles\\"      
          filepath=os.path.join(stldir, fl)
          stlw = STLUtil()
          tri = stlw.stlwrite(filepath,XEC,YEC,ZEC,scale)
          del stlw"""
      
      
      if createdata == 1:
          xcs=[]
          b=0
          for itemX in XEC: 
            xsctemp=[]                     
            b = b + 1  
            if  b ==  len(XEC):                
              c = 0 
              self.stringValsOfXEC =  self.stringValsOfXEC + '['                 
              for val in itemX:  
                c = c + 1               
                if c == len(itemX):                
                      xsctemp.append(val)    
                      self.stringValsOfXEC =   self.stringValsOfXEC + str(val) +']'       
                else:    
                      xsctemp.append(val)    
                      self.stringValsOfXEC =  self.stringValsOfXEC + str(val) + ','       
                      
            else:
              c = 0 
              self.stringValsOfXEC =  self.stringValsOfXEC + '['                           
              for val in itemX: 
                c = c + 1
                if c == len(itemX):      
                      xsctemp.append(val)              
                      self.stringValsOfXEC =   self.stringValsOfXEC + str(val) +'],'       
                else: 
                      xsctemp.append(val)       
                      self.stringValsOfXEC =  self.stringValsOfXEC + str(val) + ',' 
        
          xcs.append(xsctemp)
          
          ycs=[]
          b=0            
          for itemY in YEC:       
            ysctemp=[]               
            b = b + 1  
            if  b ==  len(YEC):                 
              c = 0 
              self.stringValsOfYEC =  self.stringValsOfYEC + '['                 
              for val in itemY:  
                c = c + 1               
                if c == len(itemY):   
                      ysctemp.append(val)             
                      self.stringValsOfYEC =   self.stringValsOfYEC + str(val) +']'       
                else:    
                      ysctemp.append(val)
                      self.stringValsOfYEC =  self.stringValsOfYEC + str(val) + ','       
                      
            else:
              c = 0 
              self.stringValsOfYEC =  self.stringValsOfYEC + '['                           
              for val in itemY: 
                c = c + 1
                if c == len(itemY):       
                      ysctemp.append(val)        
                      self.stringValsOfYEC =   self.stringValsOfYEC + str(val) +'],'       
                else:    
                      ysctemp.append(val)
                      self.stringValsOfYEC =  self.stringValsOfYEC + str(val) + ','        
                           
          ycs.append(ysctemp)           
                      
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
              self.surfacecolorcompliance =sc     


    

   def YoungModulus(self,s11, s12, s13, s14, s15, s16, s21, s22, s23, s24, s25, s26, s31, s32, s33, s34, s35, s36, s41, s42, s43, s44, s45, s46, s51, s52, s53, s54, s55, s56, s61, s62, s63, s64, s65, s66,Color,filename,res,stl_dir,createstl,createdata):   
 
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
      
      
      x = np.sin(phi)*np.cos(beta)
      y = np.sin(phi)*np.sin(beta)
      z = np.cos(phi)

      S1=s11*(x**4) + 2*s12*(x**2)*(y**2) + 2*s13*(x**2)*(z**2) + 2*s14*(x**2)*y*z + 2*s15*(x**3)*z + 2*s16*(x**3)*y
      S2=s22*(y**4) + 2*s23*(y**2)*(z**2) + 2*s24*(y**3)*z + 2*s25*x*(y**2)*z + 2*s26*x*(y**3)
      S3=s33*(z**4) + 2*s34*y*(z**3) + 2*s35*x*(z**3) + 2*s36*x*y*(z**2)
      S4=s44*(y**2)*(z**2) + 2*s45*x*y*(z**2) + 2*s46*x*(y**2)*z
      S5=s55*(x**2)*(z**2) + 2*s56*(x**2)*y*z + s66*(x**2)*(y**2)

      S=S1+S2+S3+S4+S5

      #compliance
      X=S*x
      Y=S*y
      Z=S*z

      #young modulus
      E = 1 / S
      XEC = E * x
      YEC = E * y
      ZEC = E * z
      

      
      b=0
      for itemX in XEC:                      
        b = b + 1  
        if  b ==  len(YEC):                
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


      """
      scale = 100
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
          self.surfacecolorYoungModulus =sc
         
          

 

class StiffnessT4():
   def __init__(self):
    self.error = None
    self.A = 1
    self.matrixS=None
    self.dataS = None
    self.layoutS = None
    self.stringValsOfXEC = ''
    self.stringValsOfYEC = ''
    self.stringValsOfZEC = ''
  
    self.stringValsOfXEC2 = ''
    self.stringValsOfYEC2 = ''
    self.stringValsOfZEC2 = ''
    self.youngXEC=None
    self.youngYEC=None
    self.youngZEC=None
    
    self.colorscale = ""     
    self.surfacecolorstiffness=''
    self.surfacecolorYoungModulus=''
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
        
       
   def Stiffness(self,c11, c12, c13, c14, c15, c16, c21, c22, c23, c24, c25, c26, c31, c32, c33, c34, c35, c36, c41, c42, c43, c44, c45, c46, c51, c52, c53, c54, c55, c56, c61, c62, c63, c64, c65, c66,Color,filename,res,stl_dir,createstl,createdata):  

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

      
      c = [[c11,c12,c13,c14,c15,c16],
      [c12,c22,c23,c24,c25,c26],
      [c13,c23,c33,c34,c35,c36],
      [c14,c24,c34,c44,c45,c46],
      [c15,c25,c35,c45,c55,c56],
      [c16,c26,c36,c46,c56,c66]]
      
      """
      c = [[223.0, 109.0, 102.0, 0.0, 0.0, 0.0], 
            [109.0, 223.0, 102.0, 0.0, 0.0, 0.0], 
            [102.0, 102.0, 240.0, 0.0, 0.0, 0.0], 
            [0.0, 0.0, 0.0, 121.0, 0.0, 0.0], 
            [0.0, 0.0, 0.0, 0.0, 121.0, 0.0], 
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]]
      """
      

      #fordisplay=np.matrix([[c11,c12,c13,c14,c15,c16],[c21,c22,c23,c24,c25,c26],[c31,c32,c33,c34,c35,c36],[c41,c42,c43,c44,c45,c46],[c51,c52,c53,c54,c55,c56],[c61,c62,c63,c64,c65,c66]])
      s = None
      try:
        s = np.linalg.inv(c)
      except Exception as e:
        self.error = 'Internal error occurred, consult technical support (when calculating the inverse of a matrix of Single-crystal)'
        return

      s11=s[0,0]; s12=s[0,1]; s13=s[0,2]; s14=s[0,3]; s15=s[0,4]; s16=s[0,5]
      s22=s[1,1]; s23=s[1,2]; s24=s[1,3]; s25=s[1,4]; s26=s[1,5]
      s33=s[2,2]; s34=s[2,3]; s35=s[2,4]; s36=s[2,5]
      s44=s[3,3]; s45=s[3,4]; s46=s[3,5]
      s55=s[4,4];s56=s[4,5]
      s66=s[5,5]

      #phi, beta = np.mgrid[0:np.pi:180j,0:2*np.pi:360j]

      x= np.sin(phi) * np.cos(beta)
      y= np.sin(phi) * np.sin(beta)
      z= np.cos(phi)

      S1=s11*(x**4) + 2*s12*(x**2)*(y**2) + 2*s13*(x**2)*(z**2) + 2*s14*(x**2)*y*z + 2*s15*(x**3)*z + 2*s16*(x**3)*y
      S2=s22*(y**4) + 2*s23*(y**2)*(z**2) + 2*s24*(y**3)*z + 2*s25*x*(y**2)*z + 2*s26*x*(y**3)
      S3=s33*(z**4) + 2*s34*y*(z**3) + 2*s35*x*(z**3) + 2*s36*x*y*(z**2)
      S4=s44*(y**2)*(z**2) + 2*s45*x*y*(z**2) + 2*s46*x*(y**2)*z
      S5=s55*(x**2)*(z**2) + 2*s56*(x**2)*y*z + s66*(x**2)*(y**2)
      """S4=4*s44*(y**2)*(z**2) + 2*s45*x*y*(z**2) + 2*s46*x*(y**2)*z
      S5=4*s55*(x**2)*(z**2) + 2*s56*(x**2)*y*z + 4*s66*(x**2)*(y**2)"""

      S=S1+S2+S3+S4+S5

      ''''E= 1.0/S
      XEC = E*x
      YEC = E*y
      ZEC = E*z'''

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
          self.surfacecolorstiffness=sc


    
    
   def YoungModulus(self,c11, c12, c13, c14, c15, c16, c21, c22, c23, c24, c25, c26, c31, c32, c33, c34, c35, c36, c41, c42, c43, c44, c45, c46, c51, c52, c53, c54, c55, c56, c61, c62, c63, c64, c65, c66,Color,filename,res,stl_dir,createstl,createdata):  

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

 
      c = [[c11,c12,c13,c14,c15,c16],
      [c12,c22,c23,c24,c25,c26],
      [c13,c23,c33,c34,c35,c36],
      [c14,c24,c34,c44,c45,c46],
      [c15,c25,c35,c45,c55,c56],
      [c16,c26,c36,c46,c56,c66]]

      s = np.linalg.inv(c)

      s11=s[0,0]; s12=s[0,1]; s13=s[0,2]; s14=s[0,3]; s15=s[0,4]; s16=s[0,5]
      s22=s[1,1]; s23=s[1,2]; s24=s[1,3]; s25=s[1,4]; s26=s[1,5]
      s33=s[2,2]; s34=s[2,3]; s35=s[2,4]; s36=s[2,5]
      s44=s[3,3]; s45=s[3,4]; s46=s[3,5]
      s55=s[4,4];s56=s[4,5]
      s66=s[5,5]

      #phi, beta = np.mgrid[0:np.pi:180j,0:2*np.pi:360j]

      x= np.sin(phi) * np.cos(beta)
      y= np.sin(phi) * np.sin(beta)
      z= np.cos(phi)

      S1=s11*(x**4) + 2*s12*(x**2)*(y**2) + 2*s13*(x**2)*(z**2) + 2*s14*(x**2)*y*z + 2*s15*(x**3)*z + 2*s16*(x**3)*y
      S2=s22*(y**4) + 2*s23*(y**2)*(z**2) + 2*s24*(y**3)*z + 2*s25*x*(y**2)*z + 2*s26*x*(y**3)
      S3=s33*(z**4) + 2*s34*y*(z**3) + 2*s35*x*(z**3) + 2*s36*x*y*(z**2)
      S4=s44*(y**2)*(z**2) + 2*s45*x*y*(z**2) + 2*s46*x*(y**2)*z
      S5=s55*(x**2)*(z**2) + 2*s56*(x**2)*y*z + s66*(x**2)*(y**2)

      S=S1+S2+S3+S4+S5

      E= 1.0/S
      XEC = E*x
      YEC = E*y
      ZEC = E*z

      '''XEC=S*x
      YEC=S*y
      ZEC=S*z'''
            
            
      scale = 100
       
      
      #stlw = STLUtil()
      #tri = stlw.stlwrite("ejemplo7StiffnessYoung.stl",XEC,YEC,ZEC,scale)
     
     
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
         
          self.surfacecolorYoungModulus =sc
          

   

        