from data.models import *

from django.db import models
from django.db.models import Q
from django.db.models import Count
from parse_files_2 import *
from CifMpodValidator import *
 

if __name__ == "__main__":
    cifs_dir="/EclipseWork/mpod/media/datafiles/stlfiles/"
    core_dic_filepath="/EclipseWork/mpod/media/dictionary/cif_core.dic"
    mpod_dic_filepath="/EclipseWork/mpod/media/dictionary/cif_material_properties_0_0_6.dic"
    cifs_dir_output ="/EclipseWork/mpod/media/datafiles/test/"
    sql_out_file_path="/EclipseWork/mpod/media/datafiles/test/"


    validator = CifMpodValidator(cifs_dir,core_dic_filepath,mpod_dic_filepath,cifs_dir_output)

