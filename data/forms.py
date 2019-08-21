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
from django.contrib.admin.widgets import AdminTextInputWidget
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.template.loader import render_to_string

from django.forms.widgets import HiddenInput
from data.Utils import *

from  ctypes import *
from django.http import QueryDict
import json
from collections import defaultdict
from operator import itemgetter
from data.JScriptUtil import *
from django.db.models.query import QuerySet
from django.forms import ModelChoiceField
from data.UtilParserFile import *
from data.ExtractDataFormFieldsUtil import *
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
 
 
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
    
    

def test(*args):
        print args[0]
                    

    
class ValidateAddCaseFormv2(forms.Form):
    title = forms.CharField(required=False,help_text="Enter title." ,label= 'Article Title')
    author = forms.CharField(required=True,help_text="Enter author(s) separated by commas.",label='Author(s)')
    journal = forms.CharField(required=True,help_text="Enter journal.",label='Journal/Book')
    volume = forms.CharField(required=False,help_text="Enter volume.",label='Volume',initial='')
    year = forms.CharField(required=True,help_text="Enter year.",label='Year',initial='')
    page_first = forms.CharField(required=False,help_text="Enter page.",label='First page',initial='')
    page_last = forms.CharField(required=False,help_text="Enter page.",label='Last page',initial='')
    

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
           
            if page_first:
                int(page_first)
                pass
        except ValueError:
            raise forms.ValidationError(u'Page first "%s" is not a valid value.' % page_first)
        
    def clean_page_last(self):
        page_last = self.cleaned_data['page_last']
        try:
            if page_last:
                int(page_last)
                pass
        except ValueError:
            raise forms.ValidationError(u'Page last "%s" is not a valid value.' % page_last)
      
      
     
  
    def __init__(self, *args, **kwargs):
        if 'inputList' not in kwargs:
            pass
        else:
            
            if args:
                #print  kwargs.pop('inputList') 
                inputList = kwargs.pop('inputList')  
                ar = []  
                if inputList:
                    dict = { }
                    for key, value in args[0].items():
                        dict[key] = value

                    for ipt  in inputList:
                        if  dict.has_key(ipt.name):
                            val= argsToFloat(args,ipt.name) 
                            if val != None:
                                dict[ipt.name] = val
                             
 
                    argsupdate = QueryDict('', mutable=True)
                    argsupdate.update(dict)
                    ar.append(argsupdate)
                    args = ar
                
                super(ValidateAddCaseFormv2, self).__init__(*args, **kwargs)

                if inputList:
                    for ipt  in inputList:  
                        self.fields[ ipt.name] = forms.FloatField(forms.CharField(required=True,help_text=str(ipt.name) + "Enter value" ,label= ipt.name))
                        #self.fields[ipt.name].initial = 'nnn'


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

        """
        if not name:
            pass
        else:
            try:
                print name
                PointGroupNames.objects.get(name__exact=name) 
                raise forms.ValidationError("There is already a group with the selecteds 'point groups'. use that group or the group name already exist")
            except ObjectDoesNotExist as error:
                pass
        """
            
        
        return super(GroupNamesDetailAdminForm,self).clean(*args,**kwargs)
    
    """def clean_name(self):
        return self.cleaned_data['name']"""
    
    
    def clean_catalogpointgroup(self):
        return self.cleaned_data['catalogpointgroup']
    
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
            if args:
                pointgroupnamesSelected=PointGroupNames.objects.get(id=self.instance.id)
                pointgroupnamesQuerySet =  PointGroupGroups.objects.filter(pointgroupnames=self.instance)
                catalogpointgroup_ids = argsListToIntList(args,'catalogpointgroup')
                catalogpointgroupQuerySet=CatalogPointGroup.objects.filter(id__in=catalogpointgroup_ids)
                name = "("
                for i,cpg in enumerate(catalogpointgroupQuerySet):
                    if i == (len( catalogpointgroupQuerySet  ) - 1):
                        name = name +  catalogpointgroupQuerySet[i].name
                    else:
                        name = name +  catalogpointgroupQuerySet[i].name  + ", "
                            
                name =name + ")"

                self.fields['name'].initial=name
                self.fields['description'].initial=name
                args[0]['name']=name
                args[0]['description']=name    
                self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()
                self.fields['catalogpointgroup'].initial = catalogpointgroupQuerySet
            else:
                catalogpointgroup_ids =  PointGroupGroups.objects.filter(pointgroupnames=self.instance).values_list('catalogpointgroup_id',flat=True)  
                catalogpointgroupQuerySet=CatalogPointGroup.objects.filter(id__in=catalogpointgroup_ids)
                self.fields['name'].initial=self.instance.name
                self.fields['description'].initial=self.instance.name   
                self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()
                self.fields['catalogpointgroup'].initial = catalogpointgroupQuerySet    
        else:
            if args:# true  (_addanother, _continue, _save)  when instance no exit and and change_form.html  was filled

                pointgroupnames_name = str(args[0]['name'])
                pointgroupnames_description = str(args[0]['description'])
                catalogpointgroupids=args[0].getlist('catalogpointgroup')
                catalogpointgroup_ids = []
                for id in catalogpointgroupids:
                    catalogpointgroup_ids.append(int(id))
                
                catalogpointgroupQuerySet= None
                 
                if catalogpointgroupids:
                    self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()
                    catalogpointgroupQuerySet=CatalogPointGroup.objects.filter(id__in=catalogpointgroup_ids)
                    self.fields['catalogpointgroup'].initial = catalogpointgroupQuerySet
                    
 
                    pointgroupgroups=PointGroupGroups.objects.annotate(total=models.Count('catalogpointgroup')).filter(total=len(catalogpointgroup_ids)).filter(catalogpointgroup_id__in =catalogpointgroup_ids ).values('pointgroupnames').annotate(total=Count('catalogpointgroup')).order_by('catalogpointgroup')
                    print pointgroupgroups.query   
                    print pointgroupgroups
                    if not pointgroupgroups:
                        name = "("
                        if len(pointgroupnames_name) > 0:
                            self.fields['name'].initial=pointgroupnames_name
                            self.fields['description'].initial=pointgroupnames_description
                        else:
                            for i,cpg in enumerate(catalogpointgroupQuerySet):
                                if i == (len( catalogpointgroupQuerySet  ) - 1):
                                    name = name +  catalogpointgroupQuerySet[i].name
                                else:
                                    name = name +  catalogpointgroupQuerySet[i].name  + ", "
                                    
                            name =name + ")"
                            self.fields['name'].initial=name
                            args[0]['name']=name
                            if len(pointgroupnames_description) > 0:
                                self.fields['description'].initial=pointgroupnames_description 
                                args[0]['description']=pointgroupnames_description
                            else:
                                self.fields['description'].initial=name
                                args[0]['description']=name

                    else:
                       
                        pointgroupnamesSelected=PointGroupNames.objects.get(id=int(pointgroupgroups[0]['pointgroupnames'])) 
                        self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()
                        args[0]['name']=pointgroupnamesSelected.name
                else:
         
                    self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()    
            else:#add new form for fill change_form.html 
                self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()
 

    
class AddressFieldWidget(AdminTextInputWidget):
    def render(self, name, value, attrs=None):
        html = super(AddressFieldWidget, self).render(name, value, attrs)
        html =  html +  force_unicode( """  <input type="button" value="GeoCode" class="getgeo btn"><br><br><label>Map</label><div id="gmap">This is for map rendering</div>""") 
        return mark_safe(html)  
    
class DetailFieldWidget(AdminTextInputWidget):
    def render(self, name, value, attrs=None):
        html = super(DetailFieldWidget, self).render(name, value, attrs)
        if value:
            pass
        else:
            value = ""    
            
        html =   force_unicode( """    <div class='results' id='"""+attrs['id'] +"""'>"""+ value + """</div>""") 
        return mark_safe(html)  
    
    
class HiddenFieldWidget(AdminTextInputWidget):
    def render(self, name, value, attrs=None):
        html = super(HiddenFieldWidget, self).render(name, value, attrs)
        if value:
            pass
        else:
            value = ""    
            "<input type='hidden' name='datafile' value='" + str(value) +"' />"
        #html =   force_unicode( """    <div style='display:none' id='"""+str(attrs['id']) +"""'>"""+ str(value) + """</div>""") 
        html =   force_unicode( """    <div style='display:none' >"""+ "<input type='hidden' name='datafile' value='" + str(value) +"' />" + """</div>""") 
        return mark_safe(html)  

     
