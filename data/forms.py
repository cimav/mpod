'''
Created on Aug 13, 2017

@author: admin
'''
from django import forms            
from django.contrib.auth.models import User   # fill in custom user info then save it 
from django.contrib.auth.forms import * 
from django.core.exceptions import ValidationError
 
def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an  number'),
            params={'value': value},
        )
        
def validate_empty(value):
    if value.strip() == '':
        raise ValidationError(
            _('%(value)s is empty'),
            params={'value': value},
        )

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = {'name', 'username', 'password1', 'password2', 'email'}

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['name']

        if commit:
            user.save()

        return user
    
    
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
    

  
 
  
     