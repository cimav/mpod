'''
Created on Aug 13, 2017

@author: admin
'''
from django import forms            
from django.contrib.auth.models import User   # fill in custom user info then save it 
from django.contrib.auth.forms import * 
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import string
from django.utils.translation import ugettext_lazy as _
from models import *
from django.contrib.admin import widgets
from django.contrib.admin.widgets import FilteredSelectMultiple
 
from django.contrib.auth.models import Permission, Group
from django.db.models import Q
from django.conf import settings
from cProfile import label
from django.forms.models import fields_for_model
from django.db.models import Count
from django.core  import urlresolvers
from django.core.exceptions import ObjectDoesNotExist
import numpy as N

from itertools import chain
from django.contrib import messages
from django.forms.widgets import SelectMultiple


 
 
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control','style': 'width: 300px;'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','style': 'width: 300px;'}),
            'email': forms.TextInput(attrs={'class': 'form-control','style': 'width: 300px;'}),
        }
        
     
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'phone', 'city', 'country', 'organization']
        widgets = {
            #'photo':forms.CharField(widget=forms.ImageField ()),
            'bio': forms.Textarea(attrs={'class': 'form-control','style': 'width: 350px;'}),
            'phone': forms.TextInput(attrs={'class': 'form-control','style': 'width: 300px;'}),
            'city': forms.TextInput(attrs={'class': 'form-control','style': 'width: 300px;'}),
            'country': forms.TextInput(attrs={'class': 'form-control','style': 'width: 300px;'}),
            'organization': forms.TextInput(attrs={'class': 'form-control','style': 'width: 300px;'}),
        }
        
        
"""
class SignUpForm(UserCreationForm):
    
    #email = forms.EmailField(required=True,max_length=254, help_text='Required. Inform a valid email address.')
    #name = forms.CharField(required=True)
 

    class Meta:
        model = UserProfile
        #fields = {'name', 'first_name','last_name','username', 'password1', 'password2', 'email'}
        #fields = {'user', 'bio', 'phone', 'city', 'country', 'organization'}
        fieldsets = (
        ('user', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        }),
        ('profile', {
            'fields': ('bio', 'phone', 'city', 'country', 'organization')
        }),
    )
        

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        #user.email = self.cleaned_data['email']
        #user.name = self.cleaned_data['name']
        user.is_active = False           
        if commit:
            user.save()
            #default_token_generator.make_token(user)

        return user
    """
    
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
         
        widgets = {   'first_name': forms.TextInput(attrs={'class': 'form-control input-sm','style': 'width: 350px;','placeholder':"First Name"}),
                   
                   }
        
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(u'Username "%s" is already in use.' % username)
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(u'Email "%s" is already in use.' % email)
        return email        
  
    
    
class LoginForm(AuthenticationForm):   
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.username = forms.CharField(label="Username", max_length=10, widget=forms.TextInput(attrs={'class': 'form-control',  'name': 'username'}))
        self.password = forms.CharField( label="Password",max_length=10,   widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))
        #fields = { 'username', 'password'}
         

class ValidationForm(forms.Form):
    #even_field = forms.IntegerField(validators=[validate_even])

    username = forms.CharField(help_text="Enter your username.")
    password = forms.CharField(help_text="Enter yuor password.")
    
    
class NewCaseForm(forms.Form):
    title = forms.BooleanField(required=True)
    author = forms.BooleanField(required=True)
    journal = forms.BooleanField(required=True)
    title = forms.CharField(help_text="Enter title.")
    author = forms.CharField(help_text="Enter author.")
    journal = forms.CharField(help_text="Enter journal.")

     
     
    def __init__(self, *args, **kwargs):
        if 'inputList' not in kwargs:
            pass
        else:
            #print  kwargs.pop('inputList') 
            inputList = kwargs.pop('inputList')    
            print "inout list: " 
            #print inputList
           
            super(NewCaseForm, self).__init__(*args, **kwargs)
            if inputList:
                for ipt  in inputList:  
                    print ipt.name
                    if   's' in ipt.name:
                        self.fields[ ipt.name] =forms.FloatField(widget=forms.TextInput(attrs={'class':'inlineLabels'}),label= ipt.name)
                        #self.fields[ipt.name].label = "Your name:"
                    if   'c' in ipt.name:
                        self.fields[ ipt.name] =forms.FloatField(widget=forms.TextInput(attrs={'class':'inlineLabels'}),label= ipt.name)
                    if   'd' in ipt.name:
                        self.fields[ ipt.name] =forms.FloatField(widget=forms.TextInput(attrs={'class':'inlineLabels'}),label= ipt.name)


             
           
   
   
class NewCaseFormv2(forms.Form):
    title = forms.CharField(required=True,help_text="Enter title." ,label= 'Article Title',initial='')
    author = forms.CharField(required=True,help_text="Enter author(s) separated by commas.",label='Author(s)',initial='')
    journal = forms.CharField(required=True,help_text="Enter journal.",label='Journal',initial='')
    volume = forms.CharField(required=True,help_text="Enter volume.",label='Volume',initial='')
    year = forms.IntegerField(required=True,help_text="Enter year.",label='Year',initial='')
    page_first = forms.CharField(required=True,help_text="Enter page.",label='First page',initial='')
    page_last = forms.CharField(required=True,help_text="Enter page.",label='Last page',initial='')
    
    

             

    
class ValidateAddCaseFormv2(forms.Form):
    title = forms.CharField(required=True,help_text="Enter title." ,label= 'Article Title')
    author = forms.CharField(required=True,help_text="Enter author(s) separated by commas.",label='Author(s)')
    journal = forms.CharField(required=True,help_text="Enter journal.",label='Journal')
    volume = forms.CharField(required=True,help_text="Enter volume.",label='Volume',initial='')
    year = forms.CharField(required=True,help_text="Enter year.",label='Year',initial='')
    page_first = forms.CharField(required=True,help_text="Enter page.",label='First page',initial='')
    page_last = forms.CharField(required=True,help_text="Enter page.",label='Last page',initial='')
    

    def clean_year(self):
        year = self.cleaned_data['year']
        try:
            int(year)
            pass
        except ValueError:
            raise forms.ValidationError(u'Year "%s" is not a valid year.' % year)
        
    def clean_page_first(self):
        page_first = self.cleaned_data['page_first']
        try:
            int(page_first)
            pass
        except ValueError:
            raise forms.ValidationError(u'Page first "%s" is not a valid value.' % page_first)
        
    def clean_page_last(self):
        page_last = self.cleaned_data['page_last']
        try:
            int(page_last)
            pass
        except ValueError:
            raise forms.ValidationError(u'Page last "%s" is not a valid value.' % page_last)
      
     
    def __init__(self, *args, **kwargs):
        if 'inputList' not in kwargs:
            pass
        else:
            #print  kwargs.pop('inputList') 
            inputList = kwargs.pop('inputList')    
            
            #print inputList
           
            super(ValidateAddCaseFormv2, self).__init__(*args, **kwargs)
            if inputList:
                for ipt  in inputList:  
                    #print ipt.name
                    if   's' in ipt.name:
                        #self.fields[ ipt.name] =forms.FloatField(widget=forms.TextInput(attrs={'class':'inlineLabels'}),label= ipt.name)
                        self.fields[ ipt.name] = forms.FloatField(forms.CharField(required=True,help_text=str(ipt.name) + "Enter value" ,label= ipt.name))
                        
                    if   'c' in ipt.name:
                        self.fields[ ipt.name] = forms.FloatField(forms.CharField(required=True,help_text=str(ipt.name) + "Enter value" ,label= ipt.name))
                        #self.fields[ ipt.name] =forms.FloatField(widget=forms.TextInput(attrs={'class':'inlineLabels'}),label= ipt.name)
                    if   'd' in ipt.name:
                        self.fields[ ipt.name] = forms.FloatField(forms.CharField(required=True,help_text=str(ipt.name) + "Enter value" ,label= ipt.name))
                        #self.fields[ ipt.name] =forms.FloatField(widget=forms.TextInput(attrs={'class':'inlineLabels'}),label= ipt.name)


             
         

 


FAVORITE_COLORS_CHOICES = (
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
)
CHOICES = (('1', 'First',), ('2', 'Second',))

def get_permissions():
    app_models_dict = {}

    """
    for app_model in settings.GROUP_PERMISSIONS_MODELS:
        app, model = app_model.split(".")
        app_models_dict.setdefault(app, []).append(model)
    """

    q = Q()

    for app, models in app_models_dict.iteritems():
        q |= Q(content_type__app_label=app, content_type__model__in=models)

    if q:
        return Permission.objects.filter(q)
    else:
        return Permission.objects.all()


