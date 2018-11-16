from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib import  admindocs
 
from django.conf.urls import url
from data.forms import *
from data.views import *
 

 

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()
 

urlpatterns = patterns('',
      # ADMIN
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/dictionary/$', dictionaryview,name='dictionary'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/Files/fileuser/(\d+)/showmatrix/(?P<pk>-?\d+)$', showmatrix, name='showmatrix'),
    url(r'^admin/Files/fileuser/(\d+)/updatecoefficient/(?P<pk>-?\d+)$', updatecoefficient, name='updatecoefficient'),
    

    #accounts
    url(r'^accounts/profile/$', 'data.views.viewprofile'),
    url(r'^accounts/update/(?P<pk>[\-\w]+)/$', edit_user,name='update'),
    url(r'^accounts/file/(?P<pk>\d+)$', file_detail_view, name='file-detail'),
    url(r'^accounts/onhold/(?P<todo>[\-\w]+)/(?P<index>-?\d+)/$', onhold, name='onhold'),
    url(r'^accounts/adddictionaryproperty/(?P<pk>-?\d+)$',adddictionaryproperty, name='adddictionaryproperty'), 
    url(r'^accounts/addnewdictionaryproperty/(?P<todo>[\-\w]+)/(?P<index>-?\d+)/$',addnewdictionaryproperty, name='addnewdictionaryproperty'), 
    url(r'^accounts/adddictionaryphase/(?P<pk>-?\d+)$',adddictionaryphase, name='adddictionaryphase'), 
    url(r'^accounts/adddictionaryphasecharacteristic/(?P<pk>-?\d+)$',adddictionaryphasecharacteristic , name='adddictionaryphasecharacteristic'), 
    url(r'^accounts/adddictionarymeasurement/(?P<pk>-?\d+)$',adddictionarymeasurement , name='adddictionarymeasurement'), 
    

      # USER
    #url(r'^signup/$', 'data.views.viewsignup'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^viewloginauthentication/$', 'data.views.viewloginauthentication'),
    url(r'^login/$', 'data.views.viewlogin'),
     #REGISTRATION MAIL
    url(r'^account_activation_sent/$', 'data.views.account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-=]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',  viewactivate , name='activate'),
    
    url(r'^logout/$', 'data.views.viewlogout'),
    
    # HOME
    
    url(r'^$','data.views.home'),
    #url(r'^home/$','data.views.home'),
    url(r'^$',home,name='home'),
    #url(r'^home/$', home,name='home'),
    # SEARCH BY
    url(r'^sbproperty/$','data.views.sbproperty'),
    url(r'^properties/(\d+)/$','data.views.viewproperty'),
    url(r'^dataitem/\d+/secondranktensor/$','data.views.viewsecondranktensor'),
    url(r'^dataitem/\d+/thirdranktensordg/$','data.views.viewthirdranktensordg'),
    url(r'^dataitem/\d+/thirdranktensoreh/$','data.views.viewthirdranktensoreh'),
    url(r'^dataitem/\d+/compliance/$','data.views.viewcompliance'),
    url(r'^dataitem/\d+/stiffness/$','data.views.viewstiffness'),
    url(r'^dataitem/\d+/fourthranktensor/$','data.views.viewfourthranktensor'),
    url(r'^dataitem/\d+/magnetostriction/$','data.views.viewmagnetostriction'),
    url(r'^dataitem/\d+/magnetocrystallineanisotropy/$','data.views.viewmagnetocrystallineanisotropy'),
    url(r'^dataitem/(\d+)/$','data.views.viewdataitem'),
    url(r'^datafiles/(.+[.]mpod)$','data.views.get_datafile'),
    url(r'^stlfiles/(.+[.]stl)$','data.views.get_stlfile'),    
    url(r'^datafilescreated/(.+[.]mpod)$',viewdatafilecreated, name='datafilecreated'),      
    url(r'^datafilescreated2/(?P<pk>[\-\w]+)/$', viewdatafilecreated2,name='datafilecreated2'),
    url(r'^datafilescreated3/(?P<filename>(.+[.]mpod))/$', viewdatafilecreated3,name='datafilecreated3'),
    url(r'^articles/(\d+)/$','data.views.viewarticle'),
    url(r'^exparcond/(\d+)/$','data.views.viewexparcond'),
    url(r'^dictionarydefinition/(\d+)/$','data.views.viewdictionarydefinition'),
    url(r'^sbcomposition/$','data.views.sbcomposition'),
    url(r'^sbreference/$','data.views.sbreference'),

    url(r'^newcasev2/$', newcasev2 , name='newcasev2'),
    url(r'^addcasev2/$','data.views.addcasev2'),
    url(r'^dataitem/(\d+)/rotatematrix/(?P<pk>-?\d+)$',rotatematrix, name='rotatematrix'), 
    
    
    
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



