'''
Created on Jul 23, 2017

@author: admin
'''
from CifMpodValidator import *
from data.ExtractorDataFromCIF import *
from shutil import  *

if __name__ == '__main__':

   
    pathslist=Path.objects.all()      
    pathexist = 0
    cifs_dir=''
    for cifdir in pathslist:
        paths=Path() 
        paths = cifdir
        if os.path.isdir(paths.cifs_dir): 
            pathexist = 1
            cifs_dir= paths.stl_dir
            break
    
    validator = CifMpodValidator(str(paths.cifs_dir),str(paths.core_dic_filepath),str(paths.mpod_dic_filepath),str(paths.cifs_dir_output))
    validator.getValidation()
    objectValidateds=validator.resultListVaild
    
    for objectValidated in objectValidateds:
        print objectValidated
    '''
    for code in validator.codeListValid:
        #print code              
        move(str(paths.cifs_dir)+code+".mpod", str(paths.cifs_dir_valids)+code+".mpod")
         #copyfile(str(paths.cifs_dir)+code+".mpod", str(paths.cifs_dir_valids+code+".mpod"))
           
           
    for code in validator.codeListInvalid:
        #print code              
        move(str(paths.cifs_dir)+code+".mpod", str(paths.cifs_dir_invalids)+code+".mpod")
        #copyfile(str(paths.cifs_dir)+code+".mpod", str(paths.cifs_dir_invalids+code+".mpod"))
        '''
    
        
    '''pathslist=Path.objects.all()      
    pathexist = 0
    cifs_dir=''    
    for cifdir in pathslist:
        paths=Path() 
        paths = cifdir
        if os.path.isdir(paths.cifs_dir): 
            pathexist = 1
            cifs_dir= paths.cifs_dir
            break
        
    estr = Extractor(str(paths.cifs_dir),str(paths.core_dic_filepath),str(paths.mpod_dic_filepath),str(paths.cifs_dir_output));
    estr.extractConditions(False)
    estr.extractPublarticleAndDataFile_Data(False)
    estr.extractProperties(False)'''
    
    
    
    
    print "fin de validacion"