def checkAxis(objTypeSelected,objCatalogCrystalSystemSelected,objDataProperty,objCatalogpointgroupSelected,objPuntualgroupnamesSelected):
    propertyDetailValueQuerySet = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected,dataproperty=objDataProperty).values('catalogaxis').annotate(total=Count('catalogaxis'))
    #print propertyDetailValueQuerySet
 
    for d in propertyDetailValueQuerySet:  
        if d['catalogaxis'] != 4:   
            return True
        else:
            return False
    
def setAxis(objTypeSelected,objCatalogCrystalSystemSelected,objDataProperty,objCatalogpointgroupSelected,objPuntualgroupnamesSelected):
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
    for d in propertyDetail:  
        if d['catalogpointgroup'] != 45:  
            return True
        else:
            return False

def checkPuntualGroupNames(objTypeSelected,objCatalogCrystalSystemSelected,dataPropertySelected):        
    propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected,dataproperty=dataPropertySelected).values('puntualgroupnames').annotate(total=Count('puntualgroupnames'))
    for d in propertyDetail:
        if d['puntualgroupnames'] != 21:   
            return True
        else:
            return False    
        
def setPointGroupOfGroups(objTypeSelected,objCatalogCrystalSystemSelected, dataPropertySelected):                                  
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
        puntualGroupNamesQuerySet = PuntualGroupNames.objects.filter(id__in=puntualGroupNamesList).exclude(id=21)
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
        objCatalogPointGroup=CatalogPointGroup.objects.filter(id__exact=d['catalogpointgroup'])         
        for i,obj in  enumerate(objCatalogPointGroup):
            puntualGroupList.append(objCatalogPointGroup[i].id)   
                 
    
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
            
