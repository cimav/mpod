'''
Created on 06/07/2019

@author: Jorge Torres
'''

from data.ExtractorDataFromCIFv2 import *
from django.utils.timezone import get_current_timezone
from data.UtilsForm import *

class ExtractDataFormFields(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.customdir =  None
 
        #self.loadtodatabase = False
        self.fds2 = []    
        self.user= None
        self.debug = False
        self.customForm= None
        self.fileuserutil = None
        self.estr = Extractor();
 
        
        
    def processData(self, loadtodatabase, filelist, customfile,makevalidation=None):
 
        categoryTagName1 = list(CategoryTag.objects.filter(id=1).values_list('name',flat=True))[0]#conditions 
        categoryTagName2 = list(CategoryTag.objects.filter(id=2).values_list('name',flat=True))[0]#porperties
        
         

        if isinstance(filelist, list):
            pass
        else:
            self.error = 'Parameter was not a list'
            return False


        for file in filelist:
            #print file
            self.estr.filename = None
            self.estr.dataFile = None
            self.estr.fileuser = None
            self.fileuserutil =  FileUserUtil() 
            if customfile:
                if os.path.exists(os.path.join(self.customdir,file)):
                    self.fileuserutil.custom_cifs_dir = self.customdir
                else:
                    self.error = 'File or path does not exist'
                    return False
            
            self.fileuserutil.setFile(file)
            if not self.fileuserutil.fileexist:
                break
            
            error = self.fileuserutil.parseFile()#  
            if   error:
                break
        
            if loadtodatabase:
                
                self.estr.user = self.user
                if customfile:
                    self.estr.cifs_dir_custom = self.customdir
                    
                
                self.estr.makevalidation = makevalidation
            else:
                self.customForm = CustomForm()
            
            #1000001.mpod
            #qwryety5hcfeszzcemnijzj.mpod
            
            code = None
            datacount= len(self.fileuserutil.fileParsedList)
            datacounter = 0
            if self.fileuserutil.fileParsedList:
                for fileParsed in self.fileuserutil.fileParsedList:
                    
                    if loadtodatabase:
                        self.estr.data = None 
                        if self.estr.filename == None:
                            if fileParsed.fields.has_key('filename'):
                                fname = fileParsed.fields['filename' ]
                                code = self.estr.get_data_code_linv2(fname)
                                self.estr.data_code['code'] = code
                                
                                self.estr.filename = fname
                                if self.estr.dataFile == None:
                                    if self.estr.prepareDataFile():
                                        if self.estr.message:
                                            print self.estr.message
                                            
                                        else:
                                            pass
                                    else:
                                        print self.estr.error
    
                            #print fname
                        
                    """if loadtodatabase:
                        self.estr.data = None  
                    """  
                    
                    for key,value in fileParsed.fields.iteritems():
                        if key != 'filename':
                            print '-----------------------------------------------------------------------' +key + '-----------------------------------------------------------------------'
    
                        keysplit = None
                        if loadtodatabase:
                            if not self.estr.data:
                                if fileParsed.fields.has_key('data'):
                                    data = fileParsed.fields['data' ]
                                    da = 'data_'
                                    dataval = data[0]
                                    datavalsplit=  (dataval.split())[1]
                                    datacode= datavalsplit.replace(da,'')
                                        
                                    if self.estr.publish == False:
                                        pass
                                    else:
                                        filedatacode = (fname.replace('.mpod', ' ')).strip().strip("'").strip()
                                        newdatacode =    str(self.estr.dataFile.code)
                                        datacode= datacode.replace(filedatacode, newdatacode)
                                    
                                    
                                    
                                    self.estr.data =  datacode.strip().strip("'").strip()
                                    
                                   

                        else:
                            data = fileParsed.fields['data' ]
                            dataval = data[0]
                            datavalsplit=  (dataval.split())[1]
                        
    
                        
                            #if loadtodatabase:
                        keysplit = key.split('_')
                            #print keysplit[0]
                            
                        
                        if isinstance(value,dict):
                            if loadtodatabase:
                                pass
                            else:
                                if datacount ==1:
                                    self.customForm.createAdminFields(keysplit[0])
                                else:
                                    if not self.customForm.currentdata:
                                        self.customForm.createAdminFields(datavalsplit)
                                        self.customForm.currentdata = datavalsplit
                            
                            
                            
                            alllooped = []
                            propsloop = []
                            condloop =[]
                            if isinstance(value,dict):
                                if fileParsed.fields.has_key(str(categoryTagName2) +  '_looped'):
                                    propsloop= fileParsed.fields[str(categoryTagName2) + '_looped']
                                    
                                if fileParsed.fields.has_key(str(categoryTagName1) + '_looped'):
                                    condloop = fileParsed.fields[str(categoryTagName1) + '_looped'] 
                                    
                                    
                                alllooped =propsloop + condloop
                                                
                            for k,v in  value.iteritems():
                                #print k
                                if isinstance(value[k],list):
                                    #print value[k]
                                    propertyloopedname = None
                                    propertyloopednamejquery = None
                                    tensorval1 = None
                                    tensorval2 = None
                                    tensorval3 = None
                                    tensorrules = None
                                    
                                    for v1 in value[k]:
                                        if v1.has_key('propertyloopedname'):
                                            propertyloopedname= v1['propertyloopedname']
                                            
                                        if v1.has_key('propertyloopednamejquery'):
                                            propertyloopednamejquery= v1['propertyloopednamejquery']
                                            
                                        if v1.has_key('tensorrules'):
                                            tensorrules= v1['tensorrules']
                                            

                                        if v1.has_key(str(categoryTagName1) + '_looped_consolidated'):   
                                            tensorval1 =  v1[str(categoryTagName1) + '_looped_consolidated']
                                        
                                        if v1.has_key(str(categoryTagName2) + '_looped_val'):
                                            tensorval2 =  v1[str(categoryTagName2) + '_looped_val']
                                        
                                        if v1.has_key(str(categoryTagName2) + '_looped_lines_counter'):
                                            tensorval3 =  v1[str(categoryTagName2) + '_looped_lines_counter']
    
                                    if isinstance(tensorval2,dict):
                                        lin= propertyloopedname[0] + propertyloopedname[1]
                                        #print lin, propertyloopedname[2]
                                        if loadtodatabase:
                                            pass
                                        else:
                                            self.customForm.rules = tensorrules
                                            if datacount ==1:
                                                self.customForm.addFormFields(lin,keysplit[0],propertyloopedname[2],'p')
                                                self.customForm.addFormFields(lin,keysplit[0],propertyloopednamejquery,'jq')
                                            else:
                                                self.customForm.addFormFields(lin,datavalsplit,propertyloopedname[2],'p')
                                                self.customForm.addFormFields(lin,datavalsplit,propertyloopednamejquery,'jq')
 
                                                                
                                        if loadtodatabase:
                                            for k1,v2 in  tensorval2.iteritems():
                                                if loadtodatabase:
                                                    if tensorval2:
                                                        #print tensorval2[k1]
                                                        if (self.estr.extractProperties(propertyloopedname[1:],False,tensorval2,k1)):
                                                            pass
                                                        else:
                                                            break
                                                        
                                                    if tensorval1:
                                                        #print tensorval1[k1]
                                                        
                                                        if (self.estr.extractConditions(tensorval1,True,k1)):
                                                            pass
                                                        else:
                                                            print self.estr.error
                                                            break
                                                        
                                                else:
                                                    if tensorval3:
                                                        for k2, v2 in tensorval3[k1].iteritems():
                                                            #print tensorval3[k1][k2]
                                                            pass
                                                        
                                                print '\n' 
                                   
                                            print '\n'   
                                            
                                        else:
                                            if not self.debug:
                                                for k1,v2 in  tensorval2.iteritems():
                                                    
                                                    alloopednumerline ={}
                                                    if alllooped:    
                                                        for alloop in alllooped:
                                                            nl=alloop.split()
                                                            alloopednumerline[str(nl[1])] = str(nl[0])
                                                       

                                                    if tensorval1:
                                                        if tensorval3:
                                                            listlines= []
                                                            for k2, v2 in tensorval3[k1].iteritems():
                                                                listlines.append(int((tensorval3[k1][k2][0]).split('_')[0]))
                                                            
                                                        listlines.sort()                                                        
                                                        for k5,v5 in (tensorval1[k1][0]).iteritems():
                                                            if alloopednumerline.has_key(k5):
                                                                li = alloopednumerline[k5] + '_' + str(listlines[0])+ '_' +str(listlines[-1]) + ' ' + k5 + ' '
                                                            
                                                                                    
                                                            l = len(v5) - 1
                                                            for i, c in enumerate(v5):
                                                                if i < l:
                                                                    li +=  c.strip().strip("'").strip() + ' '
                                                                else:
                                                                    li +=  c.strip().strip("'").strip()  
                                                                
                                                            print li
                                                            if datacount ==1:
                                                                self.customForm.addFormFields(li,keysplit[0],None,'char')
                                                            else:
                                                                self.customForm.addFormFields(li,datavalsplit,None,'char')
                              
                                                    if tensorval2:
                                                        if datacount ==1:
                                                            self.customForm.extractTensors(propertyloopedname,tensorval2,tensorval3,k1,keysplit[0])
                                                        else:
                                                            self.customForm.extractTensors(propertyloopedname,tensorval2,tensorval3,k1,datavalsplit)
             
                                                    
                                            else:
                                                for k1,v2 in  tensorval2.iteritems():
                                                    if tensorval2:
                                                        print tensorval2[k1]
    
                                                    if tensorval1:
                                                        print tensorval1[k1]
       
                                                    if tensorval3:
                                                        for k2, v2 in tensorval3[k1].iteritems():
                                                            print tensorval3[k1][k2]
                                                                
                                                                
                                            
                                            
                                                print '\n' 
                                   
                                            print '\n'   
                                            
                                            
                            
                        elif isinstance(value,list):
                            
                            if loadtodatabase:
                                if categoryTagName1+ '_nolooped' == key:
                                    if value:
                                        if (self.estr.extractConditions(value,False)):
                                            pass
                                        else:
                                            break
                                                    
                                elif  keysplit[0] == 'undefined':
                                    if value:
                                        if (self.estr.extractUndefined(value)):
                                            pass
                                        else:
                                            break
                                    
                                elif  keysplit[0] in ['article', 'material' , 'general']: 
                                    if value:
                                        if (self.estr.extractOther(value,keysplit[0])):
                                            pass
                                        else:
                                            break
    
                                else:
                                    for item in value:
                                        print item
                                    
                            else:
                                if not self.debug:
                                        
                                    if categoryTagName1+ '_nolooped' == key:
                                        if value:
                                            if datacount ==1:
                                                self.customForm.createAdminFields(keysplit[0])
                                            else:
                                                if not self.customForm.currentdata:
                                                    self.customForm.createAdminFields(datavalsplit)
                                                    self.customForm.currentdata = datavalsplit
                                            
                                        for item in value:
                                            #print item
                                            if datacount ==1:
                                                self.customForm.addFormFields(item,keysplit[0],None,'char')
                                            else:
                                                self.customForm.addFormFields(item,datavalsplit,None,'char')
                                        
                                    elif  keysplit[0] == 'undefined':
                                        if value:
                                            if datacount ==1:
                                                self.customForm.createAdminFields(keysplit[0])
                                            else:
                                                if not self.customForm.currentdata:
                                                    self.customForm.createAdminFields(datavalsplit)
                                                    self.customForm.currentdata = datavalsplit
                                            
                                        for item in value:
                                            #print item
                                            if datacount ==1:
                                                self.customForm.addFormFields(item,keysplit[0],None,'p')
                                            else:
                                                self.customForm.addFormFields(item,datavalsplit,None,'p')
                                        
                                        
                                    elif  keysplit[0] in ['material' , 'general']:
                                        if value:
                                            if datacount ==1:
                                                self.customForm.createAdminFields(keysplit[0])
                                            else:
                                                if not self.customForm.currentdata:
                                                    self.customForm.createAdminFields(datavalsplit)
                                                    self.customForm.currentdata = datavalsplit
                                            
                                        for item in value:
                                            """if (item.split())[1]:
                                                if  (item.split())[1] =='_symmetry_point_group_name_H-M':
                                                    symmetrypg = (item.split())
                                                    self.customForm.symmetry_point_group_name_H_M = symmetrypg[2]
                                            """
                                                
                                            if datacount ==1:
                                                self.customForm.addFormFields(item,keysplit[0],None,'char')
                                            else:
                                                self.customForm.addFormFields(item,datavalsplit,None,'char')
                                                
                                            
                                    elif keysplit[0] == 'article':
                                        if value:
                                            if datacount ==1:
                                                self.customForm.createAdminFields(keysplit[0])
                                                if (self.customForm.extractOther(value,keysplit[0])):
                                                    pass
                                                else:
                                                    break
                                            else:
                                                if not self.customForm.currentdata:
                                                    self.customForm.createAdminFields(datavalsplit)
                                                    self.customForm.currentdata = datavalsplit
                                                    
                                                if (self.customForm.extractOther(value,datavalsplit)):
                                                    pass
                                                else:
                                                    break

                                    else:
                                        for item in value:
                                            print item        
                      
                                        
                                    
                                    
                                    
                                else:
                                    for item in value:
                                        print item
                                    
                                    
                        
                                        
                            keysplit = None
                                    
                                    
                                    
                        else:
                            if loadtodatabase:
                                pass
                            else:
                                if not self.debug:
                                    print value
                                else:
                                    print value
                                
                    
                    if loadtodatabase:
                        pass
                    else:
                        self.customForm.currentdata = None    
                        
                    datacounter += 1
                        
                    print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                    
                
                if loadtodatabase:
                    if self.estr.error:
                        break
 
                    if not self.estr.error:
                        try:
         
                            #self.estr.fileuser.date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                            if not self.estr.fileuser.date:
                                self.estr.fileuser.date = datetime.datetime.now(tz=get_current_timezone()).strftime('%Y-%m-%d %H:%M:%S')
                            #self.estr.fileuser.datafile  =  self.estr.dataFile   TODO:ValueError: Cannot assign "<DataFileTemp: 1000001, None, Al72Ni16Co8>": "FileUser.datafile" must be a "DataFile" instance.
                            if self.estr.fileuser.publish:
                                self.estr.UploadFile()
                            else:
                                if customfile:
                                    self.estr.UploadFile()
                                
                 
                                
                            
                            self.estr.fileuser.datepublished =  datetime.datetime.now(tz=get_current_timezone()).strftime('%Y-%m-%d %H:%M:%S')
                            self.estr.fileuser.save()
                            
                        except Exception  as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            err= {}
                            err['file']=fname
                            err['line']=exc_tb.tb_lineno
                            err['error']="Error: {1}".format( e.message, e.args) 
                            error = err
                             
                            #roolback
                    else:
                        print self.estr.error
                        break

                else:
                    pass