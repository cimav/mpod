'''
Created on 02/06/2018

@author: Jorge Torres
'''

 
from data.models import *
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
import numpy as N
 



def argsToInt(args,field=None,value=None):
    result = None
    if field:
        if args[0].has_key(field):
            try:
                result= int(args[0][field])
            except ValueError:
                result = value
        else:
            pass
    return result

def requestPostToInt(POST,key=None,value=None):
    result = None
    if key:
        if POST.has_key(key):
            try:
                result= int(POST.get(key,False))
            except ValueError:
                result = value
        else:
            pass
    return result

def requestPostToIntList(POST,key=None,value=[]):
    result = value           
    ids = [] 
    if key:
        if POST.has_key(key):
            try:
                list=  POST.getlist(key,False)
                for id in list:
                    ids.append(int(id)) 
        
                result= ids
            except ValueError:
                result = value
        else:
            pass
    return result
       
    

def argsListToIntList(argsList):
    listInt= []
    try: 
        for id in argsList:
            listInt.append(int(id))
    except ValueError:
        pass
      
    return listInt


def getIdsFromQuerySet(queryset):
    listInt = []
    try: 
        for i,t in enumerate(queryset):
                    listInt.append(queryset[i].id )
    except ValueError:
        listInt = None
        
    return listInt

 
def getTableHTMLFromQuerySet(querySet, **kwargs):
    html =  ""
    modelname= ""
    if querySet:
        print querySet.model.__name__.lower()
        modelname =  querySet.model.__name__.lower()
        html = """<table>
                         <thead>"""
         
        html = html + "<tr>"    
              
        fields = None
        if 'fields' in kwargs:
            fields  = kwargs.pop('fields' )
        
        autofields = []  
        autofields.append( 'id') 
        autofields.append( '_state')
         
        for key,value  in querySet[0].__dict__.iteritems():
            if  fields:
                if  key in  fields:
                    html = html + "<th scope='col'>"  
                    s = key[:1].upper() + key[1:]
                    html = html + "<div class='text'><span>" + s +  "</span></div>"
                    html = html + "<div class='clear'></div>"
                    html = html + "</th>"   
            else:
                if  key not in autofields:
                    html = html + "<th scope='col'>"  
                    s = key[:1].upper() + key[1:]
                    html = html + "<div class='text'><span>" + s +  "</span></div>"
                    html = html + "<div class='clear'></div>"
                    html = html + "</th>"   


        html = html + "<th scope='col'>" + "Remove" + "</th>"  
        html = html + "</tr></thead><tbody>"    
        
        for i, pg in enumerate(querySet):
            if (i % 2) == 0:
                classTR = 'row1'
            else:
                classTR = 'row2'
                
            html = html + "<tr class="+ classTR+ ">"  
            for key,value  in querySet[i].__dict__.iteritems():
                if  fields:
                    if  key in  fields:
                        if value:
                            if  len(value.strip()) > 0:
                                html = html + "<td>" + value +  "</td>"
                            else:
                                html = html + "<td>-------------------</td>"
                            
                        else:
                            html = html + "<td>-------------------</td>"
                else:
                    if  key not in  autofields:
                        if value:
                            html = html + "<td>" + value +  "</td>"
                        else:
                            html = html + "<td>-------------------</td>"
                
            
            html = html + "<td><input type='checkbox' name='delete_"  + modelname +  "' id='id_"+ modelname  +str(i)+ "' value='"+str(querySet[i].id) + "' /></td>"             
           
        
        html = html + "</tr>"
        html =  html + """</tbody>
                                    </table>"""
                                    
                                    
                                    
                                    
    return html



def checkAxis(objTypeSelected,objCatalogCrystalSystemSelected,objDataProperty):
    propertyDetailValueQuerySet = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected,dataproperty=objDataProperty).values('catalogaxis').annotate(total=Count('catalogaxis'))
    result = False
    if propertyDetailValueQuerySet:  
        result = True
 
   
    return result
    
