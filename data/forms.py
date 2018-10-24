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

from data.Utils import *

from  ctypes import *
 
 
 
 
 
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
                    self.fields[ ipt.name] = forms.FloatField(forms.CharField(required=True,help_text=str(ipt.name) + "Enter value" ,label= ipt.name))

                    """if   's' in ipt.name:
                        self.fields[ ipt.name] = forms.FloatField(forms.CharField(required=True,help_text=str(ipt.name) + "Enter value" ,label= ipt.name))
                        
                    if   'c' in ipt.name:
                        self.fields[ ipt.name] = forms.FloatField(forms.CharField(required=True,help_text=str(ipt.name) + "Enter value" ,label= ipt.name))
                        
                    if   'd' in ipt.name:
                        self.fields[ ipt.name] = forms.FloatField(forms.CharField(required=True,help_text=str(ipt.name) + "Enter value" ,label= ipt.name))
                    """



             
         

 


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
                PuntualGroupNames.objects.get(name__exact=name) 
                raise forms.ValidationError("There is already a group with the selecteds 'puntual groups'. use that group or the group name already exist")
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
                puntualgroupnamesSelected=PuntualGroupNames.objects.get(id=self.instance.id)
                puntualgroupnamesQuerySet =  PuntualGroupGroups.objects.filter(puntualgroupnames=self.instance)
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
                catalogpointgroup_ids =  PuntualGroupGroups.objects.filter(puntualgroupnames=self.instance).values_list('catalogpointgroup_id',flat=True)  
                catalogpointgroupQuerySet=CatalogPointGroup.objects.filter(id__in=catalogpointgroup_ids)
                self.fields['name'].initial=self.instance.name
                self.fields['description'].initial=self.instance.name   
                self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()
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
    
    def clean_puntualgroupnames(self):
        puntualgroupnames = self.cleaned_data['puntualgroupnames']
        
        return puntualgroupnames
    
    def clean_catalogpointgroup(self):
        catalogpointgroup = self.cleaned_data['catalogpointgroup']
        
        return catalogpointgroup
    
    
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
            
            type_id  = argsToInt(args,'type') 
            dataproperty_id =  argsToInt(args,'dataproperty')
            catalogcrystalsystem_id =  argsToInt(args,'catalogcrystalsystem')
            catalogpointgroup_id = argsToInt(args,'catalogpointgroup',45)
            puntualgroupnames_id  =  argsToInt(args,'puntualgroupnames',21)
            axis_id  = argsToInt(args,'axis',4)
            coefficients_ids = argsListToIntList(args,'coefficients')
  
             
            
               
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
        self.fields['catalogpointgroup'] = forms.ModelChoiceField(queryset=None,label="Point Group",required=True)
        self.fields['catalogpointgroup'].widget=forms.Select(attrs={"onChange":'submit()'})
        self.fields['catalogpointgroup'].empty_label = None
        self.fields['puntualgroupnames'] =  forms.ModelChoiceField(queryset=None,label="Groups",required=True)
        self.fields['puntualgroupnames'].widget=forms.Select(attrs={"onChange":'submit()'})
        self.fields['puntualgroupnames'].empty_label = None
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

        #self.fields['crysralsystemdetail'] = forms.CharField(label='Crystal System Detail',widget = DetailFieldWidget, required=False)
        self.fields['pointgroupdetail'] = forms.CharField(label='Point Group Detail',widget = DetailFieldWidget, required=False)
        self.fields['puntualgroupnamesdetail'] = forms.CharField(label='Groups Detail',widget = DetailFieldWidget, required=False)
        self.fields['axisdetail'] = forms.CharField(label='Axis Detail',widget = DetailFieldWidget, required=False)
        self.fields['errormessage'] = forms.CharField(widget = DetailFieldWidget, required=False)
         
  
        typeSelected = None
        datapropertySelected = None
        catalogcrystalsystemSelected = None
        catalogpointgroupSelected = None
        puntualgroupnamesSelected = None
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
                datapropertyQuerySet=Property.objects.filter(id__in=dataproperty_ids)   
                self.fields['dataproperty'].queryset=datapropertyQuerySet
                datapropertySelected = Property.objects.get(id=int(dataproperty_id))  
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
                
                
                #*******************************puntualgroupnames*************************************
                puntualgroupnamesSelected = PuntualGroupNames.objects.get(id=int(puntualgroupnames_id))  
                self.fields['puntualgroupnames'].queryset = PuntualGroupNames.objects.all()
                self.fields['puntualgroupnames'].initial = puntualgroupnamesSelected
                self.fields['puntualgroupnamesdetail'].initial = "<strong>groups assigned</strong>"
                
                #*******************************axis*************************************
                axisSelected = CatalogAxis.objects.get(id=int(axis_id))  
                self.fields['axis'].queryset = PuntualGroupNames.objects.all()
                self.fields['axis'].initial = puntualgroupnamesSelected
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
                        datapropertyQuerySet=Property.objects.filter(id__in=dataproperty_ids)   
                        self.fields['dataproperty'].queryset=datapropertyQuerySet
                        if dataproperty_id in dataproperty_ids:
                            datapropertySelected = Property.objects.get(id=int(dataproperty_id))  
                        else:
                            datapropertySelected = datapropertyQuerySet[0]
                            
                        self.fields['dataproperty'].initial  = datapropertySelected
                        
                        #*******************************catalogcrystalsystem*************************************
                        catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty= self.instance)   
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
                            pointgroupQuerySet=CatalogPointGroup.objects.filter(id=45)
                            self.fields['catalogpointgroup'].queryset = pointgroupQuerySet
                            
                            catalogpointgroup_ids =CatalogPointGroup.objects.all().values_list('id',flat=True) 
                            if catalogpointgroup_id in catalogpointgroup_ids:
                                catalogpointgroupSelected = CatalogPointGroup.objects.get(id=catalogpointgroup_id)
                            else:
                                catalogpointgroupSelected = CatalogPointGroup.objects.get(id=45)
                                
                            self.fields['catalogpointgroup'].initial = catalogpointgroupSelected
                            self.fields['pointgroupdetail'].initial = "<strong>punctual group not assigned</strong>"

                        
                        #*******************************puntualgroupnames*************************************
                        puntualgroupnames_ids= CrystalSystemPuntualGroupNames.objects.filter(catalogcrystalsystem=catalogcrystalsystemSelected,type=typeSelected,active=1).values_list('puntualgroupnames_id',flat=True)  
                        if puntualgroupnames_ids:
                            puntualgroupnamesQuerySet = PuntualGroupNames.objects.filter(id__in=puntualgroupnames_ids)
                            """if checkPuntualGroupNames(typeSelected, catalogcrystalsystemSelected,datapropertySelected):
                            puntualgroupnamesQuerySet,puntualGroupsQuerySet =setPuntualGroupNames(typeSelected, catalogcrystalsystemSelected,datapropertySelected)
                            puntualgroupnames_ids = getIdsFromQuerySet(puntualgroupnamesQuerySet)"""
                            
                            fieldsList = ['name','description']
                            html = getTableHTMLFromQuerySet(puntualgroupnamesQuerySet,fields=fieldsList)
                            if puntualgroupnames_id in puntualgroupnames_ids:
                                puntualgroupnamesSelected = PuntualGroupNames.objects.get(id=int(puntualgroupnames_id))  
                                self.fields['puntualgroupnamesdetail'].initial = html
                                self.fields['puntualgroupnames'].help_text = "Group assigned,  all the point groups of this crystal system have the same matrix" 
                            else:
                                puntualgroupnamesSelected =puntualgroupnamesQuerySet[0]  
                                self.fields['puntualgroupnamesdetail'].initial = html
                                self.fields['puntualgroupnames'].help_text = "Groups not assigned, Select this option if all groups of points in this crystal system have the same matrix" 

                            self.fields['puntualgroupnames'].queryset = puntualgroupnamesQuerySet
                            self.fields['puntualgroupnames'].initial = puntualgroupnamesSelected
                            
                        else:
                            puntualGroupNamesQuerySet = PuntualGroupNames.objects.filter(id=21)
                            self.fields['puntualgroupnames'].queryset = puntualGroupNamesQuerySet
                            
                            puntualgroupnames_ids =PuntualGroupNames.objects.all().values_list('id',flat=True) 
                            puntualgroupnamesSelected = PuntualGroupNames.objects.get(id=int(puntualgroupnames_id))  
                            if puntualgroupnames_id in puntualgroupnames_ids:
                                puntualgroupnamesSelected = PuntualGroupNames.objects.get(id=int(puntualgroupnames_id))  
                            else:
                                puntualgroupnamesSelected = PuntualGroupNames.objects.get(id=21)
                             
                            self.fields['puntualgroupnames'].initial = puntualgroupnamesSelected
                            self.fields['puntualgroupnamesdetail'].initial = "<strong>Group not assigned</strong>"
                            
                        
                        
                        #*******************************axis*************************************
                        axis_ids= CrystalSystemAxis.objects.filter(catalogcrystalsystem=catalogcrystalsystemSelected,type=typeSelected,catalogpointgroup= catalogpointgroupSelected,puntualgroupnames = puntualgroupnamesSelected,active=1).values_list('axis_id',flat=True)  
                        if axis_ids:
                            axisQuerySet = CatalogAxis.objects.filter(id__in=axis_ids)
                            """if checkAxis(typeSelected, catalogcrystalsystemSelected,datapropertySelected):  
                            axisQuerySet= setAxis(typeSelected, catalogcrystalsystemSelected,datapropertySelected)
                            axis_ids = getIdsFromQuerySet(axisQuerySet)"""
                           
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
                            axis_ids=  CatalogAxis.objects.all().values_list('id',flat=True) 
                            if axis_id in axis_ids:
                                axisSelected = CatalogAxis.objects.get(id=int(axis_id))  
                            else:
                                axisSelected = CatalogAxis.objects.get(id=4)
                                
                            self.fields['axis'].initial = axisSelected
                            self.fields['axisdetail'].initial = "<strong>axis not assigned</strong>"
                            
                        
                    
                else:
                    typeSelected = typeQuerySet[0]
                    self.fields['type'].initial= typeSelected
                    
                    #*******************************dataproperty*************************************
                    dataproperty_ids=TypeDataProperty.objects.filter(type=typeSelected).values_list('dataproperty_id',flat=True)    
                    datapropertyQuerySet=Property.objects.filter(id__in=dataproperty_ids)   
                    self.fields['dataproperty'].queryset=datapropertyQuerySet
                    datapropertySelected = datapropertyQuerySet[0]
                    self.fields['dataproperty'].initial  = datapropertySelected
                    catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty= self.instance)   
                    
                    #*******************************catalogcrystalsystem*************************************
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
                    
                    
                        """if checkPointGroup(typeSelected, catalogcrystalsystemSelected,datapropertySelected):  
                        pointgroupQuerySet = setPointGroup(typeSelected, catalogcrystalsystemSelected,datapropertySelected)"""
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
            
                    #*******************************puntualgroupnames*************************************
                    
                    
                    puntualgroupnames_ids= CrystalSystemPuntualGroupNames.objects.filter(catalogcrystalsystem=catalogcrystalsystemSelected,type=typeSelected,active=1).values_list('puntualgroupnames_id',flat=True)  
                    if puntualgroupnames_ids:
                        puntualgroupnamesQuerySet = PuntualGroupNames.objects.filter(id__in=puntualgroupnames_ids)
                        
                    
                        """if checkPuntualGroupNames(typeSelected, catalogcrystalsystemSelected,datapropertySelected):
                        puntualgroupnamesQuerySet,puntualGroupsQuerySet =setPuntualGroupNames(typeSelected, catalogcrystalsystemSelected,datapropertySelected)"""
                        puntualgroupnamesSelected = puntualgroupnamesQuerySet[0]
                        self.fields['puntualgroupnames'].queryset = puntualgroupnamesQuerySet
                        self.fields['puntualgroupnames'].initial = puntualgroupnamesSelected
                        self.fields['puntualgroupnames'].help_text = "Group assigned, all the point groups of this crystal system have the same matrix" 
                        fieldsList = ['name','description']
                        html = getTableHTMLFromQuerySet(puntualgroupnamesQuerySet,fields=fieldsList)
                                    
                        self.fields['puntualgroupnamesdetail'].initial = html
                    else:
                        puntualGroupNamesQuerySet = PuntualGroupNames.objects.filter(id=21)
                        self.fields['puntualgroupnames'].queryset = puntualGroupNamesQuerySet
                        self.fields['puntualgroupnames'].help_text = "Select this option if all groups of points in this crystal system have the same matrix" 
                        puntualgroupnamesSelected = PuntualGroupNames.objects.get(id=21)
                        self.fields['puntualgroupnames'].initial = puntualgroupnamesSelected
                        self.fields['puntualgroupnamesdetail'].initial = "<strong>groups not assigned</strong>"
                    
                    #*******************************axis*************************************
                    
                    axis_ids= CrystalSystemAxis.objects.filter(catalogcrystalsystem=catalogcrystalsystemSelected,type=typeSelected,catalogpointgroup= catalogpointgroupSelected,puntualgroupnames = puntualgroupnamesSelected,active=1).values_list('axis_id',flat=True)  
                    if axis_ids:
                        axisQuerySet = CatalogAxis.objects.filter(id__in=axis_ids)
                    
                        """if checkAxis(typeSelected, catalogcrystalsystemSelected,datapropertySelected):  
                        axisQuerySet= setAxis(typeSelected, catalogcrystalsystemSelected,datapropertySelected)"""
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
                        
                    
            catalogPropertyDetailQuerySet, catalogPropertyDetailList = setCoefficients(typeSelected, catalogcrystalsystemSelected,datapropertySelected,catalogpointgroupSelected,puntualgroupnamesSelected,axisSelected)
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

 
            
        
class CatalogCrystalSystemAdminForm(forms.ModelForm):  
    
    class Meta:
        model = CatalogCrystalSystem
        
    def clean(self,*args,**kwargs):
         
        puntualgroupnames=self.cleaned_data.get("puntualgroupnames")
        catalogpointgroup=self.cleaned_data.get("catalogpointgroup")
        if not catalogpointgroup and not puntualgroupnames:
            raise forms.ValidationError("the 'Point Group' or 'Groups' fields are not selected, you must select one of the two!")
        
        if  catalogpointgroup  and  puntualgroupnames:
            if  (catalogpointgroup.id == 45  and  puntualgroupnames.id  != 21 ) or (catalogpointgroup.id  != 45  and  puntualgroupnames.id == 21):
                pass
            elif (catalogpointgroup.id  != 45  and  puntualgroupnames.id == 21):
                pass
            elif (catalogpointgroup.id  != 45  and  puntualgroupnames.id != 21):
                raise forms.ValidationError("the 'Point Group' or 'Groups' fields have selected options, you must select one of the two!")

        return super(CatalogCrystalSystemAdminForm,self).clean(*args,**kwargs)
    
    def clean_puntualgroupnames(self):
        puntualgroupnames = self.cleaned_data['puntualgroupnames']
        return puntualgroupnames
    
    def clean_catalogpointgroup(self):
        catalogpointgroup = self.cleaned_data['catalogpointgroup']
        return catalogpointgroup    
        
    def __init__(self, *args, **kwargs):   
        catalogproperty_id = None
        puntualgroupnames_id  = None
        catalogpointgroup_id = None
        onchange = False
        if args: #(true if edit and save or save an existing instance, when form was changed), false when instance was selected from change list
            type_id =  argsToInt(args,'type')
            catalogproperty_id =  argsToInt(args,'catalogproperty')
            catalogpointgroup_id = argsToInt(args,'catalogpointgroup',45)
            puntualgroupnames_id  =  argsToInt(args,'puntualgroupnames',21)
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
        self.fields['catalogpointgroup'] = forms.ModelChoiceField(queryset=None,label="Point Group",required=True)
        self.fields['catalogpointgroup'].widget=forms.Select()
        self.fields['catalogpointgroup'].empty_label = None
        self.fields['puntualgroupnames'] =  forms.ModelChoiceField(queryset=None,label="Groups",required=True)
        self.fields['puntualgroupnames'].widget=forms.Select()
        self.fields['puntualgroupnames'].empty_label = None
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
        self.fields['puntualgroupnamesdetail'] = forms.CharField(label='Groups Detail',widget = DetailFieldWidget,required=False)
        self.fields['axisdetail'] = forms.CharField(label='Axis Detail',widget = DetailFieldWidget,required=False)
 
        
        typeSelected = None
        datapropertySelected = None
        catalogcrystalsystemSelected = None
        catalogpointgroupSelected = None
        puntualgroupnamesSelected = None
        axisSelected = None
        if self.instance.pk: 
            if args:
                #*******************************type*************************************          
                typeSelected = Type.objects.get(id=type_id)
                typeQuerySet=Type.objects.filter(active=True,catalogproperty= self.instance.catalogproperty)   
                self.fields['type'].queryset = typeQuerySet
                self.fields['type'].initial = typeSelected
                
                #*******************************catalogpointgroup*************************************                
                catalogpointgroupSelected = CatalogPointGroup.objects.get(id=int(catalogpointgroup_id))
                self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()
                self.fields['catalogpointgroup'].initial = catalogpointgroupSelected
                self.fields['pointgroupdetail'].initial = "<strong>punctual group assigned</strong>"

                #*******************************puntualgroupnames*************************************
                puntualgroupnamesSelected = PuntualGroupNames.objects.get(id=int(puntualgroupnames_id))  
                self.fields['puntualgroupnames'].queryset = PuntualGroupNames.objects.all()
                self.fields['puntualgroupnames'].initial = puntualgroupnamesSelected
                self.fields['puntualgroupnamesdetail'].initial = "<strong>groups assigned</strong>"
                
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
                    
                    #puntualgroupnamesSelected = PuntualGroupNames.objects.filter(id=puntualgroupnames_id)
                    #catalogpointgroupSelected = CatalogPointGroup.objects.get(id= catalogpointgroup_id)
                    
                    #*******************************puntualgroupnames*************************************
                    puntualgroupnames_ids= CrystalSystemPuntualGroupNames.objects.filter(catalogcrystalsystem=self.instance,type=typeSelected,active =1).values_list('puntualgroupnames_id',flat=True) 
                    if puntualgroupnames_ids:
                        puntualGroupNamesQuerySet= PuntualGroupNames.objects.filter(id__in=puntualgroupnames_ids)
                        self.fields['puntualgroupnames'].queryset = PuntualGroupNames.objects.all()
                        self.fields['puntualgroupnames'].initial =puntualGroupNamesQuerySet[0]
                        puntualgroupnamesSelected= puntualGroupNamesQuerySet[0]
                        html = getTableHTMLFromQuerySet(puntualGroupNamesQuerySet)
                        self.fields['puntualgroupnamesdetail'].initial = html
                        self.fields['puntualgroupnames'].help_text = "Assigned group, all groups of points in this crystal system will have the same matrix" 
                    else:
                        puntualGroupNamesQuerySet = PuntualGroupNames.objects.all()
                        puntualgroupnamesSelected= PuntualGroupNames.objects.get(id=21)
                        self.fields['puntualgroupnames'].queryset =  puntualGroupNamesQuerySet
                        self.fields['puntualgroupnames'].initial =  PuntualGroupNames.objects.get(id=21)
                        self.fields['puntualgroupnamesdetail'].initial = "<strong>Group not assigned</strong>"
                        
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
                    axis_ids=  CrystalSystemAxis.objects.filter(catalogcrystalsystem=self.instance,type=typeSelected,catalogpointgroup= catalogpointgroupSelected,puntualgroupnames = puntualgroupnamesSelected,active = 1).values_list('axis_id',flat=True)  
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
    
                    puntualgroupnames_ids= CrystalSystemPuntualGroupNames.objects.filter(catalogcrystalsystem=self.instance,type=typeSelected,active =1).values_list('puntualgroupnames_id',flat=True) 
                     
                    if puntualgroupnames_ids:
                        puntualGroupNamesQuerySet= PuntualGroupNames.objects.filter(id__in=puntualgroupnames_ids)
                        self.fields['puntualgroupnames'].queryset =  PuntualGroupNames.objects.all()
                        self.fields['puntualgroupnames'].initial = puntualGroupNamesQuerySet[0]
                        puntualgroupnamesSelected = puntualGroupNamesQuerySet[0]
                        fieldsList = ['name','description']
                        html = getTableHTMLFromQuerySet(puntualGroupNamesQuerySet,fields=fieldsList)
                        self.fields['puntualgroupnamesdetail'].initial = html
                        self.fields['puntualgroupnames'].help_text = "Assigned group, all groups of points in this crystal system will have the same matrix" 
                    else:
                        self.fields['puntualgroupnames'].queryset =  PuntualGroupNames.objects.all()
                        puntualgroupnamesSelected = PuntualGroupNames.objects.get(id=21)
                        self.fields['puntualgroupnames'].initial = puntualgroupnamesSelected
                        self.fields['puntualgroupnamesdetail'].initial = "<strong>Group not assigned</strong>"

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

                    axis_ids=  CrystalSystemAxis.objects.filter(catalogcrystalsystem=self.instance,type=typeSelected,catalogpointgroup= catalogpointgroupSelected,puntualgroupnames = puntualgroupnamesSelected,active = 1).values_list('axis_id',flat=True)  
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
                
                
                #*******************************catalogpointgroup*************************************                
                catalogpointgroupSelected = CatalogPointGroup.objects.get(id=int(catalogpointgroup_id))
                self.fields['catalogpointgroup'].queryset = CatalogPointGroup.objects.all()
                self.fields['catalogpointgroup'].initial = catalogpointgroupSelected
                self.fields['pointgroupdetail'].initial = "<strong>punctual group assigned</strong>"

                #*******************************puntualgroupnames*************************************
                puntualgroupnamesSelected = PuntualGroupNames.objects.get(id=int(puntualgroupnames_id))  
                self.fields['puntualgroupnames'].queryset = PuntualGroupNames.objects.all()
                self.fields['puntualgroupnames'].initial = puntualgroupnamesSelected
                self.fields['puntualgroupnamesdetail'].initial = "<strong>groups assigned</strong>"
                
                #*******************************axis*************************************
                axisSelected = CatalogAxis.objects.get(id__in=axis_ids)
                self.fields['axis'].queryset = PuntualGroupNames.objects.all().exclude(id=4)
                self.fields['axis'].initial = puntualgroupnamesSelected
                self.fields['axisdetail'].initial = "<strong>groups assigned</strong>"
                
                
                
            else:#add new
                #*******************************type*************************************
                typeQuerySet=Type.objects.all()   
                self.fields['type'].queryset= typeQuerySet
                self.fields['type'].initial= typeQuerySet[0]
            
                
                #*******************************puntualgroupnames*************************************
                self.fields['puntualgroupnames'].queryset =  PuntualGroupNames.objects.all()
                self.fields['puntualgroupnamesdetail'].initial = "<strong>Group not assigned</strong>"
                #*******************************catalogpointgroup*************************************        
                self.fields['catalogpointgroup'].queryset =CatalogPointGroup.objects.all()
                self.fields['pointgroupdetail'].initial = "<strong>punctual group not assigned</strong>"
                
                
                #*******************************axis*************************************
                self.fields['axis'].queryset =  CatalogAxis.objects.all().exclude(id=4)
                self.fields['axisdetail'].initial = "<strong>Axis  not assigned</strong>"
        
        
  
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
        published = None
 
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
            published = argsCheck(args,'published') 
            
            
            if not args[0].has_key('_save') and not args[0].has_key('_addanother') and not args[0].has_key('_continue'):    
                args ={}
                onchange = True
                
        super(FileUserAdminForm, self).__init__(*args, **kwargs)
        
        #define field to form page
         
        self.fields['fileuserid']  = forms.CharField(label="")
        self.fields['fileuserid'].widget = forms.HiddenInput()
        #self.fields['fileuserid'].empty_label = None
        

        
        self.fields['properties'] = forms.ModelMultipleChoiceField(
            queryset=None,
            required=False,
            label="Properties",
            widget=FilteredSelectMultiple(
                verbose_name='Property',
                is_stacked=False,
                attrs={"ondblclick":"getProperty(this)"}
            )

        )
        
        
 
 
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
        self.fields['title']  = forms.CharField(label='Title')
        self.fields['title'].widget = forms.TextInput() 
        
        self.fields['authors']  = forms.CharField(label='Authors')
        self.fields['authors'].widget = forms.TextInput() 
        
        self.fields['journal']  = forms.CharField(label='Journal')
        self.fields['journal'].widget = forms.TextInput() 
        
        self.fields['year']  = forms.CharField(label='Year')
        self.fields['year'].widget = forms.TextInput() 
        
        self.fields['volume']  = forms.CharField(label='Volume')
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
        
        
        
        if self.instance.pk: 
            if args:
                    if published:
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
                    propertyTempQuerySet= PropertyTemp.objects.filter(id__in=properties_ids)

                    experimentalcondQuerySet = ExperimentalParCondTemp.objects.filter(id__in=experimentalcond_ids)
                    self.fields['experimentalcon'].queryset= ExperimentalParCondTemp.objects.all()
                    self.fields['experimentalcon'].initial= experimentalcondQuerySet

                    self.fields['properties'].queryset = PropertyTemp.objects.all() 
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
                    
                    
                    #self.instance.datafile
                    if  self.instance.datafile:
                        #self.fields['filenamepublished'].label = mark_safe("<a href='%s'>File name published </a>") % (reverse('get_datafile', args=[self.instance.datafile.filename]))
                        self.fields['filenamepublished'].initial = "<a href='/datafiles/" + self.instance.datafile.filename  +"' target='_blank'>"  + self.instance.datafile.filename  +"</a>"
                    else:
                        self.fields['filenamepublished'].initial = ""
                        
                        
                        

                  
                    
                        
                    
                    objDataFileTemp = DataFileTemp.objects.get(filename__exact=self.instance.filename)
                    objPublArticleTemp = objDataFileTemp.publication
                    propertyTempQuerySet= objDataFileTemp.properties.all()
                    experimentalcond_ids = ExperimentalfilecontempDatafiletemp.objects.filter(datafiletemp=objDataFileTemp).values_list('experimentalfilecontemp_id',flat=True)  
                   
                    #self.fields['reportvalidationcustom'].initial = "<strong><font color='black'>" + self.instance.reportvalidation +" </font></strong>" 
                    #self.fields['reportvalidation'].initial= self.instance.reportvalidation
                   
                    experimentalcondQuerySet = ExperimentalParCondTemp.objects.filter(id__in=experimentalcond_ids)
                    """self.fields['experimentalcon'].queryset= experimentalcondQuerySet
                    self.fields['experimentalcon'].initial= experimentalcond_ids
                    """
                    
                    self.fields['experimentalcon'].queryset= ExperimentalParCondTemp.objects.all()
                    self.fields['experimentalcon'].initial= experimentalcondQuerySet
                    
                     
                    self.fields['properties'].queryset = PropertyTemp.objects.all() 
                    self.fields['properties'].initial = propertyTempQuerySet
                    
                    self.fields['phase_generic'].initial = objDataFileTemp.phase_generic
                    self.fields['phase_name'].initial = objDataFileTemp.phase_name
                    self.fields['chemical_formula'].initial = objDataFileTemp.chemical_formula
                    
                    if objDataFileTemp.cod_code:
                        self.fields['cod_code'] = objDataFileTemp.cod_code
                    
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
        else:
            if args:#save  new
                pass
            else:#add new
                pass
        