'''
Created on 20/10/2018

@author: Jorge Alberto Torres Acosta
'''
from data.Utils import *
import re


class AttrDict(dict):
    def __getattr__(self, item):
        return self[item]

    def __dir__(self):
        return super().__dir__() + [str(k) for k in self.keys()]
    
class BaseTensor(object):
    '''
    classdocs
    '''

    def __init__(self, *args):
        '''
        Constructor
        '''
        
        self.requestdic = None or {}
        self.filename = None 
        self.filename1 = None 
        self.filename2 = None 
        self.filenames = {} 
        self.res = 1
        self.pathexist = 0
        self.stl_dir=''
        self.valuearrayrotated = None
        self.createsourface = None
        self.valij = AttrDict()
        self.valueij = AttrDict()
        self.color = 0;
        self.createstl = None
        self.createdata = 1
        self.filenameYoungModulus = None
        self.filen = ""
        self.jason_data = {} 
        self.jason_data_poly = {}  
        self.colorscale = ""
        
        if args:
            self.requestdic =  dict(args[0].iterlists())
            self.color  = requestPostCheck(self.requestdic,'color')
            
            if int(self.color[0]) == 0:
                self.colorscale='Jet';
            elif int(self.color[0]) == 1:
                self.colorscale='Hot';
            elif int(self.color[0]) == 2:
                self.colorscale='Cool'
            elif int(self.color[0])== 3:
                self.colorscale='Greys';

            
                
            for key, value in self.requestdic.iteritems():
                    v =  requestPostFilterToFloat(args[0],key,None,'value')
                    if v != None:
                        self.valueij[str(key)] = v
                        
                        
            self.valuearrayrotated  = requestPostCheck(self.requestdic,'valuearrayrotated')
             
            self.filen = requestPostCheck(self.requestdic,'filename')
            if  self.valuearrayrotated == None:
                self.filename = re.sub('[\s+]', '', self.filen[0])   
                if self.res == 1:
                    self.filenames['low'] =  [self.filename + "LowResolution" + ".stl",self.res]
                    self.filenames['lowyg'] =  [self.filename + "YoungModulusLowResolution" + ".stl" ,self.res]  
                if self.res  ==  2:
                    self.filenames['midle'] =  [self.filename + "MidleResolution" + ".stl",self.res]      
                    self.filenames['midleyg'] =  [self.filename + "MidleModulusLowResolution" + ".stl" ,self.res]  
                if self.res  ==  3:
                    self.filenames['high'] = [self.filename + "HighResolution" + ".stl",self.res]                 
                    self.filenames['highyg'] = [self.filename + "HighModulusLowResolution" + ".stl" ,self.res]   
                
            else:
                self.filename = re.sub('[\s+]', '', self.filen[0])   
                self.filename2 = re.sub('[\s+]', '', self.filen[0])   + "policrystal"
                
                if self.res  ==  1:
                    self.filenames['low'] =  [self.filename + "LowResolution" + ".stl",self.res]
                    self.filenames['lowyg'] =  [self.filename + "YoungModulusLowResolution" + ".stl" ,self.res]  
                    self.filenames['lowp'] =  [self.filename2 + "LowResolution" + ".stl",self.res]
                    self.filenames['lowygp'] =  [self.filename2 + "YoungModulusLowResolution" + ".stl" ,self.res]  
                
                if self.res  ==  2:
                    self.filenames['midle'] =  [self.filename + "MidleResolution" + ".stl",self.res]      
                    self.filenames['midleyg'] =  [self.filename + "MidleModulusLowResolution" + ".stl" ,self.res]  
                    self.filenames['midlep'] =  [self.filename2 + "MidleResolution" + ".stl",self.res]      
                    self.filenames['midleygp'] =  [self.filename2 + "MidleModulusLowResolution" + ".stl" ,self.res]  
                
                if self.res  ==  3:
                    self.filenames['high'] = [self.filename + "HighResolution" + ".stl",self.res]                 
                    self.filenames['highyg'] = [self.filename + "HighModulusLowResolution" + ".stl" ,self.res]   
                    self.filenames['highp'] = [self.filename2 + "HighResolution" + ".stl",self.res]                 
                    self.filenames['highygp'] = [self.filename2 + "HighModulusLowResolution" + ".stl" ,self.res] 
                 

                
                for i, item in enumerate(self.valuearrayrotated):
                        self.valij['val' + str(i+1)] = float(self.valuearrayrotated[i])
                


         
            
            self.setStlDir()
            self.createSTL()
            #self.valij['test'] = 'sfsd'
            #print self.valij.test
             
            
            
        
    def setStlDir(self):
        pathslist=Path.objects.all()      
        for stldir in pathslist:
            path=Path() 
            path = stldir
            if os.path.isdir(path.stl_dir): 
                self.pathexist = 1
                self.stl_dir= path.stl_dir
                break   
     
     
    def createSTL(self):
        for key, value in self.filenames.iteritems():
            filepath=os.path.join(self.stl_dir, value[0])
            if self.pathexist == 1:
                if os.path.isfile(filepath):  
                    self.filenames[key].append( 0 )   
                else:
                    self.filenames[key].append( 1 ) 
                
    def getdata(self):
        file_name = ""
        file_nameYoungModulus = ""
        create_stl= None
        create_stlym= None
        create_data_jason = None
        create_data_jasonym = None
        for key, value in self.filenames.iteritems():
            data= self.filenames[key]
            if key== 'low' or key== 'midle' or  key== 'high':
                file_name = data[0]
                create_stl = data[2]
            
            if key== 'lowyg' or key== 'midleyg' or  key== 'highyg': 
                file_nameYoungModulus = data[0]
                create_stlym = data[2] 
        
        return  file_name, create_stl, file_nameYoungModulus,create_stlym           
    
    
    def getdatapoly(self):
        file_name = ""
        file_nameYoungModulus = ""
        create_stl= None
        create_stlym= None
        create_data_jason = None
        create_data_jasonym = None
        for key, value in self.filenames.iteritems():
            data= self.filenames[key]
            if key== 'lowp' or key== 'midlep' or  key== 'highp':
                file_name = data[0]
                create_stl = data[2]
            
            if key== 'lowygp' or key== 'midleygp' or  key== 'highygp': 
                file_nameYoungModulus = data[0]
                create_stlym = data[2] 
                
        return  file_name, create_stl, file_nameYoungModulus,create_stlym          
        