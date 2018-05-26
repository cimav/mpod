from django.db import models
from django.contrib.auth.models import User , Group
import datetime,time
from django import forms
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

 
 
 
 
 


from django.db.models.signals import post_save

#from views import datafiles_path
import os
from django.db.models.fields.files import FileField

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
        app_label = 'Configuration'
        verbose_name = _('Path Configuration')
        verbose_name_plural = _('Paths')

        

 
class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self         

class FileProperty(object):
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
    
    class Meta:
        db_table = 'data_publarticle'
        app_label = 'Article'
        verbose_name = _('Article Information')
        verbose_name_plural = _('Articles')
        
 

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
    
    class Meta:
        db_table = 'data_property' 
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Data Property')
        verbose_name_plural = _('Data Properties') 
    
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
    publication = models.ForeignKey(PublArticle,verbose_name="Article")
    properties = models.ManyToManyField(Property, null=True, blank=True, db_table = 'data_datafile_property',verbose_name="Properties")
    
    class Meta:
        db_table = 'data_datafile' 
        app_label = 'Article'
         
        verbose_name = _('CIF File Information')
        verbose_name_plural = _('CIF Files')
        
        
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


    def __unicode__(self):
        return str(self.code)+", "+str(self.phase_generic)+", "+str(self.phase_name)
    
    
    
class DataFileTemp(models.Model):
    code = models.IntegerField(max_length=8)
    filename = models.CharField(max_length=500)
    cod_code = models.IntegerField(max_length=8, null=True, blank=True)
    phase_generic = models.CharField(max_length=255, null=True, blank=True)
    phase_name = models.CharField(max_length=255)
    chemical_formula = models.CharField(max_length=255)
    publication = models.ForeignKey(PublArticleTemp)
    properties = models.ManyToManyField(PropertyTemp, null=True, blank=True, db_table = 'data_datafile_property_temp',verbose_name="Properties")
     
    def ret_link_to_file(self):
        return os.path.join(datafiles_path, self.filename)

    def __unicode__(self):
        return str(self.code)+", "+str(self.phase_generic)+", "+str(self.phase_name)
    

    class Meta:
        db_table = 'data_datafile_temp'
        

class DataFileProperty(models.Model):    
    datafile =models.ForeignKey(DataFile,verbose_name="Data File")
    property=models.ForeignKey(Property,verbose_name="Property")
    
    class Meta:
        db_table = 'data_datafile_property'
        app_label = 'File Property'
        verbose_name = _('File Property Information')
        verbose_name_plural = _('Articles')

class DataFilePropertyTemp(models.Model):    
    datafiletemp =models.ForeignKey(DataFileTemp)
    propertytemp=models.ForeignKey(PropertyTemp)
    
    class Meta:
        db_table = 'data_datafile_property_temp'    
   
   
class PropertyValues(models.Model):
    datafileproperty=models.ForeignKey(DataFileProperty)
    prop_data_label = models.CharField(max_length=255)
    prop_data_tensorial_index = models.CharField(max_length=255)
    prop_data_value = models.CharField(max_length=511)
 

    def __unicode__(self):
        return str(self.name) +", "+  str(self.units)
    
    class Meta:
        db_table = 'property_values' 
        app_label = 'Article'
        verbose_name = _('Article Information')
        verbose_name_plural = _('Articles')
             
        
        
class PropertyValuesTemp(models.Model):
    datafileproperty=models.ForeignKey(DataFilePropertyTemp)
    prop_data_label = models.CharField(max_length=255)
    prop_data_tensorial_index = models.CharField(max_length=255)
    prop_data_value = models.CharField(max_length=511)
    

    def __unicode__(self):
        return str(self.name) +", "+  str(self.units)
    
    class Meta:
        db_table = 'property_values_temp' 
        app_label = string_with_title("Properties", "Properties Settings")
        #verbose_name = _('Crystal System')
        #verbose_name_plural = _('CrystalSystem')
        

        
        

