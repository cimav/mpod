from django.db import models
from django import forms
from django.utils.html import escape

#from views import datafiles_path
import os

# Create your models here.

#datafiles_path=os.path.join(os.path.dirname(__file__),'media/datafiles').replace('\\','/')
datafiles_path=''

class Path(models.Model):
    cifs_dir = models.CharField(max_length=511)
    cifs_dir_valids = models.CharField(max_length=511)
    cifs_dir_invalids = models.CharField(max_length=511)
    core_dic_filepath = models.CharField(max_length=511)
    mpod_dic_filepath = models.CharField(max_length=511)
    cifs_dir_output = models.CharField(max_length=511)
    stl_dir = models.CharField(max_length=511)
    datafiles_path = models.CharField(max_length=511)
    devmode = models.IntegerField(max_length=1)


    class Meta:
        db_table = 'path'
        
'''      
pathslist=Path.objects.all()      
pathexist = 0
for datafiles_path in pathslist:
    path=Path() 
    path = datafiles_path
    if os.path.isdir(path.datafiles_path): 
        pathexist = 1
        datafiles_path= path.datafiles_path
        break'''
            

class StructurePropertie(object):
        def __init__(self,):
            self._prop_name=''
            self._prop_data_label=[]
            self._prop_data_tensorial_index=[]
            self._prop_data_value=[]
            self._prop_measurement_method=[]

class PublArticle(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    journal = models.CharField(max_length=127)
    year = models.IntegerField(max_length=4, null=True)
    volume = models.CharField(max_length=6)
    issue = models.IntegerField(max_length=6, null=True, blank=True)
    first_page = models.IntegerField(max_length=6, null=True, blank=True)
    last_page = models.IntegerField(max_length=6, null=True, blank=True)
    reference = models.CharField(max_length=14, blank=True)
    pages_number = models.IntegerField(max_length=3, null=True, blank=True)

    def __unicode__(self):
        return str(self.title)+", "+str(self.journal)
    
    
class PublArticleTemp(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    journal = models.CharField(max_length=127)
    year = models.IntegerField(max_length=4, null=True)
    volume = models.CharField(max_length=6)
    issue = models.IntegerField(max_length=6, null=True, blank=True)
    first_page = models.IntegerField(max_length=6, null=True, blank=True)
    last_page = models.IntegerField(max_length=6, null=True, blank=True)
    reference = models.CharField(max_length=14, blank=True)
    pages_number = models.IntegerField(max_length=3, null=True, blank=True)

    def __unicode__(self):
        return str(self.title)+", "+str(self.journal)
    
    class Meta:
        db_table = 'data_publarticle_temp'  

class Property(models.Model):
    tag = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)
    tensor_dimensions = models.CharField(max_length=10)
    units = models.CharField(max_length=25)
    units_detail = models.CharField(max_length=60)

    def __unicode__(self):
        return str(self.name) +", "+  str(self.units)
    
class PropertyTemp(models.Model):
    tag = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)
    tensor_dimensions = models.CharField(max_length=10)
    units = models.CharField(max_length=25)
    units_detail = models.CharField(max_length=60)

    def __unicode__(self):
        return str(self.name) +", "+  str(self.units)
    
    class Meta:
        db_table = 'data_property_temp' 
        
   

class DataFile(models.Model):
    code = models.IntegerField(max_length=8, primary_key=True)
    filename = models.CharField(max_length=13)
    cod_code = models.IntegerField(max_length=8, null=True, blank=True)
    phase_generic = models.CharField(max_length=255, null=True, blank=True)
    phase_name = models.CharField(max_length=255)
    chemical_formula = models.CharField(max_length=255)
    publication = models.ForeignKey(PublArticle)
    properties = models.ManyToManyField(Property, null=True, blank=True, db_table = 'data_datafile_property')
    
    
    def ret_link_to_file(self):
        pathslist=Path.objects.all()      
        pathexist = 0
        for datafiles_path in pathslist:
            path=Path() 
            path = datafiles_path
            if os.path.isdir(path.datafiles_path): 
                pathexist = 1
                datafiles_path= path.datafiles_path
                break
            
        return os.path.join(datafiles_path, self.filename)
    
    def article_id(self):
        '''pathslist=Path.objects.all()      
        pathexist = 0
        for datafiles_path in pathslist:
            path=Path() 
            path = datafiles_path
            if os.path.isdir(path.datafiles_path): 
                pathexist = 1
                datafiles_path= path.datafiles_path
                break'''
        
        #link_to_article ='/admin/data/publarticle/' +self.publication.id
        link_to_article=os.path.join('./admin/data/publarticle/' , str(self.publication.id))
        return link_to_article
    
    

    
   
    
    

    def __unicode__(self):
        return str(self.code)+", "+str(self.phase_generic)+", "+str(self.phase_name)
    
    
    
class DataFileTemp(models.Model):
    code = models.IntegerField(max_length=8, primary_key=True)
    filename = models.CharField(max_length=13)
    cod_code = models.IntegerField(max_length=8, null=True, blank=True)
    phase_generic = models.CharField(max_length=255, null=True, blank=True)
    phase_name = models.CharField(max_length=255)
    chemical_formula = models.CharField(max_length=255)
    publication = models.ForeignKey(PublArticleTemp)
    properties = models.ManyToManyField(PropertyTemp, null=True, blank=True, db_table = 'data_datafile_property_temp')
    
    
    def ret_link_to_file(self):
        return os.path.join(datafiles_path, self.filename)

    def __unicode__(self):
        return str(self.code)+", "+str(self.phase_generic)+", "+str(self.phase_name)
    

    class Meta:
        db_table = 'data_datafile_temp'
        

