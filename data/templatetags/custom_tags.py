'''
Created on Oct 6, 2017

@author: admin
'''
from django import template

from data.models import *
 
register = template.Library()
 
@register.inclusion_tag('comments.html')
def display_comments(document_id):
    print document_id
    
    comments = FileUser.objects.filter(authuser=User.objects.get(id__exact=5))
  
  
    return { 'comments': comments }