class TensorAdminForm(forms.ModelForm):  
    
    class Meta:
        model = Tensor
 
        
    def clean(self,*args,**kwargs):
         
        pointgroupnames=self.cleaned_data.get("pointgroupnames")
        catalogpointgroup=self.cleaned_data.get("catalogpointgroup")
        coefficients=self.cleaned_data.get("coefficients") 
 
        if not catalogpointgroup and not pointgroupnames:
            raise forms.ValidationError("the 'Point Group' or 'Groups' fields are not selected, you must select one of the two!")
        
        if  catalogpointgroup  and  pointgroupnames:
            if  (catalogpointgroup.id == 45  and  pointgroupnames.id  != 21 ) or (catalogpointgroup.id  != 45  and  pointgroupnames.id == 21):
                pass
            elif (catalogpointgroup.id  != 45  and  pointgroupnames.id == 21):
                pass
            elif (catalogpointgroup.id  != 45  and  pointgroupnames.id != 21):
                raise forms.ValidationError("the 'Point Group' or 'Groups' fields have selected options, you must select one of the two!")
         
 
   
        return super(TensorAdminForm,self).clean(*args,**kwargs)
    
    def clean_pointgroupnames(self):
        pointgroupnames = self.cleaned_data['pointgroupnames']
        
        return pointgroupnames
    
    def clean_catalogpointgroup(self):
        catalogpointgroup = self.cleaned_data['catalogpointgroup']
        
        return catalogpointgroup
    
    def get_alert_types(self,catalogpropertydetail_id):
        """
        Creates a tuple structure of the alert types grouped by event types
        suitable for the choices of a MultipleChoiceField with optgroups
        [
          (event_type, [(alert_type, alert_type), (alert_type, alert_type)]),
          (event_type, [(alert_type, alert_type), (alert_type, alert_type)])
        ]
        """
        alert_types = defaultdict(list)
        for keyNotationCatalogPropertyDetail in KeyNotationCatalogPropertyDetail.objects.filter(catalogpropertydetail_id=catalogpropertydetail_id):
            alert_types[keyNotationCatalogPropertyDetail.keynotation.description].append(
                (keyNotationCatalogPropertyDetail.catalogpropertydetail.id, keyNotationCatalogPropertyDetail.target))
    
        return sorted(alert_types.items(), key=itemgetter(0))
    
    

    def __init__(self, *args, **kwargs):
        type_id  = None
        dataproperty_id = None
        catalogcrystalsystem_id = None
        catalogpointgroup_id = None
        pointgroupnames_id  = None
        axis_id  = None
        coefficients_ids =  []
        onchange = False
        
        
 
        try:
            if args: #(true if edit and save or save an existing instance, when form was changed), false when instance was selected from change list
                
                type_id  = argsToInt(args,'type') 
                dataproperty_id =  argsToInt(args,'dataproperty')
                catalogcrystalsystem_id =  argsToInt(args,'catalogcrystalsystem')
                catalogpointgroup_id = argsToInt(args,'catalogpointgroup',45)
                pointgroupnames_id  =  argsToInt(args,'pointgroupnames',21)
                axis_id  = argsToInt(args,'axis',4)
                coefficients_ids = argsListToIntList(args,'coefficients')
      
                 
                
                   
                if not args[0].has_key('_save') and not args[0].has_key('_addanother') and not args[0].has_key('_continue'):    
                    args ={}
                    onchange = True
                    
            super(TensorAdminForm, self).__init__(*args, **kwargs)
            """"f = self.fields.get('type', None)
            if f is not None:
                f.queryset = f.queryset
            """
    
            self.fields['type']  =forms.ModelChoiceField(queryset=None,label="Type Tensor")
            self.fields['type'].widget=forms.Select(attrs={"onChange":'submit()'})
            self.fields['type'].empty_label = None
            self.fields['dataproperty']  = forms.ModelChoiceField(queryset=None,label="Data Property")
            self.fields['dataproperty'].widget=forms.Select(attrs={"onChange":'submit()'})
            self.fields['dataproperty'].empty_label = None
            self.fields['catalogcrystalsystem']  = forms.ModelChoiceField(queryset=None,label="Crystal System")
            self.fields['catalogcrystalsystem'].widget=forms.Select(attrs={"onChange":'submit()'})
            self.fields['catalogcrystalsystem'].empty_label = None
            self.fields['catalogpointgroup'] = forms.ModelChoiceField(queryset=None,label="Point Group",required=True)
            self.fields['catalogpointgroup'].widget=forms.Select(attrs={"onChange":'submit()'})
            self.fields['catalogpointgroup'].empty_label = None
            self.fields['pointgroupnames'] =  forms.ModelChoiceField(queryset=None,label="Groups",required=True)
            self.fields['pointgroupnames'].widget=forms.Select(attrs={"onChange":'submit()'})
            self.fields['pointgroupnames'].empty_label = None
            self.fields['axis'] =  forms.ModelChoiceField(queryset=None,label="Axis",required=False)
            self.fields['axis'].widget=forms.Select(attrs={"onChange":'submit()'})
            self.fields['axis'].empty_label = None
            self.fields['coefficients'] = forms.ModelMultipleChoiceField(
                queryset=None,
                required=False,
                label="Coefficients",
                widget=FilteredSelectMultiple(
                    verbose_name='Name',
                    is_stacked=False,
                )
                                                                  
            )
            
    
            
            #self.fields['coefficientsrules']  =forms.ModelMultipleChoiceField(queryset=None,label="Coefficients for capture",required=False)
            
            self.fields['coefficientsrules']  =forms.ModelMultipleChoiceField(queryset=None,label="Coefficients for capture",required=False)
            self.fields['keynotation']  =forms.ModelMultipleChoiceField(queryset=None,label="Rules",required=False)
            self.fields['zerocomponent']  =forms.ModelMultipleChoiceField(queryset=None,label="Destination value ",required=False)
            
     
     
    
            #self.fields['crysralsystemdetail'] = forms.CharField(label='Crystal System Detail',widget = DetailFieldWidget, required=False)
            self.fields['pointgroupdetail'] = forms.CharField(label='Point Group Detail',widget = DetailFieldWidget, required=False)
            self.fields['pointgroupnamesdetail'] = forms.CharField(label='Groups Detail',widget = DetailFieldWidget, required=False)
            self.fields['axisdetail'] = forms.CharField(label='Axis Detail',widget = DetailFieldWidget, required=False) 
            self.fields['errormessage'] = forms.CharField(widget = DetailFieldWidget, required=False)
            
             
            self.fields['jquery'] = forms.CharField(label='',widget = DetailFieldWidget, required=False) 
            #self.fields['jquery'].empty_label = None
            
            self.fields['detailrules'] = forms.CharField(label='Detail rules',widget = DetailFieldWidget, required=False) 
            
            
     
           
     
             
      
            typeSelected = None
            datapropertySelected = None
            catalogcrystalsystemSelected = None
            catalogpointgroupSelected = None
            pointgroupnamesSelected = None
            axisSelected = None
            if self.instance.pk: 
                typeQuerySet=Type.objects.filter(active=True,catalogproperty= self.instance)   
                if not typeQuerySet:
                    typeQuerySet=Type.objects.filter(active=False,catalogproperty= self.instance)                  
                    self.fields['errormessage'].label='Error Message'
                    self.fields['errormessage'].initial = "<strong><font color='red'>" + self.instance.description +" is disabled</font></strong>"
                    #raise  forms.ValidationError("the 'Point Group' field are not selected, you must select one of the two")
                else:
                    self.fields['errormessage'].label='' 
                    
           
                type_ids = getIdsFromQuerySet(typeQuerySet)
                self.fields['type'].queryset= typeQuerySet
                if args:
                    #*******************************type*************************************
                    typeSelected = Type.objects.get(id=int(type_id))
                    self.fields['type'].initial= typeSelected
                    
                    #*******************************dataproperty*************************************
                    dataproperty_ids=TypeDataProperty.objects.filter(type=typeSelected).values_list('dataproperty_id',flat=True)  
                    datapropertyQuerySet=Property.objects.filter(id__in=dataproperty_ids, active=True)   
                    self.fields['dataproperty'].queryset=datapropertyQuerySet
                    datapropertySelected = Property.objects.get(id=int(dataproperty_id), active=True)  
                    self.fields['dataproperty'].initial  = datapropertySelected
                    
                    #*******************************catalogcrystalsystem*************************************
                    catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty= self.instance)   
                    catalogcrystalsystem_ids=CatalogCrystalSystem.objects.filter(catalogproperty= self.instance).values_list('id',flat=True) 
                    self.fields['catalogcrystalsystem'].queryset=catalogcrystalsystemQuerySet        
                    catalogcrystalsystemSelected = CatalogCrystalSystem.objects.get(id=int(catalogcrystalsystem_id)) 
                    
                    #*******************************catalogpointgroup*************************************
                    
                    catalogpointgroupSelected = CatalogPointGroup.objects.get(id=int(catalogpointgroup_id))
                    self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()
                    self.fields['catalogpointgroup'].initial = catalogpointgroupSelected
                    self.fields['pointgroupdetail'].initial = "<strong>punctual group assigned</strong>"
                    
                    
                    #*******************************pointgroupnames*************************************
                    pointgroupnamesSelected = PointGroupNames.objects.get(id=int(pointgroupnames_id))  
                    self.fields['pointgroupnames'].queryset = PointGroupNames.objects.all()
                    self.fields['pointgroupnames'].initial = pointgroupnamesSelected
                    self.fields['pointgroupnamesdetail'].initial = "<strong>groups assigned</strong>"
                    
                    #*******************************axis*************************************
                    axisSelected = CatalogAxis.objects.get(id=int(axis_id))  
                    self.fields['axis'].queryset = PointGroupNames.objects.all()
                    self.fields['axis'].initial = pointgroupnamesSelected
                    self.fields['axisdetail'].initial = "<strong>axis assigned</strong>"
                    
                    
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
                            datapropertyQuerySet=Property.objects.filter(id__in=dataproperty_ids, active=True)   
                            self.fields['dataproperty'].queryset=datapropertyQuerySet
                            if dataproperty_id in dataproperty_ids:
                                datapropertySelected = Property.objects.get(id=int(dataproperty_id), active=True)  
                            else:
                                datapropertySelected = datapropertyQuerySet[0]
                                
                            self.fields['dataproperty'].initial  = datapropertySelected
                            
                            #*******************************catalogcrystalsystem*************************************
                            catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty= self.instance)   
                            catalogcrystalsystemidList = []
                            for i, crystalsystem in enumerate(catalogcrystalsystemQuerySet):
                                try:     
                                    crystalsystemtype=CrystalSystemType.objects.get(catalogcrystalsystem=crystalsystem,type=typeSelected, active=True)
                                    catalogcrystalsystemidList.append(crystalsystemtype.catalogcrystalsystem.id)
                                except ObjectDoesNotExist as error:
                                    print "Message({0}): {1}".format(99, error.message) 
                                    
                                    
                            
                            if catalogcrystalsystemidList:
                                catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty= self.instance,id__in =catalogcrystalsystemidList)  
                            else:
                                catalogcrystalsystemQuerySet = None
                            
                            if catalogcrystalsystemQuerySet:
                                catalogcrystalsystem_ids=CatalogCrystalSystem.objects.filter(catalogproperty= self.instance).values_list('id',flat=True) 
                                self.fields['catalogcrystalsystem'].queryset=catalogcrystalsystemQuerySet                          
                                if catalogcrystalsystem_id in catalogcrystalsystem_ids:
                                    catalogcrystalsystemSelected = CatalogCrystalSystem.objects.get(id=int(catalogcrystalsystem_id)) 
                                else:
                                    catalogcrystalsystemSelected = catalogcrystalsystemQuerySet[0]
                            else:
                                catalogcrystalsystemSelected = CatalogCrystalSystem()
                                self.fields['catalogcrystalsystem'].help_text = "crystal system not assigned" 
                                #self.fields['crysralsystemdetail'].initial = html
      
                          
                            self.fields['catalogcrystalsystem'].initial=catalogcrystalsystemSelected
                            
                            
                            #*******************************catalogpointgroup*************************************
                            catalogpointgroup_ids= CrystalSystemPointGroup.objects.filter(catalogcrystalsystem=catalogcrystalsystemSelected,type=typeSelected,active=1).values_list('catalogpointgroup_id',flat=True)  
                            if catalogpointgroup_ids:
                                pointgroupQuerySet = CatalogPointGroup.objects.filter(id__in=catalogpointgroup_ids)
                            
                                """if checkPointGroup(typeSelected, catalogcrystalsystemSelected,datapropertySelected):  
                                pointgroupQuerySet = setPointGroup(typeSelected, catalogcrystalsystemSelected,datapropertySelected)
                                catalogpointgroup_ids = getIdsFromQuerySet(pointgroupQuerySet)"""
                                
                                fieldList = ['name','description']
                                html = getTableHTMLFromQuerySet(pointgroupQuerySet)
                                if catalogpointgroup_id in catalogpointgroup_ids:
                                    catalogpointgroupSelected = CatalogPointGroup.objects.get(id=int(catalogpointgroup_id))
                                    self.fields['pointgroupdetail'].initial = html
                                else:
                                    catalogpointgroupSelected = pointgroupQuerySet[0]
                                    self.fields['catalogpointgroup'].help_text = "punctual group not assigned" 
                                    self.fields['pointgroupdetail'].initial = html
                                    
                                    
                                self.fields['catalogpointgroup'].queryset = pointgroupQuerySet
                                self.fields['catalogpointgroup'].initial = catalogpointgroupSelected
                            else:
                                """pointgroupQuerySet=CatalogPointGroup.objects.filter(id=45)
                                self.fields['catalogpointgroup'].queryset = pointgroupQuerySet
                                
                                catalogpointgroup_ids =CatalogPointGroup.objects.all().values_list('id',flat=True) 
                                if catalogpointgroup_id in catalogpointgroup_ids:
                                    catalogpointgroupSelected = CatalogPointGroup.objects.get(id=catalogpointgroup_id)
                                else:
                                    catalogpointgroupSelected = CatalogPointGroup.objects.get(id=45)
                                    
                                self.fields['catalogpointgroup'].initial = catalogpointgroupSelected
                                self.fields['pointgroupdetail'].initial = "<strong>punctual group not assigned</strong>"
                                """
                                
                                pointgroupQuerySet=CatalogPointGroup.objects.filter(id=45)
                                self.fields['catalogpointgroup'].queryset = pointgroupQuerySet
                                catalogpointgroupSelected = CatalogPointGroup.objects.get(id=45)
                                self.fields['catalogpointgroup'].initial = catalogpointgroupSelected
                                self.fields['pointgroupdetail'].initial = "<strong>punctual group not assigned</strong>"
                                
    
    
                            
                            #*******************************pointgroupnames*************************************
                            pointgroupnames_ids= CrystalSystemPointGroupNames.objects.filter(catalogcrystalsystem=catalogcrystalsystemSelected,type=typeSelected,active=1).values_list('pointgroupnames_id',flat=True)  
                            if pointgroupnames_ids:
                                pointgroupnamesQuerySet = PointGroupNames.objects.filter(id__in=pointgroupnames_ids)
                                """if checkPointGroupNames(typeSelected, catalogcrystalsystemSelected,datapropertySelected):
                                pointgroupnamesQuerySet,pointGroupsQuerySet =setPointGroupNames(typeSelected, catalogcrystalsystemSelected,datapropertySelected)
                                pointgroupnames_ids = getIdsFromQuerySet(pointgroupnamesQuerySet)"""
                                
                                fieldsList = ['name','description']
                                html = getTableHTMLFromQuerySet(pointgroupnamesQuerySet,fields=fieldsList)
                                if pointgroupnames_id in pointgroupnames_ids:
                                    pointgroupnamesSelected = PointGroupNames.objects.get(id=int(pointgroupnames_id))  
                                    self.fields['pointgroupnamesdetail'].initial = html
                                    self.fields['pointgroupnames'].help_text = "Group assigned,  all the point groups of this crystal system have the same matrix" 
                                else:
                                    pointgroupnamesSelected =pointgroupnamesQuerySet[0]  
                                    self.fields['pointgroupnamesdetail'].initial = html
                                    self.fields['pointgroupnames'].help_text = "Groups not assigned, Select this option if all groups of points in this crystal system have the same matrix" 
    
                                self.fields['pointgroupnames'].queryset = pointgroupnamesQuerySet
                                self.fields['pointgroupnames'].initial = pointgroupnamesSelected
                                
                            else:
                                """pointGroupNamesQuerySet = PointGroupNames.objects.filter(id=21)
                                self.fields['pointgroupnames'].queryset = pointGroupNamesQuerySet
                                
                                pointgroupnames_ids =PointGroupNames.objects.all().values_list('id',flat=True) 
                                pointgroupnamesSelected = PointGroupNames.objects.get(id=int(pointgroupnames_id))  
                                if pointgroupnames_id in pointgroupnames_ids:
                                    pointgroupnamesSelected = PointGroupNames.objects.get(id=int(pointgroupnames_id))  
                                else:
                                    pointgroupnamesSelected = PointGroupNames.objects.get(id=21)
                                 
                                self.fields['pointgroupnames'].initial = pointgroupnamesSelected
                                self.fields['pointgroupnamesdetail'].initial = "<strong>Group not assigned</strong>"
                                """
                                
                                pointGroupNamesQuerySet = PointGroupNames.objects.filter(id=21)
                                self.fields['pointgroupnames'].queryset = pointGroupNamesQuerySet
                                self.fields['pointgroupnames'].help_text = "Select this option if all groups of points in this crystal system have the same matrix" 
                                pointgroupnamesSelected = PointGroupNames.objects.get(id=21)
                                self.fields['pointgroupnames'].initial = pointgroupnamesSelected
                                self.fields['pointgroupnamesdetail'].initial = "<strong>groups not assigned</strong>"
                                
                          
                            
                            
                            #*******************************axis*************************************
                            axis_ids= CrystalSystemAxis.objects.filter(catalogcrystalsystem=catalogcrystalsystemSelected,type=typeSelected,catalogpointgroup= catalogpointgroupSelected,pointgroupnames = pointgroupnamesSelected,active=1).values_list('axis_id',flat=True)  
                            if axis_ids:
                                axisQuerySet = CatalogAxis.objects.filter(id__in=axis_ids)
                                fieldsList = ['name','description']
                                html = getTableHTMLFromQuerySet(axisQuerySet,fields=fieldsList)
                                print axis_ids
                                print axis_id
                                if axis_id in axis_ids:
                                    axisSelected = CatalogAxis.objects.get(id=int(axis_id))  
                                    self.fields['axisdetail'].initial = html
                                    self.fields['axis'].help_text = "<strong>axis assigned</strong>" 
                                else:
                                    axisSelected = axisQuerySet[0]
                                    self.fields['axisdetail'].initial = html
                                    self.fields['axis'].help_text = "<strong>axis not assigned</strong>" 
                                    
                                self.fields['axis'].queryset =   axisQuerySet
                                self.fields['axis'].initial = axisSelected
                            else:
                                axisQuerySet=  CatalogAxis.objects.filter(id=4) 
                                self.fields['axis'].queryset = axisQuerySet
                                self.fields['axis'].help_text = "Axis not assigned"
                                axisSelected = CatalogAxis.objects.get(id=4)
                                self.fields['axis'].initial = axisSelected
                                self.fields['axisdetail'].initial = "<strong>axis not assigneds</strong>"
                                
                            
                        
                    else:
                        typeSelected = typeQuerySet[0]
                        self.fields['type'].initial= typeSelected
                        
                        #*******************************dataproperty*************************************
                        dataproperty_ids=TypeDataProperty.objects.filter(type=typeSelected).values_list('dataproperty_id',flat=True)    
                        datapropertyQuerySet=Property.objects.filter(id__in=dataproperty_ids, active=True)   
                        self.fields['dataproperty'].queryset=datapropertyQuerySet
                        if datapropertyQuerySet:
                            datapropertySelected = datapropertyQuerySet[0]
                            self.fields['dataproperty'].initial  = datapropertySelected
                        
                        
                        #*******************************catalogcrystalsystem*************************************
                        catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty= self.instance)   
                        catalogcrystalsystemidList = []
                        for i, crystalsystem in enumerate(catalogcrystalsystemQuerySet):
                            try:     
                                crystalsystemtype=CrystalSystemType.objects.get(catalogcrystalsystem=crystalsystem,type=typeSelected)
                                if crystalsystemtype.active == True:
                                    catalogcrystalsystemidList.append(crystalsystemtype.catalogcrystalsystem.id)
                            except ObjectDoesNotExist as error:
                                print "Message({0}): {1}".format(99, error.message) 
                                
                        
                        if catalogcrystalsystemidList:
                            catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty= self.instance,id__in =catalogcrystalsystemidList)  
                        else:
                            catalogcrystalsystemQuerySet = None
                        
                        if catalogcrystalsystemQuerySet:
                            self.fields['catalogcrystalsystem'].queryset=catalogcrystalsystemQuerySet
                            catalogcrystalsystemSelected = catalogcrystalsystemQuerySet[0]
                            self.fields['catalogcrystalsystem'].initial=catalogcrystalsystemSelected
                        else:
                            self.fields['catalogcrystalsystem'].queryset=CatalogCrystalSystem.objects.all()
                            catalogcrystalsystemSelected = CatalogCrystalSystem.objects.all()[0]
                            self.fields['catalogcrystalsystem'].initial=catalogcrystalsystemSelected
    
                        #*******************************catalogpointgroup*************************************
                        
                        catalogpointgroup_ids= CrystalSystemPointGroup.objects.filter(catalogcrystalsystem=catalogcrystalsystemSelected,type=typeSelected,active=1).values_list('catalogpointgroup_id',flat=True)  
                        if catalogpointgroup_ids:
                            pointgroupQuerySet = CatalogPointGroup.objects.filter(id__in=catalogpointgroup_ids)
                            catalogpointgroupSelected = pointgroupQuerySet[0]
                            self.fields['catalogpointgroup'].queryset = pointgroupQuerySet
                            self.fields['catalogpointgroup'].initial = catalogpointgroupSelected
                            
                            fieldsList = ['name','description']
                            html = getTableHTMLFromQuerySet(pointgroupQuerySet,fields=fieldsList)
                                        
                            self.fields['pointgroupdetail'].initial = html
                        else:
                            pointgroupQuerySet=CatalogPointGroup.objects.filter(id=45)
                            self.fields['catalogpointgroup'].queryset = pointgroupQuerySet
                            catalogpointgroupSelected = CatalogPointGroup.objects.get(id=45)
                            self.fields['catalogpointgroup'].initial = catalogpointgroupSelected
                            self.fields['pointgroupdetail'].initial = "<strong>punctual group not assigned</strong>"
                
                        #*******************************pointgroupnames*************************************
                        
                        
                        pointgroupnames_ids= CrystalSystemPointGroupNames.objects.filter(catalogcrystalsystem=catalogcrystalsystemSelected,type=typeSelected,active=1).values_list('pointgroupnames_id',flat=True)  
                        if pointgroupnames_ids:
                            pointgroupnamesQuerySet = PointGroupNames.objects.filter(id__in=pointgroupnames_ids)
                            pointgroupnamesSelected = pointgroupnamesQuerySet[0]
                            self.fields['pointgroupnames'].queryset = pointgroupnamesQuerySet
                            self.fields['pointgroupnames'].initial = pointgroupnamesSelected
                            self.fields['pointgroupnames'].help_text = "Group assigned, all the point groups of this crystal system have the same matrix" 
                            fieldsList = ['name','description']
                            html = getTableHTMLFromQuerySet(pointgroupnamesQuerySet,fields=fieldsList)
                                        
                            self.fields['pointgroupnamesdetail'].initial = html
                        else:
                            pointGroupNamesQuerySet = PointGroupNames.objects.filter(id=21)
                            self.fields['pointgroupnames'].queryset = pointGroupNamesQuerySet
                            self.fields['pointgroupnames'].help_text = "Select this option if all groups of points in this crystal system have the same matrix" 
                            pointgroupnamesSelected = PointGroupNames.objects.get(id=21)
                            self.fields['pointgroupnames'].initial = pointgroupnamesSelected
                            self.fields['pointgroupnamesdetail'].initial = "<strong>groups not assigned</strong>"
                        
                        #*******************************axis*************************************
                        
                        axis_ids= CrystalSystemAxis.objects.filter(catalogcrystalsystem=catalogcrystalsystemSelected,type=typeSelected,catalogpointgroup= catalogpointgroupSelected,pointgroupnames = pointgroupnamesSelected,active=1).values_list('axis_id',flat=True)  
                        if axis_ids:
                            axisQuerySet = CatalogAxis.objects.filter(id__in=axis_ids)
                            fieldsList = ['name','description']
                            html = getTableHTMLFromQuerySet(axisQuerySet,fields=fieldsList)
                            self.fields['axis'].queryset = axisQuerySet
                            self.fields['axis'].help_text = "<strong>axis  assigned</strong>"
                            axisSelected = axisQuerySet[0]
                            self.fields['axis'].initial =   axisSelected
                            self.fields['axisdetail'].initial = html
                        else:
                            axisQuerySet=  CatalogAxis.objects.filter(id=4) 
                            self.fields['axis'].queryset = axisQuerySet
                            self.fields['axis'].help_text = "Axis not assigned"
                            axisSelected = CatalogAxis.objects.get(id=4)
                            self.fields['axis'].initial = axisSelected
                            self.fields['axisdetail'].initial = "<strong>axis not assigneds</strong>"
                            
                        
                catalogPropertyDetailQuerySet, catalogPropertyDetailList,catalogPropertyDetailnames = setCoefficients(typeSelected, catalogcrystalsystemSelected,datapropertySelected,catalogpointgroupSelected,pointgroupnamesSelected,axisSelected)
                catalogPropertyDetailNamesList = []
                #coefficients_ids = getIdsFromQuerySet(catalogPropertyDetailQuerySet)
                
                if not  coefficients_ids:
                    none_catalogpropertydetailQuerySet=CatalogPropertyDetail.objects.none()
                    qs = list(chain(none_catalogpropertydetailQuerySet, catalogPropertyDetailList))
                    CatalogPropertyDetailTemp.objects.all().delete()#clean CatalogPropertyDetailTemp
                    for i,cname in enumerate(qs):
                        cpdt=CatalogPropertyDetailTemp()
                        cpdt.name = cname
                        cpdt.save()
                        del cpdt
                        
                    for i,obj in enumerate(catalogPropertyDetailQuerySet):
                        cpdt=CatalogPropertyDetailTemp()
                        cpdt.name = catalogPropertyDetailQuerySet[i].name
                        catalogPropertyDetailNamesList.append(catalogPropertyDetailQuerySet[i].name)
                        cpdt.save()
                        del cpdt
                    
                
               
                if catalogPropertyDetailQuerySet: #There are exist coefficients for the property and they will be deployed
                    catalogPropertyDetailTempQuerySet=CatalogPropertyDetailTemp.objects.filter(name__in=catalogPropertyDetailNamesList)
                    self.fields['coefficients'].initial = catalogPropertyDetailTempQuerySet
                elif not catalogPropertyDetailQuerySet and coefficients_ids:
                    catalogPropertyDetailQuerySet  = CatalogPropertyDetailTemp.objects.filter(id__in=coefficients_ids)  
                    self.fields['coefficients'].initial = catalogPropertyDetailQuerySet
                 
    
                catalogPropertyDetailTempQuerySet=CatalogPropertyDetailTemp.objects.all()#get all newcoefficients
                self.fields['coefficients'].queryset = catalogPropertyDetailTempQuerySet
                
                
                
                #******************************Rules**************************************************************************#
                size = 0
                if len(catalogPropertyDetailQuerySet) > 0:
                
                    if len(catalogPropertyDetailnames) > 0:
                        size = len(catalogPropertyDetailnames) 
                    else:
                        size = 10
                    
                    catalogpropertydetailnames = json.dumps(catalogPropertyDetailnames)
                    propertydetaillist = json.dumps(catalogPropertyDetailList)
                    url = reverse('admin:Properties_tensor_getrules', args=[self.instance.pk])  
                    
                        
                    #self.fields['coefficientsrules'].widget=forms.SelectMultiple(attrs={"onChange":"getRules('" +url +"'," +propertydetaillist +"," +catalogpropertydetailnames +"," + str(datapropertySelected.id )+"," +"this);",'size': size})
                    #self.fields['coefficientsrules'].widget=forms.SelectMultiple(attrs={'size': size})
                    #self.fields['coefficientsrules'].widget=forms.Select(attrs={"onChange":"getRules('" +url +"'," +propertydetaillist +"," +catalogpropertydetailnames +"," + str(datapropertySelected.id )+"," +"this);",'size': size})
                    #self.fields['coefficientsrules'].widget.attrs['style'] = 'width: 100%;'
                    self.fields['coefficientsrules'].widget=forms.SelectMultiple(attrs={'size': size})
                    self.fields['coefficientsrules'].queryset  = catalogPropertyDetailQuerySet
                 
                    
         
         
          
                    javascript =  """<script> 
         
                                            function getRules(url,propertydetaillist,catalogpropertydetailnames,datapropertySelected_id,obj){
                                                    var propertydetaillistselected = django.jQuery("[name=coefficientsrules]").val();
                                                    var keynotationselected = django.jQuery("[name=keynotation]").val();
                                                    
                                                    //alert(keynotationselected);
                                                    
                                                    datasend ={//'coefficient': obj.value,
                                                                         'catalogpropertydetaillist': propertydetaillist,
                                                                         
                                                                         'catalogpropertydetailnames':catalogpropertydetailnames,
                                                                         'propertydetaillistselected':propertydetaillistselected,
                                                                         'datapropertySelected':datapropertySelected_id,
                                                                         'keynotationselected':keynotationselected  }
                                                                         
                                                    callajax(url, datasend);
                                            } 
                                            
                                            function saveRule(url,propertydetaillist,catalogpropertydetailnames,datapropertySelected_id,obj){
                                                    var propertydetaillistselected = django.jQuery("[name=coefficientsrules]").val();
                                                    var keynotationselected = django.jQuery("[name=keynotation]").val();
                                                    var zerocomponentselected = django.jQuery("[name=zerocomponent]").val();
        
                                                    
                                                    datasend ={//'coefficient': obj.value,
                                                                         'zerocomponentselected': zerocomponentselected,
                                                                         'propertydetaillistselected':propertydetaillistselected,
                                                                         'datapropertySelected':datapropertySelected_id,
                                                                         'keynotationselected':keynotationselected  }
                                                                         
                                                    callajax(url, datasend);
                                            } 
                                            
                                            function  callajax(url, datasend)
                                            {
                                                 var csrftoken = django.jQuery("[name=csrfmiddlewaretoken]").val();
                                                 function csrfSafeMethod(method) {
                                                        // these HTTP methods do not require CSRF protection
                                                        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                                                    }
                                                                                           
                                                   // start django.jQuery
                                                     django.jQuery(function($) {
                                                     
                                                       // prepare ajax
                                                        $.ajaxSetup({
                                                            beforeSend: function(xhr, settings) {
                                                                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                                                }
                                                            }
                                                        });
                                                        
                                                        
                                                    // start ajax
                                                        $.ajax({
                                                        url : url,  
                                                        type: "POST",  
                                                        dataType: 'json',
                                                        data : datasend, 
                                                        success: function (data) {
                                     
                                                            console.log(data); // log the returned json to the console
                                                            console.log("success"); // another sanity check
                                                            django.jQuery("[name=keynotation]").val(data.keynotationlist);
                                                            
                                                        },
                                                
                                                        // handle a non-successful response
                                                        error : function(xhr,errmsg,err) {
                                                            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                                                                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                                                            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                                                        }
                                                    });
                                                    
                                                    //end ajax
                                                 });
                                                 // end django.jQuery
                                            
                                            }
                                            </script>
                                            
                                            """
                    
                    url = reverse('admin:Properties_tensor_saverule', args=[self.instance.pk])  
                    onclick = "saveRule(\"" +url +"\"," +propertydetaillist +"," +catalogpropertydetailnames +"," +  str(datapropertySelected.id )+"," +"this);"
                    #html = "<p class='deletelink-box'><a href='#' class='btn btn-sm btn-default' onclick='" +onclick+ "'><span class='glyphicon glyphicon-floppy-save'></span>  Save Rule</a> <input class='default' type='button' value='Save Rule' onclick='" +onclick+ "'> </p>"
                    html = "<p class='deletelink-box'><input class='default' type='button' value='Save Rule' onclick='" +onclick+ "'> </p>"
                   
                    html = html  + javascript
                    self.fields['jquery'].initial = html
                    #print read_write_coefficients
                    
                    
        
                    keyNotationQuerySet = KeyNotation.objects.all()
                    size = 0
                    if len(keyNotationQuerySet) > 0:
                        size = len(keyNotationQuerySet) 
                    else:
                        size = 10
                        
                
                    self.fields['keynotation'].widget=forms.Select(attrs={'size': size})
                    self.fields['keynotation'].widget.attrs['style'] = 'width: 100%;'
                    self.fields['keynotation'].queryset  = keyNotationQuerySet
        
                    
                    """
                    alert_types=self.get_alert_types(3006)
                    self.fields['alert_type'] = forms.MultipleChoiceField(
                    choices=alert_types,
                    required=False
                    )
                    """
                    
                    if int(self.instance.pk) == 1 or int(self.instance.pk) == 3:
                        symmetry = True
                    elif int(self.instance.pk) ==  2:
                        symmetry = False
                        
                        
                    jsutils = JSUtils()
          
                    dimensions=datapropertySelected.tensor_dimensions.split(',')
                    scij = None
                    if len(dimensions) == 2:
                        parts=datapropertySelected.tag.split('_')[-1]
                        scij =parts.split('ij')
                        
                        
                    col_text =['Coefficient','Destination coefficient','Rule']
                    htmlcode = ""   
                    htmlcode += "<table>"
                    htmlcode += "<thead>"
                    htmlcode += "<tr>"
                    for i, name in enumerate(col_text):
                        htmlcode += "<th scope='col'>"
                        htmlcode += "<div class='text'>"
                        htmlcode += "<span>" + name + "</span>"
                        htmlcode += "</div>"
                        htmlcode += "<div class='clear'></div>"
                        htmlcode += "</th>"
                    
                    htmlcode += "</tr>"
                    htmlcode += "</thead>"
                    htmlcode += "<tbody>"
                    
                    response_data = {}
                    for i, obj  in enumerate(catalogPropertyDetailQuerySet):   
                        keyNotationCatalogPropertyDetail= jsutils.getKeyNotation(obj)
                        rulesAndTarget =[]
                        if isinstance(keyNotationCatalogPropertyDetail, QuerySet):
                            source_target_Dic = {}
                            for x,knotationpropertydetail in enumerate(keyNotationCatalogPropertyDetail):
                                source_target = {}
                                sourceList = [y.strip() for y in knotationpropertydetail.source.split(',')]
                                if len(sourceList) > 1:
                                    targetList = [y.strip() for y in knotationpropertydetail.target.split(',')]
                                    source_target_Dic[ tuple(sourceList)]=targetList
                                    source_target[ tuple(sourceList)]=targetList
                                    source_target['keynotation']=knotationpropertydetail.keynotation
                                    rulesAndTarget.append(source_target)
                                    
                                elif len(sourceList) == 1:
                                    targetList = [y.strip() for y in knotationpropertydetail.target.split(',')]
                                    source_target_Dic[obj.name]=targetList
                                    source_target[obj.name]=targetList
                                    source_target['keynotation']=knotationpropertydetail.keynotation
                                    rulesAndTarget.append(source_target)
                                    
                                    
                            if source_target_Dic:
                                jsutils.getsimetricandnonzero( obj.name,scij,source_target_Dic,symmetry)
                                
                                for i, d in enumerate(rulesAndTarget):
                                    jsutils.getrules(obj.name,scij,d,symmetry)
                                
                            
             
                        else:
                            targetList = [x.strip() for x in keyNotationCatalogPropertyDetail.target.split(',')]
                            source_target_Dic = {}
                            source_target_Dic[obj.name]=targetList
                            source_target_Dic['keynotation']=keyNotationCatalogPropertyDetail.keynotation
                            if source_target_Dic:
                                if keyNotationCatalogPropertyDetail.keynotation.id ==4 or keyNotationCatalogPropertyDetail.keynotation.id ==6 or keyNotationCatalogPropertyDetail.keynotation.id ==5 or keyNotationCatalogPropertyDetail.keynotation.id ==10:
                                    jsutils.getsimetricandnonzero( obj.name,scij,source_target_Dic,symmetry)
                                    jsutils.getrules(obj.name,scij,source_target_Dic,symmetry)
                                else:
                                    jsutils.getsimetricandnonzero( obj.name,scij,source_target_Dic,symmetry)
                                    jsutils.getrules(obj.name,scij,source_target_Dic,symmetry)
                                
                                
                 
                    htmlcode +=  str(jsutils.htmlcode )  
         
                    htmlcode +=    "</tbody>"
                    htmlcode += "</table>"    
                    
                    self.fields['detailrules'].initial = htmlcode 
                    
                          
                    zero_component= list(set(catalogPropertyDetailList) - set(jsutils.simetricandnonzeroinputs))
                    size = 0
                    if len(zero_component) > 0:
                        size = len(zero_component) 
                        keyNotation = KeyNotation.objects.filter(id=1)
                        self.fields['keynotation'].initial  = keyNotation
                    else:
                        size = 5
                        
                        
                   
                        
                    
                    self.fields['zerocomponent'].widget=forms.SelectMultiple(attrs={'size': size})
                    self.fields['zerocomponent'].widget.attrs['style'] = 'width: 100%;'
                    self.fields['zerocomponent'].queryset = CatalogPropertyDetailTemp.objects.filter(name__in=zero_component).order_by('name')
                    
                
                else:
                    self.fields['jquery'].initial  = '' 
                    self.fields['detailrules'].initial = '' 
                    self.fields['coefficientsrules'].queryset  = CatalogPropertyDetailTemp.objects.none() 
                    self.fields['keynotation'].queryset  = KeyNotation.objects.none() 
                    zero_component= list(set(catalogPropertyDetailList))
                    self.fields['zerocomponent'].queryset = CatalogPropertyDetailTemp.objects.none() 
                
                  
    
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
                    self.fields['dataproperty'].queryset = Property.objects.filter(active=True)    
                    self.fields['catalogcrystalsystem'].queryset=CatalogCrystalSystem.objects.all()       
                    self.fields['catalogpointgroup'] = CatalogPointGroup.objects.all()    
                    self.fields['pointgroupnames'] =  PointGroupNames.objects.all()    
    
     
        except Exception  as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args)    
            print err
            #raise forms.ValidationError(str(err))
             
        
        
