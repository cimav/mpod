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
#from  data import PropertyMaster
from data.JQueryCode import *
from data.UtilParserFile import *
from django.contrib.admin.templatetags.admin_static import static
from data.ExtractDataFormFieldsUtil import *


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


class FileUserAdminv2(admin.ModelAdmin):
        list_display =('filename','date','user_name','publish','datafile_code')  
        search_fields = ['filename', 'datafile__code',]

        form=FileUserAdminFormv2
       
        
        readonly_fields=['filename','authuser','date','user_name','datepublished',]
 
 
       
        def get_fieldsets(self, request, obj=None):
            fieldsets = super(FileUserAdminv2, self).get_fieldsets(request, obj)
            
            hd= 'File'
            fieldsets=((hd, {'classes': ('collapse',),'fields': []}),)
            
            fieldsets[0][1]['fields'] += ['filename'] 
            fieldsets[0][1]['fields'] += ['filenametemp'] 
            fieldsets[0][1]['fields'] += ['datafile'] 
            
            fieldsets[0][1]['fields'] += ['authuser'] 
            fieldsets[0][1]['fields'] += ['date'] 
            
            if obj.publish:
                fieldsets[0][1]['fields'] += ['datepublished'] 
                fieldsets[0][1]['fields'] += ['filenamepublished'] 
            
            fieldsets[0][1]['fields'] += ['publish'] 
            fieldsets[0][1]['fields'] += ['reportvalidation'] 
 
            fieldsets[0][1]['fields'] += ['js'] 
            
            
            edff = None
            if not 'extractdataformfields' in request.session or not request.session['extractdataformfields' ]: 
                fromdatabase = False
                customfile = False
                loadtodatabase = False
                fds2 = []    
                fds2.append(obj.filename)
                extractdataformfields= ExtractDataFormFields()
                extractdataformfields.debug = False
                extractdataformfields.processData(loadtodatabase,fds2,customfile)
                request.session['extractdataformfields']= extractdataformfields
            else:
                extractdataformfields = request.session['extractdataformfields']
            
            
            fieldsetsupated = fieldsets  + extractdataformfields.customForm.fieldsets
            return fieldsetsupated
        
        
        def updatecoefficients(self, request,fileuserid):
            response_data = {}
            if request.method == 'POST':
               
                
                POST = request.POST.copy()
                todo=POST.pop('todo')[0]
                dimension= POST.pop('dimension')[0]   
 
                #objDataFilePropertyTemp = DataFilePropertyTemp.objects.get(datafiletemp_id=int(datadfiletemp_id), propertytemp_id =int(propertytemp_id) )
                fileuserutil = None
                if not 'extractdataformfields' in request.session: 
                    response_data['extractdataformfields'] =''
                else:
                    extractdataformfields= request.session['extractdataformfields']
                    for k,val in POST.iterlists():
                        
                        line = (k.split())
                        nlines = (line[0]).split('_')
                        #print str(nlines[0])
                        #print val[0]
                        change,error=extractdataformfields.fileuserutil.findAndUpdateLine(str(nlines[0]),val,str(dimension))
                             
                   
                    for l in extractdataformfields.fileuserutil.lines:
                        print l
                        #pass
                    
                                
                    request.session['extractdataformfields']= extractdataformfields
                          
                #response_data['result'] = 'Property updated: ' + objDataFilePropertyTemp.propertytemp.name  +' save for commit;'
 
            return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
        

        def get_urls(self):
            def wrap(view):
                def wrapper(*args, **kwargs):
                    return self.admin_site.admin_view(view)(*args, **kwargs)
                wrapper.model_admin = self
                return update_wrapper(wrapper, view)
    
            urls = super(FileUserAdminv2,self).get_urls()
    
            info = self.model._meta.app_label, self.model._meta.module_name
            property='%s_%s_property' % info
            experimental='%s_%s_experimental' % info
            updatecoefficients='%s_%s_updatecoefficients' % info
            updatecondition='%s_%s_updatecondition' % info
            
            
          
  
            my_urls = [
                #url(r'^(.+)/property/$', wrap(self.property), name=property),
                url(r'^(.+)/updatecoefficients/$', wrap(self.updatecoefficients), name=updatecoefficients),
                #url(r'^(.+)/experimental/$', wrap(self.experimental), name=experimental),
                #url(r'^(.+)/updatecondition/$', wrap(self.updatecondition), name=updatecondition),
 
               
            ]
            #print my_urls
 
            return my_urls + urls   


        def delete_model_relations(self,datafile,cifftodelete, ext):
            err = None
  
            try:
                if datafile:
                    #obj = FileUser.objects.get(filename='ywrtaw4=nzcthbjkasfbcxi.mpod')
                    epcdf = None
                    dfp = None
                    params = {}
                    if isinstance(datafile, DataFile):
                        params[ 'datafile_id'] = datafile.code
                        epcdf=ext.existObjectInDB(ExperimentalParCond_DataFile(), params, 'exact')
                        dfp=ext.existObjectInDB(DataFileProperty(), params, 'exact')
                    else:
                        params[ 'datafiletemp_id'] = datafile.id
                        epcdf=ext.existObjectInDB(ExperimentalParCondTemp_DataFileTemp(), params, 'exact')
                        dfp=ext.existObjectInDB(DataFilePropertyTemp(), params, 'exact')
 
                    if epcdf:
                        epctdftlist = []
                        if isinstance(epcdf, ExperimentalParCond_DataFile):
                            epctdftlist.append(epcdf)
                        elif isinstance(epcdf, ExperimentalParCondTemp_DataFileTemp):
                            epctdftlist.append(epcdf)
                        elif isinstance(epcdf, QuerySet):
                            epctdftlist = epcdf
                    
                        for ec in epctdftlist:
                            print ec.id
                            ec.delete()
             
                    #params = {}
                    #params[ 'datafile_id'] = obj.datafile.code
                    """if isinstance(datafile, DataFile):
                        dfp=ext.existObjectInDB(DataFileProperty(), params, 'exact')
                    else:
                        dfp=ext.existObjectInDB(DataFilePropertyTemp(), params, 'exact')
                    """
                    
                    if dfp:
                        listdfpt = []
                        if isinstance(dfp, DataFileProperty):
                            listdfpt.append(dfp)
                        elif  isinstance(dfp, DataFilePropertyTemp):
                            listdfpt.append(dfp)
                        elif isinstance(dfp, QuerySet):
                            listdfpt = dfp
                            
                            
                        for df in listdfpt:
                            print 'datafileproperty_id ', df.id
                            listpvt = []
                            pvt = None
                            dfpd = None
                            params = {}
                            if isinstance(df, DataFileProperty):
                                params[ 'datafileproperty_id'] = df.id
                                pvt=ext.existObjectInDB(PropertyValues(), params, 'exact')
                                dfpd=ext.existObjectInDB(PropertyConditionDetail(), params, 'exact')
                            elif isinstance(dfp, DataFilePropertyTemp):
                                params[ 'datafilepropertytemp_id'] = df.id
                                pvt=ext.existObjectInDB(PropertyValuesTemp(), params, 'exact')
                                params = {}
                                params[ 'datafileproperty_id'] = df.id
                                dfpd=ext.existObjectInDB(PropertyConditionDetailTemp(), params, 'exact')
 
                            if pvt:
                                if isinstance(pvt, PropertyValues):
                                    listpvt.append(pvt)
                                elif isinstance(pvt, PropertyValuesTemp):
                                    listpvt.append(pvt)
                                elif isinstance(pvt, QuerySet):
                                    listpvt = pvt
                                    
                                for ec in listpvt:
                                    print 'PropertyValues  ', ec.id
                                    ec.delete()
                                
                            
                            
                            if dfpd:
                                listdfpt = []
                                if isinstance(dfpd, PropertyConditionDetail):
                                    listdfpt.append(dfpd)
                                elif isinstance(dfp, PropertyConditionDetailTemp):
                                    listdfpt.append(dfpd)
                                elif isinstance(dfp, QuerySet):
                                    listdfpt = dfpd
                                    
                                    
                                for dfd in listdfpt:
                                    print dfd.id
                                    dfd.delete()
                                    
                            df.delete()
                         
                    datafile.delete()       
                    #obj.delete()   
                    if os.path.isfile(cifftodelete):
                        os.remove(cifftodelete)   
                        print cifftodelete
                          
 
            except Exception  as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                err= {}
                err['file']=fname
                err['line']=exc_tb.tb_lineno
                err['error']="Error: {1}".format( e.message, e.args) 
                error = err
                return err
            
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
                
 
 
                paths = None
                pathslist=Path.objects.all()      
                for path in pathslist:
                    if os.path.isdir(path.cifs_dir): 
                        paths = Path()
                        paths = path
                        break
                            
                #err = self.delete_model( obj)
                #obj = FileUser.objects.get(filename='zaabykcbqvourbmhd.mpod')
                ciffordelete1 = os.path.join(paths.cifs_dir,obj.datafile.filename)
                ext =  Extractor()         
                err = self.delete_model_relations(obj.datafile,ciffordelete1, ext)
                if  isinstance(err, type(None)):
                    pass
                else:
                    messages.add_message(request, messages.ERROR, "ERROR %s " % err)
                 
                    
                params = {}
                params[ 'filename'] = obj.filename
                datafiletemp= ext.existObjectInDB(DataFileTemp(), params, 'exact')
                ciffordelete2 = os.path.join(paths.cifs_dir_valids,obj.filename)
                err = self.delete_model_relations(datafiletemp, ciffordelete2, ext)
        
                if  isinstance(err, type(None)):
                    pass
                else:
                    messages.add_message(request, messages.ERROR, "ERROR %s " % err)
                    
                    
                obj.delete() 
                
    
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
         
         
         
        def has_add_permission(self, request):
            return False
    
        def change_view(self, request, object_id, form_url='', extra_context=None):
            extra_context = extra_context or {}
            
            
            
            #fileuserutil =  FileUserUtil()
            fileUser=FileUser.objects.get(id=object_id)
            #fileuserutil.setFile(fileUser)
            fromdatabase = False
            customfile = False
            loadtodatabase = False
            
            print 'session'
            print 'extractdataformfields' in request.session
            if not 'extractdataformfields' in request.session: 
                fds2 = []    
                fds2.append(fileUser.filename)
                extractdataformfields= ExtractDataFormFields()
                #extractdataformfields.debug = False
                extractdataformfields.processData(loadtodatabase,fds2,customfile)
                request.session['extractdataformfields']= extractdataformfields
            else:
                if request.POST:
                    extractdataformfields = request.session['extractdataformfields']
                else:
                    del request.session['extractdataformfields']
                    fds2 = []    
                    fds2.append(fileUser.filename)
                    extractdataformfields= ExtractDataFormFields()
                    #extractdataformfields.debug = False
                    extractdataformfields.processData(loadtodatabase,fds2,customfile)
                    if  extractdataformfields.fileuserutil.fileexist:
                        request.session['extractdataformfields']= extractdataformfields
                    else:
                        fileUser.delete()
                        fileUser = None
                    
            if fileUser:
                url = 'coefficientsandconditions.js'
                customMedia= forms.Media(js=[static('admin/js/%s' % url)])
                form_class = self.get_form(request, fileUser)
                form = form_class(process=False,instance=fileUser)  
                
                
                adminForm = helpers.AdminForm(form,  self.get_fieldsets(request, fileUser),
                self.get_prepopulated_fields(request, fileUser),
                self.get_readonly_fields(request, fileUser),
                model_admin=self)
     
                media = self.media + adminForm.media + customMedia
                
                """
                info = self.model._meta.app_label, self.model._meta.module_name
                property='%s_%s_property' % info
                experimental='%s_%s_experimental' % info
                updatecoefficients='%s_%s_updatecoefficients' % info
                updatecondition='%s_%s_updatecondition' % info
                """
      
                extra_context = {
                    'original':'File User',
                    'media': media,
                     
                }
 
 
            return admin.ModelAdmin.change_view(self, request, object_id, form_url=form_url, extra_context=extra_context)
        
        
        def updateLinesOnSession(self,POST,extractdataformfields):
            change = False
            error = None
 
            
            categoryTagName2 = list(CategoryTag.objects.filter(id=2).values_list('name',flat=True))[0]#properties
            categoryTagName1 = list(CategoryTag.objects.filter(id=1).values_list('name',flat=True))[0]#conditions
            properties_looped=str(categoryTagName2)+ '_looped'
            conditions_looped=str(categoryTagName1)+ '_looped'
   
            alloopedlist = []
            for fileParsed in extractdataformfields.fileuserutil.fileParsedList:
                for key,value in fileParsed.fields.iteritems():
                    allooped = []
                    if isinstance(value,dict):
                        if fileParsed.fields.has_key(properties_looped):
                            allooped= fileParsed.fields[properties_looped]
                            
                        if fileParsed.fields.has_key(conditions_looped):
                            allooped += fileParsed.fields[conditions_looped] 
                            
                    if allooped:    
                        #print allooped
                        alloopedlist.append(allooped)
                      
              
            for k,val in POST.iterlists(): 
                if k != 'csrfmiddlewaretoken':
                    line = (k.split())
                    nlines = (line[0]).split('_')
                    #print nlines
                    tag = line[1]
                    if  len(nlines) == 1:
                        if k != 'csrfmiddlewaretoken':
                            dimension = 1
                            #print str(k),val
                            lst= tag.split('_')[-1]
                            try:
                                int(lst)
                                lineindexvalue = 0
                            except  Exception as e:
                                lineindexvalue = 1
        
                            #print lineindexvalue
                            chg,error=extractdataformfields.fileuserutil.findAndUpdateLine(str(nlines[0]),val,str(dimension),lineindexvalue)
                            if error != None:
                                break
                            
                            if chg != False and change==False:
                                change = chg
                                
                        
                    elif  len(nlines) == 2:
                        #print str(k),val
                        #print tag
                        findline = str(nlines[1])  
                        #print findline,tag,val
                        lst= tag.split('_')[-1]
                        try:
                            int(lst)
                            lineindexvalue = 0
                        except  Exception as e:
                            lineindexvalue = 1
                            
                        #print lineindexvalue
                        dimension = 0
                        chg,error= extractdataformfields.fileuserutil.findAndUpdateLine(str(nlines[1]),val,str(dimension),lineindexvalue)
                        if error != None:
                            break
                        
                        if chg != False and change==False:
                                change = chg
                        
                    elif len(nlines) == 3:
                        for al in alloopedlist:
                            find = str(nlines[0]) +' ' + tag
                            if find in al:
                                indexfromal= al.index(find)
                                """print 'index of line ', indexfromal
                                print  str(nlines[0]),tag
                                print str(nlines[1]), str(nlines[2]),val
                                """
                                
                                linefrom = int(str(nlines[1]))
                                lineto = int(str(nlines[2])) + 1
                                vals = val[0].split()
                                counterlines = 0
                                for x in range(linefrom, lineto):
                                    if len(vals) == 1:
                                        #print x, tag, val
                                        dimension = 2
                                        chg,error=extractdataformfields.fileuserutil.findAndUpdateLine(str(x),val,str(dimension),indexfromal)   
                                        if error != None:
                                            break
                                        
                                        if chg != False and change==False:
                                            change = chg
                                           
                                    elif  len(vals) > 1:
                                        dimension = 1
                                        #print x, vals[counterlines]  
                                        chg,error=extractdataformfields.fileuserutil.findAndUpdateLine(str(x),[vals[counterlines]],str(dimension),indexfromal)  
                                        if error != None:
                                            break
                                        
                                        if chg != False and change==False:
                                            change = chg
                                         
                                        counterlines += 1
    
                        if error != None:
                            break
                        
            return change,error
    
        def updateFile(self,obj, lines):
            paths = None
            pathslist=Path.objects.all()      
            for path in pathslist:
                if os.path.isdir(path.cifs_dir): 
                    cifs_dir= path.cifs_dir 
                    cifs_dir_valids=path.cifs_dir_valids 
                    cifs_dir_invalids=path.cifs_dir_invalids 
                    cifs_dir_output= path.cifs_dir_output 
                    core_dic_filepath=path.core_dic_filepath 
                    mpod_dic_filepath=path.mpod_dic_filepath 
                    datafiles_path =path.mpod_dic_filepath 
                    break
 
            filename= obj.filename 
            
            ciffilein = os.path.join(str(cifs_dir_valids),filename)
            if os.path.exists(ciffilein):
                ciffileout = os.path.join(str(cifs_dir_valids),  filename  )
                with open(ciffileout, 'w') as outfile:
                    for line in lines:
                        nl = line + '\n'
                        outfile.write(nl)
            else:
                err = 'The file no longer exists'
                raise ValueError(err)
                        
       
        def sendMail(self,request,obj):      
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
                                                                            'code':  str(obj.datafile.code),
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
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                err= {}
                err['file']=fname
                err['line']=exc_tb.tb_lineno
                err['error']="Error: {1}".format( e.message, e.args) 
                messages.add_message(request, messages.ERROR, "ERROR %s " % err)
     
                                
                                       
        
        def save_model(self, request, obj, form, change):
            warning= False 
            message= ''   
            try:
                if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue') and not request.POST.has_key('_save'):
                    print "pass"
                elif  request.POST.has_key('_addanother'): 
                    print request.POST.get('_addanother',False)

                elif request.POST.has_key('_save') or request.POST.has_key('_continue'):
 
                    dosave = True
                    POST = request.POST.copy()
                    if (POST.get('publish',False)  != False):
                        on=POST.pop('publish')[0]  
                        publish=True
                    else:
                        publish= False
                        
                    _continue = None
                    _save = None
                    if POST.has_key('_save'):
                        _save = POST.pop('_save')[0]
                    
                    if POST.has_key('_continue'):
                        _continue = POST.pop('_continue')[0]
                        
                    reportvalidation=POST.pop('reportvalidation')[0]  
                    postfilename =POST.pop('datafile')[0]
                    
                    if  POST.has_key('datepublished_0'):
                        fecha =POST.pop('datepublished_0')[0]  #[u'2019-07-06']
                        hora =POST.pop('datepublished_1')[0]  # [u'23:41:27']
                        
                    if POST.has_key('datafile'):
                        postfilename =POST.pop('datafile')[0]
 
                    if publish:
                        fileuserutil = None
                        if not 'extractdataformfields' in request.session or not request.session['extractdataformfields' ]: 
                            err = 'Reselect the file to change'
                            warning = True 
                            raise ValueError(err)
                        
                        else:
                            extractdataformfields= request.session['extractdataformfields']
                            change,error = self.updateLinesOnSession(POST,extractdataformfields)
                            self.updateFile(obj, extractdataformfields.fileuserutil.lines)

                            if  isinstance(error, type(None)):
                                pass
                                """
                                if change:
                                    self.updateFile(obj, extractdataformfields.fileuserutil.lines)
                                else:
                                    scc = 'No changed detected'
                                    messages.set_level(request, messages.SUCCESS)
                                    messages.success(request,  scc ) 
                                """
                            else:
                                raise ValueError(error)
    
                            if dosave:
                                makevalidation=False
                                loadtodatabase = True
                                customfile= False
                                fds2 = []    
                                fds2.append(obj.filename)
                                extractdataformfields.estr.publish = False
                                extractdataformfields.user =  obj.authuser
                                extractdataformfields.estr.fileuser = obj
                                extractdataformfields.debug = False
                                extractdataformfields.processData(loadtodatabase,fds2,customfile,makevalidation)    
                                
                                if obj.datafile==None:
                                    extractdataformfields.estr.publish = publish
                                    extractdataformfields.estr.filename= None
                                    extractdataformfields.estr.article = None
                                    extractdataformfields.estr.dataFile = None
                                    extractdataformfields.debug = False
                                    extractdataformfields.processData(loadtodatabase,fds2,customfile,makevalidation)   
                                else:
                                    fds2 = []    
                                    fds2.append(obj.datafile.filename)
                                    extractdataformfields.estr.publish = publish
                                    extractdataformfields.estr.filename= None
                                    extractdataformfields.estr.article = None
                                    extractdataformfields.estr.dataFile = None
                                    extractdataformfields.debug = False
                                    extractdataformfields.processData(loadtodatabase,fds2,customfile,makevalidation) 
                                        
                                    
                              
                                self.sendMail(request,obj)
 
                            scc = 'Archive published'
                            messages.set_level(request, messages.SUCCESS)
                            messages.success(request, scc )
                        
                    else:

                        fileuserutil = None
                        if not 'extractdataformfields' in request.session or not request.session['extractdataformfields' ]: 
                            err = 'Reselect the file to change'
                            warning = True 
                            raise ValueError(err)
                        
                        else:
                            extractdataformfields= request.session['extractdataformfields']
                            change,error = self.updateLinesOnSession(POST,extractdataformfields)
                            self.updateFile(obj, extractdataformfields.fileuserutil.lines)
 
                            if  isinstance(error, type(None)):
                                pass
                                """if change:
                                    self.updateFile(obj, extractdataformfields.fileuserutil.lines)
                                else:
                                    scc = 'No changed detected'
                                    messages.set_level(request, messages.SUCCESS)
                                    messages.success(request,  scc ) 
                                """
                            else:
                                raise ValueError(error)
                                    
                                    
                            if dosave:
                                makevalidation=False
                                loadtodatabase = True
                                customfile= False
                                fds2 = []    
                                fds2.append(obj.filename)
                                extractdataformfields.estr.publish = publish
                                extractdataformfields.estr.fileuser = obj
                                extractdataformfields.user =  obj.authuser
                                extractdataformfields.debug = False
                                extractdataformfields.processData(loadtodatabase,fds2,customfile,makevalidation)   
                                
                                if obj.datafile.active == True:
                                    obj.datafile.active = publish
                                    obj.datafile.save()
                                    
                                #if obj.publish == True:
                                obj.publish =  publish
                                obj.save()
                                    
                                    
                                    
                                scc = 'File unpublished'
                                messages.set_level(request, messages.SUCCESS)
                                messages.success(request,  scc ) 
 
                        
            except  Exception as e:
                if not warning:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    err= {}
                    err['file']=fname
                    err['line']=exc_tb.tb_lineno
                    err['error']="Error: {1}".format( e.message, e.args) 
                    
                    messages.set_level(request, messages.ERROR)
                    messages.error(request, "ERROR %s " % err ) 
                else:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      
                    
                    messages.set_level(request, messages.WARNING)
                    messages.warning(request, "WARNING :  " + e.message  ) 
                    
                     
        
