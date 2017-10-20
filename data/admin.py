'''
Created on Aug 13, 2017

@author: admin
'''

from django.contrib.admin import *
from django.contrib import admin
from django.conf.urls import patterns, url
from functools import update_wrapper
 
 

from django.core  import urlresolvers

from .models import *

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.forms import ModelChoiceField
from forms import *
from django.contrib import messages
from django.contrib.admin.views.main import IS_POPUP_VAR
from django.template.response import SimpleTemplateResponse, TemplateResponse
import json
from django.http import HttpResponseRedirect
from django.contrib.admin.views.main import ChangeList

"""
class UserAdmin(admin.ModelAdmin):

    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')

    def get_urls(self):
        # this is just a copy paste from the admin code
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        # get the default urls
        urls = super(UserAdmin, self).get_urls()
        # define my own urls
        my_urls = patterns(
            '',
            url(r'^inactive/$',
                wrap(self.changelist_view),
                name="inactive_users")
        )
        # return the complete list of urls
        return my_urls + urls

    def get_changelist(self, request):
 
        # for inactive users use the InactiveUsersView
        print request.path_info
        #if  (request.path_info).url_name == "inactive_users":
            #pass#return InactiveUsersView
        return super(UserAdmin, self).get_changelist(request)
 
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

 """
"""
class UserAdmin(admin.ModelAdmin):

    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    actions = ['publish_selected']
    
    def publish_selected(self, request, queryset):
        queryset.update(status='p')

    publish_selected.short_description = "Publish the selected posts"
    admin.site.add_action(publish_selected)
    #admin.site.disable_action('delete_selected')
"""


 
 
 
class PathAdmin(admin.ModelAdmin):
    list_display =('cifs_dir', 'core_dic_filepath', 'mpod_dic_filepath','stl_dir','datafiles_path')     
    list_filter = ('devmode',)
    

admin.site.register(Path, PathAdmin)

class PublArticleAdmin(admin.ModelAdmin):
    list_display =('title', 'authors', 'journal','year','volume','issue','first_page','last_page','reference','pages_number')
    search_fields = ['title', 'authors', 'journal','year','volume']
    list_filter = ('year',)
    fields = [('title','authors'), ( 'journal'),('year','volume','issue'),('first_page','last_page','reference','pages_number')]
    
 
admin.site.register(PublArticle, PublArticleAdmin)

class ExperimentalParCondAdmin(admin.ModelAdmin):
    list_display =('tag', 'description', 'name','units','units_detail')
    search_fields = ['tag', 'description', 'name','units','units_detail']


admin.site.register(ExperimentalParCond,ExperimentalParCondAdmin)

class DataFileAdmin(admin.ModelAdmin):
    list_display =('code', 'filename', 'cod_code', 'phase_generic','phase_name','chemical_formula' ,'get_article')
    fieldsets = (
        (None, {
            'fields': ('code', 'filename', 'cod_code', 'phase_generic','phase_name','chemical_formula' )
        }),
        ('Articles', {
            'fields': ('publication', )
        }),
        ('Property List', {
            'fields': ('properties', )
        }),
    )
 
    def get_article(self, obj):
        link_to_article=os.path.join('../publarticle/' , str(obj.publication.id))
        link= "<a href="+link_to_article+">"+str(obj.publication.id)+"</a>"        
        return u'<a href="%s">%s</a>' % (link_to_article,obj.publication.id)    
    
    
    get_article.short_description = 'Article'
    get_article.allow_tags=True

    
admin.site.register(DataFile,DataFileAdmin)


 


class ConfigurationAdmin(admin.ModelAdmin):
    list_display =('email_host_user','email_host_password','email_port','email_host','email_use_tls','email_domain',)  

admin.site.register(Configuration, ConfigurationAdmin)


class MessageMailAdmin(admin.ModelAdmin):
    list_display =('email_subject','email_regards','email_message',)  
    
    
    '''def get_site(self, obj):
        #link_to_site=os.path.join('.././../sites/site/' , str(obj.site.id))
        link_to_site=os.path.join('../../sites/site/' , str(obj.site.id))
        #/sites/site/1/
        return u'<a href="%s">%s</a>' % (link_to_site,obj.site.name)    
     
    get_site.short_description = 'Site'
    get_site.allow_tags=True'''
    
    

admin.site.register(MessageMail, MessageMailAdmin)



