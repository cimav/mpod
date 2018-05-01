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
    catalogcrystalsystem =forms.ModelChoiceField(queryset=None,label="Crystal System",widget=forms.Select(attrs={"onChange":'refreshdetail(this)'}))
    
    quantity = forms.IntegerField(min_value=1, label="Coefficients to capture"  )
    populate =  forms.BooleanField()
    axis=forms.ModelChoiceField(queryset=None,label="Axis")
    catalogpointgroup = forms.ModelChoiceField(queryset=None,label="Point Group")
    puntualgroupnames = forms.ModelChoiceField(queryset=None,label="Groups")
    #catalogpointgroupdetail = forms.ModelMultipleChoiceField(queryset=None,label="Point Groups")
    catalogpropertydetail = forms.ModelChoiceField(queryset=None,label="Coefficients detail")
    #name = forms.CharField(widget=forms.TextInput(),max_length=15,label=mark_safe('Your Name (<a href="/questions/whyname/" target="_blank">why</a>?)'))
     

    
    class Meta:
        model = TypeDataProperty
        
    def __init__(self, *args, **kwargs):
        super(TypeDataPropertyAdminForm, self).__init__(*args, **kwargs) 
        typedataproperty = kwargs.pop('instance', None)
        if typedataproperty != None:
 
            self.fields['catalogproperty'].queryset= CatalogProperty.objects.filter(id= typedataproperty.type.catalogproperty.id)
            self.fields['catalogproperty'].initial = typedataproperty.type.catalogproperty.id            
            ccsList=CatalogCrystalSystem.objects.filter(catalogproperty=typedataproperty.type.catalogproperty)
             
            self.fields['catalogcrystalsystem'].queryset=ccsList
            self.fields['catalogcrystalsystem'].initial=ccsList[0].id
            
            
            
        
            
           
            #self.fields['catalogcrystalsystem'].initial=CatalogCrystalSystem.objects.filter(catalogproperty=typeDataProperty.type.catalogproperty).values_list('id', flat=True)
            self.fields['populate'].initial  = False
            """
            cpdList=CatalogPropertyDetail.objects.filter(type=typeDataProperty.type,crystalsystem__id=ccsList[0].id).values_list('name', flat=True)
            self.fields['catalogpropertydetail'].queryset=cpdList 
            self.fields['catalogpropertydetail'].initial  =ccsList[0]
            """
            
            axisList=CatalogPropertyDetail.objects.filter(type=typedataproperty.type,crystalsystem__id=ccsList[0].id).values_list('catalogaxis__description', flat=True).exclude(catalogaxis=4)
 
            if not axisList:
                axisList= CatalogAxis.objects.all()
                self.fields['axis'].initial = 4
            
            self.fields['axis'].queryset=axisList
            
            
            pointGroupList=CatalogPropertyDetail.objects.filter(type=typedataproperty.type,crystalsystem__id=ccsList[0].id).values_list('catalogpointgroup__name', flat=True).exclude(catalogpointgroup=45)
            if not pointGroupList:
                pointGroupList= CatalogPointGroup.objects.all()
                self.fields['catalogpointgroup'].initial = 45

            self.fields['catalogpointgroup'].queryset= pointGroupList
            
            
            
            pgnl=PuntualGroupNames.objects.all()
            self.fields['puntualgroupnames'].queryset= pgnl            
            self.fields['puntualgroupnames'].initial = pgnl[0].id
            
            #pgn = PuntualGroupNames.objects.get(name=pgnl[0])    
            #self.fields['catalogpointgroupdetail'].queryset= PuntualGroupGroups.objects.filter(puntualgroupnames=pgn).values_list('catalogpointgroup__name', flat=True) 
             
             
            typedataproperty=TypeDataProperty.objects.get(id= typedataproperty.id) 
            CatalogProperty.objects.filter(id= typedataproperty.type.catalogproperty.id)
            ccs=CatalogCrystalSystem.objects.filter(catalogproperty=typedataproperty.type.catalogproperty)
            catalogpropertydetailList=CatalogPropertyDetail.objects.filter(type=typedataproperty.type,crystalsystem__id=ccs[0].id)
            
            
            self.fields['quantity'].initial =catalogpropertydetailList.count()
             
            
            
             
        else:
            self.fields['catalogproperty'].queryset= CatalogProperty.objects.all()
            self.fields['catalogcrystalsystem'].queryset=CatalogCrystalSystem.objects.all()
            self.fields['populate'].initial  = False
            self.fields['axis'].queryset=CatalogAxis.objects.all()
            self.fields['catalogpointgroup'].queryset= CatalogPointGroup.objects.all()
            self.fields['puntualgroupnames'].queryset= PuntualGroupNames.objects.all()       
            self.fields['catalogpropertydetail'].queryset= CatalogPropertyDetail.objects.all().values_list('name', flat=True) 
            self.fields['catalogpointgroupdetail'].queryset=PuntualGroupGroups.objects.all()
           
             
            #'populate','data_property','quantity','catalogcrystalsystem','axis','catalogpointgroup','puntualgroupnames','catalogpointgroupdetail
        
       
                
            
             

 