class CatalogCrystalSystemAdminForm(forms.ModelForm):  
    
    class Meta:
        model = CatalogCrystalSystem
        
    def clean(self,*args,**kwargs):
         
        catalogpointgroup=self.cleaned_data.get("crystalsystemtype")
        pointgroupnames=self.cleaned_data.get("pointgroupnames")
        catalogpointgroup=self.cleaned_data.get("catalogpointgroup")
        
        if catalogpointgroup == True:
            if not catalogpointgroup and not pointgroupnames:
                raise forms.ValidationError("the 'Point Group' or 'Groups' fields are not selected, you must select one of the two!")
            
                if  catalogpointgroup  and  pointgroupnames:
                    if  (catalogpointgroup.id == 45  and  pointgroupnames.id  != 21 ) or (catalogpointgroup.id  != 45  and  pointgroupnames.id == 21):
                        pass
                    elif (catalogpointgroup.id  != 45  and  pointgroupnames.id == 21):
                        pass
                    elif (catalogpointgroup.id  != 45  and  pointgroupnames.id != 21):
                        raise forms.ValidationError("the 'Point Group' or 'Groups' fields have selected options, you must select one of the two!")
            else:
                pass
        

        return super(CatalogCrystalSystemAdminForm,self).clean(*args,**kwargs)
    
    def clean_pointgroupnames(self):
        pointgroupnames = self.cleaned_data['pointgroupnames']
        return pointgroupnames
    
    def clean_catalogpointgroup(self):
        catalogpointgroup = self.cleaned_data['catalogpointgroup']
        return catalogpointgroup    
    
    def clean_crystalsystemtype(self):
        catalogpointgroup = self.cleaned_data['crystalsystemtype']
        return catalogpointgroup   
        
    def __init__(self, *args, **kwargs):   
        catalogproperty_id = None
        pointgroupnames_id  = None
        catalogpointgroup_id = None
        crystalsystemtype_active = False
        onchange = False
        if args: #(true if edit and save or save an existing instance, when form was changed), false when instance was selected from change list
            type_id =  argsToInt(args,'type')
            catalogproperty_id =  argsToInt(args,'catalogproperty')
            catalogpointgroup_id = argsToInt(args,'catalogpointgroup',45)
            pointgroupnames_id  =  argsToInt(args,'pointgroupnames',21)
            crystalsystemtype_active= argsToBoolean(args,'crystalsystemtype')
            #axis_id =  argsToInt(args,'axis',4)
            axis_ids= argsListToIntList(args, 'axis')  
            if not args[0].has_key('_save') and not args[0].has_key('_addanother') and not args[0].has_key('_continue'):    
                args ={}
                onchange = True
            

  
  
        super(CatalogCrystalSystemAdminForm, self).__init__(*args, **kwargs)
        self.fields['catalogproperty'].empty_label = None
        #self.fields['catalogproperty'].widget=forms.Select()

   
        self.fields['type'] = forms.ModelChoiceField(queryset=None,label="Type",required=True)
        self.fields['type'].widget=forms.Select(attrs={"onChange":'submit()'})
        self.fields['type'].empty_label = None        
        
        #self.fields['crystalsystemtype'] = forms.ModelChoiceField(queryset=None,label="Active for this Type",required=True)
        self.fields['crystalsystemtype'] = forms.CharField(max_length=100,label="Active",required=True)
        self.fields['crystalsystemtype'].widget=forms.CheckboxInput()
          
         
        
        
        self.fields['catalogpointgroup'] = forms.ModelChoiceField(queryset=None,label="Point Group",required=True)
        self.fields['catalogpointgroup'].widget=forms.Select()
        self.fields['catalogpointgroup'].empty_label = None
        self.fields['pointgroupnames'] =  forms.ModelChoiceField(queryset=None,label="Groups",required=True)
        self.fields['pointgroupnames'].widget=forms.Select()
        self.fields['pointgroupnames'].empty_label = None
        """self.fields['axis'] =  forms.ModelChoiceField(queryset=None,label="Groups",required=True)
        self.fields['axis'].widget=forms.Select()
        self.fields['axis'].empty_label = None"""
        
        self.fields['axis'] = forms.ModelMultipleChoiceField(
            queryset=None,
            required=False,
            label="Axis",
            widget=FilteredSelectMultiple(
                verbose_name='Axis',
                is_stacked=False,
            )
        )
        
        self.fields['pointgroupdetail'] = forms.CharField(label='Point Group Detail',widget = DetailFieldWidget,required=False)
        self.fields['pointgroupnamesdetail'] = forms.CharField(label='Groups Detail',widget = DetailFieldWidget,required=False)
        self.fields['axisdetail'] = forms.CharField(label='Axis Detail',widget = DetailFieldWidget,required=False)
 
        
        typeSelected = None
        datapropertySelected = None
        catalogcrystalsystemSelected = None
        catalogpointgroupSelected = None
        pointgroupnamesSelected = None
        axisSelected = None
        if self.instance.pk: 
            if args:
                #*******************************type*************************************          
                typeSelected = Type.objects.get(id=type_id)
                typeQuerySet=Type.objects.filter(active=True,catalogproperty= self.instance.catalogproperty)   
                self.fields['type'].queryset = typeQuerySet
                self.fields['type'].initial = typeSelected
                
                
                #*******************************crystalsystemtype*************************************  
                if crystalsystemtype_active == True:
                    self.fields['crystalsystemtype'].initial= True
                else:
                    self.fields['crystalsystemtype'].initial= False

 
                
                #*******************************catalogpointgroup*************************************                
                catalogpointgroupSelected = CatalogPointGroup.objects.get(id=int(catalogpointgroup_id))
                self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()
                self.fields['catalogpointgroup'].initial = catalogpointgroupSelected
                self.fields['pointgroupdetail'].initial = "<strong>punctual group assigned</strong>"

                #*******************************pointgroupnames*************************************
                pointgroupnamesSelected = PointGroupNames.objects.get(id=int(pointgroupnames_id))  
                self.fields['pointgroupnames'].queryset = PointGroupNames.objects.all()
                self.fields['pointgroupnames'].initial = pointgroupnamesSelected
                self.fields['pointgroupnamesdetail'].initial = "<strong>groups assigned</strong>"
                
                #*******************************axis*************************************
                axisSelected = CatalogAxis.objects.filter(id__in=axis_ids)
                self.fields['axis'].queryset = CatalogAxis.objects.all()
                self.fields['axis'].initial = axisSelected
                self.fields['axisdetail'].initial = "<strong>Axis assigned</strong>"
                
                
            else:
                if onchange:                    
                    
                    #*******************************catalogproperty*************************************       
                    self.fields['catalogproperty'].queryset= CatalogProperty.objects.filter(id = self.instance.catalogproperty.id)
                    self.fields['catalogproperty'].initial= CatalogProperty.objects.get(id = self.instance.catalogproperty.id)

                    #*******************************type*************************************          
                    typeSelected = Type.objects.get(id=type_id)
                    typeQuerySet=Type.objects.filter(active=True,catalogproperty= self.instance.catalogproperty)   
                    self.fields['type'].queryset = typeQuerySet
                    self.fields['type'].initial = typeSelected
                    
                    #pointgroupnamesSelected = PointGroupNames.objects.filter(id=pointgroupnames_id)
                    #catalogpointgroupSelected = CatalogPointGroup.objects.get(id= catalogpointgroup_id)
                    
                    #*******************************crystalsystemtype*************************************  
                    crystalsystemtype=CrystalSystemType.objects.filter(catalogcrystalsystem=self.instance,type=typeSelected)   
                    if crystalsystemtype:
                        crystalsystemtypeSelected= crystalsystemtype[0]
                        if crystalsystemtypeSelected.active == True:
                            self.fields['crystalsystemtype'].initial= True
                        else:
                            self.fields['crystalsystemtype'].initial= False
                         
                    else:
                        self.fields['crystalsystemtype'].initial= False
                    
                    #*******************************pointgroupnames*************************************
                    pointgroupnames_ids= CrystalSystemPointGroupNames.objects.filter(catalogcrystalsystem=self.instance,type=typeSelected,active =1).values_list('pointgroupnames_id',flat=True) 
                    if pointgroupnames_ids:
                        pointGroupNamesQuerySet= PointGroupNames.objects.filter(id__in=pointgroupnames_ids)
                        self.fields['pointgroupnames'].queryset = PointGroupNames.objects.all()
                        self.fields['pointgroupnames'].initial =pointGroupNamesQuerySet[0]
                        pointgroupnamesSelected= pointGroupNamesQuerySet[0]
                        html = getTableHTMLFromQuerySet(pointGroupNamesQuerySet)
                        self.fields['pointgroupnamesdetail'].initial = html
                        self.fields['pointgroupnames'].help_text = "Assigned group, all groups of points in this crystal system will have the same matrix" 
                    else:
                        pointGroupNamesQuerySet = PointGroupNames.objects.all()
                        pointgroupnamesSelected= PointGroupNames.objects.get(id=21)
                        self.fields['pointgroupnames'].queryset =  pointGroupNamesQuerySet
                        self.fields['pointgroupnames'].initial =  PointGroupNames.objects.get(id=21)
                        self.fields['pointgroupnamesdetail'].initial = "<strong>Group not assigned</strong>"
                        
                    #*******************************catalogpointgroup*************************************
                    catalogpointgroup_ids = CrystalSystemPointGroup.objects.filter(catalogcrystalsystem=self.instance,type=typeSelected,active =1).values_list('catalogpointgroup_id',flat=True) 
                    if catalogpointgroup_ids:
                        catalogpointgroupQuerySet = CatalogPointGroup.objects.filter(id__in= catalogpointgroup_ids)
                        self.fields['catalogpointgroup'].queryset =CatalogPointGroup.objects.all()
                        self.fields['catalogpointgroup'].initial =catalogpointgroupQuerySet[0]
                        catalogpointgroupSelected =  catalogpointgroupQuerySet[0]
                        html = getTableHTMLFromQuerySet(catalogpointgroupQuerySet)
                        self.fields['pointgroupdetail'].initial = html
                        self.fields['pointgroupdetail'].help_text = "Punctual group  assigned" 
                    else:
                        catalogpointgroupQuerySet = CatalogPointGroup.objects.all()
                        self.fields['catalogpointgroup'].queryset =catalogpointgroupQuerySet
                        catalogpointgroupSelected = CatalogPointGroup.objects.get(id=45)
                        self.fields['catalogpointgroup'].initial = CatalogPointGroup.objects.get(id=45)
                        self.fields['pointgroupdetail'].initial = "<strong>punctual group not assigned</strong>"
  
                    #*******************************axis*************************************
                    axis_ids=  CrystalSystemAxis.objects.filter(catalogcrystalsystem=self.instance,type=typeSelected,catalogpointgroup= catalogpointgroupSelected,pointgroupnames = pointgroupnamesSelected,active = 1).values_list('axis_id',flat=True)  
                    if axis_ids:
                        axisQuerySet = CatalogAxis.objects.filter(id__in= axis_ids)
                        self.fields['axis'].queryset =CatalogAxis.objects.all().exclude(id=4)
                        self.fields['axis'].initial =axisQuerySet                   
                        """html = getTableHTMLFromQuerySet(axisQuerySet)
                        self.fields['axisdetail'].initial = html
                        self.fields['axisdetail'].help_text = "axis  assigned" """
                    else:
                        self.fields['axis'].queryset =CatalogAxis.objects.all().exclude(id=4)
                        #catalogpointgroupSelected = CatalogAxis.objects.get(id=4)
                        #self.fields['axis'].initial =catalogpointgroupSelected
                        #self.fields['axisdetail'].initial = "<strong>axis not assigned</strong>"
                    
                else:#select from list for change
                    
                    self.fields['catalogproperty'].queryset= CatalogProperty.objects.filter(id = self.instance.catalogproperty.id)
                    self.fields['catalogproperty'].initial= CatalogProperty.objects.get(id = self.instance.catalogproperty.id)

                    typeQuerySet=Type.objects.filter(catalogproperty= self.instance.catalogproperty)   
                    typeSelected= typeQuerySet[0]
                    self.fields['type'].queryset= typeQuerySet
                    self.fields['type'].initial= typeSelected
                    
                    #*******************************crystalsystemtype*************************************  
                    crystalsystemtype=CrystalSystemType.objects.filter(catalogcrystalsystem=self.instance,type=typeSelected)   
                    if crystalsystemtype:
                        crystalsystemtypeSelected= crystalsystemtype[0]
                        if crystalsystemtypeSelected.active == True:
                            self.fields['crystalsystemtype'].initial= True
                        else:
                            self.fields['crystalsystemtype'].initial= False
                         
                    else:
                        self.fields['crystalsystemtype'].initial= False
                      
                
                    
                    
                    
                    
    
                    pointgroupnames_ids= CrystalSystemPointGroupNames.objects.filter(catalogcrystalsystem=self.instance,type=typeSelected,active =1).values_list('pointgroupnames_id',flat=True) 
                     
                    if pointgroupnames_ids:
                        pointGroupNamesQuerySet= PointGroupNames.objects.filter(id__in=pointgroupnames_ids)
                        self.fields['pointgroupnames'].queryset =  PointGroupNames.objects.all()
                        self.fields['pointgroupnames'].initial = pointGroupNamesQuerySet[0]
                        pointgroupnamesSelected = pointGroupNamesQuerySet[0]
                        fieldsList = ['name','description']
                        html = getTableHTMLFromQuerySet(pointGroupNamesQuerySet,fields=fieldsList)
                        self.fields['pointgroupnamesdetail'].initial = html
                        self.fields['pointgroupnames'].help_text = "Assigned group, all groups of points in this crystal system will have the same matrix" 
                    else:
                        self.fields['pointgroupnames'].queryset =  PointGroupNames.objects.all()
                        pointgroupnamesSelected = PointGroupNames.objects.get(id=21)
                        self.fields['pointgroupnames'].initial = pointgroupnamesSelected
                        self.fields['pointgroupnamesdetail'].initial = "<strong>Group not assigned</strong>"

                    catalogpointgroup_ids = CrystalSystemPointGroup.objects.filter(catalogcrystalsystem=self.instance,type=typeSelected,active =1).values_list('catalogpointgroup_id',flat=True)  
                    
                    if catalogpointgroup_ids:
                        catalogpointgroupQuerySet = CatalogPointGroup.objects.filter(id__in= catalogpointgroup_ids)
                        self.fields['catalogpointgroup'].queryset =CatalogPointGroup.objects.all()
                        self.fields['catalogpointgroup'].initial =catalogpointgroupQuerySet[0]
                        catalogpointgroupSelected = catalogpointgroupQuerySet[0]
                        fieldList = ['name','description']
                        html = getTableHTMLFromQuerySet(catalogpointgroupQuerySet)
                        self.fields['pointgroupdetail'].initial = html
                        self.fields['pointgroupdetail'].help_text = "Punctual group  assigned" 
                    else:
                        self.fields['catalogpointgroup'].queryset =CatalogPointGroup.objects.all()
                        catalogpointgroupSelected = CatalogPointGroup.objects.get(id=45)
                        self.fields['catalogpointgroup'].initial =catalogpointgroupSelected
                        self.fields['pointgroupdetail'].initial = "<strong>punctual group not assigned</strong>"

                    axis_ids=  CrystalSystemAxis.objects.filter(catalogcrystalsystem=self.instance,type=typeSelected,catalogpointgroup= catalogpointgroupSelected,pointgroupnames = pointgroupnamesSelected,active = 1).values_list('axis_id',flat=True)  
                    if axis_ids:
                        axisQuerySet = CatalogAxis.objects.filter(id__in= axis_ids)
                        self.fields['axis'].queryset =CatalogAxis.objects.all().exclude(id=4)
                        self.fields['axis'].initial =axisQuerySet
                        """self.fields['axis'].initial =axisQuerySet[0]                        
                        html = getTableHTMLFromQuerySet(axisQuerySet)
                        self.fields['axisdetail'].initial = html
                        self.fields['axisdetail'].help_text = "axis  assigned" """
                    else:
                        self.fields['axis'].queryset =CatalogAxis.objects.all().exclude(id=4)
                        #catalogpointgroupSelected = CatalogAxis.objects.get(id=4)
                        #self.fields['axis'].initial =catalogpointgroupSelected
                        #self.fields['axisdetail'].initial = "<strong>axis not assigned</strong>"

                    
        else:
            if args:#save  new
                
                #*******************************type*************************************    
                typeQuerySet=Type.objects.all()   
                typeSelected = Type.objects.get(id=type_id)
                self.fields['type'].queryset= typeQuerySet
                self.fields['type'].initial= typeSelected
                
                #*******************************crystalsystemtype*************************************  
                crystalsystemtype=CrystalSystemType.objects.filter(catalogcrystalsystem=self.instance,type=typeSelected)   
                if crystalsystemtype:
                    crystalsystemtypeSelected= crystalsystemtype[0]
                    if crystalsystemtypeSelected.active == True:
                        self.fields['crystalsystemtype'].initial= True
                    else:
                        self.fields['crystalsystemtype'].initial= False
                     
                else:
                    self.fields['crystalsystemtype'].initial= False
                
                
                #*******************************catalogpointgroup*************************************                
                catalogpointgroupSelected = CatalogPointGroup.objects.get(id=int(catalogpointgroup_id))
                self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()
                self.fields['catalogpointgroup'].initial = catalogpointgroupSelected
                self.fields['pointgroupdetail'].initial = "<strong>punctual group assigned</strong>"

                #*******************************pointgroupnames*************************************
                pointgroupnamesSelected = PointGroupNames.objects.get(id=int(pointgroupnames_id))  
                self.fields['pointgroupnames'].queryset = PointGroupNames.objects.all()
                self.fields['pointgroupnames'].initial = pointgroupnamesSelected
                self.fields['pointgroupnamesdetail'].initial = "<strong>groups assigned</strong>"
                
                #*******************************axis*************************************
                axisSelected = CatalogAxis.objects.get(id__in=axis_ids)
                self.fields['axis'].queryset = PointGroupNames.objects.all().exclude(id=4)
                self.fields['axis'].initial = pointgroupnamesSelected
                self.fields['axisdetail'].initial = "<strong>groups assigned</strong>"
                
                
                
            else:#add new
                #*******************************type*************************************
                typeQuerySet=Type.objects.all()   
                self.fields['type'].queryset= typeQuerySet
                self.fields['type'].initial= typeQuerySet[0]
            
                
                #*******************************pointgroupnames*************************************
                self.fields['pointgroupnames'].queryset =  PointGroupNames.objects.all()
                self.fields['pointgroupnamesdetail'].initial = "<strong>Group not assigned</strong>"
                #*******************************catalogpointgroup*************************************        
                self.fields['catalogpointgroup'].queryset =CatalogPointGroup.objects.all()
                self.fields['pointgroupdetail'].initial = "<strong>punctual group not assigned</strong>"
                
                
                #*******************************axis*************************************
                self.fields['axis'].queryset =  CatalogAxis.objects.all().exclude(id=4)
                self.fields['axisdetail'].initial = "<strong>Axis  not assigned</strong>"
        
        
        

        
