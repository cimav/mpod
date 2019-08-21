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
from data.models import *
from parse_files_2 import *
from django.core.exceptions import ObjectDoesNotExist
from data.Utils import *



class Extractor (object):
    def __init__(self,cifs_dir,core_dic_filepath,mpod_dic_filepath,cifs_dir_output,filelist):
        self.cifs_dir=cifs_dir
        self.core_dic_filepath=core_dic_filepath
        self.mpod_dic_filepath=mpod_dic_filepath
        self.experimentalParCondList=[]
        self.experimentalCond={}
        self.data_code={}
        self.code = 0
        self.dataFile= None
        
        
        if len(filelist) > 0:
            self.fds= filelist
        else:
            self.fds=os.listdir(self.cifs_dir)
            
        self.fds2=filter(lambda x: x[-5:]==".mpod",  self.fds)
        self.filets=sorted(filter(lambda x: os.path.isfile(os.path.join(cifs_dir,  x)), self.fds2))
      

    
    def read_file_1(self, mpod_filepath):
        in_file = open(mpod_filepath, 'r')
        texto = in_file.read()
        in_file.close()
        return texto
    
    
    def get_data_code(self, texto):
        lins = map(lambda x: x.strip(), texto.strip().split("\n"))
        #self.code=0
        for li in lins:
             
            code = self.get_data_code_lin(li)
            #return self.get_data_code_lin(li)
            if code>0:
                return code
                
        if self.code==0:
            raise Exception('Cid data_ code', 'missing')
        """else:
            return self.code"""

    @classmethod
    def get_data_code_lin(self, lin):
        l=lin.strip()
        if l[0:5]=='data_':
            try:
                return int(l[5:])
            except ValueError:
                print("get last code from database")
                "Get last value of Code from database, and increment"
                top = DataFile.objects.order_by('-code')[0]
                #self.code = int(top.code) + 1
                return  int(top.code) + 1
        else:
            return  int(0)

    def get_info_1(self, texto,  tags):
        vals=[]
        for tag in tags:
            val=""
            rf = texto.find(tag)
            if rf>-1:
                tl=len(tag)
                st=rf+tl
                rf2 = texto[st:].find('\n')
                val=texto[st:st+rf2].strip().strip("'")
            else:
                val = ""
            vals.append(val)
        return vals
    
    def get_info_2(self, texto,  tags):
        found = ''
        vals=[]
        line=[]
        for tag in tags:
            end=tag + ' .*\n'
            try:
                found = re.search(r'\b' + end + r'\b', texto).group(0)
                tagfound = found[:len(tag)]
                
                if tag == tagfound:
                    foundval = found[len(tag) + 1:]
                    foundval = foundval.rstrip("\r\n").strip().strip("'").strip()
                    vals.append( foundval)  
  
            except AttributeError:
                if tag == '_chemical_formula':
                    try:
                        tag = '_chemical_formula_sum'
                        end=tag + ' .*\n'
                        found = re.search(r'\b' + end + r'\b', texto).group(0)
                        tagfound = found[:len(tag)]
                    
                        if tag == tagfound:
                            foundval = found[len(tag) + 1:]
                            foundval = foundval.rstrip("\r\n").strip().strip("'").strip()
                            vals.append( foundval)  
                    except AttributeError:
                        found = ''
                        vals.append( found) 
                        
                    
                else: 
                    found = ''
                    vals.append( found)  
                
                
        return vals
            
 
                
                    
               
       
    

    def get_info_title(self, texto):
        title_lins=[]
        lins = map(lambda x: x.strip(), texto.strip().split("\n"))
        ind=0
        for i, lin in enumerate(lins):
            if lin.find("_publ_section_title")>-1:
                ind = i
                break
        flag = False
        if ind > 0:
           flag = True
           
        j=2
        while flag:
            stripped = lins[ind+j].strip().strip("'").strip()
             
            if  len(stripped) > 0:            
                if stripped[0]==";":
                    break
                else:
                    title_lins.append(stripped)
                    j=j+1
            else:
                break
        return " ".join(title_lins)

    def get_info_authors(self, texto):
        authors=[]
        lins = map(lambda x: x.strip(), texto.strip().split("\n"))
        ind=0
        for i, lin in enumerate(lins):
            if lin.find("_publ_author_name")>-1:
                ind = i
                break
        if lins[ind-1]=="loop_":
            flag = True
            j=1
            while flag:
                stripped = lins[ind+j].strip().strip("'").strip()
                if stripped[0]=="_":
                    break
                else:
                    authors.append(stripped)
                    j=j+1
        else:
            authors_stri = lins[ind][len('_publ_author_name'):].strip().strip("'").strip()
            if authors_stri.find(',')>-1:
                authors = authors + authors_stri.split(',')
            else:
                authors.append(authors_stri)
        return authors

    def format_vals(self,vals, formats):
        func=None
        tvs = []
        fs =[]
        for i,v in enumerate(vals):
            if not v=="None":
                f=formats[i]
                if f=='%d':
                    func=int
                if f=='%s':
                    func=lambda x: "'"+str(x)+"'"
                if f=='%f':
                    func=float
                try:
                    vv=func(v)
                    tvs.append(vv)
                    fs.append(f)
                except:
                    pass
        frms_st = ", ".join(fs)
        vals_tup = tuple(tvs)
        return tvs
    
    

            
            
    def get_props(self,texto,tags,loopedtgs,approved):
        tg="_prop"
        ntgs=tags
        props=[]
        propsList=[]
        propstag=[]
        propsval=[]
        prop_data_tags_looped=loopedtgs
        props_tags=[]
        lins = map(lambda x: x.strip(), texto.strip().split("\n"))
        texto_loops = None
        ind=0
        filePropertyData = FilePropertyData() 
        
        for i, lin in enumerate(lins):
            if lin.find(tg)>-1:
                lcs=lin.split()
                prstr=lcs[0].strip()[5:]
                objProperty = None
                tag=lcs[0]
                try:
                    if approved:
                        objProperty=Property.objects.get(tag=tag, active=True)
                    else:
                        objProperty=PropertyTemp.objects.get(tag=tag, active=True)
                    
                except ObjectDoesNotExist as error:      
                    print "message in the function get_props for debug purposes. Message({0}): {1}".format(99, error.message)   
                    print "Property not exist"
                    
                
                parts=prstr.split('_')
                if parts[1] in ntgs: #[u'conditions', u'measurement', u'frame', u'symmetry', u'data', u'thermal']
                    if prstr not in filePropertyData._other_looped and tag not in prop_data_tags_looped :
                        if len(lcs) > 1:
                            if len(lcs) > 2:
                                val = ''
                                for i, v in enumerate(lcs):
                                    if i > 0:
                                        lcs[i] = ''
                                        val = val + " "+ v
                                lcs[1] = val.strip().strip("'").strip()
                            else:
                                lcs[1] = lcs[1].strip().strip("'").strip()
                            
                            filePropertyData._no_looped.append(lcs)
                        else:                        
                            filePropertyData._other_looped.append(tag)
                        

     
                else:
                    if prstr not in props:
                        structureProperty = FileProperty()
                        structureProperty._name["prop_name"] = prstr
                        prtagstr=lcs[1].strip()
                        #propstag.append( prtagstr)
                        structureProperty._propstag["propstag"] = prtagstr
                        coeffcounter = 0
                        cfound = False
                        for x, lin in enumerate(lins):
                            t=prtagstr.strip().strip("'").strip()
                            f =  lin.find(t)
                            if lin.find(t)>-1:
                                coeffficientsandvalues=lin.split() 
                                if not coeffficientsandvalues[0].startswith("_prop"):
                                    if t == coeffficientsandvalues[0].strip().strip("'").strip():
                                        coeff = {}
                                        if not structureProperty._coefflen:
                                            structureProperty._coefflen =  len(coeffficientsandvalues[:3])
                                            structureProperty._looped_val[0] = coeffficientsandvalues[3:]
           
                                        structureProperty._coeffi[coeffcounter] = coeffficientsandvalues[:3]
                                        coeffcounter = coeffcounter + 1
  
                        propsList.append(structureProperty)

        if filePropertyData._other_looped:
            for i, tag in enumerate(filePropertyData._other_looped):
                for x,p in enumerate(propsList):
                    p._looped_tag_val[tag] = p._looped_val[0][i].strip().strip("'").strip()
                    

        

        
        for x,p in enumerate(propsList):
            #p._loped =  []
            #print p._name['prop_name']
            for key,value in p._coeffi.items():
                for i,tag in enumerate(prop_data_tags_looped):
                    looped = {}
                    looped[tag,i] = value[i]
                    p._looped.append(looped)
                    #print p._looped[i]
            #print  p._looped
                 
        
        filePropertyData.fileproperty = propsList
        
 
        
        #return props,props_agg,propsStructure
        return filePropertyData
    
    
    

    
    
    def get_conds(self,texto,tags,approved):
        tg="_prop"
        #ntgs= ['conditions','measurement','frame','symmetry']
        
        ntgs = tags
        props_agg=[]
        experimentalParCondList =[]
        
        lins = map(lambda x: x.strip(), texto.strip().split("\n"))
        ind=0
        for i, lin in enumerate(lins):
            if lin.find(tg)>-1:
                lcs=lin.split()
                prstr=lcs[0].strip()[5:]
                parts=prstr.split('_')
                if parts[1] in ntgs:
                    if prstr not in props_agg:
                        try:
                            tag = lcs[0]
                            if approved:
                                objExperimentalParCond=ExperimentalParCond.objects.get(tag=tag, active=True)
                            else:
                                objExperimentalParCond=ExperimentalParCondTemp.objects.get(tag=tag, active=True)

                            experimentalParCondList.append(objExperimentalParCond)
                            
                        except ObjectDoesNotExist as error:
                            print "message in the function get_conds for debug purposes.  Message({0}): {1}".format(99, error.message)   
                            print tag + "Does Not Exist: Add to list for load to DB "
                            props_agg.append(prstr)

                    
                        

        return props_agg, experimentalParCondList
    
    #search in dictionary
    def props_info_in_dic(self,props):
        props_info = {}
        tgs = ['_name','_category','_type','_units', '_units_detail']
        texto = self.read_file_1(self.mpod_dic_filepath)
        lins = map(lambda x: x.strip(), texto.strip().split("\n"))
        for prop in props:
            pro_str = "data_prop"+prop
            #print pro_str
            for ii, lin in enumerate(lins):
                ind = None
                if lin.startswith(pro_str):
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
    
    def checkExperimentalParCond(self,tag):
        experimentalParCond=ExperimentalParCond.objects.filter(tag__exact=tag, active=True)
        if not experimentalParCond:
            return False
        else:
            return True
        
        
    
    def extractConditions(self,approved, *args):
        if args:
            properties_ids= argsListToIntList(args,'experimentalcon')  
         
        tg = '_prop'   
        conds = []
        inds=[]
        ntgs=[]

        proptagList=Tags.objects.filter(categorytag=CategoryTag.objects.get(id=1), active=True)
        for i, pt in enumerate(proptagList):
            ntgs.append( proptagList[i].tag )
            
         
        for i, fil in enumerate(self.filets):
            experimentalCondOutDB  = None     
            experimentalCondInDB = None    
            filepath=os.path.join(self.cifs_dir, fil)
            texto = self.read_file_1(filepath)
            experimentalCondOutDB,experimentalCondInDB = self.get_conds(texto,ntgs,approved)
 
            
            self.experimentalCond[fil] = []
            if experimentalCondInDB:
                self.experimentalCond[fil] = experimentalCondInDB
             
            if experimentalCondOutDB:
                experimentalCondOutDB = sorted(experimentalCondOutDB)
                aa = self.props_info_in_dic(experimentalCondOutDB)
                for cond in experimentalCondOutDB:
                    if approved:                
                        experimentalParCond= ExperimentalParCond()
                    else:
                        experimentalParCond=ExperimentalParCondTemp()
                        
    
                    experimentalParCond.tag=tg+cond
                    experimentalParCond.description=cond
        
                    #tp = cond
                    if bool(aa):         
                        try:       
                            na = aa[cond]['_name'][6:]
                            try:
                                un = aa[cond]['_units']
                            except:
                                un = 'n.a.'
                            try:
                                ud = aa[cond]['_units_detail']
                            except:
                                ud = 'n.a.'
                        except:
                            dictionary=Dictionary.objects.get(tag__exact=tg+cond)                 
                            na=dictionary.name  
                            un=dictionary.units  
                            ud=dictionary.units_detail 
                            
                       
                    else:

                        try:
                            dictionary=Dictionary.objects.get(tag__exact=tg+cond)                 
                            na=dictionary.name  
                            un=dictionary.units  
                            ud=dictionary.units_detail 

                            
                        except ObjectDoesNotExist as error:
                            #print "message in the function get_conds for debug purposes.  Message({0}): {1}".format(99, error.message)   
                            print tg+cond + " it does not exist in the DB or in the dictionary"
                            na= (tg+cond)[6:]
                            un='?'
                            ud='?'
                            
                            
                    
                     
                    try:                            
                        experimentalParCond.name=' '.join(na.split('_')) 
                        experimentalParCond.units=un
                        experimentalParCond.units_detail=ud
                        experimentalParCond.save()    
                        #self.experimentalParCondList.append(experimentalParCond)
                        list = self.experimentalCond[fil]
                        list.append(experimentalParCond)
                        self.experimentalCond[fil] = list

        
                    except Exception  as error:
                        print "message in the function get_conds for debug purposes.  Message({0}): {1}".format(99, error)    
                        print "I had an error when inserting record"
                        return False
                    
         
            else:
                print  "This file does not contain new experimental conditions"
                
        return True
    
        
            
    def saveDataFileProperty(self,approved,dataFileProperty,objProperty,dataFile,pr):
        sucess = False
        if approved:
            if  dataFileProperty:
                PropertyValues.objects.filter(datafileproperty=dataFileProperty).delete()
                
            try:
                if not dataFileProperty:
                    dataFileProperty=DataFileProperty()
                    dataFileProperty.property=objProperty
                    dataFileProperty.datafile=dataFile
                    dataFileProperty.save()
                
                    
            except Exception  as error:
                print "message in the function get_conds for debug purposes.  Message({0}): {1}".format(99, error)  
                print "An error occurred when inserting the DB the new dataFileProperty"
                return False

            propertyValues= PropertyValues()
            for n, it in enumerate(pr._looped):
                
                propertyValues.datafileproperty = dataFileProperty
                for key,value in it.items():
                    if key[0] == '_prop_data_label':
                        propertyValues.label = value
                        
                    if key[0] == '_prop_data_tensorial_index':
                        propertyValues.tensorial_index = value
                        
                    if key[0] == '_prop_data_value':
                        propertyValues.value = value

                if  key[1] < (pr._coefflen - 1):
                    pass
                else:
                    #counter = counter + 1
                    try:
                        propertyValues.save();  
                        propertyValues= PropertyValues()
                    except Exception  as error:
                        print "message in the function get_conds for debug purposes.  Message({0}): {1}".format(99, error)  
                        print "An error occurred when inserting the DB the new propertyValues"
                        return sucess
            
                          
                  
                  
        else:
            if  dataFileProperty:
                PropertyValuesTemp.objects.filter(datafilepropertytemp=dataFileProperty).delete()
                
            try:
                if not dataFileProperty:
                    dataFileProperty=DataFilePropertyTemp()
                    dataFileProperty.propertytemp=objProperty
                    dataFileProperty.datafiletemp=dataFile
                    dataFileProperty.save()
                    
            except Exception  as error:
                print "message in the function get_conds for debug purposes.  Message({0}): {1}".format(99, error)  
                print "An error occurred when inserting the DB the new dataFileProperty"
                return False

       
            propertyValuesTemp= PropertyValuesTemp()
            for n, it in enumerate(pr._looped):
                
                propertyValuesTemp.datafilepropertytemp = dataFileProperty
                for key,value in it.items():
                    if key[0] == '_prop_data_label':
                        propertyValuesTemp.label = value
                        
                    if key[0] == '_prop_data_tensorial_index':
                        propertyValuesTemp.tensorial_index = value
                        
                    if key[0] == '_prop_data_value':
                        propertyValuesTemp.value = value

                if  key[1] < (pr._coefflen - 1):
                    pass
                else:
                    try:
                        
                        propertyValuesTemp.save();  
                        propertyValuesTemp= PropertyValuesTemp()
                    except Exception  as error:
                        print "message in the function get_conds for debug purposes.  Message({0}): {1}".format(99, error)  
                        print "An error occurred when inserting the DB the new propertyValuesTemp"
                        return False
         
                  
        return True
    
     
    def  extractCondictionsValues(self,approved,dataFileProperty,objProperty,datafile,key,val):
        experimentalCondition = None
         
         
        if not dataFileProperty:
            try:
                if approved:
                    dataFileProperty=DataFileProperty.objects.get(property=objProperty, datafile=datafile)
                else:
                    dataFileProperty=DataFilePropertyTemp.objects.get(propertytemp=objProperty, datafiletemp=datafile)
            except ObjectDoesNotExist as error:
                print "message in the function get_conds for debug purposes.  Message({0}): {1}".format(99, error.message)  
                print "The dataFileProperty does not exist a new record will be created in the DB"
                return False
            
        try:
                if approved:
                    if not dataFileProperty:
                        dataFileProperty=DataFileProperty()
                        dataFileProperty.property=objProperty
                        dataFileProperty.datafile=datafile
                        dataFileProperty.save()
                else:
                    if not dataFileProperty:
                        dataFileProperty=DataFilePropertyTemp()
                        dataFileProperty.property=objProperty
                        dataFileProperty.datafile=datafile
                        dataFileProperty.save()
                
        except Exception  as error:
            print "message in the function get_conds for debug purposes.  Message({0}): {1}".format(99, error)  
            print "An error occurred when inserting the DB the new dataFileProperty"
            return False
        

        
        try:
            if approved:
                experimentalCondition = ExperimentalParCond.objects.get(tag__exact=key, active=True)
            else:
                experimentalCondition = ExperimentalParCondTemp.objects.get(tag__exact=key, active=True)
        
        except ObjectDoesNotExist as error:
            print "message in the function extractProperties  for debug purposes Message({0}): {1}".format(99, error.message)  
            print "The experimentalCondition does not exist"
            return False
                
                
                
        propertyConditionDetail = None   
        try:
                if approved:
                    propertyConditionDetail = PropertyConditionDetail.objects.get(datafileproperty=dataFileProperty, condition=experimentalCondition)
                else:
                    propertyConditionDetail=  PropertyConditionDetailTemp.objects.get(datafileproperty=dataFileProperty,condition=experimentalCondition)
        except ObjectDoesNotExist as error:
            print "message in the function extractProperties  for debug purposes Message({0}): {1}".format(99, error.message)  
            print "The propertyConditionDetail does not exist a new record will be created in the DB"
            
    
        try:
            if not propertyConditionDetail:
                if approved:
                    propertyConditionDetail = PropertyConditionDetail()
                    propertyConditionDetail.condition = experimentalCondition
                    propertyConditionDetail.datafileproperty = dataFileProperty
                    propertyConditionDetail.value = val
                    propertyConditionDetail.save()
    
                else:
                    propertyConditionDetail = PropertyConditionDetailTemp()                 
                    propertyConditionDetail.condition = experimentalCondition
                    propertyConditionDetail.datafileproperty = dataFileProperty
                    propertyConditionDetail.value = val
                    propertyConditionDetail.save()
                
                
            
            else:
                propertyConditionDetail.value = val
                propertyConditionDetail.save()
                
        except Exception  as error:
                        print "message in the function extractProperties  for debug purposes Message({0}): {1}".format(99, error)  
                        print "An error occurred when inserting the new  propertyConditionDetail in the DB"
                        return False
            
            
    def extractProperties(self,approved, *args):
        propertyList =[]
        dataFilePropertyList=[]
        filePropertyData = None

        
       
        try: 
            tg="_prop"
            
            data_props={}
            ntgs=[]
            loopedtgs=[]
  
            proptagList=Tags.objects.filter(categorytag=CategoryTag.objects.get(id=2),active=True)
            prop_data_tags_looped=PropLoopedTags.objects.all() 
            
            for i, pt in enumerate(proptagList):
                ntgs.append( proptagList[i].tag )
                
            for i, pt in enumerate(prop_data_tags_looped):
                loopedtgs.append( prop_data_tags_looped[i].tag)
 
            
            for i, fil in enumerate(self.filets):
                dictionary = None
                objProperty = None
                dataFileProperty = None
                dataFile = None
                filePropertyData = None
                filepath=os.path.join(self.cifs_dir, fil)
                texto = self.read_file_1(filepath)

                this_props  = []
                props_agg  = []
                propsStructure = []
                
              
                filePropertyData = self.get_props(texto,ntgs,loopedtgs,approved)
                props = []
                for pr in filePropertyData.fileproperty:
                    if not pr in props:
                        props.append(pr._name['prop_name'])



                aa = self.props_info_in_dic(props)
    
                for i_pr, pr in enumerate(filePropertyData.fileproperty):     
                    indextag = pr._propstag
                    
                    
                    if bool(aa):         
                        try:       
                            na = aa[pr._name["prop_name"]]['_name'][6:]
                            try:
                                un = aa[pr._name["prop_name"]]['_units']
                            except:
                                un = 'n.a.'
                            try:
                                ud = aa[pr._name["prop_name"]]['_units_detail']
                            except:
                                ud = 'n.a.'
                        except:
                            print tg+pr._name["prop_name"] + " it does not exist in the in the Dictionary File"
                            
                            try:
                                dictionary=Dictionary.objects.get(tag__exact=tg+pr._name["prop_name"])                 
                                na=dictionary.name  
                                un=dictionary.units  
                                ud=dictionary.units_detail 
                            except ObjectDoesNotExist as error:
                                #print "message in the function get_conds for debug purposes.  Message({0}): {1}".format(99, error.message)   
                                print tg+pr._name["prop_name"] + " it does not exist in the  Dictionary Table"
                       
                   
                    else:
                        try:
                            dictionary=Dictionary.objects.get(tag__exact=tg+pr._name["prop_name"])                 
                            na=dictionary.name  
                            un=dictionary.units  
                            ud=dictionary.units_detail 
                        except ObjectDoesNotExist as error:
                            #print "message in the function get_conds for debug purposes.  Message({0}): {1}".format(99, error.message)   
                            print tg+pr._name["prop_name"] + " it does not exist in the  Dictionary Table"
                            
                            
                            
                    
                    try:
                        if approved:
                            objProperty=Property.objects.get(tag__exact=tg+pr._name["prop_name"], active=True)
                            na=objProperty.name  
                            un=objProperty.units  
                            ud=objProperty.units_detail 
                        else:
                            objProperty=PropertyTemp.objects.get(tag__exact=tg+pr._name["prop_name"], active=True)
                            na=objProperty.name  
                            un=objProperty.units  
                            ud=objProperty.units_detail 
  
                    except ObjectDoesNotExist as error:
                        print "message in the function extractProperties for debug purposes.  Message({0}): {1}".format(99, error.message)   
                        print "the property does not exist  in the DB, a new one will be created"
                               
                    
                           

                    if objProperty == None and dictionary == None:
                        na= (tg+pr._name["prop_name"])[6:]
                        un='?'
                        ud='?'

                    if not objProperty:        
                        if approved:
                            objProperty=Property()
                        else:
                            objProperty=PropertyTemp()
                            
                            
                        
                        objProperty.tag=tg+pr._name["prop_name"]
                        objProperty.description=pr._name["prop_name"]   
                        formatedname = ' '.join(na.split('_')) 
                        print formatedname
                        objProperty.name = formatedname
                        
                        objProperty.units =un
                        objProperty.units_detail = ud
                        
                        if pr._propstag != "":
                            objProperty.short_tag =  pr._propstag["propstag"].strip().strip("'").strip()
                            
                        try:
                            objProperty.save()
                        except ObjectDoesNotExist as error:
                            print "message in the function extactProperties for debug purposes.  Message({0}): {1}".format(99, error.message)   
                            print "An error occurred when inserting the DB the new property"
                            return False
                    else:
                        pass
                    
                    
                    code = self.data_code[fil,'code']
                     
                    datafile= None
                    realfil = None 
                    try:                
                        
                            namecode = fil[:(len(fil)-5)] 
                            if str(code) == namecode:
                                if approved:   
                                    datafile=DataFile.objects.get(filename__exact=str(fil))
                                else: 
                                    datafile=DataFileTemp.objects.get(filename__exact=str(fil))  
                            else:
                                if approved: 
                                    datafile=DataFile.objects.get(filename__exact=str(code) + ".mpod")  
                                else: 
                                    datafile=DataFileTemp.objects.get(filename__exact=str(fil))  
                                
                                
                                
                    except ObjectDoesNotExist as error:
                        print "message in the function extractProperties  for debug purposes Message({0}): {1}".format(99, error.message)  
                        print "the DataFile " + fil +"The DataFile does not exist a new record will be created in the DB"
                        
                        
                    if datafile:
                        if approved:  
    
                            #self.data_code[datafile.filename,'code'] = datafile.code
                            code= datafile.code
                        else: 
                            datafile.code = code
                        
                    else:
                        if approved:   
                            datafile=DataFile()
                            datafile.code = code
                            datafile.filename = str(code) + ".mpod"
                        else:
                            datafile=DataFileTemp()
                            datafile.code = code
                            datafile.filename = fil
                            

                    dataFileProperty = None
                    try:
                            if approved:
                                dataFileProperty = DataFileProperty.objects.get(property=objProperty, datafile=datafile)
                            else:
                                dataFileProperty=  DataFilePropertyTemp.objects.get(propertytemp=objProperty,datafiletemp=datafile)
                    except ObjectDoesNotExist as error:
                        print "message in the function extractProperties  for debug purposes Message({0}): {1}".format(99, error.message)  
                        print "The dataFileProperty does not exist a new record will be created in the DB"
                         
                    

                    self.saveDataFileProperty(approved,dataFileProperty,objProperty,datafile,pr)    
      

                    for tag in filePropertyData._no_looped:
                        self.extractCondictionsValues(approved,dataFileProperty,objProperty,datafile,tag[0],tag[1])
                        
                    for key,val in pr._looped_tag_val.items():
                        self.extractCondictionsValues(approved,dataFileProperty,objProperty,datafile,key,val)
 

            return True        
                        
            
        except  Exception as e:
            print "Error in the function extractProperties for debug purposes.  Error: {1}".format( e.message, e.args) 
            return False
  
 
            

            
            
    def extractPublarticleAndDataFile_Data(self,approved, *args): 
        """gen_tags = ['_cod_database_code', '_phase_generic', '_phase_name', '_chemical_formula'] #categorytag_id=5
        publi_tags = ['_journal_name_full', '_journal_year', '_journal_volume',
                                  '_journal_issue', '_journal_page_first', '_journal_page_last',
                                  '_journal_article_reference', '_journal_pages_number' ]  #categorytag_id=3
        
        """
        gen_tags = []
        publArticle = None
        proptagList=Tags.objects.filter(categorytag=CategoryTag.objects.get(id=5),active=True)

            
        for i, pt in enumerate(proptagList):
            gen_tags.append( proptagList[i].tag )
        
        publi_tags = []
        proptagList=Tags.objects.filter(categorytag=CategoryTag.objects.get(id=3),active=True)

            
        for i, pt in enumerate(proptagList):
            publi_tags.append( proptagList[i].tag )
        

            
        
        dataFileList=[]
        
   
        gen_info_lins=[]
        publi_info_lins=[]
        titles=[]
        ii = 1
        for i, fil in enumerate(self.filets):

            if approved:   
                publicArticle=PublArticle()
            else: 
                publicArticle=PublArticleTemp()
                
            filepath=os.path.join(self.cifs_dir, fil)
            texto = self.read_file_1(filepath)
            title = self.get_info_title(texto)
            if title in titles:
                ind=1+titles.index(title)  #python indexing starts from 0 index of publis from 1
            else:
                titles.append(title)
                publi_vals=[ii]
                publi_vals = publi_vals + self.get_info_2(texto, publi_tags)
                authors = self.get_info_authors(texto)            
                
                aut=''
                for a in authors:
                    coma=''
                    if aut != '':
                        coma='; '   
                    else:
                        coma='' 
                    
                    aut=aut + coma + a
                        
                publicArticle.title=title
                publicArticle.authors=aut       

                    
                formatss = "%d, %s, %s, %s, %d, %s, %d, %d, %d, %s, %d"
                formats = map(lambda x: x.strip(), formatss.split(","))
                func=None
     
                publi_vals=[publi_vals[0]]+[title]+[authors]+publi_vals[1:]
                for i,v in enumerate(publi_vals):
                    #if not v=="None":
                    f=formats[i]
                    if f=='%d':
                        func=int
                    if f=='%s':
                        func=lambda x: ""+str(x)+""
                    if f=='%f':
                        func=float
                    try:                    
                        if i == 9:
                            if v:
                                vv=func(v)
                            else:
                                vv = '?'
                                
                            publicArticle.reference=vv
                        elif (i == 6 or i == 10):    
                            vv=0
                            if  i == 6:
                                if v:
                                    vv=func(v)
                                     
                                publicArticle.issue=vv
                            elif  i == 10:
                                if v:
                                    vv=func(v)
                                    
                                publicArticle.pages_number=vv
                                
                        else:
                            vv = None
                            if v:
                                vv=func(v)
                            else:
                                vv = v
                            
                            if i == 3:
                                publicArticle.journal=vv                             
                            elif  i == 4:
                                publicArticle.year=vv
                            elif  i == 5:
                                publicArticle.volume=vv
                            elif  i == 6:
                                publicArticle.issue=vv
                            elif  i == 7:
                                if vv:
                                    publicArticle.first_page=vv
                                else:
                                    publicArticle.first_page= 0
                            elif  i == 8:
                                if vv:
                                    publicArticle.last_page=vv
                                else:
                                    publicArticle.last_page= 0
                         
                    except  Exception as e:
                        print "Error in the function extractPublarticleAndDataFile_Data  for debug purposes.  Error: {1}".format( e.message, e.args) 
                        print "An error occurred when extracting the articles from the .mpod file"
                        return False
                        
                
                 
          
            publicArticleExist= None
            try:
                if approved: 
                
                    publicArticleExist=PublArticle.objects.get( authors__exact = publicArticle.authors,
                                                                                                 journal__exact = publicArticle.journal,
                                                                                                 year__exact = publicArticle.year)      
      

                else: 
                    publicArticleExist=PublArticleTemp.objects.get(
                                                                                         authors__exact = publicArticle.authors,
                                                                                         journal__exact = publicArticle.journal,
                                                                                         year__exact = publicArticle.year)
                    

                        
            except ObjectDoesNotExist as error:
                print "message in the function extractPublarticleAndDataFile_Data  for debug purposes Message({0}): {1}".format(99, error.message)   
                print "The article does not exist a new record will be created  in the DB"
                    
 
                
             
            if not publicArticleExist:
                try:
                    publicArticle.save()
                except Exception  as error:
                    print "message in the function extractPublarticleAndDataFile_Data  for debug purposes Message({0}): {1}".format(99, error)   
                    print "An error occurred when inert  publicArticle"
                    
            else:
                publicArticle = publicArticleExist
                    
            code = self.get_data_code(texto) 
            self.data_code[fil,'code'] = code
            datafile= None
            realfil = None 
            try:                
                
                    namecode = fil[:(len(fil)-5)] 
                    if str(code) == namecode:
                        if approved:   
                            datafile=DataFile.objects.get(filename__exact=str(fil))
                        else: 
                            datafile=DataFileTemp.objects.get(filename__exact=str(fil))  
                    else:
                        if approved: 
                            datafile=DataFile.objects.get(filename__exact=str(code) + ".mpod")  
                        else: 
                            datafile=DataFileTemp.objects.get(filename__exact=str(fil))  
                        
                        
                        
            except ObjectDoesNotExist as error:
                print "message in the function extractPublarticleAndDataFile_Data  for debug purposes Message({0}): {1}".format(99, error.message)  
                print "the DataFile: " + fil +" The DataFile does not exist a new record will be created in the DB"
                
                
            if datafile:
                if approved:  
                    self.data_code = {}
                    self.data_code[datafile.filename,'code'] = datafile.code
                    code= datafile.code
                else: 
                    datafile.code = code
                
            else:
                if approved:   
                    datafile=DataFile()
                    datafile.code = code
                    datafile.filename = str(code) + ".mpod"
                else:
                    datafile=DataFileTemp()
                    datafile.code = code
                    datafile.filename = fil
 
            
            
            ind = ii
            ii = ii+1         

            gen_vals=[code, datafile.filename]
            publi_vals=[ii]

            gen_vals = gen_vals + self.get_info_2(texto, gen_tags)
 


            #list: [1000378L, 'zaydsfjtrglkmmhup.mpod', '?', '', '', '', 1]
            formatss = "%d, %s, %d, %s, %s, %s, %d"
            formats = map(lambda x: x.strip(), formatss.split(","))
            func=None
            info_vals=gen_vals+[ind]
            for i,v in enumerate(info_vals):
                #if not v=="None":
                f=formats[i]
                if f=='%d':
                    func=int
                if f=='%s':
                    func=lambda x: ""+str(x)+""
                if f=='%f':
                    func=float

                try:
                    if ( i == 2)  and (v == '?'):   
                        if v and v != '?':
                            vv=func(v)    
                            datafile.cod_code=vv 
                        else:                             
                            pass #vv=0

                        
                        
                    else:                  
                        if v:
                            vv=func(v)   
                            if i == 1:
                                datafile.filename=vv
                            elif i == 3:
                                datafile.phase_generic=vv 
                            elif i == 4:
                                datafile.phase_name=vv 
                            elif i == 5:
                                datafile.chemical_formula=vv  
                        else:
                            pass
                            
                        
 

                except  Exception as e:
                    print "Error: {1}".format( e.message, e.args)     
                    print "There was an error while extracting data from DataFile" 
                    return False
                     
                        
            try:

                datafile.publication = publicArticle  
                datafile.save()
            except Exception  as error:
                print "message in the function extractPublarticleAndDataFile_Data  for debug purposes Message({0}): {1}".format(99, error) 
                print "There was an error inserting the DataFile object into the DB"
                return False
                
 
    
                        
            try:

                for key,list in self.experimentalCond.items():
            
                    if key == fil:
                        if approved:   
                            if list:
                                
                                for v,item in enumerate(list):
                                    experimentalParCond_DataFile = None
                                    try:
                                        experimentalParCond_DataFile = ExperimentalParCond_DataFile.objects.get(experimentalfilecon=item,datafile=datafile)
                                    except ObjectDoesNotExist as error:
                                        print "message in the function ExperimentalParCondTemp_DataFileTemp  for debug purposes Message({0}): {1}".format(99, error.message) 
                                        print "There was an error inserting the ExperimentalParCond_DataFile object into the DB"
                                        
                                        
                                    if not experimentalParCond_DataFile:
                                        try:
                                            experimentalParCond_DataFile = ExperimentalParCond_DataFile()
                                            experimentalParCond_DataFile.experimentalfilecon = item
                                            experimentalParCond_DataFile.datafile = datafile
                                            experimentalParCond_DataFile.save()
                                        except Exception  as error:
                                            print "message in the function ExperimentalParCondTemp_DataFileTemp  for debug purposes Message({0}): {1}".format(99, error) 
                                            print "There was an error inserting the ExperimentalParCondTemp_DataFileTemp object into the DB"
                                      
                                            
                        else: 
                            if list:
                                
                                for v,item in enumerate(list):
                                    experimentalParCondTemp_DataFileTemp = None
                                    try:
                                        experimentalParCondTemp_DataFileTemp = ExperimentalParCondTemp_DataFileTemp.objects.get(experimentalfilecontemp=item,datafiletemp=datafile)
                                    except ObjectDoesNotExist as error:
                                        print "message in the function ExperimentalParCondTemp_DataFileTemp  for debug purposes Message({0}): {1}".format(99, error.message) 
                                        print "There was an error inserting the ExperimentalParCondTemp_DataFileTemp object into the DB"
                                        
                                    try:
                                        if not experimentalParCondTemp_DataFileTemp:
                                            experimentalParCondTemp_DataFileTemp = ExperimentalParCondTemp_DataFileTemp()
                                            experimentalParCondTemp_DataFileTemp.experimentalfilecontemp = item
                                            experimentalParCondTemp_DataFileTemp.datafiletemp = datafile
                                            experimentalParCondTemp_DataFileTemp.save()
                                    except Exception  as error:
                                        print "message in the function ExperimentalParCondTemp_DataFileTemp  for debug purposes Message({0}): {1}".format(99, error) 
                                        print "There was an error inserting the ExperimentalParCondTemp_DataFileTemp object into the DB"
                                    
                    else:
                        pass
                                    
                                               


            except ObjectDoesNotExist as error:
                print "message in the function ExperimentalParCondTemp_DataFileTemp  for debug purposes Message({0}): {1}".format(99, error.message) 
                print "I had an error when inserting record"
                return False

        return True       
           
            
            
