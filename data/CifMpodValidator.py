'''
Created on Nov 25, 2014

@author: admin
'''
import sys

#sys.path.append('C:\\EclipseWork\\.metadata\\.plugins\\org.eclipse.wst.server.core\\tmp0\\wtpwebapps\\test\\WEB-INF\\lib\\Lib');
#sys.path.append('/jython2.5.3/Lib/site-packages')
#sys.path.append('/jython2.5.3/Lib')

import CifFile
import os



class CifMpodValidator():
   def __init__(self,cifs_dir,core_dic_filepath,mpod_dic_filepath,cifs_dir_output):
      self.cifs_dir=cifs_dir
      self.core_dic_filepath=core_dic_filepath
      self.mpod_dic_filepath=mpod_dic_filepath
      self.cifs_dir_output =cifs_dir_output
      self.codeListValid= []
      self.codeListInvalid = []
      self.resultListVaild = []
      self.resultListInvalid = []
      self.fds=os.listdir(self.cifs_dir)
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
            
            
            
        

   def UploadFile(self):  
       for fil in self.filets[:]:
            filepath=os.path.join(self.cifs_dir, fil)
            fileOutpath=os.path.join(self.cifs_dir_output, fil)
            print filepath
            in_file = open(filepath, 'r')
            lins = in_file.readlines()
            in_file.close()
            ind_beg = 0
            for i_l, lin in enumerate(lins):
                if lin.startswith('data_1000'):
                    ind_beg = i_l
                    break
            new_lins = lins[:ind_beg]
        
            new_lins2 = []
            for li in lins[ind_beg:]:
                if not li.startswith('#'):
                    new_lins.append(li)
        
            new_lins.extend(new_lins2)
        
            texto = ''.join(new_lins)
            
            #out_file = open(filepath, 'w')
            out_file = open(fileOutpath, 'w')
            
            
            
            out_file.write(texto)
            out_file.close()     
       return texto