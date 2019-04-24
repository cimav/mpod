'''
Created on Aug 10, 2017

@author: Jorge Alberto Torres Acosta
'''

from data.models import *

from django.db import models
from django.db.models import Q
from django.db.models import Count
import datetime,time
import calendar

from CifMpodValidator import *
from data.ExtractorDataFromCIF import *
from shutil import  *
from mhlib import isnumeric
import codecs


class MPODUtil():
    '''
    classdocs
    '''
    
    
    def __init__(self):
        '''
        Constructor
        '''
        self.__propertylist=None
        self.__propertyMaster = None
        self.fid = None 
        # protected variable
        self.__line =  ''
        self.__mpod_str = ''
        self.__symmetry_point_group_name = False
        self.__prop_elastic_compliance = False
        self.__prop_elastic_stiffness = False
        self.__prop_piezoelectric= False
        self.__magnetoelectricity_n = False
        self.__magnetoelectricity_y = False
        self.__loop_tag = False
        self.__loop_article_info = False
        self.__section_title = False
        self.__symmetry_point_group_name= False
        self.__condition = False
        self.__sij = ''
        self.__cij = ''
        self.__dij = ''
        self.__kij = ''
        self.__yij = ''
        self.__loopBlock = []
        self.message = None
         
        
        self.__cif_dir=''
        self.cifs_dir_valids=''
        self.cifs_dir_invalids=''
        self.__core_dic_filepath=''
        self.__mpod_dic_filepath=''
        self.__cifs_dir_output=''
        self.cif_created=''
        self.valid = False
        self.reportValidation=''
        
        self.maskmatrix6x6 =   [[1, 1, 1, 1, 1, 1],
                                                    [0, 1, 1, 1, 1, 1],
                                                    [0, 0, 1, 1, 1, 1],
                                                    [0, 0, 0, 1, 1, 1],
                                                    [0, 0, 0, 0, 1, 1],
                                                    [0, 0, 0, 0, 0, 1]]
        
        self.maskmatrix3x3 =   [[1, 1, 1],
                                                    [0, 1, 1],
                                                    [0, 0, 1]]
        
        
        self.maxmatrixnonceros = None
 


    
    
    
 
    def getTag(self,tag):    
        parts=tag.split('_')[-1]
        return parts
        
 
        
    def mpodwrite(self,filename,propertyMaster):
        self.__propertyMaster= propertyMaster
        #self.__propertylist = data.propertyList
        
        
        mpoffile=MpodFile.objects.all()
        mpf = MpodFile()
        mpf = mpoffile[0]
        
        pathslist=Path.objects.all()      
        pathexist = 0
    
        for cifdir in pathslist:
            path=Path() 
            path = cifdir
            if os.path.isdir(path.cifs_dir): 
                pathexist = 1
                self.__cif_dir= path.cifs_dir
                self.cifs_dir_valids=path.cifs_dir_valids
                self.cifs_dir_invalids=path.cifs_dir_invalids
                self.__cifs_dir_output= path.cifs_dir_output
                self.__core_dic_filepath=path.core_dic_filepath
                self.__mpod_dic_filepath=path.mpod_dic_filepath
                break
               
        filenamempod = filename + ".mpod"
        filepath=os.path.join(self.__cifs_dir_output, filenamempod)
        self.cif_created=filenamempod
        
        
        
        try:
            files = os.listdir(str(self.__cifs_dir_output))
        except:
            os.mkdir(str(self.__cifs_dir_output)) 
            files = os.listdir(str(self.__cifs_dir_output))
    
        print files
        if len(files) == 0:
            print  "folder empty"
        else:
            print  "folder no empty"
            for the_file in files:
                file_path = os.path.join(str(self.__cifs_dir_output), the_file)
                 
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    #elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    print(e)
                
                
        
        self.fid = open(filepath,'w') 
        
         
        if self.fid == None:
            self.fid.write('Unable to write to %s' % (filenamempod))
        
        mode='ascii'
        self.__mpod_str = "#------------------------------------------------------------------------------" +"\n"

        
        dt=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        
        x=datetime.datetime.today().strftime('%d %b %Y')
        
        #days=list(calendar.day_name)
        days=list(calendar.day_abbr)
        
        dayname=days[datetime.datetime.today().weekday()]




        self.__mpod_str = self.__mpod_str + "#$Date: %s " % (dt) + "+0000 ("+dayname+", " +x+") $\n"
        self.__mpod_str = self.__mpod_str + "#$Revision: %s " % (mpf.revision)+ "$\n"
        self.__mpod_str = self.__mpod_str + "#------------------------------------------------------------------------------" +"\n"
        self.__mpod_str = self.__mpod_str + "#" +"\n"
         
        lins1 = map(lambda x: x.strip(),   mpf.description1.strip().split("<br/>"))
        code=0
        for li in lins1:
            self.__mpod_str = self.__mpod_str + "# " + li + "\n"
        
        self.__mpod_str = self.__mpod_str + "# " +mpf.site +"\n"
        
        self.__mpod_str = self.__mpod_str + "#" +"\n"
        
        lins2 = map(lambda x: x.strip(),   mpf.description2.strip().split("<br/>"))
        #if "\n" in mpf.description2
        
        code=0
      
        for li in lins2:
            self.__mpod_str = self.__mpod_str + "# " + li + "\n"  
            
        self.__mpod_str = self.__mpod_str + "#" +"\n"
        
        self.__mpod_str = self.__mpod_str + "data_"+filename +"\n"
        
        self.__mpod_str = self.__mpod_str + "_cod_database_code ?"+"\n"
        
        
        
        
    def addline(self,line):
        self.__mpod_str =self.__mpod_str  + line
        
    def addinfo(self):
        
        for p  in self.__propertyMaster.propertyList:
            if self.__propertyMaster.puntualgroup  != "":
                if self.__symmetry_point_group_name == False:         
                    self.__line =  "_symmetry_point_group_name_H-M" + " " + self.__propertyMaster.puntualgroup+"\n"      
                    self.addline(self.__line)    
                        
                    self.__symmetry_point_group_name = True
            else:
                if self.__symmetry_point_group_name == False: 
                    self.__line =  "_symmetry_point_group_name_H-M" + " ?" + "\n"      
                    self.addline(self.__line)   
                    
                    self.__symmetry_point_group_name = True
                    
                    
                
            if self.__condition==False :  

                if self.__propertyMaster.headerBlockValues != None:
                    for key,value in self.__propertyMaster.headerBlockValues.items():
                        if key[1] == "char" or key[1] == None:
                            self.__line =  key[0] + " '" + value +"'" +"\n"
                            self.addline(self.__line) 
                        elif key[1] == "numb":
                            self.__line =   key[0]  + " " + value  +"\n"
                            self.addline(self.__line) 
                        
                    
                self.__condition=True
                

            if self.__loop_article_info==False:  
                self.__line =  "loop_" +"\n"
                self.addline(self.__line)   
                self.__line =  "_publ_author_name"  +"\n"
                self.addline(self.__line)   
                
              
                lins1 = map(lambda x: x.strip(),   self.__propertyMaster.authors.strip().split(","))
                print "authors"
                for li in lins1:
                    self.__line ="'" + li + "'\n"
                    self.addline(self.__line)   
                     
                if self.__section_title == False:
                    self.__section_title = True
                    
                    self.__line =  "_publ_section_title"  +"\n"
                    self.addline(self.__line)   
                    self.__line =  ";"  +"\n"
                    self.addline(self.__line)   
                    self.__line =  self.__propertyMaster.title  +"\n"
                    self.addline(self.__line)   
                    self.__line =  ";"  +"\n"
                    self.addline(self.__line)   
                    
                    self.__line = '_journal_name_full ' + "'"+self.__propertyMaster.journal +"'"+" \n"
                    self.addline(self.__line)   
                    self.__line = '_journal_volume  ' + "'"+self.__propertyMaster.volume +"'"+" \n"
                    self.addline(self.__line)   
                    self.__line = '_journal_page_first  ' + "'"+self.__propertyMaster.page_first +"'"+" \n"
                    self.addline(self.__line)  
                    self.__line = '_journal_page_last  ' + "'"+self.__propertyMaster.page_last +"'"+" \n"
                    self.addline(self.__line)    
                        
                          
                    self.__line = '_journal_year  ' + "'"+self.__propertyMaster.year +"'"+" \n"
                    self.addline(self.__line)                  
                
                self.__loop_article_info=True 
            
               

               
            if p.loopBlockValues != None:
                for key,value in p.loopBlockValues.items():
                    if key[0] not in self.__loopBlock:
                        self.__loopBlock.append(key[0])
                    else:
                        pass
                
         
                    
           
            self.__line =  p.objDataProperty.tag +" '"+p.tag+"'" + "\n"
            self.addline(self.__line)
                     
 
     
    def adddatavalue(self):
        
       
        for p  in self.__propertyMaster.propertyList:
            
            if self.__loop_tag==False:  
                self.__line =  "loop_" +"\n"
                self.addline(self.__line)   
                self.__line =  "_prop_data_label"  +"\n"
                self.addline(self.__line)   
                self.__line =  "_prop_data_tensorial_index"  +"\n"
                self.addline(self.__line)   
                self.__line =  "_prop_data_value"  +"\n"
                self.addline(self.__line)   
                
                
                
                for item in self.__loopBlock:
                    self.__line =  item  +"\n"
                    self.addline(self.__line) 
                 

                        
                self.__loop_tag=True     
                
                
            dim= p.coefficientsmatrix.shape
            self.maxmatrixnonceros = (p.coefficientsmatrix != 0) 
            if len(dim) == 2:
                for i in range(0,dim[0]):
                    for j  in range(0,dim[1]):    
                        tagindex = str(i +1 )  + str(j + 1)
                        tag = p.tag.replace('ij',tagindex);
                        lineloop = ""
                        try:
                            value1 = p.formargsvalitated[0][tag]
                            value2 = p.formdata[0][tag]
                            if p.loopBlockValues:
                                for x, item in enumerate(self.__loopBlock):
                                    lineloop = lineloop +" " +str(p.loopBlockValues[p.loopBlockValues.keys()[x]]  )
        
                                self.__line= p.tag +" " + tagindex + " "+ str(value2) + " " + lineloop+  "\n"     
                            else:
                                for x, item in enumerate(self.__loopBlock):
                                    lineloop = lineloop +" " +"?"  
                                    
                            if p.symmetry:  
                                
                                if dim[0] == 6  and dim[1] == 6:  
                                    if (self.maskmatrix6x6[i][j] and self.maxmatrixnonceros[i][j]):
                                            self.__line= p.tag +" " + tagindex + " "+ str(value2) + " " + lineloop +   "\n"     
                                            self.addline(self.__line)  
                                elif  dim[0] == 3  and dim[1] == 3:  
                                    if(self.maskmatrix3x3[i][j] and self.maxmatrixnonceros[i][j]):
                                        self.__line= p.tag +" " + tagindex + " "+ str(value2) + " " + lineloop +   "\n"     
                                        self.addline(self.__line)  
                                else:
                                    pass
                                
                            else:
                                if(self.maxmatrixnonceros[i][j]):
                                    self.__line= p.tag +" " + tagindex + " "+ str(value2) + " " + lineloop +   "\n"   
                                    self.addline(self.__line)   
                                
                                
                        except  Exception as e:
                            print " Error: {1}".format( e.message, e.args) 
                            self.message = " Error: {1}".format( e.message, e.args) 
                            self.sucess = 0
                            return     
                        
            elif len (dim) == 1:
                pass

 
                 

           
        
            
    def savefile(self):
        print self.__mpod_str     
        
        #print self.__mpod_str.encode('unicode')
        self.fid.write(self.__mpod_str.encode('utf-8'))
        self.fid.close()
        #print self.fid.name
        #print self.cif_created
  
        validator = CifMpodValidator(str(self.__cifs_dir_output),str(self.__core_dic_filepath),str(self.__mpod_dic_filepath),'')
        
        try:
            validator.getValidation()
        except Exception  as e:
            #print " Error: {1}".format( e) 
            self.message =  e
            self.sucess = 0
            return     
        
        
        objectValidateds=validator.resultListVaild
        
        for objectValidated in objectValidateds:
            print objectValidated
            self.reportValidation=objectValidated

      
        if not os.path.exists(str(self.cifs_dir_valids)):          
            os.mkdir(str(self.cifs_dir_valids)) 
            
           
            
        filelist = []
        for code in validator.codeListValid:
            #print code
            #print self.fid.name    
            print os.path.join(str(self.cifs_dir_valids), self.cif_created)
            filelist.append(self.cif_created)
            move(self.fid.name, os.path.join(str(self.cifs_dir_valids), self.cif_created))
            self.valid=True
            
      

        estr = Extractor(str(self.cifs_dir_valids),str(self.__core_dic_filepath),str(self.__mpod_dic_filepath),str(self.__cifs_dir_output),filelist);
        estr.extractConditions(False)
        estr.extractPublarticleAndDataFile_Data(False)
        estr.extractProperties(False)
        
       
    if __name__ == "__main__":      
        '''cifs_dir='/EclipseWork/mpod/media/datafiles/test/'
        core_dic_filepath='/EclipseWork/mpod/media/dictionary/cif_core.dic'
        mpod_dic_filepath='/EclipseWork/mpod/media/dictionary/cif_material_properties_0_0_6.dic'
        cifs_dir_output=''
        validator = CifMpodValidator(cifs_dir,core_dic_filepath,mpod_dic_filepath,'')
        validator.getValidation()
        objectValidateds=validator.resultListVaild 
        
        for objectValidated in objectValidateds:
         print objectValidated
         
         for code in validator.codeListValid:
            print code'''
   
    