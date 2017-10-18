'''
Created on Feb 8, 2016

@author: Jorge Alberto Torres Acosta
'''
#from matplotlib.tri import Triangulation
import numpy as np
from numpy import size
#import matplotlib.pyplot as plt
import datetime


    
class STLUtil:   
  def __init__(self):
      self.fn=None
      self.points = []
      self.triangles = []
      self.undertriangles = []
      self.vertices= []
      self.dervertices= []
      self.mainnormals= []
      self.undernormals= []
      self.pointX= []
      self.pointY= []
      self.pointZ= []
      
      self.undernormalssolid= []
      
  def stlwrite(self,filename, x,y,z,scale):
      
      if z.ndim != 2:
          error = 'Variable z must be a 2-dimensional array'

      #xec= x.ravel()
      #yec= y.ravel()
      #zec= z.ravel()
      


      
      #vertices = np.array([[x[i], y[i], z[i]] for i in range(len(z))])
      #print np.asarray(vertices).shape
      '''for i in range(0, len(vertices)):
         print vertices[i]'''

      #faces = Triangulation(xec,yec)

      fid = open(filename,'w') 
      if fid == None:
        fid.write('Unable to write to %s' % (filename))
        
      mode='ascii'
      title_str = "STL generated by  stlwrite.py %s " % (datetime.datetime.now().time())
      title_str = title_str + "\n"
      
      if  mode=='ascii':            
            fid.write( "solid %s\n" % (title_str))
     
      scl = 100
      nfacets = 0  
     
      for i in range(len(z)-1):
         for j in range(len(z[i])-1):
            p1 = [x[i,j],    y[i,j],    z[i,j]]
            p2 = [x[i,j+1],   y[i,j+1],   z[i,j+1]]
            p3 = [x[i+1,j+1], y[i+1,j+1], z[i+1,j+1]]
            
            self.vertices.append(np.array([p1[0],p1[1],p1[2]]))
            self.vertices.append(np.array([p2[0],p2[1],p2[2]]))
            self.vertices.append(np.array([p3[0],p3[1],p3[2]]))
            
            self.triangles.append([p1,p2,p3])
            self.pointX.append(p1[0])
            self.pointX.append(p2[0])
            self.pointX.append(p3[0])
            
            self.pointY.append(p1[1])
            self.pointY.append(p2[1])
            self.pointY.append(p3[1])
            
            self.pointZ.append(p1[2])
            self.pointZ.append(p2[2])
            self.pointZ.append(p3[2])
            
            '''scale1= map(lambda p: p * scale, p1)         
            scale2=map(lambda p: p * scale, p2)  
            scale3=map(lambda p: p * scale, p3)'''
            
            val = local_write_facet(self,fid,p1,p2,p3,mode,1);
            #val = local_write_facet(self,fid,scale1,scale2,scale3,mode,1);
            nfacets = nfacets + val;
            
   

            p1 = [x[i+1,j+1], y[i+1,j+1], z[i+1,j+1]]
            p2 = [x[i+1,j],   y[i+1,j],   z[i+1,j]]
            p3 = [x[i,j],     y[i,j],     z[i,j]] 
            
            self.vertices.append(np.array([p1[0],p1[1],p1[2]]))
            self.vertices.append(np.array([p2[0],p2[1],p2[2]]))
            self.vertices.append(np.array([p3[0],p3[1],p3[2]]))
            
            self.triangles.append([p1,p2,p3])
            
            self.pointX.append(p1[0])
            self.pointX.append(p2[0])
            self.pointX.append(p3[0])
            
            self.pointY.append(p1[1])
            self.pointY.append(p2[1])
            self.pointY.append(p3[1])
            
            self.pointZ.append(p1[2])
            self.pointZ.append(p2[2])
            self.pointZ.append(p3[2])
            
            
            '''scale1= map(lambda p: p * scale, p1)         
            scale2=map(lambda p: p * scale, p2)  
            scale3=map(lambda p: p * scale, p3)'''
            val = local_write_facet(self,fid,p1,p2,p3,mode,1);
            #val = local_write_facet(self,fid,scale1,scale2,scale3,mode,1);
            nfacets = nfacets + val;           
            

            

      print   str( nfacets  )    
      print  np.asarray(self.vertices).shape   
             
      
      if  mode=='ascii':       
        fid.write( "endsolid %s\n"% (title_str))

      fid.close()

      return  0
 
def   local_write_facet(self,fid,p1,p2,p3,mode,su):
    num = 0;
    if any( np.isnan(p1) | np.isnan(p2) | np.isnan(p3) ):
        num = 0;
        return;
    else:
        num = 1;
        if su ==1:
            n = local_find_normal(p1,p2,p3);
            self.mainnormals.append(n)
        else:
            n = local_find_normal(p1,p2,p3);
            self.undernormals.append(n)
            
        if su ==3:
            n = local_find_normal(p1,p2,p3);
            self.undernormalssolid.append(n)

            

        #undernormals= []
        
        if mode=='ascii' :
            
            fid.write( "facet normal %.7E %.7E %.7E\n" %( n[0],n[1],n[2] ) )
            fid.write( "  outer loop\n");        
            fid.write( "    vertex %.7E %.7E %.7E\n" %(  p1[0],p1[1],p1[2]))
            fid.write( "    vertex %.7E %.7E %.7E\n" %(  p2[0],p2[1],p2[2]))
            fid.write( "    vertex %.7E %.7E %.7E\n" %(  p3[0],p3[1],p3[2]))
            fid.write( "  endloop\n")
            fid.write( "endfacet\n")
            
        '''else:
            
            fwrite(fid,n,'float32');
            fwrite(fid,p1,'float32');
            fwrite(fid,p2,'float32');
            fwrite(fid,p3,'float32');
            fwrite(fid,0,'int16');  % unused'''
            
     
    return num
 
 
def  local_find_normal(p1,p2,p3):
   
  v1t =None 
  v2t =None
  v3t =None
  for i in range(len(p2)): 
    if i==0:
     v1t= p2[i]-p1[i]
    if i==1:
     v2t= p2[i]-p1[i]
    if i==2:
     v3t= p2[i]-p1[i]  
  
  v1 = [v1t,v2t,v3t]
        

  
  #v1 = p2-p1;
  
  v1t =None 
  v2t =None
  v3t =None
  for i in range(len(p3)): 
    if i==0:
     v1t= p3[i]-p1[i]
    if i==1:
     v2t= p3[i]-p1[i]
    if i==2:
     v3t= p3[i]-p1[i]  
  
  v2 = [v1t,v2t,v3t]

  #v2 = p3-p1;
  v3 = np.cross(v1,v2);
  v3t1=v3[0]
  v3t2=v3[1]
  v3t3=v3[2]
  if v3t1 != 0.0 and v3t2 != 0.0  and v3t3 != 0.0 :
     n = v3 / np.sqrt(sum(v3 * v3));
  else:
     n= [0.0,0.0,0.0];

  
  
  
  return n
 

    