admin.site.register(FileUser, FileUserAdminv2)

 
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
 

class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        # Return a string of the format: "firstname lastname (username)"
        return "%s (%s)"%(obj.get_full_name(), obj.username)  
    
 
class CategoryView(ChangeList):
        def __init__(self, *args, **kwargs):
            super(CategoryView, self).__init__(*args, **kwargs)
            #self.list_display = ('username', 'email', 'date_joined', 'last_login')
    
        def get_queryset(self, request):
            qs = super(CategoryView, self).get_queryset(request)
            return qs.filter(deploy=False)
        
                  
class DictionaryAdmin(admin.ModelAdmin): 
    form=DictionaryForm
    list_display =('tag','category','active','deploy','categorytag',)  
    search_fields = ['name', 'category__name','category__description','categorytag__description',]
    actions = ['make_deployed']#usando un action local
    
    def get_fieldsets(self, *args, **kwargs):
        return  (
            ('Property', {
                'fields': ('tag' ,'name' ,'description' ,'units' ,'units_detail' , 'active','definition', 'deploy','type',),
            }),
            ('Dictionary Category', {
                'fields': ('category',),
            }),
            ('Tag Category', {
                'fields': ('categorytag',), 
            })
                 
        )
 
    
    def make_deployed(self, request, queryset):
        #queryset.update(deploy=1)
        rows_updated = queryset.update(deploy=1)
        if rows_updated == 1:
            message_bit = "1 property was set for deploy"
        else:
            message_bit = "%s properties were" % rows_updated
        self.message_user(request, "%s successfully marked as deployed." % message_bit)
    
    make_deployed.short_description = "Mark selected properties as deployed"
    
    def existObjectInDB(self,model, fields, operator=None):
        kwargs = {}
        for kar,var in model.__dict__.iteritems():
            if kar == '_state':
                pass
            elif kar == 'id':
                pass
            else:
                if fields.has_key(kar):
                    if isinstance(fields, dict):
                        if operator:
                            kwargs['{0}__{1}'.format(kar, operator)] = fields[kar]
                        else:
                                kwargs['{0}'.format(kar)] = fields[kar]
                            
        art = None                   
        if isinstance(model, DataFile):
            art= list((model.__class__).objects.filter(**kwargs).values_list('code',flat=True))
        else:
            art= list((model.__class__).objects.filter(**kwargs).values_list('id',flat=True))
        
        if art:
            if isinstance(model, DataFile):
                if len(art) == 1:
                    res = (model.__class__).objects.get(code=art[0])
                else:
                    res = (model.__class__).objects.filter(code__in=art)
            else:
                if len(art) == 1:
                    res = (model.__class__).objects.get(id=art[0])
                else:
                    res = (model.__class__).objects.filter(id__in=art)
 
            return res
        else:
            return None 
    
    def saveObjectInDB(self,model,dictionary ):
        
        for key, val in dictionary.__dict__.iteritems():
            if model.__dict__.has_key(key):
                if key == '_state':
                    pass
                elif key == 'id':
                    pass
                else:
                    model.__dict__[key] = val
        
        
        model.save()             
                      
    
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
            obj.save()  
            POST = request.POST.copy()
            tag = None
            category = None
            categorytag = None
            name = None
            description = None
            units = None
            units_detail = None
            active = None
            res = None
            property = Property()
            propertyTemp = PropertyTemp()
            experimentalParCondTemp = ExperimentalParCondTemp()
            experimentalParCond = ExperimentalParCond()
           
            
            if (POST.get('tag',False)  != False):
                tag = POST.pop('tag')[0]  
                category = POST.pop('category')[0]  
                categorytag = POST.pop('categorytag')[0]  
                name = POST.pop('name')[0]  
                description = POST.pop('description')[0] 
                units = POST.pop('units')[0] 
                units_detail = POST.pop('units_detail')[0] 
                active = POST.pop('active')[0] 
                
                params = {}
                params['tag']  = tag
                
                if int(categorytag) == 2:
                    res = self.existObjectInDB(Property(), params, 'exact')
                    if res:
                        property = res
     
                    self.saveObjectInDB(property,obj )
                        
                    res = self.existObjectInDB(PropertyTemp(), params, 'exact')
                    if res:
                        propertyTemp = res
                        
                    self.saveObjectInDB(propertyTemp,obj )
                    
                    
                     
                    
                    
                else:    
                    res = self.existObjectInDB(ExperimentalParCondTemp(), params, 'exact')
                    if res:
                        experimentalParCondTemp = res
                        
                    self.saveObjectInDB(experimentalParCondTemp,obj )
                        
                    res = self.existObjectInDB(ExperimentalParCond(), params, 'exact')
                    if res:
                        experimentalParCond = res
                        
                    self.saveObjectInDB(experimentalParCond,obj )

                #tensor_dimensions = models.CharField(max_length=10)
                
                
          
                params = {}
                params['tag']  = tag.split("_")[2]     
                params['categorytag_id']  = int(categorytag) 
                res = self.existObjectInDB(Tags(), params, 'exact')
                tags = Tags()
                if res:
                    tags = res
 
                tags.tag =  tag.split("_")[2] 
                tags.active=  True
                ct=CategoryTag.objects.get(id=int(categorytag) )
                tags.categorytag =  ct
                tags.save()
            
        
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
 
