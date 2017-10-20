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
    year = forms.CharField(required=True,help_text="Enter year.",label='Year',initial='')
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


             
         

    """
    class DictionaryForm(forms.ModelForm):
        class Meta:
            model = Dictionary
      
         
        def clean_category(self):
            if not self.cleaned_data['category']:
                return Category()
            return self.cleaned_data['category']     
        
        
        def clean_type(self):
            if not self.cleaned_data['type']:
                return "char"
            return self.cleaned_data['type']    
        """