class DataFileProperty(models.Model):    
    datafile =models.ForeignKey(DataFile)
    property=models.ForeignKey(Property)
    
    class Meta:
        db_table = 'data_datafile_property'

class DataFilePropertyTemp(models.Model):    
    datafile =models.ForeignKey(DataFileTemp)
    property=models.ForeignKey(PropertyTemp)
    
    class Meta:
        db_table = 'data_datafile_property_temp'    
   
   
class PropertyValues(models.Model):
    datafileproperty=models.ForeignKey(DataFileProperty)
    prop_data_label = models.CharField(max_length=255)
    prop_data_tensorial_index = models.CharField(max_length=255)
    prop_data_value = models.CharField(max_length=511)
    prop_measurement_method = models.CharField(max_length=10)

    def __unicode__(self):
        return str(self.name) +", "+  str(self.units)
    
    class Meta:
        db_table = 'property_values' 
             
        
        
class PropertyValuesTemp(models.Model):
    datafileproperty=models.ForeignKey(DataFilePropertyTemp)
    prop_data_label = models.CharField(max_length=255)
    prop_data_tensorial_index = models.CharField(max_length=255)
    prop_data_value = models.CharField(max_length=511)
    prop_measurement_method = models.CharField(max_length=10)

    def __unicode__(self):
        return str(self.name) +", "+  str(self.units)
    
    class Meta:
        db_table = 'property_values_temp' 
        

        
        

class ExperimentalParCond(models.Model):
    tag = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)
    units = models.CharField(max_length=25)
    units_detail = models.CharField(max_length=60)

    def __unicode__(self):
        return str(self.name) +", "+  str(self.units)
    
class ExperimentalParCondTemp(models.Model):
    tag = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)
    units = models.CharField(max_length=25)
    units_detail = models.CharField(max_length=60)
    active= models.CharField(max_length=1)

    def __unicode__(self):
        return str(self.name) +", "+  str(self.units)  
    
    class Meta:
        db_table = 'data_experimentalparcond_temp'  
    
    

    
    

    
    
 

class CatalogProperty(models.Model): 
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)
    #publication = models.ForeignKey(PublArticle)
    def __unicode__(self):
        return str(self.name)+", "+str(self.description)
    
    
class CatalogCrystalSystem(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)   
    catalogproperty =   models.ForeignKey(CatalogProperty)
    
    class Meta:
        db_table = 'catalog_crystal_system'
        
        
class Type(models.Model): 
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)   
    catalogproperty=  models.ForeignKey(CatalogProperty)
    
    class Meta:
        db_table = 'type'      
        

class CatalogPointGroup(models.Model): 
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)      
    class Meta:
        db_table = 'catalog_point_group'        
        
        

class CrystalSystemPointGroup(models.Model): 
    crystalsystem= models.ForeignKey(CatalogCrystalSystem)   
    catalogpointGroup =   models.ForeignKey(CatalogPointGroup)  
        
    class Meta:
        db_table = 'crystalsystem_point_group'         
       
          
        
        
class CatalogAxis(models.Model): 
    name = models.CharField(max_length=255) 
    description = models.CharField(max_length=511)   
   
    class Meta:
        db_table = 'catalog_axis'     
        
       
class CrystalSystemAxis(models.Model): 
    crystalsystem= models.ForeignKey(CatalogCrystalSystem)   
    catalogaxis= models.ForeignKey(CatalogAxis)       
    class Meta:
        db_table = 'crystalsystem_axis'  
        
                
class PuntualGroupNames(models.Model): 
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)   
   
    class Meta:
        db_table = 'puntual_group_names'    
        
        
class PuntualGroupGroups(models.Model): 
    catalogpointgroup =   models.ForeignKey(CatalogPointGroup) 
    puntualgroupnames = models.ForeignKey(PuntualGroupNames) 
   
    class Meta:
        db_table = 'puntual_group_groups'            
        
         
        
          
class CatalogPropertyDetail(models.Model): 
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)   
    type=  models.ForeignKey(Type)
    crystalsystem= models.ForeignKey(CatalogCrystalSystem)    
    catalogaxis= models.ForeignKey(CatalogAxis)  
    catalogpointgroup =   models.ForeignKey(CatalogPointGroup)  
    puntualgroupnames = models.ForeignKey(PuntualGroupNames)  
    class Meta:
        db_table = 'catalog_property_detail'          
        
        
class MpodFile(models.Model): 
    revision = models.CharField(max_length=3)
    description1 = models.TextField()   
    site = models.CharField(max_length=100)  
    description2 = models.TextField()  

    class Meta:
        db_table = 'mpodfile'          
        
 
    
    

    
    
    
##class DataFile_Property(models.Model):
##    datafile = models.ForeignKey(DataFile)
##    property = models.ForeignKey(Property)
##    
##    def __unicode__(self):
##        return str(self.datafile)+", "+str(self.property)
