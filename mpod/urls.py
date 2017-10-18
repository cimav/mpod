from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls import url
from data.forms import *

 

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
      # ADMIN
    url(r'^admin/', admin.site.urls),
      # USER
    url(r'^signup/$', 'data.views.viewsignup'),
    url(r'^viewloginauthentication/$', 'data.views.viewloginauthentication'),
    url(r'^login/$', 'data.views.viewlogin'),
    
    url(r'^logout/$', 'data.views.viewlogout'),
    
    # HOME
    url(r'^$','data.views.home'),
    url(r'^home/$','data.views.home'),
    # SEARCH BY
    url(r'^sbproperty/$','data.views.sbproperty'),
    url(r'^properties/(\d+)/$','data.views.viewproperty'),
    url(r'^dataitem/\d+/secondranktensor/$','data.views.viewsecondranktensor'),
    url(r'^dataitem/\d+/thirdranktensor/$','data.views.viewthirdranktensor'),
    url(r'^dataitem/\d+/compliance/$','data.views.viewcompliance'),
    url(r'^dataitem/\d+/stiffness/$','data.views.viewstiffness'),
    url(r'^dataitem/\d+/fourthranktensor/$','data.views.viewfourthranktensor'),
    url(r'^dataitem/\d+/magnetostriction/$','data.views.viewmagnetostriction'),
    url(r'^dataitem/\d+/magnetocrystallineanisotropy/$','data.views.viewmagnetocrystallineanisotropy'),
    url(r'^dataitem/(\d+)/$','data.views.viewdataitem'),
    url(r'^datafiles/(.+[.]mpod)$','data.views.get_datafile'),
    url(r'^stlfiles/(.+[.]stl)$','data.views.get_stlfile'),    
    url(r'^articles/(\d+)/$','data.views.viewarticle'),
    url(r'^exparcond/(\d+)/$','data.views.viewexparcond'),
    url(r'^sbcomposition/$','data.views.sbcomposition'),
    url(r'^sbreference/$','data.views.sbreference'),
    url(r'^addcase/$','data.views.addcase'),
    url(r'^newcase/$','data.views.newcase'),
    # DOCUMENTATION
    url(r'^docintroduction/$','data.views.docintroduction'),
    url(r'^docmpodfiles/$','data.views.docmpodfiles'),
    url(r'^docdictionary/$','data.views.docdictionary'),
    
    url(r'^references/$','data.views.references'),
    # ABOUT MPOD
    url(r'^introduction/$','data.views.introduction'),
    url(r'^mpodteam/$','data.views.mpodteam'),
    url(r'^terms/$','data.views.terms'),
)



