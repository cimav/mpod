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


class MPODUtil():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def mpodwrite(self,filename):
        
        mpoffile=MpodFile.objects.all()
        mpf = MpodFile()
        mpf = mpoffile[0]
        
        pathslist=Paths.objects.all()      
        pathexist = 0
        cif_dir=''
        for cifdir in pathslist:
            path=Paths() 
            path = cifdir
            if os.path.isdir(path.cifs_dir): 
                pathexist = 1
                cif_dir= path.cifs_dir
                break
               
        filename = filename + ".mpod"
        filepath=os.path.join(cif_dir, filename)
        
        fid = open(filepath,'w') 
        if fid == None:
            fid.write('Unable to write to %s' % (filename))
        
        mode='ascii'
        mpod_str = "#------------------------------------------------------------------------------" +"\n"

        
        dt=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        
        x=datetime.datetime.today().strftime('%d %b %Y')
        
        #days=list(calendar.day_name)
        days=list(calendar.day_abbr)
        
        dayname=days[datetime.datetime.today().weekday()]



        mpod_str = mpod_str + "#$Date: %s " % (dt) + "+0000 ("+dayname+", " +x+") $\n"
        mpod_str = mpod_str + "#$Revision: %s " % (mpf.revision)+ "$\n"
        mpod_str = mpod_str + "#------------------------------------------------------------------------------" +"\n"
        mpod_str = mpod_str + "#" +"\n"
         
        lins1 = map(lambda x: x.strip(),   mpf.description1.strip().split("<br/>"))
        code=0
        for li in lins1:
            mpod_str = mpod_str + "# " + li + "\n"
        
        mpod_str = mpod_str + "# " +mpf.site +"\n"
        
        mpod_str = mpod_str + "#" +"\n"
        
        lins2 = map(lambda x: x.strip(),   mpf.description2.strip().split("<br/>"))
        #if "\n" in mpf.description2
        
        code=0
        for li in lins2:
            mpod_str = mpod_str + "# " + li + "\n"
            
        mpod_str = mpod_str + "#" +"\n"
        
        
        fid.write( mpod_str)
        fid.close()
        