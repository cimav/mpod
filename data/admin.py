'''
Created on Aug 13, 2017

@author: admin
'''
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin import *
from django.contrib import admin
from django.conf.urls import patterns, url
from functools import update_wrapper
 
 
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
 

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
from django.core import serializers

from time import gmtime, strftime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import transaction
from django.db import IntegrityError
import fileinput

from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.utils.text import force_unicode
from django.template.defaultfilters import capfirst
from django.contrib.admin.util import *
 
from django import template
from django.db import router, transaction


from django.template.loader import render_to_string
from django.core import mail
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from data.models import MessageCategoryDetail

from django.db.models import get_app, get_models
from django.contrib.admin.actions import delete_selected as delete_selected_

from django.db.models.query import QuerySet
from django.db.models import Count

import decimal
from data.Utils import requestPostToIntList

from CifMpodValidator import *
from data.ExtractorDataFromCIF import *
from django.http import QueryDict
from data.JScriptUtil import *

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
        list_display =('filename','date','user_name','publish')  
        search_fields = ['filename', ]
        
        
        form=FileUserAdminForm
        readonly_fields=['authuser','filename','date','user_name','reportvalidation']
       
        
        def get_fieldsets(self, *args, **kwargs):
            return  (
                ('File', {
                    'fields': ('properties_click','fileuserid','datafile_tempid','authuser','filename','filenamepublished','cod_code','date','datepublished','reportvalidation','publish','experimentalcon','properties','phase_generic','phase_name','chemical_formula',)
                }),
                ('Publication info', {
                      'classes': ('collapse',),
                      'fields': (  'title','authors','journal','year','volume','issue','first_page','last_page','reference','pages_number',),
                  }),
         

                 
              
            )
            
            

 
        def change_view(self, request, object_id, form_url='', extra_context=None):
            extra_context = extra_context or {}
            if not 'propertyValuesTempList' in request.session or not request.session['propertyValuesTempList' ]: 
                pass
            else:
                del request.session['propertyValuesTempList']
            extra_context = {
                'original':'File User',
                 
            }
 
          
 
            return admin.ModelAdmin.change_view(self, request, object_id, form_url=form_url, extra_context=extra_context)
         
        def delete_model_queryset(self, request, queryset):
            for obj in queryset:
                print obj
                #obj.delete()
                
        def delete_model(self, request, obj):
            
            if obj.publish != True:
                if obj.datafile:
                    publicArticle =  obj.datafile.publication
                    filename = obj.datafile.filename
                    
                    dataFilePropertyQuerySet = DataFilePropertyTemp.objects.filter(datafile=obj.datafile)                       
                    for i, item in enumerate(dataFilePropertyQuerySet):
                        propertyValuesQuerySet = PropertyValues.objects.filter(datafileproperty = item) 
                        propertyConditionDetailQuerySet = PropertyConditionDetail.objects.filter(datafileproperty = item )
                        for j, pv in enumerate(propertyValuesQuerySet):
                            pv.delete()
                            
                        for j, pcd in enumerate(propertyConditionDetailQuerySet):
                            pcd.delete()
                            
                        item.delete()
                        
                        
                    experimentalParCond_DataFileQuerySet= ExperimentalParCond_DataFile.objects.filter(datafile=obj.datafile)
                    for i, item in enumerate(experimentalParCond_DataFileQuerySet):
                        item.delete()

                    obj.datafile.delete()
                    publicArticle.delete()                                                                                                                  

                    pathslist=Path.objects.all()   
                    path=Path() 
                    for cifdir in pathslist:
                        path = cifdir
                        if os.path.isdir(path.cifs_dir):
                            break
                                        
               
                    ciffileout = os.path.join(path.cifs_dir,filename)
                    print "archivo a borrar"
                    print ciffileout
                    try:
                        if os.path.isfile(ciffileout):
                            os.remove(ciffileout)                    
                    except Exception as e:
                        raise Http404('%s object no deleted yet.' % (force_unicode(e)))
                                
                else:
                    dataFileTemp = DataFileTemp.objects.get(filename__exact=obj.filename)
                    publicArticleTemp =  dataFileTemp.publication
                    
                    dataFilePropertyTempQuerySet = DataFilePropertyTemp.objects.filter(datafiletemp=dataFileTemp)                       
                    for i, item in enumerate(dataFilePropertyTempQuerySet):
                        propertyValuesTempQuerySet = PropertyValuesTemp.objects.filter(datafilepropertytemp = item ) 
                        propertyConditionDetailTempQuerySet = PropertyConditionDetailTemp.objects.filter(datafileproperty = item)
                        for j, pvt in enumerate(propertyValuesTempQuerySet):
                            pvt.delete()
                            
                        for j, pcdt in enumerate(propertyConditionDetailTempQuerySet):
                            pcdt.delete()
                            
                        item.delete()
                        
                        
                    experimentalParCondTemp_DataFileTempQuerySet= ExperimentalParCondTemp_DataFileTemp.objects.filter(datafiletemp=dataFileTemp)
                    for i, item in enumerate(experimentalParCondTemp_DataFileTempQuerySet):
                        item.delete()

                   
                    dataFileTemp.delete()
                    publicArticleTemp.delete()
                    obj.delete()                  
                #obj.delete()
            else:
                messages.set_level(request, messages.ERROR)
                messages.error(request, 'the process was not done: ' + '%s object no unpublished yet.' % (force_unicode(obj))) 
                                  
    
            
            
        def delete_view(self, request, object_id, extra_context=None):    
            opts = self.model._meta
            app_label = opts.app_label
            try:
                obj = self.model._default_manager.get(pk=object_id)
            except self.model.DoesNotExist:
                obj = None
                    
            print obj   
            if obj is None:
                raise Http404('%s object with primary key %r does not exist.' % (force_unicode(opts.verbose_name), escape(object_id)))
              
            using = router.db_for_write(self.model)  
     
     
            (deleted_objects, perms_needed, protected) = get_deleted_objects([obj], opts, request.user, self.admin_site, using)
            if request.POST: # The user has already confirmed the deletion.
                if perms_needed:
                    raise PermissionDenied
                obj_display = force_unicode(obj)
                self.log_deletion(request, obj, obj_display)
                
              
               
                #queryset = PuntualGroupGroups.objects.filter(puntualgroupnames=obj)
                #self.delete_model_queryset( request, queryset)
                self.delete_model(request, obj)
    
                self.message_user(request,('The %(name)s "%(obj)s" was deleted successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj_display)})
    
                if not self.has_change_permission(request, None):
                    return HttpResponseRedirect(reverse('admin:index',
                                                        current_app=self.admin_site.name))
                return HttpResponseRedirect(reverse('admin:%s_%s_changelist' %
                                            (opts.app_label, opts.module_name),
                                            current_app=self.admin_site.name))
    
            object_name = force_unicode(opts.verbose_name)
    
            if perms_needed or protected:
                title = ("Cannot delete %(name)s") % {"name": object_name}
            else:
                title = ("Are you sure?")
    
            context = {
                "title": title,
                "object_name": object_name,
                "object": obj,
                "deleted_objects": deleted_objects,
                "perms_lacking": perms_needed,
                "protected": protected,
                "opts": opts,
                "app_label": app_label,
            }
            context.update(extra_context or {})
    
            return TemplateResponse(request, self.delete_confirmation_template or [
                "admin/%s/%s/delete_confirmation.html" % (app_label, opts.object_name.lower()),
                "admin/%s/delete_confirmation.html" % app_label,
                "admin/delete_confirmation.html"
            ], context, current_app=self.admin_site.name)
         
        def save_model(self, request, obj, form, change):    
            try:
                pathslist=Path.objects.all()      
                pathexist = 0
                cifs_dir=''    
                for cifdir in pathslist:
                    paths=Path() 
                    paths = cifdir
                    if os.path.isdir(paths.cifs_dir_valids): 
                        pathexist = 1
                        cifs_dir= paths.cifs_dir_valids
                        break
                    
                if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue') and not request.POST.has_key('_save'):
                    print "pass"
                elif  request.POST.has_key('_addanother'): 
                    print request.POST.get('_addanother',False)
                elif request.POST.has_key('_continue'): 
                    print request.POST.get('_continue',False)
                elif request.POST.has_key('_save'):
                    print request.POST.get('_save',False)
                    if (request.POST.get('publish',False)  != False):

                        
                        properties_ids= requestPostToIntList(request.POST,'properties')  
                        phase_name = requestPostCheck(request.POST,'phase_name')  
                        reference = requestPostCheck(request.POST,'reference')  
                        title = requestPostCheck(request.POST,'title')  
                        phase_generic = requestPostCheck(request.POST,'phase_generic')  
                        pages_number = requestPostToInt(request.POST,'pages_number') 
                        journal = requestPostCheck(request.POST,'journal') 
                        year = requestPostToInt(request.POST,'year')
                        volume = requestPostToInt(request.POST,'volume')
                        first_page = requestPostToInt(request.POST,'first_page')
                        last_page = requestPostToInt(request.POST,'last_page') 
                        authors = requestPostCheck(request.POST,'authors')  
                        issue = requestPostCheck(request.POST,'issue')  
                        cod_code = requestPostToInt(request.POST,'cod_code') 
                        chemical_formula = requestPostCheck(request.POST,'chemical_formula')  
                        publish = requestPostCheck(request.POST,'publish') 
                        experimentalcon = requestPostCheck(request.POST,'experimentalcon') 
            


 
                    
                    
                        filelist = []    
                        filelist.append(obj.filename ) 
                        estr = Extractor(str(paths.cifs_dir_valids),str(paths.core_dic_filepath),str(paths.mpod_dic_filepath),str(paths.cifs_dir_output),filelist);
                        estr.extractConditions(True,request.POST)
                        estr.extractPublarticleAndDataFile_Data(True,request.POST)
                        estr.extractProperties(True,request.POST)
                        
                         
 
                        if not obj.datepublished:
                            obj.datepublished = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                            
                        #obj.reportvalidation = reportvalidation
                        obj.publish = True
                        code=None
                        for key,code in estr.data_code.items():
                            code=estr.data_code[key[0],key[1]]
                            
                            
                        dataFile = None
                        try:
                            dataFile = DataFile.objects.get(code=code)
                            obj.datafile = dataFile
                            obj.save()  
                        except Exception  as error:
                            print "message in the function get_conds for debug purposes.  Message({0}): {1}".format(99, error)  
                            messages.set_level(request, messages.ERROR)
                            messages.error(request, 'the process was not done: Error' + '%s .' % (error) )
                        
                        try:
                            """pathslist=Path.objects.all()      
                            path=Path() 
                            for cifdir in pathslist:
                                path = cifdir
                                if os.path.isdir(path.cifs_dir):
                                    break
                            """
                           
                      
                             
                            ciffilein =os.path.join(paths.cifs_dir_valids, obj.filename)
                            ciffileout = os.path.join(paths.cifs_dir,str(code) + ".mpod")
                             
            
                   
                            datacode = "data_"+ obj.filename.replace('.mpod', ' ')
                            newdatacode =   "data_" + str(code)
                            print datacode
                            print newdatacode
                            print ciffilein
                            print ciffileout
                            
                            
                            try:
                                with open(ciffilein) as infile, open(ciffileout, 'w') as outfile:
                                    for line in infile:
                                        l = line.rstrip('\n')
                                        if l in datacode:
                                            print line
                                            line = newdatacode + '\n'
                                            outfile.write(line)
                                        else:                                        
                                            outfile.write(line)
                            except  IOError as e:
                                messages.add_message(request, messages.ERROR, "Error %s " % e.strerror)
                                
                            
                            
                            messageCategoryDetailQuerySet1=MessageCategoryDetail.objects.filter(messagecategory=MessageCategory.objects.get(pk=2))#2 for user notification
                            try:
                                for mcd in messageCategoryDetailQuerySet1:
                                    messageCategoryDetail = MessageCategoryDetail()
                                    messageCategoryDetail = mcd
                                     
                                    messageMail= MessageMail.objects.get(pk=messageCategoryDetail.message.pk)
                                    
                                    if messageMail.pk == 7:
                                        configurationMessage = ConfigurationMessage.objects.get(message=messageMail)
                                        smtpconfig= configurationMessage.account
                                        
                                        my_use_tls = False
                                        if smtpconfig.email_use_tls ==1:
                                            my_use_tls = True
                                        
                                            connection = get_connection(host=smtpconfig.email_host, 
                                                                                    port= int(smtpconfig.email_port ), 
                                                                                    username=smtpconfig.email_host_user, 
                                                                                    password=smtpconfig.email_host_password, 
                                                                                    use_tls=my_use_tls) 
                        
                             
                                            current_site = get_current_site(request)
                                            dataitem ="dataitem"
                                            forwardslash="/"
                                            message = render_to_string('notification_to_user_file_published.html', {
                                                                                            'regards':messageMail.email_regards,
                                                                                            'email_message':  messageMail.email_message,
                                                                                            'user': obj.authuser,
                                                                                            'domain': current_site.domain,
                                                                                            'code':  str(code),
                                                                                            'dataitem': dataitem,
                                                                                            'forwardslash': forwardslash,
                                                                                            
                                                                                            })
                                            
                                            print message
                         
                                            send_mail(
                                                            messageMail.email_subject,
                                                            message,
                                                            smtpconfig.email_host_user,
                                                            [obj.authuser.email],
                                                            connection=connection
                                                        )
                            except Exception  as e:
                                messages.add_message(request, messages.ERROR, "Error %s " % e)
                        

                        except ObjectDoesNotExist as error:
                                    messages.add_message(request, messages.ERROR, "Error %s " % error.message)
                    else:
                        objDataFile  = None
                        
                        if not obj.datafile:
                            datafile_tempid = requestPostCheck(request.POST,'datafile_tempid')  
                            dataFileTemp = DataFileTemp.objects.get(id = datafile_tempid)
                            
                            
                            try:
                                objDataFile = DataFile.objects.get(code= dataFileTemp.code)
                            except ObjectDoesNotExist as error:
                                print "message in the function FileUserAdmin.save_model for debug purposes.  Message({0}): {1}".format(99, error.message) 
                                messages.set_level(request, messages.WARNING)                        
                                messages.warning(request, 'the process was not done: ' + '%s object no published yet.' % (force_unicode(obj))) 
                                return
                        
                        else:
                            objDataFile = obj.datafile
                        
                        if objDataFile:
                            dataFilePropertyToDeleteQuerySet = DataFileProperty.objects.filter(datafile=objDataFile)
     
                            
                            #objDataFile = DataFile.objects.get(code=obj.datafile.code)
                            objPublArticle= objDataFile.publication
                            
                            publArticleQuerySet= PublArticle.objects.filter(id=objPublArticle.id)
    
                            for i,df in enumerate(dataFilePropertyToDeleteQuerySet):
                                dataFilePropertyToDeleteQuerySet[i].delete()
                                
                            filename = objDataFile.filename       
                            objDataFile.delete()
    
                          
                             
                            if publArticleQuerySet:
                                if len(publArticleQuerySet) == 1:
                                    for i,pa in enumerate(publArticleQuerySet):
                                        publArticleQuerySet[i].delete()
                                        
                                        
                             
                            obj.datafile = None       
                            obj.datepublished = None
                            obj.publish = False      
                            obj.save()  
                            
                            """pathslist=Path.objects.all()   
                            path=Path() 
                            for cifdir in pathslist:
                                path = cifdir
                                if os.path.isdir(path.cifs_dir):
                                    break
                            """
                                                
                       
                            ciffileout = os.path.join(paths.cifs_dir,filename)
                            print "archivo a borrar"
                            print ciffileout
                            try:
                                if os.path.isfile(ciffileout):
                                    os.remove(ciffileout)                    
                            except Exception as e:
                                raise Http404('%s object no deleted yet.' % (force_unicode(e)))
                            
                            
                            filelist = []    
                            filelist.append(obj.filename ) 
                            estr = Extractor(str(paths.cifs_dir_valids),str(paths.core_dic_filepath),str(paths.mpod_dic_filepath),str(paths.cifs_dir_output),filelist);
                            estr.extractConditions(False,request.POST)
                            estr.extractPublarticleAndDataFile_Data(False,request.POST)
                            estr.extractProperties(False,request.POST)
                                
                        else:
                            #messages.add_message(request, messages.ERROR, "An unexpected error occurred, consult technical support.")
                            messages.set_level(request, messages.ERROR)
                            messages.error(request, 'the process was not done: ' + '%s object no deleted yet.' % (force_unicode(obj))) 
     
                        
                        
                        
            except  Exception, e:
                        messages.add_message(request, messages.ERROR, "Error %s " % e.message)
 
    

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
           
            #print actions
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
        #print n
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
        #print request.path_info ==reverse('admin:Dictionaries_dictionary_category',kwargs={'id':id,'categorypk':categorypk})
        dictionary = Dictionary.objects.get(id__exact=id)
        result = super(DictionaryAdmin, self).change_view(request, id, extra_context)
        
        return result

    #al seleccionar un elemento de change_list_results.html
    def change_view(self, request, object_id, extra_context=None):
        print extra_context
         
        extra = {
            'title': 'Change Property',
            'original':'Property',

        }
        #print self.model._meta
        
        result = super(DictionaryAdmin, self).change_view(request, object_id, extra_context=extra)
        
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
        print 'dictionary selectlist_view'
        temp_list_display_links = self.list_display_links
        self.list_display_links = (None, )
        response = self.changelist_view(request, extra_context)
        self.list_display_links = temp_list_display_links
        return response
   

admin.site.register(Dictionary, DictionaryAdmin)


class FakeMeta:
        abstract            = not True
        app_label           = None
        module_name         = None
        verbose_name        = None
        verbose_name_plural = None
        
        get_ordered_objects = list
        def get_add_permission(self):    return 'add_%s'    % self.module_name
        def get_change_permission(self): return 'change_%s' % self.module_name
        def get_delete_permission(self): return 'delete_%s' % self.module_name
        def __init__(self, name, verbose_name=None, verbose_plural=None,app_label=None):
                self.app_label = app_label
                self.module_name         = name
                self.verbose_name        = verbose_name or name
                self.verbose_name_plural = verbose_plural or '%ss'%self.verbose_name
         
     
                
class DummyModel:
        _meta = FakeMeta('DummyModel',None,None,"DummyApp")
         
        
 

class DummyModelAdmin(admin.ModelAdmin):
        # see django.contrib.admin.options.ModelAdmin.get_urls()
        
        def get_urls(self):
            def wrap(view):
                def wrapper(*args, **kwargs):
                    return self.admin_site.admin_view(view)(*args, **kwargs)
                wrapper.model_admin = self
                return update_wrapper(wrapper, view)
    
            urls = super(DummyModelAdmin,self).get_urls()
    
            info = self.model._meta.app_label, self.model._meta.module_name
            n='%s_%s_save' % info
            #print n
            #Dictionaries_dictionary_review
            my_urls = [
                url(r'(?P<id>\d+)/dummy/$', wrap(self.save), name='%s_%s_save' % info),
               
            ]
 
            return my_urls + urls
        
       
    
      
        def save(self, request, id):
            print 'save'
            #dictionary = Dictionary.objects.get(pk=id)
            extra_context =   {}
    
            return render_to_response("admin/dummyapp/dummymodel/custom.html", extra_context, context_instance=RequestContext(request))
    

        def changelist_view(self, request, extra_context=None):
            print 'changelist_view DummyModel'
            extra_context = extra_context or {}
            extra_context['some_var'] = 'This is what I want to show'
            extra_context['title'] = 'Title module'
            extra_context['original'] ='Item to proccess'
            extra_context['app_label'] = "Custom app_label"
            
            
            for model in get_models():
                
                model.objects.all()
                new_object = model() # Create an instance of that model
                #model.objects.filter(...) # Query the objects of that model
                print "meta"
                print new_object._meta
                print "db_table: " + model._meta.db_table  
                
                print "\n"
                print "*--------------------------------------- " + model.__name__ + "---------------------------------------* "
                for x in model._meta.fields:
                    print x.name
            
               
       
            
            
            
            #return super(ImageAdmin, self).changelist_view(request, extra_context=extra_context)
        
            #return HttpResponseRedirect("test/image/change_form.html", extra_context)
            return render_to_response("admin/dummyapp/dummymodel/custom.html", extra_context, context_instance=RequestContext(request))
        
        
                # ...
        def add_view(self, request, form_url='', extra_context=None):
            print 'add_view DummyModel'
            pass
        
            #alseleccionar un elemento de menu
        def selectlist_view(self, request, extra_context=None):
            print 'selectlist_view DummyModel'
            temp_list_display_links = self.list_display_links
            self.list_display_links = (None, )
            response = self.changelist_view(request, extra_context)
            self.list_display_links = temp_list_display_links
            return response
 
admin.site.register([DummyModel], DummyModelAdmin)

 
 
class TypeInline(admin.TabularInline):
    model = Type
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'catalogproperty':
            urlactual=request.get_full_path()
            urlactual=urlactual.split('/')
            type_id=int(urlactual[4])
       
            
            kwargs["queryset"] = TypeDataProperty.objects.filter(type=Type.objects.filter(id=type_id))
            #kwargs["queryset"] = Type.objects.filter(~Q(id=type_id))
        return super(TypeInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
       
        

    extra = 0

 
    

class CatalogCrystalSystemInline(admin.TabularInline):
    model = CatalogCrystalSystem
    extra = 0
    
    



class CatalogPropertyAdmin(admin.ModelAdmin):
    form = CatalogPropertyAdminForm
    fieldsets = (
        ('Category Property', {
            'fields': ('name','description','active',)
        }),
    )
    
    
    #inlines = [TypeInline,CatalogCrystalSystemInline]
    
admin.site.register(CatalogProperty, CatalogPropertyAdmin)

class TypeAdmin(admin.ModelAdmin):
    list_display =('get_description','get_name',)  
    #list_display =('title', 'authors', 'journal','year','volume','issue','first_page','last_page','reference','pages_number')
    search_fields = ['name', 'description', ]
    list_filter = ('description',)
    
    fieldsets = (
        ('Type Information', {
            'fields': ('name','description','catalogproperty','active','tensor','clusterurl',)
        }),  
    )
          
          
    def get_name(self, obj):
        return  u'%s' % (obj.name)   
            
    def get_description(self, obj):
        return  u'%s' % (obj.description)  
    
    get_name.short_description = 'Name'
    get_name.allow_tags=True 
    
    get_description.short_description = 'Description'
    get_description.allow_tags=True 
    
admin.site.register(Type, TypeAdmin)


class CatalogAxisAdmin(admin.ModelAdmin):
    list_display =('get_name','get_description',)  
    #list_display =('title', 'authors', 'journal','year','volume','issue','first_page','last_page','reference','pages_number')
    search_fields = ['name', 'description', ]
    list_filter = ('name',)
          
          
    def get_name(self, obj):
        try:
            return  u'%s' % (obj.name)               
        except ObjectDoesNotExist as error:
            return ""
     
            
    def get_description(self, obj):
        try:
            return  u'%s' % (obj.description)               
        except ObjectDoesNotExist as error:
            return ""
    
    get_name.short_description = 'Name'
    get_name.allow_tags=True 
    
    get_description.short_description = 'Description'
    get_description.allow_tags=True 
    
admin.site.register(CatalogAxis, CatalogAxisAdmin)


class CatalogCrystalSystemAdmin(admin.ModelAdmin):
    form = CatalogCrystalSystemAdminForm
    list_display =('name','description','get_catalogproperty_description',)  
    ordering = ('catalogproperty__description',) 
    search_fields = ['name', 'description', ]
    list_filter = ('description','active')
    #readonly_fields=['name','description','active']

        
    def get_catalogproperty_description(self, obj):
        try:
            return  u'%s' % (obj.catalogproperty.description)               
        except ObjectDoesNotExist as error:
            return ""

    get_catalogproperty_description.short_description = 'Property'
    get_catalogproperty_description.allow_tags=True 
    
    def get_fieldsets(self, *args, **kwargs):
        return  (
            ('Crystal System', {
                'fields': ('name','description','active','catalogproperty','type','catalogpointgroup','pointgroupdetail','puntualgroupnames','puntualgroupnamesdetail','axis','axisdetail'),
            }),
        )
        
    def save_model(self, request, obj, form, change):
        print 'CatalogCrystalSystemAdmin_save_model'
        print request.POST
        print obj.name
        print form.changed_data # list name of field was changed
        print change #True or False
        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue') and not request.POST.has_key('_save'):
            print "pass"
        elif  request.POST.has_key('_addanother') or request.POST.has_key('_continue') or request.POST.has_key('_save'):
            if change:
                obj.save() 
                
            catalogpointgroup_id = requestPostToInt(request.POST,'catalogpointgroup')
            puntualgroupnames_id = requestPostToInt(request.POST,'puntualgroupnames')
            type_id  = requestPostToInt(request.POST,'type')
            del_catalogpointgroup_ids = requestPostToIntList(request.POST,'delete_catalogpointgroup')
            del_puntualgroupnames_ids = requestPostToIntList(request.POST,'delete_puntualgroupnames')
            axis_new_ids = requestPostToIntList(request.POST,'axis')
            typeSelected = Type.objects.get(id= type_id)
            puntualgroupnamesSelected = PuntualGroupNames.objects.get(id= puntualgroupnames_id)
            catalogpointgroupSelected = CatalogPointGroup.objects.get(id=catalogpointgroup_id)
            
            
            if axis_new_ids:
                axis_old_ids = CrystalSystemAxis.objects.filter(catalogcrystalsystem=obj,type_id = type_id,catalogpointgroup= catalogpointgroupSelected,puntualgroupnames = puntualgroupnamesSelected,active=1).values_list('axis_id',flat=True)  
                listAB = list(set(axis_old_ids) & set(axis_new_ids))
                newlist = []
                oldlist = []
                for c in axis_old_ids:
                    if c not in listAB:
                        oldlist.append(str(c))
            
                for c in axis_new_ids:
                    if c not in listAB:
                        newlist.append(str(c))
                        
                
                if len(newlist) != 0:
                    for i,o in enumerate(newlist):
                        #csa = CrystalSystemAxis.objects.get(catalogcrystalsystem=obj,type_id = type_id, axis_id = newlist[i],active=0)
                        csaQuerySet = CrystalSystemAxis.objects.filter(axis_id=newlist[i],catalogcrystalsystem=obj,type_id = type_id,catalogpointgroup= catalogpointgroupSelected,puntualgroupnames = puntualgroupnamesSelected,active=0)
                        if csaQuerySet:
                            csa =   csaQuerySet[0]
                        
                            csa.active = 1
                            csa.save()
                        else:
                            csa=CrystalSystemAxis()
                            csa.active = 1
                            csa.catalogcrystalsystem = obj
                            csa.axis = CatalogAxis.objects.get(id=newlist[i])
                            csa.type = typeSelected
                            csa.catalogpointgroup= catalogpointgroupSelected
                            csa.puntualgroupnames = puntualgroupnamesSelected
                            csa.save()
                            
                        del csa
                        
                    print 'save'
                
                if len(oldlist) != 0:
                    for i,o in enumerate(oldlist):
                        csa = CrystalSystemAxis.objects.get(catalogcrystalsystem=obj,type_id = type_id, axis_id = oldlist[i],active=1)
                        if csa:
                            csa.active = 0
                            csa.save()
                            #catalogaxisOldQuerySet[i].delete()
                        del csa
                        
                    print 'delete'
 
 
    
            if del_catalogpointgroup_ids or del_puntualgroupnames_ids:
 
                for id in del_puntualgroupnames_ids:
                    catalogpointgroupSelected = CatalogPointGroup.objects.get(id= id)
                    cspgn=CrystalSystemPuntualGroupNames.objects.get(catalogcrystalsystem=obj,puntualgroupnames_id=id,type_id = type_id)
                    cspgn.active = 0
                    print cspgn.puntualgroupnames.name
                    cspgn.save()
                    del cspgn
                    
                for id in del_catalogpointgroup_ids:
                    cspg=CrystalSystemPointGroup.objects.get(catalogcrystalsystem=obj,catalogpointgroup=catalogpointgroupSelected,type_id = type_id)
                    cspg.active = 0
                    cspg.save()
                    #cspg.delete()
                    del cspg
  
            else:
                if  (catalogpointgroup_id == 45  and  puntualgroupnames_id  != 21 ):
                    if obj.pk: 
                        crystalsystempuntualgroupnamesQuerySet = CrystalSystemPuntualGroupNames.objects.filter(catalogcrystalsystem=obj,puntualgroupnames=puntualgroupnamesSelected,type=typeSelected,active =1)
                        if  crystalsystempuntualgroupnamesQuerySet:
                            messages.set_level(request, messages.WARNING)
                            messages.warning(request, 'the process was not done, puntual group names "'+ puntualgroupnamesSelected.name +'" already exist for this crystal system: ' + typeSelected.description)
                        else:
                            crystalsystempuntualgroupnamesQuerySet = CrystalSystemPuntualGroupNames.objects.filter(catalogcrystalsystem=obj,puntualgroupnames=puntualgroupnamesSelected,type=typeSelected,active =0)
                            if crystalsystempuntualgroupnamesQuerySet:
                                for i,o in enumerate(crystalsystempuntualgroupnamesQuerySet):
                                    crystalsystempuntualgroupnamesQuerySet[i].active = True
                                    crystalsystempuntualgroupnamesQuerySet[i].save()
    
                                crystalsystempointgroupQuerySet = CrystalSystemPointGroup.objects.filter(catalogcrystalsystem=obj, type=typeSelected,active =1)
                                if crystalsystempointgroupQuerySet:
                                    for i,o in enumerate(crystalsystempointgroupQuerySet):
                                        crystalsystempointgroupQuerySet[i].active = False
                                        crystalsystempointgroupQuerySet[i].save()
                    
                            else:
                                crystalsystempuntualgroupnames=CrystalSystemPuntualGroupNames()
                                crystalsystempuntualgroupnames.catalogcrystalsystem = obj
                                crystalsystempuntualgroupnames.puntualgroupnames= puntualgroupnamesSelected
                                crystalsystempuntualgroupnames.type=typeSelected
                                crystalsystempuntualgroupnames.active = True
                                crystalsystempuntualgroupnames.save()
                                
                                crystalsystempointgroupQuerySet = CrystalSystemPointGroup.objects.filter(catalogcrystalsystem=obj, type=typeSelected,active =1)
                                if crystalsystempointgroupQuerySet:
                                    for i,o in enumerate(crystalsystempointgroupQuerySet):
                                        crystalsystempointgroupQuerySet[i].active = False
                                        crystalsystempointgroupQuerySet[i].save()
                    else:
                        obj.save()
                        crystalsystempuntualgroupnames=CrystalSystemPuntualGroupNames()
                        crystalsystempuntualgroupnames.catalogcrystalsystem = obj
                        crystalsystempuntualgroupnames.puntualgroupnames= puntualgroupnamesSelected
                        crystalsystempuntualgroupnames.type=typeSelected
                        crystalsystempuntualgroupnames.active = True
                        crystalsystempuntualgroupnames.save()
    
                elif (catalogpointgroup_id  != 45  and  puntualgroupnames_id== 21):
                    if obj.pk: 
                        crystalsystempointgroupQuerySet = CrystalSystemPointGroup.objects.filter(catalogcrystalsystem=obj,catalogpointgroup=catalogpointgroupSelected, type=typeSelected,active =1)
                        if  crystalsystempointgroupQuerySet:
                            messages.set_level(request, messages.WARNING)
                            messages.warning(request, 'the process was not done, puntual group  "'+ catalogpointgroupSelected.name +'" already exist for this crystal system: ' + typeSelected.description)
                        else:
                            crystalsystempointgroupQuerySet = CrystalSystemPointGroup.objects.filter(catalogcrystalsystem=obj,catalogpointgroup=catalogpointgroupSelected, type=typeSelected,active =0)
                            if crystalsystempointgroupQuerySet:
                                for i,o in enumerate(crystalsystempointgroupQuerySet):
                                    crystalsystempointgroupQuerySet[i].active = True
                                    crystalsystempointgroupQuerySet[i].save()
                                        
                                
                                crystalsystempuntualgroupnamesQuerySet = CrystalSystemPuntualGroupNames.objects.filter(catalogcrystalsystem=obj,type=typeSelected,active =1)
                                if crystalsystempuntualgroupnamesQuerySet:
                                    for i,o in enumerate(crystalsystempuntualgroupnamesQuerySet):
                                        print crystalsystempuntualgroupnamesQuerySet[i].puntualgroupnames
                                        crystalsystempuntualgroupnamesQuerySet[i].active = False
                                        crystalsystempuntualgroupnamesQuerySet[i].save()
   
                            else:       
                                crystalsystempointgroup=CrystalSystemPointGroup()
                                crystalsystempointgroup.catalogcrystalsystem = obj
                                crystalsystempointgroup.type=typeSelected
                                crystalsystempointgroup.active = True
                                crystalsystempointgroup.catalogpointgroup= catalogpointgroupSelected
                                crystalsystempointgroup.save()
                            
                                crystalsystempuntualgroupnamesQuerySet = CrystalSystemPuntualGroupNames.objects.filter(catalogcrystalsystem=obj,type=typeSelected,active =1)
                                if crystalsystempuntualgroupnamesQuerySet:
                                    for i,o in enumerate(crystalsystempuntualgroupnamesQuerySet):
                                        print crystalsystempuntualgroupnamesQuerySet[i].puntualgroupnames
                                        crystalsystempuntualgroupnamesQuerySet[i].active = False
                                        crystalsystempuntualgroupnamesQuerySet[i].save()
                    else:
                        obj.save()
                        crystalsystempointgroup=CrystalSystemPointGroup()
                        crystalsystempointgroup.catalogcrystalsystem = obj
                        crystalsystempointgroup.type=typeSelected
                        crystalsystempointgroup.active = True
                        crystalsystempointgroup.catalogpointgroup= catalogpointgroupSelected
                        crystalsystempointgroup.save()
                
                 
                else:
                    print  "Error o warning"
  
            
            #obj.save()
    
admin.site.register(CatalogCrystalSystem, CatalogCrystalSystemAdmin)


class CatalogPointGroupAdmin(admin.ModelAdmin):
    list_display =('name',)  
    ordering = ('name',) 
    search_fields = ['name', ]
    #list_filter = ('name',)

        
    def get_catalogpointgroup_name(self, obj):
        try:
            return  u'%s' % (obj.name)               
        except ObjectDoesNotExist as error:
            return ""

    get_catalogpointgroup_name.short_description = 'Point Group'
    get_catalogpointgroup_name.allow_tags=True 
    
admin.site.register(CatalogPointGroup, CatalogPointGroupAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display =('name',)  
    ordering = ('name',) 
    search_fields = ['name', ]
    #list_filter = ('name',)

admin.site.register(Category, CategoryAdmin)

class PuntualGroupGroupsInline(admin.TabularInline):
    model = PuntualGroupGroups
    insert_after = 'description'
    

class PuntualGroupNamesAdmin(admin.ModelAdmin):
    list_display =('name',)  
    ordering = ('name',) 
    search_fields = ['name', ]
    #list_filter = ('name',)
    #fields = ('name', 'display_point_group')
 
    """
    fields = (
        'name',
        'description'
    )
     
    inlines = [
            PuntualGroupGroupsInline,
        ]
    
    """
   
 
    
    def selectlist_view(self, request, extra_context=None):
            print 'PuntualGroupNames_selectlist_view'
            temp_list_display_links = self.list_display_links
            self.list_display_links = (None, )
            response = self.changelist_view(request, extra_context)
            self.list_display_links = temp_list_display_links
            return response
    
    def change_view(self, request, object_id, extra_context=None):
        print 'PuntualGroupNames_change_view'
        
        extra = {
            'n1': 'Change Property', 
            'n2':'Property',
        }
        
        #print self.model._meta
        
        result = super(PuntualGroupNamesAdmin, self).change_view(request, object_id, extra_context=extra)        
        puntualGroupNames = PuntualGroupNames.objects.get(id__exact=object_id)
        #if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):

        return result
  
    
    def save_model(self, request, obj, form, change):
        print 'PuntualGroupNames_save_model'
        print request.POST
        print obj.name
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
            
            obj.save()
     

    
#admin.site.register(PuntualGroupNames, PuntualGroupNamesAdmin)

 
        



class GroupNamesDetailAdmin(admin.ModelAdmin):
    form=GroupNamesDetailAdminForm
    """fieldsets = (
        ('Group Names Detail', {
            'fields': ('puntualgroupnames', 'catalogpointgroup',)
        }),
    )
    """
    readonly_fields=['name','description']
    
    
    def get_fieldsets(self, *args, **kwargs):
        return  (
            ('Group Names Detail', {
                'fields': ('name','description', 'catalogpointgroup',),
            }),
        )
 
    
    def changelist_view(self, request, extra_context=None):
        extra_context = {
            #'groups': [x[0] for x in groups],
            'obj':'obj',
        }
        return super(GroupNamesDetailAdmin, self).changelist_view(request, extra_context=extra_context)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        model = self.model
        opts = model._meta
        obj = self.get_object(request, unquote(object_id))
        if obj is None:
            raise Http404(('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})
                                                                                           
        extra_context = extra_context or {}
        extra_context = {
                'original':obj,

            }
        return admin.ModelAdmin.change_view(self, request, object_id, form_url=form_url, extra_context=extra_context)
    
    def delete_model_queryset(self, request, queryset):
        for obj in queryset:
            print obj
            #obj.delete()
            
    def delete_model(self, request, obj):
        pass
        #obj.delete()
        
           
    def delete_view(self, request, object_id, extra_context=None):    
        opts = self.model._meta
        app_label = opts.app_label
        try:
            obj = self.model._default_manager.get(pk=object_id)
        except self.model.DoesNotExist:
            obj = None
                
        print obj   
        if obj is None:
              raise Http404('%s object with primary key %r does not exist.' % (force_unicode(opts.verbose_name), escape(object_id)))
          
        using = router.db_for_write(self.model)  
 
 
        (deleted_objects, perms_needed, protected) = get_deleted_objects([obj], opts, request.user, self.admin_site, using)
        if request.POST: # The user has already confirmed the deletion.
            if perms_needed:
                raise PermissionDenied
            obj_display = force_unicode(obj)
            self.log_deletion(request, obj, obj_display)
            
            #TODO:checar primero que no alla sido usado en catalog_property_detail
           
            queryset = PuntualGroupGroups.objects.filter(puntualgroupnames=obj)
            self.delete_model_queryset( request, queryset)
            self.delete_model(request, obj)

            self.message_user(request,_('The %(name)s "%(obj)s" was deleted successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj_display)})

            if not self.has_change_permission(request, None):
                return HttpResponseRedirect(reverse('admin:index',
                                                    current_app=self.admin_site.name))
            return HttpResponseRedirect(reverse('admin:%s_%s_changelist' %
                                        (opts.app_label, opts.module_name),
                                        current_app=self.admin_site.name))

        object_name = force_unicode(opts.verbose_name)

        if perms_needed or protected:
            title = ("Cannot delete %(name)s") % {"name": object_name}
        else:
            title = ("Are you sure?")

        context = {
            "title": title,
            "object_name": object_name,
            "object": obj,
            "deleted_objects": deleted_objects,
            "perms_lacking": perms_needed,
            "protected": protected,
            "opts": opts,
            "app_label": app_label,
        }
        context.update(extra_context or {})

        return TemplateResponse(request, self.delete_confirmation_template or [
            "admin/%s/%s/delete_confirmation.html" % (app_label, opts.object_name.lower()),
            "admin/%s/delete_confirmation.html" % app_label,
            "admin/delete_confirmation.html"
        ], context, current_app=self.admin_site.name)
        
    def save_model(self, request, obj, form, change):
        print 'GroupNamesDetailAdmin_save'
        print request.POST
        print obj.name
        print form.changed_data # list name of field was changed
        print change #True or False
        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue') and not request.POST.has_key('_save'):
            print "pass"
 
        elif request.POST.has_key('_save') or  request.POST.has_key('_continue') or request.POST.has_key('_addanother'): 
            obj.name = request.POST.get('name',False)
            obj.description = request.POST.get('description',False)
            obj.save()
            catalogpointgroup_new_ids = requestPostToIntList(request.POST,'catalogpointgroup')
            catalogpointgroup_old_ids =  PuntualGroupGroups.objects.filter(puntualgroupnames=obj).values_list('catalogpointgroup_id',flat=True)  
            listAB = list(set(catalogpointgroup_old_ids) & set(catalogpointgroup_new_ids))

            newlist = []
            oldlist = []
            for c in catalogpointgroup_old_ids:
                if c not in listAB:
                    oldlist.append(str(c))
        
            for c in catalogpointgroup_new_ids:
                if c not in listAB:
                    newlist.append(str(c))
                    
            if len(newlist) != 0:
                catalogpointgroupNewQuerySet=CatalogPointGroup.objects.filter(id__in=newlist)
                for i,o in enumerate(catalogpointgroupNewQuerySet):
                    pgg=PuntualGroupGroups()
                    pgg.catalogpointgroup = catalogpointgroupNewQuerySet[i]
                    pgg.puntualgroupnames = obj
                    pgg.save()
                    
                print 'save'
            
            if len(oldlist) != 0:
                catalogpointgroupOldQuerySet=CatalogPointGroup.objects.filter(id__in=oldlist)
                for i,o in enumerate(catalogpointgroupOldQuerySet):
                    print catalogpointgroupOldQuerySet[i].name
                    catalogpointgroupOldQuerySet[i].delete()
                    
                print 'delete'
                            
                            
        """elif request.POST.has_key('_save'):
            obj.name = request.POST.get('name',False)
            obj.description = request.POST.get('description',False)
            #obj.save()
            catalogpointgroup=  request.POST.getlist('catalogpointgroup',False)
            catalogpointgroup_ids = []
            for id in catalogpointgroup:
                catalogpointgroup_ids.append(int(id))
                
            catalogpointgroupQuerySet=CatalogPointGroup.objects.filter(id__in=catalogpointgroup_ids)
 
            for i, cpg in enumerate( catalogpointgroupQuerySet ):
                pgg=PuntualGroupGroups()
                pgg.catalogpointgroup = catalogpointgroupQuerySet[i]
                pgg.puntualgroupnames = obj
                #pgg.save()
                del pgg"""
   
        #super(GroupNamesDetailAdmin, self).save_model(request, obj, form, change)

    def queryset(self, request):
        qs = super(GroupNamesDetailAdmin, self).queryset(request)

        return qs.all().exclude(id=21)
        #return super(GroupNamesDetailAdmin, self).get_queryset().all().exclude(id=21)

admin.site.register(GroupNamesDetail, GroupNamesDetailAdmin)

class CatalogPropertyDetailAdmin(admin.ModelAdmin):
    list_display =('name','get_type_description','get_crystalsystem_catalogproperty_description','get_crystalsystem_description','get_catalogaxis_name','get_catalogpointgroup_name','get_puntualgroupnames_name','dataproperty')  
    #list_display =('title', 'authors', 'journal','year','volume','issue','first_page','last_page','reference','pages_number')
    ordering = ('crystalsystem__catalogproperty__description',) 
    search_fields = [ 'crystalsystem__description','type__description','catalogaxis__name',]
    list_filter = ('crystalsystem__catalogproperty__description',)
    #list_select_related = True
    
    fieldsets = (
        ('Property Detail', {
            'fields': ('name','description')
        }),
        ('Catalog Types', {
            'fields': ('type', )
        }),
        ('Catalog Crystal System', {
            'fields': ('crystalsystem',)
        }),
        ('Property Tag', {
            'fields': ('dataproperty' ,)
        }),

        ('Catalog Point Group', {
            'fields': ('catalogpointgroup', )
        }),
        ('Catalog Puntual Group Names', {
            'fields': ('puntualgroupnames', )
        }),
            ('Catalog Axis', {
            'fields': ('catalogaxis', )
        }),
    )
          
          
          
    def get_type_name(self, obj):
        try:
            return  u'%s' % (obj.type.name)               
        except ObjectDoesNotExist as error:
            return ""
     
            
    def get_type_description(self, obj):
        try:
            return  u'%s' % (obj.type.description)               
        except ObjectDoesNotExist as error:
            return ""
    
    def get_crystalsystem_description(self, obj):
        try:
            return  u'%s' % (obj.crystalsystem.description)               
        except ObjectDoesNotExist as error:
            return ""    
        
    def get_crystalsystem_catalogproperty_description(self, obj):
        try:
            return  u'%s' % (obj.crystalsystem.catalogproperty.description)               
        except ObjectDoesNotExist as error:
            return ""
        
         
    def get_catalogaxis_name(self, obj):
        try:
            return  u'%s' % (obj.catalogaxis.name)               
        except ObjectDoesNotExist as error:
            return ""     
        
    def get_catalogpointgroup_name(self, obj):
        try:
            return  u'%s' % (obj.catalogpointgroup.name)               
        except ObjectDoesNotExist as error:
            return ""       
        
    def get_puntualgroupnames_name(self, obj):
        try:
            return  u'%s' % (obj.puntualgroupnames.name)               
        except ObjectDoesNotExist as error:
            return ""       
    
    get_type_name.short_description = 'Type Name'
    get_type_name.allow_tags=True 
    
    get_type_description.short_description = 'Type Description'
    get_type_description.allow_tags=True 
    
    get_crystalsystem_description.short_description = 'Crystal System'
    get_crystalsystem_description.allow_tags=True 
    
    get_crystalsystem_catalogproperty_description.short_description = 'Property'
    get_crystalsystem_catalogproperty_description.allow_tags=True 
    
    
    get_catalogaxis_name.short_description = 'Axis'
    get_catalogaxis_name.allow_tags=True 
    
    get_catalogpointgroup_name.short_description = 'Group'
    get_catalogpointgroup_name.allow_tags=True 
    
    get_puntualgroupnames_name.short_description = 'Groups'
    get_puntualgroupnames_name.allow_tags=True 
    
    
     
    
    
admin.site.register(CatalogPropertyDetail, CatalogPropertyDetailAdmin)


class TypeDataPropertyAdmin(admin.ModelAdmin):
 
    
    list_display =('type','dataproperty', )   
    list_filter = ('type__catalogproperty__description','type__description',)
    #fields = ['puntualgroupnames','catalogpointgroup','catalogpointgroup1']
    fieldsets = (
        ('Property information', {
            'fields': ('type','dataproperty',)
        }),

    )
 
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
       
        extra_context = {
                'original':'Type and Data Property',
                 
            }
 
        #print 'id_typedataproperty ' + str(object_id)
 
        return admin.ModelAdmin.change_view(self, request, object_id, form_url=form_url, extra_context=extra_context)
    
    
admin.site.register(TypeDataProperty, TypeDataPropertyAdmin)
 
 

   
 
            
#admin.site.register(DataPropertyDetail, DataPropertyDetailAdmin)

class PropertyAdmin(admin.ModelAdmin):
    pass
    
    
admin.site.register(Property,PropertyAdmin)










class TensorAdmin(admin.ModelAdmin):
    form=TensorAdminForm
    readonly_fields=['name','description','active']
   
    
    def get_fieldsets(self, *args, **kwargs):
        return  (
            ('Tensor', {
                'fields': ('errormessage','name','description','active','type','dataproperty','catalogcrystalsystem','catalogpointgroup','pointgroupdetail','puntualgroupnames','puntualgroupnamesdetail','axis','axisdetail','coefficients',('coefficientsrules','keynotation','zerocomponent','jquery',),'detailrules',),
            }),
        )
        
        
 
 
    
       
    def saverule(self, request,id):
        if request.method == 'POST':
            response_data = {}
            if int(id) == 1 or int(id) == 3:
                symmetry = True
            elif int(id) ==  2:
                symmetry = False
                
                
            jsutils = JSUtils()
            #catalogpropertydetaillist = request.POST.getlist('catalogpropertydetaillist[]',False)
            datapropertySelected = request.POST.getlist('datapropertySelected',False)
            propertydetaillistselected = request.POST.getlist('propertydetaillistselected[]',False)
            keynotationselected = request.POST.getlist('keynotationselected',False)
            zerocomponentselected = request.POST.getlist('zerocomponentselected[]',False)
            
            sourceList = []
            sourceListstr = ""
            targetListstr= ""
            kNotation = None
            if keynotationselected:
                kNotation= KeyNotation.objects.get(id=keynotationselected[0])
            
            size = 0
            if propertydetaillistselected:
                size = len(propertydetaillistselected) - 1
                for i, id in enumerate(propertydetaillistselected):
                    catalogPropertyDetailTemp= CatalogPropertyDetail.objects.get(id=id)
                    #sourceListstr.append(catalogPropertyDetailTemp.name)
                    if i < size:
                        sourceListstr +=   catalogPropertyDetailTemp.name + ', ' 
                    else:
                        sourceListstr +=   catalogPropertyDetailTemp.name 
                      
                    sourceList.append(catalogPropertyDetailTemp)

            if zerocomponentselected:
                size = len(zerocomponentselected) - 1
                for i, id in enumerate(zerocomponentselected):
                    catalogPropertyDetailTemp= CatalogPropertyDetailTemp.objects.get(id=id)
                    if i < size:
                        targetListstr +=   catalogPropertyDetailTemp.name + ', ' 
                    else:
                        targetListstr +=   catalogPropertyDetailTemp.name 
                    
                    
            for source in sourceList:
                keyNotationCatalogPropertyDetail = jsutils.getKeyNotationCatalogPropertyDetail(source,kNotation)
                keyNotationCatalogPropertyDetail.source =sourceListstr
                keyNotationCatalogPropertyDetail.target = targetListstr
                #keyNotationCatalogPropertyDetail.save()
            
            response_data['test'] = 'test'
     
        
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({"nothing to see": "this isn't happening"}),
                content_type="application/json"
            )
            
    def getrules(self, request,id):
        if request.method == 'POST':
            #coefficient_id = request.POST.get('coefficient')
            
            if int(id) == 1 or int(id) == 3:
                symmetry = True
            elif int(id) ==  2:
                symmetry = False
                
                
            jsutils = JSUtils()
            catalogpropertydetaillist = request.POST.getlist('catalogpropertydetaillist[]',False)
            catalogpropertydetailnames = request.POST.getlist('catalogpropertydetailnames[]',False)
            propertydetaillistselected = request.POST.getlist('propertydetaillistselected',False)
            keynotationselected = request.POST.getlist('keynotationselected',False)
            
            
            datapropertySelected_id = request.POST.get('datapropertySelected',False)
            datapropertySelected= Property.objects.get(id=int(datapropertySelected_id))  
            dimensions=datapropertySelected.tensor_dimensions.split(',')
            scij = None
            if len(dimensions) == 2:
                coefficients = N.zeros([int(dimensions[0]),int(dimensions[1])])    
                parts=datapropertySelected.tag.split('_')[-1]
                scij =parts.split('ij')
                
            keynotationlist= []
            response_data = {}
            for i, coefficient_id in enumerate(propertydetaillistselected):   
                obj=CatalogPropertyDetail.objects.get(id=coefficient_id)
                keyNotationCatalogPropertyDetail= jsutils.getKeyNotation(obj)
                if isinstance(keyNotationCatalogPropertyDetail, QuerySet):
                    
                    source_target_Dic = {}
                    size = len(keyNotationCatalogPropertyDetail) -1
                    for x,knotationpropertydetail in enumerate(keyNotationCatalogPropertyDetail):
                        keynotationlist.append(str(knotationpropertydetail.keynotation.id))
    
                        sourceList = [x.strip() for x in knotationpropertydetail.source.split(',')]
                        if len(sourceList) > 1:
                            targetList = [x.strip() for x in knotationpropertydetail.target.split(',')]
                            source_target_Dic[ tuple(sourceList)]=targetList
                        elif len(sourceList) == 1:
                            targetList = [x.strip() for x in knotationpropertydetail.target.split(',')]
                            source_target_Dic[obj.name]=targetList
     
     
                    jsutils.getrules( obj.name,scij,source_target_Dic,False,symmetry)
                    
     
                else:
     
                    keynotationlist.append(str(keyNotationCatalogPropertyDetail.keynotation.id))
                    targetList = [x.strip() for x in keyNotationCatalogPropertyDetail.target.split(',')]
                    source_target_Dic = {}
                    source_target_Dic[obj.name]=targetList
                    
                    if keyNotationCatalogPropertyDetail.keynotation.id ==4 or keyNotationCatalogPropertyDetail.keynotation.id ==6 or keyNotationCatalogPropertyDetail.keynotation.id ==5 or keyNotationCatalogPropertyDetail.keynotation.id ==10:
                        jsutils.getrules( obj.name,scij,source_target_Dic,True,symmetry)
                      
                    else:
                        jsutils.getrules( obj.name,scij,source_target_Dic, False,symmetry)
                    

                response_data['keynotationlist'] = keynotationlist
     
        
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({"nothing to see": "this isn't happening"}),
                content_type="application/json"
            )
            
        
    def get_urls(self):
            def wrap(view):
                def wrapper(*args, **kwargs):
                    return self.admin_site.admin_view(view)(*args, **kwargs)
                wrapper.model_admin = self
                return update_wrapper(wrapper, view)
    
            urls = super(TensorAdmin,self).get_urls()
    
            info = self.model._meta.app_label, self.model._meta.module_name
            getrules='%s_%s_getrules' % info
            saverule='%s_%s_saverule' % info
             
  
            my_urls = [
                url(r'^(.+)/getrules/$', wrap(self.getrules), name=getrules),
                url(r'^(.+)/saverule/$', wrap(self.saverule), name=saverule),
               
            ]
 
            return my_urls + urls
 
    """def changelist_view(self, request, extra_context=None):
        extra_context = {
            #'groups': [x[0] for x in groups],
            'obj':'obj',
        }
        return super(TensorAdmin, self).changelist_view(request, extra_context=extra_context)
    """
    
    """def change_view(self, request, object_id, form_url='', extra_context=None):
        model = self.model
        opts = model._meta
        obj = self.get_object(request, unquote(object_id))
        if obj is None:
            raise Http404(('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})
                                                                                           
        extra_context = extra_context or {}
        extra_context = {
                'original':obj,

            }
        return admin.ModelAdmin.change_view(self, request, object_id, form_url=form_url, extra_context=extra_context)"""
    
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    
    def delete_model_queryset(self, request, queryset):
        for obj in queryset:
            print obj
            #obj.delete()
            
    def delete_model(self, request, obj):
        pass
        #obj.delete()
        
           
    def delete_view(self, request, object_id, extra_context=None):    
        opts = self.model._meta
        app_label = opts.app_label
        try:
            obj = self.model._default_manager.get(pk=object_id)
        except self.model.DoesNotExist:
            obj = None
                
        print obj   
        if obj is None:
            raise Http404('%s object with primary key %r does not exist.' % (force_unicode(opts.verbose_name), escape(object_id)))
          
        using = router.db_for_write(self.model)  
 
 
        (deleted_objects, perms_needed, protected) = get_deleted_objects([obj], opts, request.user, self.admin_site, using)
        if request.POST: # The user has already confirmed the deletion.
            if perms_needed:
                raise PermissionDenied
            obj_display = force_unicode(obj)
            self.log_deletion(request, obj, obj_display)
            
            #TODO:checar primero que no alla sido usado en catalog_property_detail
           
            queryset = PuntualGroupGroups.objects.filter(puntualgroupnames=obj)
            self.delete_model_queryset( request, queryset)
            self.delete_model(request, obj)

            self.message_user(request,_('The %(name)s "%(obj)s" was deleted successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj_display)})

            if not self.has_change_permission(request, None):
                return HttpResponseRedirect(reverse('admin:index',
                                                    current_app=self.admin_site.name))
            return HttpResponseRedirect(reverse('admin:%s_%s_changelist' %
                                        (opts.app_label, opts.module_name),
                                        current_app=self.admin_site.name))

        object_name = force_unicode(opts.verbose_name)

        if perms_needed or protected:
            title = ("Cannot delete %(name)s") % {"name": object_name}
        else:
            title = ("Are you sure?")

        context = {
            "title": title,
            "object_name": object_name,
            "object": obj,
            "deleted_objects": deleted_objects,
            "perms_lacking": perms_needed,
            "protected": protected,
            "opts": opts,
            "app_label": app_label,
        }
        context.update(extra_context or {})

        return TemplateResponse(request, self.delete_confirmation_template or [
            "admin/%s/%s/delete_confirmation.html" % (app_label, opts.object_name.lower()),
            "admin/%s/delete_confirmation.html" % app_label,
            "admin/delete_confirmation.html"
        ], context, current_app=self.admin_site.name)
        
    def save_model(self, request, obj, form, change):
        print 'TensorAdmin_save'
        print request.POST
        print form.changed_data # list name of field was changed
        print change #True or False
        """if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue') and not request.POST.has_key('_save'):
            print "pass"
        elif  request.POST.has_key('_addanother'): 
            pass
            #obj.save()      
        elif request.POST.has_key('_continue'): 
            pass
            #obj.save()"""

        if request.POST.has_key('_save') or request.POST.has_key('_continue'):
            dataproperty_id = 0
            if request.POST.get('dataproperty',False)  != False:
                dataproperty_id = int(request.POST.get('dataproperty',False))
                print dataproperty_id
                datapropertySelected=Property.objects.get(id=int(dataproperty_id))
                print datapropertySelected
            
            catalogcrystalsystem_id = 0
            if request.POST.get('catalogcrystalsystem',False)  != False:
                catalogcrystalsystem_id = int(request.POST.get('catalogcrystalsystem',False))
                print catalogcrystalsystem_id
                
            type_id = 0
            if  request.POST.get('type',False) != False:
                type_id=int(request.POST.get('type',False))
                print type_id
                
            puntualgroupnames_id = 21
            if  request.POST.get('puntualgroupnames',False) != False:
                puntualgroupnames_id=int(request.POST.get('puntualgroupnames',False))
                print puntualgroupnames_id

            catalogpointgroup_id = 45
            if  request.POST.get('catalogpointgroup',False) != False:
                catalogpointgroup_id=int(request.POST.get('catalogpointgroup',False))
                print catalogpointgroup_id
                    
            catalogaxis_id = 4
            if  request.POST.get('axis',False) != False:
                catalogaxis_id=int(request.POST.get('axis',False))
                print catalogaxis_id
                
 
                


            if request.POST.getlist('coefficients',False):
                coefficients=  request.POST.getlist('coefficients',False)
                if coefficients[0] != '':
                    coefficients_ids = []
                    for id in coefficients:
                        coefficients_ids.append(int(id))
                        
                    try:
                        nameTempValuesQuerySet = CatalogPropertyDetailTemp.objects.filter(id__in= coefficients_ids).values('name')
                        coefficients_name_temp = []
                        if nameTempValuesQuerySet:
                            for field in nameTempValuesQuerySet:
                                coefficients_name_temp.append(field['name'])
                    
                        #TODO: checar que hacer si llos coefficnetes son nuevos
                        nameValuesQuerySet = CatalogPropertyDetail.objects.filter(   dataproperty_id = dataproperty_id,
                                                                                                                                            crystalsystem_id=catalogcrystalsystem_id,
                                                                                                                                            type_id=type_id,
                                                                                                                                            puntualgroupnames_id=puntualgroupnames_id,
                                                                                                                                            catalogpointgroup_id=catalogpointgroup_id,
                                                                                                                                            catalogaxis_id=catalogaxis_id).values('name')
                        coefficients_name = []
                        if nameValuesQuerySet:
                            for field in nameValuesQuerySet:
                                coefficients_name.append(field['name'])
                    
                        listAB = list(set(coefficients_name_temp) & set(coefficients_name))
                        
                        disctincttemp = []
                        disctinct = []
                        for c in coefficients_name_temp:
                            if c not in listAB:
                                disctincttemp.append(str(c))
                    
                        for c in coefficients_name:
                            if c not in listAB:
                                disctinct.append(str(c))
                                
                        if len(disctincttemp) != 0:
                            print disctincttemp
                            tempQuerySet= CatalogPropertyDetailTemp.objects.filter(name__in =disctincttemp)  
                            for i,obj in enumerate(tempQuerySet):
                                newObj= CatalogPropertyDetail()
                                newObj.name = tempQuerySet[i].name
                                newObj.dataproperty = Property.objects.get(id=int(dataproperty_id))
                                newObj.crystalsystem = CatalogCrystalSystem.objects.get(id=int(catalogcrystalsystem_id))
                                newObj.type = Type.objects.get(id=int(type_id))
                                newObj.puntualgroupnames = PuntualGroupNames.objects.get(id=int(puntualgroupnames_id))
                                newObj.catalogpointgroup = CatalogPointGroup.objects.get(id=int(catalogpointgroup_id))
                                newObj.catalogaxis = CatalogAxis.objects.get(id=int(catalogaxis_id))
                                print 'save ' + newObj.name 
                                newObj.save()
                                
                                
                
                        if len(disctinct) != 0:
                                print disctinct
                                for i,c in enumerate(disctinct):
                                    oldObj= CatalogPropertyDetail.objects.get(name__exact =c,
                                                                                                                    dataproperty_id = dataproperty_id,
                                                                                                                    crystalsystem_id=catalogcrystalsystem_id,
                                                                                                                    type_id=type_id,
                                                                                                                    puntualgroupnames_id=puntualgroupnames_id,
                                                                                                                    catalogpointgroup_id=catalogpointgroup_id,
                                                                                                                   catalogaxis_id=catalogaxis_id)  
                                    oldObj.delete()
                                    print 'delete ' + oldObj.name 
                         
                        if len(disctincttemp) == 0 and len(disctinct) == 0:
                            messages.set_level(request, messages.WARNING)
                            messages.warning(request, 'The process was not done, no new coefficient selected for this property: ' + datapropertySelected.name)    
                            
                                    
                    except ObjectDoesNotExist as error:
                        messages.set_level(request, messages.ERROR)
                        messages.error(request, 'The process was not done: ' + error) 
                        
                    
                    
                else:
                    messages.set_level(request, messages.WARNING)
                    messages.warning(request, 'The process was not done, no coefficient selected for this property: ' + datapropertySelected.name) 
                    #messages.set_level(request, messages.ERROR)
                    #messages.ERROR(request, 'The process was not done')
                
            else:
                messages.set_level(request, messages.WARNING)
                messages.warning(request, 'the process was not done, no coefficient selected for this property: ' + datapropertySelected.name)
                
   
        #super(TensorAdmin, self).save_model(request, obj, form, change)




    def queryset(self, request):
        qs = super(TensorAdmin, self).queryset(request)

        return qs.all()
        #return super(TensorAdmin, self).get_queryset().all().exclude(id=21)
 
admin.site.register(Tensor,TensorAdmin)




#Modul for permissions
#admin.site.register(Permission)
