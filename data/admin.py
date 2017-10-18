'''
Created on Aug 13, 2017

@author: admin
'''

from django.contrib.admin import *
from django.contrib import admin

from django.core  import urlresolvers

from .models import *
 



 
'''
@admin.register(models.Paths)
class PathsAdmin(admin.ModelAdmin):
      date_hierarchy = 'created'
      search_fields = ['cifs_dir', 'core_dic_filepath', 'mpod_dic_filepath','stl_dir','datafiles_path']
      list_display = ('cifs_dir', 'core_dic_filepath', 'mpod_dic_filepath','stl_dir','datafiles_path')
      list_filter = ('devmode',)'''


class MyAdminSite(AdminSite):
    site_header = 'Monty Python administration'
    
    

admin_site = MyAdminSite(name='MPOD')

admin.site.site_header = ("MPOD Administration")
admin.site.site_title = ("MPOD Admin")
admin.site.index_title=""
#admin.site.register(Paths)
'''
@admin.register(models.Paths)
class PathsAdmin(admin.ModelAdmin):
      date_hierarchy = 'created'
      search_fields = ['cifs_dir', 'core_dic_filepath', 'mpod_dic_filepath','stl_dir','datafiles_path']
      list_display = ('cifs_dir', 'core_dic_filepath', 'mpod_dic_filepath','stl_dir','datafiles_path')
      list_filter = ('devmode',)'''
      
      
 
class PathAdmin(admin.ModelAdmin):
    list_display =('cifs_dir', 'core_dic_filepath', 'mpod_dic_filepath','stl_dir','datafiles_path')     
    list_filter = ('devmode',)

admin.site.register(Path, PathAdmin)

class PublArticleAdmin(admin.ModelAdmin):
    list_display =('title', 'authors', 'journal','year','volume','issue','first_page','last_page','reference','pages_number')
    search_fields = ['title', 'authors', 'journal','year','volume']
    list_filter = ('year',)
    
admin.site.register(PublArticle, PublArticleAdmin)

class ExperimentalParCondAdmin(admin.ModelAdmin):
    list_display =('tag', 'description', 'name','units','units_detail')
    search_fields = ['tag', 'description', 'name','units','units_detail']


admin.site.register(ExperimentalParCond,ExperimentalParCondAdmin)

class DataFileAdmin(admin.ModelAdmin):
    list_display =('code', 'filename', 'cod_code', 'phase_generic','phase_name','chemical_formula' ,'get_article')
     
    def get_article(self, obj):
        link_to_article=os.path.join('../publarticle/' , str(obj.publication.id))
        link= "<a href="+link_to_article+">"+str(obj.publication.id)+"</a>"        
        return u'<a href="%s">%s</a>' % (link_to_article,obj.publication.id)    
    get_article.short_description = 'Article'
    get_article.allow_tags=True

    
admin.site.register(DataFile,DataFileAdmin)




 