def setAxis(objTypeSelected,objCatalogCrystalSystemSelected,objDataProperty):
    propertyDetailValueQuerySet = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected,dataproperty=objDataProperty).values('catalogaxis').annotate(total=Count('catalogaxis'))
    
    axisList = []
    for d in propertyDetailValueQuerySet:  
        if d['catalogaxis']:       
            objCatalogAxis=CatalogAxis.objects.filter(id=d['catalogaxis'] )
            for i,obj in enumerate(objCatalogAxis):
                axisList.append(objCatalogAxis[i].id)
             
    axisQuerySet = None
    try:
        
        axisQuerySet=CatalogAxis.objects.filter(id__in=axisList)         
    except ObjectDoesNotExist as error:
        print "Message({0}): {1}".format(99, error.message)      
      
     
    return  axisQuerySet       




def checkPointGroup(objTypeSelected,objCatalogCrystalSystemSelected,dataPropertySelected):
    propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected,dataproperty=dataPropertySelected).values('catalogpointgroup').annotate(total=Count('catalogpointgroup'))
    result = False
    if propertyDetail:  
        result = True
 
    return result

def checkPointGroupFiltred(objTypeSelected,objCatalogCrystalSystemSelected,dataPropertySelected):
    propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected,dataproperty=dataPropertySelected).values('catalogpointgroup').annotate(total=Count('catalogpointgroup'))
    result = False
    if propertyDetail:  
        for d in propertyDetail:
            if d['catalogpointgroup'] != 45:   
                result = True
 
    return result



def checkPuntualGroupNames(objTypeSelected,objCatalogCrystalSystemSelected,dataPropertySelected):        
    propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected,dataproperty=dataPropertySelected).values('puntualgroupnames').annotate(total=Count('puntualgroupnames'))
    result = False
    if propertyDetail:  
        result = True
 
    return result
        
def setPuntualGroupNames(objTypeSelected,objCatalogCrystalSystemSelected, dataPropertySelected):                                  
    propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected,dataproperty=dataPropertySelected).values('puntualgroupnames').annotate(total=Count('puntualgroupnames'))
    puntualGroupsList=[]
    puntualGroupNamesList = []
    for d in propertyDetail:
        #if d['puntualgroupnames'] != 21:   
            #print d['puntualgroupnames']              
        objPuntualgroupnames=PuntualGroupNames.objects.get(id__exact=d['puntualgroupnames']) 
        puntualGroupNamesList.append(objPuntualgroupnames.id)
        catalogpointgroupValuesQuerySet = PuntualGroupGroups.objects.filter(puntualgroupnames=objPuntualgroupnames).values('catalogpointgroup')
        del objPuntualgroupnames
        for obj in catalogpointgroupValuesQuerySet:
            puntualGroupsList.append(obj['catalogpointgroup'])
                
     
    try:
        puntualGroupNamesQuerySet = PuntualGroupNames.objects.filter(id__in=puntualGroupNamesList)
        puntualGroupsQuerySet = CatalogPointGroup.objects.filter(id__in=puntualGroupsList)
    except ObjectDoesNotExist as error:
        print "Message({0}): {1}".format(99, error.message)            

    
    return puntualGroupNamesQuerySet,puntualGroupsQuerySet
    
def setPointGroup(objTypeSelected,objCatalogCrystalSystemSelected,objDataProperty):                                                                                               
    propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected,dataproperty=objDataProperty).values('catalogpointgroup').annotate(total=Count('catalogpointgroup'))
    puntualGroupList = []
    for d in propertyDetail:  
        #if d['catalogpointgroup'] != 45:       
            #print d['catalogpointgroup']  
        objCatalogPointGroup=CatalogPointGroup.objects.get(id =d['catalogpointgroup'])  
        puntualGroupList.append(objCatalogPointGroup.id)   
        
    puntualGroupQuerySet = None
    try:
        puntualGroupQuerySet=CatalogPointGroup.objects.filter(id__in=puntualGroupList)
    except ObjectDoesNotExist as error:
        print "Message({0}): {1}".format(99, error.message) 
    
    return  puntualGroupQuerySet