class ExperimentalParCond(models.Model):
    tag = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)
    units = models.CharField(max_length=25)
    units_detail = models.CharField(max_length=60)
    
    class Meta:
        db_table = 'data_experimentalparcond' 
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Experimental par condition')
        verbose_name_plural = _('Experimental par conditions')
    
    
    

    def __unicode__(self):
        return str(self.name) +", "+  str(self.units)
    
class ExperimentalParCondTemp(models.Model):
    tag = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)
    units = models.CharField(max_length=25)
    units_detail = models.CharField(max_length=60)
    #active= models.CharField(max_length=1)

    def __unicode__(self):
        return str(self.name) +", "+  str(self.units)  
    
    class Meta:
        db_table = 'data_experimentalparcond_temp'  
    


class CatalogProperty(models.Model): 
    name = models.CharField(max_length=255,verbose_name="Name")
    description = models.CharField(max_length=511,verbose_name="Description")
    active = models.BooleanField(_(u'Active'),default=False)
   
    class Meta:
        db_table = 'data_catalogproperty'
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Poperty')
        verbose_name_plural = _('Properties')
        
        
    def __unicode__(self):
        return str(self.description)
    
    
class CatalogCrystalSystem(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)   
    catalogproperty =   models.ForeignKey(CatalogProperty,verbose_name="Property")
    active = models.BooleanField(_(u'Active'),default=False)
    
    class Meta:
        db_table = 'catalog_crystal_system'
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Crystal System')
        verbose_name_plural = _('Crystal Systems')
 
    
    def __unicode__(self):
        return str(self.catalogproperty.description)+" - " +  str(self.description) 
        
        
class Type(models.Model): 
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)   
    catalogproperty=  models.ForeignKey(CatalogProperty,verbose_name="Property")
    active = models.BooleanField(_(u'Active'),default=False)
    
    class Meta:
        db_table = 'type'     
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Type')
        verbose_name_plural = _('Types') 
    
    def __unicode__(self):
        return str(self.catalogproperty.description)+" - " +  str(self.description) 
        

class CatalogPointGroup(models.Model): 
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)      
    class Meta:
        db_table = 'catalog_point_group'        
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Point Group')
        verbose_name_plural = _('Point Groups')
        
    def __unicode__(self):
        return str(self.name)   
        

class CrystalSystemPointGroup(models.Model): 
    crystalsystem= models.ForeignKey(CatalogCrystalSystem,verbose_name="Crystal System")   
    catalogpointgroup =   models.ForeignKey(CatalogPointGroup,verbose_name="Point Group")  
        
    class Meta:
        db_table = 'crystalsystem_point_group'    
        app_label = string_with_title("Properties", "Properties Settings")
        #verbose_name = _('Crystal System')
        #verbose_name_plural = _('CrystalSystem')     
       
          
        
        
class CatalogAxis(models.Model): 
    name = models.CharField(max_length=255) 
    description = models.CharField(max_length=511)   
   
    class Meta:
        db_table = 'catalog_axis'   
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Axis')
        verbose_name_plural = _('Axes')  
        
    def __unicode__(self):
        return str(self.name)
        
       
class CrystalSystemAxis(models.Model): 
    crystalsystem= models.ForeignKey(CatalogCrystalSystem,verbose_name="Crystal System")   
    catalogaxis= models.ForeignKey(CatalogAxis,verbose_name="Axis")       
    class Meta:
        db_table = 'crystalsystem_axis'  
        app_label = string_with_title("Properties", "Properties Settings")
        #verbose_name = _('Crystal System')
        #verbose_name_plural = _('CrystalSystem')
        
                
class PuntualGroupNames(models.Model): 
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511,blank=True)   
   
    class Meta:
        db_table = 'puntual_group_names'    
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        
    def __unicode__(self):
        return str(self.name)   
    

        
class PuntualGroupGroups(models.Model): 
    catalogpointgroup =   models.ForeignKey(CatalogPointGroup,verbose_name="Point Group") 
    puntualgroupnames = models.ForeignKey(PuntualGroupNames,verbose_name="Group Names")     
   
    class Meta:
        db_table = 'puntual_group_groups'            
        #app_label = 'Propertie_Settings'
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Point Group and Group')
        verbose_name_plural = _('Point Groups and Groups')
         
    def __unicode__(self):
        return  str(self.puntualgroupnames)    
    
    
 
    
 
          
