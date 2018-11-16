'''
Created on Nov 25, 2014

@author: admin
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
             
            self.code = self.get_data_code_lin(li)
            if self.code>0:
                break
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
            if stripped[0]==";":
                break
            else:
                title_lins.append(stripped)
                j=j+1
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
    
    
    def get_props(self,texto,tags):
        
        
        tg="_prop"
        #ntgs= ['conditions','measurement','frame','symmetry', 'data']
        ntgs=tags
        props=[]
        propsStructure=[]
        propstag=[]
        propsval=[]
        props_agg=[]
        lins = map(lambda x: x.strip(), texto.strip().split("\n"))
        ind=0
        for i, lin in enumerate(lins):
            if lin.find(tg)>-1:
                lcs=lin.split()
                prstr=lcs[0].strip()[5:]
                objProperty = None
                try:
                    tag=lcs[0]
                    objProperty=Property.objects.get(tag=tag)
                except ObjectDoesNotExist as error:      
                    print "Message({0}): {1}".format(99, error.message)   
                    
                
                parts=prstr.split('_')
                if parts[1] in ntgs:
                    if prstr not in props_agg and objProperty == None:
                        props_agg.append(tag)
                else:
                    if prstr not in props:
                        structureProperty=FileProperty()
                        structureProperty._prop_name=prstr
                        prtagstr=lcs[1].strip()
                        propstag.append( prtagstr)
                        propsStructure.append(structureProperty)
                        props.append(prstr)
                      
                                     
        for j,tag in enumerate(propstag):
            for i, lin in enumerate(lins):
                t=tag.strip().strip("'").strip()
                if lin.find(t)>-1:
                    lcs=lin.split() 
                    if not lcs[0].startswith("_prop"):
                        if '_prop_data_label'  in props_agg:
                            propsStructure[j]._prop_data_label.append(lcs[0])
                            
                        if '_prop_data_tensorial_index' in props_agg:  
                            propsStructure[j]._prop_data_tensorial_index.append(lcs[1])
                        
                        if  '_prop_data_value' in props_agg:
                            propsStructure[j]._prop_data_value.append(lcs[2])
                        
                        if  '_prop_measurement_method' in props_agg:
                            propsStructure[j]._prop_measurement_method.append(lcs[3])
                        else:
                            propsStructure[j]._prop_measurement_method.append('')

                        if  '_prop_conditions_frequency' in props_agg:
                            propsStructure[j]._prop_conditions_frequency.append(lcs[4])
                        else:
                            propsStructure[j]._prop_conditions_frequency.append('')
          
                #for tag in propstag:
                #propsval.append(object)
                            
        
        return props,props_agg,propsStructure
    
    
    

    
    
    def get_conds(self,texto,tags):
        tg="_prop"
        #ntgs= ['conditions','measurement','frame','symmetry']
        
        ntgs = tags
        props_agg=[]
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
                            objExperimentalParCond=ExperimentalParCond.objects.get(tag=tag)
                            props_agg.append(prstr)
                        except ObjectDoesNotExist as error:
                            print "Message({0}): {1}".format(99, error.message)   

                    
                        

        return props_agg
    
    #search in dictionary
    def props_info_in_dic(self,props):
        props_info = {}
        tgs = ['_name','_category','_type','_units', '_units_detail']
        texto = self.read_file_1(self.mpod_dic_filepath)
        lins = map(lambda x: x.strip(), texto.strip().split("\n"))
        for prop in props:
            pro_str = "data_prop"+prop
            print pro_str
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
        print "hecho"
        return props_info
    
    def checkExperimentalParCond(self,tag):
        experimentalParCond=ExperimentalParCond.objects.filter(tag__exact=tag)
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
        #proptagList=PropTags.objects.filter(active=1).exclude(tag__exact= 'data')        #categorytag_id=1
        proptagList=Tags.objects.filter(categorytag=CategoryTag.objects.get(id=1))
        for i, pt in enumerate(proptagList):
            ntgs.append( proptagList[i].tag )
            
            
        for i, fil in enumerate(self.filets):
            filepath=os.path.join(self.cifs_dir, fil)
            texto = self.read_file_1(filepath)
            this_conds = self.get_conds(texto,ntgs)
            for cn in this_conds:
                if not cn in conds:
                    conds.append(cn)
                    
                cond_ind=conds.index(cn)+1
                inds.append(cond_ind)
                
            conds = sorted(conds)

        aa = self.props_info_in_dic(conds)
        for cond in conds:
            if approved == False:                
                experimentalParCond= ExperimentalParCondTemp()
            else:
                experimentalParCond=ExperimentalParCond()
                
            
            print tg+cond
            print cond
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
                dictionary=Dictionary.objects.get(tag__exact=tg+cond)                 
                #print dictionary.tag
                na=dictionary.name  
                #dictionary.description  
                un=dictionary.units  
                ud=dictionary.units_detail 
                #dictionary.active 
                #dictionary.definition 
                #dictionary.deploy 
                #dictionary.type  
                #dictionary.category
                    
            
             
            try:    
                if approved == False:      
                    try:
                        experimentalParCondExist=ExperimentalParCondTemp.objects.get(tag__exact=experimentalParCond.tag)
                    except ObjectDoesNotExist as error:
                        print "Message({0}): {1}".format(99, error.message)   
                        experimentalParCondExist = None
                        
                
                    
                    if not experimentalParCondExist:
                        print 'propiedad nueva'
                        experimentalParCond.name=' '.join(na.split('_')) 
                        experimentalParCond.units=un
                        experimentalParCond.units_detail=ud
                        experimentalParCond.save()    
                        self.experimentalParCondList.append(experimentalParCond)
                    else:
                        print 'propiedad existe' 
                        self.experimentalParCondList.append(experimentalParCondExist)
               
                    
                else:
                    try:
                        experimentalParCondExist=ExperimentalParCond.objects.get(tag__exact=experimentalParCond.tag)
                    except ObjectDoesNotExist as error:
                        print "Message({0}): {1}".format(99, error.message)   
                        experimentalParCondExist = None
                 
                    if not experimentalParCondExist:
                        experimentalParCondExistTemp=ExperimentalParCondTemp.objects.get(tag__exact=experimentalParCond.tag)
                        print 'propiedad nueva'
                        experimentalParCond.name= experimentalParCondExistTemp.name
                        experimentalParCond.units=experimentalParCondExistTemp.units
                        experimentalParCond.units_detail=experimentalParCondExistTemp.units_detail
                        experimentalParCond.save()    
                        self.experimentalParCondList.append(experimentalParCond)
                    else:
                        print 'propiedad existe' 
                        #experimentalParCondExist.update(name=' '.join(na.split('_')),units=un,units_detail=ud) 
                        self.experimentalParCondList.append(experimentalParCondExist)
                
                        
                
                        
                    

            except  Exception, e:
                print "Error({0}): {1}".format(e.errno, e.strerror)       
                
         
        
        
    def extractProperties(self,approved, *args):
        propertyList =[]
        dataFilePropertyList=[]
        
       
        try: 
            tg="_prop"
            props = []
            data_props={}
            ntgs=[]
            #proptagList=PropTags.objects.filter(active=1)        #categorytag_id=2
            proptagList=Tags.objects.filter(categorytag=CategoryTag.objects.get(id=2))
            for i, pt in enumerate(proptagList):
                ntgs.append( proptagList[i].tag )
 
            
            for i, fil in enumerate(self.filets):
                filepath=os.path.join(self.cifs_dir, fil)
                texto = self.read_file_1(filepath)
                #code = self.get_data_code(texto)          
                this_props,props_agg,propsStructure = self.get_props(texto,ntgs)
                for pr in this_props:
                    if not pr in props:
                        props.append(pr)
                #props = sorted(props)   
    
                #dataFilePropertyold=False
                aa = self.props_info_in_dic(props)
    
                for i_pr, pr in enumerate(propsStructure):     
                    
                    if bool(aa):         
                        try:       
                            na = aa[pr._prop_name]['_name'][6:]
                            try:
                                un = aa[pr._prop_name]['_units']
                            except:
                                un = 'n.a.'
                            try:
                                ud = aa[pr._prop_name]['_units_detail']
                            except:
                                ud = 'n.a.'
                        except:
                            dictionary=Dictionary.objects.get(tag__exact=tg+pr._prop_name)                 
                            na=dictionary.name  
                            un=dictionary.units  
                            ud=dictionary.units_detail 
                        
                   
                    else:
                        dictionary=Dictionary.objects.get(tag__exact=tg+pr._prop_name)                 
                        #print dictionary.tag
                        na=dictionary.name  
                        #dictionary.description  
                        un=dictionary.units  
                        ud=dictionary.units_detail 
                        #dictionary.active 
                        #dictionary.definition 
                        #dictionary.deploy 
                        #dictionary.type  
                        #dictionary.category
                        
                        
                    

                    try:
                        if approved:
                            propertyExist=Property.objects.get(tag__exact=tg+pr._prop_name)
                        else:
                            propertyExist=PropertyTemp.objects.get(tag__exact=tg+pr._prop_name)
  
                    except ObjectDoesNotExist as error:
                        print "Message({0}): {1}".format(99, error.message)   
                        propertyExist = None
    
                        
                    dataFilePropertyExist = None    
                    
                    dataFileProperty = None
                    if not propertyExist:        
                        if approved:
                            objProperty=Property()
                        else:
                            objProperty=PropertyTemp()
                        
                        objProperty.tag=tg+pr._prop_name
                        objProperty.description=pr._prop_name     
                        formatedname = ' '.join(na.split('_')) 
                        print formatedname
                        objProperty.name = formatedname
                        
                        objProperty.units =un
                        objProperty.units_detail = ud
                        if pr._prop_data_label[0] != "":
                            objProperty.short_tag =  pr._prop_data_label[0]
                            
                        objProperty.save()
                        
 
                        try:
                            if approved:
                                self.dataFile=DataFile.objects.get(filename__exact=str(self.code) + '.mpod') 
                            else:
                                self.dataFile=DataFileTemp.objects.get(filename__exact=fil) 
                                
                        except ObjectDoesNotExist as error:
                            print "Message({0}): {1}".format(99, error.message)   
                            
                            
                        if not self.dataFile:     
                            if approved: 
                                self.dataFile=DataFile()
                            else:
                                self.dataFile=DataFileTemp()    
                        else:
                            try:
                                if approved:
                                    dataFileProperty = DataFileProperty.objects.get(property=objProperty, datafile=self.dataFile)
                                else:
                                    dataFileProperty=  DataFilePropertyTemp.objects.get(propertytemp=objProperty,datafiletemp=self.dataFile)
                                
                            except ObjectDoesNotExist as error:
                                print "Message({0}): {1}".format(99, error.message)     
                                
 

                        
                        if not dataFileProperty:  
                            if approved:
                                dataFileProperty=DataFileProperty()
                                dataFileProperty.property=objProperty
                            else:
                                dataFileProperty=DataFilePropertyTemp()
                                dataFileProperty.propertytemp=objProperty
                        else:
                            if approved:
                                dataFileProperty.property=objProperty
                            else:
                                dataFileProperty.propertytemp=objProperty

                    else:     
                        try:
                            if approved:
                                self.dataFile=DataFile.objects.get(filename__exact=str(self.code) + '.mpod') 
                            else:
                                self.dataFile=DataFileTemp.objects.get(filename__exact=fil) 
                                
                        except ObjectDoesNotExist as error:
                            print "Message({0}): {1}".format(99, error.message)  
                            
                            
                        if not self.dataFile:     
                            if approved: 
                                self.dataFile=DataFile()
                                dataFileTemp  =DataFileTemp.objects.get(filename__exact=fil) 
                                self.dataFile.code =  dataFileTemp.code
                                self.dataFile.filename =  str(self.code) + '.mpod'
                                self.dataFile.cod_code =  dataFileTemp.cod_code 
                                self.dataFile.phase_generic =  dataFileTemp.phase_generic 
                                self.dataFile.phase_name =  dataFileTemp.phase_name
                                self.dataFile.chemical_formula =  dataFileTemp.chemical_formula

                            else:
                                pass
                            
                        else:
                            try:
                                if approved:
                                    dataFileProperty = DataFileProperty.objects.get(property=propertyExist, datafile=self.dataFile)
                                else:
                                    dataFileProperty=  DataFilePropertyTemp.objects.get(propertytemp=propertyExist,datafiletemp=self.dataFile)
                                
                            except ObjectDoesNotExist as error:
                                print "Message({0}): {1}".format(99, error.message)     
                            
                            
                        if not dataFileProperty:  
                            if approved:
                                dataFileProperty=DataFileProperty()
                                dataFileProperty.property=propertyExist
                                dataFileProperty.datafile=self.dataFile
                                dataFileProperty.save()
                                for i, label in enumerate(pr._prop_data_label):
                                    propertyValues= PropertyValues()
                                    propertyValues.datafileproperty = dataFileProperty
                                    propertyValues.prop_data_label  = pr._prop_data_label[i]
                                    propertyValues.prop_data_tensorial_index = pr._prop_data_tensorial_index[i]
                                    propertyValues.prop_data_value =  pr._prop_data_value[i]
                                    propertyValues.prop_measurement_method =   pr._prop_measurement_method[i]
                                    propertyValues. prop_conditions_frequency = pr._prop_conditions_frequency[i]
                                    propertyValues.save();
                                #PropertyValues
                                
                            else:
                                dataFileProperty=DataFilePropertyTemp()
                                dataFileProperty.propertytemp=propertyExist
                                dataFileProperty.datafiletemp=self.dataFile
                                dataFileProperty.save()
                                for i, label in enumerate(pr._prop_data_label):
                                    propertyValuesTemp= PropertyValuesTemp()
                                    propertyValuesTemp.datafilepropertytemp = dataFileProperty
                                    propertyValuesTemp.prop_data_label  = pr._prop_data_label[i]
                                    propertyValuesTemp.prop_data_tensorial_index = pr._prop_data_tensorial_index[i]
                                    propertyValuesTemp.prop_data_value =  pr._prop_data_value[i]
                                    propertyValuesTemp.prop_measurement_method =   pr._prop_measurement_method[i]
                                    propertyValuesTemp. prop_conditions_frequency = pr._prop_conditions_frequency[i]
                                    propertyValuesTemp.save();
                        else:
                            pass
                            
                        
                        """if approved:
                            fileUser=FileUser.objects.get(filename__exact=fil)
                            fileUser.datafile=self.dataFile
                            fileUser.save()"""

                    
            
        except  Exception as e:
            print "Error: {1}".format( e.message, e.args) 
  
 
            

            
            
    def extractPublarticleAndDataFile_Data(self,approved, *args): 
        """gen_tags = ['_cod_database_code', '_phase_generic', '_phase_name', '_chemical_formula'] #categorytag_id=5
        publi_tags = ['_journal_name_full', '_journal_year', '_journal_volume',
                                  '_journal_issue', '_journal_page_first', '_journal_page_last',
                                  '_journal_article_reference', '_journal_pages_number' ]  #categorytag_id=3
        
        """
        gen_tags = []
        proptagList=Tags.objects.filter(categorytag=CategoryTag.objects.get(id=5))

            
        for i, pt in enumerate(proptagList):
            gen_tags.append( proptagList[i].tag )
        
        publi_tags = []
        proptagList=Tags.objects.filter(categorytag=CategoryTag.objects.get(id=3))

            
        for i, pt in enumerate(proptagList):
            publi_tags.append( proptagList[i].tag )
        
        if approved == False:   
            publicArticle=PublArticleTemp()
        else: 
            publicArticle=PublArticle()
            
        
        dataFileList=[]
        
   
        gen_info_lins=[]
        publi_info_lins=[]
        titles=[]
        ii = 1
        for i, fil in enumerate(self.filets):
            print fil
            filepath=os.path.join(self.cifs_dir, fil)
            texto = self.read_file_1(filepath)
            title = self.get_info_title(texto)
            if title in titles:
                ind=1+titles.index(title)  #python indexing starts from 0 index of publis from 1
            else:
                titles.append(title)
                publi_vals=[ii]
                publi_vals = publi_vals + self.get_info_1(texto, publi_tags)
                authors = self.get_info_authors(texto)            
                
                aut=''
                for a in authors:
                    coma=''
                    if aut != '':
                        coma=', '   
                    else:
                        coma=' ' 
                    
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
                            vv = '?'
                            if  i == 9:
                                publicArticle.reference=vv
                        elif (i == 6 or i == 10):    
                            vv=0
                            if  i == 6:
                                publicArticle.issue=vv
                            elif  i == 10:
                                publicArticle.pages_number=vv
                                
                        else:
                            vv=func(v)
                            if i == 3:
                                publicArticle.journal=vv                             
                            elif  i == 4:
                                publicArticle.year=vv
                            elif  i == 5:
                                publicArticle.volume=vv
                            elif  i == 6:
                                publicArticle.issue=vv
                            elif  i == 7:
                                publicArticle.first_page=vv
                            elif  i == 8:
                                publicArticle.last_page=vv
                            
                            

                         
                    except  Exception as e:
                        print "Error: {1}".format( e.message, e.args) 
                        
                
                publArticle = None 
                

                try:
                        if approved == False:   
                            publArticle=PublArticleTemp.objects.get(  title = publicArticle.title,
                                                                                                                     authors = publicArticle.authors,
                                                                                                                     journal = publicArticle.journal,
                                                                                                                     year = publicArticle.year,
                                                                                                                     volume = publicArticle.volume,
                                                                                                                     issue = publicArticle.issue,
                                                                                                                     first_page = publicArticle.first_page,
                                                                                                                     last_page = publicArticle.last_page,
                                                                                                                     reference = publicArticle.reference,
                                                                                                                     pages_number = publicArticle.pages_number)
                            

                        else: 
                            publArticle=PublArticle.objects.get(  title = publicArticle.title,
                                                                                         authors = publicArticle.authors,
                                                                                         journal = publicArticle.journal,
                                                                                         year = publicArticle.year,
                                                                                         volume = publicArticle.volume,
                                                                                         issue = publicArticle.issue,
                                                                                         first_page = publicArticle.first_page,
                                                                                         last_page = publicArticle.last_page,
                                                                                         reference = publicArticle.reference,
                                                                                         pages_number = publicArticle.pages_number)        
                            
                except ObjectDoesNotExist as error:
                    print "Message({0}): {1}".format(99, error.message)   
                    
 
                
             
                if not publArticle:
                    publicArticle.save()
                else:
                    pass
                    """publArticleExist.title = publicArticle.title
                    publArticleExist.authors = publicArticle.authors
                    publArticleExist.journal = publicArticle.journal
                    publArticleExist.year = publicArticle.year
                    publArticleExist.volume = publicArticle.volume
                    publArticleExist.issue = publicArticle.issue
                    publArticleExist.first_page = publicArticle.first_page
                    publArticleExist.last_page = publicArticle.last_page
                    publArticleExist.reference = publicArticle.reference
                    publArticleExist.pages_number = publicArticle.pages_number                    
                    publArticleExist.save()
                    """
                    
                self.get_data_code(texto) 
                datafileExist = None
                realfil = None 
                datafile = None
                try:
                        
                        if approved == False:   
                            datafile=DataFileTemp.objects.get(filename__exact=str(fil))
                            self.code = datafile.code
                        else: 
                            datafileTemp=DataFileTemp.objects.get(filename__exact=str(fil))
                            self.code = datafileTemp.code
                            fil=str(self.code) + ".mpod"
                            datafile=DataFile.objects.get(filename__exact=fil)          
                            
                except ObjectDoesNotExist as error:
                    print "Message({0}): {1}".format(99, error.message)   

                        
   
               
                ind = ii
                ii = ii+1         
                
                 
                    
                
              
                gen_vals=[self.code, fil]
                publi_vals=[ii]

                gen_vals = gen_vals + self.get_info_1(texto, gen_tags)
                
                if not datafile:
                    if approved == False:
                        datafile=DataFileTemp()
                    else: 
                        datafile=DataFile()
                else:
                    pass
                        
 
                    
                datafile.code=self.code 
  
    
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
                            vv=0
                            if i == 2:
                                datafile.cod_code=vv 
                        else:                  
                            vv=func(v)    
                            if i == 1:
                                datafile.filename=vv
                            elif i == 3:
                                datafile.phase_generic=vv 
                            elif i == 4:
                                datafile.phase_name=vv 
                            elif i == 5:
                                datafile.chemical_formula=vv 
                            """elif i == 6:                                                                  
                                datafile.publication= publicArticle"""

                    except  Exception as e:
                        print "Error: {1}".format( e.message, e.args)       
                        
                try:
                    if not publArticle:
                        datafile.publication = publicArticle     
                    else:    
                        datafile.publication = publArticle
                        
                    datafile.save()
                        
                    """if not datafile: 
                        if not publArticle:
                            datafile.publication = publicArticle     
                        else:    
                            datafile.publication = publArticle 

                        datafile.save()

                    else:
                        if not publArticle:
                            datafile.publication = publicArticle     
                        else:    
                            datafile.publication = publArticle
                        datafile.save()
                    """
                        
                        
 
                                  
                    #filename= datafile.filename
        
                            
            
                    for i,obj in enumerate(self.experimentalParCondList):
                        #print type(obj) # <class 'project.app.models.Car'>
                        #print str(isinstance(obj, ExperimentalParCondTemp))

                        if approved == False:
                            dataFileTemp=DataFileTemp.objects.get(filename__exact=datafile.filename)
                            #por si en un futuro se registran nuevas ExperimentalCon para este archivo
                            experimentalfilecontempDatafiletempQuerySet = ExperimentalfilecontempDatafiletemp.objects.filter(experimentalfilecontemp=obj,datafiletemp=dataFileTemp)
                            if experimentalfilecontempDatafiletempQuerySet:
                                pass
                            else:            
                                experimentalfilecontempDatafiletemp = ExperimentalfilecontempDatafiletemp()
                                experimentalfilecontempDatafiletemp.experimentalfilecontemp = obj
                                experimentalfilecontempDatafiletemp.datafiletemp = dataFileTemp
                                experimentalfilecontempDatafiletemp.save()
    
                        else: 
                            pass                           
                            """experimentalParCond = ExperimentalParCond()
                            for efct in experimentalfilecontempDatafiletempQuerySet:
                                try:
                                    experimentalParCond = ExperimentalParCond.objects.get(tag__exact=efct.experimentalfilecontemp.tag)
                                    #experimentalParCond= None
                                except ObjectDoesNotExist as error:
                                    print "Error({0}): {1}".format(99, error.message) 
                                     
                                    experimentalParCond.tag = efct.experimentalfilecontemp.tag
                                    experimentalParCond.name =  efct.experimentalfilecontemp.name
                                    experimentalParCond.description =  efct.experimentalfilecontemp.description
                                    experimentalParCond.units =  efct.experimentalfilecontemp.units
                                    experimentalParCond.units_detail =  efct.experimentalfilecontemp.units_detail
                                    experimentalParCond.save()
                            """

                except  Exception as e:
                        print "Error: {1}".format( e.message, e.args)       

                
           
            
            