class FileUserAdminFormv2(forms.ModelForm):  
    
    class Meta:
        model = FileUser
        #widgets = {'datafile': forms.HiddenInput()}
        
        
    def __init__(self, *args, **kwargs):
        process = True
        if kwargs.has_key('process'):
            process= kwargs.pop('process')
            
        publish = None
        onchange = False
        datepublished = None
        pointGroupSelectedName = None
        if args:
            
            if not args[0].has_key('_save') and not args[0].has_key('_addanother') and not args[0].has_key('_continue'):    
                args ={}
                onchange = True
        
        super(FileUserAdminFormv2, self).__init__(*args, **kwargs)
      
        self.fields['filenamepublished'] = forms.CharField(widget = DetailFieldWidget, required=False)
        self.fields['filenamepublished'].label='File name published'   
        
        self.fields['reportvalidation'] = forms.CharField(widget = forms.Textarea, required=False)
        self.fields['reportvalidation'].label='Report  validation'   
        self.fields['reportvalidation'].widget.attrs['readonly'] = True
        
        
        self.fields['filenametemp'] = forms.CharField(widget = DetailFieldWidget, required=False)
        self.fields['filenametemp'].label='Show file'   

        #self.fields['datepublished'].widget.attrs['readonly'] = True
 
        if self.instance.pk: 
            if args:
                if self.instance.datafile != None:
                    print self.instance.datafile.filename
                else:
                    print ""
                    
                    
                #self.fields['filenamepublished'].initial = self.instance.datafile
                
    
                        
            else:
                if onchange:
                    pass
                else:#select from list for change
                    if  self.instance.publish:
                        if  self.instance.datafile:
                            self.fields['filenamepublished'].initial = "<a href='/datafiles/" + self.instance.datafile.filename  +"' target='_blank'>"  + self.instance.datafile.filename  +"</a>"
                        else:
                            self.fields['filenamepublished'].initial = ""
                    else:
                        self.fields['filenamepublished'].initial = ""
                        
                    
                    
                    self.fields['filenametemp'].initial = "<a href='/datafiles/valid/" + self.instance.filename  +"' target='_blank'>"  + self.instance.filename  +"</a>"
                    print self.fields['filenametemp'].initial
 
                    self.fields['datafile'].widget = forms.HiddenInput()
                    self.fields['datafile'].required = False
                    self.fields['datafile'].label= ''
                    
 
  
           
                    if process:
                        customfile = False
                        loadtodatabase = False
                        fds2 = []    
                        fds2.append(self.instance.filename)
                        edff= ExtractDataFormFields()
                        edff.debug = False
                        edff.processData(loadtodatabase,fds2,customfile)

    
                        if edff:
                            self.fields.update(edff.customForm.fields)
                            """
                            for key, v in self.fields.iteritems():
                                if edff.customForm.readonly_fields.has_key(key):
                                    self.fields[key].widget.attrs['readonly'] = True
                                    print 'readonly',key
                            """
                                    

                     
                    #urlproperties = reverse('admin:Files_fileuser_property', args=[self.instance.pk]) 
                    #urlexperimentalcon = reverse('admin:Files_fileuser_experimental', args=[self.instance.pk]) 
                    urlupdatecoefficients = reverse('admin:Files_fileuser_updatecoefficients', args=[self.instance.pk]) 
                    #urlupdatecondition=reverse('admin:Files_fileuser_updatecondition', args=[self.instance.pk]) 
                     
                    javascript =  "<script>"
                    #javascript += "var urlproperties = \"" +urlproperties +"\""
                    javascript +="\n"
                    #javascript +="var urlexperimentalcon = \"" +urlexperimentalcon +"\""   
                    javascript +="\n"
                    javascript +="var urlupdatecoefficients = \"" +urlupdatecoefficients +"\""   
                    javascript +="\n"
                    #javascript +="var urlupdatecondition = \"" +urlupdatecondition +"\""  
                    javascript +="</script>"""
                    
                    
                    
                    self.fields['js'] = forms.CharField(label='',widget = JQueryCustomFieldWidget, required=False) 
                    self.fields['js'].initial = javascript
 
                
        else:
            if args:#save  new
                pass
            else:#add new
                pass


        
        
        
 

  
