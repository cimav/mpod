'''
Created on 04/09/2018

@author: Jorge Torres
'''

import numpy as N
import re
from django.db import models
from data.models import *
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from data.Utils import *
import os
import sys
from data.JQueryCode import *
import shlex

class AttrDict(dict):
    def __getattr__(self, item):
        return self[item]

    def __dir__(self):
        return super().__dir__() + [str(k) for k in self.keys()]
    
class BaseFile(object):
    '''
    classdocs
    '''
    def __init__(self, *args):
        self.fields = {}
 
        if args:
 
            for key in args[0]:
                if key != None:
                    self.fields[str(key)] = []
          
                    
 
class FileParsed(BaseFile): 
    def __init__(self, *args):
        super(FileParsed, self).__init__(*args)
        
    def addField(self,name,value = None):
        self.fields[name] = value

                
 

class FileUserUtil(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
     
         
        
        self.coefficientsmatrix = None
        self.__inputList = None
        self.catalogproperty_name = None

        self.catalogPointGroupSelectedName =None             
        self.dataproperty = None
        self.coefficientsmatrix2 = None
 
        self.catalogpointgroup_id = None
        self.propertyDetail = None
        self.objCatalogProperty = None
        self.objDataProperty = None
        self.objCatalogCrystalSystemSelected = None
        self.objTypeSelected = None
        self.objCatalogPointGroupSelected = None
        self.objPointGroupNamesSelected = None
        self.objAxisSelected=None
        self.typeSelectedId = None
        self.dimensions = None
        self.read_write_inputs = {}
        self.scij = None
        self.symmetry = None
        self.dataPropertyTempQuerySet= None
        self.ciffilein = None
        self.ciffileout = None
        self.pathexist = False
        self.fileexist = False
        self.loopedTag = 0
        self.text = None
        self.lines= None
        self.prop_index = None
        self.filenamein = None
        self.filenameout = None
        self.loops = None
        self.no_loops = None

        self.newotgs  = None
        self.props_exp  = None
        self.props_tens2   = None
        self.other_props  = None
        self.authors = {}
        self.fileParsedList = []
        self.custom_cifs_dir = ''
        self.error = None

        
    def setPointGroup(self,catalogproperty, property_name,inputList,dictitems,tenso_props_ids):
        self.catalogPointGroupSelectedName =str(dictitems['_symmetry_point_group_name_H-M']).replace(' ',"")                
        self.dataproperty = tenso_props_ids
        self.__inputList = inputList
        self.catalogproperty_name = catalogproperty
        
    def fillCoefficientsmatrix(self):
        for cursor, p in enumerate(self.__inputList):   
            index=self.getIndex(p[0]) 
            i = index[0]
            j= index[1]
            if p[1] == '?':
                self.coefficientsmatrix2[i][j]  = '?'
                self.coefficientsmatrix2[j][i]  = '?'
            else:
                self.coefficientsmatrix2[i][j]  = p[1]
                self.coefficientsmatrix2[j][i]  = p[1]
    
 
            
            
            
    def setCoefficientsmatrix(self,dim):
        self.dimensions = dim
        if len(self.dimensions) == 2:
            #self.coefficientsmatrix = N.zeros([int(dimensions[0]),int(dimensions[1])])  
            self.coefficientsmatrix2 =  [[0 for x in range(int(self.dimensions[0]))] for y in range(int(self.dimensions[1]))] 
            self.fillCoefficientsmatrix()
           

                    
                    
    def getIndex(self,coefficientsTag):       
        match = re.match(r"([0-9]+)",  coefficientsTag, re.I)
        if match:
            items = match.groups()
            numbers = items[0]
            index = re.findall(r'.{1,1}',numbers,re.DOTALL)
            indextem=[]
            indextem.append(int(index[0]) - 1)
            indextem.append( int(index[1]) - 1)
            return indextem
        
        
    def splitIndexFromTag(self,tag):  
        coefficients = None
        try:
            coefficients = re.findall('\d+', tag ) 
            match = re.match(r"([0-9]+)",  coefficients[0], re.I)
            if match:
                return coefficients[0]
            else:
                return coefficients
        except Exception, e:
            print "Message({0}): {1}".format(99, e)    
            return coefficients
     
        
               
           
    def seDataProperty(self,tag):
        try:
            self.objDataProperty=Property.objects.get(tag__exact=tag, active=True) 
        
             
        except  Exception as e:         
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            print err
            #self.error = err
            
        
        
    def setType(self):
        try:
            #typeDataPropertyQS=TypeDataProperty.objects.filter(dataproperty=self.objDataProperty)
            type_ids=TypeDataProperty.objects.filter(dataproperty=self.objDataProperty).values_list('type_id',flat=True)
            self.typeSelectedId = type_ids[0]
            self.objTypeSelected  = Type.objects.get(id=type_ids[0])
            self.objCatalogProperty = self.objTypeSelected.catalogproperty
            if self.objCatalogProperty.id == 1:
                self.symmetry = True
            if self.objCatalogProperty.id == 2:
                self.symmetry = False
            if self.objCatalogProperty.id == 3:
                self.symmetry = True
                
       
        except  Exception as e:         
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            print err
            #self.error = err
           
       
       
    def setFile(self,file=None):       
            try:
                tg =  None
                vtg = None
                pathslist=Path.objects.all()   
                for cifdir in pathslist:
                    paths=Path() 
                    paths = cifdir
                    if os.path.isdir(paths.cifs_dir_valids): 
                        self.pathexist = True
                        break
                    

                if self.pathexist== True:
                    if isinstance(file,FileUser):
                        self.filenamein = file.filename
                        self.ciffilein =os.path.join(paths.cifs_dir_valids, file.filename)
                        if file.publish:
                            self.ciffileout = os.path.join(paths.cifs_dir,str(file.datafile.code) + ".mpod")
                            self.filenameout = str(file.datafile.code) + ".mpod"
                        else:
                            self.ciffileout = os.path.join(paths.cifs_dir_valids, file.filename)
                            self.filenameout = file.filename
                            
                    else:
                        self.filenamein = file
                        if os.path.exists(os.path.join(paths.cifs_dir,file)):
                            self.ciffilein = os.path.join(paths.cifs_dir,file)
                            self.filenameout = file
                        elif os.path.exists(os.path.join(paths.cifs_dir_valids,file)):
                            self.ciffilein = os.path.join(paths.cifs_dir_valids, file)
                            self.filenameout = file
                        elif os.path.exists(os.path.join(self.custom_cifs_dir,file)):
                            self.ciffilein = os.path.join(self.custom_cifs_dir, file)
                            self.filenameout = file
                            
                    if self.ciffilein:
                        if os.path.exists(self.ciffilein):
                            self.fileexist = True
                            self.loadTextFile()
                        else:
                            self.fileexist = False
                    else:
                        self.fileexist = False
                        
                    
                            
            except Exception, e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                err= {}
                err['file']=fname
                err['line']=exc_tb.tb_lineno
                err['error']="Error: {1}".format( e.message, e.args) 
                print err
                #self.error = err
                    
       
    def loadTextFile(self):
        infile = open(self.ciffilein, 'r')
        self.text = infile.read()
        infile.close()
        self.lines = map(lambda x: x.strip(), self.text.strip().split("\n"))
 
       
    def isnumber(self, param):
        result = False
        try:
            val = float(param)
            result = True
            return result
        except ValueError:
            return result
        
        
    def setLoops(self ):
        non_loop_lines=[]
        non_loop_lines_dic={}
        loops = []
        loops_start_inds=[]
        loops_end_inds=[]
        il = 0
        loop_n = 0
        len_lins = len(self.lines)
        il2= 0
        loop_flag = False
        while il<len_lins:
            if self.lines[il].startswith("loop_"):
                loop_flag = True
                non_loop_lines_dic[loop_n]=non_loop_lines
                loop_n = loop_n + 1
                loop_tags = []
                loop_val_lins = []
                loops_start_inds.append(il+1)
                n_tags = 0
                vals_found = False
                for iloli, loli in enumerate(self.lines[il+1:]):
                    if loli.strip().startswith("_"):
                        if vals_found == False:
                            loop_tags.append(loli.strip())
                        else:
                            loops_end_inds.append(il2)
                            il = il2
                            break
                    else:
                        vals_found = True
                        loop_val_lins.append(loli)
                        il2 = il+1+iloli+loop_n
                loops.append([loop_tags, loop_val_lins])
                non_loop_lines=[]
                il = il2
            else:
                non_loop_lines.append(self.lines[il])
                il = il+1
                loop_flag = False
        if not loop_flag:
            loops.append([[None], [None]])
            non_loop_lines_dic[loop_n]=non_loop_lines
            
            
        self.loops = loops
        self.no_loops = non_loop_lines_dic
     
    
    
    def setAuthors(self):
        author = []
        for i ,item in enumerate(self.loops):
            if  item[0][0] == '_publ_author_name':
                tagsno = len( item[0])
                for i ,value in enumerate(item[1]):
                    author.append(value)
            else:
                pass
                 
                    
        self.authors['_publ_author_name'] = author
 
        
        
        
    def getLoops(self):
        for i ,item in enumerate(self.loops):
            print ' loop ' + str(i)+ ' ' 
            print ' tag ',  item[0][0]
            #print ' values ',  item[1]
            tagsno = len( item[0])
            for i ,value in enumerate(item[1]):
                valsno = len(value.split(' '))
                if tagsno == valsno:
                    print value.split(' ')
                elif tagsno== 1:
                    print value
                    
    def getNoLoops(self):
     
        porp_experimental_tgs=list(Tags.objects.filter(categorytag=CategoryTag.objects.get(id=1),active = True).values_list('tag',flat=True))#conditions
        props_tag=list(Tags.objects.filter(categorytag=CategoryTag.objects.get(id=2),active = True).values_list('tag',flat=True)) # properties
        otgs=list(Tags.objects.filter(categorytag=CategoryTag.objects.get(id=4),active = True).values_list('tag',flat=True))#Material
        
        self.newotgs={}
        self.props_exp= {}
        self.props_tens2 = {}
        props_tens = {}
        self.other_props = {}
        btg="_prop_"
        for lin in self.lines:    
            first = ''
            if lin.startswith('_'):
                first = lin.split('_')[1]
            if lin.startswith(btg):
                if lin != 'symmetry_point_group_name_H-M':
                    lcs=lin.split()
                    tagfind = lcs[0]
                    expc=list(ExperimentalParCond.objects.filter(tag=tagfind,active=True).values_list('tag',flat=True)) 
        
                    p=list(Property.objects.filter(tag=tagfind,active=True).values_list('tag',flat=True)) 
                else:
                    lcs[0]= lin.split()[0]            
                    lcs[1]= lin[len(lin.split()[0].strip()[6:]) + 6:]
         
                pr_str=lcs[0].strip()[6:]
                parts=pr_str.split('_')
                like =btg+ parts[0]  
                
                if parts[0] in porp_experimental_tgs and len(expc) > 0: #experimental
                    if pr_str not in self.props_exp:
                        if len(lcs) > 1:
                            self.props_exp[pr_str] =  lcs[1].strip().strip("'").strip()
                elif parts[0] in props_tag:          
                    if pr_str not in props_tens and len(p) > 0:  #properties tensor
                        if len(lcs) > 1:
                            self.props_tens2[pr_str] = lcs[1].strip().strip("'").strip()
                            props_tens[lcs[1].strip().strip("'").strip()]= pr_str
    
            elif first in otgs:
                    olcs =[]
                    if lin.split()[0].strip() != '_symmetry_point_group_name_H-M':
                        olcs=lin.split()
                    else:
                        olcs = {}
                        olcs[0]= lin.split()[0]            
                        olcs[1]= lin[len(lin.split()[0].strip()[6:]) + 6:]
                        
                    opr_str=olcs[0].strip()
                    opr_val=olcs[1].strip().strip("'").strip()
                    self.other_props[opr_str] = opr_val
            elif first not in self.newotgs:
                if first != '':
                    olcs=lin.split()
                    if len(olcs) > 1:
                        opr_str=olcs[0].strip()
                        opr_val=olcs[1].strip().strip("'").strip()
                        self.newotgs[opr_str] = opr_val
                        
                        
        print self.newotgs 
        print self.props_exp 
        print self.props_tens2  
        #print props_tens  
        print self.other_props 
    
    def parseFile(self):  
        error = False  
        iscondition= None
        categoryTagDic = {}
        conditions=[]
        properties = []
        foundproperties = True
        categoryTagName = ''
        tensor_dimensions = ''
        dataCounter = 0

        try:
            index = 0
            propertydatatag = 'data_' 
            proptag ='_prop_'
            tagfind = 'loop_'
            publ ='_publ_'
            
            categoryTagNames= list(CategoryTag.objects.all().values_list('name',flat=True))
            for name in categoryTagNames:
                categoryTagDic[name] = list(Tags.objects.filter(categorytag=CategoryTag.objects.get(name__exact=name),active = True).values_list('tag',flat=True))
 
 
            length =len (self.lines)
            numberlineandline = ''

            while index < length -1:
                prop_index = None
                data = {}
                for x in range(index, length):
                    line1= self.lines[x].rstrip('\n')
                    if line1.startswith(propertydatatag):
                        if data.has_key('data'):   
                            pass
                        else:
                            numberlineandline=  str(x) + ' '  + line1
                            data['data'] = [numberlineandline]
                            numberlineandline = ''

                        coeff=[]
                        #coeffdimen= {}
                        #porpertiestag=[]

                        
                        y = x + 1
                        #print  self.lines[y].rstrip('\n')
                        while y < length:
                        #for y in range(x + 1, length):
                            
                            line2= self.lines[y].rstrip('\n')
                            if line2.startswith(propertydatatag):   
                                index = y
                                break
                            else:
                                index = y
                                if line2.startswith('#'):
                                    #print line2
                                    pass
                                    
                                if line2 != '' and not line2.startswith('#'):
                                    identified = False
                                    
                                    lcs =line2.split()
                                    prstr = ''
                                    if line2.startswith(proptag):   
                                        prstr=(lcs[0].strip()[6:]).decode('latin-1')
                                        #tagfind = lcs[0]
                                        tagfind = (lcs[0]).decode('latin-1')
                                        tensor_dimensions = ''
                                        conditions = list(ExperimentalParCond.objects.filter(tag=tagfind,active=True).values_list('tag',flat=True)) 
                                        if conditions:
                                            pass
                                            
                                        properties = list(Property.objects.filter(tag=tagfind,active=True).values_list('tag',flat=True)) 
                                        if properties:
                                            if len(lcs) > 0:
                                                coeff.append(lcs[1].strip().strip("'").strip())
                                            
                                            #porpertiestag.append(lcs[0].strip().strip("'").strip())
                                            tensor_dimensions = list(Property.objects.filter(tag=tagfind,active=True).values_list('tensor_dimensions',flat=True))[0]
                                            
                                            #coeffdimen[lcs[1].strip().strip("'").strip()] = tensor_dimensions
                                    else:
                                        tagfind = (lcs[0]).decode('latin-1')
                                        prstr=(lcs[0].strip()[1:]).decode('latin-1')
                                        #categoryTagName = key
 
                                  
                     
                                    #dictionaryObj=Dictionary.objects.get(tag=tagfind,active=True)    
                                    categorytag_id=list(Dictionary.objects.filter(tag=tagfind,active=True).values_list('categorytag',flat=True))                                  
                                    parts=prstr.split('_')
                                    tagQuerySet = []
                                    if parts[0] != '':
                                        prts = parts[0]
                                        #tagQuerySet = Tags.objects.filter(tag__startswith=prts,active = True)
                                        tagQuerySet = Tags.objects.filter(tag__in=[prts],active = True)
                                        
                  
                                    for tagObj in tagQuerySet:
                                        if categorytag_id:
                                            if categorytag_id[0] == tagObj.categorytag.id:
                                                #print tagObj.categorytag.name
                                                categoryTagName = tagObj.categorytag.name
                                                if len(lcs) > 1:
                                                    identified = True
                                                    numberlineandline=  str(y) + ' '  + line2.decode('latin-1')
                                                    if not conditions and not properties:
                                                        if  data.has_key(categoryTagName):   
                                                            data[categoryTagName] += [numberlineandline]
                                                        else:
                                                            data[categoryTagName] = [numberlineandline]
                                                            
                                                        if not self.catalogPointGroupSelectedName:
                                                            if len(numberlineandline.split()) == 3:
                                                                if ((numberlineandline.split())[1]):
                                                                    if  (numberlineandline.split())[1] =='_symmetry_point_group_name_H-M':
                                                                        symmetrypg = (numberlineandline.split())
                                                                        self.catalogPointGroupSelectedName = (symmetrypg[2]).strip().strip("'").strip()
                                                       
                                            
                                                        numberlineandline = ''
                                                        
                   
                                                    if tensor_dimensions:
                                                        if not data.has_key('tensor_dimensions'):   
                                                            data['tensor_dimensions'] = [lcs[0] + ' ' +tensor_dimensions]
        
                                                        else:
                                                            data['tensor_dimensions'] += [lcs[0] + ' ' +tensor_dimensions]
         
                                                    if conditions or properties:
                                                        if  data.has_key(categoryTagName + '_nolooped'):   
                                                            data[categoryTagName+ '_nolooped'] += [numberlineandline]
                                                        else:
                                                            data[categoryTagName + '_nolooped'] = [numberlineandline]
                                                            
                                                        numberlineandline = ''
                                                        conditions = []
                                                        properties = []
                   
                   
                                                    break
                                                
                                                elif len(lcs) == 1:
                                                    identified = True
                                                    numberlineandline =  str(y) + ' '  + line2.decode('latin-1')
                                                    if not conditions and not properties and parts[0].decode('latin-1') != 'data':
                                                        #if parts[0] != 'data':
                                                        if  data.has_key(categoryTagName):   
                                                            data[categoryTagName] += [numberlineandline]
                                                        else:
                                                            data[categoryTagName] = [numberlineandline]
                                                            
                                                        numberlineandline = ''
           
                                                    elif conditions or  properties or  parts[0].decode('latin-1') == 'data':
                                                            if  data.has_key(categoryTagName + '_looped'):   
                                                                data[categoryTagName + '_looped'] += [numberlineandline]
                                                            else:
                                                                data[categoryTagName + '_looped'] = [numberlineandline]
     
                 
                                                            if not data.has_key('allloopeds'):
                                                                data['allloopeds'] = [numberlineandline]
                                                            else:
                                                                data['allloopeds'] +=  [numberlineandline]
      
                                                            numberlineandline = ''
                                                            conditions = []
                                                            properties = []
                                                            
                                                            
                                                    else:
                                                        if  data.has_key( 'other_looped'):   
                                                            data['other_looped'] += [numberlineandline]
                                                        else:
                                                            data[ 'other_looped'] = [numberlineandline]
  
                                                        numberlineandline = ''
                                                            
                                                    break
                                                    
                                                else:
                                                    identified = False
                                        else:    
                                            identified = False
                                            if tagObj.categorytag:
                                                categoryTagName = tagObj.categorytag.name
                                                if line2.startswith('_'):   
                                                    lt = line2.split()   
                                                    if len( line2.split()  )> 1:
                                                        numberlineandline=  str(y) + ' '  + line2
                                                        
                                                        if  data.has_key(categoryTagName):   
                                                            data[categoryTagName] += [numberlineandline]
                                                        else:
                                                            data[categoryTagName] = [numberlineandline]
                                                    else:
                                                        numberlineandline=  str(y) + ' '  + line2
                                                        if  data.has_key(categoryTagName):   
                                                            data[categoryTagName] += [numberlineandline]
                                                        else:
                                                            data[categoryTagName] = [numberlineandline]

                                                        #index = y
                                                        for z in range(y + 1, length):
                                                            #index = z
                                                            numberlineandline = ''
                                                            line3= self.lines[z].rstrip('\n')
                                                            if line3.startswith('_'):     
                                                                numberlineandline = ''
                                                                break
                                                            elif  line3 != '' and line3 != ';' and not line3.startswith('loop_'):
                                                                numberlineandline += str(z) + ' '  + line3.strip().strip("'").strip()
                                                                if  data.has_key(categoryTagName):   
                                                                    data[categoryTagName] += [numberlineandline]
                                                                else:
                                                                    data[categoryTagName] = [numberlineandline]
 
                                                        

                                                    break
      
                                    if not identified:     
                                        if line2.startswith('_'):   
                                            lt = line2.split()   
                                            categoryTagName = categoryTagName = list(CategoryTag.objects.filter(id=6).values_list('name',flat=True))[0]
                                            if len( line2.split()  )> 1:
                                                numberlineandline=  str(y) + ' '  + line2
                                                if  data.has_key(categoryTagName):   
                                                    data[categoryTagName] += [numberlineandline]
                                                else:
                                                    data[categoryTagName] = [numberlineandline]
                                            else:
                                                numberlineandline=  str(y) + ' '  + line2
                                                if  data.has_key(categoryTagName):   
                                                    data[categoryTagName] += [numberlineandline]
                                                else:
                                                    data[categoryTagName] = [numberlineandline]
                                                            
                                                for z in range(y + 1, length):
                                                    numberlineandline = ''
                                                    line3= self.lines[z].rstrip('\n')
                                                    if line3.startswith('_'):   
                                                        numberlineandline = ''
                                                        y = z  - 1
                                                        break
                                                    elif  line3 != '' and line3 != ';' and not line3.startswith('loop_'):
                                                        numberlineandline += str(z) + ' '  + line3.strip().strip("'").strip()
                                                        if  data.has_key(categoryTagName):   
                                                            data[categoryTagName] += [numberlineandline]
                                                        else:
                                                            data[categoryTagName] = [numberlineandline]
       
                                                #break    
 
                                                
                                        elif  line2 != '' and line2 != ';' and not line2.startswith('loop_'): 
                                            lt = line2.split()
                                            if lt[0] not in coeff:
                                                numberlineandline=  str(y) + ' '  + line2
                                                if  data.has_key(categoryTagName):   
                                                    data[categoryTagName] += [numberlineandline]
                                                else:
                                                    data[categoryTagName] = [numberlineandline]
                                            
                                                numberlineandline = ''
                            y += 1
                        break
                     
                #print data
                """if  data.has_key('other_looped'): 
                    for item in data['other_looped']:
                        categoryTagName = list(CategoryTag.objects.filter(id=3).values_list('name',flat=True))[0]
                        if  data.has_key(categoryTagName):   
                            article=data[categoryTagName]
                            for v, item2 in enumerate(article):
                                if item2 == item:
                                    line =  item.split()
                                    for z in range(int(line[0]) + 1, length):
                                        loopedline= self.lines[z].rstrip('\n')
                                        if not loopedline.startswith('_'):
                                            if not loopedline.startswith(';'):
                                                article[v] +=   ' ' + loopedline + ', '
                                        else:
                                            break
                """                       
                categoryTagListName = list(CategoryTag.objects.filter(id__in=[1,2]).values_list('name',flat=True))
                         
                if categoryTagListName:           
                    """for tag in categoryTagListName:     
                        if  data.has_key(tag+'_looped'):
                            if not data.has_key('allloopeds'):
                                n = data[tag+'_looped']
                                data['allloopeds'] = n
                            else:
                                data['allloopeds'] =  data[tag+'_looped'] + n
                    """

                    categoryTagName = list(CategoryTag.objects.filter(id=2).values_list('name',flat=True))[0]
                    if  data.has_key(categoryTagName+'_nolooped'):
                        for item in data[categoryTagName + '_nolooped']:
                            for td in data['tensor_dimensions']:
                                tdtag= td.split()
                                itemtag= item.split()
                                if tdtag[0] == itemtag[1]:
                                    #print tdtag[1] #dimension
                                    cindex = tdtag[1].split(",")
                                    if data.has_key('allloopeds'):
                                        #print data['allloopeds']     
                                        allloopeds= data['allloopeds']
                                        linesnumer= []
                                        for looped in allloopeds:
                                            linesnumer.append(looped.split()[0])
                                        
                                        linesnumer.sort()
                                        line= linesnumer[-1]
                                        coefftag = itemtag[2].strip().strip("'").strip()
                                        listSameProperties = []
                                        numberlinesValues = []
                                        last = False
                                        for z in range(int(line) + 1, length):         
                                            loopedline= self.lines[z].strip('\n')
                                            linesplite= loopedline.split()
                                            
                                            if loopedline != '':
                                                if linesplite[0] == coefftag:
                                                #if loopedline.startswith(coefftag):
                                                    if len(cindex) == 2: 
                                                        
                                                        if linesplite[1]  not in listSameProperties:
                                                            listSameProperties.append(linesplite[1] )
                                                            numberlinesValues.append(str(z) + ' ' + loopedline)
                                                        else:
                                                            if data.has_key('numberlinesValues'):
                                                                if numberlinesValues:
                                                                    data['numberlinesValues'] += [numberlinesValues]
                                                            else:
                                                                if numberlinesValues:
                                                                    data['numberlinesValues'] = [numberlinesValues]
 
                                                            last = False
                                                            listSameProperties = []
                                                            numberlinesValues = []
                                                            listSameProperties.append(linesplite[1] )
                                                            numberlinesValues.append(str(z) + ' ' + loopedline)
                                                            
                                                        tensorial_index= list(linesplite[1] )

                                                    elif len(cindex) == 1: 
                                                        #linesplite= loopedline.split()
                                                        #coefficientsmatrix.append(linesplite)
                                                        numberlinesValues.append(str(z) + ' ' + loopedline)
 
                                                else:
                                                    if data.has_key('numberlinesValues') and len(numberlinesValues) > 0:
                                                        data['numberlinesValues'] += [numberlinesValues]
                                                        numberlinesValues=[]
                                                    elif not data.has_key('numberlinesValues') and len(numberlinesValues) > 0:
                                                        data['numberlinesValues'] = [numberlinesValues]
                                                        numberlinesValues=[]
 
                                            else:
                                                if data.has_key('numberlinesValues') and len(numberlinesValues) > 0:
                                                        data['numberlinesValues'] += [numberlinesValues]
                                                        numberlinesValues=[]
                                                elif not data.has_key('numberlinesValues') and len(numberlinesValues) > 0:
                                                        data['numberlinesValues'] = [numberlinesValues]
                                                        numberlinesValues=[]
                                                        
                                                break
 
                                        if data.has_key('numberlinesValues') and len(numberlinesValues) > 0:
                                                data['numberlinesValues'] += [numberlinesValues]
                                                numberlinesValues=[]
                                        elif not data.has_key('numberlinesValues') and len(numberlinesValues) > 0:
                                                data['numberlinesValues'] = [numberlinesValues]
                                                numberlinesValues=[]
                                        
                                        break
                    
                
                error = False
 
                #print file
                tensors = {}
                tensorsjs_jq = {}
                if not error:
                    categoryTagName6 = list(CategoryTag.objects.filter(id=6).values_list('name',flat=True))[0]#undefined
                    categoryTagName3 = list(CategoryTag.objects.filter(id=3).values_list('name',flat=True))[0]#article
                    categoryTagName2 = list(CategoryTag.objects.filter(id=2).values_list('name',flat=True))[0]#properties
                    categoryTagName1 = list(CategoryTag.objects.filter(id=1).values_list('name',flat=True))[0]#conditions

                    categoryTagNameList=[categoryTagName2+ '_nolooped', categoryTagName2 + '_looped', 'allloopeds', categoryTagName1+ '_looped', 'tensor_dimensions' , 'numberlinesValues', 'other_looped','data',categoryTagName1 + '_nolooped',categoryTagName3,categoryTagName6]
                     
                    categoryTagListName = list(CategoryTag.objects.all().exclude(id__in=[1,2]).values_list('name',flat=True))
                    
                    fileParsed= FileParsed(categoryTagListName)
                    fileParsed.addField('filename', self.filenamein)
                
                    """morthan_one = []
                    if len(self.datalist) > 1:
                        morthan_one.append(file )
                    """
                    
                    #for itemDic in self.datalist:
                    #print data['data']
     
                    fileParsed.addField('data', data['data'])
                    if data.has_key(categoryTagName3):
                        fileParsed.addField(categoryTagName3, data[categoryTagName3])
                        
                    if data.has_key(categoryTagName6):
                        fileParsed.addField(categoryTagName6, data[categoryTagName6])
                         
                    for key, value in data.iteritems():
                        if key not in categoryTagNameList: 
                            #print  key
                            #print value
                            if fileParsed.fields.has_key(key):
                                if value == None:
                                    fileParsed.fields[key] = value
                                else:
                                    fileParsed.fields[key] += value
                                    
                                    
                               
                        
                        elif key == categoryTagName2 + '_nolooped': # 'properties_nolooped'
                            
                            #print categoryTagName1+ '_nolooped'
                            if data.has_key(categoryTagName1+ '_nolooped'):
                                #print data[categoryTagName1+ '_nolooped']
                                fileParsed.addField(str(categoryTagName1)+ '_nolooped', data[categoryTagName1+ '_nolooped'])
                                
                            #print categoryTagName2+ '_nolooped'
                            if data.has_key(categoryTagName2+ '_nolooped'):
                                #print data[categoryTagName2+ '_nolooped']
                                fileParsed.addField(str(categoryTagName2)+ '_nolooped', data[categoryTagName2+ '_nolooped'])
                                
                            #print categoryTagName2+ '_looped'
                            if data.has_key(categoryTagName2+ '_looped'):
                                #print data[categoryTagName2+ '_looped']
                                fileParsed.addField(str(categoryTagName2)+ '_looped', data[categoryTagName2+ '_looped'])
                            
                            counterProperty = 0
                            #print data['allloopeds']
                            allloopeds = []
                            if data.has_key( 'allloopeds'):
                                allloopeds= data['allloopeds']
                                
                            conditions_looped = []
                            cointitionsindex = []
                            if data.has_key(categoryTagName1+ '_looped'):
                                #print categoryTagName1+ '_looped'
                                #print data[categoryTagName1+ '_looped']
                                fileParsed.addField(str(categoryTagName1)+ '_looped', data[categoryTagName1+ '_looped'])
             
                                conditions_looped= data[categoryTagName1+ '_looped']
                                for cl in conditions_looped:
                                    if cl in allloopeds:
                                        indexfromcl= allloopeds.index(cl)
                                        cointitionsindex.append(indexfromcl)
             
                            #print '******************************************************tensor values*************************************************'
                            
                            coefficientsmatrix = None
                            conditions_looped_consolidated = {}
                            
                            
                            #print value  
                            for item in value:
                                #fileParsed.addField('propertyLoopedName', item.split())
                                tensors[counterProperty] = [{'propertyloopedname': item.split()}]
                                
                                if (item.split())[1]:
                                    propertytagsplit = (item.split())
                                    propertytag = propertytagsplit[1]
                                    propertytagcoeff = propertytagsplit[2]
                                    self.seDataProperty(propertytag)
                                    self.setType()
                                    self.setCrystalSystem()
                                    self.setCatalogPointGroupSelected()
                                    self.setPointGroupNamesSelected()
                                    self.setAxisSelected()
                                    self.setCatalogPropertyDetail()
                                    #if self.setDataProperties():
                                    
                                    jqueryRules= JQueryRules()
                                    if self.propertyDetail:
                                        jqueryRules= JQueryRules()
                                        jqueryRules.generateCode(self.symmetry, self.propertyDetail, self.read_write_inputs,self.scij, False)
                                        #print jqueryRules.jquery
                                        tensors[counterProperty] += [{'tensorrules': True}] 
                                        self.propertyDetail = []
                                    else:
                                        tensors[counterProperty] += [{'tensorrules': False}] 
                                         
                                    

                                tensors[counterProperty] += [{'propertyloopednamejquery': jqueryRules.jquery}]    
                                
                                #print item.split()
                                property= item.split()
                                coefftag = property[2].strip().strip("'").strip()
                                #print  property
                                 
                                #counterProperty += 1
                                
                                dimension = ''
                                tensor_dimensions= data['tensor_dimensions']
 
                                for ts in tensor_dimensions:
                                    tslist =  ts.split()
                                    if property[1] == tslist[0]:
                                        dimension = tslist[1].split(',')
                                        #print tslist[1]
                                        cindex = dimension
                                        if len(cindex) == 2:
                                            indexi = int(cindex[0])
                                            indexj=  int(cindex[1])
                                            coefficents = indexi * indexj
                                            coefficientsmatrix = [["0" for xi in range(indexj)] for yj in range(indexi)] 
                                        elif len(cindex) == 1:
                                            if int(cindex[0]) ==0:
                                                coefficientsmatrix = [] 
                                            elif int(cindex[0])  !=0:
                                                indexi = int(1)
                                                indexj=  int(cindex[0])
                                                coefficientsmatrix = [["0" for xi in range(indexj)] for yj in range(indexi)] 
                                        
             
                                        
                                numberlinesValues = []
                                if data.has_key( 'numberlinesValues'):
                                    numberlinesValues= data['numberlinesValues']
                                    
                                found = False
                                counterLinesValues = 0
                                
                                conditions_looped_val = {}
                                properties_looped_val= {}
                                properties_looped_lines_val = {}
                                properties_looped_lines_counter = {}
                                for linesValues in numberlinesValues:
                                    if found:
                                        
                                        #print coefficientsmatrix
                                        counterLinesValues += 1           
                                        
        
                                    condlen=len(cointitionsindex) 
                                    for lines in linesValues:
                                        vals =  lines.split()
                                        """if coefftag== 'Tcoff10':
                                            if vals[1] == coefftag:
                                                print coefftag
                                        """
                                            
                                        if vals[1] == coefftag:
                                            if len(cointitionsindex) > 0:
                                                for ind in cointitionsindex:
                                                    if len(dimension) == 2:
                                                        conditionname = (allloopeds[ind]).split()
                                                        inputfieldname = conditionname[1]
                                                        if conditions_looped_val.has_key(inputfieldname ):
                                                            #print vals[ind + 1].strip().strip("'").strip()
                                                            #print val[inputfieldname]
                                                            if   vals[ind + 1].strip().strip("'").strip() not in conditions_looped_val[inputfieldname]:
                                                                conditions_looped_val[inputfieldname] = [vals[ind + 1].strip().strip("'").strip()]
                                                                #print inputfieldname
                                                                #print inputfieldname.replace(' ', '_' + str(counterProperty) + '_' + str(counterLinesValues))
                                                                #print vals[ind + 1]
                                                        else:
                                                            conditions_looped_val[inputfieldname] = [vals[ind + 1].strip().strip("'").strip()]
                                                            #print inputfieldname
                                                            #print vals[ind + 1]
                                                
                                                    elif len(dimension) == 1:
                                                        conditionname = (allloopeds[ind]).split()
                                                        inputfieldname = conditionname[1]
                                                        if conditions_looped_val.has_key(inputfieldname ):
                                                            #if   vals[ind + 1].strip().strip("'").strip() not in conditions_looped_val[inputfieldname]:
                                                            conditions_looped_val[inputfieldname] += [vals[ind + 1].strip().strip("'").strip()]
                                                        else:
                                                            conditions_looped_val[inputfieldname] = [vals[ind + 1].strip().strip("'").strip()]
                                                    
                                                        
                                                #print vals
                                                #inp = k2 + '_'+ tensorval3[k1][k2][0]
                                                #input = inp.replace('ij',tensorval3[k1][k2][1])
                                                
                                                inp = vals[0] + '_'+ vals[1]
                                                input = inp.replace('ij',vals[2])
                                                properties_looped_lines_val[vals[0]] = [input]
                                                #properties_looped_lines_val[vals[0]] = vals[1:]
                                                
                                                #print vals[1:len(vals) - condlen]
                                                if len(dimension) == 2:
                                                    tensorial_index= list(vals[2] )
                                                    coefficientsmatrix[int(tensorial_index[0]) - 1 ][int(tensorial_index[1]) - 1] = vals[3]
                                                elif len(dimension) == 1:
                                                    if int(dimension[0]) ==0:
                                                        coefficientsmatrix.append(vals[2])
                                                    elif int(dimension[0]) !=0:
                                                        tensorial_index= list(vals[2] )
                                                        coefficientsmatrix[0][int(tensorial_index[0]) - 1] = vals[3]
                                                             
                                                        
                                           
                                                        
                                            else:
                                                if len(dimension) == 2:
                                                    #print vals
                                                    inp = vals[0] + '_'+ vals[1]
                                                    input = inp.replace('ij',vals[2])
                                                    properties_looped_lines_val[vals[0]] = [input]
                                                
                                                    #properties_looped_lines_val[vals[0]] = vals[1:]
                                                    tensorial_index= list(vals[2] )
                                                    coefficientsmatrix[int(tensorial_index[0]) - 1 ][int(tensorial_index[1]) - 1] = vals[3]
                                                    #print vals[1:]
                                                    #inputfieldname = '_'.join(str(e) for e in vals[:2])
                                                    #print inputfieldname
                                                elif len(dimension) == 1:
                                                    #print vals
                                                    inp = vals[0] + '_'+ vals[1]
                                                    input = inp.replace('ij',vals[2])
                                                    properties_looped_lines_val[vals[0]] = [input]
                                                
                                                    #properties_looped_lines_val[vals[0]] = vals[1:]
                                                    if int(dimension[0]) ==0:
                                                        coefficientsmatrix.append(vals[2])
                                                    elif int(dimension[0]) !=0:
                                                        tensorial_index= list(vals[2] )
                                                        coefficientsmatrix[0][int(tensorial_index[0]) - 1] = vals[3]
                                                     
                                                    #print vals[1:]
            
                                            found = True
                                        else:
                                            found = False
                                            break
      
                                    if found:
                                        #print counterLinesValues
                                        #print coefficientsmatrix
                                        
                                        if conditions_looped_val:
                                            #print conditions_looped_val
                                            conditions_looped_consolidated[counterLinesValues] = [conditions_looped_val] 
                                            conditions_looped_val = {}
 
                                        properties_looped_val[counterLinesValues ]= coefficientsmatrix
                                        #print coefficientsmatrix
                
                                        cindex = dimension
                                        if len(cindex) == 2:
                                            indexi = int(cindex[0])
                                            indexj=  int(cindex[1])
                                            coefficents = indexi * indexj
                                            coefficientsmatrix = [["0" for xi in range(indexj)] for yj in range(indexi)] 
                                        elif len(cindex) == 1:
                                            if int(cindex[0]) ==0:
                                                coefficientsmatrix = [] 
                                            elif int(cindex[0])  !=0:
                                                indexi = int(1)
                                                indexj=  int(cindex[0])
                                                coefficientsmatrix = [["0" for xi in range(indexj)] for yj in range(indexi)]   
                                         
         
                                        properties_looped_lines_counter[counterLinesValues]=properties_looped_lines_val
                                        #print properties_looped_lines_val
                                        properties_looped_lines_val = {}
                                         
                                        
                                    else:
                                        if properties_looped_val:
                                            if conditions_looped_consolidated:
                                                #print conditions_looped_consolidated
                                                #print properties_looped_val
                                                #print properties_looped_lines_counter
                                                """for k,v in conditions_looped_consolidated.iteritems():                                                    
                                                    print conditions_looped_consolidated[k]
                                                    print properties_looped_val[k]
                                                    print properties_looped_lines_counter[k]
                                              
                                                print '\n'
                                                """
                                                
                                                tensors[counterProperty] += [{'conditions_looped_consolidated':conditions_looped_consolidated}]
                                                tensors[counterProperty] += [{'properties_looped_val':properties_looped_val}]
                                                tensors[counterProperty] += [{'properties_looped_lines_counter':properties_looped_lines_counter}] 
                                                
                                                
                                                #counterProperty += 1
                                                properties_looped_val= {}
                                                conditions_looped_consolidated = {}
                                            else:
                                                #print properties_looped_val
                                                #print properties_looped_lines_counter
                                                """for k,v in properties_looped_val.iteritems():
                                                    print properties_looped_val[k]
                                                    print properties_looped_lines_counter[k]

                                                print '\n'
                                                """
                                                
                                                
                                                tensors[counterProperty] += [{'properties_looped_val':properties_looped_val}]
                                                tensors[counterProperty] += [{'properties_looped_lines_counter':properties_looped_lines_counter}] 
                                                
                                                properties_looped_val = {}
                                                properties_looped_lines_counter = {}
                                                
                                            counterProperty += 1
                     
                                                
                                                
                                if  found:
                                        if properties_looped_val:
                                            if conditions_looped_consolidated:
                                                #print conditions_looped_consolidated
                                                #print properties_looped_val
                                                #print properties_looped_lines_counter
                                                """for k,v in conditions_looped_consolidated.iteritems():
                                                    print conditions_looped_consolidated[k]
                                                    print properties_looped_val[k]
                                                    print properties_looped_lines_counter[k]
                                             
                                                print '\n'
                                                """
 
                                                
                                                tensors[counterProperty] += [{'conditions_looped_consolidated':conditions_looped_consolidated}]
                                                tensors[counterProperty] += [{'properties_looped_val':properties_looped_val}]
                                                tensors[counterProperty] += [{'properties_looped_lines_counter':properties_looped_lines_counter}] 
                                                #counterProperty += 1
 
                                            else:
                                                #print properties_looped_val
                                                #print properties_looped_lines_counter
                                                """for k,v in properties_looped_val.iteritems():
                                                    print properties_looped_val[k]
                                                    print properties_looped_lines_counter[k]
                                                print '\n'
                                                """
                                                
                                                
                                                tensors[counterProperty] += [{'properties_looped_val':properties_looped_val}]
                                                tensors[counterProperty] += [{'properties_looped_lines_counter':properties_looped_lines_counter}] 
                                                
                                                
                                                
                                            counterProperty += 1
 
                                    
                                                  
                        else:
                            pass
                            #print key
                            #print value
                            
                    
                    #print '*****************************************************'
    
                fileParsed.addField('tensors', tensors) 
                self.fileParsedList.append(fileParsed)  
        
                 
            return  error   
                
                
                
 
        except Exception, e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            print err
            #self.error = err
            
            return True
 
 
    def findAndUpdateLine(self,li,value,dimension,value_index=None):
        change = False
        error = None
 
        try:
            line =li.split('_')
            if len(line) == 1:
                if isinstance(line[0], str):
                    #print self.lines[int(line[0])]
                    if dimension== '2':
                        if value_index == None:
                            value_index  = 2
                    elif dimension== '1':
                        if value_index == None:
                            value_index  = 1
                    elif dimension== '0':
                        if value_index == None:
                            value_index  = 0
                        

                    vtg = None
                    valt = None
                    valn = None
                    isquotedvalue = False
                    lu = (self.lines[int(line[0])]).split()
                    vt= lu[value_index]
                    lu2= shlex.split(self.lines[int(line[0])])
                    if vt.startswith("'"): 
                        vtg=  "'" + lu2[value_index] +"'"
                        newval = (str(value[0])).strip().strip("'").strip()
                        valn  = "'" + newval +"'"
                        isquotedvalue = True
                    elif not vt.startswith("'") and value_index ==0: 
                        lu2 =[self.lines[int(line[0])]]
                        vtg= self.lines[int(line[0])]  
                        valn = value[0]
                        isquotedvalue = False
                        #print valn
                        #print lu2
                    else:
                        vtg= lu2[value_index]
                        valn = value[0]
                        isquotedvalue = False
                        #print valn
                        

                    if vtg != valn:
                        lu2[value_index] = valn
                        updatedline = ' '.join(str(e) for e in lu2)
                        self.lines[int(line[0])]  = updatedline
                        #print self.lines[int(line[0])]  
                        change = True
                    
                
            return change,error
             
        except  Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            error = err
            return change,error
           
        
        
        
        
    def findProperty(self,propTag,newvalue,category_tags,tag=None, indexij=None):  
        
 
        found = False  
        try:
            index = 0
            start ='_prop_'
            tagfind = 'loop_'
            
            publ ='_publ_'
  
            porp_tgs=[]
            tagsQuerySet = None
            if category_tags:
                if category_tags== 2:
                    porp_tgs=list(Tags.objects.filter(categorytag=CategoryTag.objects.get(id=category_tags),active = True).values_list('tag',flat=True))# for properties
                elif category_tags == 1:
                    porp_tgs=list(Tags.objects.filter(categorytag=CategoryTag.objects.get(id=category_tags),active = True).values_list('tag',flat=True))# for experimentalparcond
 
 
            length =len (self.lines)
            #data = 'data_' + self.filenamein.replace(".mpod",  '')
            
            coeffToFind= None
            if tag and indexij:
                coeffToFind= tag + ' ' + str(indexij)
            elif tag:
                coeffToFind= tag
            
            objDictionarySelected = None
            if propTag:
                objDictionarySelected = Dictionary.objects.get(tag=propTag)
                if objDictionarySelected.type == "numb":
                    if isinstance(newvalue, float): 
                        newvalue = float(newvalue)
                elif objDictionarySelected.type == "char":
                        newvalue = "'" + str(newvalue) + "'"    
                elif objDictionarySelected.type == None:
                    if self.isnumber(newvalue): 
                        newvalue = float(newvalue)
                    else:
                        newvalue = "'" + str(newvalue) + "'"    
 
            while index < length -1:
                prop_index = None
                for x in range(index, length):
                    line1= self.lines[x].rstrip('\n')
                    if line1.startswith('loop_') and tag:
                        loopedTag = 0
                        for i in range(x + 1, length):
                            line2= self.lines[i].rstrip('\n')
                            if line2.startswith(start):
                                print line2
                                if line2== propTag:
                                    prop_index = loopedTag
                                    loopedTag += 1
                                    self.loopedTag = loopedTag
                                else:       
                                    loopedTag += 1
                                    self.loopedTag = loopedTag
                                    
                                index = i
                            elif coeffToFind and line2.startswith(coeffToFind):
                                print line2
                                plps =  line2.split(' ')
                                vtg = plps[prop_index]
                                vtg =vtg.strip().strip("'").strip()
                                if newvalue:
                                    plps[prop_index] = newvalue
                                    updatedline = ' '.join(str(e) for e in plps)
                                    self.lines[i]= updatedline  
                                    index = length
                                    found = True 
                                    break
                                
                            elif line2.startswith(publ):
                                for j in range(i + 1, length):
                                    line3= self.lines[j].rstrip('\n')
                                    print line3
                                    if line3.startswith('loop_'):
                                        index = j
                                        break
                                    else:
                                        index = j
                                break  
                            elif line2.startswith('data_'):       
                                for j in range(i + 1, length):
                                    line3= self.lines[j].rstrip('\n')
                                    print line3
                                    if line3.startswith('loop_'):
                                        index = j
                                        break
                                    else:
                                        index = j
                                break  
             
     
                        break                    

                    else:
                        if line1.startswith(start):
                            lcs=line1.split()
                            prstr=lcs[0].strip()[5:]
                            parts=prstr.split('_')
                            if parts[1] in porp_tgs:
                                ptgs=lcs[0]
                                if ptgs == propTag and len(lcs) > 1:
                                    vtg = lcs[1]
                                    if newvalue:
                                        lcs[1] = newvalue
                                        updatedline = ' '.join(str(e) for e in lcs)
                                        self.lines[x]= updatedline + '\n'
                                        index = length
                                        found = True 
                                        break
 
            return found 
        except Exception, e:
            found = False
            return found
            

        except  IOError as e:
            print "Error %s " % e.strerror
         
    def findLoopedValue(self, tag, index=None):       
        #pathexist = False
        tg =  None
        vtg = None
        lineToFind= None
        if index:
            lineToFind= tag + ' ' + str(index)
        else:
            lineToFind= tag
            
            
        try:
            index = None
            for i, line in enumerate(self.lines):
                l = line.rstrip('\n')
                if line.startswith(lineToFind):
                    index = i
                    plps =  l.split(' ')
                    try:
                        vtg = plps[self.prop_index]
                        vtg =vtg.strip().strip("'").strip()
                        break
                    except:
                        index = None

        except  IOError as e:
            print "Error %s " % e.strerror
            
    def findPointGroupSelectedName(self, tag):       
        #pathexist = False
        tg =  None
        vtg = None
        try:
            index = None
            for i, line in enumerate(self.lines):
                l = line.rstrip('\n')
                if line.startswith(tag):
                    plps =  l.split(' ')
                    try:
                        tg, vtg = plps
                        tg =tg.strip().strip("'").strip()
                        vtg =vtg.strip().strip("'").strip()
                        self.catalogPointGroupSelectedName = vtg
                        break
                    except:
                        self.catalogPointGroupSelectedName = None

        except  IOError as e:
            print "Error %s " % e.strerror
               
            
            #return vtg   
               
    def prepareHTMLTable(self,todo,objDataFileTemp,objPropertyTemp, fileUser ):
        try:
            idupdatemessage =str(fileUser.id) +  str(objDataFileTemp.id) + str(objPropertyTemp.id)
            function = ''
            htmlLabel = ''
            input = ''
            label =objPropertyTemp.short_tag
            coeffTags = ''
            coeffTags += 'idupdatemessage_id=' + str(idupdatemessage) + ','
            coeffTags += 'datadfiletemp_id=' + str(objDataFileTemp.id) + ','
            coeffTags += 'propertytemp_id=' + str(objPropertyTemp.id) + ','
            coeffTags += 'pointgroupselectedname=' +self.catalogPointGroupSelectedName+ ','
            coeffTags += 'coeffTag=' +label+ ','
           
        
            datafilepropertytemp_ids=DataFilePropertyTemp.objects.filter(datafiletemp=objDataFileTemp,propertytemp=objPropertyTemp).values_list('id',flat=True)
            index = objPropertyTemp.tensor_dimensions.split(",")
            indexi = int(index[0])
            indexj=  int(index[1])
            
            coefficents = indexi * indexj
        
            coefficientsmatrix = [["" for x in range(indexj)] for y in range(indexi)] 
            propertyValuesTempQuerySet=[]
            if  datafilepropertytemp_ids:
                propertyValuesTempQuerySet= PropertyValuesTemp.objects.filter(datafilepropertytemp_id__in=datafilepropertytemp_ids).order_by('tensorial_index')
                for x,item in enumerate( propertyValuesTempQuerySet):
                    tensorial_index= list(str(item.tensorial_index)  )
                    i =int(tensorial_index[0]) - 1
                    j = int(tensorial_index[1]) -1
                    coefficientsmatrix[i][j] =str(item.value)
                    lbl= str(i +1) + str(j +1)
                    inputlabel = label.replace("ij",  lbl)
                    if x != (len(propertyValuesTempQuerySet) - 1 ):
                        coeffTags += inputlabel + ',' 
                    else:
                        coeffTags += inputlabel
            else:
                countercoeff = 0
                for i in range(indexi):
                    for j in range(indexj):
                        lbl= str(i +1) + str(j +1)
                        inputlabel = label.replace("ij",  lbl)
                        if countercoeff != (coefficents - 1):
                            coeffTags += inputlabel + ',' 
                        else:
                            coeffTags += inputlabel
                            
                        countercoeff += 1
                            
        
            table = '<table style="border-collapse: collapse;"  > <tbody>' 
            for i in range(indexi):
                table = table +  ' <tr  >' 
                for j in range(indexj):
                    lbl=  str(i +1) + str(j +1)
                    inputlabel = label.replace("ij",  lbl)
                    htmlLabel = ''
                    htmlLabel = '<label style="width: 53px;" for="journal">' + inputlabel +'</label><br/>'    
                    input = '<input type="text" id="'+ inputlabel+'" name="'+ inputlabel+'" value="'+ str(coefficientsmatrix[i][j])+'"   placeholder=""  style="width: 53px;" >'
    
                   
                    table = table + ' <td> '+htmlLabel + input+'</td>' 
                 
                table = table +  ' </tr>' 
                
            table = table +  ' <tr >' 
            
 
            function  = "updatecoefficient('" + coeffTags + "');"
            
            td = ' <td colspan="'+str(indexj)+'"> <div class="submit-row"><p><a href="#" class="submit-row" onclick="' + function + '">Update</a></p></div></td>' 
            
            table = table +td
            #table = table + ' <td colspan="'+str(indexj)+'"> <div class="submit-row"><label id="' + idupdatemessage + '">xc</label><p><a href="#" class="submit-row" onclick="' + function + '">Update</a></p></div></td>' 
          
            table = table +  ' </tr>' 
            
            table = table + '<tr> <td colspan="'+str(indexj)+'" id="' + idupdatemessage + '">    </td></tr>'
            
                
            table = table + ' </tbody></table>'
            
           
            return table
    
        except Exception, e:
            print "Message({0}): {1}".format(99, e)    
            return ''
    

    
    def setCatalogPropertyDetail(self):
        try:
            try:
                    self.propertyDetail = CatalogPropertyDetail.objects.filter(  dataproperty  = self.objDataProperty,
                                                                                                                            crystalsystem =self.objCatalogCrystalSystemSelected,
                                                                                                                            type =self.objTypeSelected,
                                                                                                                            catalogpointgroup =self.objCatalogPointGroupSelected,
                                                                                                                             pointgroupnames =self.objPointGroupNamesSelected,
                                                                                                                            catalogaxis=self.objAxisSelected).order_by('name')
                
                
                     
                    #print self.propertyDetail.query                                                                                                  
                    for i,obj in enumerate(self.propertyDetail):
                        self.read_write_inputs[obj.name] = 'w'
                        
                        
                    self.dimensions=self.objDataProperty.tensor_dimensions.split(',')
                    parts=self.objDataProperty.tag.split('_')[-1]
                    self.scij =parts.split('ij')
                    
                    if len(self.dimensions) == 2:
                        for i in range(0,int(self.dimensions[0])):
                            for j  in range(0,int(self.dimensions[1])):  
                                tagindex = str(i +1 )  + str(j + 1)
                                tag = parts.replace('ij',tagindex);
                                if (tag) not in self.read_write_inputs:
                                    self.read_write_inputs[tag] =  "r"  
                        
            except ObjectDoesNotExist as error:
                print "Message({0}): {1}".format(99, error.message)

        
        except Exception, e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            print err
            #self.error = err
                    
                    
    
            
    #*******************************catalogcrystalsystem*************************************        
    def setCrystalSystem(self):
        catalogPointGroup = None
        pointgroupnames_id = None
        try:
            catalogPointGroup=CatalogPointGroup.objects.get(name=self.catalogPointGroupSelectedName) 
            try:
                catalogcrystalsystem_id = CrystalSystemPointGroup.objects.filter(catalogpointgroup=catalogPointGroup).values_list('catalogcrystalsystem_id',flat=True)
                if catalogcrystalsystem_id:
                    self.objCatalogCrystalSystemSelected=CatalogCrystalSystem.objects.get(id=catalogcrystalsystem_id[0])
            except ObjectDoesNotExist as error:
                print "Message({0}): {1}".format(99, error.message)
                
            try:
                pointgroupnames_id= PointGroupGroups.objects.filter(catalogpointgroup=catalogPointGroup ).values_list('pointgroupnames_id',flat=True) 
                pointgroupnames_id= PointGroupNames.objects.filter(id__in=pointgroupnames_id ).values_list('id',flat=True)
                catalogcrystalsystem_id= CrystalSystemPointGroupNames.objects.filter(pointgroupnames_id__in=pointgroupnames_id,type=self.objTypeSelected).values_list('catalogcrystalsystem_id',flat=True)
                self.objCatalogCrystalSystemSelected=CatalogCrystalSystem.objects.get(id=catalogcrystalsystem_id[0])
            except ObjectDoesNotExist as error:
                print "Message({0}): {1}".format(99, error.message)

     
    
        except  Exception as e:         
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            print err
            #self.error = err
            
        
    
    #*******************************catalogpointgroup*************************************           
    def setCatalogPointGroupSelected(self):
        try:
            self.catalogpointgroup_id = 0
            
            self.catalogpointgroup_id = CatalogPointGroup.objects.filter(name__exact=self.catalogPointGroupSelectedName).values_list('id',flat=True)[0]    
            self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(id=self.catalogpointgroup_id)
            
            
            catalogpointgroup_ids= CrystalSystemPointGroup.objects.filter(catalogcrystalsystem=self.objCatalogCrystalSystemSelected,type=self.objTypeSelected,active=1).values_list('catalogpointgroup_id',flat=True)  
            if catalogpointgroup_ids:
                catalogpointgroupQuerySet =  CatalogPointGroup.objects.filter(id__in=self.catalogpointgroup_id)
        
                if self.catalogpointgroup_id in catalogpointgroup_ids:
                    self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(id=self.catalogpointgroup_id)
                else:
                    self.objCatalogPointGroupSelected  = catalogpointgroupQuerySet[0]
            else:
                if self.catalogpointgroup_id in catalogpointgroup_ids:
                    self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(id=self.catalogpointgroup_id)
                else:
                    self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(id=45)           
 
          
        except Exception, e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            error = err     
 
                
     
    #*******************************pointgroupnames*************************************
    def setPointGroupNamesSelected(self):
        try:
            try:
                pointgroupnames_ids= CrystalSystemPointGroupNames.objects.filter(catalogcrystalsystem=self.objCatalogCrystalSystemSelected,type=self.objTypeSelected,active=1).values_list('pointgroupnames_id',flat=True)  
                if pointgroupnames_ids:
                    pointgroupnamesQuerySet = PointGroupNames.objects.filter(id__in=pointgroupnames_ids)
                    for i,pgnobj in enumerate(pointgroupnamesQuerySet):
                        objPointGroupGroups = PointGroupGroups.objects.filter(pointgroupnames=pointgroupnamesQuerySet[i])  
                        #catalogpointgroup_ids = PointGroupGroups.objects.filter(pointgroupnames=pointgroupnamesQuerySet[i]).values_list('catalogpointgroup_id',flat=True)
                        for j,pggobj in enumerate(objPointGroupGroups):
                            if(objPointGroupGroups[j].catalogpointgroup.id ==self.catalogpointgroup_id):
                                self.objPointGroupNamesSelected  = pointgroupnamesQuerySet[i]
            
                    if not self.objPointGroupNamesSelected:
                        for i,pgn in enumerate(pointgroupnamesQuerySet):
                            if self.pointgroupselected_name  in pointgroupnamesParse(pointgroupnamesQuerySet[i].name):
                                self.objPoitGroupNamesSelected  = pointgroupnamesQuerySet[i]
            
                else:  
                    self.objPointGroupNamesSelected  = PointGroupNames.objects.get(id=21)
            
            except ObjectDoesNotExist as error:
                print "Message({0}): {1}".format(99, error.message)
        
        
        
        except  Exception as e:         
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            print err
            #self.error = err
    
            
    #*******************************axis*************************************         
    def setAxisSelected(self):
        try: 
            axis_ids= CrystalSystemAxis.objects.filter(catalogcrystalsystem=self.objCatalogCrystalSystemSelected,
                                                                                            catalogpointgroup= self.objCatalogPointGroupSelected,
                                                                                            pointgroupnames = self.objPointGroupNamesSelected,
                                                                                            type=self.objTypeSelected,active=1).values_list('axis_id',flat=True)  
        
            if axis_ids:
                axisQuerySet = CatalogAxis.objects.filter(id__in=axis_ids)
                self.objAxisSelected  = axisQuerySet[0]
            else:
                    self.objAxisSelected  = CatalogAxis.objects.get(id=4)
            
            
       
        except  Exception as e:         
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            print err
            #self.error = err
 
 
                
                
                

#*******************************data_property*************************************        
    def setDataProperties(self):
        catalogPointGroup = None
        pointgroupnames_id = None
        type_ids = None
        dataproperty_ids = None
        propertyQuerySet = None
        listTag = []
        try:
            catalogPointGroup=CatalogPointGroup.objects.get(name=self.catalogPointGroupSelectedName) 
            try:
                try:
                        try:
                            type_ids = CrystalSystemPointGroup.objects.filter(catalogpointgroup=catalogPointGroup).values_list('type_id',flat=True)  
                            dataproperty_ids = TypeDataProperty.objects.filter(type_id__in=type_ids).values_list('dataproperty_id',flat=True)   
                            propertyQuerySet = Property.objects.filter(id__in=dataproperty_ids, active=True)
                            for i,p in enumerate(propertyQuerySet):
                                listTag.append(p.tag)
                        except ObjectDoesNotExist as error:
                            print "Message({0}): {1}".format(99, error.message)
        
        
                        try:
                            pointgroupnames_ids = PointGroupGroups.objects.filter(catalogpointgroup=catalogPointGroup).values_list('pointgroupnames_id',flat=True) 
                            type_ids = CrystalSystemPointGroupNames.objects.filter(pointgroupnames_id__in=pointgroupnames_ids).values_list('type_id',flat=True)        
                            dataproperty_ids = TypeDataProperty.objects.filter(type_id__in=type_ids).values_list('dataproperty_id',flat=True) 
                            propertyQuerySet = Property.objects.filter(id__in=dataproperty_ids, active=True)
                            for i,p in enumerate(propertyQuerySet):
                                listTag.append(p.tag)

                        except Exception, e:
                            print "Message({0}): {1}".format(99, error.message)
                    
                       
                        self.dataPropertyTempQuerySet=PropertyTemp.objects.filter(tag__in=listTag, active=True)  
                        
                       
                except Exception, e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    err= {}
                    err['file']=fname
                    err['line']=exc_tb.tb_lineno
                    err['error']="Error: {1}".format( e.message, e.args) 
                    print err
                    #self.error = err
                
 
            except Exception, e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                err= {}
                err['file']=fname
                err['line']=exc_tb.tb_lineno
                err['error']="Error: {1}".format( e.message, e.args) 
                print err
                #self.error = err
 
 
             
        
        except  Exception as e:         
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            print err
            #self.error = err
      
           
 