'''
Created on Jul 23, 2017

@author: Jorge Torres
'''
#from CifMpodValidator import *
from data.ExtractorDataFromCIFv2 import *
from shutil import  *
import re
from data.kNotation import *
from django.http import QueryDict
from math import *
import random
from data.JScriptUtil import *
from django.db.models import Q
from django.utils.timezone import get_current_timezone
from data.ExtractDataFormFieldsUtil import *
 

if __name__ == '__main__':
    
    ct=CategoryTag.objects.get(id=int(1) )
    
    #*******************************set categorytag to dictionary**********
 
    """
    listtags=list(Property.objects.all().values_list('tag',flat=True)) 
    
    listtags=list(ExperimentalParCond.objects.filter(active=True).values_list('tag',flat=True)) 
    
    
    qs= Dictionary.objects.filter(tag__in=listtags) 
    
    for i, item in enumerate(qs):
        print item.tag
        try:
            item.categoryTag=CategoryTag.objects.get(id=1)
            item.save()
        except ObjectDoesNotExist as error:
            dic=None
            
    """
            
    
    
    #**************************subir propiedades a el diccionario********
    """cat=Category.objects.get(id=9)
    listtags=list(Dictionary.objects.all().values_list('tag',flat=True)) 
    qs= Property.objects.filter(active=True).exclude(tag__in=listtags)
    dic= None
    for i, item in enumerate(qs):
        print item.tag
        try:
            dic=Dictionary.objects.get(tag__exact=item.tag)
        except ObjectDoesNotExist as error:
            dic=None
            
        if not dic:
            dic=Dictionary()
            dic.tag = item.tag 
            dic.name = item.name 
            dic.description = item.description 
            dic.units = item.units 
            dic.units_detail = item.units_detail 
            dic.active= True
            dic.definition= ''
            #dic.deploy= True
            dic.type = '' 
            dic.category = cat
            dic.save()
    """
    
    
    #**************************extraer tags de las propiedades********
    """
    list = []
    qs= Property.objects.filter(tensor_dimensions__in=['0'])
    for i, item in enumerate(qs):
        print i,  item.tag.split("_")[2]
        if item.tag.split("_")[2] not in list:
            list.append(item.tag.split("_")[2])
        print list
        
    props_tens_tag=Tags.objects.filter(categorytag=CategoryTag.objects.get(id=2)).values_list('tag',flat=True)
 
    ct=CategoryTag.objects.get(id=2)
    for i, item in enumerate(list):   
        if item not in  props_tens_tag:
            t= Tags()
            t.tag = item
            active = True
            t.categorytag = ct
            t.save()
    """
 
    
    
  
    
 
    #fileuserutil =  FileUserUtil()
    #fileUser=FileUser.objects.get(id=6)
    #fileuserutil.setFile('1000066.mpod')
    """fileuserutil.setLoops()
    fileuserutil.getLoops()
    fileuserutil.getNoLoops()"""
 
    #newvalue = '6.8'
    #fileuserutil.findProperty('_prop_data_value',newvalue,2,'cij',11)# property  looped
    #fileuserutil.findProperty('_prop_data_value',newvalue,2,'cij',12)# property  looped
    #fileuserutil.parseFile()#  
    #fileuserutil.findProperty('_prop_measurement_method',newvalue,1)# conditions not looped 
    #fileuserutil.findProperty('_prop_conditions_temperature',newvalue,1)# conditions not looped 
    
    #fileuserutil.findProperty('_prop_data_value',newvalue,2,'no')# property  looped
    #fileuserutil.findProperty('_prop_conditions_wavelength',newvalue,2,'no')# property  looped
 
    
    #fds2 = list(DataFile.objects.filter(code__gt=1000000,code__lt=1000369).values_list('code',flat=True))
    #fds3 = list(FileUser.objects.all().values_list('datafile_id',flat=True))
    #fds4 = set(fds2) - set(fds3)
    #fds4 = [1000068L, 1000170L, 1000171L, 1000145L, 1000146L, 1000179L, 1000340L, 1000121L, 1000187L]
    """print fds4
    fds2 = list(DataFile.objects.filter(code__gt=1000000,code__lt=1000369).exclude(code__in=fds4).values_list('filename',flat=True))
    for item in  fds2:
        print item
    """
    
    
    fieldsets1= ( ('File', {'fields': ('jquery',)}))
 
    #fieldsets2=((None, {'fields': ['username', 'password']}),)
    hd= 'otro1'
    fieldsets2=((hd, {'fields': []}),)
    fieldsets2[0][1]['fields'] += ['filename'] 
    fieldsets2[0][1]['fields'] += ['authuser'] 
 
    hd = 'otro2'
    fieldsets2 +=((hd, {'fields': []}),)
    fieldsets2[1][1]['fields'] = ['authuser2'] 
    fieldsets2[1][1]['fields'] += ['dfsfsdfdsfsd'] 
    
        
    
    fieldsets = (
        ("data_1000001", {'fields': fieldsets2}),
    )
    
  
            
    paths = None
    pathslist=Path.objects.all()      
    for path in pathslist:
        if os.path.isdir(path.cifs_dir): 
            paths = Path()
            paths = path
            break
            
    test= True
    if test==True:
        #obj = FileUser.objects.get(filename='ywrtaw4=nzcthbjkasfbcxi.mpod')
        pass
        
        
 
            
 
 
        
           

 
    test = True
    
    if test==True:
 
        fromdatabase = False
        multifile = False
        #customdir = 'C:/Users/admin/Documents/'
        customdir = 'C:/EclipseWork/mpod/media/datafiles'
        customfile = False
        loadtodatabase = True
        frompath = False
        fds2 = []    
 
        if multifile:
            fds4 = [1000068L, 1000170L, 1000171L, 1000145L, 1000146L, 1000179L, 1000340L, 1000121L, 1000187L]
            if not fromdatabase:
                if frompath:
                    fds=os.listdir(paths.cif_dir)
                    fds2=filter(lambda x: x[-5:]==".mpod",  fds)
                else:
                    fds2.append("1000379.mpod")
                    fds2.append("1000380.mpod")
                    fds2.append("1000381.mpod")
                    fds2.append("1000382.mpod")
                    fds2.append("1000383.mpod")
                    fds2.append("1000384.mpod")
                
            else:
                fds2 = list(DataFile.objects.filter(code__gt=1000368,code__lt=1000378).exclude(code__in=fds4).values_list('filename',flat=True))
                #fds2 = list(DataFile.objects.filter(code__in=[1000005,1000006,1000007,1000008,1000009,1000010]).values_list('filename',flat=True))
                 
        else:
            fds2.append("qwryety5wuegwlalkrhcdpn.mpod")
 
            
            
        makevalidation=True
        edff= ExtractDataFormFields()
        edff.customdir =  customdir
        edff.user =  User.objects.get(id=16)
        edff.debug = False
        edff.processData(loadtodatabase,fds2,customfile,makevalidation)     
        
        

        
        
        
    """
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
        
    """     
        
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
    
    """    
    dictionaryTagList=[]
    dictionaryQuerySet1= Dictionary.objects.filter(category = Category.objects.get(pk=9), deploy = 1)
    dictionaryQuerySet2= Dictionary.objects.filter(category = Category.objects.get(pk=12), deploy = 1)
    dictionaryQuerySet= (dictionaryQuerySet1 | dictionaryQuerySet2).distinct()    
    for i,dictionary in enumerate(dictionaryQuerySet): 
        dictionaryTagList.append(dictionaryQuerySet[i].tag)
        
        
 
    """        
    
    """def _ssh(hostname, port):
        pass

    def _telnet(hostname, port):
        pass 
    
    def _mosh(hostname, port):
        pass
    
    
    protocols = {
        'ssh': _ssh,
        'mosh': _mosh,
        'telnet': _telnet
    }

    # call your function by string
    hostname = 'localhost'
    port = '22'
    protocol = 'ssh'
    result = protocols[protocol](hostname, port)
    
    protocol = 'mosh'
    result = protocols[protocol](hostname, port)
    
    protocol = 'telnet'
    result = protocols[protocol](hostname, port)
    """

 
    pathslist=Path.objects.all()      
    pathexist = 0
    cifs_dir=''    
    for cifdir in pathslist:
        paths=Path() 
        paths = cifdir
        if os.path.isdir(paths.cifs_dir_valids): 
            pathexist = 1
            cifs_dir= paths.cifs_dir_valids
            break
            
 
    
    filelist = []    
    filelist.append("n.mpod")
    estr = Extractor(str(paths.cifs_dir_valids),str(paths.core_dic_filepath),str(paths.mpod_dic_filepath),str(paths.cifs_dir_output),filelist);
    approved = False
    estr.extractConditions(approved)
    estr.extractPublarticleAndDataFile_Data(approved)
    estr.extractProperties(approved)
    user= User.objects.get(id=16)
 
    for key,code in estr.data_code.items():
        fileuser = FileUser()
        fileuser.authuser=user 
        code=estr.data_code[key[0],key[1]]
        dataFile = DataFileTemp.objects.get(filename='zahtcdfxluqcgewdl.mpod')
        if approved:
            fileuser.datafile = dataFile
            
        fileuser.filename= key[0]
        #fileuser.save()


    
    
    print "fin"