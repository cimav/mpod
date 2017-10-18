'''
Created on Jul 13, 2017

@author: admin
'''

cifs_dir="/EclipseWork/mpod/media/datafiles/test/"
core_dic_filepath="/EclipseWork/mpod/media/dictionary/cif_core.dic"
mpod_dic_filepath="/EclipseWork/mpod/media/dictionary/cif_material_properties_0_0_6.dic"
cifs_dir_output ="/EclipseWork/mpod/media/datafiles/test/"
sql_out_file_path="/EclipseWork/mpod/media/datafiles/test/"
#from Extractor import Extractor
from data.ExtractorDataFromCIF import *
 



if __name__ == "__main__":
    estr = Extractor(cifs_dir,core_dic_filepath,mpod_dic_filepath,cifs_dir_output,sql_out_file_path);
    estr.extractConditions(False)
    estr.extractPublarticleAndDataFile_Data(False)
    estr.extractProperties(False)
    
    
    
    print "Hello PyDev!"