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
from django.core.exceptions import ObjectDoesNotExist
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


#admin.site.register(ExperimentalParCond,ExperimentalParCondAdmin)

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
 
    
        def get_fieldsets(self, request, obj=None):
            fieldsets = super(FileUserAdmin, self).get_fieldsets(request, obj)
            print #
            print fieldsets[0][1]['fields']
            
            #fieldsets[0][1]['fields'] += ['foo'] 

            fieldsets = (
                  ('Standard info', {
                       #'classes': ('collapse',),
                      'fields': ('filename','authuser','date','datepublished','published')
                  }),
                  ('Validation info', {
                      'classes': ('collapse',),
                      'fields': ( ( 'reportvalidation','datafile'))
                  }),
                    
               )
            
            return fieldsets
                
        #al dar click en unaocion del menu preincipal
        def changelist_view(self, request, extra_context=None):
            print 'FileUser changelist_view'
            extra_context = extra_context or {}
            extra_context['some_var'] = 'This is what I want to show'
            return super(FileUserAdmin, self).changelist_view(request, extra_context=extra_context)

            #alseleccionar un elemento de menu
        def selectlist_view(self, request, extra_context=None):
            print 'FileUser selectlist_view'
            temp_list_display_links = self.list_display_links
            self.list_display_links = (None, )
            response = self.changelist_view(request, extra_context)
            self.list_display_links = temp_list_display_links
            return response

        #al seleccionar un elemento de change_list_results.html
        def change_view(self, request, object_id, extra_context=None):
            print extra_context
            print object_id
            fileuser = FileUser.objects.get(id__exact=object_id)
            print fileuser.filename
            objModel=DataFileTemp.objects.get(filename__exact=fileuser.filename)
       

    
            custom_admin_formsets = {}
            custom_admin_formsets['contentmaintitlepublicationtext']= "Publication"
            custom_admin_formsets['formrowpublicationtext']= "Publication info"
            
            custom_admin_formsets['contentmaintitledatafiletext']= "File"
            custom_admin_formsets['formrowdatafiletext']= "File info"
 
            custom_admin_formfields = {}
            custom_admin_formfields_foreignkey = {}

          
            for f in DataFileTemp._meta.fields:
                #print f.name
                if f.get_internal_type() == 'ForeignKey':
                    field_name_obj = getattr(objModel, f.name)
                    for f2 in field_name_obj._meta.fields:
                        #print f2.name
                        field_name_val = getattr(field_name_obj, f2.name)
                        if field_name_val != None:
                            custom_admin_formfields_foreignkey[f2.name.replace('_', ' '),f2.name,''] =field_name_val
                        else:
                            custom_admin_formfields_foreignkey[f2.name.replace('_', ' '),f2.name,''] =""
                        
                    custom_admin_formfields[f.name.replace('_', ' '),f.name,'publication'] = custom_admin_formfields_foreignkey
                    #print custom_admin_formfields
                else:
                    single_field_name_val = getattr(objModel, f.name)
                    #print field_name_val
                    custom_admin_formfields[f.name.replace('_', ' '),f.name,'datafile'] = single_field_name_val

            #print custom_admin_formfields
            contentmaintitle = 1
            formrow = 1
            
            extra = {
                'title': 'Publish file',
                'original':'Property',
                'objModel':objModel,
                'contentmaintitle':contentmaintitle,
                'formrow':formrow,
                "custom_admin_formsets":custom_admin_formsets,
                'custom_admin_formfields':custom_admin_formfields
                
            }
            

            result = super(FileUserAdmin, self).change_view(request, object_id, extra_context=extra)
            print "FileUser change_view"    
            return result
        
        
        actions = ['delete_selected']
        def delete_selected(self, request, queryset):
            if request.POST.get('post'):
                counter = 0
                for obj in queryset:
                    if obj.published != True:
                        objDataFileTemp=DataFileTemp.objects.get(filename__exact=obj.filename)
                        pat=PublArticleTemp.objects.get(id=objDataFileTemp.publication.id)
                        #objDataFileTemp.delete()
                        #pat.delete() 
                        dataFilePropertyTempDataSet=DataFilePropertyTemp.objects.filter(datafiletemp=objDataFileTemp)
                        for dfptds in dataFilePropertyTempDataSet:
                            print dfptds.propertytemp.tag
                            dfpt=DataFilePropertyTemp()
                            dfpt=dfptds
                            dfpt.delete()
           
                        objDataFileTemp.delete()
                        pat.delete() 
                        
                        
                        #pat.delete() 
                        experimentalfilecontempDatafiletempDataSet=ExperimentalfilecontempDatafiletemp.objects.filter(datafiletemp=objDataFileTemp)
                        
                        for efctdf in experimentalfilecontempDatafiletempDataSet:
                            print efctdf.experimentalfilecontemp.tag
                            efctdf.delete()
                        
                        
                        pathslist=Path.objects.all()   
                        path=Path() 
                        for cifdir in pathslist:
                            path = cifdir
                            if os.path.isdir(path.cifs_dir):
                                break
                                            
                        ciffilein =os.path.join(path.cifs_dir_valids, obj.filename)
                        ciffileout = os.path.join(path.cifs_dir,objDataFileTemp.filename)
                        print "archivo a borrar"
                        print ciffileout
                        try:
                            if os.path.isfile(ciffilein):
                                os.remove(ciffilein)                    
                        except Exception as e:
                            raise Http404('%s object no published yet.' % (force_unicode(e)))
                
                        obj.delete()  
                        counter = counter + 1
                        self.message_user(request, "%s file(s) successfully deleted.." % counter  )
                        
                    else:
                        #pass
                        self.message_user(request, ""  )
                        #messages.debug(request, '%s SQL statements were executed.' % count)
                        #messages.info(request, 'Three credits remain in your account.')
                        #messages.success(request, 'Profile details updated.')
                        messages.warning(request, 'The file currently unpublished.')
                        messages.error(request, 'The file was not deleted.')
                    
                    
                    
                    
            else:
                return delete_selected_(self, request, queryset)
        
        delete_selected.short_description = "Delete selected files unpublished"
        
        
        def delete_model(self, request, obj):
            obj.delete()
            
        def get_actions(self, request):
            actions = super(FileUserAdmin, self).get_actions(request)
            try:
               
                #print actions
                if 'delete_selected' in actions:
                    #del actions['delete_selected']
                    #del actions['delete_selected'] #disable
                    pass
            except KeyError:
                pass
            return actions

        def delete_view(self, request, object_id, extra_context=None):
            
            opts = self.model._meta
            app_label = opts.app_label
             
            try:
                obj = self.model._default_manager.get(pk=object_id)
            except self.model.DoesNotExist:
                obj = None
                  
            if not self.has_delete_permission(request, obj):
                raise PermissionDenied
  
            if obj is None:
                raise Http404('%s object with primary key %r does not exist.' % (force_unicode(opts.verbose_name), escape(object_id)))
 
            if obj.published == False:
                raise Http404('can not carry out the operation because the object %s  is unpublished' % (force_unicode(opts.verbose_name)))
            
                       
            
            using = router.db_for_write(self.model)  
 
 
            (deleted_objects, perms_needed, protected) = get_deleted_objects([obj], opts, request.user, self.admin_site, using)
            
       

            #if request.POST is set, the user already confirmed deletion
            if not request.POST:
                print 'not request.POST'
            else:
                print 'request.POST'
                if perms_needed:
                    raise PermissionDenied
                
                dataFileTemp=DataFileTemp.objects.get(filename__exact=obj.filename)

                publication= None
                try: 
                    dataFile=DataFile.objects.get(code__exact = dataFileTemp.code )    
                    publication = dataFile.publication
                except ObjectDoesNotExist as error:
                    print "Message({0}): {1}".format(99, error.message) 
                    dataFile = None                 
                    
                if dataFile is None:
                    raise Http404('%s object no published yet.' % (force_unicode(dataFileTemp.filename)))
  
                dataFilePropertyQuerySet = None
                try: 
                    dataFilePropertyQuerySet=DataFileProperty.objects.filter(datafile = dataFile )    
                except ObjectDoesNotExist as error:
                    print "Message({0}): {1}".format(99, error.message) 
                    dataFilePropertyQuerySet = None        
                    
                if dataFilePropertyQuerySet is None:
                    raise Http404('%s object no published yet.' % (force_unicode(dataFile.code)))

                for dfp in dataFilePropertyQuerySet:
                    dataFilePropertyObj = DataFileProperty()
                    dataFilePropertyObj = dfp
                    
                    print "dataFilePropertyObj.delete()"
                    print dataFilePropertyObj.datafile.filename
                    dataFilePropertyObj.delete()
 
                pathslist=Path.objects.all()   
                path=Path() 
                for cifdir in pathslist:
                    path = cifdir
                    if os.path.isdir(path.cifs_dir):
                        break
                                    
                ciffilein =os.path.join(path.cifs_dir_valids, obj.filename)
                ciffileout = os.path.join(path.cifs_dir,dataFile.filename)
                print "archivo a borrar"
                print ciffileout
                try:
                    if os.path.isfile(ciffileout):
                        os.remove(ciffileout)                    
                except Exception as e:
                    raise Http404('%s object no published yet.' % (force_unicode(e)))


                dataFile.delete() 
                publication.delete()
      
                obj_display = str(obj)
                #self.delete_model(request, obj)
                obj.published = False
                obj.save()  
 
                  
                self.log_deletion(request, obj, obj_display)
                self.message_user(request, ('The %(name)s "%(obj)s" was deleted successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj_display)})
             
                if not self.has_change_permission(request, None):
                    return HttpResponseRedirect(reverse('admin:index',
                                                        current_app=self.admin_site.name))
                return HttpResponseRedirect(reverse('admin:%s_%s_changelist' %
                                            (opts.app_label, opts.module_name),
                                            current_app=self.admin_site.name))
                
            
            object_name = force_unicode(opts.verbose_name)
            if perms_needed or protected:
                title = "Cannot delete %(name)s" % {"name": object_name}
            else:
                title = "Are you sure?"
            
            context = {
                  "title": title,
                  "object_name": object_name,
                  "object": obj,
                  "deleted_objects": deleted_objects,
                  "perms_lacking": perms_needed,
                  "opts": opts,
                  "root_path": self.admin_site,
                  "app_label": app_label,
              }
            
            context.update(extra_context or {})
            
            return render_to_response(self.delete_confirmation_template or [
              "admin/%s/%s/delete_confirmation.html" % (app_label, opts.object_name.lower()),
              "admin/%s/delete_confirmation.html" % app_label,
              "admin/delete_confirmation.html"
              ], context, context_instance=template.RequestContext(request))
            
            #todo lo anterior + self.delete_model(request, obj)
            #super(FileUserAdmin, self).delete_view(request, obj, extra_context)
 
        def save_model(self, request, obj, form, change):
            try:

                #print request.POST
                message_bit = "" 
                #print form.changed_data # list name of field was changed
                #print change #True or False
                
               
                if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue') and not request.POST.has_key('_save'):
                    print "pass"
                elif  request.POST.has_key('_addanother'): 
                    print request.POST.get('_addanother',False)
                elif request.POST.has_key('_continue'): 
                    print request.POST.get('_continue',False)
                elif request.POST.has_key('_save'):
                    print request.POST.get('_save',False)
                    if request.POST.get('published',False)  != False:
                        try:
                            
          
                            obj.datepublished = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                            dataFileTemp=DataFileTemp.objects.get(filename__exact=obj.filename)
             
                            experimentalfilecontempDatafiletempQuerySet = ExperimentalfilecontempDatafiletemp.objects.filter(datafiletemp=dataFileTemp)
                            experimentalParCond = ExperimentalParCond()
                            for efct in experimentalfilecontempDatafiletempQuerySet:
                                try:
                                    experimentalParCond = ExperimentalParCond.objects.get(tag__exact=efct.experimentalfilecontemp.tag)
                                    #experimentalParCond= None
                                except ObjectDoesNotExist as error:
                                    print "Error({0}): {1}".format(99, error.message) 
                                     
                                    experimentalParCond.tag = efct.experimentalfilecontemp.tag
                                    experimentalParCond.name =  efct.experimentalfilecontemp.name
                                    experimentalParCond.description =  efct.experimentalfilecontemp.description
                                    experimentalParCond.units =  efct.experimentalfilecontemp.units
                                    experimentalParCond.units_detail =  efct.experimentalfilecontemp.units_detail
                                    experimentalParCond.save()
    
                            publicArticle=PublArticle()                      
                            publicArticle.title =  dataFileTemp.publication.title
                            publicArticle.authors =  dataFileTemp.publication.authors
                            publicArticle.journal =  dataFileTemp.publication.journal
                            publicArticle.year =  dataFileTemp.publication.year
                            publicArticle.volume =  dataFileTemp.publication.volume
                            publicArticle.issue =  dataFileTemp.publication.issue
                            publicArticle.first_page =  dataFileTemp.publication.first_page
                            publicArticle.last_page =  dataFileTemp.publication.last_page
                            publicArticle.reference =  dataFileTemp.publication.reference
                            publicArticle.pages_number =  dataFileTemp.publication.pages_number
                            publicArticle.save()
                            
          
                            
                            dataFile=DataFile()
                            top = DataFile.objects.order_by('-code')[0]
                            code = top.code + 1
                            dataFile.code = code 
                            dataFile.filename = str(code) + ".mpod"
                            dataFile.cod_code = dataFileTemp.cod_code
                            dataFile.phase_generic =  dataFileTemp.phase_generic
                            dataFile.phase_name =  dataFileTemp.phase_name
                            dataFile.chemical_formula = dataFileTemp.chemical_formula
                            dataFile.publication = publicArticle
                  
                            dataFile.save()
              
                            obj.datafile =dataFile
                            
                            dataFileTemp.code = dataFile.code
                            dataFileTemp.save()
                     
                            
                                                        
                            dataFilePropertyTemp = DataFilePropertyTemp.objects.get(datafiletemp = dataFileTemp)
                            dataFileProperty=DataFileProperty()
                            property=Property()
                            
                            try:
                                property = Property.objects.get(tag__exact=dataFilePropertyTemp.propertytemp.tag)
                            except ObjectDoesNotExist as error:
                                #print "Error({0}): {1}".format(99, error.message) 
                                 
                                property.tag = dataFilePropertyTemp.propertytemp.tag
                                property.name =  dataFilePropertyTemp.propertytemp.name
                                property.description =  dataFilePropertyTemp.propertytemp.description
                                property.tensor_dimensions =  dataFilePropertyTemp.propertytemp.tensor_dimensions
                                property.units =  dataFilePropertyTemp.propertytemp.units
                                property.units_detail =  dataFilePropertyTemp.propertytemp.units_detail
                                property.save()
    
                            dataFileProperty.property=property
                            dataFileProperty.datafile = dataFile
                            dataFileProperty.save()
   
                            
                            obj.save()  
                          
                            
                            pathslist=Path.objects.all()      
                            pathexist = 0
                            
                            filepath = ""
                            path=Path() 
                            for cifdir in pathslist:
                                path = cifdir
                                if os.path.isdir(path.cifs_dir):
                                    break
                            
                            ciffilein =os.path.join(path.cifs_dir_valids, obj.filename)
                            ciffileout = os.path.join(path.cifs_dir,dataFile.filename)
                            print dataFile.filename
            
                            #line.replace("data_" + obj.filename, "data_" +dataFile.code ), end='')
                            datacode = "data_"+ obj.filename.replace('.mpod', ' ')
                            newdatacode =   "data_" + str(dataFile.code)
                            print datacode
                            print newdatacode
           
                            with open(ciffilein) as infile, open(ciffileout, 'w') as outfile:
                                for line in infile:
                                    l = line.rstrip('\n')
                                    if l in datacode:
                                        print line
                                        line = newdatacode + '\n'
                                        outfile.write(line)
                                    else:                                        
                                        outfile.write(line)
                            
                            
                            messageCategoryDetailQuerySet1=MessageCategoryDetail.objects.filter(messagecategory=MessageCategory.objects.get(pk=2))#2 for user notification
                       
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
                                                                                    'code':  dataFile.code,
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
                            
    
                        except ObjectDoesNotExist as error:
                                    #print "Error({0}): {1}".format(99, error.message)  
                                    messages.add_message(request, messages.ERROR, "Error %s " % error.message)
                    else:
                          
                        opts = self.model._meta
                        obj_display = force_unicode(obj)
                        """   
                        self.log_change(request, obj, message)
                        self.log_addition(request, obj)
                        self.log_deletion(request, obj, obj_display)
                        """
                        #self.message_user(request, ('The %(name)s "%(obj)s" was changed  successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj_display)})
                            
                      
             
             
                            
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



class CatalogPropertyAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(CatalogProperty, CatalogPropertyAdmin)

class TypeAdmin(admin.ModelAdmin):
    list_display =('get_description','get_name',)  
    #list_display =('title', 'authors', 'journal','year','volume','issue','first_page','last_page','reference','pages_number')
    search_fields = ['name', 'description', ]
    list_filter = ('description',)
          
          
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
    list_display =('name','description','get_catalogproperty_description',)  
    ordering = ('catalogproperty__description',) 
    search_fields = ['name', 'description', ]
    list_filter = ('catalogproperty__description',)

        
    def get_catalogproperty_description(self, obj):
        try:
            return  u'%s' % (obj.catalogproperty.description)               
        except ObjectDoesNotExist as error:
            return ""

    get_catalogproperty_description.short_description = 'Property'
    get_catalogproperty_description.allow_tags=True 
    
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
   
   
 
    
        
    def add_view(self,request,extra_content=None):
        print 'PuntualGroupNames_add_view'
        return super(PuntualGroupNamesAdmin,self).add_view(request)
    
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
     

    
admin.site.register(PuntualGroupNames, PuntualGroupNamesAdmin)

 
        

class PuntualGroupGroupsAdmin(admin.ModelAdmin):
   
   
    form= PuntualGroupGroupsAdminForm
    fieldsets = (
        ('Point Groups and Groups', {
            'fields': ('puntualgroupnames','pointgroups',)
        }),

    )
    
    list_display =('catalogpointgroup','puntualgroupnames',)  
    

        
            
    #fields = ['puntualgroupnames','catalogpointgroup','catalogpointgroup1']
    idList=[]  
    nameList=[]
    def get_puntualgroupnamesgroup_by(self, obj):
        try:
            puntualgroupnamesQuerySet=PuntualGroupGroups.objects.filter(puntualgroupnames=obj.puntualgroupnames).values('puntualgroupnames').annotate(total=Count('puntualgroupnames'))
            name = ""
            for d in puntualgroupnamesQuerySet:
                if d['puntualgroupnames'] != 21:          
                    objPuntualgroupnames=PuntualGroupNames.objects.get(id__exact=d['puntualgroupnames']) 
                    if int(d['puntualgroupnames']) not in  self.idList:
                        self.idList.append(int(d['puntualgroupnames']))
                        name =objPuntualgroupnames.name
                    else:
                        #print "esta " + str(int(d['puntualgroupnames']))
                        pass
            return name

        except ObjectDoesNotExist as error:
            return ""
    
    
    
 
    """
    def change_view(self, request, object_id, form_url='', extra_context=None):
        print 'PuntualGroupGroupsAdmin_change_view'
        extra_context = extra_context or {}

        return admin.ModelAdmin.change_view(self, request, object_id, form_url=form_url, extra_context=extra_context)
    """
 
    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        urls = super(PuntualGroupGroupsAdmin,self).get_urls()

        info = self.model._meta.app_label, self.model._meta.module_name
    
        n='%s_%s_detail' % info

        """
        my_urls = [ 
                            #url(r'^(.+)/detail/(?P<tdpid>\d+)$',wrap(self.properties_typedataproperty_detail_view), name=('%s_%s_detail' % info)), 
                            url(r'^(?P<id>\d+)/detail/(?P<csid>\d+)$',wrap(self.properties_typedataproperty_detail_view), name=('%s_%s_detail' % info)), 
                            ]
        
        """ 
        print  urls
        #return  my_urls + urls
        return  urls

admin.site.register(PuntualGroupGroups, PuntualGroupGroupsAdmin)



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
 
    
    list_display =('type','get_crystalsystem','dataproperty', )   
 
    form = TypeDataPropertyAdminForm       
    #fields = ['puntualgroupnames','catalogpointgroup','catalogpointgroup1']
    fieldsets = (
        ('Property information', {
            'fields': ('catalogproperty','type','catalogcrystalsystem',)
        }),
        ('Data Property Detail', {
            'fields': ('populate','dataproperty','quantity','coefficients','catalogpointgroup','puntualgroupnames','axis',)
        }),
            
    )
 
    
    def get_crystalsystem(self,obj):
        ids=CatalogProperty.objects.filter(id=obj.type.catalogproperty.id).values_list('id', flat=True) 
        catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty_id__in=ids).values_list('description',flat=True)
        
        result = ""
        for description in catalogcrystalsystemQuerySet:
            if result =="":
                result=   str(description)
            else:
                result= result + ", " + str(description)
 
        return   result
    
    #print fieldsets[3][1]['fields']
    
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
                    """
                    if self.puntualgroupselected_name == '':
                        self.puntualgroupselected_name=cpg.name
                    """
               
                    puntualGroupList.append(cpg)                       
    
                                                            
        propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected).values('puntualgroupnames').annotate(total=Count('puntualgroupnames'))
         
        for d in propertyDetail:
            if d['puntualgroupnames'] != 21:   
                #print d['puntualgroupnames']              
                objPuntualgroupnames=PuntualGroupNames.objects.filter(id__exact=d['puntualgroupnames']) 
                objPuntualGroupGroups = PuntualGroupGroups.objects.filter(puntualgroupnames=objPuntualgroupnames)    
                for obj in objPuntualGroupGroups:
                    pgg=PuntualGroupGroups()
                    pgg=obj
                    #print pgg.catalogpointgroup.name
                    """
                    if self.puntualgroupselected_name == '':
                        self.puntualgroupselected_name=pgg.catalogpointgroup.name
                    """
             
                    puntualGroupList.append(pgg.catalogpointgroup)
                    
        return puntualGroupList
                    
    def setAxis(self,objTypeSelected,objCatalogCrystalSystemSelected):
        propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=objCatalogCrystalSystemSelected).values('catalogaxis').annotate(total=Count('catalogaxis'))
        axisList = []
        for d in propertyDetail:  
            if d['catalogaxis'] != 4:       
                #print d['catalogaxis']  
                objCatalogAxis=CatalogAxis.objects.filter(id=d['catalogaxis'] )
                for obj in objCatalogAxis:
                    ca=CatalogAxis()
                    ca=obj
                    #print ca.name
                    axisList.append(ca)
                    
        return  axisList   
    
    
    def detail(self,  id):
        catalogpropertydetailList = []
        try:    
            typedataproperty=TypeDataProperty.objects.get(id= id) 
            CatalogProperty.objects.filter(id= typedataproperty.type.catalogproperty.id)
            catalogcrystalsystemQuerySet=CatalogCrystalSystem.objects.filter(catalogproperty=typedataproperty.type.catalogproperty)
            
            print 'id_catalogcrystalsystem ' + str(catalogcrystalsystemQuerySet[0].id)

            catalogpointgroupList=self.setPointGroup(typedataproperty.type,catalogcrystalsystemQuerySet[0])
            print catalogpointgroupList

            catalogpropertydetailList=[]
            return   catalogpropertydetailList
 
        except ObjectDoesNotExist as error:
            print "Message({0}): {1}".format(99, error.message)   
            return  error.message
        
    def save_model(self, request, obj, form, change):
        print 'PuntualGroupNames_save_model'
        print request.POST
        #print obj.name
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
            
             
            if  request.POST.has_key('populate'):
                if request.POST.get('dataproperty',False) != False:
                    datapropertytag=Property.objects.filter(id=request.POST.get('dataproperty',False) )
                    print datapropertytag
                    catalogpropertydetail = CatalogPropertyDetail.objects.filter(dataproperty=datapropertytag).values('dataproperty').annotate(total=Count('dataproperty'))

                    print str(catalogpropertydetail[0]['total'])
                    print str(catalogpropertydetail[0]['dataproperty'])

                    print  request.POST.has_key('populate')
                    print  request.POST.has_key('quantity')
                    #self.message_user(request, "%s file(s) successfully saved.." % counter  )
                        
            else:
                        #pass
                #self.message_user(request, ""  )
                #messages.debug(request, '%s SQL statements were executed.' % count)
                #messages.info(request, 'Three credits remain in your account.')
                #messages.success(request, 'Profile details updated.')
                messages.set_level(request, messages.WARNING)
                messages.warning(request, 'The process was not done, mark the populate field to perform the process.')
                #messages.set_level(request, messages.ERROR)
                #messages.error(request, 'The file was not populated.')
                
                
            
      
            
            
            #obj.save()
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}

        extra_context = {
                'original':'Type and Data Property',
                'object_id':object_id
            }
 
        print 'id_typedataproperty ' + str(object_id)
 
        return admin.ModelAdmin.change_view(self, request, object_id, form_url=form_url, extra_context=extra_context)
      
 
    def properties_typedataproperty_detail_view(self, request, id,  csid):
        error = ""
        html ="<table id='result_list'>"
        axisdic = []
        try:
            
            id_puntualgroupnames  = request.POST.get('id_puntualgroupnames', False)
            id_catalogproperty  = request.POST.get('id_catalogproperty', False)
            id_axis  = request.POST.get('id_axis', False)
            id_type  = request.POST.get('id_type', False)
            id_catalogpointgroup  = request.POST.get('id_catalogpointgroup', False)
            id_puntualgroupnames  = request.POST.get('id_puntualgroupnames', False)
            todo  = request.POST.get('todo', False)
            

            
            if  todo == False:
                pass
            else:
                typedataproperty=TypeDataProperty.objects.get(id= id) 
                if  todo == "crystalsystemchange":
                    typeObj=Type.objects.get(id=id_type)
                    catalogpropertyObj=CatalogProperty.objects.get(id= id_catalogproperty)
                    catalogcrystalsystemObj=CatalogCrystalSystem.objects.get(id= csid)
                    catalogaxisObj=CatalogAxis.objects.get(id=id_axis)
                    catalogpointgroupObj=CatalogPointGroup.objects.get(id=id_catalogpointgroup)
                    puntualgroupnamesObj=PuntualGroupNames.objects.get(id=id_puntualgroupnames)
                    
                    print "id_type " + str(id_type)
                    print "id_crystalsystemchange " + str(csid)
                    
                    """
                    axisid=CatalogPropertyDetail.objects.filter(type=typedataproperty.type,crystalsystem=catalogcrystalsystemObj).values_list('catalogaxis_id', flat=True)#.exclude(catalogaxis__id=4)
                    axisQuerySet=CatalogAxis.objects.filter(id__in=axisid) 
                    
                    axisinitial = 4
 
                    if axisQuerySet:
                        axistostring = ""
                        #axistostring =  axistostring + "<option value=''>---------</option>"
                        for axis in axisQuerySet:
                            if axis.id == axisQuerySet[0].id:
                                axistostring = axistostring +  "<option value='" +str(axis.id) + "' selected='selected'>"+axis.name+"</option>"
                            else:
                                axistostring = axistostring +  "<option value='"+str(axis.id) +"' >"+axis.name+"</option>"
                    else:
                        axisObj= CatalogAxis.objects.get(id=axisinitial)
                        axistostring = axistostring +  "<option value='" +str(axisObj.id) + "' selected='selected'>"+axisObj.name+"</option>"
                            
                    
                     
                    #print "id_axis " + str(axisQuerySet[0].id)
       
                   
                    catalogpointgroupids=CatalogPropertyDetail.objects.filter(type=typedataproperty.type,crystalsystem=catalogcrystalsystemObj,catalogaxis= axisQuerySet[0]).values_list('catalogpointgroup_id', flat=True)#.exclude(catalogpointgroup__id=45)
                    catalogpointgroupQuerySet=CatalogPointGroup.objects.filter(id__in=catalogpointgroupids)
                     
                    catalogpointgroupinitial = 45
                    if  catalogpointgroupQuerySet:
                        catalogpointgrouptostring = ""
                        #catalogpointgrouptostring =  catalogpointgrouptostring + "<option value=''>---------</option>"
                        for catalogpointgroup in catalogpointgroupQuerySet:
                            if catalogpointgroup.id == catalogpointgroupQuerySet[0].id:
                                catalogpointgrouptostring = catalogpointgrouptostring +  "<option value='" +str(catalogpointgroup.id) + "' selected='selected'>"+catalogpointgroup.name+"</option>"
                            else:
                                catalogpointgrouptostring = catalogpointgrouptostring +  "<option value='"+str(catalogpointgroup.id) +"' >"+catalogpointgroup.name+"</option>"
                    else:
                            catalogpointgroupObj= CatalogPointGroup.objects.get(id=catalogpointgroupinitial)
                            catalogpointgrouptostring = catalogpointgrouptostring +  "<option value='" +str(catalogpointgroup.id) + "' selected='selected'>"+catalogpointgroup.name+"</option>"
                            
                            
                    #print "id_catalogpointgroup " + str(catalogpointgroupQuerySet[0].id)
                    
                    
                        
                    puntualgroupnamesids=CatalogPropertyDetail.objects.filter(type=typedataproperty.type,crystalsystem=catalogcrystalsystemObj,catalogaxis= axisQuerySet[0],catalogpointgroup=catalogpointgroupQuerySet[0]).values_list('puntualgroupnames_id', flat=True)
                    puntualgroupnamesQuerySet=PuntualGroupNames.objects.filter(id__in=puntualgroupnamesids)
                    puntualgroupnamesinitial = 21
                    if puntualgroupnamesQuerySet:
                        puntualgroupnamestostring = ""
                        for puntualgroupnames in puntualgroupnamesQuerySet:
                            if puntualgroupnames.id == puntualgroupnamesQuerySet[0].id:
                                puntualgroupnamestostring = puntualgroupnamestostring +  "<option value='" +str(puntualgroupnames.id) + "' selected='selected'>"+puntualgroupnames.name+"</option>"
                            else:
                                puntualgroupnamestostring = puntualgroupnamestostring +  "<option value='"+str(puntualgroupnames.id) +"' >"+puntualgroupnames.name+"</option>"
                    else:
                        puntualgroupnamesObj= PuntualGroupNames.objects.get(id=puntualgroupnamesinitial)
                        puntualgroupnamestostring = puntualgroupnamestostring +  "<option value='" +str(puntualgroupnamesObj.id) + "' selected='selected'>"+puntualgroupnamesObj.name+"</option>"      
                    
                    
                    
                    #print "id_puntualgroupnames " + str(puntualgroupnamesQuerySet[0].id)
                        
                    catalogpropertydetailQuerySet= CatalogPropertyDetail.objects.filter(type=typeObj,crystalsystem=catalogcrystalsystemObj,catalogaxis=axisQuerySet[0],catalogpointgroup=catalogpointgroupQuerySet[0],puntualgroupnames=puntualgroupnamesQuerySet[0]).order_by('name')
 
                    for i,catalogpropertydetail in enumerate(catalogpropertydetailQuerySet):
                        
                        if i % 2 == 0:
                            html = html +"<tr class='row"+ str(1)+"'><td class='action-checkbox'>" + catalogpropertydetail.name + "</td/></tr>"
                        else:
                            html = html +"<tr class='row"+ str(2)+"'><td class='action-checkbox'>" + catalogpropertydetail.name + "</td/></tr>"
 
                                   
                    html = html +"</table>"
                """
                    
        
        except ObjectDoesNotExist as error:
            print "Message({0}): {1}".format(99, error.message)   
            return  error.message
        
        
        
        data = {
                'error':error,
                'html':html,
                #'axistostring':axistostring,   
                #'catalogpointgrouptostring':catalogpointgrouptostring,
                #'puntualgroupnamestostring':puntualgroupnamestostring
            }
        print data
            
        return  HttpResponse(json.dumps(data), content_type="application/json")   


 

 
    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        urls = super(TypeDataPropertyAdmin,self).get_urls()

        info = self.model._meta.app_label, self.model._meta.module_name
    
        n='%s_%s_detail' % info


        my_urls = [ 
                            #url(r'^(.+)/detail/(?P<tdpid>\d+)$',wrap(self.properties_typedataproperty_detail_view), name=('%s_%s_detail' % info)), 
                            url(r'^(?P<id>\d+)/detail/(?P<csid>\d+)$',wrap(self.properties_typedataproperty_detail_view), name=('%s_%s_detail' % info)), 
                            ]
        
         
        #print  my_urls + urls
        return  my_urls + urls
    
      
    
    def account_actions(self, obj):
        
            #'<a class="button" href="{}">Deposit</a>&nbsp;'  '<a class="button" href="{}">Withdraw</a>', reverse('admin:account-deposit', args=[obj.pk]), reverse('admin:account-withdraw', args=[obj.pk]);
        url= u'<a class="button" href="%s">%s</a>' % (reverse('admin:Properties_typedataproperty_detail', args=[obj.pk,obj.pk]),"ejemplo")  
        return url
        
        
    account_actions.short_description = 'Account Actions'
    account_actions.allow_tags = True
    
    
admin.site.register(TypeDataProperty, TypeDataPropertyAdmin)


    



