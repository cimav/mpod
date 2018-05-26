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

    

                

           
              
        
        
class TypeDataPropertyAdminForm(forms.ModelForm):
    #product = forms.ModelChoiceField(queryset=Product.objects.all())
    catalogproperty = forms.ModelChoiceField(queryset=None,label="Property")
    #catalogcrystalsystem = forms.ModelMultipleChoiceField(queryset=None,label="Crystal System")
 
    #catalogcrystalsystem =forms.ModelChoiceField(queryset=None,label="Crystal System",widget=forms.Select(attrs={"onChange":"refreshdetail(this,'crystalsystemchange')"}))
    catalogcrystalsystem =forms.ModelChoiceField(queryset=None,label="Crystal System")
    
    
    #quantity = forms.IntegerField(min_value=1, label="Coefficients to capture" , required=True,)
    populate =  forms.BooleanField(required=False,label="Populated")
    axis=forms.ModelChoiceField(queryset=None,label="Axis", required=False,)
    #catalogpointgroup = forms.ModelMultipleChoiceFieldChoiceField(queryset=None,label="Point Group")
    catalogpointgroup = forms.ModelMultipleChoiceField(
            queryset=None,
            required=False,
            label="Point Groups",
            widget=FilteredSelectMultiple(
                verbose_name='Point groups',
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
    
    def empty(self):
        pass

    coefficients.validate=empty
    
    
        
    puntualgroupnames = forms.ModelChoiceField(queryset=None,label="Groups", required=False,)
    #catalogpropertydetail = forms.ModelChoiceField(queryset=None,label="Coefficients detail")
    #name = forms.CharField(widget=forms.TextInput(),max_length=15,label=mark_safe('Your Name (<a href="/questions/whyname/" target="_blank">why</a>?)'))
     
    dataproperty = forms.ModelChoiceField(queryset=None,label="Data Property")
    
    class Meta:
        model = TypeDataProperty
     
    def setPointGroups(self,objTypeSelected,objCatalogCrystalSystemSelected):                                  
        propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected).values('puntualgroupnames').annotate(total=Count('puntualgroupnames'))
        puntualGroupsList=[]
        for d in propertyDetail:
            #if d['puntualgroupnames'] != 21:   
                #print d['puntualgroupnames']              
            objPuntualgroupnames=PuntualGroupNames.objects.filter(id__exact=d['puntualgroupnames']) 
            objPuntualGroupGroups = PuntualGroupGroups.objects.filter(puntualgroupnames=objPuntualgroupnames)    
            for obj in objPuntualGroupGroups:
                pgg=PuntualGroupGroups()
                pgg=obj
                puntualGroupsList.append(pgg.puntualgroupnames.id)

        return puntualGroupsList
    
    def checkPointGroup(self,objTypeSelected,objCatalogCrystalSystemSelected):
        propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected).values('catalogpointgroup').annotate(total=Count('catalogpointgroup'))
        for d in propertyDetail:  
            if d['catalogpointgroup'] != 45:  
                return True
            else:
                return False
    
    def checkPuntualGroupNames(self,objTypeSelected,objCatalogCrystalSystemSelected):        
        propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected).values('puntualgroupnames').annotate(total=Count('puntualgroupnames'))
        for d in propertyDetail:
            if d['puntualgroupnames'] != 21:   
                return True
            else:
                return False
                
                
                        
    def setPointGroup(self,objTypeSelected,objCatalogCrystalSystemSelected):  
        propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected).values('catalogpointgroup').annotate(total=Count('catalogpointgroup'))
        puntualGroupList = []
        for d in propertyDetail:  
            if d['catalogpointgroup'] != 45:       
                #print d['catalogpointgroup']  
                objCatalogPointGroup=CatalogPointGroup.objects.filter(id__exact=d['catalogpointgroup'])         
                for obj in  objCatalogPointGroup:
                    cpg=CatalogPointGroup()
                    cpg=obj        
                    puntualGroupList.append(cpg.id)                       
    
                                                            
        propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected).values('puntualgroupnames').annotate(total=Count('puntualgroupnames'))
         
        for d in propertyDetail:
            if d['puntualgroupnames'] != 21:   
                #print d['puntualgroupnames']              
                objPuntualgroupnames=PuntualGroupNames.objects.filter(id__exact=d['puntualgroupnames']) 
                objPuntualGroupGroups = PuntualGroupGroups.objects.filter(puntualgroupnames=objPuntualgroupnames)    
                for obj in objPuntualGroupGroups:
                    pgg=PuntualGroupGroups()
                    pgg=obj
                    puntualGroupList.append(pgg.catalogpointgroup.id)
                    
        return puntualGroupList
                    
    def setAxis(self,objTypeSelected,objCatalogCrystalSystemSelected):
        propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected).values('catalogaxis').annotate(total=Count('catalogaxis'))
        axisList = []
        for d in propertyDetail:  
            #if d['catalogaxis'] != 4:       
                #print d['catalogaxis']  
            objCatalogAxis=CatalogAxis.objects.filter(id=d['catalogaxis'] )
            for obj in objCatalogAxis:
                ca=CatalogAxis()
                ca=obj
                #print ca.name
                axisList.append(ca.id)
                    
        return  axisList   
    
    def isnumber(self,param):
        result = False
        try:
            val = float(param)
            result = True
            return result
        except ValueError:
            print("That's not an int!")
            return result
       
    def __init__(self, *args, **kwargs):
       
        typedataproperty = kwargs.pop('instance', None)
        if typedataproperty != None:
            try:
            
                super(TypeDataPropertyAdminForm, self).__init__(*args, **kwargs) 
                 
                
                #print "id_type " +str( typedataproperty.type.id)
     
                ids=CatalogProperty.objects.filter(id=typedataproperty.type.catalogproperty.id).values_list('id', flat=True) 
                catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty_id__in=ids)   
                
                #print "id_crystalsystem " +str( catalogcrystalsystemQuerySet[0].id)
    
                ids=CatalogProperty.objects.filter(name=typedataproperty.type.catalogproperty.name).values_list('id', flat=True)   
                typeQuerySet=Type.objects.filter(catalogproperty_id__in=ids,active=True)   
                
                self.fields['type'].queryset= typeQuerySet
                self.fields['type'].initial= typedataproperty.type.id
                
                
                catalogpropertyQuerySet=CatalogProperty.objects.filter(id=typedataproperty.type.catalogproperty.id)
                self.fields['catalogproperty'].queryset=CatalogProperty.objects.filter(id=typedataproperty.type.catalogproperty.id)
                self.fields['catalogproperty'].initial=catalogpropertyQuerySet[0]
             
                
                print "id_catalogproperty " +str(catalogpropertyQuerySet[0].id)
                
                
                self.fields['catalogcrystalsystem'].queryset=catalogcrystalsystemQuerySet
                self.fields['catalogcrystalsystem'].initial=catalogcrystalsystemQuerySet[0] #initialization to first  on the list
                
                
                catalogpointgroupList=self.setPointGroup(typedataproperty.type, catalogcrystalsystemQuerySet[0])
    
                
                #catalogpointgroupids=CatalogPropertyDetail.objects.filter(type=typedataproperty.type,crystalsystem=catalogcrystalsystemQuerySet[0]).values_list('catalogpointgroup_id', flat=True)
                catalogpointgroupQuerySet=CatalogPointGroup.objects.filter(id__in=catalogpointgroupList)
    
                self.fields['catalogpointgroup'].queryset= catalogpointgroupQuerySet
                self.fields['catalogpointgroup'].initial  = [c.id for c in catalogpointgroupQuerySet]
    
                pointgroupsList=self.setPointGroups(typedataproperty.type, catalogcrystalsystemQuerySet[0])
                puntualgroupnamesQuerySet=PuntualGroupNames.objects.filter(id__in=pointgroupsList)
                   
                self.fields['puntualgroupnames'].queryset= puntualgroupnamesQuerySet
                if (puntualgroupnamesQuerySet.count() > 0):
                    self.fields['puntualgroupnames'].initial = puntualgroupnamesQuerySet[0]
                else:
                    self.fields['catalogpointgroup'].queryset= CatalogPointGroup.objects.all()
                    self.fields['catalogpointgroup'].initial  = [c.id for c in catalogpointgroupQuerySet]
                    
                
                
                axisList= self.setAxis(typedataproperty.type, catalogcrystalsystemQuerySet[0])
                
                #axisid=CatalogPropertyDetail.objects.filter(type=typedataproperty.type,crystalsystem=catalogcrystalsystemQuerySet[0]).values_list('catalogaxis_id', flat=True)
                axisQuerySet=CatalogAxis.objects.filter(id__in=axisList) 
                self.fields['axis'].queryset=axisQuerySet
                self.fields['axis'].initial = axisQuerySet[0] #initialization to first  on the list
                #self.fields['axis'].widget.attrs['disabled'] = 'True'
                
                 
                pgn =False
                if self.checkPointGroup(typedataproperty.type, catalogcrystalsystemQuerySet[0]):
                    catalogpropertydetailQuerySet=CatalogPropertyDetail.objects.filter(type=typedataproperty.type,crystalsystem=catalogcrystalsystemQuerySet[0],catalogaxis_id=axisQuerySet[0],catalogpointgroup=catalogpointgroupQuerySet[0],puntualgroupnames_id=21)
                    pgn = True
                
                pg =False
                if self.checkPuntualGroupNames(typedataproperty.type, catalogcrystalsystemQuerySet[0]):
                    catalogpropertydetailQuerySet=CatalogPropertyDetail.objects.filter(type=typedataproperty.type,crystalsystem=catalogcrystalsystemQuerySet[0],catalogaxis_id=axisQuerySet[0],catalogpointgroup_id=45,puntualgroupnames=puntualgroupnamesQuerySet[0])
                    pg =True
                
                pgpgn =False
                if self.checkPointGroup(typedataproperty.type, catalogcrystalsystemQuerySet[0]) and self.checkPuntualGroupNames(typedataproperty.type, catalogcrystalsystemQuerySet[0]):
                    catalogpropertydetailQuerySet=CatalogPropertyDetail.objects.filter(type=typedataproperty.type,crystalsystem=catalogcrystalsystemQuerySet[0],catalogaxis_id=axisQuerySet[0],catalogpointgroup=catalogpointgroupQuerySet[0],puntualgroupnames=puntualgroupnamesQuerySet[0])
                    pgpgn = True
    
                if pg == True:
                    self.fields['catalogpointgroup'].widget.attrs['disabled'] = True
    
                    
                if pgn == True:
                    self.fields['puntualgroupnames'].widget.attrs['disabled'] = True
                    
                    
                if pgpgn == True:
                    self.fields['catalogpointgroup'].widget.attrs['disabled'] = True
                    self.fields['puntualgroupnames'].widget.attrs['disabled'] = True
                    
                
    
                self.fields['quantity'].initial =catalogpropertydetailQuerySet.count()
                #self.fields['quantity'].widget.attrs['readonly'] = True
                self.fields['populate'].initial  = False
                
                ids=CatalogProperty.objects.filter(name=typedataproperty.type.catalogproperty.name).values_list('id', flat=True)    
                type_ids=Type.objects.filter(catalogproperty_id__in=ids,active=True, name=typedataproperty.type.name).values_list('id',flat=True)    
                dataproperty_ids=TypeDataProperty.objects.filter(type_id__in=type_ids).values_list('dataproperty_id',flat=True)    
                datapropertyQuerySet=Property.objects.filter(id__in=dataproperty_ids)   
                self.fields['dataproperty'].queryset=datapropertyQuerySet
                self.fields['dataproperty'].initial  = typedataproperty.dataproperty.id
                
            except ObjectDoesNotExist as error:
                print "Message({0}): {1}".format(99, error.message)   
                return  error.message
        else:
            if not args: #it arrives here after _addanother
                try:
                    super(TypeDataPropertyAdminForm, self).__init__(*args, **kwargs) 
                    self.fields['catalogproperty'].queryset= CatalogProperty.objects.all()
                    self.fields['catalogcrystalsystem'].queryset=CatalogCrystalSystem.objects.all()
                    self.fields['populate'].initial  = False
                    self.fields['axis'].queryset=CatalogAxis.objects.all()
                    self.fields['catalogpointgroup'].queryset= CatalogPointGroup.objects.all()
                    self.fields['puntualgroupnames'].queryset= PuntualGroupNames.objects.all()       
                    self.fields['coefficients'].queryset = CatalogPropertyDetail.objects.none()                              
                    self.fields['dataproperty'].queryset=Property.objects.all()
                except ObjectDoesNotExist as error:
                    print "Message({0}): {1}".format(99, error.message)   
                    return  error.message
            else:
                for arg in args:
                    print arg
                    if arg:
                        for item in arg:
                            print item + ":" + str(arg[item] )
                        
                        datapropertytag = None
                        
                        if arg.has_key('_continue') or arg.has_key('todo') and arg['todo'] != '': #'selectcatalogpropertyChange' or 'selecttypeChange' or 'selectcatalogcrystalsystemChange' or 'selectdatapropertyChange':

                            try:
                                if arg.has_key('_continue'):
                                    pass
                                else:
                                    args= {}
                                    
                                super(TypeDataPropertyAdminForm, self).__init__(*args, **kwargs) 
                                
                                catalogproperty=CatalogProperty.objects.get(id=int(arg['catalogproperty']))
                                catalogcrystalsysteminitial=None
                                catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty=catalogproperty)   
                                self.fields['catalogcrystalsystem'].queryset=catalogcrystalsystemQuerySet
                                if arg['catalogcrystalsystem'] =='':
                                    catalogcrystalsysteminitial = catalogcrystalsystemQuerySet[0] #initialization to first  on the list
                                    self.fields['catalogcrystalsystem'].initial=catalogcrystalsysteminitial
                                else:
                                    catalogcrystalsysteminitial = CatalogCrystalSystem.objects.get(id=int(arg['catalogcrystalsystem']))
                                    
                                self.fields['catalogcrystalsystem'].initial=catalogcrystalsysteminitial

                                typeinitial= None
                                typeQuerySet=Type.objects.filter(catalogproperty=catalogproperty,active=True) 
                                self.fields['type'].queryset= typeQuerySet
                                if arg['type'] =='':
                                    typeinitial = typeQuerySet[0]
                                else:
                                    typeinitial=Type.objects.get(id=int(arg['type']))

                                self.fields['type'].initial= Type.objects.get(id=typeinitial.id)    
 
                                self.fields['catalogproperty'].queryset=CatalogProperty.objects.all()
                                self.fields['catalogproperty'].initial=int(arg['catalogproperty'])
             
                                catalogpointgroupList=self.setPointGroup(typeinitial, catalogcrystalsysteminitial)
                                catalogpointgroupQuerySet=CatalogPointGroup.objects.filter(id__in=catalogpointgroupList)
                    
                                self.fields['catalogpointgroup'].queryset= catalogpointgroupQuerySet
                                self.fields['catalogpointgroup'].initial  = [c.id for c in catalogpointgroupQuerySet]
                    
                                pointgroupsList=self.setPointGroups(typeinitial,catalogcrystalsysteminitial)
                                puntualgroupnamesQuerySet=PuntualGroupNames.objects.filter(id__in=pointgroupsList)
                                   
                                self.fields['puntualgroupnames'].queryset= puntualgroupnamesQuerySet
                                if (puntualgroupnamesQuerySet.count() > 0):
                                    self.fields['puntualgroupnames'].initial = puntualgroupnamesQuerySet[0]
                                else:
                                    self.fields['catalogpointgroup'].queryset= CatalogPointGroup.objects.all()
                                    self.fields['catalogpointgroup'].initial  = [c.id for c in catalogpointgroupQuerySet]

                                dataproperty_ids = None
                                type_ids=Type.objects.filter(catalogproperty=catalogproperty,active=True, name=typeinitial.name).values_list('id',flat=True)    
                                if datapropertytag==None:
                                    dataproperty_ids=TypeDataProperty.objects.filter(type_id__in=type_ids).values_list('dataproperty_id',flat=True) 
                                else:
                                    dataproperty_ids=TypeDataProperty.objects.filter(type_id__in=type_ids).values_list('dataproperty_id',flat=True).exclude(dataproperty=datapropertytag) 
 
                                datapropertyinitial= None
                                datapropertyQuerySet=Property.objects.filter(id__in=dataproperty_ids)   
                                self.fields['dataproperty'].queryset=datapropertyQuerySet
                                #self.fields['dataproperty'].initial  =datapropertyQuerySet[0].id
                                
                                if arg['dataproperty'] =='':
                                    datapropertyinitial = datapropertyQuerySet[0]
                                else:
                                    datapropertyinitial=Property.objects.get(id=int(arg['dataproperty']))

                                self.fields['dataproperty'].initial= datapropertyinitial

                                axisList= self.setAxis(typeinitial, catalogcrystalsysteminitial)
                                axisQuerySet=CatalogAxis.objects.filter(id__in=axisList) 
                                self.fields['axis'].queryset=axisQuerySet
                                self.fields['axis'].initial = axisQuerySet[0] #initialization to first  on the list

                                pgn =False
                                if self.checkPointGroup(typeinitial, catalogcrystalsysteminitial):
                                    catalogpropertydetailQuerySet=CatalogPropertyDetail.objects.filter(type=typeinitial,crystalsystem=catalogcrystalsysteminitial,catalogaxis_id=axisQuerySet[0],catalogpointgroup=catalogpointgroupQuerySet[0],puntualgroupnames_id=21,dataproperty=datapropertyinitial)
                                    dataporpertygroup_by=CatalogPropertyDetail.objects.filter(type=typeinitial,crystalsystem=catalogcrystalsysteminitial,catalogaxis_id=axisQuerySet[0],catalogpointgroup=catalogpointgroupQuerySet[0],puntualgroupnames_id=21).values('dataproperty').annotate(total=Count('dataproperty'))
                                    if dataporpertygroup_by[0]['total'] != 0:
                                        datapropertytag=Property.objects.get(id=dataporpertygroup_by[0]['dataproperty'])

                                    pgn = True
                                
                                pg =False
                                if self.checkPuntualGroupNames(typeinitial, catalogcrystalsysteminitial):
                                    catalogpropertydetailQuerySet=CatalogPropertyDetail.objects.filter(type=typeinitial,crystalsystem=catalogcrystalsysteminitial,catalogaxis_id=axisQuerySet[0],catalogpointgroup_id=45,puntualgroupnames=puntualgroupnamesQuerySet[0],dataproperty=datapropertyinitial)
                                    dataporpertygroup_by=CatalogPropertyDetail.objects.filter(type=typeinitial,crystalsystem=catalogcrystalsysteminitial,catalogaxis_id=axisQuerySet[0],catalogpointgroup_id=45,puntualgroupnames=puntualgroupnamesQuerySet[0]).values('dataproperty').annotate(total=Count('dataproperty'))
                   
                                    if dataporpertygroup_by[0]['total'] != 0:
                                        datapropertytag=Property.objects.get(id=dataporpertygroup_by[0]['dataproperty'])
                        
                                    pg =True
                                
                                pgpgn =False
                                if self.checkPointGroup(typeinitial, catalogcrystalsysteminitial) and self.checkPuntualGroupNames(typeinitial, catalogcrystalsysteminitial):
                                    catalogpropertydetailQuerySet=CatalogPropertyDetail.objects.filter(type=typeinitial,crystalsystem=catalogcrystalsysteminitial,catalogaxis_id=axisQuerySet[0],catalogpointgroup=catalogpointgroupQuerySet[0],puntualgroupnames=puntualgroupnamesQuerySet[0],dataproperty=datapropertyinitial)
                                    dataporpertygroup_by=CatalogPropertyDetail.objects.filter(type=typeinitial,crystalsystem=catalogcrystalsysteminitial,catalogaxis_id=axisQuerySet[0],catalogpointgroup=catalogpointgroupQuerySet[0],puntualgroupnames=puntualgroupnamesQuerySet[0]).values('dataproperty').annotate(total=Count('dataproperty'))
                                    if dataporpertygroup_by[0]['total'] != 0:
                                        datapropertytag=Property.objects.get(id=dataporpertygroup_by[0]['dataproperty'])
                                        
                                    pgpgn = True
                    
                                if pg == True:
                                    self.fields['catalogpointgroup'].widget.attrs['disabled'] = True

                                if pgn == True:
                                    self.fields['puntualgroupnames'].widget.attrs['disabled'] = True
                                    
                                if pgpgn == True:
                                    self.fields['catalogpointgroup'].widget.attrs['disabled'] = True
                                    self.fields['puntualgroupnames'].widget.attrs['disabled'] = True

                                #self.fields['quantity'].initial =catalogpropertydetailQuerySet.count()
                                #self.fields['quantity'].widget.attrs['readonly'] = True

                                if catalogpropertydetailQuerySet.count() == 0:
                                    self.fields['populate'].initial  = False
                                    dimensions=datapropertyinitial.tensor_dimensions.split(',')
                                    none_catalogpropertydetailcustomQuerySet=CatalogPropertyDetail.objects.none()
                                    catalogpropertydetailcustomObjList  = []
                                    qs = None
                                    if len(dimensions) == 2:
                                        coefficients = N.zeros([int(dimensions[0]),int(dimensions[1])])    
                                        print datapropertyinitial.tag
                                        parts=datapropertyinitial.tag.split('_')[-1]
                                        letters =parts.split('ij')
                                        x = 0
                                        row = []
                                        for r in coefficients:
                                            x=x+ 1
                                            y=1   
                                            for c in r: 
                                                col= str(x) + str(y)                
                                                print letters[0] +col + letters[1] 
                                                #catalogpropertydetailObj=CatalogPropertyDetail()
                                                catalogpropertydetailObj=CatalogPropertyDetailTemp()
                                                catalogpropertydetailObj.name= letters[0] +col + letters[1] 
                                                catalogpropertydetailObj.type = typeinitial
                                                catalogpropertydetailObj.crystalsystem= catalogcrystalsysteminitial
                                               
                                                catalogpropertydetailObj.catalogaxis= axisQuerySet[0] 
                                                #catalogpropertydetailObj.catalogpointgroup=
                                                #catalogpropertydetailObj.puntualgroupnames=
                                                catalogpropertydetailObj.dataproperty=datapropertytag
                                                
                                                catalogpropertydetailObj.dataproperty=datapropertyinitial
                                                catalogpropertydetailObj.save()
                                                catalogpropertydetailcustomObjList.append(catalogpropertydetailObj)
                                                del catalogpropertydetailObj
                                                y= y + 1 
                                    
                                       
                                        qs = list(chain(none_catalogpropertydetailcustomQuerySet, catalogpropertydetailcustomObjList))
                                    creator_choices1 = [(c.id, c.name) for i,c in enumerate(qs)]
                                    self.fields['coefficients'].choices=creator_choices1
                                    
                                    """
                                    lastobjid = CatalogPropertyDetail.objects.latest('id')
                                    counter= 0
                                    creator_choices2 = []
                                    for i,c in enumerate(qs):
                                        counter=counter + 1
                                        creator_choices2.append((c,c))
                                    """
                                    
                                     
                                    
  
                                else:
                                    self.fields['populate'].initial  = True
                                    self.fields['coefficients'].queryset = CatalogPropertyDetail.objects.filter(type=typeinitial)
                                    self.fields['coefficients'].initial = catalogpropertydetailQuerySet
                                    #print catalogpropertydetailQuerySet
                                      
                            except ObjectDoesNotExist as error:
                                print "Message({0}): {1}".format(99, error.message)   
                                return  error.message   
                             
                        if arg.has_key('_save') :
                            try:
                                
                                valuelistcoefficients = arg.getlist('coefficients')
                                create = False
                                if not self.isnumber(valuelistcoefficients[0]):
                                    print "crear coeficientes"
                                    create = True
                                    vals = []
                                    
                                    lastobjid = CatalogPropertyDetail.objects.latest('id')
                                    counter= lastobjid.id
                                    
                                    catalogpropertydetailcustomObjList =[]
                                    for i,v in enumerate(valuelistcoefficients):
                                        vals.append(v)
                                        cpdObj=CatalogPropertyDetail()
                                        cpdObj.name = v
                                        catalogpropertydetailcustomObjList.append(cpdObj)
 
                                    
                                    none_catalogpropertydetailcustomQuerySet=CatalogPropertyDetail.objects.none()
                                    qs = list(chain(none_catalogpropertydetailcustomQuerySet, catalogpropertydetailcustomObjList))
                                    #creator_choices = [(c, c.name) for i,c in enumerate(qs)]
                                    print qs
                                    creator_choices= tuple((str(i), str(n)) for i,n in  enumerate(valuelistcoefficients))
                                    
                                    """
                                    creator_choices = []
                                    for i,c in enumerate(qs):
                                        counter=counter + 1
                                        creator_choices.append((c,c))
                                    """
                                    
                                 
                                    for i,c in enumerate(valuelistcoefficients):
                                        counter=counter + 1
                                        #valuelistcoefficients[i] = u'' + str(c)
            
                                         

                                    #print valuelistcoefficients
                                    print args[0]
                                    #print vals
                                    print creator_choices
                                else:
                                    print "no crear coeficientes"
                                    
                                
                                super(TypeDataPropertyAdminForm, self).__init__(*args, **kwargs) 
                                
                                    
                                
                                self.fields['catalogproperty'].queryset= CatalogProperty.objects.all()
                                self.fields['catalogcrystalsystem'].queryset=CatalogCrystalSystem.objects.all()
                                self.fields['populate'].initial  = False
                                self.fields['axis'].queryset=CatalogAxis.objects.all()
                                self.fields['catalogpointgroup'].queryset= CatalogPointGroup.objects.all()
                                self.fields['puntualgroupnames'].queryset= PuntualGroupNames.objects.all()       
                                self.fields['dataproperty'].queryset=Property.objects.all()
                                self.fields['coefficients'].queryset = CatalogPropertyDetail.objects.all()
                                #self.fields['coefficients'].choices = creator_choices
                                
                                
                                """
                                for v in enumerate(vals):
                                        counter=counter + 1
                                        valuelistcoefficients[i] = u'' + str(v)
                                """
                                    
                                
                                #print valuelist
                                print '_save'
                            except ObjectDoesNotExist as error:
                                print "Message({0}): {1}".format(99, error.message)   
                                return  error.message  
                           
                        if arg.has_key('_addanother'):
                            try:
                                valuelist = arg.getlist('coefficients')
                                print valuelist
                                lastobjid = CatalogPropertyDetail.objects.latest('id')
                                counter= lastobjid.id
                                creator_choices = []
                                for i,c in enumerate(valuelist):
                                    counter=counter + 1
                                    creator_choices.append((counter,c))
                                    
                                #newargs= args.copy()
                                print args[0]#QueryDict
                                querydict = args[0]
                                querydict['coefficients']=creator_choices
                                print args[1]#MultiValueDict
                                
                                super(TypeDataPropertyAdminForm, self).__init__(*args, **kwargs) 
                                self.fields['catalogproperty'].queryset= CatalogProperty.objects.all()
                                self.fields['catalogcrystalsystem'].queryset=CatalogCrystalSystem.objects.all()
                                self.fields['populate'].initial  = False
                                self.fields['axis'].queryset=CatalogAxis.objects.all()
                                self.fields['catalogpointgroup'].queryset= CatalogPointGroup.objects.all()
                                self.fields['puntualgroupnames'].queryset= PuntualGroupNames.objects.all()       
                                 
                                #print '_addanother'
                                listc= arg['coefficients']
                                valuelist = arg.getlist('coefficients')
                                """for key in arg.iterkeys(): 
                                  
                                    valuelist = arg.getlist(key)
                                    print valuelist
                                 """   
                                """
                                print valuelist
                                lastobjid = CatalogPropertyDetail.objects.latest('id')
                                counter= lastobjid.id
                                creator_choices = []
                                for i,c in enumerate(valuelist):
                                    counter=counter + 1
                                    creator_choices.append((counter,c))
                                """    
                                
                                datapropertyinitial=Property.objects.get(id=int(arg['dataproperty']))
                                catalogproperty=CatalogProperty.objects.get(id=int(arg['catalogproperty']))
                                typeinitial= None
                                typeQuerySet=Type.objects.filter(catalogproperty=catalogproperty,active=True) 
                                self.fields['type'].queryset= typeQuerySet
                                if arg['type'] =='':
                                    typeinitial = typeQuerySet[0]
                                else:
                                    typeinitial=Type.objects.get(id=int(arg['type']))
                                    
                                catalogpropertydetailQuerySet  = CatalogPropertyDetail.objects.filter(type=typeinitial,crystalsystem_id=int(arg['catalogcrystalsystem']))
                                self.fields['coefficients'].queryset = catalogpropertydetailQuerySet
                                
                                #self.fields['coefficients'].choices= creator_choices
                                #self.fields['coefficients'].initial = creator_choices
                                
                                
                                self.fields['dataproperty'].queryset=Property.objects.all()
                            except ObjectDoesNotExist as error:
                                print "Message({0}): {1}".format(99, error.message)   
                                return  error.message  

                   
                        
                

                #print unzipped
                    
        
     
        
       