#admin.site.register([DummyModel], DummyModelAdmin)


"""
class TagsInline(admin.TabularInline):
    model = Tags
    extra = 0
    
class CategoryTagAdmin(admin.ModelAdmin):
    form = CatalogPropertyAdminForm
    fieldsets = (
        ('Category Tag', {
            'fields': ('name','description',)
        }),
    )
    
    
    inlines = [TagsInline,]
    
admin.site.register( CategoryTag, CategoryTagAdmin)
"""


class TagsAdmin(admin.ModelAdmin):
    model = Tags
    list_display =('tag','active','categorytag',)  
    
    fieldsets = (
        ('Tag', {
            'fields': ('tag','active','categorytag',)
        }),
    )
 
    
#admin.site.register( Tags, TagsAdmin)

class CategoryTagAdmin(admin.ModelAdmin):
    form = CatalogPropertyAdminForm
    fieldsets = (
        ('Category Tag', {
            'fields': ('name','description',)
        }),
    )
 
admin.site.register( CategoryTag, CategoryTagAdmin)
 
 
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
                'fields': ('name','description','active','catalogproperty',('type','crystalsystemtype'),'catalogpointgroup','pointgroupdetail','pointgroupnames','pointgroupnamesdetail','axis','axisdetail'),
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
            pointgroupnames_id = requestPostToInt(request.POST,'pointgroupnames')
            type_id  = requestPostToInt(request.POST,'type')
            del_catalogpointgroup_ids = requestPostToIntList(request.POST,'delete_catalogpointgroup')
            del_pointgroupnames_ids = requestPostToIntList(request.POST,'delete_pointgroupnames')
            axis_new_ids = requestPostToIntList(request.POST,'axis')
            axis_new_ids = requestPostToIntList(request.POST,'axis')
            typeSelected = Type.objects.get(id= type_id)
            pointgroupnamesSelected = PointGroupNames.objects.get(id= pointgroupnames_id)
            catalogpointgroupSelected = CatalogPointGroup.objects.get(id=catalogpointgroup_id)
            
            crystalsystemtype_active= requestPostToBoolean(request.POST,'crystalsystemtype')
            crystalsystemtype = None
            try:
                crystalsystemtype=CrystalSystemType.objects.get(catalogcrystalsystem=obj,type=typeSelected)   
            except ObjectDoesNotExist as error:
                print "Message({0}): {1}".format(99, error.message) 
            
            if crystalsystemtype: 
                crystalsystemtype.active= crystalsystemtype_active
                crystalsystemtype.save()
            else:
                crystalsystemtype=CrystalSystemType()
                crystalsystemtype.catalogcrystalsystem = obj
                crystalsystemtype.type = typeSelected
                crystalsystemtype.active = crystalsystemtype_active
                crystalsystemtype.save()
                
            
            if crystalsystemtype_active== True:
                if axis_new_ids:
                    axis_old_ids = CrystalSystemAxis.objects.filter(catalogcrystalsystem=obj,type_id = type_id,catalogpointgroup= catalogpointgroupSelected,pointgroupnames = pointgroupnamesSelected,active=1).values_list('axis_id',flat=True)  
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
                            csaQuerySet = CrystalSystemAxis.objects.filter(axis_id=newlist[i],catalogcrystalsystem=obj,type_id = type_id,catalogpointgroup= catalogpointgroupSelected,pointgroupnames = pointgroupnamesSelected,active=0)
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
                                csa.pointgroupnames = pointgroupnamesSelected
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
     
     
        
                if del_catalogpointgroup_ids or del_pointgroupnames_ids:
     
                    for id in del_pointgroupnames_ids:
                        catalogpointgroupSelected = CatalogPointGroup.objects.get(id= id)
                        cspgn=CrystalSystemPointGroupNames.objects.get(catalogcrystalsystem=obj,pointgroupnames_id=id,type_id = type_id)
                        cspgn.active = 0
                        print cspgn.pointgroupnames.name
                        cspgn.save()
                        del cspgn
                        
                    for id in del_catalogpointgroup_ids:
                        cspg=CrystalSystemPointGroup.objects.get(catalogcrystalsystem=obj,catalogpointgroup=catalogpointgroupSelected,type_id = type_id)
                        cspg.active = 0
                        cspg.save()
                        #cspg.delete()
                        del cspg
      
                else:
                    if  (catalogpointgroup_id == 45  and  pointgroupnames_id  != 21 ):
                        if obj.pk: 
                            crystalsystempointgroupnamesQuerySet = CrystalSystemPointGroupNames.objects.filter(catalogcrystalsystem=obj,pointgroupnames=pointgroupnamesSelected,type=typeSelected,active =1)
                            if  crystalsystempointgroupnamesQuerySet:
                                messages.set_level(request, messages.WARNING)
                                messages.warning(request, 'the process was not done, point group names "'+ pointgroupnamesSelected.name +'" already exist for this crystal system: ' + typeSelected.description)
                            else:
                                crystalsystempointgroupnamesQuerySet = CrystalSystemPointGroupNames.objects.filter(catalogcrystalsystem=obj,pointgroupnames=pointgroupnamesSelected,type=typeSelected,active =0)
                                if crystalsystempointgroupnamesQuerySet:
                                    for i,o in enumerate(crystalsystempointgroupnamesQuerySet):
                                        crystalsystempointgroupnamesQuerySet[i].active = True
                                        crystalsystempointgroupnamesQuerySet[i].save()
        
                                    crystalsystempointgroupQuerySet = CrystalSystemPointGroup.objects.filter(catalogcrystalsystem=obj, type=typeSelected,active =1)
                                    if crystalsystempointgroupQuerySet:
                                        for i,o in enumerate(crystalsystempointgroupQuerySet):
                                            crystalsystempointgroupQuerySet[i].active = False
                                            crystalsystempointgroupQuerySet[i].save()
                        
                                else:
                                    crystalsystempointgroupnames=CrystalSystemPointGroupNames()
                                    crystalsystempointgroupnames.catalogcrystalsystem = obj
                                    crystalsystempointgroupnames.pointgroupnames= pointgroupnamesSelected
                                    crystalsystempointgroupnames.type=typeSelected
                                    crystalsystempointgroupnames.active = True
                                    crystalsystempointgroupnames.save()
                                    
                                    crystalsystempointgroupQuerySet = CrystalSystemPointGroup.objects.filter(catalogcrystalsystem=obj, type=typeSelected,active =1)
                                    if crystalsystempointgroupQuerySet:
                                        for i,o in enumerate(crystalsystempointgroupQuerySet):
                                            crystalsystempointgroupQuerySet[i].active = False
                                            crystalsystempointgroupQuerySet[i].save()
                        else:
                            obj.save()
                            crystalsystempointgroupnames=CrystalSystemPointGroupNames()
                            crystalsystempointgroupnames.catalogcrystalsystem = obj
                            crystalsystempointgroupnames.pointgroupnames= pointgroupnamesSelected
                            crystalsystempointgroupnames.type=typeSelected
                            crystalsystempointgroupnames.active = True
                            crystalsystempointgroupnames.save()
        
                    elif (catalogpointgroup_id  != 45  and  pointgroupnames_id== 21):
                        if obj.pk: 
                            crystalsystempointgroupQuerySet = CrystalSystemPointGroup.objects.filter(catalogcrystalsystem=obj,catalogpointgroup=catalogpointgroupSelected, type=typeSelected,active =1)
                            if  crystalsystempointgroupQuerySet:
                                messages.set_level(request, messages.WARNING)
                                messages.warning(request, 'the process was not done, point group  "'+ catalogpointgroupSelected.name +'" already exist for this crystal system: ' + typeSelected.description)
                            else:
                                crystalsystempointgroupQuerySet = CrystalSystemPointGroup.objects.filter(catalogcrystalsystem=obj,catalogpointgroup=catalogpointgroupSelected, type=typeSelected,active =0)
                                if crystalsystempointgroupQuerySet:
                                    for i,o in enumerate(crystalsystempointgroupQuerySet):
                                        crystalsystempointgroupQuerySet[i].active = True
                                        crystalsystempointgroupQuerySet[i].save()
                                            
                                    
                                    crystalsystempointgroupnamesQuerySet = CrystalSystemPointGroupNames.objects.filter(catalogcrystalsystem=obj,type=typeSelected,active =1)
                                    if crystalsystempointgroupnamesQuerySet:
                                        for i,o in enumerate(crystalsystempointgroupnamesQuerySet):
                                            print crystalsystempointgroupnamesQuerySet[i].pointgroupnames
                                            crystalsystempointgroupnamesQuerySet[i].active = False
                                            crystalsystempointgroupnamesQuerySet[i].save()
       
                                else:       
                                    crystalsystempointgroup=CrystalSystemPointGroup()
                                    crystalsystempointgroup.catalogcrystalsystem = obj
                                    crystalsystempointgroup.type=typeSelected
                                    crystalsystempointgroup.active = True
                                    crystalsystempointgroup.catalogpointgroup= catalogpointgroupSelected
                                    crystalsystempointgroup.save()
                                
                                    crystalsystempointgroupnamesQuerySet = CrystalSystemPointGroupNames.objects.filter(catalogcrystalsystem=obj,type=typeSelected,active =1)
                                    if crystalsystempointgroupnamesQuerySet:
                                        for i,o in enumerate(crystalsystempointgroupnamesQuerySet):
                                            print crystalsystempointgroupnamesQuerySet[i].pointgroupnames
                                            crystalsystempointgroupnamesQuerySet[i].active = False
                                            crystalsystempointgroupnamesQuerySet[i].save()
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