class CatalogPropertyDetail(models.Model): 
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)   
    type=  models.ForeignKey(Type)
    crystalsystem= models.ForeignKey(CatalogCrystalSystem,verbose_name="Crystal System")    
    catalogaxis= models.ForeignKey(CatalogAxis,verbose_name="Axes")  
    catalogpointgroup =   models.ForeignKey(CatalogPointGroup,verbose_name="Point Group")  
    puntualgroupnames = models.ForeignKey(PuntualGroupNames,verbose_name="Group Names")  
    dataproperty = models.ForeignKey(Property,verbose_name="Tag",blank=True)  
    class Meta:
        db_table = 'catalog_property_detail'       
        
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Property Detail')
        verbose_name_plural = _('Properties Detail')
        
    def __unicode__(self):
        return str(self.name)
    
class CatalogPropertyDetail1(models.Model): 
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)   
    type=  models.ForeignKey(Type)
    crystalsystem= models.ForeignKey(CatalogCrystalSystem,verbose_name="Crystal System")    
    catalogaxis= models.ForeignKey(CatalogAxis,verbose_name="Axes")  
    catalogpointgroup =   models.ForeignKey(CatalogPointGroup,verbose_name="Point Group")  
    puntualgroupnames = models.ForeignKey(PuntualGroupNames,verbose_name="Group Names")  
    dataproperty = models.ForeignKey(Property,verbose_name="Tag",blank=True)  
    class Meta:
        db_table = 'catalog_property_detail12'       
        
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Property Detail')
        verbose_name_plural = _('Properties Detail')
        
    def __unicode__(self):
        return str(self.name)
        
    
class CatalogPropertyDetailTemp(models.Model): 
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)   
    type=  models.ForeignKey(Type)
    crystalsystem= models.ForeignKey(CatalogCrystalSystem,verbose_name="Crystal System")    
    catalogaxis= models.ForeignKey(CatalogAxis,verbose_name="Axes")  
    catalogpointgroup =   models.ForeignKey(CatalogPointGroup,verbose_name="Point Group")  
    puntualgroupnames = models.ForeignKey(PuntualGroupNames,verbose_name="Group Names")  
    dataproperty = models.ForeignKey(Property,verbose_name="Tag",blank=True)  
    class Meta:
        db_table = 'catalog_property_detail_temp'       
        
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Property Detail')
        verbose_name_plural = _('Properties Detail')
        
    def __unicode__(self):
        return str(self.name)
        
        
class MpodFile(models.Model): 
    revision = models.CharField(max_length=3)
    description1 = models.TextField()   
    site = models.CharField(max_length=100)  
    description2 = models.TextField()  

    class Meta:
        db_table = 'mpodfile'          
        



class Configuration(models.Model):
    email_use_tls = models.BooleanField(_(u'TLS'),default=True)
    email_host = models.CharField(_(u'HOST'),max_length=1024)
    email_host_user = models.CharField(_(u'USER'),max_length=255)
    email_host_password = models.CharField(_(u'PASSWORD'),max_length=255)
    email_port = models.PositiveIntegerField(_(u'PORT'),default=587)
    email_domain = models.CharField(_(u'DOMAIN'),max_length=1024)
      
    
    class Meta:
        db_table = 'mail_configuration'
        #app_label = 'Configuration'
        app_label = string_with_title("Configuration", "Configuration Message")
        verbose_name = _('SMTP Server Configuration')
        verbose_name_plural = _('SMTP Server Configurations')
        ordering = ('email_host',)
        
        
    def __unicode__(self):
        return str(self.email_host_user)
        
        
class MessageMail(models.Model):
    email_subject= models.CharField(_(u'SUBJECT'),max_length=255)
    email_regards= models.CharField(_(u'REGARDS'),max_length=255)
    email_message = models.TextField(_(u'BODY MESSAGE'),max_length=3072)
    
    class Meta:
        db_table = 'message_mail'
        #app_label = 'Configuration'
        app_label = string_with_title("Configuration", "Configuration Message")
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ('email_message',)
        
    def __unicode__(self):
        return str(self.email_subject)

        
