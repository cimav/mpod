'''
Created on Feb 10, 2019

@author: Jorge Alberto Torres Acosta
'''

import os
import numpy as N
from django.db import models
from data.models import *
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import re
from data.Utils import *
#from data.JScriptUtil import *
#from django.db.models.query import QuerySet
from data.JQueryCode import *
import collections
 

class Propertiesv2(object):


    def __init__(self,catalogproperty_name, csn ,typesc,datapropertytagselected,ismagnetoelectricity,  *args,  **kwargs):
            """self.title =  ""
            self.authors =  ""
            self.journal =  ""
            self.volume =  ""
            self.year = ""
            self.page_first =  ""
            self.page_last = ""
            """
            self.formdata = args
            self.formargsvalitated=None
            self.catalogproperty_name = catalogproperty_name
            self.type = typesc # s (compliance) o c (stiffness)?
            self.crystalsystem_name = csn
            self.pointgroupselected_name =None
            self.axisselected_name =None
            self.dataproperty = datapropertytagselected
            #self.coefficientsparts =[]
            #self.coefficientspartssplit = []
            
            self.message=''
            self.questionAxis=''
            self.questionGp =''
            self.objCatalogPointGroupSelected =None            
            self.objProperty  =None
            self.objTypeSelected  =None
            self.objCatalogCrystalSystemSelected  =None
            self.objAxisSelected=None
            self.objPointGroupNamesSelected = None
            self.dictionaryValues = None
            self.loopBlockValues = None
            self.catalogPropertyDetail=[]
            self.catalogPropertyDetailReadOnly = []
            self.propertyDetail = None
            self.pointGroupList=[]
            self.pointGroupListNames =[]
            self.pointGroupNamesList = []
            self.axisList =[]
            self.listofemptyInputs =[]
            self.magnetoelectricity = None
            if ismagnetoelectricity == False:
                self.magnetoelectricity = 0
            else:
                self.magnetoelectricity = 1
                
                
            self.objDataProperty = None
            self.scij = ''
            self.tag = ''
            self.symmetry = None
            self.jquery= ""
            
            self.__inputList = []
            self.s = N.zeros([6,6])
            self.c = N.zeros([6,6])
            self.d = N.zeros([3,6])
            self.k = N.zeros([3,3])
            self.coefficientsmatrix = None
            self.coefficientsmatrix1 = None

            if 'inputList' in kwargs:
                self.__inputList  = kwargs.pop('inputList' )

            self.__dict = {}
            self.read_write_inputs = {}
            
            
            self.sucess = 0
            

                        
    def NewProperties(self,pgn,aname,*args):
        self.formargsvalitated=args
        try:
            self.objProperty=CatalogProperty.objects.get(name=self.catalogproperty_name)
            typeQuerySet=Type.objects.filter(active=True,catalogproperty= self.objProperty)   
            type_ids = getIdsFromQuerySet(typeQuerySet) 
            
            #*******************************type*************************************
            if self.type != '':
                objType = None 
                try:
                    objType  = Type.objects.get(catalogproperty=self.objProperty,name=self.type)
                except ObjectDoesNotExist as error:
                    print "Message({0}): {1}".format(99, error.message) 

                if  objType != None and objType.id in type_ids:
                    self.objTypeSelected  = objType
                else:
                    self.objTypeSelected  = typeQuerySet[0]
            else:
                self.objTypeSelected  = typeQuerySet[0]
                
                
            #*******************************dataproperty*************************************
            dataproperty_ids=TypeDataProperty.objects.filter(type=self.objTypeSelected).values_list('dataproperty_id',flat=True)    
            datapropertyQuerySet=Property.objects.filter(id__in=dataproperty_ids, active=True)   
            if int(self.dataproperty) in dataproperty_ids:
                self.objDataProperty = Property.objects.get(id=int(self.dataproperty), active=True)  
            else:
                self.objDataProperty = datapropertyQuerySet[0]
             
             
            #*******************************catalogcrystalsystem*************************************
            catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty= self.objProperty)   
            catalogcrystalsystem_names=CatalogCrystalSystem.objects.filter(catalogproperty= self.objProperty).values_list('name',flat=True)                        
            if self.crystalsystem_name in catalogcrystalsystem_names:
                self.objCatalogCrystalSystemSelected = CatalogCrystalSystem.objects.get(name=self.crystalsystem_name,catalogproperty=self.objProperty) 
            else:
                self.objCatalogCrystalSystemSelected = catalogcrystalsystemQuerySet[0]   
                
                
            #*******************************catalogpointgroup*************************************
            catalogpointgroup_id = 0
            if pgn != '':
                self.pointgroupselected_name =pgn 
                catalogpointgroup_id = CatalogPointGroup.objects.filter(name__exact=pgn).values_list('id',flat=True)[0]    
                self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(id=catalogpointgroup_id)
            
            
            catalogpointgroup_ids= CrystalSystemPointGroup.objects.filter(catalogcrystalsystem=self.objCatalogCrystalSystemSelected,type=self.objTypeSelected,active=1).values_list('catalogpointgroup_id',flat=True)  
            if catalogpointgroup_ids:
                self.questionGp = 'Point Group?'  
                catalogpointgroupQuerySet =  CatalogPointGroup.objects.filter(id__in=catalogpointgroup_ids)
                for i,pggobj in enumerate(catalogpointgroupQuerySet):
                    self.pointGroupList.append(catalogpointgroupQuerySet[i])
                    self.pointGroupListNames.append(str(catalogpointgroupQuerySet[i].name))
                    
            
                if catalogpointgroup_id in catalogpointgroup_ids:
                    self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(id=catalogpointgroup_id)
                else:
                    self.objCatalogPointGroupSelected  = catalogpointgroupQuerySet[0]
            else:
                if catalogpointgroup_id in catalogpointgroup_ids:
                    self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(id=catalogpointgroup_id)
                else:
                    self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(id=45)
                    
                    
                    
            #*******************************pointgroupnames*************************************
            groups = []
            pointgroupnames_ids= CrystalSystemPointGroupNames.objects.filter(catalogcrystalsystem=self.objCatalogCrystalSystemSelected,type=self.objTypeSelected,active=1).values_list('pointgroupnames_id',flat=True)  
            if pointgroupnames_ids:
                self.questionGp = 'Point Group?'  
                pointgroupnamesQuerySet = PointGroupNames.objects.filter(id__in=pointgroupnames_ids)
                for i,pgnobj in enumerate(pointgroupnamesQuerySet):
                    objPointGroupGroups = PointGroupGroups.objects.filter(pointgroupnames=pointgroupnamesQuerySet[i])  
                    #catalogpointgroup_ids = PointGroupGroups.objects.filter(pointgroupnames=pointgroupnamesQuerySet[i]).values_list('catalogpointgroup_id',flat=True)
                    for j,pggobj in enumerate(objPointGroupGroups):
                        self.pointGroupList.append(objPointGroupGroups[j].catalogpointgroup)
                        if str(objPointGroupGroups[j].catalogpointgroup.name) not in self.pointGroupListNames:
                            self.pointGroupListNames.append(str(objPointGroupGroups[j].catalogpointgroup.name))
                            groups.append(str(objPointGroupGroups[j].catalogpointgroup.name))
     
                        if(objPointGroupGroups[j].catalogpointgroup.id ==catalogpointgroup_id):
                            self.pointgroupselected_name = objPointGroupGroups[j].catalogpointgroup.name
                            self.objPointGroupNamesSelected  = pointgroupnamesQuerySet[i]
                            
                    self.pointGroupNamesList.append(groups)
                    groups = []
                            
                if not self.objPointGroupNamesSelected:
                    self.pointgroupselected_name = objPointGroupGroups[0].catalogpointgroup.name
                    for i,pgn in enumerate(pointgroupnamesQuerySet):
                        if self.pointgroupselected_name  in pointgroupnamesParse(pointgroupnamesQuerySet[i].name):
                            self.objPointGroupNamesSelected  = pointgroupnamesQuerySet[i]
 
            else:  
                self.objPointGroupNamesSelected  = PointGroupNames.objects.get(id=21)
                
                
     
                


             
            if  self.objPointGroupNamesSelected.id ==21 and self.objCatalogPointGroupSelected.id ==45:
                self.message ="there is no registered 'Point Group' for this 'Crystal System'"
                return
            
            #*******************************axis*************************************
            axis_id = 0
            if aname != '':
                self.axisselected_name =aname
                axis_id = CatalogAxis.objects.filter(name__exact=aname).values_list('id',flat=True)[0] 
                self.objAxisSelected = CatalogAxis.objects.get(id=axis_id)

            
            #queryobj = CrystalSystemAxis.objects.filter(catalogcrystalsystem=self.objCatalogCrystalSystemSelected,catalogpointgroup= self.objCatalogPointGroupSelected,pointgroupnames = self.objPointGroupNamesSelected  ,type=self.objTypeSelected,active=1)
            #print queryobj.query
            axis_ids= CrystalSystemAxis.objects.filter(catalogcrystalsystem=self.objCatalogCrystalSystemSelected,catalogpointgroup= self.objCatalogPointGroupSelected,pointgroupnames = self.objPointGroupNamesSelected  ,type=self.objTypeSelected,active=1).values_list('axis_id',flat=True)  
            if axis_ids:
                self.questionAxis = 'Where is the special axis?' 
                axisQuerySet = CatalogAxis.objects.filter(id__in=axis_ids)
                for i,ax in enumerate(axisQuerySet):
                    self.axisList.append(axisQuerySet[i])
                
                if axis_id in axis_ids:
                    self.objAxisSelected  = CatalogAxis.objects.get(id=int(axis_id))  
                else:
                    self.objAxisSelected  = axisQuerySet[0]
                    
                self.axisselected_name = self.objAxisSelected.name
            else:
                    self.objAxisSelected  = CatalogAxis.objects.get(id=4)
             
            
            
            self.setDimension(self.objDataProperty)
            self.setCatalogPropertyDetailkeyNotation()

        except ObjectDoesNotExist as error:
            print "Message({0}): {1}".format(99, error.message)   
            self.message= "Message({0}): {1}".format(99, error.message)  
                        

            
        #*******************************Elastisity*****************************************    
        if self.catalogproperty_name == 'e':
            
            if self.crystalsystem_name == 'iso':  
                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(True)    
                    self.sucess = 1
                    return
                else:
                    self.questionGp = 'Point Group?'    
                    self.message= 'All the point groups of this crystal system have the same matrix'
                    if self.pointgroupselected_name == None or self.pointgroupselected_name == None or self.pointgroupselected_name == '':
                        return
                    
                    self.setCoefficientsforjQuery(self.type );
                    self.setCatalogPropertyDetail()
                    self.createJQueryCode(True)
 
            elif self.crystalsystem_name == 'c': 
                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(True)
                    #print (self.coefficientsmatrix)          
                    self.sucess = 1
                    return
                else:
                    self.questionGp = 'Point Group?'   
                    self.message= 'All the point groups of this crystal system have the same matrix'
                    if  self.pointgroupselected_name == None or self.pointgroupselected_name == '':
                        return

                    self.setCoefficientsforjQuery(self.type );
                    self.setCatalogPropertyDetail()
                    self.createJQueryCode(True)
                    
            elif self.crystalsystem_name == 'h': 
                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(True)
                    self.sucess = 1
                    return
                else:
                    self.questionGp = 'Point Group?'    
                    self.message= 'All the point groups of this crystal system have the same matrix'
                    if  self.pointgroupselected_name == None or self.pointgroupselected_name == '':
                        return

                    self.setCoefficientsforjQuery(self.type );
                    self.setCatalogPropertyDetail()
                    self.createJQueryCode(True)

            elif self.crystalsystem_name == 'o': 
                    if  self.formargsvalitated != None and len(self.__inputList) > 0:
                        self.setCoefficentsValues(True)   
                        self.sucess = 1
                        return
                    else:
                        self.questionGp = 'Point Group?'    
                        self.message= 'All the point groups of this crystal system have the same matrix'
                        if  self.pointgroupselected_name == None or self.pointgroupselected_name == '':
                            return

                        self.setCoefficientsforjQuery(self.type );
                        self.setCatalogPropertyDetail()
                        self.createJQueryCode(True)
                           
                    
            elif self.crystalsystem_name == 'tc':
                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(True)    
                    self.sucess = 1
                    return
                else:
     
                    self.message= 'All the point groups of this crystal system have the same matrix'
                    self.setCoefficientsforjQuery(self.type );
                    self.setCatalogPropertyDetail()
                    self.createJQueryCode(True)

 
                    
            elif self.crystalsystem_name == 'te':    
                self.questionGp = 'Point Group?'                     
                if  self.pointgroupselected_name == None or self.pointgroupselected_name == '' or self.pointgroupselected_name not in '4, -4, 4/m, 422, 4mm, -42m, 4/mmm':
                    return

                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(True)    
                    self.sucess = 1
                    return
                else:
                    self.setCoefficientsforjQuery(self.type );
                    self.setCatalogPropertyDetail()                                       
                    self.createJQueryCode(True)
                     
                    
                    
            elif self.crystalsystem_name == 'm':   
                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(True)     
                    self.sucess = 1          
                else:
                    self.questionGp = 'Point Group:'          
                    if self.pointgroupselected_name == None or self.pointgroupselected_name == '' or self.pointgroupselected_name not in '2, m, 2/m':    
                        return

                    if  self.axisselected_name   == None or self.axisselected_name   == '' or self.axisselected_name  not in 'x2, x3':
                        self.questionAxis = 'Where is the special axis?' 
                        return

                    
                    self.setCoefficientsforjQuery(self.type );
                    self.setCatalogPropertyDetail()                              
                    self.createJQueryCode(True)
 
                
            elif self.crystalsystem_name == 'tg':    
                self.questionGp = 'Point Group:'          
                if  self.pointgroupselected_name == None or self.pointgroupselected_name == '' or self.pointgroupselected_name not in '3, -3, 32, 3m, -3m':
                    return
    
                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(True)       
                    self.sucess = 1
                    return
                else:

                    self.setCoefficientsforjQuery(self.type );
                    self.setCatalogPropertyDetail()
                    self.createJQueryCode(True)
 
                     
        #*******************************Piezolectricity*****************************************            
        if self.catalogproperty_name == 'p':
            if self.crystalsystem_name == 'tc':          
                self.questionGp = 'Point Group?'   
                if  self.pointgroupselected_name ==None or  self.pointgroupselected_name == '' or self.pointgroupselected_name  not in '1, -1':
                    return
              
                if self.pointgroupselected_name == '-1':
                    self.message ='This point group does not have priezoelectricity' 
                    return

                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(False)    
                    self.sucess = 1
                    return

                else:    
                    self.setCoefficientsforjQuery(self.type );
                    self.setCatalogPropertyDetail()
                    self.createJQueryCode(False)
  
                
            if self.crystalsystem_name == 'm':
                if (self.axisselected_name == None  or self.axisselected_name == '' or self.axisselected_name not in 'x2, x3') or  (self.pointgroupselected_name == None or self.pointgroupselected_name == '' or self.pointgroupselected_name not in  '2, m, 2/m'):
                    self.questionGp = 'Point Group:'    
                    if self.axisselected_name != None:
                        self.questionAxis = 'Where is the special axis?' 
                    return
                
                if self.pointgroupselected_name == '2/m':
                    self.questionAxis = 'Where is the special axis?' 
                    self.message='This point group does not have priezoelectricity'
                    return

                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(False)   
                    self.sucess = 1
                    return
                else:

                    self.questionAxis = 'Where is the special axis?' 
                    self.questionGp = 'Point Group:'     
                    self.setCoefficientsforjQuery(self.type );
                    self.setCatalogPropertyDetail()
                    self.createJQueryCode(False)

                
            if self.crystalsystem_name == 'o':
                self.questionGp = 'Point Group?'     
                if  self.pointgroupselected_name ==  None or self.pointgroupselected_name == '' or self.pointgroupselected_name not  in '222, 2mm, mmm' :  
                    return
           
                if self.pointgroupselected_name == 'mmm':
                    self.message ='This point group does not have priezoelectricity'
                    return

                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(False)     
                    self.sucess = 1
                    return
                else:
                    self.setCoefficientsforjQuery(self.type );
                    self.setCatalogPropertyDetail()
                    self.createJQueryCode(False)
     
 
            
            if self.crystalsystem_name == 'te':
                self.questionGp = 'Point Group:' 
                if  self.pointgroupselected_name == None or self.pointgroupselected_name == '' or self.pointgroupselected_name not in '4, -4, 4/m, 422, 4mm, -42m, 4/mmm':
                    return
               
                if self.pointgroupselected_name in ('4/m', '4/mmm'):
                    self.message ='This point group does not have priezoelectricity'
                    return

                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(False)
                    self.sucess = 1
                    return
                else:
                    self.setCoefficientsforjQuery(self.type );
                    self.setCatalogPropertyDetail() 
                    self.createJQueryCode(False)
                    
            
            
            
            if self.crystalsystem_name == 'c':
                self.questionGp = 'Point Group:'     
                if  self.pointgroupselected_name == None or self.pointgroupselected_name == ''  or self.pointgroupselected_name not in '23, m3, 432, -43m, m3m':
                    return
               
                if self.pointgroupselected_name in ('m3', '432', 'm3m'):
                    self.message ='This point group does not have priezoelectricity'  
                    return

                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(False)     
                    self.sucess = 1
                    return
                else:
                    self.setCoefficientsforjQuery(self.type );
                    self.setCatalogPropertyDetail() 
                    self.createJQueryCode(False)
 
                
            elif self.crystalsystem_name == 'tg':
                self.questionGp = 'Point Group:'       
                if  self.pointgroupselected_name == None or self.pointgroupselected_name == '' or self.pointgroupselected_name not in '3, -3, 32, 3m, -3m':
                    return
               
                if self.pointgroupselected_name in ('-3', '-3m'):
                    self.message ='This point group does not have priezoelectricity'      
                    return
                self.questionAxis = 'Where is the special axis?' 
                if self.pointgroupselected_name == '3m':
                    if self.axisselected_name == None or self.axisselected_name == '' or self.axisselected_name not in 'x1, x2':
                        return 
                    
                    

                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(False)    
                    self.sucess = 1
                    return
                else:
                    self.setCoefficientsforjQuery(self.type );
                    self.setCatalogPropertyDetail() 
                    self.createJQueryCode(False)

            elif self.crystalsystem_name == 'h':
                self.questionGp = 'Point Group:'   
                if  self.pointgroupselected_name == None or self.pointgroupselected_name == '' or self.pointgroupselected_name not in '6, -6, 6/m, 6mm, 622, -6m2, 6/mmm' :
                    return    

                if self.pointgroupselected_name  in ('6/m', '6/mmm'):
                    self.message ='This point group does not have priezoelectricity' 
                    return
                
                if self.pointgroupselected_name == '-6m2':
                    self.questionAxis = 'Where is the special axis?' 
                    if  self.axisselected_name == None or self.axisselected_name == '' or self.axisselected_name not in 'x1, x2':
                        return 

                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(False)      
                    self.sucess = 1
                    return
                else:
                    self.setCoefficientsforjQuery(self.type );
                    self.setCatalogPropertyDetail() 
                    self.createJQueryCode(False)
                    
                    
                    
        #*******************************Second Rank Tensor*****************************************  
        if self.catalogproperty_name == '2nd':   
            self.questionGp = 'Point Group:'      
            if self.crystalsystem_name == 'tc': 
                if  self.pointgroupselected_name == None or  self.pointgroupselected_name == '' or self.pointgroupselected_name not in '1, -1 -1*' :
                    return

                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(True)     
                    self.sucess = 1
                    return
                else:
                    self.message= 'All the point groups of this crystal system have the same matrix' 
                    self.setCoefficientsforjQuery(self.type );
                    self.setCatalogPropertyDetail() 
                    self.createJQueryCode(True)

            if self.crystalsystem_name == 'm': 
                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                        self.setCoefficentsValues(True)   
                        self.sucess = 1
                        return
                    
                else:
                    self.questionGp = 'Point Group:'   
                    self.message= 'All the point groups of this crystal system have the same matrix'
                    if self.pointgroupselected_name == None or self.pointgroupselected_name == '' or self.pointgroupselected_name not in self.pointGroupListNames:#self.pointgroupselected_name not in ['2', '2m', '2/m'] :  
                        return   
 
                      
                    self.setCoefficientsforjQuery(self.type);
                    self.setCatalogPropertyDetail() 
                    self.createJQueryCode(True)
                    
            if self.crystalsystem_name == 'o': 
                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                        self.setCoefficentsValues(True)
                        self.sucess = 1
                        return
                    
                else:
                    self.questionGp = 'Point Group:'     
                    self.message= 'All the point groups of this crystal system have the same matrix'
                    if  self.pointgroupselected_name == None or self.pointgroupselected_name == '' or self.pointgroupselected_name not in  self.pointGroupListNames: #self.pointgroupselected_name not in '222, 2mm, mmm' :   
                        return  
 
                    self.setCoefficientsforjQuery(self.type);
                    self.setCatalogPropertyDetail() 
                    self.createJQueryCode(True)
 
            if self.crystalsystem_name == 'u':
                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(True)    
                    self.sucess = 1
                    return
                else:
                    self.questionGp = 'Point Group:'     
                    self.message= 'All the point groups of this crystal system have the same matrix for Trigonal, Tetragonal and Hexagonal'
                    if  self.pointgroupselected_name ==  None or self.pointgroupselected_name == '' or self.pointgroupselected_name not in self.pointGroupListNames: 
                        return  

                    self.setCoefficientsforjQuery(self.type);
                    self.setCatalogPropertyDetail() 
                    self.createJQueryCode(True)
                         
                    
            if self.crystalsystem_name == 'c':    
                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(True)    
                    self.sucess = 1
                    return
                     
                else:
                    self.questionGp = 'Point Group:'   
                    self.message= 'All the point groups of this crystal system have the same matrix'
                    if  self.pointgroupselected_name == None or self.pointgroupselected_name == '' or self.pointgroupselected_name not in self.pointGroupListNames:#self.pointgroupselected_name not in '23, m3, 432, -43m, m3m, infinf, infinfm' :    
                        return  

                    self.setCoefficientsforjQuery(self.type);
                    self.setCatalogPropertyDetail() 
                    self.createJQueryCode(True)
                    
                        
            if self.crystalsystem_name == 'te':     
                if  self.formargsvalitated != None and len(self.__inputList) > 0:
                    self.setCoefficentsValues(True)    
                    self.sucess = 1
                    return
                else:
                    self.questionGp = 'Point Group:'  
                    if  self.pointgroupselected_name == None or self.pointgroupselected_name == '' or self.pointgroupselected_name not in self.pointGroupListNames:#self.pointgroupselected_name not in '23, m3, 432, -43m, m3m, infinf, infinfm' :
                        return  

                    self.setCoefficientsforjQuery(self.type);
                    self.setCatalogPropertyDetail() 
                    self.setCoefficentsValues(True)
                    self.createJQueryCode(True)
                    
                         
    #start setCatalogPropertyDetail
    def setCatalogPropertyDetail(self):
        if self.catalogproperty_name == 'e' or self.catalogproperty_name == 'p' or self.catalogproperty_name == '2nd':
            self.propertyDetail = CatalogPropertyDetail.objects.filter(  dataproperty  = self.objDataProperty,
                                                                                                                        crystalsystem =self.objCatalogCrystalSystemSelected,
                                                                                                                        type =self.objTypeSelected,
                                                                                                                        catalogpointgroup =self.objCatalogPointGroupSelected,
                                                                                                                         pointgroupnames =self.objPointGroupNamesSelected,
                                                                                                                        catalogaxis=self.objAxisSelected).order_by('name')

 
             
            print self.propertyDetail.query                                                                                                  
            for obj in self.propertyDetail:
                cpd=CatalogPropertyDetail()
                cpd = obj
                self.read_write_inputs[cpd.name] = 'w'
                self.catalogPropertyDetail.append(cpd) 
                del cpd   
        
    #end setCatalogPropertyDetail    
        
                
                
    def setPointGroup(self):  
        propertyDetail = CatalogPropertyDetail.objects.filter(type=self.objTypeSelected,crystalsystem=self.objCatalogCrystalSystemSelected).values('catalogpointgroup').annotate(total=Count('catalogpointgroup'))
       
        for d in propertyDetail:  
            if d['catalogpointgroup'] != 45:       
                #print d['catalogpointgroup']  
                objCatalogPointGroup=CatalogPointGroup.objects.filter(id__exact=d['catalogpointgroup'])         
                for obj in  objCatalogPointGroup:
                    cpg=CatalogPointGroup()
                    cpg=obj        
                    
                    if self.pointgroupselected_name == None or self.pointgroupselected_name == '' or self.pointgroupselected_name == None:
                        self.pointgroupselected_name=cpg.name
                        self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(name__exact=self.pointgroupselected_name) 
                    elif self.pointgroupselected_name != '' or self.pointgroupselected_name != None:  
                        if self.pointgroupselected_name == cpg.name:
                            self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(name__exact=self.pointgroupselected_name) 
                        
               
                    self.pointGroupList.append(cpg)
                    
        if not self.pointGroupList:
            self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(id=45)
        else:
            if self.objCatalogPointGroupSelected == None:
                self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(name__exact=self.pointGroupList[0])         
      
                
        
        
        propertyDetail = CatalogPropertyDetail.objects.filter(type=self.objTypeSelected,crystalsystem=self.objCatalogCrystalSystemSelected).values('pointgroupnames').annotate(total=Count('pointgroupnames'))
        for d in propertyDetail:
            if d['pointgroupnames'] != 21:   
                objPointgroupNames=PointGroupNames.objects.get(id__exact=d['pointgroupnames']) 
                objPointGroupGroups = PointGroupGroups.objects.filter(pointgroupnames=objPointgroupNames)    

                for i,obj in enumerate(objPointGroupGroups):
                    if self.pointgroupselected_name == '':
                        self.pointgroupselected_name=objPointGroupGroups[i].catalogpointgroup.name
                    
                    if objPointGroupGroups[i].catalogpointgroup.name == self.pointgroupselected_name:
                        self.objPointGroupNamesSelected = objPointGroupGroups[i].pointgroupnames
             
                    self.pointGroupList.append(objPointGroupGroups[i].catalogpointgroup)
                    
                    
                if self.objPointGroupNamesSelected ==None:
                    self.objPointGroupNamesSelected = objPointgroupNames
            else:
                self.objPointGroupNamesSelected = PointGroupNames.objects.get(id=21) 
             
        #print str(len(propertyDetail))
        if len(propertyDetail) ==  0:
            self.objPointGroupNamesSelected = PointGroupNames.objects.get(id=21) 
 
        
            
            #self.objPointGroupNamesSelected.append(self.objCatalogPointGroupSelected.id)
                
                
             
                    
    def setAxis(self):
        propertyDetail = CatalogPropertyDetail.objects.filter(type=self.objTypeSelected,
                                                                                                            crystalsystem=self.objCatalogCrystalSystemSelected,
                                                                                                            catalogpointgroup=self.objCatalogPointGroupSelected,
                                                                                                            pointgroupnames=self.objPointGroupNamesSelected,
                                                                                                            dataproperty=self.objDataProperty).values('catalogaxis').annotate(total=Count('catalogaxis')).order_by('catalogaxis')
         
        for d in propertyDetail:  
            if d['catalogaxis'] != 4:       
                #print d['catalogaxis']  
                objCatalogAxis=CatalogAxis.objects.filter(id=d['catalogaxis'] )
                for obj in objCatalogAxis:
                    ca=CatalogAxis()
                    ca=obj
                    #print ca.name
                    if self.axisselected_name =='':
                        self.axisselected_name = ca.name
                    
                    self.axisList.append(ca)
                    
                if self.axisselected_name ==None:
                        self.axisselected_name = ca.name
                    
        if self.axisList:
            self.questionAxis = 'Where is the special axis?' 
        else:
            self.objAxisSelected = CatalogAxis.objects.get(id=4)
   
                        
        
    def preparedataforjQuery(self,t):
        if t == "s" or t == "c":
            x = 0
            row = []
            for r in self.s:
                x=x+ 1
                y=1   
                for c in r: 
                    col=t+str(x) + str(y)
                    if col in self.read_write_inputs:
                        pass
                    else: 
                        self.read_write_inputs[col] = "r"  
                    row.append(col)
                    y= y + 1 
                self.catalogPropertyDetailReadOnly.append(row)     
                row = []  
        elif t == "d":
            x = 0
            row = []
            for r in self.d:
                x=x+ 1
                y=1   
                for c in r: 
                    col=t+str(x) + str(y)
                    if col in self.read_write_inputs:
                        pass
                    else: 
                        self.read_write_inputs[col] = "r"  
                    row.append(col)
                    y= y + 1 
                self.catalogPropertyDetailReadOnly.append(row)     
                row = []  
        elif t == "k":
            """
            x = 0
            row = []
            for r in self.k:
                x=x+ 1
                y=1   
                for c in r: 
                    col=t+str(x) + str(y)
                    if col in self.read_write_inputs:
                        pass
                    else: 
                        self.read_write_inputs[col] = "r"  
                    row.append(col)
                    y= y + 1 
                self.catalogPropertyDetailReadOnly.append(row)     
                row = []  
                """
    def setCoefficientsforjQuery(self,t):            
  
        #catalogPropertyDetail=CatalogPropertyDetail.objects.filter(type=self.objTypeSelected,crystalsystem=self.objCatalogCrystalSystemSelected,dataproperty=self.objDataProperty,catalogaxis=self.objAxisSelected)
        catalogPropertyDetail = CatalogPropertyDetail.objects.filter(  dataproperty  = self.objDataProperty,
                                                                                                                        crystalsystem =self.objCatalogCrystalSystemSelected,
                                                                                                                        type =self.objTypeSelected,
                                                                                                                        catalogpointgroup =self.objCatalogPointGroupSelected,
                                                                                                                         pointgroupnames=self.objPointGroupNamesSelected,
                                                                                                                        catalogaxis=self.objAxisSelected).order_by('name')
                                                                                                               
                                                                                                        
        read_write_inputs_temp =  {}
        for cpd in catalogPropertyDetail:
            catalogPropertyDetailObj = CatalogPropertyDetail()
            catalogPropertyDetailObj =  cpd
            read_write_inputs_temp[catalogPropertyDetailObj.name] = "w"  
            del catalogPropertyDetailObj
        
        datapropertyinitial=self.objDataProperty
        dimensions=datapropertyinitial.tensor_dimensions.split(',')
        #print str(len(dimensions))
        
        if len(dimensions) == 2:
            coefficients = N.zeros([int(dimensions[0]),int(dimensions[1])])    
            #print datapropertyinitial.tag
            parts=datapropertyinitial.tag.split('_')[-1]
            self.scij =parts.split('ij')
            x = 0
            row = []
            for r in coefficients:
                x=x+ 1
                y=1   
                for c in r: 
                    col= str(x) + str(y)                

                    if catalogPropertyDetail:
                        if (self.scij[0] +col + self.scij[1]) not in read_write_inputs_temp:
                            self.read_write_inputs[self.scij[0] +col + self.scij[1]] =   "r"  
                            
                        else:
                            #self.coefficientsparts.append(self.scij[0] +col + self.scij[1] )  
                            pass
                    else:
                        self.read_write_inputs[self.scij[0] +col + self.scij[1]] =   "w"  
                        #self.coefficientsparts.append(self.scij[0] +col + self.scij[1] ) 
                         
                        
        
                    row.append(self.scij[0] +col + self.scij[1] )
                    y= y + 1 
                self.catalogPropertyDetailReadOnly.append(row)     
                row = [] 
                    
 
    def setDimension(self,objDataProperty):
        dimensions=self.objDataProperty.tensor_dimensions.split(',')
        if len(dimensions) == 2:
            #self.coefficientsmatrix = N.zeros([int(dimensions[0]),int(dimensions[1])])  
            self.coefficientsmatrix1 = N.chararray([int(dimensions[0]),int(dimensions[1])])  
            self.coefficientsmatrix1[:] = ''
            
            self.coefficientsmatrix = [["" for x in range(int(dimensions[1]))] for y in range(int(dimensions[0]))] 

            self.tag=self.objDataProperty.tag.split('_')[-1]
            self.scij =self.tag.split('ij')
            
            
        elif len (dimensions) == 1:
            if  dimensions[0] == '2':
                self.scij  = []
                items = self.objDataProperty.tag.split('_')
                f=items[len(items) - 2].split(',')
                self.scij.append( f[0] )
                self.scij.append(items[len(items)-1 ])
                #print self.scij 
                
                self.coefficientsmatrix = N.zeros([int(dimensions[0])])  
                
            elif  dimensions[0] == '0':
                pass
            
            
    def setCoefficentsValues(self,symmetry):
        #dim= self.coefficientsmatrix[0]
        dimensions=self.objDataProperty.tensor_dimensions.split(',')

        self.symmetry  = symmetry
        if  self.formargsvalitated != None and len(self.__inputList) > 0:
            for i in range(0,int(dimensions[0])):
                for j  in range(0,int(dimensions[1])):    
                    tagindex = str(i +1 )  + str(j + 1)
                    tag = self.tag.replace('ij',tagindex);

                    try:
                        value1 = self.formargsvalitated[0][tag]
                        value2 = self.formdata[0][tag]
                        if self.symmetry:
                            if self.coefficientsmatrix[i][j] == '':
                                self.coefficientsmatrix[i][j] = value2
                                self.coefficientsmatrix[j][i] = value2
                                self.coefficientsmatrix1[i,j] = value2
                                self.coefficientsmatrix1[j,i] = value2
                        else:
                            self.coefficientsmatrix[i][j] = value2
                            
                            
                    except  Exception as e:
                        print " Error: {1}".format( e.message, e.args) 
                        self.message = " Error: {1}".format( e.message, e.args) 
                        self.sucess = 0
                        return 
                              
                        
                
        

    def getIndex(self,coefficientsTag):              
        match = re.match(r"([a-z]+)([0-9]+)",  coefficientsTag, re.I)
        if match:
            items = match.groups()
            numbers = items[1]
            index = re.findall(r'.{1,1}',numbers,re.DOTALL)
            indextem=[]
            indextem.append(int(index[0]) - 1)
            indextem.append( int(index[1]) - 1)
            return indextem
        
          
    def contains(self,listObject, obj):
        result = False
        for x in listObject:
            #print x.catalogproperty_name + " == " + obj.catalogproperty_name
            if x == obj :         
                result = True
                break       

        return result
            

    """def releaseRequet(self):
        self.__request =None
    """
        
        
    def __del__(self):
        print "delete object"
        
        
        
        
        #start setCatalogPropertyDetailkeyNotation
    def setCatalogPropertyDetailkeyNotation(self):
        if self.catalogproperty_name == 'e' or self.catalogproperty_name == 'p' or self.catalogproperty_name == '2nd':
            propertyDetail = CatalogPropertyDetail.objects.filter(  dataproperty  = self.objDataProperty,
                                                                                                                crystalsystem =self.objCatalogCrystalSystemSelected,
                                                                                                                type =self.objTypeSelected,
                                                                                                                catalogpointgroup =self.objCatalogPointGroupSelected,
                                                                                                                 pointgroupnames =self.objPointGroupNamesSelected,
                                                                                                                catalogaxis=self.objAxisSelected).order_by('name')

 
 
 
            #print self.objDataProperty.tag
            kNotation = None
         
 
            if self.catalogproperty_name == 'e':
                targetList = []
                sourceList = []
                targetListstr = ''
                sourceListstr = ''
                for i, obj in enumerate(propertyDetail):    
                    item = obj.name
                    #print 'source ' + item
                    keyNotationCatalogPropertyDetail = None
                    
                
                    if self.objCatalogCrystalSystemSelected.name == "iso" or   self.objCatalogCrystalSystemSelected.name == "h" or self.objCatalogCrystalSystemSelected.name == "tg":
  
                        if self.objCatalogCrystalSystemSelected.name == "iso":
                            
                            
                            if item == self.scij[0]+ '11' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=3)
                                targetList =[self.scij[0]+ '22' +self.scij[1], self.scij[0] + '33' + self.scij[1]] 
                                sourceList.append(obj)
                                sourceListstr = sourceListstr + item
                                targetListstr = self.scij[0]+ '22' +self.scij[1] +', ' + self.scij[0] + '33' + self.scij[1]
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                                
                                
                            elif item == self.scij[0]+ '12' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=3)
                                targetList =[self.scij[0]+ '13' +self.scij[1], self.scij[0] + '23'  + self.scij[1]] 
                                sourceList.append(obj)
                                targetListstr = self.scij[0]+ '13' +self.scij[1]+ ', ' +self.scij[0] + '23'  + self.scij[1]
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
 
                           
                                
                                
                                if len(sourceList) == 2:
                                    if 'c' in self.scij[0]:   
                                        #print "stiffness"
                                        if len(sourceList) == 2:
                                            kNotation= KeyNotation.objects.get(id=8)
                                            
                                   
            
                                    elif 's' in self.scij[0]:
                                        #print "compliance"    
                                        if len(sourceList) == 2:                        
                                            kNotation=KeyNotation.objects.get(id=7)
                                            
                                            
                                    targetList =[self.scij[0]+ '44' +self.scij[1], self.scij[0] + '55' +self.scij[1], self.scij[0] + '66' +self.scij[1]] 
                                    targetListstr = self.scij[0]+ '44' +self.scij[1] + ', '+ self.scij[0] + '55' +self.scij[1]+ ', '+  self.scij[0] + '66' +self.scij[1]
                                    
                                  
                                    
                                    sourceListstr = sourceListstr + ', '  + item                                    

                                    for source in sourceList:
                                        keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(source,kNotation)
                                        keyNotationCatalogPropertyDetail.source =sourceListstr
                                        keyNotationCatalogPropertyDetail.target = targetListstr
                                        keyNotationCatalogPropertyDetail.save()

                                    sourceList = []
                                    targetListstr = ''
                                    sourceListstr = ''
                                    
 
                          
                              
                           

                        if self.objCatalogCrystalSystemSelected.name == "h" or self.objCatalogCrystalSystemSelected.name == "tg":
                            
                            if item == self.scij[0]+ '11' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=3)
                                targetList =[self.scij[0]+ '22' +self.scij[1]] 
                                sourceList.append(obj)
                                sourceListstr = sourceListstr + item
                                targetListstr =   self.scij[0]+ '22' +self.scij[1]
   
                                
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                            
                     
                                
                                
                            elif item == self.scij[0]+ '12' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=2)
                                sourceList.append(obj)   
 
                                 
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = item
                                keyNotationCatalogPropertyDetail.save()
              
                                
                                if len(sourceList) == 2:
                                    if 'c' in self.scij[0]:   
                                        #print "stiffness"
                                        if len(sourceList) == 2:
                                            kNotation= KeyNotation.objects.get(id=8)
                                            
                                   
            
                                    elif 's' in self.scij[0]:
                                        #print "compliance"    
                                        if len(sourceList) == 2:                        
                                            kNotation=KeyNotation.objects.get(id=7)
                                            
                                            
                                            
                                    targetList =[self.scij[0]+ '66' +self.scij[1]]
                                    targetListstr = self.scij[0]+ '66' +self.scij[1]
                                    
                                    sourceListstr = sourceListstr + ', '  + item
 
                                    
                                    for source in sourceList:
                                        keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(source,kNotation)
                                        keyNotationCatalogPropertyDetail.source =sourceListstr
                                        keyNotationCatalogPropertyDetail.target = targetListstr
                                        keyNotationCatalogPropertyDetail.save()

                                    sourceList = []
                                    targetListstr = ''
                                    sourceListstr = ''
                                 


                                
                            elif item == self.scij[0]+ '13' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=3)
                                targetList =[self.scij[0]+ '23' +self.scij[1] ] 
                                targetListstr = self.scij[0]+ '23' +self.scij[1]
 
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
 
                                
                            elif item== self.scij[0]+ '14' +self.scij[1]:
                                if 'c' in self.scij[0]:   
                                    kNotation=KeyNotation.objects.get(id=6)
                                else:    
                                    kNotation=KeyNotation.objects.get(id=5)
                                    
                                targetList =[self.scij[0]+ '24' +self.scij[1],self.scij[0]+ '56' +self.scij[1]  ]   
                                targetListstr = self.scij[0]+ '24' +self.scij[1] + ', ' +self.scij[0]+ '56' +self.scij[1] 
        
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
   
                                
                                    
                            elif item== self.scij[0]+ '25' +self.scij[1]:
                                if self.pointgroupselected_name in ('3', '-3'):
                                    if 'c' in self.scij[0]:   
                                        kNotation=KeyNotation.objects.get(id=6) 
                                    else:    
                                        kNotation=KeyNotation.objects.get(id=5)
                                        
                                    targetList =[self.scij[0]+ '15' +self.scij[1], self.scij[0]+ '46' +self.scij[1]  ] 
                                    targetListstr = self.scij[0]+ '15' +self.scij[1] +', ' +self.scij[0]+ '46' +self.scij[1] 
                                    
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = targetListstr
                                    keyNotationCatalogPropertyDetail.save()
 
                                
                            elif item == self.scij[0]+ '44' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=3)
                                targetList =[self.scij[0]+ '55' +self.scij[1] ] 
                                targetListstr = self.scij[0]+ '55' +self.scij[1]
                      
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
 
                            else:
                                kNotation=KeyNotation.objects.get(id=2)
                                 
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = item
                                keyNotationCatalogPropertyDetail.save()


                        
                    elif  self.objCatalogCrystalSystemSelected.name == "tc" or self.objCatalogCrystalSystemSelected.name == "m" or self.objCatalogCrystalSystemSelected.name == "o"  :
                        kNotation=KeyNotation.objects.get(id=2)
 
                        keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                        keyNotationCatalogPropertyDetail.source =item
                        keyNotationCatalogPropertyDetail.target = item
                        keyNotationCatalogPropertyDetail.save()
           

                        
                    elif  self.objCatalogCrystalSystemSelected.name == "c":
                        kNotation=KeyNotation.objects.get(id=2)
                        targetListstr = ""
                        if i==0:
                            targetList =[self.scij[0]+ '22' +self.scij[1], self.scij[0] + '33'  + self.scij[1]] 
                            targetListstr = self.scij[0]+ '22' +self.scij[1] +', ' + self.scij[0] + '33'   + self.scij[1]
                        if i==1:
                            targetList =[self.scij[0]+ '13' +self.scij[1], self.scij[0] + '23'  + self.scij[1]]
                            targetListstr = self.scij[0]+ '13' +self.scij[1]  +', ' +  self.scij[0] + '23'   + self.scij[1]
                        if i==2:
                            targetList =[self.scij[0]+ '55' +self.scij[1], self.scij[0] + '66'  + self.scij[1] ] 
                            targetListstr = self.scij[0]+ '55' +self.scij[1]  +', ' +  self.scij[0] + '66'   + self.scij[1]
 
                        
                        keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                        keyNotationCatalogPropertyDetail.source =item
                        keyNotationCatalogPropertyDetail.target = targetListstr
                        keyNotationCatalogPropertyDetail.save()
                        

 
                    
                    elif  self.objCatalogCrystalSystemSelected.name == "te" :
                        kNotation=KeyNotation.objects.get(id=3)
                        if item== self.scij[0]+ '11' +self.scij[1]:
                            targetList =[self.scij[0]+ '22' +self.scij[1]] 
                            targetListstr = self.scij[0]+ '22' +self.scij[1]
                          
                            keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                            keyNotationCatalogPropertyDetail.source =item
                            keyNotationCatalogPropertyDetail.target = targetListstr
                            keyNotationCatalogPropertyDetail.save()
                            
                             
                            
                        elif item== self.scij[0]+ '13' +self.scij[1]:
                            targetList =[self.scij[0]+ '23' +self.scij[1]] 
                            targetListstr = self.scij[0]+ '23' +self.scij[1]
                          
                            keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                            keyNotationCatalogPropertyDetail.source =item
                            keyNotationCatalogPropertyDetail.target = targetListstr
                            keyNotationCatalogPropertyDetail.save()
                             
                             
                            
                        elif item== self.scij[0]+ '44' +self.scij[1]:
                            targetList =[self.scij[0]+ '55' +self.scij[1]] 
                            targetListstr = self.scij[0]+ '55' +self.scij[1]
                            
                            keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                            keyNotationCatalogPropertyDetail.source =item
                            keyNotationCatalogPropertyDetail.target = targetListstr
                            keyNotationCatalogPropertyDetail.save()
                        
                            
                        elif item== self.scij[0]+ '16' +self.scij[1]:
                            if self.pointgroupselected_name in ('4', '-4', '4/m'):
                                kNotation=KeyNotation.objects.get(id=4)
                                targetList =[self.scij[0]+ '26' +self.scij[1]] 
                                targetListstr = self.scij[0]+ '26' +self.scij[1]
                               
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                            
                        else:   
                            kNotation=KeyNotation.objects.get(id=2)
                
                            keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                            keyNotationCatalogPropertyDetail.source =item
                            keyNotationCatalogPropertyDetail.target = item
                            keyNotationCatalogPropertyDetail.save()
              
                print ' \n'     
        
        
        
            if self.catalogproperty_name == 'p':
                targetList = []
                sourceList = []
                targetListstr = ''
                sourceListstr = ''
                for i, obj in enumerate(propertyDetail):  
                    item = obj.name  
                    if  self.objCatalogCrystalSystemSelected.name == "tc" or self.objCatalogCrystalSystemSelected.name == "m" or self.objCatalogCrystalSystemSelected.name == "o":
                        keyNotationCatalogPropertyDetail = None        
                        kNotation=KeyNotation.objects.get(id=2)
                    
                        keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                        keyNotationCatalogPropertyDetail.source =item
                        keyNotationCatalogPropertyDetail.target = item
                        keyNotationCatalogPropertyDetail.save()
                        
                    elif self.objCatalogCrystalSystemSelected.name == "c":
                        kNotation=KeyNotation.objects.get(id=3)
                        if item== self.scij[0]+ '14' +self.scij[1]:
                            targetListstr = self.scij[0]+ '25' +self.scij[1] +', ' + self.scij[0] + '36'   + self.scij[1]
                        
                            keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                            keyNotationCatalogPropertyDetail.source =item
                            keyNotationCatalogPropertyDetail.target = targetListstr
                            keyNotationCatalogPropertyDetail.save()
                    elif self.objCatalogCrystalSystemSelected.name == "te":
                        if self.pointgroupselected_name == '4':
                            if item== self.scij[0]+ '14' +self.scij[1]:
                                kNotation=KeyNotation.objects.get(id=4)
                                targetListstr = self.scij[0]+ '25' +self.scij[1]
                   
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                                
                            elif item== self.scij[0]+ '15' +self.scij[1]:
                                kNotation=KeyNotation.objects.get(id=3)
                                targetListstr = self.scij[0]+ '24' +self.scij[1]
        
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                                
                            elif item== self.scij[0]+ '31' +self.scij[1]:
                                kNotation=KeyNotation.objects.get(id=3)
                                targetListstr = self.scij[0]+ '32' +self.scij[1]
                        

                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                            else:
                                kNotation=KeyNotation.objects.get(id=2)
 
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = item
                                keyNotationCatalogPropertyDetail.save()
                        elif  self.pointgroupselected_name == '-4':      
                            if item== self.scij[0]+ '14' +self.scij[1]:
                                kNotation=KeyNotation.objects.get(id=3)
                                targetListstr = self.scij[0]+ '25' +self.scij[1]
 
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                                
                            elif item== self.scij[0]+ '15' +self.scij[1]:
                                kNotation=KeyNotation.objects.get(id=4)
                                targetListstr = self.scij[0]+ '24' +self.scij[1]
                          
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                                
                            elif item== self.scij[0]+ '31' +self.scij[1]:
                                kNotation=KeyNotation.objects.get(id=3)
                                targetListstr = self.scij[0]+ '32' +self.scij[1]
                         

                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                            else:
                                kNotation=KeyNotation.objects.get(id=2)
                                 
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = item
                                keyNotationCatalogPropertyDetail.save() 
                            
                        elif  self.pointgroupselected_name == '422':     
                            if item== self.scij[0]+ '14' +self.scij[1]:
                                kNotation=KeyNotation.objects.get(id=4)
                                targetListstr = self.scij[0]+ '25' +self.scij[1]
                 
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                            
                        elif  self.pointgroupselected_name == '4mm':   
                            if item== self.scij[0]+ '15' +self.scij[1]:
                                kNotation=KeyNotation.objects.get(id=3)
                                targetListstr = self.scij[0]+ '24' +self.scij[1]
                             
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()   
                                
                            elif item== self.scij[0]+ '31' +self.scij[1]:
                                kNotation=KeyNotation.objects.get(id=3)
                                targetListstr = self.scij[0]+ '32' +self.scij[1]
                         
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()  
                            else:
                                kNotation=KeyNotation.objects.get(id=2)
                       
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = item
                                keyNotationCatalogPropertyDetail.save() 
                                 
                            
                        elif  self.pointgroupselected_name == '-42m': 
                            if item== self.scij[0]+ '14' +self.scij[1]:
                                kNotation=KeyNotation.objects.get(id=3)
                                targetListstr = self.scij[0]+ '25' +self.scij[1]
                                
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()   
                            else:
                                kNotation=KeyNotation.objects.get(id=2)
   
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = item
                                keyNotationCatalogPropertyDetail.save() 
                            
                    elif self.objCatalogCrystalSystemSelected.name == "tg":
                        if  self.pointgroupselected_name == '3': 
                            if item == self.scij[0]+ '11' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=10)
                                   
                                targetListstr = self.scij[0]+ '12' +self.scij[1] + ', '  + self.scij[0]+ '26' +self.scij[1]                  
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()

                            elif item == self.scij[0]+ '14' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=4)
                       
                                targetListstr = self.scij[0]+ '25' +self.scij[1]                  
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()

                            elif item == self.scij[0]+ '15' +self.scij[1] :   
                                kNotation=KeyNotation.objects.get(id=3)
                                    
                                targetListstr = self.scij[0]+ '24' +self.scij[1]                  
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                                
                            elif item == self.scij[0]+ '22' +self.scij[1] : 
                                kNotation=KeyNotation.objects.get(id=10)
             
                                targetListstr = self.scij[0]+ '21' +self.scij[1] + ', '  + self.scij[0]+ '16' +self.scij[1]                  
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                                
                            elif item == self.scij[0]+ '31' +self.scij[1] : 
                                kNotation=KeyNotation.objects.get(id=3)
                    
                                targetListstr = self.scij[0]+ '32' +self.scij[1]                  
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                                
                            else:
                                kNotation=KeyNotation.objects.get(id=2)
                           
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = item
                                keyNotationCatalogPropertyDetail.save()
    
                        elif  self.pointgroupselected_name == '32':      
                            if item == self.scij[0]+ '11' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=10)
                               
                                targetListstr = self.scij[0]+ '12' +self.scij[1] + ', '  + self.scij[0]+ '26' +self.scij[1]                  
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()

                            elif item == self.scij[0]+ '14' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=4)
      
                                targetListstr = self.scij[0]+ '25' +self.scij[1]                  
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
            
                            
                        elif  self.pointgroupselected_name == '3m':          
                            if self.axisselected_name == 'x1': 
                                if item == self.scij[0]+ '14' +self.scij[1] :
                                    kNotation=KeyNotation.objects.get(id=4)
          
                                    targetListstr = self.scij[0]+ '25' +self.scij[1]                  
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = targetListstr
                                    keyNotationCatalogPropertyDetail.save()
                                elif item == self.scij[0]+ '15' +self.scij[1] :
                                    kNotation=KeyNotation.objects.get(id=2)
                       
                                    targetListstr = self.scij[0]+ '24' +self.scij[1]              
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = targetListstr
                                    keyNotationCatalogPropertyDetail.save()
                                    
                                elif item == self.scij[0]+ '22' +self.scij[1] :
                                    kNotation=KeyNotation.objects.get(id=10)
                                            
                                    targetListstr = self.scij[0]+ '21' +self.scij[1] + ', '  + self.scij[0]+ '16' +self.scij[1]                  
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = targetListstr
                                    keyNotationCatalogPropertyDetail.save()
                                    
                                elif item == self.scij[0]+ '31' +self.scij[1] :
                                    kNotation=KeyNotation.objects.get(id=3)
                                          
                                    targetListstr = self.scij[0]+ '32' +self.scij[1]              
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = targetListstr
                                    keyNotationCatalogPropertyDetail.save()
                                else:
                                    kNotation=KeyNotation.objects.get(id=2)
                                      
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = item
                                    keyNotationCatalogPropertyDetail.save()
        
                            elif self.axisselected_name == 'x2':
                                if item == self.scij[0]+ '11' +self.scij[1] :
                                    kNotation=KeyNotation.objects.get(id=10)
           
                                    targetListstr = self.scij[0]+ '12' +self.scij[1] + ', '  + self.scij[0]+ '26' +self.scij[1]                  
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = targetListstr
                                    keyNotationCatalogPropertyDetail.save()
                                elif item == self.scij[0]+ '14' +self.scij[1] :
                                    kNotation=KeyNotation.objects.get(id=4)
                                  
                                    targetListstr = self.scij[0]+ '25' +self.scij[1]                  
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = targetListstr
                                    keyNotationCatalogPropertyDetail.save()
                                elif item == self.scij[0]+ '15' +self.scij[1] :
                                    kNotation=KeyNotation.objects.get(id=3)
                    
                                    targetListstr = self.scij[0]+ '24' +self.scij[1]              
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = targetListstr
                                    keyNotationCatalogPropertyDetail.save()
                                elif item == self.scij[0]+ '31' +self.scij[1] :
                                    kNotation=KeyNotation.objects.get(id=3)
           
                                    targetListstr = self.scij[0]+ '32' +self.scij[1]              
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = targetListstr
                                    keyNotationCatalogPropertyDetail.save()
                                else:
                                    kNotation=KeyNotation.objects.get(id=2)
          
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = item
                                    keyNotationCatalogPropertyDetail.save()
 
                    elif self.objCatalogCrystalSystemSelected.name == "h":
                        if  self.pointgroupselected_name == '6': 
                            if item == self.scij[0]+ '14' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=4)
 
                                targetListstr = self.scij[0]+ '25' +self.scij[1]                  
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                            elif item == self.scij[0]+ '15' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=3)
          
                                targetListstr = self.scij[0]+ '24' +self.scij[1]              
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                            elif item == self.scij[0]+ '31' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=3)
             
                                targetListstr = self.scij[0]+ '32' +self.scij[1]              
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                            else:
                                kNotation=KeyNotation.objects.get(id=2)
                                      
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = item
                                keyNotationCatalogPropertyDetail.save()
   
                        elif self.pointgroupselected_name == '6mm': 
                            if item == self.scij[0]+ '15' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=3)
                                       
                                targetListstr = self.scij[0]+ '24' +self.scij[1]              
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                            elif item == self.scij[0]+ '31' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=3)
                             
                                targetListstr = self.scij[0]+ '32' +self.scij[1]              
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                            else:
                                kNotation=KeyNotation.objects.get(id=2)
                                      
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = item
                                keyNotationCatalogPropertyDetail.save()
                                
                                
                        elif self.pointgroupselected_name == '622': 
                            if item == self.scij[0]+ '14' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=4)
                                           
                                targetListstr = self.scij[0]+ '25' +self.scij[1]                  
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                                    
                        elif self.pointgroupselected_name == '-6': 
                            if item == self.scij[0]+ '11' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=10)
                                              
                                targetListstr = self.scij[0]+ '12' +self.scij[1] + ', '  + self.scij[0]+ '26' +self.scij[1]                  
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                            elif item == self.scij[0]+ '22' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=10)
                                   
                                targetListstr = self.scij[0]+ '21' +self.scij[1] + ', '  + self.scij[0]+ '16' +self.scij[1]                  
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                                
                                
                                
                        elif self.pointgroupselected_name == '-6m2': 
                            if self.axisselected_name == 'x1':
                                if item == self.scij[0]+ '22' +self.scij[1] :
                                    kNotation=KeyNotation.objects.get(id=10)
                                        
                                    targetListstr = self.scij[0]+ '21' +self.scij[1] + ', '  + self.scij[0]+ '16' +self.scij[1]                  
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = targetListstr
                                    keyNotationCatalogPropertyDetail.save()
                            elif self.axisselected_name == 'x2':
                                if item == self.scij[0]+ '11' +self.scij[1] :
                                    kNotation=KeyNotation.objects.get(id=10)
                                     
                                    targetListstr = self.scij[0]+ '12' +self.scij[1] + ', '  + self.scij[0]+ '26' +self.scij[1]                  
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = targetListstr
                                    keyNotationCatalogPropertyDetail.save()
                                    
                                    
                                    
            if self.catalogproperty_name == '2nd':
                targetList = []
                sourceList = []
                targetListstr = ''
                sourceListstr = ''
                for i, obj in enumerate(propertyDetail):  
                    item = obj.name  
                    if self.objCatalogCrystalSystemSelected.name == "tc" or self.objCatalogCrystalSystemSelected.name == "m" or self.objCatalogCrystalSystemSelected.name == "o":
                        if item == self.scij[0]+ '12' +self.scij[1] :
                            kNotation=KeyNotation.objects.get(id=3)
                                           
                            targetListstr = self.scij[0]+ '21' +self.scij[1]              
                            keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                            keyNotationCatalogPropertyDetail.source =item
                            keyNotationCatalogPropertyDetail.target = targetListstr
                            keyNotationCatalogPropertyDetail.save()
                        elif item == self.scij[0]+ '13' +self.scij[1] :
                            kNotation=KeyNotation.objects.get(id=3)
                                           
                            targetListstr = self.scij[0]+ '31' +self.scij[1]              
                            keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                            keyNotationCatalogPropertyDetail.source =item
                            keyNotationCatalogPropertyDetail.target = targetListstr
                            keyNotationCatalogPropertyDetail.save()
                        elif item == self.scij[0]+ '23' +self.scij[1] :
                            kNotation=KeyNotation.objects.get(id=3)
                                           
                            targetListstr = self.scij[0]+ '32' +self.scij[1]              
                            keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                            keyNotationCatalogPropertyDetail.source =item
                            keyNotationCatalogPropertyDetail.target = targetListstr
                            keyNotationCatalogPropertyDetail.save()
                        else:
                            kNotation=KeyNotation.objects.get(id=2)
                                                
                            keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                            keyNotationCatalogPropertyDetail.source =item
                            keyNotationCatalogPropertyDetail.target = item
                            keyNotationCatalogPropertyDetail.save()

                    elif self.objCatalogCrystalSystemSelected.name == "c":
                        if item == self.scij[0]+ '11' +self.scij[1] :
                            kNotation=KeyNotation.objects.get(id=3)
                                           
                            targetListstr = self.scij[0]+ '22' +self.scij[1] + ', '  + self.scij[0]+ '33' +self.scij[1]             
                            keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                            keyNotationCatalogPropertyDetail.source =item
                            keyNotationCatalogPropertyDetail.target = targetListstr
                            keyNotationCatalogPropertyDetail.save()
                    elif  self.objCatalogCrystalSystemSelected.name == "te":
                        if self.pointgroupselected_name in ['-4', '4*/m*', '4*']:
                            if item == self.scij[0]+ '11' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=4)
                                               
                                targetListstr = self.scij[0]+ '22' +self.scij[1]           
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                            elif item == self.scij[0]+ '12' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=3)
                                               
                                targetListstr = self.scij[0]+ '21' +self.scij[1]              
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()

                        elif self.pointgroupselected_name in  ['-42m', '4*22', '4*mm*', '-42*m*', '4*/m*mm*']:     
                            if item == self.scij[0]+ '11' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=4)
                                               
                                targetListstr = self.scij[0]+ '22' +self.scij[1]           
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()                                                                                                                                                                                        
                    elif  self.objCatalogCrystalSystemSelected.name == "u":   
                        if self.magnetoelectricity:
                            listnames=groupNamesSelectedDesciptionToList( self.objPointGroupNamesSelected.description)
                            list2 = []
                            list2=compareList(listnames, ['4', '3', '6', 'inf', '-3*', '-4*', '4/m*', '-6*', '6/m*', 'infm*'])
                            if self.pointgroupselected_name in ['4', '3', '6', 'inf', '-3*', '-4*', '4/m*', '-6*', '6/m*', 'infm*'] and len(list2) == 0:
                                if item == self.scij[0]+ '11' +self.scij[1] :
                                    kNotation=KeyNotation.objects.get(id=3)
                                                   
                                    targetListstr = self.scij[0]+ '22' +self.scij[1]              
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = targetListstr
                                    keyNotationCatalogPropertyDetail.save()
                                elif item == self.scij[0]+ '12' +self.scij[1] :
                                    kNotation=KeyNotation.objects.get(id=4)
                                                   
                                    targetListstr = self.scij[0]+ '21' +self.scij[1]              
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = targetListstr
                                    keyNotationCatalogPropertyDetail.save()
                                else:
                                    kNotation=KeyNotation.objects.get(id=2)
                                                            
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = item
                                    keyNotationCatalogPropertyDetail.save()

                        
                        
                            list2=compareList(listnames, ['422', '32', '622', 'inf2', 'infm*', '3m*', '-3*m*','4m*m*', '4/m*m*m*', '6m*m*', '-6*m*2', '-4*2m*', '6/m*m*m*', 'inf/m*m*'] )        
                            if self.pointgroupselected_name in ['422', '32', '622', 'inf2', 'infm*', '3m*', '-3*m*','4m*m*', '4/m*m*m*', '6m*m*', '-6*m*2', '-4*2m*', '6/m*m*m*', 'inf/m*m*']  and  len(list2) == 0:
                                if item == self.scij[0]+ '11' +self.scij[1] :
                                    kNotation=KeyNotation.objects.get(id=3)
                                                   
                                    targetListstr = self.scij[0]+ '22' +self.scij[1]              
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = targetListstr
                                    keyNotationCatalogPropertyDetail.save()
                                else:
                                    kNotation=KeyNotation.objects.get(id=2)
                                                            
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = item
                                    keyNotationCatalogPropertyDetail.save()
                        
                            list2=compareList(listnames, ['4mm', '3m', '6mm', '32*', '42*2*','4/m*mm', '62*2*', '-6*m2*', '6/m*mm', 'inf2*', 'inf/m*m', '-3*m', '-4*2*m'] )           
                            if self.pointgroupselected_name in ['4mm', '3m', '6mm', '32*', '42*2*','4/m*mm', '62*2*', '-6*m2*', '6/m*mm', 'inf2*', 'inf/m*m', '-3*m', '-4*2*m']  and  len(list2) == 0:
                                if item == self.scij[0]+ '12' +self.scij[1] :
                                    kNotation=KeyNotation.objects.get(id=4)
                                                   
                                    targetListstr = self.scij[0]+ '21' +self.scij[1]              
                                    keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                    keyNotationCatalogPropertyDetail.source =item
                                    keyNotationCatalogPropertyDetail.target = targetListstr
                                    keyNotationCatalogPropertyDetail.save()
                            
                        else:
                            if item == self.scij[0]+ '11' +self.scij[1] :
                                kNotation=KeyNotation.objects.get(id=3)
                                               
                                targetListstr = self.scij[0]+ '22' +self.scij[1]              
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = targetListstr
                                keyNotationCatalogPropertyDetail.save()
                            else:
                                kNotation=KeyNotation.objects.get(id=2)
                                                        
                                keyNotationCatalogPropertyDetail = self.getKeyNotationCatalogPropertyDetail(obj,kNotation)
                                keyNotationCatalogPropertyDetail.source =item
                                keyNotationCatalogPropertyDetail.target = item
                                keyNotationCatalogPropertyDetail.save()
                                
                            
                        
                        


                
    def getsimetric(self,item, scij):
        item1= item.replace(scij[0], '')
        item2=item1.replace(scij[1], '')
        index = list(item2)

        source= (scij[0]+ str(index[1]) + str(index[0]) +scij[1])
        
        return source
    
    def issimetric(self,item,target):
        if target == item:
            return False
        else:
            return True
        
    def getKeyNotationCatalogPropertyDetail(self,catalogpropertydetail,keynotation):
        keyNotationCatalogPropertyDetail = None
        try: 
            keyNotationCatalogPropertyDetail = KeyNotationCatalogPropertyDetail.objects.get(keynotation=keynotation, catalogpropertydetail = catalogpropertydetail)
            #keyNotationCatalogPropertyDetail.keynotation=keynotation
        except ObjectDoesNotExist as error:      
            print "message in the function get_props for debug purposes. Message({0}): {1}".format(99, error.message)   
            print "Not exist"
        
        
        if keyNotationCatalogPropertyDetail == None:
            keyNotationCatalogPropertyDetail = KeyNotationCatalogPropertyDetail()
            keyNotationCatalogPropertyDetail.keynotation=keynotation
            keyNotationCatalogPropertyDetail.catalogpropertydetail=catalogpropertydetail
            
        return keyNotationCatalogPropertyDetail
    
    
    
    def getKeyNotation(self,catalogpropertydetail):
        keyNotationCatalogPropertyDetail = None
        try: 
            keyNotationCatalogPropertyDetail = KeyNotationCatalogPropertyDetail.objects.get(catalogpropertydetail = catalogpropertydetail)
            #keyNotationCatalogPropertyDetail.keynotation=keynotation
        except (ObjectDoesNotExist, MultipleObjectsReturned) as error:      
            print "message in the function get_props for debug purposes. Message({0}): {1}".format(99, error.message)   
            #print "Not exist"
            
            
        if keyNotationCatalogPropertyDetail == None:
            try: 
                keyNotationCatalogPropertyDetail = KeyNotationCatalogPropertyDetail.objects.filter(catalogpropertydetail = catalogpropertydetail)
                #keyNotationCatalogPropertyDetail.keynotation=keynotation
            except ObjectDoesNotExist as error:      
                print "message in the function get_props for debug purposes. Message({0}): {1}".format(99, error.message)   
                #print "Not exist"
            
            
 
            
        return keyNotationCatalogPropertyDetail
    
    
    def createJQueryCode(self,symmetry):
        
        jqueryRules= JQueryRules()
        jqueryRules.generateCode(symmetry, self.propertyDetail, self.read_write_inputs,self.scij,True)
        self.jquery = jqueryRules.jquery
    
         
 
        
        

             