class DataPropertyDetailAdminForm(forms.ModelForm):

    catalogproperty = forms.ModelChoiceField(queryset=None,label="Property")
    type = forms.ModelChoiceField(queryset=None,label="Type")
    dataproperty = forms.ModelChoiceField(queryset=None,label="Data Property")
    catalogcrystalsystem =forms.ModelChoiceField(queryset=None,label="Crystal System")

    
    catalogpointgroup = forms.ModelMultipleChoiceField(
            queryset=None,
            required=False,
            label="Point Group",
            widget=FilteredSelectMultiple(
                verbose_name='Point Group',
                is_stacked=False
            )
    )
    
    
    puntualgroupnames= forms.ModelMultipleChoiceField(
            queryset=None,
            required=False,
            label="Groups",
            widget=FilteredSelectMultiple(
                verbose_name='Groups',
                is_stacked=False
            )
    )
    
    
    axis = forms.ModelMultipleChoiceField(
            queryset=None,
            required=False,
            label="Axis",
            widget=FilteredSelectMultiple(
                verbose_name='Axis',
                is_stacked=False
            )
    )
    
    
    coefficients = forms.ModelMultipleChoiceField(
            queryset=None,
            required=False,
            label="Coefficients",
            widget=FilteredSelectMultiple(
                verbose_name='Name',
                is_stacked=False,
                 
                
            )
        )
    
    
     
    class Meta:
        model = DataPropertyDetail
    
     
    def clean(self,*args,**kwargs):
        puntualgroupnames=self.cleaned_data.get("puntualgroupnames")
        catalogpointgroup=self.cleaned_data.get("catalogpointgroup")
         
        if not catalogpointgroup  and not puntualgroupnames:
            raise forms.ValidationError("the 'Point Group' or 'Groups' fields are not selected, you must select one of the two!")
        
        if  catalogpointgroup  and  puntualgroupnames:
            raise forms.ValidationError("the 'Point Group' or 'Groups' fields have selected options, you must select one of the two!")
            
   
        return super(DataPropertyDetailAdminForm,self).clean(*args,**kwargs)
     
     
        
    def __init__(self, *args, **kwargs):
        print "kwargs"    
        print kwargs    
        typedataproperty = kwargs.pop('instance', None)
        #print args
        if typedataproperty != None:
            try:
 
                if args:
                    if args[0].has_key('_save'):
                        super(DataPropertyDetailAdminForm, self).__init__(*args, **kwargs)
                        id_type = int(args[0]['type'])
                        id_dataproperty = int(args[0]['dataproperty'])
                        id_catalogcrystalsystem= int(args[0]['catalogcrystalsystem'])
                        id_catalogpointgroup=args[0].getlist('catalogpointgroup')
                        id_puntualgroupnames=args[0].getlist('puntualgroupnames')
                       
                        
                        self.fields['catalogproperty'].queryset=CatalogProperty.objects.filter(id=typedataproperty.type.catalogproperty.id)
                        self.fields['catalogproperty'].initial=typedataproperty.type.catalogproperty.id
                        ids=CatalogProperty.objects.filter(id=typedataproperty.type.catalogproperty.id).values_list('id', flat=True) 
     
                        #ids=CatalogProperty.objects.filter(name=typedataproperty.type.catalogproperty.name).values_list('id', flat=True)   
                        typeQuerySet=Type.objects.filter(active=True,id= typedataproperty.type.id)   
                        self.fields['type'].queryset= typeQuerySet
                        self.fields['type'].initial= typedataproperty.type.id
         
                        type_ids=Type.objects.filter(catalogproperty_id__in=ids,active=True, name=typedataproperty.type.name).values_list('id',flat=True)    
                        dataproperty_ids=TypeDataProperty.objects.filter(type_id__in=type_ids).values_list('dataproperty_id',flat=True)    
                        datapropertyQuerySet=Property.objects.filter(id=typedataproperty.dataproperty.id)   
                        self.fields['dataproperty'].queryset=datapropertyQuerySet
                        self.fields['dataproperty'].initial  = typedataproperty.dataproperty.id
                        
                        objCatalogCrystalSystemSelected=CatalogCrystalSystem.objects.get(id=id_catalogcrystalsystem)
                        catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty_id__in=ids)   
                        self.fields['catalogcrystalsystem'].queryset=catalogcrystalsystemQuerySet
                        self.fields['catalogcrystalsystem'].initial=objCatalogCrystalSystemSelected #initialization to first  on the list
                     
                                        
                        objDataProperty = Property.objects.filter(id=typedataproperty.dataproperty.id)   
                        objTypeSelected= typedataproperty.type
                        puntualgroupnamesNone = None
                       
 
                        id_catalogpointgroup=args[0].getlist('catalogpointgroup')
                        print id_catalogpointgroup
                        """***********************catalogpointgroup******************************************"""
                        if checkPointGroup(objTypeSelected,objCatalogCrystalSystemSelected):
                            pass
                            #self.fields['catalogpointgroup'].required = True 
                            
                        catalogpointgroup_ids_to_int =[]    
                        catalogpointgroup_ids =   args[0].getlist('catalogpointgroup')
                        for id in catalogpointgroup_ids:
                            catalogpointgroup_ids_to_int.append(int(id))
                        
                        self.fields['catalogpointgroup'].queryset =CatalogPointGroup.objects.all().exclude(id=45) 
                        if catalogpointgroup_ids_to_int:
                            self.fields['catalogpointgroup'].initial =  CatalogPointGroup.objects.filter(id__in=catalogpointgroup_ids_to_int)
                            
                            
                        id_puntualgroupnames=args[0].getlist('puntualgroupnames')
                        print id_puntualgroupnames
                        """***********************puntualgroupnames******************************************"""
                        if checkPuntualGroupNames(objTypeSelected, objCatalogCrystalSystemSelected):
                            pass
                            #self.fields['puntualgroupnames'].required = True 

                        puntualgroupnames_ids_to_int =[]    
                        puntualgroupnames_ids =   args[0].getlist('puntualgroupnames')
                        for id in puntualgroupnames_ids:
                            puntualgroupnames_ids_to_int.append(int(id))

                        self.fields['puntualgroupnames'].queryset =PuntualGroupNames.objects.all().exclude(id=21)
                        if puntualgroupnames_ids_to_int:
                            self.fields['puntualgroupnames'].initial =  PuntualGroupNames.objects.filter(id__in=puntualgroupnames_ids_to_int)
                        
      
                        
                        """***********************axis******************************************"""
                        if checkAxis(objTypeSelected, objCatalogCrystalSystemSelected):
                            self.fields['axis'].required = True 

                        self.fields['axis'].queryset=CatalogAxis.objects.all().exclude(id=4)
                        
                        axis_ids_to_int =[]    
                        axis_ids =   args[0].getlist('axis')
                        for id in axis_ids:
                            axis_ids_to_int.append(int(id))

                        self.fields['axis'].queryset =CatalogAxis.objects.all().exclude(id=4)
                        if axis_ids_to_int:
                            self.fields['axis'].initial =  CatalogAxis.objects.filter(id__in=axis_ids_to_int)
                            
                            
                            
                        """***********************coefficients******************************************"""    
                         
                        #if checkCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty):
                        self.fields['coefficients'].required = True 

                        checkcoefficients=  checkCoefficients(objTypeSelected, objCatalogCrystalSystemSelected, objDataProperty)
                        #if checkCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty):
                        self.fields['coefficients'].required = True 
                        coefficients_names = []
                        coefficients_ids_to_int =[]    
                        coefficients_ids =   args[0].getlist('coefficients')
                        coefficients_name = []
                        fieldstemp = CatalogPropertyDetailTemp.objects.filter(id__in= coefficients_ids).values('name')
                            

                        if not fieldstemp:
                            for id in coefficients_ids:
                                coefficients_ids_to_int.append(int(id))
                                
                            catalogpropertydetailList=CatalogPropertyDetail.objects.filter(id__in=coefficients_ids_to_int)
                       
    
                            if catalogpropertydetailList:
                                print "reales"
                                self.fields['coefficients'].queryset =CatalogPropertyDetail.objects.filter(type_id =id_type,dataproperty_id=id_dataproperty,crystalsystem_id=id_catalogcrystalsystem) 
                                self.fields['coefficients'].initial = coefficients_ids_to_int
                            else:
                                print "en ninuga de las dos: generar coefficientes"
                                #CatalogPropertyDetailTemp.objects.all().delete()
                                CatalogPropertyDetailTemp.objects.all().delete()
                                #catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty) 
                                catalogpropertydetailtemp = []
                                print axis_ids_to_int
                                if axis_ids_to_int:
                                    for axisid in axis_ids_to_int:
                                        if catalogpointgroup_ids_to_int:
                                            for cpgid in catalogpointgroup_ids_to_int:
                                                catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty) 
                                                for cpd in catalogPropertyDetailList:
                                                    cpdt=CatalogPropertyDetailTemp()
                                                    if checkcoefficients:
                                                        cpdt.name = cpd.name
                                                    else:
                                                        cpdt.name = cpd[1]
                                                    cpdt.type =typedataproperty.type
                                                    cpdt.description = ""
                                                    cpdt.crystalsystem = objCatalogCrystalSystemSelected
                                                    cpdt.dataproperty = typedataproperty.dataproperty
                                                    cpdt.catalogaxis = CatalogAxis.objects.get(id=axisid)
                                                    cpdt.catalogpointgroup = CatalogPointGroup.objects.get(id=cpgid)
                                                    cpdt.puntualgroupnames =PuntualGroupNames.objects.get(id=21)
                                                    catalogpropertydetailtemp.append(cpdt)
                                                    cpdt.save()
                                                    del cpdt
                                        else:
                                            for pgnid in puntualgroupnames_ids_to_int:
                                                catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty) 
                                                for cpd in catalogPropertyDetailList:
                                                    cpdt=CatalogPropertyDetailTemp()
                                                    if checkcoefficients:
                                                        cpdt.name = cpd.name
                                                    else:
                                                        cpdt.name = cpd[1]
                                                    cpdt.type =typedataproperty.type
                                                    cpdt.description = ""
                                                    cpdt.crystalsystem = objCatalogCrystalSystemSelected
                                                    cpdt.dataproperty = typedataproperty.dataproperty
                                                    cpdt.catalogaxis = CatalogAxis.objects.get(id=axisid)
                                                    cpdt.catalogpointgroup= CatalogPointGroup.objects.get(id=45)
                                                    cpdt.puntualgroupnames = PuntualGroupNames.objects.get(id=pgnid) 
                                                    catalogpropertydetailtemp.append(cpdt)
                                                    cpdt.save()
                                                    del cpdt
                                
                                else:
                                    if catalogpointgroup_ids_to_int:
                                        for cpgid in catalogpointgroup_ids_to_int:
                                            catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty) 
                                            for cpd in catalogPropertyDetailList:
                                                cpdt=CatalogPropertyDetailTemp()
                                                if checkcoefficients:
                                                    cpdt.name = cpd.name
                                                else:
                                                    cpdt.name = cpd[1]
                                                cpdt.type =typedataproperty.type
                                                cpdt.description = ""
                                                cpdt.crystalsystem = objCatalogCrystalSystemSelected
                                                cpdt.dataproperty = typedataproperty.dataproperty
                                                cpdt.catalogpointgroup = CatalogPointGroup.objects.get(id=cpgid)
                                                cpdt.puntualgroupnames =PuntualGroupNames.objects.get(id=21)
                                                cpdt.catalogaxis = CatalogAxis.objects.get(id=4)
                                                catalogpropertydetailtemp.append(cpdt)
                                                cpdt.save()
                                                del cpdt
                                    else:
                                        for pgnid in puntualgroupnames_ids_to_int:
                                            catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty) 
                                            for cpd in catalogPropertyDetailList:
                                                cpdt=CatalogPropertyDetailTemp()
                                                if checkcoefficients:
                                                    cpdt.name = cpd.name
                                                else:
                                                    cpdt.name = cpd[1]
                                                    
                                                cpdt.type =typedataproperty.type
                                                cpdt.description = ""
                                                cpdt.crystalsystem = objCatalogCrystalSystemSelected
                                                cpdt.dataproperty = typedataproperty.dataproperty
                                                cpdt.catalogpointgroup= CatalogPointGroup.objects.get(id=45)
                                                cpdt.puntualgroupnames = PuntualGroupNames.objects.get(id=pgnid) 
                                                cpdt.catalogaxis = CatalogAxis.objects.get(id=4)
                                                catalogpropertydetailtemp.append(cpdt)
        
                                                cpdt.save()
                                                del cpdt
                                
 
                                self.fields['coefficients'].queryset = CatalogPropertyDetailTemp.objects.filter(type_id =id_type,dataproperty_id=id_dataproperty,crystalsystem_id=id_catalogcrystalsystem)
                        else:
                            print "consulta temporales"
                            for field in fieldstemp:
                                coefficients_name.append(field['name'])
                            
                            catalogpropertydetailtempQuerySet = CatalogPropertyDetailTemp.objects.filter(name__in=coefficients_name)
                            for i, cpdt in enumerate(catalogpropertydetailtempQuerySet):
                                coefficients_ids_to_int.append(catalogpropertydetailtempQuerySet[i].id)
                                
                            for i, item in enumerate(catalogpropertydetailtempQuerySet):
                                    print catalogpropertydetailtempQuerySet[i].name
                                        
                             
                            
                            self.fields['coefficients'].queryset = catalogpropertydetailtempQuerySet                
                        
 
                        
                        
                        """               
                        else:
                            catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty) 
                            self.fields['coefficients'].choices = catalogPropertyDetailList
                        """

    
                    elif (args[0].has_key('_todo') and args[0]['_todo'] != u''):
                        
                        id_type = int(args[0]['type'])
                        id_dataproperty = int(args[0]['dataproperty'])
                        id_catalogcrystalsystem= int(args[0]['catalogcrystalsystem'])
                        
                        
                        
                        
                        args= {}
                        super(DataPropertyDetailAdminForm, self).__init__(*args, **kwargs)
                        self.fields['catalogproperty'].queryset=CatalogProperty.objects.filter(id=typedataproperty.type.catalogproperty.id)
                        self.fields['catalogproperty'].initial=typedataproperty.type.catalogproperty.id
                        ids=CatalogProperty.objects.filter(id=typedataproperty.type.catalogproperty.id).values_list('id', flat=True) 
     
                        #ids=CatalogProperty.objects.filter(name=typedataproperty.type.catalogproperty.name).values_list('id', flat=True)   
                        typeQuerySet=Type.objects.filter(active=True,id= typedataproperty.type.id)   
                        self.fields['type'].queryset= typeQuerySet
                        self.fields['type'].initial= typedataproperty.type.id
         
                        type_ids=Type.objects.filter(catalogproperty_id__in=ids,active=True, name=typedataproperty.type.name).values_list('id',flat=True)    
                        dataproperty_ids=TypeDataProperty.objects.filter(type_id__in=type_ids).values_list('dataproperty_id',flat=True)    
                        datapropertyQuerySet=Property.objects.filter(id=typedataproperty.dataproperty.id)   
                        self.fields['dataproperty'].queryset=datapropertyQuerySet
                        self.fields['dataproperty'].initial  = typedataproperty.dataproperty.id
                        
                        objCatalogCrystalSystemSelected=CatalogCrystalSystem.objects.get(id=id_catalogcrystalsystem)
                        catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty_id__in=ids)   
                        self.fields['catalogcrystalsystem'].queryset=catalogcrystalsystemQuerySet
                        self.fields['catalogcrystalsystem'].initial=objCatalogCrystalSystemSelected #initialization to first  on the list
                     
                                        
                        objDataProperty = Property.objects.filter(id=typedataproperty.dataproperty.id)   
                        objTypeSelected= typedataproperty.type
                        puntualgroupnamesNone = None
                        
                        catalogpointgroup_ids = []
                        if checkPointGroup(objTypeSelected,objCatalogCrystalSystemSelected):
                            catalogpointgroupList= setPointGroup(objTypeSelected, objCatalogCrystalSystemSelected)
                            puntualgroupnamesNone=PuntualGroupNames.objects.get(id=21)
    
                            none_catalogpointgroupQuerySet=CatalogPointGroup.objects.none()
                            qs = list(chain(none_catalogpointgroupQuerySet, catalogpointgroupList))
                            self.fields['catalogpointgroup'].choices=[(c.id, c.name) for i,c in enumerate(qs)]
                            self.fields['catalogpointgroup'].initial = [(c.id) for i,c in enumerate(qs)] 
                            self.fields['catalogpointgroup'].required = True 
                            
                            for i,c in enumerate(qs):
                                catalogpointgroup_ids.append(c.id)
                                
                        else:
                            print "nada catalogpointgroup"
                            self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all().exclude(id=45)
                            
                        
                        puntualgroupnames_ids =   []
                        catalogpointgroupNone = None
                        if checkPuntualGroupNames(objTypeSelected, objCatalogCrystalSystemSelected):
                            puntualGroupNamesList,catalogpointgroupList=setPointGroupOfGroups(objTypeSelected, objCatalogCrystalSystemSelected)
                            catalogpointgroupNone = CatalogPointGroup.objects.get(id=45)
                            none_puntualgroupnamesQuerySet=PuntualGroupNames.objects.none()
                            qs = list(chain(none_puntualgroupnamesQuerySet, puntualGroupNamesList))
                            self.fields['puntualgroupnames'].choices= [(c.id, c.name) for i,c in enumerate(qs)] #+ [('new stuff', 'new')] for extra choices
                            self.fields['puntualgroupnames'].initial=[(c.id) for i,c in enumerate(qs)] 
                            self.fields['puntualgroupnames'].required = True 
                            
                            for i,c in enumerate(qs):
                                puntualgroupnames_ids.append(c.id)
                                
                        else:
                            print "nada puntualgroupnames"
                            self.fields['puntualgroupnames'].queryset =PuntualGroupNames.objects.all().exclude(id=21)
                            #catalogpointgroup_ids.append(4)
                            
                        axis_ids = []
                        if checkAxis(objTypeSelected, objCatalogCrystalSystemSelected):
                            axisList=setAxis(objTypeSelected, objCatalogCrystalSystemSelected) 
                            none_axisQuerySet=CatalogAxis.objects.none()
                            qs = list(chain(none_axisQuerySet, axisList))
                            self.fields['axis'].choices=[(c.id, c.name) for i,c in enumerate(qs)] 
                            self.fields['axis'].initial = [(c.id) for i,c in enumerate(qs)]
                            self.fields['axis'].required = True
                            
                            for i,c in enumerate(qs):
                                axis_ids.append(c.id)
                             
                        else:
                            print "nada axis"
                            self.fields['axis'].queryset=CatalogAxis.objects.all().exclude(id=4)
                            #axis_ids.append(4)
                            
                         
                        catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty)   
                        if checkCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty):
                            none_catalogpropertydetailQuerySet=CatalogPropertyDetail.objects.none()
                            qs = list(chain(none_catalogpropertydetailQuerySet, catalogPropertyDetailList))
                            self.fields['coefficients'].choices = [(c.id, c.name) for i,c in enumerate(qs)] 
                            self.fields['coefficients'].initial  = [(c.id) for i,c in enumerate(qs)]
                           
                        else:
                            catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty)
                            self.fields['coefficients'].choices = catalogPropertyDetailList

                            """***********************coefficients catalog_property_detail_temp******************************************"""    
                            """
                            coefficients_ids_to_int =[]    
                            for i,item in enumerate(setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty)):
                               coefficients_ids_to_int.append(item[0])
                            """
                           
                           
                            checkcoefficients=  checkCoefficients(objTypeSelected, objCatalogCrystalSystemSelected, objDataProperty)
                            axis_ids_to_int =[]  
                            for id in axis_ids:
                                axis_ids_to_int.append(int(id))

                            catalogpointgroup_ids_to_int = []
                            for id in catalogpointgroup_ids:
                                catalogpointgroup_ids_to_int.append(int(id))
                       
                            puntualgroupnames_ids_to_int = []
                            for id in  puntualgroupnames_ids:
                                puntualgroupnames_ids_to_int.append(int(id))


                            print "temporales"
                            CatalogPropertyDetailTemp.objects.all().delete()
                            #catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty) 
                            catalogpropertydetailtemp = []
                            print axis_ids_to_int
                            if axis_ids_to_int:
                                for axisid in axis_ids_to_int:
                                    if catalogpointgroup_ids_to_int:
                                        for cpgid in catalogpointgroup_ids_to_int:
                                            catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty) 
                                            for cpd in catalogPropertyDetailList:
                                                cpdt=CatalogPropertyDetailTemp()
                                                if checkcoefficients:
                                                    cpdt.name = cpd.name
                                                else:
                                                    cpdt.name = cpd[1]
                                                
                                                cpdt.type =typedataproperty.type
                                                cpdt.description = ""
                                                cpdt.crystalsystem = objCatalogCrystalSystemSelected
                                                cpdt.dataproperty = typedataproperty.dataproperty
                                                cpdt.catalogaxis = CatalogAxis.objects.get(id=axisid)
                                                cpdt.catalogpointgroup = CatalogPointGroup.objects.get(id=cpgid)
                                                cpdt.puntualgroupnames =PuntualGroupNames.objects.get(id=21)
                                                catalogpropertydetailtemp.append(cpdt)
                                                cpdt.save()
                                                del cpdt
                                    else:
                                        for pgnid in puntualgroupnames_ids_to_int:
                                            catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty) 
                                            for cpd in catalogPropertyDetailList:
                                                cpdt=CatalogPropertyDetailTemp()
                                                if checkcoefficients:
                                                    cpdt.name = cpd.name
                                                else:
                                                    cpdt.name = cpd[1]
                                                    
                                                cpdt.type =typedataproperty.type
                                                cpdt.description = ""
                                                cpdt.crystalsystem = objCatalogCrystalSystemSelected
                                                cpdt.dataproperty = typedataproperty.dataproperty
                                                cpdt.catalogaxis = CatalogAxis.objects.get(id=axisid)
                                                cpdt.catalogpointgroup= CatalogPointGroup.objects.get(id=45)
                                                cpdt.puntualgroupnames = PuntualGroupNames.objects.get(id=pgnid) 
                                                catalogpropertydetailtemp.append(cpdt)
                                                cpdt.save()
                                                del cpdt
                            
                            else:
                                if catalogpointgroup_ids_to_int:
                                    for cpgid in catalogpointgroup_ids_to_int:
                                        catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty) 
                                        for cpd in catalogPropertyDetailList:
                                            cpdt=CatalogPropertyDetailTemp()
                                            if checkcoefficients:
                                                cpdt.name = cpd.name
                                            else:
                                                cpdt.name = cpd[1]
                                            cpdt.type =typedataproperty.type
                                            cpdt.description = ""
                                            cpdt.crystalsystem = objCatalogCrystalSystemSelected
                                            cpdt.dataproperty = typedataproperty.dataproperty
                                            cpdt.catalogpointgroup = CatalogPointGroup.objects.get(id=cpgid)
                                            cpdt.puntualgroupnames =PuntualGroupNames.objects.get(id=21)
                                            cpdt.catalogaxis = CatalogAxis.objects.get(id=4)
                                            catalogpropertydetailtemp.append(cpdt)
                                            cpdt.save()
                                            del cpdt
                                else:
                                    for pgnid in puntualgroupnames_ids_to_int:
                                        catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty) 
                                        for cpd in catalogPropertyDetailList:
                                            cpdt=CatalogPropertyDetailTemp()
                                            if checkcoefficients:
                                                cpdt.name = cpd.name
                                            else:
                                                cpdt.name = cpd[1]
                                            cpdt.type =typedataproperty.type
                                            cpdt.description = ""
                                            cpdt.crystalsystem = objCatalogCrystalSystemSelected
                                            cpdt.dataproperty = typedataproperty.dataproperty
                                            cpdt.catalogpointgroup= CatalogPointGroup.objects.get(id=45)
                                            cpdt.puntualgroupnames = PuntualGroupNames.objects.get(id=pgnid) 
                                            cpdt.catalogaxis = CatalogAxis.objects.get(id=4)
                                            catalogpropertydetailtemp.append(cpdt)
    
                                            cpdt.save()
                                            del cpdt
                             
            
                                    
                        
                        #args[0]['_continue'] = 'Save and continue editing'
                    elif args[0].has_key('_continue'):
                        
                        id_type = int(args[0]['type'])
                        id_dataproperty = int(args[0]['dataproperty'])
                        id_catalogcrystalsystem= int(args[0]['catalogcrystalsystem'])
                        
                        super(DataPropertyDetailAdminForm, self).__init__(*args, **kwargs)
                        self.fields['catalogproperty'].queryset=CatalogProperty.objects.filter(id=typedataproperty.type.catalogproperty.id)
                        self.fields['catalogproperty'].initial=typedataproperty.type.catalogproperty.id
                        ids=CatalogProperty.objects.filter(id=typedataproperty.type.catalogproperty.id).values_list('id', flat=True) 
     
                        #ids=CatalogProperty.objects.filter(name=typedataproperty.type.catalogproperty.name).values_list('id', flat=True)   
                        typeQuerySet=Type.objects.filter(active=True,id= typedataproperty.type.id)   
                        self.fields['type'].queryset= typeQuerySet
                        self.fields['type'].initial= typedataproperty.type.id
         
                        type_ids=Type.objects.filter(catalogproperty_id__in=ids,active=True, name=typedataproperty.type.name).values_list('id',flat=True)    
                        dataproperty_ids=TypeDataProperty.objects.filter(type_id__in=type_ids).values_list('dataproperty_id',flat=True)    
                        datapropertyQuerySet=Property.objects.filter(id=typedataproperty.dataproperty.id)   
                        self.fields['dataproperty'].queryset=datapropertyQuerySet
                        self.fields['dataproperty'].initial  = typedataproperty.dataproperty.id
                        
                        objCatalogCrystalSystemSelected=CatalogCrystalSystem.objects.get(id=id_catalogcrystalsystem)
                        catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty_id__in=ids)   
                        self.fields['catalogcrystalsystem'].queryset=catalogcrystalsystemQuerySet
                        self.fields['catalogcrystalsystem'].initial=objCatalogCrystalSystemSelected #initialization to first  on the list
                     
                                        
                        objDataProperty = Property.objects.filter(id=typedataproperty.dataproperty.id)   
                        objTypeSelected= typedataproperty.type
                        puntualgroupnamesNone = None
                       
 
                     
                        """***********************catalogpointgroup******************************************"""
                        if checkPointGroup(objTypeSelected,objCatalogCrystalSystemSelected):
                            self.fields['catalogpointgroup'].required = True 
                            
                        catalogpointgroup_ids_to_int =[]    
                        catalogpointgroup_ids =   args[0].getlist('catalogpointgroup')
                        for id in catalogpointgroup_ids:
                            catalogpointgroup_ids_to_int.append(int(id))
                        
                        self.fields['catalogpointgroup'].queryset =CatalogPointGroup.objects.all().exclude(id=45) 
                        if catalogpointgroup_ids_to_int:
                            self.fields['catalogpointgroup'].initial =  CatalogPointGroup.objects.filter(id__in=catalogpointgroup_ids_to_int)
                            
                            
                        
                        """***********************puntualgroupnames******************************************"""
                        if checkPuntualGroupNames(objTypeSelected, objCatalogCrystalSystemSelected):
                            self.fields['puntualgroupnames'].required = True 

                        puntualgroupnames_ids_to_int =[]    
                        puntualgroupnames_ids =   args[0].getlist('puntualgroupnames')
                        for id in puntualgroupnames_ids:
                            puntualgroupnames_ids_to_int.append(int(id))

                        self.fields['puntualgroupnames'].queryset =PuntualGroupNames.objects.all().exclude(id=21)
                        if puntualgroupnames_ids_to_int:
                            self.fields['puntualgroupnames'].initial =  PuntualGroupNames.objects.filter(id__in=puntualgroupnames_ids_to_int)
                        
      
                        
                        """***********************axis******************************************"""
                        if checkAxis(objTypeSelected, objCatalogCrystalSystemSelected):
                            self.fields['axis'].required = True 

                        self.fields['axis'].queryset=CatalogAxis.objects.all().exclude(id=4)
                        
                        axis_ids_to_int =[]    
                        axis_ids =   args[0].getlist('axis')
                        for id in axis_ids:
                            axis_ids_to_int.append(int(id))

                        self.fields['axis'].queryset =CatalogAxis.objects.all().exclude(id=4)
                        if axis_ids_to_int:
                            self.fields['axis'].initial =  CatalogAxis.objects.filter(id__in=axis_ids_to_int)
                            
                            
                            
                        """***********************coefficients******************************************"""    
                        checkcoefficients=  checkCoefficients(objTypeSelected, objCatalogCrystalSystemSelected, objDataProperty)
                        #if checkCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty):
                        self.fields['coefficients'].required = True 
                        coefficients_names = []
                        coefficients_ids_to_int =[]    
                        coefficients_ids =   args[0].getlist('coefficients')
                        coefficients_name = []
                        fieldstemp = CatalogPropertyDetailTemp.objects.filter(id__in= coefficients_ids).values('name')

                            
                            
                        #print coefficients_ids_to_int
                        #if coefficients_ids_to_int:
                        if not fieldstemp:
                            for id in coefficients_ids:
                                coefficients_ids_to_int.append(int(id))
                                
                            catalogpropertydetailList=CatalogPropertyDetail.objects.filter(id__in=coefficients_ids_to_int)
                       
    
                            if catalogpropertydetailList:
                                print "reales"
                                self.fields['coefficients'].queryset =CatalogPropertyDetail.objects.filter(type_id =id_type,dataproperty_id=id_dataproperty,crystalsystem_id=id_catalogcrystalsystem) 
                                self.fields['coefficients'].initial = coefficients_ids_to_int
                            else:
                                print "en ninuga de las dos: generar coefficientes"
                                #CatalogPropertyDetailTemp.objects.all().delete()
                                CatalogPropertyDetailTemp.objects.all().delete()
                                #catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty) 
                                catalogpropertydetailtemp = []
                                print axis_ids_to_int
                                if axis_ids_to_int:
                                    for axisid in axis_ids_to_int:
                                        if catalogpointgroup_ids_to_int:
                                            for cpgid in catalogpointgroup_ids_to_int:
                                                catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty) 
                                                for cpd in catalogPropertyDetailList:
                                                    cpdt=CatalogPropertyDetailTemp()
                                                    if checkcoefficients:
                                                        cpdt.name = cpd.name
                                                    else:
                                                        cpdt.name = cpd[1]
                                                    cpdt.type =typedataproperty.type
                                                    cpdt.description = ""
                                                    cpdt.crystalsystem = objCatalogCrystalSystemSelected
                                                    cpdt.dataproperty = typedataproperty.dataproperty
                                                    cpdt.catalogaxis = CatalogAxis.objects.get(id=axisid)
                                                    cpdt.catalogpointgroup = CatalogPointGroup.objects.get(id=cpgid)
                                                    cpdt.puntualgroupnames =PuntualGroupNames.objects.get(id=21)
                                                    catalogpropertydetailtemp.append(cpdt)
                                                    cpdt.save()
                                                    del cpdt
                                        else:
                                            for pgnid in puntualgroupnames_ids_to_int:
                                                catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty) 
                                                for cpd in catalogPropertyDetailList:
                                                    cpdt=CatalogPropertyDetailTemp()
                                                    if checkcoefficients:
                                                        cpdt.name = cpd.name
                                                    else:
                                                        cpdt.name = cpd[1]
                                                    cpdt.type =typedataproperty.type
                                                    cpdt.description = ""
                                                    cpdt.crystalsystem = objCatalogCrystalSystemSelected
                                                    cpdt.dataproperty = typedataproperty.dataproperty
                                                    cpdt.catalogaxis = CatalogAxis.objects.get(id=axisid)
                                                    cpdt.catalogpointgroup= CatalogPointGroup.objects.get(id=45)
                                                    cpdt.puntualgroupnames = PuntualGroupNames.objects.get(id=pgnid) 
                                                    catalogpropertydetailtemp.append(cpdt)
                                                    cpdt.save()
                                                    del cpdt
                                
                                else:
                                    if catalogpointgroup_ids_to_int:
                                        for cpgid in catalogpointgroup_ids_to_int:
                                            catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty) 
                                            for cpd in catalogPropertyDetailList:
                                                cpdt=CatalogPropertyDetailTemp()
                                                if checkcoefficients:
                                                    cpdt.name = cpd.name
                                                else:
                                                    cpdt.name = cpd[1]
                                                cpdt.type =typedataproperty.type
                                                cpdt.description = ""
                                                cpdt.crystalsystem = objCatalogCrystalSystemSelected
                                                cpdt.dataproperty = typedataproperty.dataproperty
                                                cpdt.catalogpointgroup = CatalogPointGroup.objects.get(id=cpgid)
                                                cpdt.puntualgroupnames =PuntualGroupNames.objects.get(id=21)
                                                cpdt.catalogaxis = CatalogAxis.objects.get(id=4)
                                                catalogpropertydetailtemp.append(cpdt)
                                                cpdt.save()
                                                del cpdt
                                    else:
                                        for pgnid in puntualgroupnames_ids_to_int:
                                            catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty) 
                                            for cpd in catalogPropertyDetailList:
                                                cpdt=CatalogPropertyDetailTemp()
                                                if checkcoefficients:
                                                    cpdt.name = cpd.name
                                                else:
                                                    cpdt.name = cpd[1]
                                                    
                                                cpdt.type =typedataproperty.type
                                                cpdt.description = ""
                                                cpdt.crystalsystem = objCatalogCrystalSystemSelected
                                                cpdt.dataproperty = typedataproperty.dataproperty
                                                cpdt.catalogpointgroup= CatalogPointGroup.objects.get(id=45)
                                                cpdt.puntualgroupnames = PuntualGroupNames.objects.get(id=pgnid) 
                                                cpdt.catalogaxis = CatalogAxis.objects.get(id=4)
                                                catalogpropertydetailtemp.append(cpdt)
        
                                                cpdt.save()
                                                del cpdt
                                
                                    
                                self.fields['coefficients'].queryset = CatalogPropertyDetailTemp.objects.filter(type_id =id_type,dataproperty_id=id_dataproperty,crystalsystem_id=id_catalogcrystalsystem)
         
                        else:
                            print "consulta temporales"
                            for field in fieldstemp:
                                coefficients_name.append(field['name'])
                            
                            catalogpropertydetailtempQuerySet = CatalogPropertyDetailTemp.objects.filter(name__in=coefficients_name)
                            for i, cpdt in enumerate(catalogpropertydetailtempQuerySet):
                                coefficients_ids_to_int.append(catalogpropertydetailtempQuerySet[i].id)
                                
                            for i, item in enumerate(catalogpropertydetailtempQuerySet):
                                    print catalogpropertydetailtempQuerySet[i].name
                                        
                             
                            
                            self.fields['coefficients'].queryset = catalogpropertydetailtempQuerySet
                                
 
 
                        
                else:
                    
                    super(DataPropertyDetailAdminForm, self).__init__(*args, **kwargs)
                    #catalogpropertyQuerySet=CatalogProperty.objects.filter(id=typedataproperty.type.catalogproperty.id)
                    self.fields['catalogproperty'].queryset=CatalogProperty.objects.filter(id=typedataproperty.type.catalogproperty.id)
                    self.fields['catalogproperty'].initial=typedataproperty.type.catalogproperty.id
                    ids=CatalogProperty.objects.filter(id=typedataproperty.type.catalogproperty.id).values_list('id', flat=True) 
 
                    #ids=CatalogProperty.objects.filter(name=typedataproperty.type.catalogproperty.name).values_list('id', flat=True)   
                    typeQuerySet=Type.objects.filter(active=True,id= typedataproperty.type.id)   
                    self.fields['type'].queryset= typeQuerySet
                    self.fields['type'].initial= typedataproperty.type.id
     
                    type_ids=Type.objects.filter(catalogproperty_id__in=ids,active=True, name=typedataproperty.type.name).values_list('id',flat=True)    
                    dataproperty_ids=TypeDataProperty.objects.filter(type_id__in=type_ids).values_list('dataproperty_id',flat=True)    
                    datapropertyQuerySet=Property.objects.filter(id=typedataproperty.dataproperty.id)   
                    self.fields['dataproperty'].queryset=datapropertyQuerySet
                    self.fields['dataproperty'].initial  = typedataproperty.dataproperty.id
                    
                    
                    catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty_id__in=ids)   
                    self.fields['catalogcrystalsystem'].queryset=catalogcrystalsystemQuerySet
                    self.fields['catalogcrystalsystem'].initial=catalogcrystalsystemQuerySet[0] #initialization to first  on the list
                 
                                    
                    objDataProperty = Property.objects.filter(id=typedataproperty.dataproperty.id)   
                    objTypeSelected= typedataproperty.type
                    puntualgroupnamesNone = None
                    objCatalogCrystalSystemSelected=CatalogCrystalSystem.objects.get(id=catalogcrystalsystemQuerySet[0].id)
                    if checkPointGroup(objTypeSelected,objCatalogCrystalSystemSelected):
                        catalogpointgroupList= setPointGroup(objTypeSelected, objCatalogCrystalSystemSelected)
                        puntualgroupnamesNone=PuntualGroupNames.objects.get(id=21)

                        none_catalogpointgroupQuerySet=CatalogPointGroup.objects.none()
                        qs = list(chain(none_catalogpointgroupQuerySet, catalogpointgroupList))
                        self.fields['catalogpointgroup'].choices=[(c.id, c.name) for i,c in enumerate(qs)]
                        self.fields['catalogpointgroup'].initial = [(c.id) for i,c in enumerate(qs)] 
                    else:
                        print "nada catalogpointgroup"
                        self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all().exclude(id=45)
                        
                        
                    catalogpointgroupNone = None
                    if checkPuntualGroupNames(objTypeSelected, objCatalogCrystalSystemSelected):
                        puntualGroupNamesList,catalogpointgroupList=setPointGroupOfGroups(objTypeSelected, objCatalogCrystalSystemSelected)
                        catalogpointgroupNone = CatalogPointGroup.objects.get(id=45)
                        none_puntualgroupnamesQuerySet=PuntualGroupNames.objects.none()
                        qs = list(chain(none_puntualgroupnamesQuerySet, puntualGroupNamesList))
                        self.fields['puntualgroupnames'].choices= [(c.id, c.name) for i,c in enumerate(qs)] #+ [('new stuff', 'new')] for extra choices
                        self.fields['puntualgroupnames'].initial=[(c.id) for i,c in enumerate(qs)] 
                    else:
                        print "nada puntualgroupnames"
                        self.fields['puntualgroupnames'].queryset =PuntualGroupNames.objects.all().exclude(id=21)
                        
                    
                    if checkAxis(objTypeSelected, objCatalogCrystalSystemSelected):
                        axisList=setAxis(objTypeSelected, objCatalogCrystalSystemSelected) 
           
                        none_axisQuerySet=CatalogAxis.objects.none()
                        qs = list(chain(none_axisQuerySet, axisList))
                        self.fields['axis'].queryset=[(c.id, c.name) for i,c in enumerate(qs)] 
                        self.fields['axis'].initial = [(c.id) for i,c in enumerate(qs)]
                    else:
                        print "nada axis"
                        self.fields['axis'].queryset=CatalogAxis.objects.all().exclude(id=4)
                        
                        
                    catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty)   
                    if checkCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty):
                        none_catalogpropertydetailQuerySet=CatalogPropertyDetail.objects.none()
                        qs = list(chain(none_catalogpropertydetailQuerySet, catalogPropertyDetailList))
                        self.fields['coefficients'].choices = [(c.id, c.name) for i,c in enumerate(qs)] 
                        self.fields['coefficients'].initial  = [(c.id) for i,c in enumerate(qs)]
                        
                         
                    else:
                        catalogPropertyDetailList = setCoefficients(objTypeSelected, objCatalogCrystalSystemSelected,typedataproperty.dataproperty)
                        self.fields['coefficients'].choices = catalogPropertyDetailList

        
            except ObjectDoesNotExist as error:
                print "Message({0}): {1}".format(99, error.message)   
                return  error.message
        else:
            if not args: #it arrives here after _addanother
                try:
                    super(DataPropertyDetailAdminForm, self).__init__(*args, **kwargs) 
                    print "it arrives here after _addanother"
                except ObjectDoesNotExist as error:
                    print "Message({0}): {1}".format(99, error.message)   
                    return  error.message
            else:
                for arg in args:
                    print arg
                    if arg:
                        for item in arg:
                            print item + ":" + str(arg[item] )
                            
                            if arg.has_key('_continue') or arg.has_key('todo') and arg['todo'] != '': #'selectcatalogpropertyChange' or 'selecttypeChange' or 'selectcatalogcrystalsystemChange' or 'selectdatapropertyChange':
                                try:
                                    if arg.has_key('_continue'):
                                        pass
                                    else:
                                        args= {}
                                        
                                    super(DataPropertyDetailAdminForm, self).__init__(*args, **kwargs) 
                                    print "_continue"
                                except ObjectDoesNotExist as error:
                                    print "Message({0}): {1}".format(99, error.message)   
                                    return  error.message   
                    
                            if arg.has_key('_save') :
                                try:
                                    super(DataPropertyDetailAdminForm, self).__init__(*args, **kwargs)
                                    print "_save"
                                except ObjectDoesNotExist as error:
                                    print "Message({0}): {1}".format(99, error.message)   
                                    return  error.message   
     
                            if arg.has_key('_addanother'):
                                try:
                                    super(DataPropertyDetailAdminForm, self).__init__(*args, **kwargs)
                                    print "_addanother"
                                except ObjectDoesNotExist as error:
                                    print "Message({0}): {1}".format(99, error.message)   
                                    return  error.message   
                                
  
            
            
            