class PuntualGroupGroupsAdminForm(forms.ModelForm):
 
    #point_groups = forms.ModelMultipleChoiceField(CatalogPointGroup.objects.filter(id=0))
    pointgroups = forms.ModelMultipleChoiceField(
            queryset=None,
            required=True,
            label="Point Groups",
            widget=FilteredSelectMultiple(
                verbose_name='Point groups',
                is_stacked=False
            )
        )
    
     
     

    class Meta:
        model = PuntualGroupGroups
 

        
    def __init__(self, *args, **kwargs):
        super(PuntualGroupGroupsAdminForm, self).__init__(*args, **kwargs) 
        print kwargs
        puntualgroupgroups = kwargs.pop('instance', None)
        if puntualgroupgroups != None:
            ids = PuntualGroupNames.objects.filter(name=self.instance.puntualgroupnames.name).values_list('id', flat=True)    
            idspgg=PuntualGroupGroups.objects.filter(puntualgroupnames_id__in=ids).values_list('catalogpointgroup',flat=True)         
            catalogpointgroupQuerySet = CatalogPointGroup.objects.filter(id__in=idspgg) 
            self.fields['pointgroups'].queryset= CatalogPointGroup.objects.all()
            self.fields['pointgroups'].initial  = [c.id for c in catalogpointgroupQuerySet]
            
            #args=[valor]
            url= u'%s' % (reverse('admin:Properties_puntualgroupgroups_changelist',args=[])) 
            print url
            
            print puntualgroupgroups.id
            #kwargs={'object_id': puntualgroupgroups.id} Nombre de parametro y valor
            #url= u'%s' % (reverse('admin:PuntualGroupGroupsAdmin_change_view' ,args=(puntualgroupgroups.id,) ))
            #url = reverse('PuntualGroupGroupsAdmin_change_view',  args=[puntualgroupgroups.id] )
            print url
            
            
 
 
 
 