class FileUserAdminForm(forms.ModelForm):  
    
    class Meta:
        model = FileUser
        
        
    #for validation 
    def clean(self,*args,**kwargs):
         
        reportvalidation=self.cleaned_data.get("reportvalidation")
        
        if not reportvalidation:
            pass
            #raise forms.ValidationError("the 'Point Group' or 'Groups' fields are not selected, you must select one of the two!")
        
 

        return super(FileUserAdminForm,self).clean(*args,**kwargs)
    
    
    #for validation 
    def clean_reportvalidation(self):
        reportvalidation = self.cleaned_data['reportvalidation']
        return reportvalidation
    
        
    def __init__(self, *args, **kwargs):   
        # initialice local fields
        #user_id = None
        datepublished = None
        properties_ids = None
        experimentalcon_ids = None
        phase_name = None
        reference = None
        title = None
        phase_generic = None
        pages_number = None
        journal = None
        year = None
        volume = None
        first_page = None
        last_page = None
        authors = None
        issue = None
        cod_code = None
        chemical_formula = None
        publish = None
 
        onchange = False
        if args: #(true if edit and save or save an existing instance, when form was changed), false when instance was selected from change list
            #receive values from form page and asing to local field
            #user_id =  argsToInt(args,'authuser_id')
            datepublished =  argsToDateTime(args,'datepublished')
            properties_ids= argsListToIntList(args,'properties')  
            experimentalcond_ids= argsListToIntList(args,'experimentalcon')
            phase_name = argsCheck(args,'phase_name')  
            reference = argsCheck(args,'reference')  
            title = argsCheck(args,'title')  
            phase_generic = argsCheck(args,'phase_generic')  
            pages_number = argsToInt(args,'pages_number') 
            journal = argsCheck(args,'journal') 
            year = argsToInt(args,'year')
            volume = argsToInt(args,'volume')
            first_page = argsToInt(args,'first_page')
            last_page = argsToInt(args,'last_page') 
            authors = argsCheck(args,'authors')  
            issue = argsCheck(args,'issue')  
            cod_code = argsToInt(args,'cod_code') 
            chemical_formula = argsCheck(args,'chemical_formula')  
            publish = argsCheck(args,'publish') 
            
            
            if not args[0].has_key('_save') and not args[0].has_key('_addanother') and not args[0].has_key('_continue'):    
                args ={}
                onchange = True
         
        
        
        super(FileUserAdminForm, self).__init__(*args, **kwargs)
        
        #define field to form page
         
        self.fields['fileuserid']  = forms.CharField(label="")
        self.fields['fileuserid'].widget = forms.HiddenInput()
        #self.fields['fileuserid'].empty_label = None
        
        
        self.fields['datafile_tempid']  = forms.CharField(label="")
        self.fields['datafile_tempid'].widget = forms.HiddenInput()

        
        self.fields['properties'] = forms.ModelMultipleChoiceField(
            queryset=None,
            required=False,
            label="Properties",
            widget=FilteredSelectMultiple(
                verbose_name='Property',
                is_stacked=False,
                #attrs={"onclick":"oneclick(this);"}
                #attrs={"ondblclick":"towclick(this)", "onclick":"oneclick(this)"}
            )

        )
 
        
        self.fields['jquery'] = forms.CharField(label='',widget = DetailFieldWidget, required=False) 
        #self.fields['jquery'].initial  = ''
        #self.fields['properties_click'].initial="properties"
 
 
        """self.fields['reportvalidationcustom'] = forms.CharField(widget = DetailFieldWidget, required=False)
        self.fields['reportvalidationcustom'].label='Report Validation'
       """
        
      
        #self.fields['filenamepublished'].label = mark_safe(_("File name published <a href='#'>Terms and Conditions</a>"))
       
        self.fields['filenamepublished'] = forms.CharField(widget = DetailFieldWidget, required=False)
        self.fields['filenamepublished'].label='File name published'      
        
               
            
            
                                                                                                                                             
        self.fields['phase_generic']  = forms.CharField(label='Phase generic', required=False)
        self.fields['phase_generic'].widget = forms.TextInput() 
        
        self.fields['phase_name']  = forms.CharField(label='Phase name', required=False)
        self.fields['phase_name'].widget = forms.TextInput() 
        
        self.fields['chemical_formula']  = forms.CharField(label='Chemical formula', required=False)
        self.fields['chemical_formula'].widget = forms.TextInput() 
        
        #self.fields['reportvalidation']  = forms.CharField(label='Report validation', required=False)
        #self.fields['reportvalidation'].widget = forms.TextInput() 
        
        
         
        #self.fields['title']  = forms.CharField(label='Title', required=False)
        self.fields['title']  = forms.CharField(label='Title',required=False)
        self.fields['title'].widget = forms.TextInput() 
        
        self.fields['authors']  = forms.CharField(label='Authors')
        self.fields['authors'].widget = forms.TextInput() 
        
        self.fields['journal']  = forms.CharField(label='Journal')
        self.fields['journal'].widget = forms.TextInput() 
        
        self.fields['year']  = forms.CharField(label='Year')
        self.fields['year'].widget = forms.TextInput() 
        
        self.fields['volume']  = forms.CharField(label='Volume',required=False)
        self.fields['volume'].widget = forms.TextInput() 
        
        self.fields['issue']  = forms.CharField(label='Issue')
        self.fields['issue'].widget = forms.TextInput() 
        
        self.fields['first_page']  = forms.CharField(label='First page')
        self.fields['first_page'].widget = forms.TextInput() 
        
        self.fields['last_page']  = forms.CharField(label='Last page')
        self.fields['last_page'].widget = forms.TextInput() 
        
        self.fields['reference']  = forms.CharField(label='Reference')
        self.fields['reference'].widget = forms.TextInput() 
        
        self.fields['pages_number']  = forms.CharField(label='Pages number')
        self.fields['pages_number'].widget = forms.TextInput() 
        
        self.fields['cod_code']  = forms.CharField(label='Code', required=False)
        self.fields['cod_code'].widget = forms.TextInput() 
        
        self.fields['pointgroup']  = forms.CharField(label='Point group', required=False)
        self.fields['pointgroup'].widget = forms.TextInput() 
        self.fields['pointgroup'].widget.attrs['readonly'] = True
        
        
      
        self.fields['experimentalcon'] = forms.ModelMultipleChoiceField(queryset=None,
                                                                                                                required=False,
                                                                                                                label="Experimental conditions",
                                                                                                                widget=FilteredSelectMultiple(
                                                                                                                    verbose_name='Experimental conditions',
                                                                                                                    is_stacked=False
                                                                                                                ))
        
        
 
        """self.fields['experimentalcon']  =forms.ModelChoiceField(queryset=None,label="Experimental conditions")
        self.fields['experimentalcon'].widget=forms.SelectMultiple()
        self.fields['experimentalcon'].empty_label = None
        """
        
        
        #self.fields['foo']  = forms.CharField(label='foo',required=False)
        #self.fields['foo'].widget = forms.TextInput() 
        
        
        
        if self.instance.pk: 
            if args:
                    if publish:
                        if datepublished:
                            self.instance.datepublished = datetime.datetime.strptime(datepublished, '%Y-%m-%d %H:%M:%S')
                            if  self.instance.datafile:
                                self.fields['filenamepublished'].initial = "<a href='/datafiles/" + self.instance.datafile.filename  +"' target='_blank'>"  + self.instance.datafile.filename  +"</a>"
                            else:
                                self.fields['filenamepublished'].initial = ""
                    else:
                        #self.instance.datafile = None
                        self.fields['filenamepublished'].initial = ""
                         
    
                    
                    objDataFileTemp = DataFileTemp.objects.get(filename__exact=self.instance.filename)
                    objPublArticleTemp = objDataFileTemp.publication
                    propertyTempQuerySet= PropertyTemp.objects.filter(id__in=properties_ids, active=True)

                    experimentalcondQuerySet = ExperimentalParCondTemp.objects.filter(id__in=experimentalcond_ids)
                    self.fields['experimentalcon'].queryset= ExperimentalParCondTemp.objects.all()
                    self.fields['experimentalcon'].initial= experimentalcondQuerySet

                    
                    

                    self.fields['properties'].queryset = PropertyTemp.objects.filer(active=True) 
                    self.fields['properties'].initial = propertyTempQuerySet
                    
                    #self.fields['reportvalidationcustom'].initial = "<strong><font color='black'>" + self.instance.reportvalidation +" </font></strong>" 

                    self.fields['phase_generic'].initial = phase_generic
                    self.fields['phase_name'].initial = phase_name
                    self.fields['chemical_formula'].initial = chemical_formula
                    self.fields['cod_code'].initial = cod_code
                    self.fields['title'].initial = title
                    self.fields['authors'].initial = authors
                    self.fields['journal'].initial = journal
                    self.fields['year'].initial = year
                    self.fields['volume'].initial = volume
                    self.fields['issue'].initial = issue
                    self.fields['first_page'].initial = first_page
                    self.fields['last_page'].initial = last_page
                    self.fields['reference'].initial = reference
                    self.fields['pages_number'].initial = pages_number

            else:
                if onchange:
                    pass
                else:#select from list for change
                    
                    
                        
                    fields1  = []
                    self.fields['fileuserid'].initial = self.instance.pk
                    """for item in self.instance.__dict__.items():
                            for field in item[1]:
                                fields1.append(field)
                    """
                    #fn=reverse('get_datafile', args=['1000377.mpod'])  
                    
                    
                    try:
                        
                        if  self.instance.datafile:
                            #self.fields['filenamepublished'].label = mark_safe("<a href='%s'>File name published </a>") % (reverse('get_datafile', args=[self.instance.datafile.filename]))
                            self.fields['filenamepublished'].initial = "<a href='/datafiles/" + self.instance.datafile.filename  +"' target='_blank'>"  + self.instance.datafile.filename  +"</a>"
                        else:
                            self.fields['filenamepublished'].initial = ""
                            
                    except Exception  as error:
                        print "message in the function get_conds for debug purposes.  Message({0}): {1}".format(99, error)  

                    try:
                        objDataFileTemp = DataFileTemp.objects.get(filename__exact=self.instance.filename)
                        self.fields['datafile_tempid'].initial = objDataFileTemp.pk
                        objPublArticleTemp = objDataFileTemp.publication
                        propertyTempQuerySet= objDataFileTemp.properties.all()
                        experimentalcond_ids = ExperimentalParCondTemp_DataFileTemp.objects.filter(datafiletemp=objDataFileTemp).values_list('experimentalfilecontemp_id',flat=True)  
             
                        experimentalcondQuerySet = ExperimentalParCondTemp.objects.filter(id__in=experimentalcond_ids, active=True)
                  
                        
                        self.fields['experimentalcon'].queryset= ExperimentalParCondTemp.objects.filter(active=True)
                        self.fields['experimentalcon'].initial= experimentalcondQuerySet
                        
                         
                        fileuserutil =  FileUserUtil()
                        #print propertyTempQuerySet[0].pk
                        fileuserutil.seDataProperty(propertyTempQuerySet[0].tag)
                        fileuserutil.setFile(self.instance)
                        fileuserutil.findPointGroupSelectedName('_symmetry_point_group_name_H-M')
                        fileuserutil.setDataProperties()
                        
                        
                        
                        self.fields['pointgroup'].initial = fileuserutil.catalogPointGroupSelectedName
                        
                        self.fields['properties'].queryset = fileuserutil.dataPropertyTempQuerySet
                        self.fields['properties'].initial = propertyTempQuerySet
                        del fileuserutil
                        
                        
                        
                        self.fields['phase_generic'].initial = objDataFileTemp.phase_generic
                        self.fields['phase_name'].initial = objDataFileTemp.phase_name
                        self.fields['chemical_formula'].initial = objDataFileTemp.chemical_formula
                        
                        if objDataFileTemp.cod_code:
                            self.fields['cod_code'].initial = objDataFileTemp.cod_code
                        
                        self.fields['title'].initial = objPublArticleTemp.title
                        self.fields['authors'].initial = objPublArticleTemp.authors
                        self.fields['journal'].initial = objPublArticleTemp.journal
                        self.fields['year'].initial = objPublArticleTemp.year
                        self.fields['volume'].initial = objPublArticleTemp.volume
                        self.fields['issue'].initial = objPublArticleTemp.issue
                        self.fields['first_page'].initial = objPublArticleTemp.first_page
                        self.fields['last_page'].initial = objPublArticleTemp.last_page
                        self.fields['reference'].initial = objPublArticleTemp.reference
                        self.fields['pages_number'].initial = objPublArticleTemp.pages_number
                        
                        datafilepropertytemp_ids=DataFilePropertyTemp.objects.filter(datafiletemp=objDataFileTemp).values_list('id',flat=True) 
                        propertyValuesTempQuerySet= PropertyValuesTemp.objects.filter(datafilepropertytemp_id__in=datafilepropertytemp_ids)
                    except ObjectDoesNotExist as error:
                        print "message in the function extractProperties  for debug purposes Message({0}): {1}".format(99, error.message)  
 
 
 

 
                    urlproperties = reverse('admin:Files_fileuser_property', args=[self.instance.pk]) 
                    urlexperimentalcon = reverse('admin:Files_fileuser_experimental', args=[self.instance.pk]) 
                    urlupdatecoefficients = reverse('admin:Files_fileuser_updatecoefficients', args=[self.instance.pk]) 
                    urlupdatecondition=reverse('admin:Files_fileuser_updatecondition', args=[self.instance.pk]) 
                    #print urlproperties
                    #print urlexperimentalcon
                     
                    javascript =  "<script>"
                    javascript += "var urlproperties = \"" +urlproperties +"\""
                    javascript +="\n"
                    javascript +="var urlexperimentalcon = \"" +urlexperimentalcon +"\""   
                    javascript +="\n"
                    javascript +="var urlupdatecoefficients = \"" +urlupdatecoefficients +"\""   
                    javascript +="\n"
                    javascript +="var urlupdatecondition = \"" +urlupdatecondition +"\""  
                    
                    
                    
                                             
                                            
                                            
                    javascript +=  """
                                                       var listOfSelectMultiple = []
                                                       django.jQuery(function($) {
                                                           $( window ).load(function() {
                                                                  
                                                                  $( "select" ).each(function( index ) {
                                                                          if($( this ).attr('multiple'))
                                                                          {
                                                                                //console.log( index + ": " + $( this ).attr('name'));
                                                                                //console.log( $( this ).attr('id'));
                                                                                
                                                                                domId=$( this ).attr('id');
                                                                                
                                                                                strId= "id_";
                                                                                strFrom= "_from";
                                                                                strTo= "_to";
                                                                                var domName = domId.substring(strId.length, domId.length);
                                                                                var url='';
                                                                                var todo = '';
                                                                                var fullUrl ='';
                                                                                divformrowfield = "div.form-row.field-" ;
                                                                             
                                                                                if (domName.indexOf("_from") >= 0)
                                                                                {
                                                                                    url = domName.substring(0 ,  domName.length - strFrom.length );
                                                                                    todo='from'
                                                                                }
                                                                               
                                                                                if (domName.indexOf("_to") >= 0)
                                                                                {
                                                                                    url = domName.substring(0 ,  domName.length - strTo.length );
                                                                                    todo='to'
                                                                                }
                                                                                    
                                                                                   
                                                                                if(url == 'properties')
                                                                                {
                                                                                   fullUrl = urlproperties;
                                                                                   listOfSelectMultiple[index] = $( this ).attr('id')
                                                                                    
                                                                                }
                                                                                   
                                                                                if(url == 'experimentalcon')
                                                                                {
                                                                                   fullUrl = urlexperimentalcon;
                                                                                   
                                                                                }
                                                                                  
                                                                               
                                                                                divformrowfield = divformrowfield + url;
                                                                                iddivformrowfield = "divformrowfield" + url
                                                                                //console.log($('#' + iddivformrowfield).html());
                                                                                if  ($('#' + iddivformrowfield).html() == null)
                                                                                {
                                                                                    //console.log(  $('#' + iddivformrowfield).html() == null )
                                                                                
                                                                                    //$(divformrowfield).append('<div id="' + iddivformrowfield+ '" style="display:none;" > </div>');
                                                                                    $(divformrowfield).append('<div   id="' + iddivformrowfield+ '" style="border:0px solid black; width: 40%; float: left;  " > </div>');
                                                                                 }
                             
                                                                              //console.log( $( this ).attr('id'));
                                                                              $( this ).click(function() {
                                                                                    iddivformrowfield = "divformrowfield" + url;        
                                                                                    
                                                                                    datasend ={
                                                                                                         'todo': todo,
                                                                                                         'value':$(this).val()[0] 
                                                                                                         }
                                                                                 
                                                                                    callajax(fullUrl, datasend,iddivformrowfield);
                                                                                });
                                                                          }
                                                                    });

                                                                });
            
                                                           /* $(document).ready(function() {
                                                                  django.jQuery("[name=properties]").change(function() {
                                                                        console.log($(this).val());
                                                                    });

                                                            });*/
                                                            
                                                            
                                                         });

                                                    function updatecondition(conditionId)
                                                    {
                                                       var listParams= []
                                                       datasend ={}
                                                       listConditionId= conditionId.split(",")
                                                       for (var i=0; i <  (listConditionId.length); i++) 
                                                       {
                                                           extra = listConditionId[i].split("=")
                                                           if (extra.length > 1)
                                                           {
                                                              //console.log(listConditionId[i] );
                                                              if (extra[0] =='labelmsgid')
                                                              {
                                                                  django.jQuery('#' + extra[1]).text('');
                                                                  id_to_display_result =  extra[1]
                                                              }
                                                              else
                                                              {
                                                                  datasend[extra[0]]= extra[1]
                                                              }
                                              
                                                            //datasend[extra[0]]= extra[1]
                                                 
                                                    
                                                              //console.log(extra[1]);
                                                              
                                                           }
                                                           else
                                                           {
                                                              datasend[listConditionId[i] ]=  django.jQuery('#' + listConditionId[i]).val();
                                                            }
                                                       }
                                                       
                                                       
                                                       datasend['todo'] = 'update';
                                                 
                                                            
                                                       console.log(datasend)
                                                       
                                                        
                                                       fullUrl = urlupdatecondition;
                                                       callajax(fullUrl, datasend,id_to_display_result)
       
                                                       
                                                    }
                                                 
                                                    function updatecoefficient(coeffTags)
                                                    {
                                                       var listParams= []
                                                       datasend ={}
                                                       listCoeffTags = coeffTags.split(",")
                                                       for (var i=0; i <  (listCoeffTags.length); i++) 
                                                       {
                                                           extra = listCoeffTags[i].split("=")
                                                           if (extra.length > 1)
                                                           {
                                                              //console.log(listCoeffTags[i] );
                                                              if (extra[0] =='idupdatemessage_id')
                                                              {
                                                                  django.jQuery('#' + extra[1]).text('');
                                                                  id_to_display_result =  extra[1]
                                                              }
                                                              else
                                                              {
                                                                  datasend[extra[0]]= extra[1].replace(/\s/g, '');
                                                            }
                                                 
                                                    
                                                              //console.log(extra[1]);
                                                              
                                                           }
                                                           else
                                                           {
                                                              datasend[listCoeffTags[i] ]=  parseFloat(django.jQuery('#' + listCoeffTags[i]).val());
                                                            }
                                                       }
                                                       
                                                       
                                                       datasend['todo'] = 'update';
                                                 
                                                            
                                                       //console.log(datasend)
                                                       
                                                        
                                                       fullUrl = urlupdatecoefficients;
                                                       callajax(fullUrl, datasend,id_to_display_result)
       
                                                       
                                                    }
        
                                                    
                                                    function  callajax(url, datasend,id_to_display_result)
                                                    {
                                                         var csrftoken = django.jQuery("[name=csrfmiddlewaretoken]").val();
                                                         function csrfSafeMethod(method) {
                                                                // these HTTP methods do not require CSRF protection
                                                                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                                                            }
                                                                                                   
                                                           // start django.jQuery
                                                             django.jQuery(function($) {
                                                             
                                                               // prepare ajax
                                                                $.ajaxSetup({
                                                                    beforeSend: function(xhr, settings) {
                                                                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                                                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                                                        }
                                                                    }
                                                                });
                                                                
                                                               
                                                               for (var i=0; i <  (listOfSelectMultiple.length); i++) 
                                                               {
                                                                    if($('#' + listOfSelectMultiple[i]).val() != null)
                                                                    {
                                                                       //console.log(listOfSelectMultiple[i]);
                                                                       //console.log($('#' + listOfSelectMultiple[i]).val());
                                                                       datasend[listOfSelectMultiple[i]] = $('#' + listOfSelectMultiple[i]).val()[0];
                                                                   }
                                                               }
                                                               
                                                               console.log(datasend);
                                                            // start ajax
                                                                $.ajax({
                                                                url : url,  
                                                                type: "POST",  
                                                                dataType: 'json',
                                                                data : datasend, 
                                                                success: function (data) {
                                              
                                                                    console.log("success"); // another sanity check
                                                                    
 
                                                                    
                                                                    html = django.jQuery('#' + id_to_display_result).html( );
                                                                    if(django.jQuery('#' + id_to_display_result).html( ) == null) 
                                                                    {
                                                                        django.jQuery('#' + id_to_display_result).text( data.result ); 
                                                                         
                                                                    }
                                                                    else
                                                                    {
                                                                        django.jQuery('#' + id_to_display_result).empty();
                                                                        django.jQuery('#' + id_to_display_result).html( data.result );
                                                                        django.jQuery('#' + id_to_display_result).show();
                                                                    }
                                                                    
                                                                    
                                                                    
                                                                    
                                                                },
                                                        
                                                                // handle a non-successful response
                                                                error : function(xhr,errmsg,err) {
                                                                    $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                                                                        " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                                                                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                                                                }
                                                            });
                                                            
                                                            //end ajax
                                                         });
                                                         // end django.jQuery
                                                    
                                                    }
                                                    </script>
                                        
                                        """
                    self.fields['jquery'].initial = javascript
                    
        else:
            if args:#save  new
                pass
            else:#add new
                pass
        
        
class CategoryModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        # Return a string of the format: "description  (name)"
        return "%s (%s)"%( obj.description,obj.name)  
        
class DictionaryForm(forms.ModelForm):
    category = CategoryModelChoiceField(Category.objects.all().order_by('description'))
    class Meta:
        model = Dictionary    
        
        
class CatalogPropertyAdminForm(forms.ModelForm):  
    class Meta:
        model = CatalogProperty
        
    def __init__(self, *args, **kwargs):   
        super(CatalogPropertyAdminForm, self).__init__(*args, **kwargs)