class PointGroupGroupsInline(admin.TabularInline):
    model = PointGroupGroups
    insert_after = 'description'
    

class PointGroupNamesAdmin(admin.ModelAdmin):
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
            PointGroupGroupsInline,
        ]
    
    """
   
 
    
    def selectlist_view(self, request, extra_context=None):
            print 'PointGroupNames_selectlist_view'
            temp_list_display_links = self.list_display_links
            self.list_display_links = (None, )
            response = self.changelist_view(request, extra_context)
            self.list_display_links = temp_list_display_links
            return response
    
    def change_view(self, request, object_id, extra_context=None):
        print 'PointGroupNames_change_view'
        
        extra = {
            'n1': 'Change Property', 
            'n2':'Property',
        }
        
        #print self.model._meta
        
        result = super(PointGroupNamesAdmin, self).change_view(request, object_id, extra_context=extra)        
        pointGroupNames = PointGroupNames.objects.get(id__exact=object_id)
        #if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):

        return result
  
    
    def save_model(self, request, obj, form, change):
        print 'PointGroupNames_save_model'
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
     

    
#admin.site.register(PointGroupNames, PointGroupNamesAdmin)

 
        



class GroupNamesDetailAdmin(admin.ModelAdmin):
    form=GroupNamesDetailAdminForm
    """fieldsets = (
        ('Group Names Detail', {
            'fields': ('pointgroupnames', 'catalogpointgroup',)
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
           
            queryset = PointGroupGroups.objects.filter(pointgroupnames=obj)
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
            catalogpointgroup_old_ids =  PointGroupGroups.objects.filter(pointgroupnames=obj).values_list('catalogpointgroup_id',flat=True)  
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
                    pgg=PointGroupGroups()
                    pgg.catalogpointgroup = catalogpointgroupNewQuerySet[i]
                    pgg.pointgroupnames = obj
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
                pgg=PointGroupGroups()
                pgg.catalogpointgroup = catalogpointgroupQuerySet[i]
                pgg.pointgroupnames = obj
                #pgg.save()
                del pgg"""
   
        #super(GroupNamesDetailAdmin, self).save_model(request, obj, form, change)

    def queryset(self, request):
        qs = super(GroupNamesDetailAdmin, self).queryset(request)

        return qs.all().exclude(id=21)
        #return super(GroupNamesDetailAdmin, self).get_queryset().all().exclude(id=21)

admin.site.register(GroupNamesDetail, GroupNamesDetailAdmin)

class CatalogPropertyDetailAdmin(admin.ModelAdmin):
    list_display =('name','get_type_description','get_crystalsystem_catalogproperty_description','get_crystalsystem_description','get_catalogaxis_name','get_catalogpointgroup_name','get_pointgroupnames_name','dataproperty')  
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
        ('Catalog Point Group Names', {
            'fields': ('pointgroupnames', )
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
        
    def get_pointgroupnames_name(self, obj):
        try:
            return  u'%s' % (obj.pointgroupnames.name)               
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
    
    get_pointgroupnames_name.short_description = 'Groups'
    get_pointgroupnames_name.allow_tags=True 
    
    
     
    
    
admin.site.register(CatalogPropertyDetail, CatalogPropertyDetailAdmin)


class TypeDataPropertyAdmin(admin.ModelAdmin):
 
    
    list_display =('type','dataproperty', )   
    list_filter = ('type__catalogproperty__description','type__description',)
    #fields = ['pointgroupnames','catalogpointgroup','catalogpointgroup1']
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
    
    
#admin.site.register(Property,PropertyAdmin)










class TensorAdmin(admin.ModelAdmin):
    form=TensorAdminForm
    readonly_fields=['name','description','active']
   
    
    def get_fieldsets(self, *args, **kwargs):
        return  (
            ('Tensor', {
                'fields': ('errormessage','name','description','active','type','dataproperty','catalogcrystalsystem','catalogpointgroup','pointgroupdetail','pointgroupnames','pointgroupnamesdetail','axis','axisdetail','coefficients',('coefficientsrules','keynotation','zerocomponent','jquery',),'detailrules',),
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
                keyNotationCatalogPropertyDetail.save()
            
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
            datapropertySelected= Property.objects.get(id=int(datapropertySelected_id), active=True)  
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
    """
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
    """
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
            
 
           
            queryset = PointGroupGroups.objects.filter(pointgroupnames=obj)
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
                datapropertySelected=Property.objects.get(id=int(dataproperty_id), active=True)
                print datapropertySelected
            
            catalogcrystalsystem_id = 0
            if request.POST.get('catalogcrystalsystem',False)  != False:
                catalogcrystalsystem_id = int(request.POST.get('catalogcrystalsystem',False))
                print catalogcrystalsystem_id
                
            type_id = 0
            if  request.POST.get('type',False) != False:
                type_id=int(request.POST.get('type',False))
                print type_id
                
            pointgroupnames_id = 21
            if  request.POST.get('pointgroupnames',False) != False:
                pointgroupnames_id=int(request.POST.get('pointgroupnames',False))
                print pointgroupnames_id

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
                    
                  
                        nameValuesQuerySet = CatalogPropertyDetail.objects.filter(   dataproperty_id = dataproperty_id,
                                                                                                                                            crystalsystem_id=catalogcrystalsystem_id,
                                                                                                                                            type_id=type_id,
                                                                                                                                            pointgroupnames_id=pointgroupnames_id,
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
                                newObj.dataproperty = Property.objects.get(id=int(dataproperty_id), active=True)
                                newObj.crystalsystem = CatalogCrystalSystem.objects.get(id=int(catalogcrystalsystem_id))
                                newObj.type = Type.objects.get(id=int(type_id))
                                newObj.pointgroupnames = PointGroupNames.objects.get(id=int(pointgroupnames_id))
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
                                                                                                                    pointgroupnames_id=pointgroupnames_id,
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