class ConfigurationMessageAdmin(admin.ModelAdmin):
    list_display =('account','get_message','is_active')  
    
    
     
    def get_message(self, obj):
        return  u'%s' % (obj.message.email_subject)   
     
    def get_message_domain(self, obj):
        return  u'%s' % (obj.message.site.domain)     
     
    
     
    get_message.short_description = 'Message'
    get_message.allow_tags=True
    
    get_message_domain.short_description = 'Activation in'
    get_message_domain.allow_tags=True
                

admin.site.register(ConfigurationMessage, ConfigurationMessageAdmin)


class MessageCategoryAdmin(admin.ModelAdmin):
        list_display =('name','description',)  

admin.site.register(MessageCategory, MessageCategoryAdmin)


class MessageCategoryDetailAdmin(admin.ModelAdmin):
        #pass
        list_display =('get_message','get_category','get_group','get_user')  
          
          
        def get_message(self, obj):
                return  u'%s' % (obj.message.email_subject)   
            
        def get_category(self, obj):
                return  u'%s' % (obj.messagecategory.name)     
            
        def get_group(self, obj):
                return  u'%s' % (obj.group.name)     
            
        def get_user(self, obj):
                return  u'%s' % (obj.user.username)     
            
            
        get_message.short_description = 'Message'
        get_message.allow_tags=True
       
        get_category.short_description = 'Category name'
        get_category.allow_tags=True
        
        
        get_group.short_description = 'Group'
        get_group.allow_tags=True
       
        get_user.short_description = 'User'
        get_user.allow_tags=True

admin.site.register(MessageCategoryDetail, MessageCategoryDetailAdmin)



class FileUserAdmin(admin.ModelAdmin):
        list_display =('filename','date','user_name')  
        search_fields = ['filename', ]
        
        
        #change_form_template = 'admin/properties/fileuser/change_form.html'
        #filter_horizontal = ('authuser',) #only in manytomany
        #raw_id_fields = ('authuser',)
        """
        def change_view(self, request, object_id, extra_context=None):
            result = super(FileUserAdmin, self).change_view(request, object_id, extra_context)
            
            fileuser = FileUser.objects.get(id__exact=object_id)
            if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
                result['Location'] = "_save"
               
                 
            return result
        """
        
      
        
        
        
        


admin.site.register(FileUser, FileUserAdmin)



#ejemplo action para ser usado global
def apply_discount(modeladmin, request, queryset):
    """
    for book in queryset:
        book.price = book.price * decimal.Decimal('0.9')
        book.save()
    """
    pass 
 
apply_discount.short_description = 'Apply 10%% discount'


# Globally disable delete selected
#admin.site.disable_action('delete_selected')




class CategoryModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        # Return a string of the format: "description  (name)"
        return "%s (%s)"%( obj.description,obj.name)  
    
 

class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        # Return a string of the format: "firstname lastname (username)"
        return "%s (%s)"%(obj.get_full_name(), obj.username)  
    
    
    

    
class DictionaryForm(forms.ModelForm):
    category = CategoryModelChoiceField(Category.objects.all().order_by('description'))
    class Meta:
        model = Dictionary
    
  
  
class CategoryView(ChangeList):
        def __init__(self, *args, **kwargs):
            super(CategoryView, self).__init__(*args, **kwargs)
            #self.list_display = ('username', 'email', 'date_joined', 'last_login')
    
        def get_queryset(self, request):
            qs = super(CategoryView, self).get_queryset(request)
            return qs.filter(deploy=False)
        
                  
