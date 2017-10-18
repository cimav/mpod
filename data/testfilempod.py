'''
Created on Jul 14, 2017

@author: admin
'''
from data.models import *

from django.db import models
from django.db.models import Q
from django.db.models import Count
from parse_files_2 import *
 

if __name__ == "__main__":
    tg="_prop"
    props = []
    fil = "1000367.mpod"
    dataitem_id = "1000367"
#    fil = "1000097.mpod"
#    fil = "1000272.mpod"
#    fil = "1000196.mpod"  
    #data_item_html("1000367.mpod")
  
    datafile_item = DataFile.objects.get(code__exact = dataitem_id)
    
    datafiles_path="/EclipseWork/mpod/media/datafiles/test"   
    mpod_filepath = os.path.join(datafiles_path, dataitem_id+".mpod")
    file_data_blocks = parse_mpod_file(mpod_filepath)
    print 'file_data_blocks', file_data_blocks
    tenso_props, nl_props, l_props = all_props_list(file_data_blocks)
    print 'tenso_props', tenso_props
    print 'nl_props', nl_props
    print 'l_props', l_props
    
    tenso_props_dims_dict = {}
    tenso_props_ids_dict = {}
    tenso_props_units_dict = {}
    lnl_props_ids_dict = {}
    lnl_props_units_dict = {}
    for tp in tenso_props:
        tprp = Property.objects.get(tag__exact = tp)
        tenso_props_dims_dict[tp] = tprp.tensor_dimensions
        tenso_props_ids_dict[tp] = tprp.id
        tenso_props_units_dict[tp] = tprp.units
    for nlp in nl_props:
        nlprp = ExperimentalParCond.objects.get(tag__exact = nlp)
        lnl_props_ids_dict[nlp] = nlprp.id
        lnl_props_units_dict[nlp] = nlprp.units
    for lp in l_props:
        lprp = ExperimentalParCond.objects.get(tag__exact = lp)
        lnl_props_ids_dict[lp] = lprp.id
        lnl_props_units_dict[lp] = lprp.units
    props_ids = [tenso_props_dims_dict, tenso_props_ids_dict, lnl_props_ids_dict,
     tenso_props_units_dict, lnl_props_units_dict ]
    formatted_data_blocks = format_data_blocks(file_data_blocks, props_ids)
    '''t_tables = get_template('data/view_dataitem_tensors_new.html')
    html_datafile = html_linked_dataitem(datafile_item)
    c_tables=Context({
    'header': "Property values",
    'formatted_data_blocks' : formatted_data_blocks,
    })
    html_tables = t_tables.render(c_tables)'''
    
    #return html_datafile, html_tables