class GroupNamesDetailAdminForm(forms.ModelForm):  
    
    class Meta:
        model = GroupNamesDetail
        
 
    def clean(self,*args,**kwargs):
        name=self.cleaned_data.get("name")
        catalogpointgroup=self.cleaned_data.get("catalogpointgroup")
         
        if not catalogpointgroup:
            raise forms.ValidationError("the 'Point Group' field are not selected, you must select one of the two")
        elif len(catalogpointgroup) < 2:
            raise forms.ValidationError("You must select at least two to create the group")

    
        if not name:
            pass
        else:
            try:
                print name
                PuntualGroupNames.objects.get(name__exact=name) 
                raise forms.ValidationError("There is already a group with the selecteds 'puntual groups'. use that group or the group name already exist")
            except ObjectDoesNotExist as error:
                pass
            
        
        return super(GroupNamesDetailAdminForm,self).clean(*args,**kwargs)
    
    """def clean_name(self):
        if self.cleaned_data['name']:
            raise forms.ValidationError("5 Countries can be featured at most!")
        return self.cleaned_data['name']"""
    
    def __init__(self, *args, **kwargs):
        super(GroupNamesDetailAdminForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(label='Groups Name',widget=forms.TextInput(attrs={'size': 40}))
        self.fields['name'].help_text = "enter the name or leave the field blank to autogenerate the name"
        self.fields['name'].required = False 
        
        self.fields['description'] = forms.CharField(label='Groups Description',widget=forms.TextInput(attrs={'size': 40}))
        self.fields['description'].help_text = "enter the description or leave the field blank to autogenerate the description"
        self.fields['description'].required = False 
 
        self.fields['catalogpointgroup'] = forms.ModelMultipleChoiceField(queryset=None,
                                                                                                                        required=False,
                                                                                                                        label="Point Group",
                                                                                                                        widget=FilteredSelectMultiple(
                                                                                                                            verbose_name='Point Group',
                                                                                                                            is_stacked=False
                                                                                                                        ))
       
        if self.instance.pk:#_addanother, _continue, _save from change_form.html when instance exit
            puntualgroupnamesSelected=PuntualGroupNames.objects.get(id=self.instance.id)
            #self.fields['puntualgroupnames'].queryset =PuntualGroupNames.objects.filter(id=self.instance.id)
            #self.fields['puntualgroupnames'].initial = puntualgroupnamesSelected
            self.fields['name'].initial=puntualgroupnamesSelected.name
            self.fields['description'].initial=puntualgroupnamesSelected.description
                
            puntualgroupnamesQuerySet =  PuntualGroupGroups.objects.filter(puntualgroupnames=self.instance)
            catalogpointgroup_ids = []
            for i, pgg in  enumerate(puntualgroupnamesQuerySet):
                catalogpointgroup_ids.append( puntualgroupnamesQuerySet[i].catalogpointgroup.id )
                
            self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()
            catalogpointgroupQuerySet=CatalogPointGroup.objects.filter(id__in=catalogpointgroup_ids)
            self.fields['catalogpointgroup'].initial = catalogpointgroupQuerySet
            
        else:
            if args:# true  (_addanother, _continue, _save)  when instance no exit and and change_form.html  was filled

                puntualgroupnames_name = str(args[0]['name'])
                puntualgroupnames_description = str(args[0]['description'])
                catalogpointgroupids=args[0].getlist('catalogpointgroup')
                catalogpointgroup_ids = []
                for id in catalogpointgroupids:
                    catalogpointgroup_ids.append(int(id))
                
                catalogpointgroupQuerySet= None
                 
                if catalogpointgroupids:
                    self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()
                    catalogpointgroupQuerySet=CatalogPointGroup.objects.filter(id__in=catalogpointgroup_ids)
                    self.fields['catalogpointgroup'].initial = catalogpointgroupQuerySet
                    
                    #puntualgroupgroups=PuntualGroupGroups.objects.filter(catalogpointgroup_id__in =catalogpointgroup_ids ).values('puntualgroupnames').annotate(total=Count('puntualgroupnames')).order_by('puntualgroupnames')
                    #puntualgroupgroups= reduce(lambda qs, pk: qs.filter(catalogpointgroup=pk), catalogpointgroup_ids, PuntualGroupGroups.objects.all())
                    puntualgroupgroups=PuntualGroupGroups.objects.annotate(total=models.Count('catalogpointgroup')).filter(total=len(catalogpointgroup_ids)).filter(catalogpointgroup_id__in =catalogpointgroup_ids ).values('puntualgroupnames').annotate(total=Count('catalogpointgroup')).order_by('catalogpointgroup')
                    print puntualgroupgroups.query   
                    print puntualgroupgroups
                    if not puntualgroupgroups:
                        name = "("
                        if len(puntualgroupnames_name) > 0:
                            self.fields['name'].initial=puntualgroupnames_name
                            self.fields['description'].initial=puntualgroupnames_description
                        else:
                            for i,cpg in enumerate(catalogpointgroupQuerySet):
                                if i == (len( catalogpointgroupQuerySet  ) - 1):
                                    name = name +  catalogpointgroupQuerySet[i].name
                                else:
                                    name = name +  catalogpointgroupQuerySet[i].name  + ", "
                                    
                            name =name + ")"
                            self.fields['name'].initial=name
                            args[0]['name']=name
                            if len(puntualgroupnames_description) > 0:
                                self.fields['description'].initial=puntualgroupnames_description 
                                args[0]['description']=puntualgroupnames_description
                            else:
                                self.fields['description'].initial=name
                                args[0]['description']=name

                    else:
                       
                        puntualgroupnamesSelected=PuntualGroupNames.objects.get(id=int(puntualgroupgroups[0]['puntualgroupnames'])) 
                        self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()
                        args[0]['name']=puntualgroupnamesSelected.name
                else:
         
                    self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()    
            else:#add new form for fill change_form.html 
                self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()
 
 
 
def argsToInt(args,value):
    result = None
    try:
        result= int(args)
    except ValueError:
        result = value
    return result


def argsListToIntList(argsList):
    listInt= []
    try: 
        for id in argsList:
            listInt.append(int(id))
    except ValueError:
        listInt = None
      
    return listInt

def getIdsFromQuerySet(queryset):
    listInt = []
    try: 
        for i,t in enumerate(queryset):
                    listInt.append(queryset[i].id )
    except ValueError:
        listInt = None
        
    return listInt
                    
                    
     
class TensorAdminForm(forms.ModelForm):  
    
    class Meta:
        model = Tensor
        
    def clean(self,*args,**kwargs):
        puntualgroupnames=self.cleaned_data.get("puntualgroupnames")
        catalogpointgroup=self.cleaned_data.get("catalogpointgroup")
        coefficients=self.cleaned_data.get("coefficients") 
 
        if not catalogpointgroup and not puntualgroupnames:
            raise forms.ValidationError("the 'Point Group' or 'Groups' fields are not selected, you must select one of the two!")
        
        if  catalogpointgroup  and  puntualgroupnames:
            if  (catalogpointgroup.id == 45  and  puntualgroupnames.id  != 21 ) or (catalogpointgroup.id  != 45  and  puntualgroupnames.id == 21):
                pass
            elif (catalogpointgroup.id  != 45  and  puntualgroupnames.id == 21):
                pass
            elif (catalogpointgroup.id  != 45  and  puntualgroupnames.id != 21):
                raise forms.ValidationError("the 'Point Group' or 'Groups' fields have selected options, you must select one of the two!")
         
 
   
        return super(TensorAdminForm,self).clean(*args,**kwargs)
    
    
    
    def __init__(self, *args, **kwargs):
        type_id  = None
        dataproperty_id = None
        catalogcrystalsystem_id = None
        catalogpointgroup_id = None
        puntualgroupnames_id  = None
        axis_id  = None
        coefficients_ids =  []
        onchange = False
 
        if args: #(true if edit and save or save an existing instance, when form was changed), false when instance was selected from change list
            
            type_id  = argsToInt(args[0]['type'],None) 
            dataproperty_id =  argsToInt(args[0]['dataproperty'],None)
            catalogcrystalsystem_id =  argsToInt(args[0]['catalogcrystalsystem'],None)
            """catalogpointgroup_id = argsToInt(args[0]['catalogpointgroup'],45)
            puntualgroupnames_id  =  argsToInt(args[0]['puntualgroupnames'],21)
            axis_id  = argsToInt(args[0]['axis'],4)
            coefficients_ids = argsListToIntList(args[0].getlist('coefficients'))"""
  
                
            if not args[0].has_key('_save') and not args[0].has_key('_addanother') and not args[0].has_key('_continue'):    
                args ={}
                onchange = True
                
        super(TensorAdminForm, self).__init__(*args, **kwargs)

        self.fields['type']  =forms.ModelChoiceField(queryset=None,label="Type Tensor")
        self.fields['type'].widget=forms.Select(attrs={"onChange":'submit()'})
        self.fields['type'].empty_label = None
        self.fields['dataproperty']  = forms.ModelChoiceField(queryset=None,label="Data Property")
        self.fields['dataproperty'].widget=forms.Select(attrs={"onChange":'submit()'})
        self.fields['dataproperty'].empty_label = None
        self.fields['catalogcrystalsystem']  = forms.ModelChoiceField(queryset=None,label="Crystal System")
        self.fields['catalogcrystalsystem'].widget=forms.Select(attrs={"onChange":'submit()'})
        self.fields['catalogcrystalsystem'].empty_label = None
        self.fields['catalogpointgroup'] = forms.ModelChoiceField(queryset=None,label="Point Group",required=False)
        self.fields['catalogpointgroup'].widget=forms.Select(attrs={"onChange":'submit()'})
        self.fields['puntualgroupnames'] =  forms.ModelChoiceField(queryset=None,label="Groups",required=False)
        self.fields['puntualgroupnames'].widget=forms.Select(attrs={"onChange":'submit()'})
        self.fields['axis'] =  forms.ModelChoiceField(queryset=None,label="Axis",required=False)
        self.fields['axis'].widget=forms.Select(attrs={"onChange":'submit()'})
        self.fields['coefficients'] = forms.ModelMultipleChoiceField(
            queryset=None,
            required=False,
            label="Coefficients",
            widget=FilteredSelectMultiple(
                verbose_name='Name',
                is_stacked=False,
            )
        )

        self.fields['pointgroup']  =  forms.MultipleChoiceField( label="Group Detail",  widget=SelectMultiple(attrs={'disabled': True}),required=False)

        if self.instance.pk: 
            typeQuerySet=Type.objects.filter(active=True,catalogproperty= self.instance)   
            type_ids = getIdsFromQuerySet(typeQuerySet)
            self.fields['type'].queryset= typeQuerySet
            if args:
                #*******************************type*************************************
                typeSelected = Type.objects.get(id=int(type_id))
                self.fields['type'].initial= typeSelected
                
                #*******************************dataproperty*************************************
                dataproperty_ids=TypeDataProperty.objects.filter(type=typeSelected).values_list('dataproperty_id',flat=True)  
                datapropertyQuerySet=Property.objects.filter(id__in=dataproperty_ids)   
                self.fields['dataproperty'].queryset=datapropertyQuerySet
                datapropertySelected = Property.objects.get(id=int(dataproperty_id))  
                self.fields['dataproperty'].initial  = datapropertySelected
                
                #*******************************catalogcrystalsystem*************************************
                catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty= self.instance)   
                catalogcrystalsystem_ids=CatalogCrystalSystem.objects.filter(catalogproperty= self.instance).values_list('id',flat=True) 
                self.fields['catalogcrystalsystem'].queryset=catalogcrystalsystemQuerySet        
                catalogcrystalsystemSelected = CatalogCrystalSystem.objects.get(id=int(catalogcrystalsystem_id)) 
                
                
            else:
                if onchange:
                    if type_id == None:
                        typeSelected = typeQuerySet[0]
                        self.fields['type'].initial= typeSelected
                    else:
                        #*******************************type*************************************
                        typeSelected = Type.objects.get(id=int(type_id))
                        self.fields['type'].initial= typeSelected
                        #*******************************dataproperty*************************************
                        dataproperty_ids=TypeDataProperty.objects.filter(type=typeSelected).values_list('dataproperty_id',flat=True)    
                        datapropertyQuerySet=Property.objects.filter(id__in=dataproperty_ids)   
                        self.fields['dataproperty'].queryset=datapropertyQuerySet
                        if dataproperty_id in dataproperty_ids:
                            datapropertySelected = Property.objects.get(id=int(dataproperty_id))  
                        else:
                            datapropertySelected = datapropertyQuerySet[0]
                            
                        self.fields['dataproperty'].initial  = datapropertySelected
                        
                        #*******************************catalogcrystalsystem*************************************
                        catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty= self.instance)   
                        catalogcrystalsystem_ids=CatalogCrystalSystem.objects.filter(catalogproperty= self.instance).values_list('id',flat=True) 
                        self.fields['catalogcrystalsystem'].queryset=catalogcrystalsystemQuerySet                          
                        if catalogcrystalsystem_id in catalogcrystalsystem_ids:
                            catalogcrystalsystemSelected = CatalogCrystalSystem.objects.get(id=int(catalogcrystalsystem_id)) 
                        else:
                            catalogcrystalsystemSelected = catalogcrystalsystemQuerySet[0]
 
                      
                        self.fields['catalogcrystalsystem'].initial=catalogcrystalsystemSelected
                        
                        
                        #*******************************catalogpointgroup*************************************
                        
                        #*******************************puntualgroupnames*************************************
                        
                    
                else:
                    typeSelected = typeQuerySet[0]
                    self.fields['type'].initial= typeSelected
                    dataproperty_ids=TypeDataProperty.objects.filter(type=typeSelected).values_list('dataproperty_id',flat=True)    
                    datapropertyQuerySet=Property.objects.filter(id__in=dataproperty_ids)   
                    self.fields['dataproperty'].queryset=datapropertyQuerySet
                    self.fields['dataproperty'].initial  = datapropertyQuerySet[0]
                    catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty= self.instance)   
                    #catalogcrystalsystem_ids=CatalogCrystalSystem.objects.filter(catalogproperty= self.instance).values_list('id',flat=True)   
                    self.fields['catalogcrystalsystem'].queryset=catalogcrystalsystemQuerySet
                    catalogcrystalsystemSelected = catalogcrystalsystemQuerySet[0]
                    self.fields['catalogcrystalsystem'].initial=catalogcrystalsystemSelected
                       

        else:
            if args:#save  new
                catalogproperty_id = str(args[0]['catalogproperty'])
                catalogpointgroupids = None
                if catalogpointgroupids:
                    pass
                else:
                    pass 
            else:#add new
                self.fields['type'].queryset   = Type.objects.all()
                self.fields['dataproperty'].queryset = Property.objects.all()    
                self.fields['catalogcrystalsystem'].queryset=CatalogCrystalSystem.objects.all()       
                self.fields['catalogpointgroup'] = CatalogPointGroup.objects.all()    
                self.fields['puntualgroupnames'] =  PuntualGroupNames.objects.all()    

 
            
        
 
        

        