class MessageCategory(models.Model):
    name = models.CharField(_(u'NAME'),max_length=100)
    description = models.CharField(_(u'DESCRIPTION'),max_length=255)
    

    class Meta:
        db_table = 'message_category'
        #app_label = 'Configuration'
        app_label = string_with_title("Configuration", "Configuration Message")
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        
    def __unicode__(self): # __str__ on Python 3
        return str(self.name)
        
        
#poll = models.ForeignKey(Poll,on_delete=models.CASCADE,verbose_name="the related poll")
class MessageCategoryDetail(models.Model):
    message=models.ForeignKey(MessageMail,verbose_name="Message")  
    messagecategory=models.ForeignKey(MessageCategory,verbose_name="Category")
    group = models.ForeignKey(Group,verbose_name="Group") 
    user = models.ForeignKey(User,verbose_name="User") 
        
    class Meta:
        db_table = 'message_category_detail'
        #app_label = 'Configuration'
        app_label = string_with_title("Configuration", "Configuration Message")
        verbose_name = _('Message And Category')
        verbose_name_plural = _('Message And Categories')
         
        
    def get_category(self):
         return str(self.messagecategory.name)
     
    def get_message(self):
         return str(self.message)
     

    
    
    
    
class ConfigurationMessage(models.Model):
        account=models.ForeignKey(Configuration)  
        message=models.ForeignKey(MessageMail)  
        is_active = models.BooleanField(_(u'Active'),default=False)
           
        class Meta:
             db_table = 'configuration_message'
             #app_label = 'Configuration'
             app_label = string_with_title("Configuration", "Configuration Message")
             verbose_name = _('Message Send By Email  Account')
             verbose_name_plural = _('Message  Send By Email Accounts')
             
        def get_email_host_user(self):
             return str(self.account.email_host_user)
         
        def get_message(self):
             return str(self.message.email_subject)
         
         
         
          
class FileUser(models.Model):
    filename = models.CharField(_(u'File Name'),max_length=100)
    authuser=models.ForeignKey(User,verbose_name="User Name")  
    #authuser=models.ForeignKey(to=User, related_name="pk", null=True, blank=True)
    date = models.DateTimeField(_(u'Registration Date'),default=datetime.datetime.now(), blank=True)
    reportvalidation =  models.TextField(_(u'Report Validation'))
    datafile  = models.ForeignKey(DataFile,verbose_name="File",null=True,blank=True)   
    published= models.BooleanField(_(u'Publish'),max_length=1)
    datepublished = models.DateTimeField(_(u'Published Date'),default=None, blank=True)
   
     
     
    class Meta:
        db_table = 'file_user'
        app_label = string_with_title("Users", "Users Files")
        verbose_name = _('Publish file')
        verbose_name_plural = _('Publish files') 
    """     
    def get_absolute_url(self):
        #from django.urls import reverse
        form_url  =reverse('update',kwargs={'pk':self.pk})
        form_url =""
        return form_url
    """
     
    def user_name(self):
        return   self.authuser.username

        
        
        
        

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user',on_delete=models.CASCADE)
    #photo = FileField(verbose_name=_("Profile Picture"),  upload_to=upload_to("main.UserProfile.photo", "profiles"), format="Image", max_length=255, null=True, blank=True)    

    #photo = models.FileField(_("Profile Picture"), upload_to='profiles', max_length=255, null=True, blank=True)
    
    bio = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    organization = models.CharField(max_length=100, default='', blank=True)

    class Meta:
        db_table = 'user_profile'


    def filename(self):
        return os.path.basename(self.file.name)


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)






    
    
class Category(models.Model):
    name = models.CharField(_(u'Name'),max_length=100)
    description = models.CharField(_(u'Description'),max_length=255)
    
    class Meta:
        db_table = 'category'
        app_label = 'Dictionaries'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        
    def __unicode__(self): # __str__ on Python 3
        return str(self.name)
        
        
