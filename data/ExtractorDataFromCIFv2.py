'''
Created on Nov 25, 2014

@author: Jorge Torres
'''

import os
import re
import string

from django.db import models
from django.db.models import Q
from django.db.models import Count
 
from parse_files_2 import *
from django.core.exceptions import ObjectDoesNotExist
from data.Utils import *
from __builtin__ import setattr

import base64 
from django.utils.encoding import  force_text
import six
import random
import code
from django.db.models.query import QuerySet
#from django.db.transaction import rollback
from django.db import DatabaseError, transaction
from CifMpodValidator import *
import difflib
from django.db import connection


class Extractor (object):
    def __init__(self):
        self.experimentalParCondList=[]
        self.experimentalCond={}
        self.data_code={}
        self.filename= None
        self.article= None
        self.code = 0
        self.dataFile= None
        self.dictionarytext = None
        self.undefinedList=[]
        self.undefinedNameList=[]
        self.user = None
        self.dataFileProperty = None
        self.fileuser = None
 
        self.cifs_dir_custom = None
        self.cifs_dir=  None
        self.cifs_dir_valids= None
        self.cifs_dir_invalids= None
        self.cifs_dir_output=  None
        self.core_dic_filepath=None
        self.mpod_dic_filepath= None
        self.message =  None
        self.error = None
        self.makevalidation = None
        self.data = None
        self.publish= False
        self.paths()
        
        
 

    def paths(self):
        paths = None
        pathslist=Path.objects.all()      
        for path in pathslist:
            if os.path.isdir(path.cifs_dir): 
                #paths = Path()
                #path = paths
                self.cifs_dir= path.cifs_dir 
                self.cifs_dir_valids=path.cifs_dir_valids 
                self.cifs_dir_invalids=path.cifs_dir_invalids 
                self.cifs_dir_output= path.cifs_dir_output 
                self.core_dic_filepath=path.core_dic_filepath 
                self.mpod_dic_filepath=path.mpod_dic_filepath 
                self.datafiles_path =path.mpod_dic_filepath 
                break
            
            
    @classmethod
    def get_nextid(self, mymodel ):
        
        cursor = connection.cursor()
        table = '%s' %  mymodel._meta.db_table
        pkname=mymodel._meta.pk.name
        sql="""SELECT u."""+pkname+""" + 1 AS FirstAvailableCode
                FROM """ + str(table)+ """ u
                LEFT JOIN  """ + str(table)+ """ u1 ON u1."""+pkname+""" = u."""+pkname+""" + 1
                WHERE u1."""+pkname+""" IS NULL
                ORDER BY u."""+pkname+"""
                LIMIT 0, 1"""
        
        
        cursor.execute(sql)
 
        row = cursor.fetchone()
        cursor.close()
        return row[0]
        
    #se usa
    def read_file_1(self, mpod_filepath):
        in_file = open(mpod_filepath, 'r')
        texto = in_file.read()
        in_file.close()
        return texto
    
 
 
        
        
    @classmethod
    def get_data_code_linv2(self, lin):
        l=lin[:-5]
        ml = 0
        try:
            pkname=DataFile._meta.pk.name
            for f in DataFile._meta.fields:
                if f.name == pkname:
                    ml =  f.max_length
                    break
            

            if (len(l) + 1) == ml:
                return int(l)
            else:
                """top = DataFile.objects.order_by('-code')[0]
                return  int(top.code) + 1
                """
                
                code = self.get_nextid(DataFile)
                if code:
                    return  int(code) 
                else:
                    top = DataFile.objects.order_by('-code')[0]
                    return  int(top.code) + 1
                
                

        except Exception  as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            error = err
                
            print("get  code from database")
            code = self.get_nextid(DataFile)
            if code:
                return  int(code) 
            else:
                top = DataFile.objects.order_by('-code')[0]
                return  int(top.code) + 1
                
 
    #se usa
    def props_info_in_dic(self,props):
        props_info = {}
        tgs = ['_name','_category','_type','_units', '_units_detail']
        if self.dictionarytext:
            pass
        else:            
            self.dictionarytext = self.read_file_1(self.mpod_dic_filepath)
 
        
        lins = map(lambda x: x.strip(), self.dictionarytext.strip().split("\n"))
        for prop in props:
            pro_str = "data_prop"+prop
            #print pro_str
            for ii, lin in enumerate(lins):
                ind = None
                if lin.decode('latin-1') == pro_str:
                #if lin.decode('latin-1').startswith(pro_str):
                    ind = ii
                    break
            cond = True
            jj=1
            if ind:
                props_info[prop] = {}
                while cond:
                    pl = lins[ind+jj]
                    if pl:
                        plps = pl.split(None, 1)
                        try:
                            tg, vtg = plps
                        except:
                            cond = False
                        tg =tg.strip().strip("'").strip()
                        vtg =vtg.strip().strip("'").strip()
                        if tg in tgs:
                            indt = tgs.index(tg)
                            props_info[prop][tg] = vtg
                    else:
                        cond = False
                    jj = jj+1
    #                if jj > len(tgs) + 1 :
    #                    cond = False
        #print "hecho"
        return props_info
    
 
        
    
    def extractConditions(self, condition,looped,tensorindex=None):
        tg = '_prop' 
        con = ''
        try:
              
            conds = []
            """
            if self.dataFile == None:
                if self.prepareDataFile():
                    pass
                else:
                    return False
            """
                
            if isinstance(condition, dict):
                cons = condition[tensorindex]
            else:
                cons = condition
    
            for item in cons:
                if isinstance(item, dict):
                    for key,value in item.iteritems():
                        c = '0 ' + key + ' '+  value[0]
                        conds.append(c)
                else:
                    conds.append(item)
                    
            
            for item in conds:
                con = ((item.split())[1]).replace(tg,'')
                val =   ((item.split())[2]).strip().strip("'").strip()
                
                params = {}
                params['tag' ] =tg+con
                dicexist = self.existObjectInDB(Dictionary(), params, 'exact')
                if dicexist:
                    pass
                else:
                    dicexist = Dictionary()
                    dicexist.tag =  tg+con
                    name = con.split('_')
                    name = ' '.join(str(e) for e in name)
                    dicexist.name =   name
                    dicexist.description = con
                    dicexist.units = 'n.a.'
                    dicexist.units_detail = 'n.a.'
                    dicexist.active= True
                    dicexist.definition= ''
                    dicexist.deploy= False
                    dicexist.type = 'char'
                    dicexist.category = Category.objects.get(id=9)
                    dicexist.categorytag =CategoryTag.objects.get(id=1)
                    dicexist.save()
     
                 
                aa = self.props_info_in_dic([con])
                name = con.split('_')
                name = ' '.join(str(e) for e in name)
                na = name
                un = 'n.a.'
                ud = 'n.a.'
                if bool(aa):         
                    try:       
                        na = aa[con]['_name'][6:]
                        try:
                            un = aa[con]['_units']
                        except:
                            un = 'n.a.'
                        try:
                            ud = aa[con]['_units_detail']
                        except:
                            ud = 'n.a.'
                        
                        name = na.split('_')
                        name = ' '.join(str(e) for e in name)
                        dicexist.name  = name
                        dicexist.units  = un 
                        dicexist.units_detail = ud
                        dicexist.save()
    
                        
                    except:
                        if dicexist:
                            na = dicexist.name
                            un = dicexist.units
                            ud = dicexist.units_detail
                        
                else:              
                    pass
                
                
                params = {}
                params['tag' ] =tg+con
                experimentalParCond = None
                epc = None
     
                if isinstance(self.dataFile, DataFile):   
                    
                    epc = self.existObjectInDB(ExperimentalParCond(), params, 'exact')
                    if epc:
                        experimentalParCond = epc
                    else:
                        experimentalParCond= ExperimentalParCond()
    
                elif  isinstance(self.dataFile, DataFileTemp):
                    epc = self.existObjectInDB(ExperimentalParCondTemp(), params, 'exact')
                    if epc:
                        experimentalParCond = epc
                    else:
                        experimentalParCond= ExperimentalParCondTemp()
    
                else:
                    return False
                
            
                if not epc:
                    experimentalParCond.tag=tg+con
                    experimentalParCond.description=  con
                    name = con.split('_')
                    name = ' '.join(str(e) for e in name)
                    experimentalParCond.name  = na
                    experimentalParCond.units  = un 
                    experimentalParCond.units_detail = ud
                    experimentalParCond.description =''
                    experimentalParCond.save()
     
                if looped:
                    params= {}
                    if isinstance(epc, ExperimentalParCondTemp):
                        propertyConditionDetail  = PropertyConditionDetailTemp()
                        params['condition_id' ] = experimentalParCond.id
                        params[ 'datafileproperty_id'] = self.dataFileProperty.id
                        params[ 'tensorindex'] = tensorindex
                         
                    elif isinstance(epc, ExperimentalParCond):
                        propertyConditionDetail  = PropertyConditionDetail()
                        params['condition_id' ] = experimentalParCond.id
                        params[ 'datafileproperty_id'] = self.dataFileProperty.id
                        params[ 'tensorindex'] = tensorindex
                        
                        
                        
                    res = self.existObjectInDB(propertyConditionDetail, params)
                    if res:
                        if isinstance(res, propertyConditionDetail.__class__):
                            propertyConditionDetail = res

                        if isinstance(res, QuerySet):
                            for pcd in res:
                                pcd.delete()
                        
                         
                        if str(propertyConditionDetail.value)   !=  str(val): 
                            for key, value in params.iteritems():
                                if propertyConditionDetail.__dict__.has_key(key):
                                    propertyConditionDetail.__dict__[key] = value
                                    propertyConditionDetail.value  = val 
                              
                            propertyConditionDetail.save()
                            
                    else:
                        for key, value in params.iteritems():
                            #propertyConditionDetail = propertyConditionDetail.__class__
                            if propertyConditionDetail.__dict__.has_key(key):
                                propertyConditionDetail.__dict__[key] = value
                                
                        propertyConditionDetail.value = val
                        propertyConditionDetail.save()
                  
     
    
    
                else:
     
                    params= {}
                    if isinstance(epc, ExperimentalParCondTemp):
                        experimentalParCondDataFile  = ExperimentalParCondTemp_DataFileTemp()
                        params['experimentalfilecontemp_id' ] = experimentalParCond.id
                        params[ 'datafiletemp_id'] = self.dataFile.id
                        params[ 'data'] = self.data
                         
                    elif isinstance(epc, ExperimentalParCond):
                        experimentalParCondDataFile  = ExperimentalParCond_DataFile()
                        params['experimentalfilecon_id' ] = experimentalParCond.id
                        params[ 'datafile_id'] = self.dataFile.code
                        params[ 'data'] = self.data
                         
                        #val
                        
                    res = self.existObjectInDB(experimentalParCondDataFile, params)
                    if res:
                        if isinstance(res, experimentalParCondDataFile.__class__):
                            experimentalParCondDataFile = res 
 
                        if isinstance(res, QuerySet):
                            for epcdf in res:
                                epcdf.delete()
                           
                        if str(experimentalParCondDataFile.value) != str(val):
                            experimentalParCondDataFile.value = str(val)
                            experimentalParCondDataFile.data = self.data
                            experimentalParCondDataFile.save()
                        
                        
                    else:
                        experimentalParCondDataFile= experimentalParCondDataFile.__class__()
                        for key, value in params.iteritems():
                            if experimentalParCondDataFile.__dict__.has_key(key):
                                if key != 'data':
                                    experimentalParCondDataFile.__dict__[key] = value
                                else:
                                    experimentalParCondDataFile.__dict__[key] = value
                                    
                                
                        experimentalParCondDataFile.value = str(val)
                        experimentalParCondDataFile.save()
                        
                        
            return True
 
        except  Exception as e:
            #self.error ="Error in the function extractProperties for debug purposes.  Error: {1}".format( e.message, e.args)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            self.error = err
            
            
            params['tag' ] =tg+con
            epc = self.existObjectInDB(ExperimentalParCond(), params, 'exact')
            if  looped:
                if isinstance(epc, ExperimentalParCondTemp):
                    propertyConditionDetail  = PropertyConditionDetailTemp()
                    params['condition_id' ] = experimentalParCond
                    params[ 'datafileproperty_id'] = self.dataFileProperty
                   
                     
                elif isinstance(epc, ExperimentalParCond):
                    propertyConditionDetail  = PropertyConditionDetail()
                    params['condition_id' ] = experimentalParCond
                    params[ 'datafileproperty_id'] = self.dataFileProperty

                        
                res = self.existObjectInDB(self.dataFileProperty, params)
                if res:
                    if isinstance(res, self.dataFileProperty.__class__):
                        res.delete()
   
                    elif isinstance(res, QuerySet):
                        for dfp in res:
                                dfp.delete()
                    
                    else:
                        pass
 
                            
            else:
                params = {}
                if isinstance(self.dataFile, DataFile):  
                    params[ 'datafile_id'] = self.dataFile
 
                elif  isinstance(self.dataFile, DataFileTemp):
                    params[ 'datafiletemp_id'] = self.dataFile
                    
                #rollback
                if isinstance(self.dataFile, DataFile):   
                    epc = self.existObjectInDB(ExperimentalParCond_DataFile(), params)
                    if epc:
                        if isinstance(epc, ExperimentalParCond_DataFile):
                            epc.delete()
                        elif isinstance(epc, ):
                            for ep in epc:
                                ep.delete()
                        else:
                            pass
                elif isinstance(self.dataFile, DataFileTemp):
                    epc = self.existObjectInDB(ExperimentalParCond_DataFile(), params)
                    if epc:
                        if isinstance(epc, ExperimentalParCondTemp_DataFileTemp):
                            epc.delete()
                        elif isinstance(epc, ):
                            for ep in epc:
                                ep.delete()
                        else:
                            pass
                        
                        
            if self.dataFile:
                self.dataFile.delete()
                
            if self.dataFileProperty:   
                self.dataFileProperty.delete()
            
            if self.article:
                if isinstance(self.article, QuerySet):
                    pass
                else:
                    pass
            
            
            self.dataFile = None
            self.dataFileProperty= None
            self.article = None
            
            return False
    
    def extractUndefined(self,undefined):
        
        try:
            und = None
            undefinedlist = []
            for item in undefined:
                und = (item.split())[1]
                undefinedlist.append(und)
                
            if undefinedlist:
                for i,und in enumerate(undefinedlist):
                    dictionary=Dictionary() 
                    value = (undefined[i].split())[2:]
                    dictionary.tag =  und
                    lcs = und.split('_')
                    name= ' '.join(str(e) for e in lcs[1:])
                    dictionary.name =  name
                    cat=Category.objects.get(id=9)
                    dictionary.description = name
                    dictionary.units = 'n.a.'
                    dictionary.units_detail = 'n.a.'
                    dictionary.active= True
                    dictionary.definition= ''
                    dictionary.deploy= False
                    dictionary.type = 'char'   
                    dictionary.category = cat
                    dictionary.categorytag = CategoryTag.objects.get(id=6)
                    self.undefinedList.append(dictionary)
                    self.undefinedNameList.append(und)
                    
            return True
                    
        except  Exception as e:
            
            #self.error ="Error in the function extractProperties for debug purposes.  Error: {1}".format( e.message, e.args)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            self.error = err
            return False
        
        
        
    def force_bytes(self,value):
        if isinstance(value, six.string_types):
            return value.encode()
        return value

    def extractOther(self, other, section):
        try:
            und = None
            otherlist = []
            valuesDict = {}
            tagName = ''
            val = []
            objecToSave = None
            for item in other:
                oth = (item.split()) 
                if oth[1].startswith('_') :
                    if len(oth) == 2:
                        tagName = oth[1]
                        valuesDict[oth[1]] = []
                        val = []
                    elif len(oth) > 2:
                        val= ' '.join(str(e) for e in oth[2:])
                        valuesDict[oth[1]] = val
     
                else:
                    val1= ' '.join(str(e) for e in oth[1:])
                    val += [val1]
                    valuesDict[tagName] = val
                 
         
            if valuesDict:  
                #--------------------------------------------------------article--------------------------------------------------------------------------
                if  section == 'article':
                    categoryTagObj= CategoryTag.objects.get(id=3)
                    tags= list( Dictionary.objects.filter(categorytag=categoryTagObj,active = True).values_list('tag',flat=True))
     
                    modelfieldsdatatype = {}
                    if self.article:
                        objecToSave = self.article
                    else:
                        if isinstance(self.dataFile, DataFile):
                            objecToSave=PublArticle()
                        else:
                            objecToSave=PublArticleTemp()
                        
                     
                         
     
                    dictionaryfields = {}
                    dictionaryfields['_publ_author_name'] =  'authors'    
                    dictionaryfields['_publ_section_title'] =  'title'    
                    dictionaryfields['_journal_name_full'] =  'journal'          
                    dictionaryfields['_journal_year'] =  'year'
                    dictionaryfields['_journal_volume']='volume'
                    dictionaryfields['_journal_issue']= 'issue'
                    dictionaryfields['_journal_page_first' ] ='first_page'
                    dictionaryfields['_journal_page_last']  = 'last_page'
                    dictionaryfields['_journal_article_reference'] = 'reference'
                    dictionaryfields['_journal_pages_number']   = 'pages_number' 
                        
                        
                    for key, value in valuesDict.iteritems():
                        if key not in tags:
                            tags.append(str(key))
                            
                        for i, und in enumerate(self.undefinedNameList):
                            if key == und: 
                                self.undefinedList[i].categorytag = categoryTagObj       
                            
                    if isinstance(objecToSave, PublArticle):
                        for k, v in dictionaryfields.iteritems():
                                for f in PublArticle._meta.fields:
                                    if f.name == v:
                                        modelfieldsdatatype[v]= type(f)
                        
                    elif isinstance(objecToSave, PublArticleTemp):
                            for k, v in dictionaryfields.iteritems():
                                    for f in PublArticleTemp._meta.fields:
                                        if f.name == v:
                                            modelfieldsdatatype[v]= type(f)
    
    
                #--------------------------------------------------------material--------------------------------------------------------------------------
                elif section == 'material': 
                    categoryTagObj= CategoryTag.objects.get(id=4)
                    tags= list( Dictionary.objects.filter(categorytag=categoryTagObj,active = True).values_list('tag',flat=True))
                    dictionaryfields = {}
    
                #--------------------------------------------------------general--------------------------------------------------------------------------
                elif section == 'general': 
                    #gen_tags = ['_cod_database_code', '_phase_generic', '_phase_name', '_chemical_formula_sum', '_chemical_formula']
                    categoryTagObj= CategoryTag.objects.get(id=5)
                    tags= list( Dictionary.objects.filter(categorytag=categoryTagObj,active = True).values_list('tag',flat=True))
                    
                    dictionaryfields = {}
                    dictionaryfields['_cod_database_code'] =  'cod_code'    
                    dictionaryfields['_phase_generic'] =  'phase_generic'    
                    dictionaryfields['_phase_name'] =  'phase_name'    
                    dictionaryfields['_chemical_formula_sum'] =  'chemical_formula'          
                    dictionaryfields['_chemical_formula'] =  'chemical_formula'   
                    dictionaryfields['publication'] =  'publication_id'   
                    #dictionaryfields['filename'] =  'filename'   
                    
                    modelfieldsdatatype = {}
                    for k, v in dictionaryfields.iteritems():
                        for f in self.dataFile._meta.fields:
                            if f.name == v:
                                modelfieldsdatatype[f.name]= type(f)
                                break
                            elif v.endswith('_id'):
                                v2 = v.replace('_id','')
                                if f.name == v2:
                                    modelfieldsdatatype[f.name]= type(f)
                                    break
                        
                    tags += ['publication']
                    valuesDict['publication'] = 'publication_id'
    
                    objecToSave = self.dataFile
                    
                if objecToSave:
                    for key, value in valuesDict.iteritems():
                        print key, value
                        
                        if dictionaryfields:
                            for k, v in dictionaryfields.iteritems():
                                if dictionaryfields.has_key(key):
                                    if v == 'authors' and k in tags:
                                        aut=''
                                        authors = value
                                        for a in authors:
                                            coma=''
                                            if aut != '':
                                                coma='; '   
                                            else:
                                                coma='' 
                                            
                                            a1 = a.strip().strip("'").strip()
                                            a2 = a.strip().strip("'").strip()
                                            aut=aut.decode('latin-1') + coma + a1.decode('latin-1')
                            
                                        if objecToSave.__dict__.has_key(v):
                                            objecToSave.__dict__[v] = aut
                                            tags.remove(key)
                                            
                                        break
                                            
                                    elif v == 'title' and k in tags:
                                        title = ''
                                        for item in value:
                                            #title += item
      
                                            try:
                                                title += item.decode('latin-1')
                                            except  Exception as e:
                                                title += item 
                                            
                                        if objecToSave.__dict__.has_key(v):
                                            objecToSave.__dict__[v] = title
                                            tags.remove(key)
                            
                                        break
                                    
                                    elif  v == 'publication_id' and k in tags:
                                        if objecToSave.__dict__.has_key(v):
                                            params = {}
                                            art = None
                                            if self.article:
                                                params['authors' ] =self.article.authors
                                                params['journal'] = self.article.journal
                                                params['year']  =self.article.year
                                                
                                            else:
                                                params['authors' ] ='?;'
                                                params['journal'] = '?'
                                                params['year']  = 0
                                                
                                                if isinstance(self.dataFile, DataFile):
                                                    self.article =  PublArticle()
                                                elif isinstance(self.dataFile, DataFileTemp):
                                                    self.article = PublArticleTemp()

                                                
                                            art = self.existObjectInDB(self.article, params, 'exact')
                                            if not isinstance(art, QuerySet):
                                                if art:
                                                    values = {}
                                                    other_values = {}
                                                    
                                                    for kar,var in self.article.__dict__.iteritems():
                                                        if kar == '_state':
                                                            pass
                                                        elif kar == 'id':
                                                            pass
                                                        else:
                                                            other_values[kar] = var
                                                            values[kar] = art.__dict__[kar]
        
                                                    
                                                    fieldupdate = []
                                                    if other_values == values:
                                                        self.article = art
                                                    else:
                                                        fieldupdate =  set(other_values.items() ) - set(values.items()) 
                                                        print fieldupdate
                                                        for e in fieldupdate:
                                                            art.__dict__[e[0]]=e[1]
                                                            self.article = art

                                                    self.dataFile.__dict__[v] = self.article
                                                else:
                                                    self.dataFile.__dict__[v] = self.article
                                                    
                                                
                                            else:
                                                pass
 
                                            
                                            tags.remove(key)
                                        break
                                            
                                    else:
                                        if key == k:
                                            if modelfieldsdatatype[v] == models.IntegerField:
                                                if objecToSave.__dict__.has_key(v):
                                                    if value != '?':
                                                        objecToSave.__dict__[v] = int(value.strip().strip("'").strip())
                                                    else:
                                                        objecToSave.__dict__[v] = int(0)
                                                        
                                                    tags.remove(key)
          
                                            elif modelfieldsdatatype[v] == models.FloatField:
                                                if objecToSave.__dict__.has_key(v):
                                                    if value != '?':
                                                        objecToSave.__dict__[v] = int(value.strip().strip("'").strip())
                                                    else:
                                                        objecToSave.__dict__[v] = int(0)
                                                        
                                                    tags.remove(key)
    
                                            else:
                                                if objecToSave.__dict__.has_key(v):
                                                    if isinstance(value, list):
                                                        nv=''
                                                        for a in value:
                                                            coma=''
                                                            if nv != '':
                                                                coma='; '   
                                                            else:
                                                                coma='' 
                                                            
                                                            nv=nv + coma + a.strip().strip("'").strip()
                                                         
                                                        objecToSave.__dict__[v] = nv
                                                    else:
                                                        objecToSave.__dict__[v] = value.strip().strip("'").strip()
                                                    
                                                    tags.remove(key)
                                                
                                                    
                                                    
                                                    
                                            break
                        else:        
                            break        
                   
             
                else:
                    pass
                
                
                #--------------------------------------------------------article--------------------------------------------------------------------------
                if  section == 'article':    
                    params = {}
                    try:
                        params['authors' ] =objecToSave.authors.decode('latin-1')
                        params['journal'] = objecToSave.journal.decode('latin-1')
                    except  Exception as e:
                        params['authors' ] =objecToSave.authors
                        params['journal'] = objecToSave.journal
                        
                    
                    params['year']  =objecToSave.year 
                    
                    art = self.existObjectInDB(objecToSave, params, 'exact')
                    
                    if art:
                        self.article = art           
                    else:
                        self.article  = objecToSave
                        
                   
                    self.article.save()  
                 
 
                    #print self.article 
 
                #--------------------------------------------------------general--------------------------------------------------------------------------               
                elif section == 'general':      
                    #self.dataFile= objecToSave
                    self.dataFile.save()
                    print self.dataFile 
 
                return True
                
        except  Exception as e:
            
            #self.error ="Error in the function extractProperties for debug purposes.  Error: {1}".format( e.message, e.args) 
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            self.error = err
            
            params = {}
            if isinstance(self.dataFile, DataFile):  
                params[ 'datafile_id'] = self.dataFile
            
            elif  isinstance(self.dataFile, DataFileTemp):
                params[ 'datafiletemp_id'] = self.dataFile


            #rollback
            if isinstance(self.dataFile, DataFile):   
                epc = self.existObjectInDB(ExperimentalParCond_DataFile(), params)
                if epc:
                    if isinstance(epc, ExperimentalParCond_DataFile):
                        epc.delete()
                    elif isinstance(epc, ):
                        for ep in epc:
                            ep.delete()
                    else:
                        pass
            elif isinstance(self.dataFile, DataFileTemp):
                epc = self.existObjectInDB(ExperimentalParCond_DataFile(), params)
                if epc:
                    if isinstance(epc, ExperimentalParCondTemp_DataFileTemp):
                        epc.delete()
                    elif isinstance(epc, ):
                        for ep in epc:
                            ep.delete()
                    else:
                        pass
                    
                    
            if self.dataFile:
                self.dataFile.delete()
                
            if self.dataFileProperty:
                self.dataFileProperty.delete()
                
            if self.article:
                if isinstance(self.article, QuerySet):
                    pass
                else:
                    self.article.delete()
            
            self.dataFile = None
            self.dataFileProperty= None
            self.article = None
            
            return False
 
            
             
    def existObjectInDB(self,model, fields, operator=None):
        kwargs = {}
        for kar,var in model.__dict__.iteritems():
            if kar == '_state':
                pass
            elif kar == 'id':
                pass
            else:
                if fields.has_key(kar):
                    if isinstance(fields, dict):
                        if operator:
                            kwargs['{0}__{1}'.format(kar, operator)] = fields[kar]
                        else:
                                kwargs['{0}'.format(kar)] = fields[kar]
                            
        art = None                   
        if isinstance(model, DataFile):
            art= list((model.__class__).objects.filter(**kwargs).values_list('code',flat=True))
        else:
            art= list((model.__class__).objects.filter(**kwargs).values_list('id',flat=True))
        
        if art:
            if isinstance(model, DataFile):
                if len(art) == 1:
                    res = (model.__class__).objects.get(code=art[0])
                else:
                    res = (model.__class__).objects.filter(code__in=art)
            else:
                if len(art) == 1:
                    res = (model.__class__).objects.get(id=art[0])
                else:
                    res = (model.__class__).objects.filter(id__in=art)
 
            return res
        else:
            return None


    def prepareDataFile(self):
        
        try:

            dataFileObj= None
            dataFileTempObj = None
            code = self.data_code['code'] 
            filenametemp = None
            filenamecode = None
            params = {}
            params['filename'] = self.filename
            fd = self.existObjectInDB(DataFile(), params, 'exact')
            
            if fd:
                dataFileObj= fd #DataFile.objects.get(filename__exact=str(self.filename))
                params = {}
                params['datafile_id'] = dataFileObj.code
                fn = self.existObjectInDB(FileUser(), params)
                if fn:
                        self.fileuser = fn
                        dataFileTempObj=DataFileTemp.objects.get(filename__exact=str(fn.filename)) 
                        filenametemp = str(fn.filename)
                else:
                        name_str = lambda n: ''.join([random.choice(string.lowercase) for i in xrange(n)])
                        usernamebase64= base64.b64encode(self.force_bytes(str(self.user.username)))
                        newusernamebase64 = usernamebase64.replace("==", "")
                        filenametemp = newusernamebase64.lower() + name_str(15) + ".mpod"
            
            else:
                params = {}
                params['filename'] = self.filename
                fd = self.existObjectInDB(DataFileTemp(), params, 'exact')
                if fd:
                    filenametemp = self.filename
                    dataFileTempObj= fd
                    params = {}
                    params['filename'] = self.filename
                    fn = self.existObjectInDB(FileUser(), params, 'exact')
                    if fn:
                        self.fileuser = fn
                        dataFileObj=fn.datafile
                        if dataFileObj:
                            self.filename = dataFileObj.filename
                        else:
                            self.filename = str(code) + '.mpod'
                            
                    else:
                        self.filename = str(code) + '.mpod'
            
                else:
                    #filenametemp = self.filename
                    #self.filename = str(code) + '.mpod'
                    if self.cifs_dir_custom:
                        name_str = lambda n: ''.join([random.choice(string.lowercase) for i in xrange(n)])
                        usernamebase64= base64.b64encode(self.force_bytes(str(self.user.username)))
                        newusernamebase64 = usernamebase64.replace("==", "")
                        filenametemp = newusernamebase64.lower() + name_str(15) + ".mpod"
                      
            
            
            if dataFileObj and dataFileTempObj: # published by system
                print self.filename
                print filenametemp
                print dataFileObj.code
                print dataFileTempObj.code
                self.data_code['code'] = dataFileObj.code
                self.message = 'el archivo ya esta publicado'
                
                validator = None
                if self.makevalidation:
                    #validator = CifMpodValidator(str(self.cifs_dir),str(self.core_dic_filepath),str(self.mpod_dic_filepath ),  [str(dataFileTempObj.filename)])
                    validator = CifMpodValidator(str(self.cifs_dir_valids),str(self.core_dic_filepath),str(self.mpod_dic_filepath ) , [str(filenametemp)])
                    try:
                        validator.getValidation()
                    except Exception  as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        err= {}
                        err['file']=fname
                        err['line']=exc_tb.tb_lineno
                        err['error']="Error: {1}".format( e.message, e.args) 
                        self.error = err
                        #self.error =  e
                        validator = exc_obj
                    

                self.fileuser.publish=  True
    
                if validator:
                    if isinstance(validator, CifMpodValidator):
                        objectValidateds=validator.resultListVaild
                        for objectValidated in objectValidateds:
                            print objectValidated
                            self.fileuser.reportvalidation =objectValidated
                    else:
                        self.fileuser.reportvalidation = validator


                if self.publish:
                    #self.data = str(dataFileObj.code)
                    self.dataFile=dataFileObj
                    self.dataFile.active = True
                else:
                    self.dataFile=dataFileTempObj
                        
                return True
                
            elif dataFileObj and dataFileTempObj == None:  #exists before being published by the system
                validator = None
                if self.makevalidation:
                    validator = CifMpodValidator(str(self.cifs_dir),str(self.core_dic_filepath),str(self.mpod_dic_filepath ),  [str(dataFileObj.filename)])
                    try:
                        validator.getValidation()
                    except Exception  as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        err= {}
                        err['file']=fname
                        err['line']=exc_tb.tb_lineno
                        err['error']="Error: {1}".format( e.message, e.args) 
                        self.error = err
                        #self.error =  e
                        validator = exc_obj
                         
                
                
                if not self.fileuser:
                    self.fileuser = FileUser()
                    
                
                self.fileuser.filename = filenametemp
                self.fileuser.authuser = self.user
                self.fileuser.publish=  True
    
                if validator:
                    if isinstance(validator, CifMpodValidator):
                        objectValidateds=validator.resultListVaild
                        for objectValidated in objectValidateds:
                            print objectValidated
                            self.fileuser.reportvalidation =objectValidated
                    else:
                        self.fileuser.reportvalidation = validator
                    

                self.dataFile=DataFileTemp()
                self.dataFile.code = code
                
                self.dataFile.filename = filenametemp
                self.dataFile.save()
                
                if not self.fileuser.datafile:
                    self.fileuser.datafile=dataFileObj
                    
                return True

 
                
            elif dataFileObj == None and dataFileTempObj == None: #File created  externally.
                print self.filename
                print filenametemp
                
                validator = None
                if not self.cifs_dir_custom:
                    validator = CifMpodValidator(str(self.cifs_dir_valids),str(self.core_dic_filepath),str(self.mpod_dic_filepath ) , [str(self.filename)])
                else:
                    validator = CifMpodValidator(str(self.cifs_dir_custom),str(self.core_dic_filepath),str(self.mpod_dic_filepath ), [str(self.filename)])
                    
                    
                try:
                    validator.getValidation()
                except Exception  as e:
                    #self.error =  e
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    err= {}
                    err['file']=fname
                    err['line']=exc_tb.tb_lineno
                    err['error']="Error: {1}".format( e.message, e.args) 
                    self.error = err
                  
                    validator = exc_obj
                
                                
                if not self.fileuser:
                    self.fileuser = FileUser()
                    
                self.fileuser.filename = filenametemp
                self.fileuser.authuser = self.user
                self.fileuser.publish=  False
    
                if validator:
                    if isinstance(validator, CifMpodValidator):
                        objectValidateds=validator.resultListVaild
                        for objectValidated in objectValidateds:
                            print objectValidated
                            self.fileuser.reportvalidation =objectValidated
                    else:
                        self.fileuser.reportvalidation = validator
                    
                self.dataFile=DataFileTemp()
                #self.dataFile.code = code
                self.dataFile.filename = filenametemp
                self.dataFile.save()
                
                
                return True
     
 
                
            elif dataFileObj == None and dataFileTempObj: #file created by a user to be published by the system
                validator = None
                if self.makevalidation:
                    validator = CifMpodValidator(str(self.cifs_dir_valids),str(self.core_dic_filepath),str(self.mpod_dic_filepath ),  [str(dataFileTempObj.filename)])
                    try:
                        validator.getValidation()
                    except Exception  as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        err= {}
                        err['file']=fname
                        err['line']=exc_tb.tb_lineno
                        err['error']="Error: {1}".format( e.message, e.args) 
                        self.error = err
                        #self.error =  e
                        validator = exc_obj
                
                
                if not self.fileuser:
                    self.fileuser = FileUser()
                    
                    
                if validator:
                    if isinstance(validator, CifMpodValidator):
                        objectValidateds=validator.resultListVaild
                        for objectValidated in objectValidateds:
                            print objectValidated
                            self.fileuser.reportvalidation =objectValidated
                    else:
                        self.fileuser.reportvalidation = validator
                        
                        
 
                self.fileuser.filename = filenametemp
                self.fileuser.authuser = self.user
                if self.publish:
                    self.fileuser.publish=  True
 
                    params = {}
                    params['code'] = code
                    ex = self.existObjectInDB(DataFile(), params, 'exact')
                    if not ex:
                        self.dataFile=DataFile()
                        dataFileTempObj.code = code
                        dataFileTempObj.save()
                        self.dataFile.code = code
                        self.dataFile.active = True
                        self.dataFile.filename = self.filename
                        self.dataFile.save()
                    else:
                        self.message = "Recently used code, try again"
                
                        return False
                    
                    if not self.fileuser.datafile:
                        self.fileuser.datafile=self.dataFile
                else:
                    self.dataFile= dataFileTempObj
                    
                    
                return True
 
                        
                
        except Exception  as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            self.error = err
            
            #rollback
            self.fileuser = None
            if self.dataFile:
                self.dataFile.delete()
                
            self.dataFile = None
   
            return False

            
    def extractProperties(self,properties,looped, tensorvalues,tensorindex):
        tg="_prop"
        props = None
        short_tag = None
        try: 
            
            if isinstance(properties, list):
                props = properties[0].replace(tg,'')
                short_tag = properties[1].strip().strip("'").strip()
            else:
                props = (properties.split())[1]
 
            params = {}
            params['tag' ] =tg+props
            dicexist = self.existObjectInDB(Dictionary(), params, 'exact')
            if dicexist:
                pass
            else:
                dicexist = Dictionary()
                dicexist.tag = tg+props
                name = (tg + props).split('_')
                name = ' '.join(str(e) for e in name)
                dicexist.name =   name
                description = (props[1:]).split('_')
                dicexist.description = ' '.join(str(e) for e in description)
                dicexist.units = 'n.a.'
                dicexist.units_detail = 'n.a.'
                dicexist.active= True
                dicexist.definition= ''
                dicexist.deploy= False
                dicexist.type = 'char'
                dicexist.category = Category.objects.get(id=9)
                dicexist.categorytag =CategoryTag.objects.get(id=1)
                dicexist.save()
 
             
            aa = self.props_info_in_dic([props])
            name = (tg + props).split('_')
            name = ' '.join(str(e) for e in name)
            na = name
            un = 'n.a.'
            ud = 'n.a.'
            if bool(aa):         
                try:       
                    na = aa[props]['_name'][1:]
                    
                    try:
                        un = aa[props]['_units']
                    except:
                        un = 'n.a.'
                    try:
                        ud = aa[props]['_units_detail']
                    except:
                        ud = 'n.a.'
                    
                    name = na.split('_')
                    name = ' '.join(str(e) for e in name)
                    dicexist.name  = name
                    dicexist.units  = un 
                    dicexist.units_detail = ud
                    description = (na.split('_'))[1:]
                    dicexist.description = ' '.join(str(e) for e in description)
                    dicexist.save()

                    
                except:
                    if dicexist:
                        na = dicexist.name
                        un = dicexist.units
                        ud = dicexist.units_detail
                    
            else:              
                pass
            
            
            params = {}
            params['tag' ] =tg+props
            objProperty = None
            pr = None
 
            if isinstance(self.dataFile, DataFile):    
                pr = self.existObjectInDB(Property(), params, 'exact')
                if pr:
                    objProperty = pr
                else:
                    objProperty= Property()

            elif  isinstance(self.dataFile, DataFileTemp):
                pr = self.existObjectInDB(PropertyTemp(), params, 'exact')
                if pr:
                    objProperty = pr
                else:
                    objProperty= PropertyTemp()
                    
                    
                if objProperty.short_tag==None:
                    objProperty.short_tag = short_tag
                    objProperty.save()

            else:
                return False

    
            
            if not pr:
                objProperty.tag =  tg+props
                name = (tg + props).split('_')
                name = ' '.join(str(e) for e in name)
                objProperty.name =  name
                description = (props[1:]).split('_')
                objProperty.description = ' '.join(str(e) for e in description)
                #objProperty.tensor_dimensions =  ''
                objProperty.units  = un 
                objProperty.units_detail = ud
                objProperty.short_tag = short_tag
                objProperty.active = False
    
                objProperty.save()
                
                
                
            self.dataFileProperty = None
 
            if looped:
                """
                 _prop_data_label
                 _prop_data_tensorial_index
                 _prop_data_value
                """
                pass
 
            else:

                params= {}
                if isinstance(pr, PropertyTemp):
                    self.dataFileProperty  = DataFilePropertyTemp()
                    params['propertytemp_id' ] = objProperty.id
                    params[ 'datafiletemp_id'] = self.dataFile.id
                     
                elif isinstance(pr, Property):
                    self.dataFileProperty = DataFileProperty()
                    params['property_id' ] = objProperty.id
                    params[ 'datafile_id'] = self.dataFile.code
 
                res = self.existObjectInDB(self.dataFileProperty, params)
                if res:
                    if isinstance(res, self.dataFileProperty.__class__):
                        self.dataFileProperty = res
   
                    elif isinstance(res, QuerySet):
                        pass
                    
                    else:
                        pass
                else:
                    for key, value in params.iteritems():
                        if self.dataFileProperty.__dict__.has_key(key):
                            self.dataFileProperty.__dict__[key] = value
                    
                    self.dataFileProperty.save()        
                    #experimentalParCondDataFile.value = val
                    
                                        

                        
                propertyValues=  None     
                if tensorvalues:
                    params= {}
                    if isinstance(pr, PropertyTemp):
                        propertyValues= PropertyValuesTemp()
                        params['datafilepropertytemp_id' ] = self.dataFileProperty.id
                        params['tensorindex' ] = tensorindex
                         
                    elif isinstance(pr, Property):
                        propertyValues= PropertyValues()
                        params['datafileproperty_id' ] = self.dataFileProperty.id
                        params['tensorindex' ] = tensorindex

 
                    #dimensions= [len(tensorvalues[tensorindex]),  len(tensorvalues[tensorindex][1])]
                    tensorvalueslist=tensorvalues[tensorindex]
                    
                    dimensions=[]
                    if isinstance(tensorvalueslist, list):
                        dimensions.append(len(tensorvalueslist))
                        if isinstance(tensorvalueslist[0], list):
                            dimensions.append(len(tensorvalueslist[0]))
                        else:
                            pass
                        
                    
                    res = self.existObjectInDB(propertyValues, params)
                    if len(dimensions) ==2:
                        if res:
                            if isinstance(res, propertyValues.__class__):
                                res.delete()
                                
                            if isinstance(res, QuerySet):
                                    for pv in res:
                                        pv.delete()

                            for i in range(int(dimensions[0])):
                                for j in range(int(dimensions[1])):
                                    if tensorvalueslist[i][j] != '0':
                                        propertyValues = propertyValues.__class__()
                                        if isinstance(self.dataFileProperty, DataFilePropertyTemp):
                                            propertyValues.datafilepropertytemp= self.dataFileProperty
                                        else:
                                            propertyValues.datafileproperty= self.dataFileProperty
                                            
                                        propertyValues.label=  short_tag
                                        propertyValues.tensorial_index=  str(i +1) + str(j +1)
                                        propertyValues.value  =   tensorvalueslist[i][j]
                                        propertyValues.tensorindex = tensorindex
                                        propertyValues.save()
         
                        else:
                            for i in range(int(dimensions[0])):
                                for j in range(int(dimensions[1])):
                                    if tensorvalueslist[i][j] != '0':
                                        propertyValues = propertyValues.__class__()
                                        if isinstance(self.dataFileProperty, DataFilePropertyTemp):
                                            propertyValues.datafilepropertytemp= self.dataFileProperty
                                        else:
                                            propertyValues.datafileproperty= self.dataFileProperty
                                            
                                        propertyValues.label=  short_tag
                                        propertyValues.tensorial_index=  str(i +1) + str(j +1)
                                        propertyValues.value  =   tensorvalueslist[i][j]
                                        propertyValues.tensorindex = tensorindex
                                        propertyValues.save()
                                        
                                        
                    elif len(dimensions) == 1:
                        if res:
                            if isinstance(res, propertyValues.__class__):
                                res.delete()
                                
                            if isinstance(res, QuerySet):
                                    for pv in res:
                                        pv.delete()
                                        
                                        
                            for i in range(int(dimensions[0])):
                                if tensorvalueslist[i] != '0':
                                    propertyValues = propertyValues.__class__()
                                    if isinstance(self.dataFileProperty, DataFilePropertyTemp):
                                        propertyValues.datafilepropertytemp= self.dataFileProperty
                                    else:
                                        propertyValues.datafileproperty= self.dataFileProperty
                                        
                                    propertyValues.label=  short_tag
                                    #propertyValues.tensorial_index=  str(i +1) + str(j +1)
                                    propertyValues.value  =   tensorvalueslist[i]
                                    propertyValues.tensorindex = tensorindex
                                    propertyValues.save()
                                    
                        else:               
                            for i in range(int(dimensions[0])):
                                if tensorvalueslist[i] != '0':
                                    propertyValues = propertyValues.__class__()
                                    if isinstance(self.dataFileProperty, DataFilePropertyTemp):
                                        propertyValues.datafilepropertytemp= self.dataFileProperty
                                    else:
                                        propertyValues.datafileproperty= self.dataFileProperty
                                        
                                    propertyValues.label=  short_tag
                                    #propertyValues.tensorial_index=  str(i +1) + str(j +1)
                                    propertyValues.value  =   tensorvalueslist[i]
                                    propertyValues.tensorindex = tensorindex
                                    propertyValues.save()
                    
                        
                        
                else:
                    pass
 
                    
            return True
                        
            
        except  Exception as e:
           
            #self.error = "Error in the function extractProperties for debug purposes.  Error: {1}".format( e.message, e.args) 
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            self.error = err
            
            if  looped:
                pass
            else:
                params = {}
                #rollback
                if isinstance(self.dataFile, DataFile):   
                    params[ 'datafile_id'] = self.dataFile
                    epc = self.existObjectInDB(ExperimentalParCond_DataFile(), params)
                    if epc:
                        if isinstance(epc, ExperimentalParCond_DataFile):
                            epc.delete()
                        elif isinstance(epc, ):
                            for ep in epc:
                                ep.delete()
                        else:
                            pass
     
                elif  isinstance(self.dataFile, DataFileTemp):
                    params[ 'datafiletemp_id'] = self.dataFile
                    epc = self.existObjectInDB(ExperimentalParCondTemp_DataFileTemp(), params)
                    if isinstance(epc, ExperimentalParCondTemp_DataFileTemp):
                        epc.delete()
                    elif isinstance(epc, QuerySet):
                        for ep in epc:
                            ep.delete()
                    else:
                            pass
                    
                
            if  self.dataFile:   
                self.dataFile.delete()
            
            if  self.dataFileProperty:  
                self.dataFileProperty.delete()
            
            if self.article:
                if isinstance(self.article, QuerySet):
                    pass
                else:
                    self.article.delete()
            
            
            self.dataFile = None
            self.dataFileProperty= None
            self.article = None
            
            return False
        
        
    def UploadFile(self):  
        datacode =''
        newdatacode = ''
        if isinstance(self.dataFile, DataFile):
            ciffilein = os.path.join(str(self.cifs_dir_valids ), self.fileuser.filename)
            ciffileout = os.path.join(str(self.cifs_dir), self.dataFile.filename )
            datacode = ("data_"+ self.fileuser.filename.replace('.mpod', ' ')).strip().strip("'").strip()
            newdatacode =   "data_" + str(self.data_code['code'] )
 
        elif isinstance(self.dataFile, DataFileTemp):
            if not self.cifs_dir_custom:
                ciffilein = os.path.join(str(self.cifs_dir_valids),self.dataFile.filename)
                if os.path.exists(ciffilein):
                    ciffileout = os.path.join(str(self.cifs_dir),  self.filename  )
                    datacode = ("data_"+ self.dataFile.filename.replace('.mpod', ' ')).strip().strip("'").strip()
                    newdatacode =   "data_" + str(self.data_code['code'] )
                else:
                    ciffilein = os.path.join(str(self.cifs_dir),  self.filename  ) 
                    if os.path.exists(ciffilein):
                        ciffileout = os.path.join(str(self.cifs_dir_valids),self.dataFile.filename) 
                        datacode = ("data_"+ self.filename.replace('.mpod', ' ')).strip().strip("'").strip()
                        newdatacode =   ("data_" + self.dataFile.filename.replace('.mpod', ' ')).strip().strip("'").strip()
 
            else:
                ciffilein = os.path.join(str(self.cifs_dir_custom), self.filename   )
                ciffileout = os.path.join(str(self.cifs_dir_valids),  self.dataFile.filename  ) 
                datacode = ("data_"+ self.filename.replace('.mpod', ' ')).strip().strip("'").strip()
                newdatacode =   ("data_" + self.dataFile.filename.replace('.mpod', ' ')).strip().strip("'").strip()
                
 
    
        res = None
        sz=0
        datanested = ''
        try:
            with open(ciffilein) as infile, open(ciffileout, 'w') as outfile:
                for line in infile:
                    ln = line.rstrip('\n')
                    print ln
                    if ln.startswith("data_"):
                         
                        matches = difflib.SequenceMatcher(None, datacode, ln).get_matching_blocks()
                        for match in matches:
                            if sz == 0:
                                sz = match.size
                                
                            if match.a != match.b:
                                datanested = ln[sz:match.b]
    
                        line = newdatacode + datanested + '\n'
                        print line
                        outfile.write(line)
                    else:                                        
                        outfile.write(line)
         
            return True
                    
        except  IOError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            self.error = err
            
            return False
        
 
 
            
 