def setPointGroupFiltred(objTypeSelected,objCatalogCrystalSystemSelected,objDataProperty):                                                                                               
    propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected,dataproperty=objDataProperty).values('catalogpointgroup').annotate(total=Count('catalogpointgroup'))
    puntualGroupList = []
    for d in propertyDetail:  
        if d['catalogpointgroup'] != 45:       
            #print d['catalogpointgroup']  
            objCatalogPointGroup=CatalogPointGroup.objects.get(id =d['catalogpointgroup'])  
            puntualGroupList.append(objCatalogPointGroup.id)   
        
    puntualGroupQuerySet = None
    try:
        puntualGroupQuerySet=CatalogPointGroup.objects.filter(id__in=puntualGroupList)
    except ObjectDoesNotExist as error:
        print "Message({0}): {1}".format(99, error.message) 
    
    return  puntualGroupQuerySet
                    
def get_nextautoincrement( mymodel ):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute( "SELECT AUTO_INCREMENT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='mpod'  AND TABLE_NAME='%s';" %  mymodel._meta.db_table)
        row = cursor.fetchone()
        cursor.close()
        return row[0]
    
def setCoefficients(objTypeSelected,objCatalogCrystalSystemSelected,objDataProperty,objCatalogpointgroupSelected,objPuntualgroupnamesSelected,axisSelected): 
    print 'SELECT *  FROM mpod.catalog_property_detail '
    print 'where type_id = ' + str(objTypeSelected.id)
    print 'and crystalsystem_id = ' + str(objCatalogCrystalSystemSelected.id)  
    print 'and dataproperty_id = '  + str(objDataProperty.id)  
    print 'and catalogpointgroup_id = ' + str(objCatalogpointgroupSelected.id)   
    print 'and puntualgroupnames_id = '  + str(objPuntualgroupnamesSelected.id)
    print 'and catalogaxis_id = ' + str(axisSelected.id)   
    
    
    catalogPropertyDetailList = []
    catalogPropertyDetailQuerySet= None
    try:
        catalogPropertyDetailQuerySet=CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected,dataproperty=objDataProperty,catalogpointgroup=objCatalogpointgroupSelected,puntualgroupnames=objPuntualgroupnamesSelected,catalogaxis=axisSelected).order_by('name')
        
    except ObjectDoesNotExist as error:
        pass
    
     
    #read_write_inputs_temp =  {}
    read_write_coefficients = {}
    for i,cpd in enumerate(catalogPropertyDetailQuerySet):
        read_write_coefficients[catalogPropertyDetailQuerySet[i].name] = "w"  
 
    #print read_write_coefficients
    datapropertyinitial=objDataProperty
    dimensions=datapropertyinitial.tensor_dimensions.split(',')
    #print str(len(dimensions))
    
    if len(dimensions) == 2:
        coefficients = N.zeros([int(dimensions[0]),int(dimensions[1])])    
        #print datapropertyinitial.tag
        parts=datapropertyinitial.tag.split('_')[-1]
        letters =parts.split('ij')
        x = 0
        #row = []
        for r in coefficients:
            x=x+ 1
            y=1   
            for c in r: 
                col= str(x) + str(y)                
                if (letters[0] +col + letters[1]) not in read_write_coefficients:
                    read_write_coefficients[letters[0] +col + letters[1]] =   "r"  
                    catalogPropertyDetailList.append(letters[0] +col + letters[1])
                y= y + 1 
 
                
 
         
    return catalogPropertyDetailQuerySet, catalogPropertyDetailList
 
         
    
    

def checkCoefficients(objTypeSelected,objCatalogCrystalSystemSelected,objDataProperty,objCatalogpointgroupSelected,objPuntualgroupnamesSelected,axisSelected): 
    catalogPropertyDetail=CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected,dataproperty=objDataProperty,catalogpointgroup=objCatalogpointgroupSelected,puntualgroupnames=objPuntualgroupnamesSelected,catalogaxis=axisSelected).order_by('name')
    #catalogPropertyDetail=CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected,dataproperty=objDataProperty).order_by('name')
 
    if catalogPropertyDetail:
        return True
    else:
        return False
    
    
def puntualgroupnamesParse(puntualgroupname):    
    line =  puntualgroupname
    line = line.replace('(',"")   
    line = line.replace(')',"")   
    line = line.strip()
    line=line.split(",")
    return line
    
    
    
    
