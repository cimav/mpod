'''
Created on 04/09/2018

@author: admin
'''

import numpy as N
import re
from django.db import models
from data.models import *
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist


class PuntualGroup(object):
    '''
    classdocs
    '''


    def __init__(self, catalogproperty, property_name,dimensions,inputList,dictitems,tenso_props_ids):
        '''
        Constructor
        '''
        self.catalogproperty_name = catalogproperty
        self.coefficientsmatrix = None
        self.__inputList = inputList
        self.objDataProperty = None
        self.objCatalogPointGroupSelected =None            
        self.objProperty  =None
        self.objTypeSelected  =None
        self.objCatalogCrystalSystemSelected  =None
        self.objAxisSelected=None
        self.objPuntualgroupNamesSelected = None
        self.dataproperty = tenso_props_ids
        self.coefficientsmatrix2 = None
        
        
        
        self.setDimension(dimensions)
        self.objProperty = CatalogProperty.objects.get(name__exact=self.catalogproperty_name)
        self.objDataProperty = Property.objects.get(id=int(self.dataproperty))  
        type_ids=TypeDataProperty.objects.filter(dataproperty=self.objDataProperty).values_list('type_id',flat=True)   
        if type_ids: #type_ids estara vacio en fourthranktensor  pues no le he asignado tipo
            self.objTypeSelected = Type.objects.get(id__in=type_ids)   
           
        #tetragonal
        """SELECT * FROM mpod.puntual_group_names
            where id in (SELECT puntualgroupnames_id FROM mpod.catalog_property_detail
                                where puntualgroupnames_id in (SELECT id FROM mpod.puntual_group_names
                                                                where id in (SELECT puntualgroupnames_id FROM mpod.puntual_group_groups
                                                                                where catalogpointgroup_id in (SELECT id FROM mpod.catalog_point_group
                                                                                                                where name ='4')))
                                and type_id = 2
                                and dataproperty_id =8
                                group by puntualgroupnames_id)
        """
        #ortorombica mm2 o 2mm
        """
        SELECT * FROM mpod.puntual_group_names
        where id in (SELECT puntualgroupnames_id FROM mpod.catalog_property_detail
                                where puntualgroupnames_id in (SELECT id FROM mpod.puntual_group_names
                                                where id in (SELECT puntualgroupnames_id FROM mpod.puntual_group_groups
                                                                where catalogpointgroup_id in (SELECT id FROM mpod.catalog_point_group
                                                                                                where name ='2mm')))
                                and type_id = 1
                                and dataproperty_id =10
                                group by puntualgroupnames_id)
        """

                
        for cursor, p in enumerate(self.__inputList):
            """extravalue = None
        
            if p[1].find('(') != -1:
                extravalue = p[1][p[1].find('('):]"""
                
                
            index=self.getIndex(p[0]) 
            i = index[0]
            j= index[1]
            print str(i) + "," + str(j)
            self.coefficientsmatrix2[i][j]  = p[1]
    
        for i in range(int(dimensions[0])):        
            for j in range(int(dimensions[1])):
                if self.coefficientsmatrix2[i][j]  != '0':
                    self.coefficientsmatrix2[j][i]   = self.coefficientsmatrix2[i][j]  

        print (self.coefficientsmatrix)
            
            
    def setDimension(self,dimensions):
        if len(dimensions) == 2:
            self.coefficientsmatrix = N.zeros([int(dimensions[0]),int(dimensions[1])])  
            self.coefficientsmatrix2 =  [[0 for x in range(int(dimensions[0]))] for y in range(int(dimensions[1]))] 
            
            
            
    def getIndex(self,coefficientsTag):              
        match = re.match(r"([0-9]+)",  coefficientsTag, re.I)
        if match:
            items = match.groups()
            numbers = items[0]
            index = re.findall(r'.{1,1}',numbers,re.DOTALL)
            indextem=[]
            indextem.append(int(index[0]) - 1)
            indextem.append( int(index[1]) - 1)
            return indextem
        
    def setCatalogPropertyDetail(self):
        #if self.catalogproperty_name == 'e' or self.catalogproperty_name == 'p' or self.catalogproperty_name == '2nd':
        propertyDetail = CatalogPropertyDetail.objects.filter(  dataproperty  = self.objDataProperty,
                                                                                                            crystalsystem =self.objCatalogCrystalSystemSelected,
                                                                                                            type =self.objTypeSelected,
                                                                                                            catalogpointgroup =self.objCatalogPointGroupSelected,
                                                                                                             puntualgroupnames =self.objPuntualgroupNamesSelected,
                                                                                                            catalogaxis=self.objAxisSelected).order_by('name')