class Dictionary(models.Model):
    tag = models.CharField(_(u'Tag'),max_length=255)
    name = models.CharField(_(u'Name'),max_length=255)
    description = models.CharField(_(u'Description'),max_length=511)
    units = models.CharField(_(u'Units'),max_length=25)
    units_detail = models.CharField(_(u'Units Detail'),max_length=60)
    active= models.BooleanField(_(u'Active'),max_length=1)
    definition= models.TextField()  
    deploy= models.BooleanField(_(u'Deploy'),max_length=1)
    type = models.CharField(_(u'Data type'),max_length=45,choices=(('char','char'),('numb','numb')))
    category = models.ForeignKey(Category,related_name="Category",verbose_name="Category")
    
    class Meta:
        db_table = 'dictionary'
        
        
        app_label = 'Dictionaries'
        verbose_name = _('Properties')
        verbose_name_plural = _('Dictionary')
         
        #verbose_name_plural = _('Uploaded files')
        
    
        
class PropTags(models.Model):
    tag = models.CharField(_(u'tag'),max_length=100)
    active= models.BooleanField(_(u'Active'),max_length=1,default=True)
    
    class Meta:
        db_table = 'prop_tags'
        
    def __unicode__(self): # __str__ on Python 3
        return str(self.tag)
    
class CatalogpropertyDictionary(models.Model):
    catalogproperty = models.ForeignKey(CatalogProperty,related_name="CatalogProperty", verbose_name="Catalog Properties")
    dictionary =models.ForeignKey(Dictionary,related_name="Dictionary",verbose_name="Dictionary")
    
    

    class Meta:
        db_table = 'catalogproperty_dictionary'
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Detail Property')
        verbose_name_plural = _('Detail Properties')
     

    def __unicode__(self): # __str__ on Python 3
        return str('')
        
        
    def get_property(self):
        return str(self.dataproperty.name)
     
    def get_catalogproperty(self):
        return str(self.catalogproperty.description)
    
    

class  ExperimentalfilecontempDatafiletemp(models.Model):
    datafiletemp =models.ForeignKey(DataFileTemp,verbose_name="Data File")
    experimentalfilecontemp = models.ForeignKey(ExperimentalParCondTemp, verbose_name="Experimental conditions")
  
    
    class Meta:
        db_table = 'experimentalfilecontemp_datafiletemp'
    
 
 
class   TypeDataProperty(models.Model):
    type=  models.ForeignKey(Type,verbose_name="Type")
    dataproperty= models.ForeignKey(Property,verbose_name="Data Property")
    
    
    class Meta:
        db_table = 'type_data_property'
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Type and Data Property')
        verbose_name_plural = _('Types and Data Properties') 
    
    def __unicode__(self):
        return str(self.dataproperty.tag)
    
         
         
    
class DataPropertyDetail(TypeDataProperty):
    class Meta:
        proxy=True
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Data Property Detail')
        verbose_name_plural = _('Data Properties Details') 
        
        
class PuntualGroupsDetail(PuntualGroupGroups):
    class Meta:
        proxy=True
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Group Detail')
        verbose_name_plural = _('Groups Detail')
        
    """def save(self, *args, **kwargs):
        self.catalogpointgroup = CatalogPointGroup.objects.get(name='1')
         
        super(PuntualGroupsDetail, self).save(*args, **kwargs)
    """   
    
  
  
class PuntualGroupNamesManager(models.Manager):
    def get_queryset(self):

        return super(PuntualGroupNamesManager, self).get_queryset().all().exclude(id=21)
        
class GroupNamesDetail(PuntualGroupNames):
    #objects = PuntualGroupNamesManager()

    class Meta:
        proxy=True
        app_label = string_with_title("Properties", "Properties Settings")
        verbose_name = _('Group Name Detail')
        verbose_name_plural = _('Group Names Detail')  
    def save(self, *args, **kwargs):
        #self.section = Section.objects.get(name='reviews')
        super(GroupNamesDetail, self).save(*args, **kwargs)

        
class DummyModel(models.Model):
        def __init__(self, filename, original=None):
            pass
        def save(self):
            pass
        def get_absolute_url(self):
            pass



 

 
 
        

        
    