class DictionaryAdmin(admin.ModelAdmin): 
    #dictionary_change_form = 'dictionary.html'
    
    form=DictionaryForm
    
    
    list_display =('tag','category',)  
    search_fields = ['name', ]
    #readonly_fields=['tag',]
    
    #actions = ['delete_selected', 'a_third_action']#ejemplo  2 action locales
    #actions = ['make_deployed',apply_discount]#ejemplo usando un action global y uno local
    actions = ['make_deployed']#usando un action local
    
    
    def make_deployed(self, request, queryset):
        #queryset.update(deploy=1)
        rows_updated = queryset.update(deploy=1)
        if rows_updated == 1:
            message_bit = "1 property was set for deploy"
        else:
            message_bit = "%s properties were" % rows_updated
        self.message_user(request, "%s successfully marked as deployed." % message_bit)
    
    make_deployed.short_description = "Mark selected properties as deployed"
    
    
    def save_model(self, request, obj, form, change):
        print request.POST
        print obj.tag
        print form.changed_data # list name of field was changed
        print change #True or False
        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue') and not request.POST.has_key('_save'):
            print "pass"
        elif  request.POST.has_key('_addanother'): 
            print request.POST.get('_addanother',False)
        elif request.POST.has_key('_continue'): 
            print request.POST.get('_continue',False)
        elif request.POST.has_key('_save'):
            print request.POST.get('_save',False)
        
        
        #super(DictionaryAdmin, self).save_model(request, obj, form, change)    # con esto guarda normalmente
        message_bit = "properties were" 
        #self.message_user(request, "%s successfully saved." % message_bit)
        
        #messages.success(request, 'Your profile was updated.')
        messages.add_message(request, messages.SUCCESS, "%s successfully saved." % message_bit)
        #messages.add_message(request, messages.ERROR, mark_safe("Please see <a href='/destination'>here</a> for further details"))

        obj.save() # con esto guarda 
            
        
    def has_add_permission(self, request):
        return_value = False
        user = request.user
        if user.is_authenticated() and user.is_superuser:
            return_value = True
        
        print "tiene permisos para agregar:"  + str(return_value)
        return return_value    
   
    def has_delete_permission(self, request, obj=None):
        return_value = False
        user = request.user
        if user.is_authenticated() and user.is_staff:
            return_value = True
        
        print "tiene permisos para borrar:"  + str(return_value)
        return return_value     
        
        #obj.preformed_by = request.user
        #obj.ipaddress = utils.get_client_ip(request)
        #obj.save()
         
    def get_actions(self, request):
        actions = super(DictionaryAdmin, self).get_actions(request)
        try:
           
            print actions
            if 'delete_selected' in actions:
                del actions['delete_selected']
                #del actions['delete_selected'] #disable
                
        except KeyError:
            pass
        return actions
    
    
    def get_readonly_fields(self, request, obj = None):
        if obj:
            if not (request.user.is_staff or request.user.is_superuser):
                return ['category',] + self.readonly_fields
            return self.readonly_fields
        else:
            return self.readonly_fields
    
    
    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        urls = super(DictionaryAdmin,self).get_urls()

        info = self.model._meta.app_label, self.model._meta.module_name
        n='%s_%s_review' % info
        print n
        #Dictionaries_dictionary_review
        my_urls = [
            url(r'(?P<id>\d+)/review/$', wrap(self.review), name='%s_%s_review' % info),
            url(r'(?P<id>\d+)/category/(?P<categorypk>\d+)/$', wrap(self.custom_changelist_view), name='%s_%s_category' % info),
           
        ]
        #print my_urls
        return my_urls + urls
    
    
    def review(self, request, id):
        print 'review'
        dictionary = Dictionary.objects.get(pk=id)

        return render_to_response("dictionary.html", {
            'Tag': 'Review dictionary: %s' % dictionary.tag,
            'dictionary': dictionary,
            'opts': self.model._meta,
           # 'root_path': self.admin_site.root_path,
        }, context_instance=RequestContext(request))
    

    def custom_changelist_view(self, request,id,categorypk):
        print 'custom_changelist_view'
        extra_context=None
        #print reverse('admin:Dictionaries_dictionary_category',kwargs={'id':id,'categorypk':categorypk})
        print request.path_info ==reverse('admin:Dictionaries_dictionary_category',kwargs={'id':id,'categorypk':categorypk})
        dictionary = Dictionary.objects.get(id__exact=id)
        result = super(DictionaryAdmin, self).change_view(request, id, extra_context)
        
        return result

    #al seleccionar un elemento de change_list_results.html
    def change_view(self, request, object_id, extra_context=None):
        result = super(DictionaryAdmin, self).change_view(request, object_id, extra_context)
        
        dictionary = Dictionary.objects.get(id__exact=object_id)
        #if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
            
        print "change_view"
               
                 
        return result
    
    
    
    def add_view(self,request,extra_content=None):
        print 'add_view'
         
        return super(DictionaryAdmin,self).add_view(request)
        
 
    def changelist_view(self, request, extra_context=None):
        print 'changelist_view'
        extra_context = extra_context or {}
        extra_context['some_var'] = 'This is what I want to show'
        return super(DictionaryAdmin, self).changelist_view(request, extra_context=extra_context)
    
    
    
    
    #alseleccionar un elemento de menu
    def selectlist_view(self, request, extra_context=None):
        print 'selectlist_view'
        temp_list_display_links = self.list_display_links
        self.list_display_links = (None, )
        response = self.changelist_view(request, extra_context)
        self.list_display_links = temp_list_display_links
        return response
   

admin.site.register(Dictionary, DictionaryAdmin)
    
    



