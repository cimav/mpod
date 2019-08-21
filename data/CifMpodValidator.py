'''
Created on Nov 25, 2014

@author: admin
'''
import sys
import CifFile
import os

class CifMpodValidator():
    
    def __init__(self,cifs_dir,core_dic_filepath,mpod_dic_filepath,fileList=None):
        self.cifs_dir=cifs_dir
        self.core_dic_filepath=core_dic_filepath
        self.mpod_dic_filepath=mpod_dic_filepath
        #self.cifs_dir_output =cifs_dir_output
        self.codeListValid= []
        self.codeListInvalid = []
        self.resultListVaild = []
        self.resultListInvalid = []
        self.fds=os.listdir(self.cifs_dir)
        
        if fileList != None:
            self.fds2=filter(lambda x: x[-5:]==".mpod",  fileList)
            self.filets=sorted(filter(lambda x: os.path.isfile(os.path.join(self.cifs_dir,  x)), self.fds2))
        else:
            self.fds2=filter(lambda x: x[-5:]==".mpod",  self.fds)
            self.filets=sorted(filter(lambda x: os.path.isfile(os.path.join(self.cifs_dir,  x)), self.fds2))
        
        print self.fds2


   
    def getValidation(self):
        core_dic = CifFile.CifDic(self.core_dic_filepath)
        mpod_dic = CifFile.CifDic(self.mpod_dic_filepath)
        
        for fil in self.filets[:]:
            filepath=os.path.join(self.cifs_dir, fil)
            df=CifFile.ReadCif(filepath)
            val_report = CifFile.validate(filepath,  diclist=[self.core_dic_filepath, self.mpod_dic_filepath])
            result = CifFile.validate_report(val_report)
            #self.resultFiles.append(result);
            
            rf = result.find('VALID')
            k=df.keys()
            
            #print result
            #print k
            
            if rf>-1:
                self.codeListValid.append(k[0])               
                self.resultListVaild.append(result)
            else:             
                self.codeListInvalid.append(k[0])
                self.resultListInvalid.append(result)
            
            
            
        
    
