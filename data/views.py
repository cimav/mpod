# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from data.models import *

from django.db import models
from django.db.models import Q
from django.db.models import Count
import random
from my_forms import *
from requests.sessions import session
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_exempt
from WebT4 import * 
from WebRankTensors import *
from Magnetic import *
from Properties import *
from Propertiesv2 import *
from PropertyMaster import *
from mpodwrite import *
import gc
from forms import *

from django.contrib.auth import login, authenticate, logout
   
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from tokens import account_activation_token
from django.template.loader import render_to_string
#from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import base64 
from django.utils.encoding import  force_text
import six
from django.core import mail
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
from django.core.mail.backends.smtp import EmailBackend

from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied

from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http import Http404
import json
import urllib2
 
from UtilPlot  import *
from django.utils.timezone import get_current_timezone





#from django.core.urlresolvers import reverse
#from django.core.administration import EmailMessage
#from django.contrib.sites.models import *



######################################################################################
#                                 ''' GLOBAL FUNCTIONS '''
######################################################################################

######################################################################################
#                                 ''' HOME '''
######################################################################################
def home(request):
    current_site = get_current_site(request)#127.0.0.1:8000
    print current_site.domain
    print  request.build_absolute_uri('/')#http://127.0.0.1:8000/
    return render_to_response('home.html', context_instance=RequestContext(request))



######################################################################################
#                                 ''' ADMIN '''
######################################################################################
@staff_member_required
def dictionaryview(request):
    current_site = get_current_site(request)#127.0.0.1:8000
  
    return render_to_response('dictionary.html', context_instance=RequestContext(request))


#report = staff_member_required(report)

######################################################################################
#                                 ''' USER '''
######################################################################################
@csrf_exempt 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.instance.is_active = False
            form.save()
            
            #user.refresh_from_db()  # load the profile instance created by the signal
            #user.profile.birth_date = form.cleaned_data.get('birth_date')
            
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            #login(request, user)
            #uid= base64.b64encode(force_bytes(str(user.pk))),
            #token= account_activation_token.make_token(user)
            urlactivate ="activate"
            forwardslash="/"
            #print current_site.domain
            #linkactivate = os.path.join(urlactivate,forwardslash)
            #print request.build_absolute_uri('/activate/')
            
            current_site = get_current_site(request)
             
            print current_site.domain
            #smtpconfig = Configuration.objects.get(pk=1)
            print  request.build_absolute_uri('/')
                
 
             
            messageCategoryDetail1=MessageCategoryDetail.objects.get(messagecategory=MessageCategory.objects.get(pk=1))#category activation
            #messageMail= MessageMail.objects.get(pk=messageCategoryDetail1.message.pk)
            messageMailQuerySet2= MessageMail.objects.filter(pk=messageCategoryDetail1.message.pk)
                    
            for message   in messageMailQuerySet2:
                messageMail= MessageMail()
                messageMail = message
                
                if messageMail.pk == 1:
                    configurationMessage = ConfigurationMessage.objects.get(message=messageMail)
                    smtpconfig= configurationMessage.account
                    
                    
                    my_use_tls = False
                    if smtpconfig.email_use_tls ==1:
                        my_use_tls = True
                    
                    #fail_silently= False
                    connection = get_connection(host=smtpconfig.email_host, 
                                                                            port= int(smtpconfig.email_port ), 
                                                                            username=smtpconfig.email_host_user, 
                                                                            password=smtpconfig.email_host_password, 
                                                                            use_tls=my_use_tls) 
                
                     
                    message = render_to_string('account_activation_email.html', {
                        'regards':messageMail.email_regards,
                        'email_message':  messageMail.email_message,
                        'user': user,
                        'domain': current_site.domain,
                        'uid': base64.b64encode(force_bytes(str(user.pk))),
                        'token': account_activation_token.make_token(user),
                        'linkactivate': urlactivate,
                        'forwardslash':forwardslash
                    })
                    
                    print message
 
                    send_mail(
                                    messageMail.email_subject,
                                    message,
                                    smtpconfig.email_host_user,
                                    [user.email],
                                    connection=connection
                                )
                    
       
            return redirect('/account_activation_sent')
             
             
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


    
def force_bytes(value):
    if isinstance(value, six.string_types):
        return value.encode()
    return value

    
def viewactivate(request, uidb64, token):
    
    try:
        #uid = force_text(base64.urlsafe_b64decode(uidb64))
        uid = base64.urlsafe_b64decode(str(uidb64)) 
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
       
        
        '''user = authenticate(username=user.username, password=user.password)
        login(request, user)'''
        return redirect('/login')
    
    else:
        return render(request, 'account_activation_invalid.html')
    

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')  


def viewlogout(request):
    logout(request)
    return redirect('/login')
    
    
@csrf_exempt 
def viewloginauthentication(request):
    if request.method == 'POST':
        form = ValidationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)          
 
                request.session['user']=user
                 
                hop_form_url =reverse(edit_user,kwargs={'pk':user.pk})
                print hop_form_url 
                hop_form_url  =reverse('update',kwargs={'pk':user.pk})
                print hop_form_url 
                 
                return render_to_response('account/profile.html', {'form': form,'user':user}, context_instance=RequestContext(request))
            else:
                message = " Please try again."
                    
                return render_to_response('login.html', {'form': form,'message':message}, context_instance=RequestContext(request))
        
               
    else:
        form = ValidationForm()
        
    return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
        
      
       
     


def viewlogin(request):
    
    form = LoginForm()
    return render(request, 'login.html', {'form': form})



@login_required
def edit_user(request, pk):
    print "edit_user"
    user = User.objects.get(pk=pk)
    user_form = UserProfileForm(instance=user)
    """                                       inlineformset_factory(parent_model, model, form=ModelForm,
                                                                      formset=BaseInlineFormSet, fk_name=None,
                                                                      fields=None, exclude=None,
                                                                      extra=3, can_order=False, can_delete=True, max_num=None,
                                                                      formfield_callback=None):"""
                                                                      
    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('bio', 'phone', 'city', 'country', 'organization'),form=ProfileForm,can_delete=False)
    formset = ProfileInlineFormset(instance=user)
    
    
    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserProfileForm(request.POST, request.FILES, instance=user)
             
            try:
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)
            except ValidationError:
                formset = None

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                try:
                    formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)
                except ValidationError:
                    formset = None

                if formset and formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/accounts/profile/')
        
        
        current ="Update Profile"
        

        return render(request, "account/account_update.html", {
            "noodle": pk,
            "user_form": user_form,
            "formset": formset,
            "current": current,
        })
    else:
        raise PermissionDenied
    
@login_required
def viewprofile(request):   
    #TODO: crear lista de links para el menu
    navigation  = []

    return render_to_response("account/profile.html", {"navigation" : navigation}, context_instance=RequestContext(request))


@login_required
def file_detail_view(request,pk):
    try:
        user=User.objects.get(pk=pk)      
        files_user=FileUser.objects.filter(authuser=user)
        
        
        
        current ="My Files"
        counterfiles = 0
        if len(files_user) > 0:
            counterfiles = len(files_user)
            
        print counterfiles
        
    except FileUser.DoesNotExist:
        raise Http404("File does not exist")
    

    #book_id=get_object_or_404(Book, pk=pk)

    return render_to_response("account/file_detail.html", {'files':files_user,"current": current,"counterfiles": counterfiles}, context_instance=RequestContext(request))
    
            

######################################################################################
#                                ''' SEARCH BY '''
######################################################################################
def sbproperty(request):
    ogge = Property.objects.filter(active=True)
    properties_list_table_html = view_linked_properties_list(oggetti=ogge, header=None)
    return render_to_response('sbproperty.html', {"properties_list_table" : properties_list_table_html}, context_instance=RequestContext(request))

#-------------------------------------------------------------------------------------------

def viewproperty(request, property_id):
    ogge = None
    html_res = None
    html_res2 = None
    try:
        ogge = Property.objects.get(id__exact = property_id, active=True)
    except:
        pass
    if ogge:
        datafiles = DataFile.objects.filter(properties__id__exact = property_id, active=True)
        html_res = view_obj_as_2cols_table (Property, ogge, cap="Property details")
        html_res2 = view_as_linked_table(DataFile, oggetti=datafiles, header='Associated datafiles')
    #request_path=request.get_full_path()
    #debug_info=request_path
    return render_to_response('viewproperty.html', {"property_table": html_res, "associated_datafiles": html_res2}, context_instance=RequestContext(request))

#def viewdataitem(request, dataitem_id):
#    html_dataitem, html_tables = data_item_html(dataitem_id)
#    return render_to_response('viewdataitem.html', {"html_dataitem":html_dataitem, "html_tables":html_tables}, context_instance=RequestContext(request))

#antes era viewgraph
def viewdataitem(request, dataitem_id):
    html_dataitem, html_tables = data_item_html(dataitem_id)
    return render_to_response('viewdataitem.html', {"html_dataitem":html_dataitem, "html_tables":html_tables}, context_instance=RequestContext(request))

def viewsecondranktensor(request):
    
    secondRankTensor = SecondRankTensor(request.GET)

    XEC = None
    YEC = None
    ZEC = None
    filename1 = None
    surfacecolor = None
    colorscale = None
    colorscalep = None
    surfacecolorp = None
    XECp = None
    YECp = None
    ZECp = None
    filename1p = None
  
    tableWidth = 450
    tableHeight = 500
    divWidth = 450
    divHeight = 450 
    layoutHeight = 450
    layoutWeight = 450
    tableWidthHeight = ""
    divWidthHeight = ""
 
    resolutionTag = ""
    if secondRankTensor.valuearrayrotated == None:
        secondRankTensor.SingleCrystal()        
        XEC = secondRankTensor.jason_data['XEC']
        YEC = secondRankTensor.jason_data['YEC']
        ZEC = secondRankTensor.jason_data['ZEC']
        filename1 = secondRankTensor.jason_data['filename1']
        surfacecolor = secondRankTensor.jason_data['surfacecolor']

    else:
        secondRankTensor.SingleCrystalAndPoly()
        XEC = secondRankTensor.jason_data['XEC']
        YEC = secondRankTensor.jason_data['YEC']
        ZEC = secondRankTensor.jason_data['ZEC']
        filename1 = secondRankTensor.jason_data['filename1'] 
        surfacecolor = secondRankTensor.jason_data['surfacecolor']

        XECp = secondRankTensor.jason_data_poly['XEC']
        YECp = secondRankTensor.jason_data_poly['YEC']
        ZECp = secondRankTensor.jason_data_poly['ZEC']
        filename1p = secondRankTensor.jason_data_poly['filename1'] 
        surfacecolorp = secondRankTensor.jason_data_poly['surfacecolor']
        
        #tableHeight = tableHeight  * 2
        tableWidth = tableWidth * 2 
 
    
       

    tableWidthHeight = 'height:'+  str(tableHeight) +'px;  width:' +  str(tableWidth) + 'px;'
    divWidthHeight = 'height:'+  str(divHeight) +'px;  width:' +  str(divWidth) + 'px;'
    
    colorscale = secondRankTensor.colorscale
     
 
    if secondRankTensor.res == 1:
        resolutionTag = "Low"
    elif secondRankTensor.res == 2:
        resolutionTag = "Middle"
    elif secondRankTensor.res == 3:
        resolutionTag = "High"
        

    return render_to_response('secondranktensor.html',{"XEC": XEC,
                                                                                                  "YEC": YEC,
                                                                                                   "ZEC": ZEC,
                                                                                                   "filename1":filename1,
                                                                                                   'colorscale':colorscale,
                                                                                                   'surfacecolor':surfacecolor,
                                                                                                   "XECp": XECp,
                                                                                                  "YECp": YECp,
                                                                                                   "ZECp": ZECp,
                                                                                                   "filename1p":filename1p, 
                                                                                                   'surfacecolorp':surfacecolorp,                                                                                          
                                                                                                   "resolutionTag":resolutionTag,
                                                                                                    "tableWidth": tableWidth,
                                                                                                    "tableHeight": tableHeight,
                                                                                                    "divWidth" : divWidth,
                                                                                                    "divHeight" : divHeight,          
                                                                                                    "tableWidthHeight": tableWidthHeight,
                                                                                                    "divWidthHeight": divWidthHeight,
                                                                                                    "layoutHeight":layoutHeight,
                                                                                                      "layoutWeight":layoutWeight,                                                                                 
                                                                                                  }, context_instance=RequestContext(request))

        
    #return render_to_response('secondranktensor.html', context_instance=RequestContext(request))

def viewthirdranktensordg(request):
    
    thirdRankTensordg = ThirdRankTensordg(request.GET)

    XEC = None
    YEC = None
    ZEC = None
    filename1 = None
    surfacecolor = None
    colorscale = None
    colorscalep = None
    surfacecolorp = None
    XECp = None
    YECp = None
    ZECp = None
    filename1p = None
  
    tableWidth = 450
    tableHeight = 500
    divWidth = 450
    divHeight = 450 
    layoutHeight = 450
    layoutWeight = 450
    tableWidthHeight = ""
    divWidthHeight = ""
 
    resolutionTag = ""
    if thirdRankTensordg.valuearrayrotated == None:
        thirdRankTensordg.SingleCrystal()        
        XEC = thirdRankTensordg.jason_data['XEC']
        YEC = thirdRankTensordg.jason_data['YEC']
        ZEC = thirdRankTensordg.jason_data['ZEC']
        filename1 = thirdRankTensordg.jason_data['filename1']
        surfacecolor = thirdRankTensordg.jason_data['surfacecolor']

    else:
        thirdRankTensordg.SingleCrystalAndPoly()
        XEC = thirdRankTensordg.jason_data['XEC']
        YEC = thirdRankTensordg.jason_data['YEC']
        ZEC = thirdRankTensordg.jason_data['ZEC']
        filename1 = thirdRankTensordg.jason_data['filename1'] 
        surfacecolor = thirdRankTensordg.jason_data['surfacecolor']

        XECp = thirdRankTensordg.jason_data_poly['XEC']
        YECp = thirdRankTensordg.jason_data_poly['YEC']
        ZECp = thirdRankTensordg.jason_data_poly['ZEC']
        filename1p = thirdRankTensordg.jason_data_poly['filename1'] 
        surfacecolorp = thirdRankTensordg.jason_data_poly['surfacecolor']
        
        #tableHeight = tableHeight  * 2
        tableWidth = tableWidth * 2 
       

    tableWidthHeight = 'height:'+  str(tableHeight) +'px;  width:' +  str(tableWidth) + 'px;'
    divWidthHeight = 'height:'+  str(divHeight) +'px;  width:' +  str(divWidth) + 'px;'
    
    colorscale = thirdRankTensordg.colorscale
 
    if thirdRankTensordg.res == 1:
        resolutionTag = "Low"
    elif thirdRankTensordg.res == 2:
        resolutionTag = "Middle"
    elif thirdRankTensordg.res == 3:
        resolutionTag = "High"
        

    return render_to_response('thirdranktensor.html',{"XEC": XEC,
                                                                                                  "YEC": YEC,
                                                                                                   "ZEC": ZEC,
                                                                                                   "filename1":filename1,
                                                                                                   'colorscale':colorscale,
                                                                                                   'surfacecolor':surfacecolor,
                                                                                                   "XECp": XECp,
                                                                                                  "YECp": YECp,
                                                                                                   "ZECp": ZECp,
                                                                                                   "filename1p":filename1p, 
                                                                                                   'surfacecolorp':surfacecolorp,                                                                                          
                                                                                                   "resolutionTag":resolutionTag,
                                                                                                    "tableWidth": tableWidth,
                                                                                                    "tableHeight": tableHeight,
                                                                                                    "divWidth" : divWidth,
                                                                                                    "divHeight" : divHeight,          
                                                                                                    "tableWidthHeight": tableWidthHeight,
                                                                                                    "divWidthHeight": divWidthHeight,
                                                                                                    "layoutHeight":layoutHeight,
                                                                                                      "layoutWeight":layoutWeight,                                                                                 
                                                                                                  }, context_instance=RequestContext(request))
    
def viewthirdranktensoreh(request):
  
    thirdRankTensoreh = ThirdRankTensoreh(request.GET)

    XEC = None
    YEC = None
    ZEC = None
    filename1 = None
    surfacecolor = None
    colorscale = None
    colorscalep = None
    surfacecolorp = None
    XECp = None
    YECp = None
    ZECp = None
    filename1p = None
  
    tableWidth = 450
    tableHeight = 500
    divWidth = 450
    divHeight = 450 
    layoutHeight = 450
    layoutWeight = 450
    tableWidthHeight = ""
    divWidthHeight = ""
 
    resolutionTag = ""
    if thirdRankTensoreh.valuearrayrotated == None:
        thirdRankTensoreh.SingleCrystal()        
        XEC = thirdRankTensoreh.jason_data['XEC']
        YEC = thirdRankTensoreh.jason_data['YEC']
        ZEC = thirdRankTensoreh.jason_data['ZEC']
        filename1 = thirdRankTensoreh.jason_data['filename1']
        surfacecolor = thirdRankTensoreh.jason_data['surfacecolor']

    else:
        thirdRankTensoreh.SingleCrystalAndPoly()
        XEC = thirdRankTensoreh.jason_data['XEC']
        YEC = thirdRankTensoreh.jason_data['YEC']
        ZEC = thirdRankTensoreh.jason_data['ZEC']
        filename1 = thirdRankTensoreh.jason_data['filename1'] 
        surfacecolor = thirdRankTensoreh.jason_data['surfacecolor']

        XECp = thirdRankTensoreh.jason_data_poly['XEC']
        YECp = thirdRankTensoreh.jason_data_poly['YEC']
        ZECp = thirdRankTensoreh.jason_data_poly['ZEC']
        filename1p = thirdRankTensoreh.jason_data_poly['filename1'] 
        surfacecolorp = thirdRankTensoreh.jason_data_poly['surfacecolor']
        
        #tableHeight = tableHeight  * 2
        tableWidth = tableWidth * 2  

      

    tableWidthHeight = 'height:'+  str(tableHeight) +'px;  width:' +  str(tableWidth) + 'px;'
    divWidthHeight = 'height:'+  str(divHeight) +'px;  width:' +  str(divWidth) + 'px;'
    
    colorscale = thirdRankTensoreh.colorscale
 
    if thirdRankTensoreh.res == 1:
        resolutionTag = "Low"
    elif thirdRankTensoreh.res == 2:
        resolutionTag = "Middle"
    elif thirdRankTensoreh.res == 3:
        resolutionTag = "High"
        

    return render_to_response('thirdranktensor.html',{"XEC": XEC,
                                                                                                  "YEC": YEC,
                                                                                                   "ZEC": ZEC,
                                                                                                   "filename1":filename1,
                                                                                                   'colorscale':colorscale,
                                                                                                   'surfacecolor':surfacecolor,
                                                                                                   "XECp": XECp,
                                                                                                  "YECp": YECp,
                                                                                                   "ZECp": ZECp,
                                                                                                   "filename1p":filename1p, 
                                                                                                   'surfacecolorp':surfacecolorp,                                                                                          
                                                                                                   "resolutionTag":resolutionTag,
                                                                                                    "tableWidth": tableWidth,
                                                                                                    "tableHeight": tableHeight,
                                                                                                    "divWidth" : divWidth,
                                                                                                    "divHeight" : divHeight,          
                                                                                                    "tableWidthHeight": tableWidthHeight,
                                                                                                    "divWidthHeight": divWidthHeight,
                                                                                                    "layoutHeight":layoutHeight,
                                                                                                      "layoutWeight":layoutWeight,                                                                                 
                                                                                                  }, context_instance=RequestContext(request))

def viewcompliance(request):
    elasticity = Elasticity(request.GET)
     
    XEC = None
    YEC = None
    ZEC = None
    youngModulusXEC = None
    youngModulusYEC = None
    youngModulusZEC = None
    filename1 = None
    filenameYoungModulus = None  
    surfacecolor = None
    surfacecolorYoungModulus = None
    colorscale = None
    
    XECp = None
    YECp = None
    ZECp = None
    youngModulusXECp = None
    youngModulusYECp = None
    youngModulusZECp = None
    filename1p = None
    filenameYoungModulusp = None  
    surfacecolorp = None
    surfacecolorYoungModulusp = None
    resolutionTag = ""
    tableWidth = 450
    tableHeight = 500
    divWidth = 450
    divHeight = 450 
    layoutHeight = 450
    layoutWeight = 450
    tableWidthHeight = ""
    divWidthHeight = ""
 
    resolutionTag = ""
    if elasticity.valuearrayrotated == None:
        elasticity.ComplianceAndYoungModulus()
        XEC = elasticity.jason_data['XEC']
        YEC = elasticity.jason_data['YEC']
        ZEC = elasticity.jason_data['ZEC']
        youngModulusXEC = elasticity.jason_data['youngModulusXEC']
        youngModulusYEC = elasticity.jason_data['youngModulusYEC']
        youngModulusZEC = elasticity.jason_data['youngModulusZEC']
        filename1 = elasticity.jason_data['filename1']
        #filename2 = elasticity.jason_data['filename1']
        filenameYoungModulus = elasticity.jason_data['filenameYoungModulus']
        surfacecolor = elasticity.jason_data['surfacecolor']
        surfacecolorYoungModulus = elasticity.jason_data['surfacecolorYoungModulus']
        colorscale = elasticity.colorscale
 
    else:
        elasticity.ComplianceAndYoungModulusAndPoly()
        XEC = elasticity.jason_data['XEC']
        YEC = elasticity.jason_data['YEC']
        ZEC = elasticity.jason_data['ZEC']
        youngModulusXEC = elasticity.jason_data['youngModulusXEC']
        youngModulusYEC = elasticity.jason_data['youngModulusYEC']
        youngModulusZEC = elasticity.jason_data['youngModulusZEC']
        filename1 = elasticity.jason_data['filename1']
        #filename2 = elasticity.jason_data['filename1']
        filenameYoungModulus = elasticity.jason_data['filenameYoungModulus']
        surfacecolor = elasticity.jason_data['surfacecolor']
        surfacecolorYoungModulus = elasticity.jason_data['surfacecolorYoungModulus']
        
        XECp = elasticity.jason_data_poly['XEC']
        YECp = elasticity.jason_data_poly['YEC']
        ZECp = elasticity.jason_data_poly['ZEC']
        youngModulusXECp = elasticity.jason_data_poly['youngModulusXEC']
        youngModulusYECp = elasticity.jason_data_poly['youngModulusYEC']
        youngModulusZECp = elasticity.jason_data_poly['youngModulusZEC']
        filename1p = elasticity.jason_data_poly['filename1']
        #filename2 = elasticity.jason_data['filename1']
        filenameYoungModulusp = elasticity.jason_data_poly['filenameYoungModulus']
        surfacecolorp = elasticity.jason_data_poly['surfacecolor']
        surfacecolorYoungModulusp = elasticity.jason_data_poly['surfacecolorYoungModulus']
        
        
        tableHeight = tableHeight  * 2
       
 
    
    tableWidth = tableWidth * 2        
    tableWidthHeight = 'height:'+  str(tableHeight) +'px;  width:' +  str(tableWidth) + 'px;'
    divWidthHeight = 'height:'+  str(divHeight) +'px;  width:' +  str(divWidth) + 'px;'
        
    colorscale = elasticity.colorscale
    if elasticity.res == 1:
        resolutionTag = "Low"
    elif elasticity.res == 2:
        resolutionTag = "Middle"
    elif elasticity.res == 3:
        resolutionTag = "High"
    

    return render_to_response('compliance.html',{"XEC": XEC,
                                                                                          "YEC":YEC,
                                                                                          "ZEC": ZEC,
                                                                                          "youngModulusXEC": youngModulusXEC,
                                                                                          "youngModulusYEC": youngModulusYEC,
                                                                                          "youngModulusZEC": youngModulusZEC,
                                                                                          "resolutionFileName":filename1,
                                                                                          "filenameYoungModulus":filenameYoungModulus,
                                                                                          "surfacecolor":surfacecolor,
                                                                                          "surfacecolorYoungModulus":surfacecolorYoungModulus,
                                                                                          "XECp": XECp,
                                                                                          "YECp":YECp,
                                                                                          "ZECp": ZECp,
                                                                                          "youngModulusXECp": youngModulusXECp,
                                                                                          "youngModulusYECp": youngModulusYECp,
                                                                                          "youngModulusZECp": youngModulusZECp,
                                                                                          "resolutionFileNamep":filename1p,
                                                                                          "filenameYoungModulusp":filenameYoungModulusp,
                                                                                          "surfacecolorp":surfacecolorp,
                                                                                          "surfacecolorYoungModulusp":surfacecolorYoungModulusp,
                                                                                          "colorscale":colorscale,
                                                                                          "resolutionTag":resolutionTag,
                                                                                          "tableWidth": tableWidth,
                                                                                          "tableHeight": tableHeight,
                                                                                          "divWidth" : divWidth,
                                                                                          "divHeight" : divHeight,          
                                                                                          "tableWidthHeight": tableWidthHeight,
                                                                                          "divWidthHeight": divWidthHeight,
                                                                                          "layoutHeight":layoutHeight,
                                                                                          "layoutWeight":layoutWeight,      }, context_instance=RequestContext(request))
        #return render_to_response('compliance.html', context_instance=RequestContext(request))
def viewstiffness(request):
    elasticity = Elasticity(request.GET)
     
    XEC = None
    YEC = None
    ZEC = None
    youngModulusXEC = None
    youngModulusYEC = None
    youngModulusZEC = None
    filename1 = None
    filenameYoungModulus = None  
    surfacecolor = None
    surfacecolorYoungModulus = None
    colorscale = None    
    XECp = None
    YECp = None
    ZECp = None
    youngModulusXECp = None
    youngModulusYECp = None
    youngModulusZECp = None
    filename1p = None
    filenameYoungModulusp = None  
    surfacecolorp = None
    surfacecolorYoungModulusp = None
    error = None
    errorp = None
    resolutionTag = ""
    tableWidth = 450
    tableHeight = 500
    divWidth = 450
    divHeight = 450 
    layoutHeight = 450
    layoutWeight = 450
    tableWidthHeight = ""
    divWidthHeight = ""
    
    
    if elasticity.valuearrayrotated == None:
        elasticity.StiffnessAndYoungModulus()
        if elasticity.jason_data['error'] == None:
            XEC = elasticity.jason_data['XEC']
            YEC = elasticity.jason_data['YEC']
            ZEC = elasticity.jason_data['ZEC']
            youngModulusXEC = elasticity.jason_data['youngModulusXEC']
            youngModulusYEC = elasticity.jason_data['youngModulusYEC']
            youngModulusZEC = elasticity.jason_data['youngModulusZEC']
            filename1 = elasticity.jason_data['filename1']
            #filename2 = elasticity.jason_data['filename1']
            filenameYoungModulus = elasticity.jason_data['filenameYoungModulus']
            surfacecolor = elasticity.jason_data['surfacecolor']
            surfacecolorYoungModulus = elasticity.jason_data['surfacecolorYoungModulus']
            colorscale = elasticity.colorscale
 
        else:
            error = elasticity.jason_data['error'] 

        

                
    else:
        elasticity.StiffnessAndYoungModulusAndPoly()
        if elasticity.jason_data['error'] == None:
            XEC = elasticity.jason_data['XEC']
            YEC = elasticity.jason_data['YEC']
            ZEC = elasticity.jason_data['ZEC']
            youngModulusXEC = elasticity.jason_data['youngModulusXEC']
            youngModulusYEC = elasticity.jason_data['youngModulusYEC']
            youngModulusZEC = elasticity.jason_data['youngModulusZEC']
            filename1 = elasticity.jason_data['filename1']
            #filename2 = elasticity.jason_data['filename1']
            filenameYoungModulus = elasticity.jason_data['filenameYoungModulus']
            surfacecolor = elasticity.jason_data['surfacecolor']
            surfacecolorYoungModulus = elasticity.jason_data['surfacecolorYoungModulus']
 
            
            if elasticity.jason_data_poly['error'] == None:
                XECp = elasticity.jason_data_poly['XEC']
                YECp = elasticity.jason_data_poly['YEC']
                ZECp = elasticity.jason_data_poly['ZEC']
                youngModulusXECp = elasticity.jason_data_poly['youngModulusXEC']
                youngModulusYECp = elasticity.jason_data_poly['youngModulusYEC']
                youngModulusZECp = elasticity.jason_data_poly['youngModulusZEC']
                filename1p = elasticity.jason_data_poly['filename1']
                #filename2 = elasticity.jason_data['filename1']
                filenameYoungModulusp = elasticity.jason_data_poly['filenameYoungModulus']
                surfacecolorp = elasticity.jason_data_poly['surfacecolor']
                surfacecolorYoungModulusp = elasticity.jason_data_poly['surfacecolorYoungModulus']
            else:
                errorp = elasticity.jason_data['error']     
        else:
            error = elasticity.jason_data['error']     
            
        tableHeight = tableHeight  * 2
       
 
    
    tableWidth = tableWidth * 2        
    tableWidthHeight = 'height:'+  str(tableHeight) +'px;  width:' +  str(tableWidth) + 'px;'
    divWidthHeight = 'height:'+  str(divHeight) +'px;  width:' +  str(divWidth) + 'px;'
    
    colorscale = elasticity.colorscale
 
    if elasticity.res == 1:
        resolutionTag = "Low"
    elif elasticity.res == 2:
        resolutionTag = "Middle"
    elif elasticity.res == 3:
        resolutionTag = "High"
    

    return render_to_response('stiffness.html',{"XEC": XEC,
                                                                                          "YEC":YEC,
                                                                                          "ZEC": ZEC,
                                                                                          "youngModulusXEC": youngModulusXEC,
                                                                                          "youngModulusYEC": youngModulusYEC,
                                                                                          "youngModulusZEC": youngModulusZEC,
                                                                                          "resolutionFileName":filename1,
                                                                                          "filenameYoungModulus":filenameYoungModulus,
                                                                                          "surfacecolor":surfacecolor,
                                                                                          "surfacecolorYoungModulus":surfacecolorYoungModulus,
                                                                                          "error":error,
                                                                                          "XECp": XECp,
                                                                                          "YECp":YECp,
                                                                                          "ZECp": ZECp,
                                                                                          "youngModulusXECp": youngModulusXECp,
                                                                                          "youngModulusYECp": youngModulusYECp,
                                                                                          "youngModulusZECp": youngModulusZECp,
                                                                                          "resolutionFileNamep":filename1p,
                                                                                          "filenameYoungModulusp":filenameYoungModulusp,
                                                                                          "surfacecolorp":surfacecolorp,
                                                                                          "surfacecolorYoungModulusp":surfacecolorYoungModulusp,
                                                                                          "errorp":errorp,
                                                                                          "colorscale":colorscale,
                                                                                          "resolutionTag":resolutionTag,
                                                                                          "tableWidth": tableWidth,
                                                                                          "tableHeight": tableHeight,
                                                                                          "divWidth" : divWidth,
                                                                                          "divHeight" : divHeight,          
                                                                                          "tableWidthHeight": tableWidthHeight,
                                                                                          "divWidthHeight": divWidthHeight,
                                                                                          "layoutHeight":layoutHeight,
                                                                                          "layoutWeight":layoutWeight,      }, context_instance=RequestContext(request))
    
    


def viewfourthranktensor(request):
    fourthRankTensor = FourthRankTensor(request.GET)

    XEC = None
    YEC = None
    ZEC = None
    filename1 = None
    surfacecolor = None
    colorscalep = None
    colorscale = None
    surfacecolorp = None
    XECp = None
    YECp = None
    ZECp = None
    filename1p = None
  
    tableWidth = 450
    tableHeight = 500
    divWidth = 450
    divHeight = 450 
    layoutHeight = 450
    layoutWeight = 450
    tableWidthHeight = ""
    divWidthHeight = ""
 
    resolutionTag = ""
    if fourthRankTensor.valuearrayrotated == None:
        fourthRankTensor.SingleCrystal()        
        XEC = fourthRankTensor.jason_data['XEC']
        YEC = fourthRankTensor.jason_data['YEC']
        ZEC = fourthRankTensor.jason_data['ZEC']
        filename1 = fourthRankTensor.jason_data['filename1']
        surfacecolor = fourthRankTensor.jason_data['surfacecolor']

    else:
        fourthRankTensor.SingleCrystalAndPoly()
        XEC = fourthRankTensor.jason_data['XEC']
        YEC = fourthRankTensor.jason_data['YEC']
        ZEC = fourthRankTensor.jason_data['ZEC']
        filename1 = fourthRankTensor.jason_data['filename1'] 
        surfacecolor = fourthRankTensor.jason_data['surfacecolor']

        XECp = fourthRankTensor.jason_data_poly['XEC']
        YECp = fourthRankTensor.jason_data_poly['YEC']
        ZECp = fourthRankTensor.jason_data_poly['ZEC']
        filename1p = fourthRankTensor.jason_data_poly['filename1']
        surfacecolorp = fourthRankTensor.jason_data_poly['surfacecolor']
        tableWidth = tableWidth * 2 
    
    
    
    tableWidthHeight = 'height:'+  str(tableHeight) +'px;  width:' +  str(tableWidth) + 'px;'
    divWidthHeight = 'height:'+  str(divHeight) +'px;  width:' +  str(divWidth) + 'px;'
    
    colorscale = fourthRankTensor.colorscale
 
    if fourthRankTensor.res == 1:
        resolutionTag = "Low"
    elif fourthRankTensor.res == 2:
        resolutionTag = "Middle"
    elif fourthRankTensor.res == 3:
        resolutionTag = "High"
    
 
                        
    return render_to_response('fourthranktensor.html',{"XEC": XEC,
                                                                                                  "YEC": YEC,
                                                                                                   "ZEC": ZEC,
                                                                                                   "filename1":filename1,
                                                                                                   'colorscale':colorscale,
                                                                                                   'surfacecolor':surfacecolor,
                                                                                                   "XECp": XECp,
                                                                                                  "YECp": YECp,
                                                                                                   "ZECp": ZECp,
                                                                                                   "filename1p":filename1p,
                                                                                                   'surfacecolorp':surfacecolorp,
                                                                                                   "resolutionTag":resolutionTag,
                                                                                                    "tableWidth": tableWidth,
                                                                                                    "tableHeight": tableHeight,
                                                                                                    "divWidth" : divWidth,
                                                                                                    "divHeight" : divHeight,          
                                                                                                    "tableWidthHeight": tableWidthHeight,
                                                                                                    "divWidthHeight": divWidthHeight,
                                                                                                    "layoutHeight":layoutHeight,
                                                                                                      "layoutWeight":layoutWeight,                                                                                 
                                                                                                  }, context_instance=RequestContext(request))
        
def viewmagnetocrystallineanisotropy(request):
    """value1 = (request.GET.get('value1', ''))
        value2 = (request.GET.get('value2', ''))
        filename = (request.GET.get('filename', ''))
        color = (request.GET.get('color', ''))
        filename = (request.GET.get('filename', ''))
        promertyname=(request.GET.get('promertyname', ''))
        if(value1 and value2 and color):
            val1 = float(value1)
            val2 = float(value2)
        
        color = int(color)
        if color == 0:
            colorscale='Jet';
        elif color == 1:
            colorscale='Hot';
        elif color == 2:
            colorscale='Cool'
        elif color == 3:
            colorscale='Greys';
            
        filename = re.sub('[\s+]', '', filename)

        magneto =  Magneto();
        
        
        pathslist=Path.objects.all()      
        pathexist = 0
        stl_dir=''
        for stldir in pathslist:
            path=Path() 
            path = stldir
            if os.path.isdir(path.stl_dir): 
                pathexist = 1
                stl_dir= path.stl_dir
                break

        filename1 = filename+"MagneticLowResolution" + ".stl"
        filepath=os.path.join(stl_dir, filename1)
        res=1;
        createstl = 0;
        if pathexist == 1:
            if os.path.isfile(filepath):
                createstl = 0          
            else:
                createstl = 1
      
        createdata =  1
        

        magneto.MagnetocrystallineAnisotropy(val1, val2, color, filename1, res, stl_dir, createstl, createdata);
        
        XEC=magneto.stringValsOfXEC
        YEC = magneto.stringValsOfYEC
        ZEC= magneto.stringValsOfZEC
        surfacecolorMagnetic=magneto.surfacecolorMagneticAnisotropy
        del magneto
        
        filename2 = filename+"MagneticMiddleResolution" + ".stl"
        

        #filename = "ejemplo"+str(ejemplo)+"R4MidleResolution" + ".stl"
        res=2;
        filepath=os.path.join(stl_dir, filename2)       
        createstl = 0;
        if pathexist == 1:
            if os.path.isfile(filepath):
                createstl = 0          
            else:
                createstl = 1
      
        if createstl == 1:
            createdata =  0     
            magneto = Magneto()
            magneto.MagnetocrystallineAnisotropy(val1, val2, color, filename2, res, stl_dir, createstl, createdata);
            
            del magneto 
    
        return render_to_response('magneto.html',{"XEC": XEC,"YEC":YEC,"ZEC": ZEC,"LowResolutionFileName":filename1,"MiddleResolutionFileName":filename2,'promertyname':promertyname,'colorscale':colorscale,'surfacecolorMagnetic':surfacecolorMagnetic}, context_instance=RequestContext(request))
    """
    magnetoCrystallineAnisotropy = MagnetoCrystallineAnisotropy(request.GET)

    XEC = None
    YEC = None
    ZEC = None
    filename1 = None
    surfacecolor = None
    colorscale = None
    colorscalep = None
    surfacecolorp = None
    XECp = None
    YECp = None
    ZECp = None
    filename1p = None
  
    tableWidth = 450
    tableHeight = 500
    divWidth = 450
    divHeight = 450 
    layoutHeight = 450
    layoutWeight = 450
    tableWidthHeight = ""
    divWidthHeight = ""
 
    resolutionTag = ""
    if magnetoCrystallineAnisotropy.valuearrayrotated == None:
        magnetoCrystallineAnisotropy.SingleCrystal()        
        XEC = magnetoCrystallineAnisotropy.jason_data['XEC']
        YEC = magnetoCrystallineAnisotropy.jason_data['YEC']
        ZEC = magnetoCrystallineAnisotropy.jason_data['ZEC']
        filename1 = magnetoCrystallineAnisotropy.jason_data['filename1']
        surfacecolor = magnetoCrystallineAnisotropy.jason_data['surfacecolor']

    else:
        magnetoCrystallineAnisotropy.SingleCrystalAndPoly()
        XEC = magnetoCrystallineAnisotropy.jason_data['XEC']
        YEC = magnetoCrystallineAnisotropy.jason_data['YEC']
        ZEC = magnetoCrystallineAnisotropy.jason_data['ZEC']
        filename1 = magnetoCrystallineAnisotropy.jason_data['filename1'] 
        surfacecolor = magnetoCrystallineAnisotropy.jason_data['surfacecolor']

        XECp = magnetoCrystallineAnisotropy.jason_data_poly['XEC']
        YECp = magnetoCrystallineAnisotropy.jason_data_poly['YEC']
        ZECp = magnetoCrystallineAnisotropy.jason_data_poly['ZEC']
        filename1p = magnetoCrystallineAnisotropy.jason_data_poly['filename1'] 
        surfacecolorp = magnetoCrystallineAnisotropy.jason_data_poly['surfacecolor']
        
        #tableHeight = tableHeight  * 2
        tableWidth = tableWidth * 2
       
 
    
        

    tableWidthHeight = 'height:'+  str(tableHeight) +'px;  width:' +  str(tableWidth) + 'px;'
    divWidthHeight = 'height:'+  str(divHeight) +'px;  width:' +  str(divWidth) + 'px;'
    
    colorscale = magnetoCrystallineAnisotropy.colorscale
 
    if magnetoCrystallineAnisotropy.res == 1:
        resolutionTag = "Low"
    elif magnetoCrystallineAnisotropy.res == 2:
        resolutionTag = "Middle"
    elif magnetoCrystallineAnisotropy.res == 3:
        resolutionTag = "High"
        

    return render_to_response('magneto.html',{"XEC": XEC,
                                                                                                  "YEC": YEC,
                                                                                                   "ZEC": ZEC,
                                                                                                   "filename1":filename1,
                                                                                                   'colorscale':colorscale,
                                                                                                   'surfacecolor':surfacecolor,
                                                                                                   "XECp": XECp,
                                                                                                  "YECp": YECp,
                                                                                                   "ZECp": ZECp,
                                                                                                   "filename1p":filename1p, 
                                                                                                   'surfacecolorp':surfacecolorp,                                                                                          
                                                                                                   "resolutionTag":resolutionTag,
                                                                                                    "tableWidth": tableWidth,
                                                                                                    "tableHeight": tableHeight,
                                                                                                    "divWidth" : divWidth,
                                                                                                    "divHeight" : divHeight,          
                                                                                                    "tableWidthHeight": tableWidthHeight,
                                                                                                    "divWidthHeight": divWidthHeight,
                                                                                                    "layoutHeight":layoutHeight,
                                                                                                      "layoutWeight":layoutWeight,                                                                                 
                                                                                                  }, context_instance=RequestContext(request))
    
def viewmagnetostriction(request):
    
    
    """value1 = (request.GET.get('value1', ''))
        value2 = (request.GET.get('value2', ''))
        filename = (request.GET.get('filename', ''))
        color = (request.GET.get('color', ''))
        filename = (request.GET.get('filename', ''))
        promertyname=(request.GET.get('promertyname', ''))
        if(value1 and value2 and color):
            val1 = float(value1)
            val2 = float(value2)
        
        color = int(color)
        if color == 0:
            colorscale='Jet';
        elif color == 1:
            colorscale='Hot';
        elif color == 2:
            colorscale='Cool'
        elif color == 3:
            colorscale='Greys';
            
        filename = re.sub('[\s+]', '', filename)

        magneto =  Magneto();
        
        pathslist=Path.objects.all()      
        pathexist = 0
        stl_dir=''
        for stldir in pathslist:
            path=Path() 
            path = stldir
            if os.path.isdir(path.stl_dir): 
                pathexist = 1
                stl_dir= path.stl_dir
                break

             

                 
        filename1 = filename+"MagnetoLowResolution" + ".stl"
        filepath=os.path.join(stl_dir, filename1)
        res=1;
        createstl = 0;
        if pathexist == 1:
            if os.path.isfile(filepath):
                createstl = 0          
            else:
                createstl = 1
      
        createdata =  1
        
        ''' if(promertyname=="Magnetostriction")                                              
        if(promertyname=="Magnetocrystalline Anisotropy")'''
        

        magneto.MagnetoStriction(val1, val2, color, filename1, res, stl_dir, createstl, createdata);
        
        XEC=magneto.stringValsOfXEC
        YEC = magneto.stringValsOfYEC
        ZEC= magneto.stringValsOfZEC
        surfacecolorMagnetic=magneto.surfacecolorMagnetostriction
        del magneto
        
        filename2 = filename+"MagnetoMiddleResolution" + ".stl"
            
        res=2;
        filepath=os.path.join(stl_dir, filename2)       
        createstl = 0;
        if pathexist == 1:
            if os.path.isfile(filepath):
                createstl = 0          
            else:
                createstl = 1
      
        if createstl == 1:
            createdata =  0     
            magneto = Magneto()
            magneto.MagnetoStriction(val1, val2, color, filename2, res, stl_dir, createstl, createdata);            
            del magneto 
            
            
            
    
        return render_to_response('magneto.html',{"XEC": XEC,"YEC":YEC,"ZEC": ZEC,"LowResolutionFileName":filename1,"MiddleResolutionFileName":filename2,'promertyname':promertyname,'colorscale':colorscale,'surfacecolorMagnetic':surfacecolorMagnetic}, context_instance=RequestContext(request))
    """
    magnetostriction = Magnetostriction(request.GET)

    XEC = None
    YEC = None
    ZEC = None
    filename1 = None
    surfacecolor = None
    colorscale = None
    colorscalep = None
    surfacecolorp = None
    XECp = None
    YECp = None
    ZECp = None
    filename1p = None
  
    tableWidth = 450
    tableHeight = 500
    divWidth = 450
    divHeight = 450 
    layoutHeight = 450
    layoutWeight = 450
    tableWidthHeight = ""
    divWidthHeight = ""
 
    resolutionTag = ""
    if magnetostriction.valuearrayrotated == None:
        magnetostriction.SingleCrystal()        
        XEC = magnetostriction.jason_data['XEC']
        YEC = magnetostriction.jason_data['YEC']
        ZEC = magnetostriction.jason_data['ZEC']
        filename1 = magnetostriction.jason_data['filename1']
        surfacecolor = magnetostriction.jason_data['surfacecolor']

    else:
        magnetostriction.SingleCrystalAndPoly()
        XEC = magnetostriction.jason_data['XEC']
        YEC = magnetostriction.jason_data['YEC']
        ZEC = magnetostriction.jason_data['ZEC']
        filename1 = magnetostriction.jason_data['filename1'] 
        surfacecolor = magnetostriction.jason_data['surfacecolor']

        XECp = magnetostriction.jason_data_poly['XEC']
        YECp = magnetostriction.jason_data_poly['YEC']
        ZECp = magnetostriction.jason_data_poly['ZEC']
        filename1p = magnetostriction.jason_data_poly['filename1'] 
        surfacecolorp = magnetostriction.jason_data_poly['surfacecolor']
        
        #tableHeight = tableHeight  * 2
        tableWidth = tableWidth * 2 
 
    
       

    tableWidthHeight = 'height:'+  str(tableHeight) +'px;  width:' +  str(tableWidth) + 'px;'
    divWidthHeight = 'height:'+  str(divHeight) +'px;  width:' +  str(divWidth) + 'px;'
    
    colorscale = magnetostriction.colorscale
 
    if magnetostriction.res == 1:
        resolutionTag = "Low"
    elif magnetostriction.res == 2:
        resolutionTag = "Middle"
    elif magnetostriction.res == 3:
        resolutionTag = "High"
        

    return render_to_response('magnetostriction.html',{"XEC": XEC,
                                                                                                  "YEC": YEC,
                                                                                                   "ZEC": ZEC,
                                                                                                   "filename1":filename1,
                                                                                                   'colorscale':colorscale,
                                                                                                   'surfacecolor':surfacecolor,
                                                                                                   "XECp": XECp,
                                                                                                  "YECp": YECp,
                                                                                                   "ZECp": ZECp,
                                                                                                   "filename1p":filename1p, 
                                                                                                   'surfacecolorp':surfacecolorp,                                                                                          
                                                                                                   "resolutionTag":resolutionTag,
                                                                                                    "tableWidth": tableWidth,
                                                                                                    "tableHeight": tableHeight,
                                                                                                    "divWidth" : divWidth,
                                                                                                    "divHeight" : divHeight,          
                                                                                                    "tableWidthHeight": tableWidthHeight,
                                                                                                    "divWidthHeight": divWidthHeight,
                                                                                                    "layoutHeight":layoutHeight,
                                                                                                      "layoutWeight":layoutWeight,                                                                                 
                                                                                                  }, context_instance=RequestContext(request))



def get_datafile(request, file_name):
    ext=file_name.split(".")[1]
    
    pathslist=Path.objects.all()      
    pathexist = 0
    for files_path in pathslist:
        path=Path() 
        path = files_path
        if os.path.isdir(path.datafiles_path): 
            pathexist = 1
            datafiles_path= path.datafiles_path
            break
    
    datafile_path=os.path.join(datafiles_path,file_name)
    datafile_data = open(datafile_path, "rb").read()
    return HttpResponse(datafile_data, mimetype="text")


def viewdatafilecreated2(request, pk):
    print ""
   
    return   render_to_response("account/file_detail.html", context_instance=RequestContext(request))

def viewdatafilecreated3(request, filename):
    ext=filename.split(".")[1]
    
    pathslist=Path.objects.all()      
    pathexist = 0
    for cifstest in pathslist:
        path=Path() 
        path = cifstest
        if os.path.isdir(path.cifs_dir_valids): 
            pathexist = 1
            datafiles_path= path.cifs_dir_valids
            break
    
    datafile_path=os.path.join(datafiles_path,filename)
    datafile_data = open(datafile_path, "rb").read()
    #HttpResponse(datafile_data, mimetype="application/octet-stream")  download
 
    
     
    return HttpResponse(datafile_data, mimetype="text/plain; charset=utf-8")
  
#example http://127.0.0.1:8000/datafilescreated/jnhwfomtxo.mpod
def viewdatafilecreated(request, filename):
    ext=filename.split(".")[1]
    
    pathslist=Path.objects.all()      
    pathexist = 0
    for cifstest in pathslist:
        path=Path() 
        path = cifstest
        if os.path.isdir(path.cifs_dir_valids): 
            pathexist = 1
            datafiles_path= path.cifs_dir_valids
            break
    
    datafile_path=os.path.join(datafiles_path,filename)
    datafile_data = open(datafile_path, "rb").read()
    #HttpResponse(datafile_data, mimetype="application/octet-stream")  download
    return HttpResponse(datafile_data, mimetype="text")


def get_stlfile(request, file_name):
    ext=file_name.split(".")[1]
    pathslist=Path.objects.all()      
    pathexist = 0
    stl_dir=''
    for stldir in pathslist:
        path=Path() 
        path = stldir
        if os.path.isdir(path.stl_dir): 
            pathexist = 1
            stl_dir= path.stl_dir
            break

           
    stlfile_path=os.path.join(stl_dir,file_name)
    #stlfile_path=os.path.join(".\\media\\stlfiles\\",file_name)
    stlfile_path = open(stlfile_path, "rb").read()
    return HttpResponse(stlfile_path, mimetype="application/x-download")

def viewarticle(request, article_id):
    ogge = None
    html_res = None
    html_res2 = None
    datafiles = None
    try:
        ogge = PublArticle.objects.get(id__exact = article_id)
        datafiles = DataFile.objects.filter(publication__id__exact = article_id)
    except:
        pass
    if ogge:
        html_res = view_obj_as_2cols_table ( PublArticle, ogge, cap="Publication details")
        html_res2 = view_as_linked_table(DataFile, oggetti=datafiles, header='Associated datafiles')
    request_path=request.get_full_path()
    debug_info=request_path
    return render_to_response('viewarticle.html', {"publi_table": html_res, "associated_datafiles": html_res2}, context_instance=RequestContext(request))

def viewexparcond(request, exparcond_id):
    request_path=request.get_full_path()
    debug_info=request_path
    ogge = ExperimentalParCond.objects.filter(id__exact = exparcond_id , active=True).distinct()
    html_res = None
    if ogge:
        ogge = ogge[0]
        html_res = view_obj_as_2cols_table (ExperimentalParCond, ogge, cap="Experimental Parameter/Condition details")
    return render_to_response('viewexparcond.html', {"property_table": html_res}, context_instance=RequestContext(request))


def viewdictionarydefinition(request, id):
    request_path=request.get_full_path()
    debug_info=request_path
    ogge = Dictionary.objects.filter(id__exact = id).distinct()
    html_res = None
    if ogge:
        ogge = ogge[0]
        html_res = view_obj_as_2cols_table (Dictionary, ogge, cap="Dictionary definition/ Detail")
         
    return render_to_response('viewdictionary.html', {"property_table": html_res}, context_instance=RequestContext(request))

#-------------------------------------------------------------------------------------------

def get_datafiles(phase_name_q='', formula_q='', mpod_code_q='', cod_code_q='', publ_author_q=''):
    name_set = None
    formula_set = None
    cod_code_set = None
    mpod_code_set = None
    tot_set = None
    res = None
    res_obj = None
    if phase_name_q:
        name_set = (Q(phase_name__icontains=phase_name_q) | Q(phase_generic__icontains=phase_name_q))
        res_obj = DataFile.objects.filter(name_set, active=True)

    if formula_q:
        formula_set = Q(chemical_formula__icontains=formula_q)
        if res_obj:
            res_obj = res_obj.filter(formula_set)
        else:
            res_obj = DataFile.objects.filter(formula_set,active=True)
    
    if publ_author_q:
        author_set = Q(publication__authors__icontains=publ_author_q)
        if res_obj:
            res_obj = res_obj.filter(author_set)
        else:
            res_obj = DataFile.objects.filter(author_set, active=True)

    if mpod_code_q:
        try:
            mpod_code_set = Q(code__icontains = int(mpod_code_q))
            res_obj = DataFile.objects.filter(mpod_code_set, active=True).order_by('code')
        except:
            pass

    if cod_code_q:
        try:
            cod_code_set = Q(cod_code__exact = int(cod_code_q))
            res_obj = DataFile.objects.filter(cod_code_set, active=True).order_by('code')
        except:
            pass
        
    if res_obj:
        html_res = view_as_linked_table(DataFile, oggetti=res_obj)
    else:
        html_res=''
    return html_res

def sbcomposition(request):
    t = get_template('sbcomposition.html')
    request_path=request.get_full_path()
    query_phase_name = request.GET.get('phase_name', '')
    query_formula = request.GET.get('formula', '')
    query_mpod_code = request.GET.get('mpod_code', '')
    query_cod_code = request.GET.get('cod_code', '')
    query_publ_author = request.GET.get('publ_author', '')
    if ( query_phase_name or query_formula or query_mpod_code or query_cod_code or query_publ_author):
        html_results = get_datafiles(query_phase_name, query_formula, query_mpod_code, query_cod_code, query_publ_author)
    else:
        html_results=None
    return render_to_response('sbcomposition.html', {"query_phase_name": query_phase_name, "query_formula": query_formula, "query_code": query_mpod_code, "query_cod_code": query_cod_code, "query_publ_author": query_publ_author, "results": html_results}, context_instance=RequestContext(request))

def get_publis(title_q='', author_q='', journal_q=''):
    title_set = None
    journal_set = None
    author_set = None
    tot_set = None
    res = None
    res_obj = None
    if title_q:
        title_set = Q(title__icontains=title_q)
        res_obj = PublArticle.objects.filter(title_set)
    if author_q:
        author_set = Q(authors__icontains=author_q)
        if res_obj:
            res_obj = res_obj.filter(author_set)
        else:
            res_obj = PublArticle.objects.filter(author_set)
    if journal_q:
        journal_set = Q(journal__icontains=journal_q)
        if res_obj:
            res_obj = res_obj.filter(journal_set)
        else:
            res_obj = PublArticle.objects.filter(journal_set)
    if res_obj:
        html_res = view_linked_articles_list(oggetti=res_obj, header='Found articles')
    else:
        html_res=''
    return html_res

def sbreference(request):
    t = get_template('sbreference.html')
    request_path=request.get_full_path()
    query_title = request.GET.get('title', '')
    query_author = request.GET.get('author', '')
    query_journal = request.GET.get('journal', '')
    if ( query_title or query_author or query_journal):
        html_results = get_publis(query_title, query_author, query_journal)
    else:
        html_results=None
    return render_to_response('sbreference.html', {"query_title": query_title, "query_author": query_author, "query_journal": query_journal, "results": html_results,}, context_instance=RequestContext(request))



def get_catalog_property():
    res_obj = None
    opts = CatalogProperty._meta
    list_obj = CatalogProperty.objects.all()
    field_list = []
    data_lists=[]
    for ii, f in enumerate(opts.fields):       
        if not f.editable or isinstance(f, models.AutoField):
            continue
        field_list.append(format_name(f.name))
        if list_obj:
            data_list=[]
            for obj in list_obj:
                cp = CatalogProperty()
                cp = obj
                cp.name
                #print cp.description
                val = f.value_from_object(obj)
                data_list.append(val)
               
        data_lists.append(data_list)
    return (field_list, zip(*data_lists))

def get_catalog_propertyv2():
    catalogPropertyList = [];
    list_obj = CatalogProperty.objects.filter(active= True)
    for obj in list_obj:
        cp = CatalogProperty()
        cp = obj; 
        #print ccs.description
        catalogPropertyList.append(cp)
        
    return catalogPropertyList
   
def get_catalog_crystal_system():
    catalogCrystalSystemList = [];
    list_obj = CatalogCrystalSystem.objects.all()
    for obj in list_obj:
        ccs = CatalogCrystalSystem()
        ccs = obj; 
        
        #print ccs.description
        catalogCrystalSystemList.append(ccs)
        
    return catalogCrystalSystemList
        
def get_catalog_type():
    typeList = [];
    list_obj = Type.objects.filter(catalog_property_id=1)#filtra porcualquiera de los propiedades de la clase(id,name,description o catalog_property_id) o description__startswith='co'
    for obj in list_obj:
        t = Type
        t = obj
        typeList.append(t) 

    return  typeList





@login_required(login_url="/login")
def newcasev2(request): 
    
       
    if 'inputList' not in request.session  or not request.session['inputList']:
        pass
    else:
        del request.session['inputList']
    
    form= NewCaseFormv2()
    propertyCategoryName=get_catalog_propertyv2();
    if 'propertyCategoryNameListOnSession' not in request.session  or not request.session['propertyCategoryNameListOnSession']:
        request.session['propertyCategoryNameListOnSession']=propertyCategoryName
            
    catalogproperty_name="e"
    catalogproperty_id = 1
    questionAxis=''
    axisList=''
    questionGp=''
    pointGroupList=''
    inputList=''
    questionAxis=''
    message=""
    axisselected_name=""
    
    
    
    catalogCrystalSystemList = [];
    """list_CatalogCrystalSystem= CatalogCrystalSystem.objects.filter(catalogproperty=propertyCategoryName[0],active=True)
    for register_catalogCrystalSystem in list_CatalogCrystalSystem: 
        objCatalogCrystalSystem=CatalogCrystalSystem();
        objCatalogCrystalSystem = register_catalogCrystalSystem
        catalogCrystalSystemList.append(objCatalogCrystalSystem)   
        del objCatalogCrystalSystem
    """
    
        
    
   
    typeList =  [];
   
    list_Type = Type.objects.filter(catalogproperty=propertyCategoryName[0],active=True)
    for register_type in list_Type: 
        objType=Type();
        objType = register_type
        typeList.append(objType)
        del objType
        
    if 'typeListOnSession' not in request.session  or not request.session['typeListOnSession']:
        request.session['typeListOnSession']=typeList
         
    #initialization
    crystalsystem_name= "tc"
    #questiontype =""
    
    #initialization
    typeselected = "c"   
    questiontype = "s (compliance) o c (stiffness)?"    
    questionAxis=''
    axisList =[]
    
    if not 'dataPropertyListOnSession' in request.session or not request.session['dataPropertyListOnSession' ]:  
        pass
    else:
        del request.session['dataPropertyListOnSession']    
        
    
    list_CatalogCrystalSystem= CatalogCrystalSystem.objects.filter(catalogproperty=CatalogProperty.objects.get(name__exact=catalogproperty_name),active=True)
    for i,crystalsystem in enumerate(list_CatalogCrystalSystem): 
        try:
            crystalsystemtype=CrystalSystemType.objects.get(catalogcrystalsystem=crystalsystem,type=Type.objects.filter(active=True, name=typeselected),active=True)
            catalogCrystalSystemList.append(crystalsystemtype.catalogcrystalsystem)
        except ObjectDoesNotExist as error:
                print "Message({0}): {1}".format(99, error.message) 
        
    if 'catalogCrystalSystemListOnSession' not in request.session  or not request.session['catalogCrystalSystemListOnSession']:
        request.session['catalogCrystalSystemListOnSession']=catalogCrystalSystemList
     
    ids=CatalogProperty.objects.filter(active=True,name=catalogproperty_name).values_list('id', flat=True)    
    type_ids=Type.objects.filter(catalogproperty_id__in=ids,active=True, name=typeselected).values_list('id',flat=True)    
    data_property_ids=TypeDataProperty.objects.filter(type_id__in=type_ids).values_list('dataproperty_id',flat=True)    
    dataPropertyList=Property.objects.filter(id__in=data_property_ids,active=True)
    request.session['dataPropertyListOnSession']=dataPropertyList
    property=Property()
    property = dataPropertyList[0] 
    datapropertytagselected = property.id
    
    #initialization
    ShowBtnSend = 1
    ShowBtnProcess = 0
    ShowBtnSave = 0
    
 
    validationbyform = 0
    
    
    lengthlist = 0
    if not 'propertySessionList' in request.session or not request.session['propertySessionList' ]:  
        pass
    else:
        del request.session['propertySessionList']    
 
        
       
    dictionaryList=[]
    dictionaryQuerySet= Dictionary.objects.filter(category = Category.objects.get(pk=9), deploy = 1)
    for dictionary in dictionaryQuerySet: 
        objDictionary =Dictionary();
        objDictionary = dictionary
        dictionaryList.append(objDictionary)
        del objDictionary
        
        
    dictionaryPhaseList=[]
    dictionaryPhaseQuerySet1= Dictionary.objects.filter(category = Category.objects.get(pk=4), deploy = 1)
    dictionaryPhaseQuerySet2= Dictionary.objects.filter(category = Category.objects.get(pk=8), deploy = 1)
    dictionaryPhaseQuerySet= (dictionaryPhaseQuerySet1 | dictionaryPhaseQuerySet2).distinct()
    for dictionary in dictionaryPhaseQuerySet: 
        objDictionary =Dictionary();
        objDictionary = dictionary
        dictionaryPhaseList.append(objDictionary)
        del objDictionary 
        
    dictionaryPhaseCharacteristicList=[]
    dictionaryPhaseCharacteristicQuerySet= Dictionary.objects.filter(category = Category.objects.get(pk=11), deploy = 1)
    for dictionary in dictionaryPhaseCharacteristicQuerySet: 
        objDictionary =Dictionary();
        objDictionary = dictionary
        dictionaryPhaseCharacteristicList.append(objDictionary)
        del objDictionary     
        
        
    dictionaryMeasurementList=[]
    dictionaryMeasurementQuerySet= Dictionary.objects.filter(category = Category.objects.get(pk=12), deploy = 1)
    for dictionary in dictionaryMeasurementQuerySet: 
        objDictionary =Dictionary();
        objDictionary = dictionary
        dictionaryMeasurementList.append(objDictionary)
        del objDictionary     
 
    
     
    if 'dictionaryValues'  not  in request.session  or not request.session['dictionaryValues']:
        pass
    else:
        del  request.session['dictionaryValues']
        
        
    if 'newDictionaryList' not in request.session  or not request.session['newDictionaryList']:
        pass
    else:
        del  request.session['newDictionaryList']   
         

        
    if 'dictionaryList' not in request.session  or not request.session['dictionaryList']:
        request.session['dictionaryList']=dictionaryList   
        
    if 'dictionaryPhaseList' not in request.session  or not request.session['dictionaryPhaseList']:
        request.session['dictionaryPhaseList']=dictionaryPhaseList   
        
    #if 'dictionaryPhaseCharacteristicList' not in request.session  or not request.session['dictionaryCharacteristicPhaseList']:
    #    request.session['dictionaryPhaseCharacteristicList']=dictionaryPhaseCharacteristicList   
        
        
    if not 'propertyMaster' in request.session or not request.session['propertyMaster' ]:  
        pass
    else:
        del  request.session['propertyMaster']   
            
    
    current ="New Case"
            
    return render_to_response('newcasev2.html', {"form":form,
                                                                                         "propertyCategoryName":propertyCategoryName,
                                                                                         "catalogCrystalSystemList":catalogCrystalSystemList,
                                                                                         "typeList":typeList,
                                                                                         "axisList":axisList,
                                                                                         "questionAxis":questionAxis,
                                                                                         "crystalsystem_name":crystalsystem_name,
                                                                                         "questiontype":questiontype,
                                                                                         "typeselected":typeselected,
                                                                                         "ShowBtnSend":ShowBtnSend,
                                                                                         "ShowBtnProcess":ShowBtnProcess,
                                                                                         "ShowBtnSave":ShowBtnSave,
                                                                                         "validationbyform":validationbyform,
                                                                                         "current":current,
                                                                                         "lengthlist":lengthlist,
                                                                                         "dictionaryMeasurementList":dictionaryMeasurementList,
                                                                                         "dictionaryList":dictionaryList,
                                                                                         "dictionaryPhaseList":dictionaryPhaseList,
                                                                                         "dictionaryPhaseCharacteristicList":dictionaryPhaseCharacteristicList,
                                                                                         #"experimentalparcond_name_selected":experimentalparcond_name_selected,
                                                                                         "list_Type":list_Type,
                                                                                         'dataPropertyList':dataPropertyList,
                                                                                         'datapropertytagselected':datapropertytagselected
                                                                                         }, context_instance=RequestContext(request))
    
    
    
    
@login_required
@csrf_exempt 
def onhold(request,todo,index): 
    #todo = request.POST.get('todo', False)
    propertySessionList=[]
    response =None
    current ="On Hold"
    sizelist = 0;
    message = ""
    
    if todo == 'show' and int(index) == -2 :
        if not 'propertyMaster' in request.session or not request.session['propertyMaster']:
            pass
        elif  'propertyMaster' in request.session or  request.session['propertyMaster']:
            propertyMasterSession = request.session['propertyMaster']
            print "show "
            
            
            
    
    if todo == 'remove' and int(index)  > 0:
        if  'propertyMaster' in request.session or  request.session['propertyMaster']:
            propertyMaster = request.session['propertyMaster']
            
            try:
                print "remove: " + index
                #print propertySessionList[int(index)-1]
                del propertyMaster.propertyList[int(index)-1]       
                sizelist = len(propertyMaster.propertyList)
                if sizelist==0:
                    propertyMaster.pointgroup = None
                    
                request.session['propertyMaster']=propertyMaster    
                   
                data = {
                'tblProperty': "tblProperty" + str(index),
                'sizelist':  str(sizelist),
                'error' : ''
                } 
                
                response =  HttpResponse(json.dumps(data), content_type="application/json")          
                
            except ValueError:
                pass  
            
    if todo == 'removeall' and int(index)  == -1 :
        if  'propertyMaster' in request.session or  request.session['propertyMaster']:
                propertyMaster = request.session['propertyMaster']
      
                try:
                    print "removeall "
                    sizelist = len(propertyMaster.propertyList)
                    #del request.session['propertyMaster']     
                    propertyMaster.propertyList = []
                    
                    propertyMaster.pointgroup = None
                    request.session['propertyMaster'] = propertyMaster
                    data = {
                        'tblProperty': "tblProperty",
                        'sizelist':  str(sizelist),
                        'error' : ''
                        } 
                        
                    response =  HttpResponse(json.dumps(data), content_type="application/json")       
                except ValueError:
                    pass  
        
 
        
                
    if todo == 'save' and  int(index) == -2:
        if not 'propertyMaster' in request.session or not request.session['propertyMaster']:
            #propertySessionList=[]
            pass
        elif  'propertyMaster' in request.session or  request.session['propertyMaster']:
                propertyMaster = request.session['propertyMaster']
                #propertySessionList = propertyMaster.propertyList
                if len(propertyMaster.propertyList)  > 0:
                    try:
                        name_str = lambda n: ''.join([random.choice(string.lowercase) for i in xrange(n)])
                        #  length 10
                        
                        user =None
                        if 'user' not in request.session  or not request.session['user']:
                            pass
                        else:
                            user= request.session['user']
                            
                        usernamebase64= base64.b64encode(force_bytes(str(user.username)))
                        newusernamebase64 = usernamebase64.replace("==", "")
                        
                        
                        filename = newusernamebase64.lower() + name_str(15) 
                                          
                        """
                        if 'newDictionaryList' not in request.session  or not request.session['newDictionaryList']:
                            pass
                        else:
                            newDictionaryList =  request.session['newDictionaryList']
                            for d in newDictionaryList:
                                try:
                                    dictionary=Dictionary.objects.get(tag__exact=d.tag)                                                          
                                except ObjectDoesNotExist as error:
                                    print "Message({0}): {1}".format(99, error.message)  
                                    d.save()  
                                    try:                               
                                        
                                        lcs=d.tag.split()
                                        prstr=lcs[0].strip()[5:]
                                        parts=prstr.split('_')                                
                                        #proptag=PropTags.objects.get(tag__exact=parts[1])
                                    except ObjectDoesNotExist as error:
                                        print "Message({0}): {1}".format(99, error.message)  
                                        pt=PropTags()
                                        pt.tag= parts[1]
                                        pt.save()
                            """
                                
                                
                        mpodutil=MPODUtil()
                        mpodutil.mpodwrite(filename,propertyMaster)
                        mpodutil.addinfo()
                        mpodutil.adddatavalue()                
                        mpodutil.user = user
                        mpodutil.savefile()
                        
                        if mpodutil.message:
                            message = mpodutil.message
                            description = "An error occurred while creating the" + filename + ".mpod file" 
                            response = render_to_response('account/500.html', { "message":message, "current" :"File created and sent","description" :description,}, context_instance=RequestContext(request))  
                            return response
    
                        """
                        u= User()
                        u=user
                        fileuser = FileUser()
                        fileuser.filename=mpodutil.cif_created
                        fileuser.authuser=u 
                        fileuser.date = datetime.datetime.now(tz=get_current_timezone()).strftime('%Y-%m-%d %H:%M:%S')
                        fileuser.reportvalidation = mpodutil.reportValidation
                        fileuser.save()
                        
                       """
                        
                        
                        
                        #uid= base64.b64encode(force_bytes(str(user.pk))),
                        #token= account_activation_token.make_token(user)
                        datafilescreated ="datafilescreated"
                        forwardslash="/"
                        #request.session['cif_created']=mpodutil.cif_created
        
                        #linkactivate = os.path.join(datafilescreated,forwardslash)
                       
                        
                        current_site = get_current_site(request)
                        
                        
                        messageCategoryDetailQuerySet1=MessageCategoryDetail.objects.filter(messagecategory=MessageCategory.objects.get(pk=3))#3 for category staff notification
                        #messageMailQuerySet1= MessageMail.objects.filter(pk=messageCategoryDetail1.message.pk)
                        sendmsg = True
                        
                        try:
                            for mcd in messageCategoryDetailQuerySet1:
                                messageCategoryDetail = MessageCategoryDetail()
                                messageCategoryDetail = mcd
                                messageMail= MessageMail.objects.get(pk=messageCategoryDetail.message.pk)
                                
                                if messageMail.pk == 5:
                                    configurationMessage = ConfigurationMessage.objects.get(message=messageMail)
                                    smtpconfig= configurationMessage.account
                     
                                    my_use_tls = False
                                    if smtpconfig.email_use_tls ==1:
                                        my_use_tls = True
                                    
                                    fail_silently= False
                                    listemail=[]
                                    listuser=User.objects.filter(groups=messageCategoryDetail.group)
                                    for u in listuser:
                                        #print u.email   
                                        listemail.append(u.email)
                                    
                                    
                
                                    message = render_to_string('notification_to_staff_email.html', {
                                                                                            'regards':messageMail.email_regards,
                                                                                            'email_message':  messageMail.email_message,
                                                                                            'user': user,
                                                                                            'domain': current_site.domain,
                                                                                            'datafilescreated': datafilescreated,
                                                                                            'cif_created': mpodutil.cif_created,
                                                                                            'reportValidation':mpodutil.reportValidation,
                                                                                            'forwardslash':forwardslash
                                    })
                                
                                    print message
                                
                                    
                                                   
                                    backend = EmailBackend(   host=smtpconfig.email_host, 
                                                                                        port=int(smtpconfig.email_port ), 
                                                                                        username=smtpconfig.email_host_user, 
                                                                                        password=smtpconfig.email_host_password, 
                                                                                        use_tls=my_use_tls,
                                                                                        fail_silently=fail_silently)
                                                                
                                    email = EmailMessage( messageMail.email_subject,
                                                                                message,
                                                                                smtpconfig.email_host_user,
                                                                                listemail,
                                                                                connection=backend)
                                    
                                    email.attach_file(os.path.join(str(mpodutil.cifs_dir_valids), mpodutil.cif_created))
                                    if sendmsg:
                                        email.send()
                                        
                        except Exception  as e:
                            response = render_to_response('account/500.html', { "message":e, "current" :"File created and sent","description" :"Error when sending the email for staff notification",}, context_instance=RequestContext(request))  
                            return response
                                
                                
                                
                        messageCategoryDetailQuerySet2=MessageCategoryDetail.objects.filter(messagecategory=MessageCategory.objects.get(pk=2))#2 for category User notification
                        #messageMail= MessageMail.objects.get(pk=messageCategoryDetailQuerySet2.message.pk)
     
                        for mcd in messageCategoryDetailQuerySet2:
                            messageCategoryDetail = MessageCategoryDetail()
                            messageCategoryDetail = mcd
                            messageMail= MessageMail.objects.get(pk=messageCategoryDetail.message.pk)
                           
                            if messageMail.pk == 6:
                                configurationMessage = ConfigurationMessage.objects.get(message=messageMail)
                                smtpconfig= configurationMessage.account
                                
                                my_use_tls = False
                                if smtpconfig.email_use_tls ==1:
                                    my_use_tls = True
                                
                                fail_silently= False
                                
                            
                                
                                message = render_to_string('notification_to_user_email.html', {
                                                                                        'regards':messageMail.email_regards,
                                                                                        'email_message':  messageMail.email_message,
                                                                                        'user': user,
                                                                                        'domain': current_site.domain,
                                                                                        'datafilescreated': datafilescreated,
                                                                                        'cif_created': mpodutil.cif_created,
                                                                                        'forwardslash':forwardslash
                                })
                            
                                
                            
                                
                                               
                                backend = EmailBackend(   host=smtpconfig.email_host, 
                                                                                    port=int(smtpconfig.email_port ), 
                                                                                    username=smtpconfig.email_host_user, 
                                                                                    password=smtpconfig.email_host_password, 
                                                                                    use_tls=my_use_tls,
                                                                                    fail_silently=fail_silently)
                                                            
                                email = EmailMessage( messageMail.email_subject,
                                                                            message,
                                                                            smtpconfig.email_host_user,
                                                                              [user.email],
                                                                            connection=backend)
                                
                                email.attach_file(os.path.join(str(mpodutil.cifs_dir_valids), mpodutil.cif_created))
                                if sendmsg:
                                    email.send()
                                
                                
                        del request.session['propertyMaster']     
 
                        current ="File created and sent"
                        response = render_to_response('account/successfile.html', {"propertySessionList":propertySessionList,
                                                                                                                                        'propertyMaster':propertyMaster,
                                                                                                                                        "current":current,}, context_instance=RequestContext(request))  
                    except  ValueError as e:
                        response = render_to_response('account/500.html', { "message":e, "current" :"File created and sent","description" :"Error when sending the email for user notification",}, context_instance=RequestContext(request))  
                        return response
 
        #return newcase(request);#render_to_response('newcase.html', { "saved_compliancepropetyList":saved_compliancepropetyList}, context_instance=RequestContext(request))
    return response

     
 
   
@login_required
@csrf_exempt 
def addnewdictionaryproperty(request,todo,index): 

    dicvalue = request.POST.get('valuenew', False)
    
    underscore = '_'
    property = "_prop_" 
   
  
    name = request.POST.get('namenew', False)
    lins1 = map(lambda x: x.strip(),    name.strip().split(" "))
    line =  "_prop_"   
    x= len(lins1)  
    print x
    for i, li in enumerate(lins1):
        if i < (x -1):
            line =line + li + underscore
        else:
            line =line +  li 


    
    in_list = False
    newItem=Dictionary()
    newItem.tag =line
    newItem.name = request.POST.get('namenew', False)
     
    newItem.description= request.POST.get('namenew', False)
    newItem.category= Category.objects.get(pk=9) 
    
    newItem.units = request.POST.get('unitsnew', False)
    newItem.units_detail = request.POST.get('units_detailnew', False)
    newItem.definition= request.POST.get('definitionnew', False)
    
    if not isnumber(dicvalue):
        newItem.type='char'
    else:
        newItem.type='numb'
 
    if  todo == "addnew":    
        if 'newDictionaryList' not in request.session  or not request.session['newDictionaryList']:
            if not 'dictionaryValues' in request.session or not request.session['dictionaryValues' ]:  
                newDictionaryList=[]
                newDictionaryList.append(newItem)
                dictionaryValues = {}    
                dictionaryValues[newItem.tag.encode("ascii"),newItem.type]=dicvalue.encode("ascii")
                request.session['dictionaryValues' ] = dictionaryValues        
                request.session['newDictionaryList']=newDictionaryList   
            else:
                newDictionaryList=[]
                dictionaryValues=request.session['dictionaryValues' ] 
                if newItem.tag.encode("ascii") in dictionaryValues:
                    in_list = True
                else:
                    in_list = False
                    dictionaryValues[newItem.tag.encode("ascii"),newItem.type]=dicvalue.encode("ascii")
                    request.session['dictionaryValues' ] = dictionaryValues
                    newDictionaryList.append(newItem)
                    request.session['newDictionaryList']=newDictionaryList   
                
                
                
        else:
            newDictionaryList =  request.session['newDictionaryList']
            dictionaryValues=request.session['dictionaryValues' ] 
            if newItem.tag.encode("ascii") in dictionaryValues:
                in_list = True
            else:
                in_list = False
                dictionaryValues[newItem.tag.encode("ascii"),newItem.type]=dicvalue.encode("ascii")
                request.session['dictionaryValues' ] = dictionaryValues
                newDictionaryList.append(newItem)
                #request.session['newDictionaryList'] = newDictionaryList
                
            print newDictionaryList
            print dictionaryValues

    data = {
        'name': newItem.name,
        'units': newItem.units,
        'units_detail': newItem.units_detail,
        'dicvalue': dicvalue,
        'in_list': in_list,
 
    } 
    
    del newItem
    
    return HttpResponse(json.dumps(data), content_type="application/json")            

def isnumber(param):
    result = False
    try:
        val = float(param)
        result = True
        return result
    except ValueError:
        print("That's not an int!")
        return result


@csrf_exempt 
def rotatematrix(request,pk): 
 
    if request.is_ajax():
        omeg =  request.POST.get('omeg', False)   
        mh =  request.POST.get('mh', False)   
        mk =  request.POST.get('mk', False)   
        ml =  request.POST.get('ml', False)   
        mat =  request.POST.get('mat', False)   
        tensor =  request.POST.get('url', False)   
        #url ='http://supercomputo.cimav.edu.mx:8080/mpod/finpiezo?'
        
    
        values2= "mh="+ mh + "&mk=" + mk +"&ml="+ ml
        mat = "&mat=" +mat
        ome="&omeg=" + omeg;
        
        urlcluster = "http://supercomputo.cimav.edu.mx:8080/mpod/" + tensor+"?" + values2 + ome + mat
        print urlcluster
        response = urllib2.urlopen(urlcluster)
        
         
         
        
        resultado = json.loads(response.read())
        
        rotated = resultado['resultado']
         
         
        #values = "?value11="+val1+"&value12="+val2+"&value13="+val3+"&value14="+val4+"&value15="+val5+"&value16="+val6+"&value21="+val7+"&value22="+val8+"&value23="+val9+"&value24="+val10+"&value25="+val11+"&value26="+val12+"&value31="+val13+"&value32="+val14+"&value33="+val15+"&value34="+val16+"&value35="+val17+"&value36="+val18;
        rotatedparameters =""
        valuearrayrotated =""
        ampersand = "&"
        html= """<div class='container-fluid'><table class='table table-striped table-condensed table-hover sm_table' >
                    <tbody>"""
        
        lastindex = len( rotated ) * len( rotated[0])     
        counterindex = 0
        for i,row in enumerate(rotated):
            rowrotated=rotated[i]
            #print len(rowrotated)  
            html=  html+ "<tr>" 
            for j,row in enumerate(rowrotated):
                #print rowrotated[j]
                #valuearrayrotated.append("'" + str(float(rowrotated[j])) +"'")
                
                counterindex = counterindex + 1 
                html=  html+  "<td>" + str(float(rowrotated[j]) )+ "</td>"
                if  counterindex <  lastindex:
                    rotatedparameters =  rotatedparameters + "value"+str(i+1)+str(j+1)  +"="+ str(float(rowrotated[j]) ) + ampersand
                    valuearrayrotated = valuearrayrotated +"valuearrayrotated=" + str(float(rowrotated[j])) + ampersand 
                else:
                    rotatedparameters =  rotatedparameters + "value"+str(i+1)+str(j+1)  +"="+ str(float(rowrotated[j]) ) 
                    valuearrayrotated = valuearrayrotated + "valuearrayrotated=" + str(float(rowrotated[j])) 
                    
                
                
            html=  html+ "</tr>" 
                 
        html=  html+  "</tbody></table></div>"      

        data = {'html': html,
                     'rotatedparameters': rotatedparameters,
                     'valuearrayrotated': valuearrayrotated
                     }
        
        return HttpResponse(json.dumps(data), content_type="application/json")   
    else:
        raise Http404
    
    
 
@csrf_exempt 
def showmatrix(request,pk): 
    
    if request.is_ajax():
        datafile_id =  request.POST.get('datafile_id', False)   
        
        datafiletemp = DataFileTemp.objects.get(id=int(datafile_id))
        
        
        objPropertyTemp=PropertyTemp.objects.get(id=pk, active=True)
        dim = get_dimensions(objPropertyTemp.tensor_dimensions)
        coefficents = get_coefficents_total(objPropertyTemp.tensor_dimensions)
        #parts=objPropertyTemp.tag.split('_')[-1]
        #label =objPropertyTemp.tag.split('_')[-1]
        label =objPropertyTemp.short_tag
        print label
        datafilepropertytemp_ids=DataFilePropertyTemp.objects.filter(datafiletemp=datafiletemp,propertytemp=objPropertyTemp).values_list('id',flat=True) 
        
        
        indexi = 0
        indexj = 0
        data =""  
        table = ""
        input = "" 
        coefficientsmatrix = None
        if dim == 1:
            print "dimension 1"
            print objPropertyTemp.tensor_dimensions
            index = objPropertyTemp.tensor_dimensions
            indexj = int(index)
            
            
            
            if indexj != 0:
               
                coefficientsmatrix = N.zeros(indexj) 
                print datafilepropertytemp_ids
                if  datafilepropertytemp_ids:
                    propertyValuesTempQuerySet= PropertyValuesTemp.objects.filter(datafilepropertytemp_id__in=datafilepropertytemp_ids).order_by('prop_data_tensorial_index')
                    #label = propertyValuesTempQuerySet.reverse()[0].prop_data_label
            
                    
                    #print coefficientsmatrix
                    for x,item in enumerate( propertyValuesTempQuerySet):
                        index= list(propertyValuesTempQuerySet[x].prop_data_tensorial_index)  
                        i =int(index[0]) - 1
                        j = int(index[1]) -1
                        coefficientsmatrix[i,j] = float(propertyValuesTempQuerySet[x].prop_data_value)
                        
                        lbl='_' + str(j +1)
                        inputlabel = label.replace("i",  lbl)
                        if x != (len(propertyValuesTempQuerySet) - 1 ):
                            data = data + inputlabel +'=' +str(coefficientsmatrix[i,j] ) +'&' 
                        else:
                            data = data + inputlabel +'=' +str(coefficientsmatrix[i,j] ) 
                else:
                    #pass
                    countercoeff = 0
                    for i in range(dim):
                        for j in range(indexj):
                            lbl='_' + str(j +1)
                            inputlabel = label.replace("i",  lbl)
                        
                            if countercoeff != (coefficents -1):
                                data = data + inputlabel +'=' +str(coefficientsmatrix[j] ) +'&' 
                            else:
                                data = data + inputlabel +'=' +str(coefficientsmatrix[j] ) 
                                
                            countercoeff = countercoeff + 1
                    
                        
                
                
                table = '<table class="table table-striped table-condensed table-hover sm_table" > <tbody>' 
                print coefficientsmatrix
                #for i in range(int(indexi[-1])):
                for i in range(dim):
                    table = table +  ' <tr>' 
                    #for j in range(int(indexj[-1])):
                    for j in range(indexj):
                        lbl='_' +  str(j +1)
                        inputlabel = label.replace("i",  lbl)
                        if coefficientsmatrix[j] != 0.0:
                            input = '<input type="text" name="coeff_'+ inputlabel+'" value="'+ str(coefficientsmatrix[j] )+'" id="id_'+ inputlabel+'" style="width: 50px;" />'
                        else:
                            if datafilepropertytemp_ids:
                                input = '<input type="text" name="coeff_'+ inputlabel+'" value="'+ str(coefficientsmatrix[j] )+'" id="id_'+ inputlabel+'" style="width: 50px;" readonly="readonly"  disabled/>'
                            else:
                                input = '<input type="text" name="coeff_'+ inputlabel+'" value="'+ str(coefficientsmatrix[j] )+'" id="id_'+ inputlabel+'" style="width: 50px;" />'
                       
                       
                        table = table + ' <td> '+ input+'</td>' 
                     
                    table = table +  ' </tr>' 
                    
                table = table +  ' <tr >' 
           
                #data = data + 'propertyid' + '=' + pk
                function = "updatecoefficient('" + data + "', '"+ pk + "', '"+ datafile_id + "')"
                #table = table + ' <td colspan="'+str(indexj[-1])+'"> <div class="submit-row"><p  ><a href="#" class="submit-row" onclick="' + function + '">Update</a></p></div></td>' 
                table = table + ' <td colspan="'+str(indexj)+'"> <div class="submit-row"><p  ><a href="#" class="submit-row" onclick="' + function + '">Update</a></p></div></td>' 
              
                table = table +  ' </tr>' 
                    
                table = table + ' </tbody></table>'
                
            
        if dim == 2:
            print "dimension 2"
            print objPropertyTemp.tensor_dimensions
            index = objPropertyTemp.tensor_dimensions.split(",")
            indexi = int(index[0])
            indexj=  int(index[1])
 
            print coefficents
            coefficientsmatrix = N.zeros([indexi,indexj]) 
            print coefficientsmatrix
            
            
            
            
            print datafilepropertytemp_ids
            if  datafilepropertytemp_ids:
                propertyValuesTempQuerySet= PropertyValuesTemp.objects.filter(datafilepropertytemp_id__in=datafilepropertytemp_ids).order_by('prop_data_tensorial_index')
                #label = propertyValuesTempQuerySet.reverse()[0].prop_data_label
        
                
                #print coefficientsmatrix
                for x,item in enumerate( propertyValuesTempQuerySet):
                    index= list(propertyValuesTempQuerySet[x].prop_data_tensorial_index)  
                    i =int(index[0]) - 1
                    j = int(index[1]) -1
                    coefficientsmatrix[i,j] = float(propertyValuesTempQuerySet[x].prop_data_value)
                    
                    lbl='_' + str(i +1) + str(j +1)
                    inputlabel = label.replace("ij",  lbl)
                    if x != (len(propertyValuesTempQuerySet) - 1 ):
                        data = data + inputlabel +'=' +str(coefficientsmatrix[i,j] ) +'&' 
                    else:
                        data = data + inputlabel +'=' +str(coefficientsmatrix[i,j] ) 
            else:
                #pass
                countercoeff = 0
                for i in range(indexi):
                    for j in range(indexj):
                        lbl='_' + str(i +1) + str(j +1)
                        inputlabel = label.replace("ij",  lbl)
                    
                        if countercoeff != (coefficents -1):
                            data = data + inputlabel +'=' +str(coefficientsmatrix[i,j] ) +'&' 
                        else:
                            data = data + inputlabel +'=' +str(coefficientsmatrix[i,j] ) 
                            
                        countercoeff = countercoeff + 1
                
                    
            
            
            table = '<table class="table table-striped table-condensed table-hover sm_table" > <tbody>' 
            print coefficientsmatrix
            #for i in range(int(indexi[-1])):
            for i in range(indexi):
                table = table +  ' <tr>' 
                #for j in range(int(indexj[-1])):
                for j in range(indexj):
                    lbl='_' + str(i +1) + str(j +1)
                    inputlabel = label.replace("ij",  lbl)
                    if coefficientsmatrix[i,j] != 0.0:
                        input = '<input type="text" name="coeff_'+ inputlabel+'" value="'+ str(coefficientsmatrix[i,j] )+'" id="id_'+ inputlabel+'" style="width: 50px;" />'
                    else:
                        if datafilepropertytemp_ids:
                            input = '<input type="text" name="coeff_'+ inputlabel+'" value="'+ str(coefficientsmatrix[i,j] )+'" id="id_'+ inputlabel+'" style="width: 50px;" readonly="readonly"  disabled/>'
                        else:
                            input = '<input type="text" name="coeff_'+ inputlabel+'" value="'+ str(coefficientsmatrix[i,j] )+'" id="id_'+ inputlabel+'" style="width: 50px;" />'
                   
                   
                    table = table + ' <td> '+ input+'</td>' 
                 
                table = table +  ' </tr>' 
                
            table = table +  ' <tr >' 
            
            #data = data + 'propertyid' + '=' + pk
            function  = "updatecoefficient('" + data + "', '"+ pk + "', '"+ datafile_id + "')"
            #table = table + ' <td colspan="'+str(indexj[-1])+'"> <div class="submit-row"><p  ><a href="#" class="submit-row" onclick="' + function + '">Update</a></p></div></td>' 
            table = table + ' <td colspan="'+str(indexj)+'"> <div class="submit-row"><p  ><a href="#" class="submit-row" onclick="' + function + '">Update</a></p></div></td>' 
          
            table = table +  ' </tr>' 
                
            table = table + ' </tbody></table>'
        
        if dim == 3:
            print "dimension 3"
            print objPropertyTemp.tensor_dimensions
            index = objPropertyTemp.tensor_dimensions.split(",")
            indexi = int(index[0])
            indexj=  int(index[1])
       
        

    data = {'html': table,
                     }
    return HttpResponse(json.dumps(data), content_type="application/json")   
    
    
    
@csrf_exempt 
def updatecoefficient(request,pk): 
    
    if request.is_ajax():
        datafile_id =  request.POST.get('datafile_id', False)   
        
        datafiletemp = DataFileTemp.objects.get(id=int(datafile_id))
        
        objPropertyTemp=PropertyTemp.objects.get(id=pk, active=True)
        dim = get_dimensions(objPropertyTemp.tensor_dimensions)
        coefficents = get_coefficents_total(objPropertyTemp.tensor_dimensions)
        #parts=objPropertyTemp.tag.split('_')[-1]
        label =objPropertyTemp.tag.split('_')[-1]
        print label
        
        datafilepropertytemp_ids=DataFilePropertyTemp.objects.filter(datafiletemp=datafiletemp,propertytemp=objPropertyTemp).values_list('id',flat=True) 
        #print datafilepropertytemp_ids
        
    
        def getIndex(coefficientsTag):              
            match = re.match(r"([a-z]+)([0-9]+)",  coefficientsTag, re.I)
            if match:
                items = match.groups()
                numbers = items[1]
                index = re.findall(r'.{1,1}',numbers,re.DOTALL)
                indextem=[]
                indextem.append(int(index[0]) - 1)
                indextem.append( int(index[1]) - 1)
                return indextem
        
        objPropertyValuesTemp = None
        for k,v in request.POST.iterlists():
            #index = k.split("_")
            #print index 
            tag = k.replace("_","")
            #print tag 
            index= getIndex(tag)
            if index:
                tensorial_index = str(index[0] +1) + str( index[1] +1)
                #print tensorial_index
                    
                if datafilepropertytemp_ids:
                    objPropertyValuesTemp= PropertyValuesTemp.objects.get(datafilepropertytemp_id=datafilepropertytemp_ids[0],prop_data_tensorial_index=tensorial_index)
                    objPropertyValuesTemp.prop_data_value = float(v[0])
                else:
                    objDtaFilePropertyTemp = DataFilePropertyTemp()
                    objDtaFilePropertyTemp.propertytemp = objPropertyTemp
                    objPropertyValuesTemp= PropertyValuesTemp()
                    objPropertyValuesTemp.datafilepropertytemp=objDtaFilePropertyTemp
                    objPropertyValuesTemp.prop_data_label = label
                    objPropertyValuesTemp.prop_data_tensorial_index =  tensorial_index
                    objPropertyValuesTemp.prop_data_value = float(v[0])
                    """objPropertyValuesTemp.prop_measurement_method =   
                    objPropertyValuesTemp.prop_conditions_frequency =   
                    """
                    
     
                    
                 
        propertyValuesTempList =[]
        if not 'propertyValuesTempList' in request.session or not request.session['propertyValuesTempList' ]: 
            
            propertyValuesTempList.append(objPropertyValuesTemp)
            request.session['propertyValuesTempList' ] = propertyValuesTempList
        else:
            #del request.session['propertyValuesTempList']
            found = False
            propertyValuesTempList = request.session['propertyValuesTempList' ] 
            for i, item in enumerate(propertyValuesTempList):
                if propertyValuesTempList[i].datafilepropertytemp.propertytemp.id == objPropertyTemp.id:
                    propertyValuesTempList[i] = objPropertyValuesTemp
                    found = True
                    break
                 
             
            if not  found:       
                propertyValuesTempList.append(objPropertyValuesTemp)
            
            
            request.session['propertyValuesTempList' ] = propertyValuesTempList
        
        
        print len(propertyValuesTempList)
        
        data = {'html': 'table',
         }
         
    return HttpResponse(json.dumps(data), content_type="application/json")   
        
          
          
          

@login_required
@csrf_exempt 
def addmaterial(request,pk):
    #response= None
    todo  = request.POST.get('todo', False)    
    dicvalue = request.POST.get('dicvalue', False)
    apply_to_all = request.POST.get('apply_to_all', False)
    """dicvalue = request.POST.get('phasevalue', False)
    dicvalue = request.POST.get('phasecharacteristicvalue', False)
    dicvalue = request.POST.get('measurementvalue', False)"""
    print 'addmaterial'
    
    in_list = False
    error =""
    dictionary_pk =  request.POST.get('dictionary_pk', False) 
    objDictionarySelected = Dictionary.objects.get(pk=dictionary_pk, active=True) 
    print objDictionarySelected.type
    if dicvalue != "":
        if objDictionarySelected.type == "numb":
            if not isnumber(dicvalue):
                error ="The value must be numeric"        
        elif objDictionarySelected.type == "char":
            pass
    else:
        error ="the field can not be empty"        
         
    if error != "":  
            data = {
                'name': objDictionarySelected.name,
                'units': objDictionarySelected.units,
                'units_detail': objDictionarySelected.units_detail,
                'dicvalue': dicvalue,
                'in_list': in_list,
                'error':error,
         
            }
            return  HttpResponse(json.dumps(data), content_type="application/json")   
    
    
    

    if pk == '-1' and todo == "change":
        print "selected"  
        print  objDictionarySelected
        pass
    elif  pk == '-1' and todo == "add":
        if not 'dictionaryValues' in request.session or not request.session['dictionaryValues' ]:                 
            dictionaryValues = {}
            dictionaryValues[objDictionarySelected.tag.encode("ascii"),objDictionarySelected.type,apply_to_all]=dicvalue.encode("ascii")
            request.session['dictionaryValues' ] = dictionaryValues
        else:
            dictionaryValues=request.session['dictionaryValues' ] 
            if objDictionarySelected.tag.encode("ascii") in dictionaryValues:
                in_list = True
            else:
                in_list = False
                dictionaryValues[objDictionarySelected.tag.encode("ascii"),objDictionarySelected.type,apply_to_all]=dicvalue.encode("ascii")
                request.session['dictionaryValues' ] = dictionaryValues

    data = {
        'name': objDictionarySelected.name,
        'units': objDictionarySelected.units,
        'units_detail': objDictionarySelected.units_detail,
        'dicvalue': dicvalue,
        'in_list': in_list,
        'error':error,
 
    }
   


    return HttpResponse(json.dumps(data), content_type="application/json")  
    
    
    
@login_required
@csrf_exempt 
def addcasev2(request): 
    
    todo = request.POST.get('todo', False)
    experimentalparcond_name_selected = request.POST.get('experimentalparcond_name', False)
    chkBoxmge = request.POST.getlist('chkBoxmge', False) 
    #print experimentalparcond_name_selected

    if todo == 'submit':
        current ="Add Case"
        isvalid =False
        form=None  
        inputList = []   
        #coefficientsparts = []
        if 'inputList' not in request.session  or not request.session['inputList']:
            pass
        else:
            selectChange = request.POST.get('selectChange', False)  
            #print selectChange
            if selectChange == "0":
                inputList=request.session['inputList']
            else:
                del request.session['inputList']
                
 
            
        #list initialisation 
        propertyCategoryName=[]   
        catalogCrystalSystemList=[]   
        typeList=[]  
        
        catalogproperty_name = request.POST.get('catalogproperty_name', False)            
        crystalsystem_name= request.POST.get('crystalsystem_name', False) 
        
        
        datapropertytagselected = ''
        datapropertytagselected= request.POST.get('datapropertytag', False) 
        if datapropertytagselected == False:
            datapropertytagselected =''   
            

       
        
        typeselected=''
        typeselected = request.POST.get('type', False)  
        if typeselected == False:
            typeselected =''   
        
        #initialisation
        piezoelectricitydgeh = 0
        magnetoelectricity = 0
        chkBoxMagnetoelectricity = 0
        questiontype =''
        if catalogproperty_name == "e":
            questiontype = "s (compliance) o c (stiffness)?"
            
        if 'typeListOnSession' not in request.session  or not request.session['typeListOnSession']:
            pass
        else:
            if catalogproperty_name == "e":
                typeList=request.session['typeListOnSession']
                if typeselected == '':
                    typeselected = 's'
            if catalogproperty_name == "p":
                print len(typeselected)
                if typeselected != "dg" and typeselected != "eh" and (len(typeselected)  == 0) != True:
                    typeselected='dg'
                else:
                    objDataProperty = Property.objects.get(id=int(datapropertytagselected), active=True)  
                    typeQuerySet=Type.objects.filter(catalogproperty=CatalogProperty.objects.get(name__exact=catalogproperty_name))
           
                     
                    
                    typeselected=typeQuerySet[0].name
                  
                typeselecteddg='dg'
                typeselectedeh='eh'
            if catalogproperty_name == "2nd":
                chkBoxMagnetoelectricity = 1
                questiontype = "Magnetoelectricity?"  
                if chkBoxmge == False:
                    magnetoelectricity = 0
                    typeselected='k'
                else:
                    magnetoelectricity = 1  
                    typeselected='y'
 
                     
            
        axisselected_name =''
        axisselected_name = request.POST.get('axisselected_name', False)   
        if axisselected_name == False:
            axisselected_name =''
        
        pointgroupselected_name =''
        pointgroupselected_name =  request.POST.get('pointgroupselected_name', False)
        if pointgroupselected_name == False:
            pointgroupselected_name =''
        
        
        if 'propertyCategoryNameListOnSession' not in request.session  or not request.session['propertyCategoryNameListOnSession']:
            propertyCategoryName=CatalogProperty.objects.filter(active= True)
            request.session['propertyCategoryNameListOnSession'] =propertyCategoryName
        else:
            propertyCategoryName =request.session['propertyCategoryNameListOnSession']
          
          
        list_CatalogCrystalSystem= CatalogCrystalSystem.objects.filter(catalogproperty=CatalogProperty.objects.get(name__exact=catalogproperty_name),active=True)
        """for register_catalogCrystalSystem in list_CatalogCrystalSystem: 
            objCatalogCrystalSystem=CatalogCrystalSystem();
            objCatalogCrystalSystem = register_catalogCrystalSystem
            catalogCrystalSystemList.append(objCatalogCrystalSystem)"""
        for i,crystalsystem in enumerate(list_CatalogCrystalSystem): 
            try:
                crystalsystemtype=CrystalSystemType.objects.get(catalogcrystalsystem=crystalsystem,type=Type.objects.filter(active=True, name=typeselected),active=True)
                catalogCrystalSystemList.append(crystalsystemtype.catalogcrystalsystem)
            except ObjectDoesNotExist as error:
                print "Message({0}): {1}".format(99, error.message) 

        if 'catalogCrystalSystemListOnSession' not in request.session  or not request.session['catalogCrystalSystemListOnSession']:
            pass
        else:
            del request.session['catalogCrystalSystemListOnSession']

 
            
        request.session['catalogCrystalSystemListOnSession']=catalogCrystalSystemList
            
            
        if 'dataPropertyListOnSession' not in request.session  or not request.session['dataPropertyListOnSession']:
            pass
        else:
            del request.session['dataPropertyListOnSession']
            
        ids=CatalogProperty.objects.filter(name=catalogproperty_name,active=True).values_list('id', flat=True)    
        if catalogproperty_name == "p":
            type_ids1=Type.objects.filter(catalogproperty_id__in=ids,active=True, name=typeselecteddg).values_list('id',flat=True)    
            type_ids2=Type.objects.filter(catalogproperty_id__in=ids,active=True, name=typeselectedeh).values_list('id',flat=True)    
        
            type_ids = list(set(type_ids1) | set(type_ids2)) 
        else:
            
            type_ids=Type.objects.filter(catalogproperty_id__in=ids,active=True, name=typeselected).values_list('id',flat=True)    
 
        
        data_property_ids=TypeDataProperty.objects.filter(type_id__in=type_ids).values_list('dataproperty_id',flat=True)    
        dataPropertyList=Property.objects.filter(id__in=data_property_ids, active=True)
        request.session['dataPropertyListOnSession']=dataPropertyList


        dictionaryList=[]
        dictionaryQuerySet= Dictionary.objects.filter(category = Category.objects.get(pk=9), deploy = 1, active=True)
        for dictionary in dictionaryQuerySet: 
            objDictionary =Dictionary();
            objDictionary = dictionary
            dictionaryList.append(objDictionary)
            del objDictionary
            
        request.session['dictionaryList'] =dictionaryList
        
        
        dictionaryPhaseList=[]
        
        dictionaryPhaseQuerySet1= Dictionary.objects.filter(category = Category.objects.get(pk=4), deploy = 1, active=True)
        dictionaryPhaseQuerySet2= Dictionary.objects.filter(category = Category.objects.get(pk=8), deploy = 1, active=True)
        dictionaryPhaseQuerySet= (dictionaryPhaseQuerySet1 | dictionaryPhaseQuerySet2).distinct()
        for dictionary in dictionaryPhaseQuerySet: 
            objDictionary =Dictionary();
            objDictionary = dictionary
            dictionaryPhaseList.append(objDictionary)
            del objDictionary  
            
        request.session['dictionaryPhaseList'] =dictionaryPhaseList
        
        dictionaryPhaseCharacteristicList=[]
        dictionaryPhaseCharacteristicQuerySet= Dictionary.objects.filter(category = Category.objects.get(pk=11), deploy = 1, active=True)
        for dictionary in dictionaryPhaseCharacteristicQuerySet: 
            objDictionary =Dictionary();
            objDictionary = dictionary
            dictionaryPhaseCharacteristicList.append(objDictionary)
            del objDictionary    
            
            
        dictionaryMeasurementList=[]
        dictionaryMeasurementQuerySet= Dictionary.objects.filter(category = Category.objects.get(pk=12), deploy = 1, active=True)
        for dictionary in dictionaryMeasurementQuerySet: 
            objDictionary =Dictionary();
            objDictionary = dictionary
            dictionaryMeasurementList.append(objDictionary)
            del objDictionary     

        
        ShowBtnSend=0

        form =ValidateAddCaseFormv2(request.POST,inputList=inputList)
        

         
        validationbyform = 0
        propertiesv2=None
        
                
        propertyMaster = PropertyMaster()
        lengthlist = 0
        if not 'propertyMaster' in request.session or not request.session['propertyMaster' ]:  
            pass
        else:
            propertyMaster = request.session['propertyMaster' ]
            print propertyMaster
            if propertyMaster.propertyList:
                print propertyMaster.propertyList
                lengthlist =len(propertyMaster.propertyList) 
                


        propertaddedmessage =""
        sucess = 0
        added = 0
        inputListReadOnly = [] 
        inputListValues = {}
      
        warning2 = ""
        warning = ""
        samepointgroup = True
        if form.is_valid():
            #request.POST = form.data
           
            if not propertyMaster.pointgroup:
                propertyMaster.pointgroup = pointgroupselected_name
            elif not propertyMaster.pointgroup == pointgroupselected_name:
                samepointgroup = False
                warning = "The punctual group " +propertyMaster.pointgroup +" must be the same for all the properties of this case"
            
            
            propertiesv2=Propertiesv2(catalogproperty_name, crystalsystem_name, typeselected,datapropertytagselected, chkBoxmge,request.POST, inputList=inputList)#,coefficientsparts=coefficientsparts)
            qd =[]
            qd.append(form.data)
            propertiesv2.NewProperties(pointgroupselected_name,axisselected_name,*qd)

            sucess=propertiesv2.sucess  

 

             

            
            if  sucess  == 0:
                inputList=propertiesv2.catalogPropertyDetail
                request.session['inputList']=inputList
                #request.session['coefficientsparts']=propertiesv2.coefficientsparts
                
                inputListReadOnly=propertiesv2.catalogPropertyDetailReadOnly
 
                print "continue"
            else:
 
                propertyMaster.title = request.POST.get('title', False)
                propertyMaster.authors = request.POST.get('author', False)
                propertyMaster.journal = request.POST.get('journal', False)
                propertyMaster.year = request.POST.get('year', False)
                propertyMaster.volume = request.POST.get('volume', False)
                propertyMaster.page_first = request.POST.get('page_first', False)
                propertyMaster.page_last = request.POST.get('page_last', False)
               
                 
 
     
                if not 'dictionaryValues' in request.session or not request.session['dictionaryValues' ]:                 
                    pass 
                else:
                    dictionaryValues =request.session['dictionaryValues' ] 
                    #propertiesv2.dictionaryValues=dictionaryValues
                 
                    if dictionaryValues:
                        if not propertyMaster.headerBlockValues:
                            propertyMaster.headerBlockValues = {}
                            
                        if not propertiesv2.loopBlockValues:
                            propertiesv2.loopBlockValues = {}    
                        
                            
                        for key,value in dictionaryValues.items():
                            for i, item in enumerate(dictionaryPhaseList):
                                if  dictionaryPhaseList[i].tag == key[0]:
                                    propertyMaster.headerBlockValues[key[0],key[1],key[2]] = value
                                    
                                    break
                              
                            for i, item in enumerate(dictionaryPhaseCharacteristicList):
                                if  dictionaryPhaseCharacteristicList[i].tag == key[0]:
                                    propertyMaster.headerBlockValues[key[0],key[1],key[2]] = value     
                                   
                                    break
                                    
                            for i, item in enumerate(dictionaryList):
                                if  dictionaryList[i].tag == key[0]:
                                    if key[2] == 'false':
                                        propertiesv2.loopBlockValues[key[0],key[1],key[2]] = value  
                                    else:
                                        propertyMaster.headerBlockValues[key[0],key[1],key[2]] = value
                                        
                                     
                                    break
                                    
                            for i, item in enumerate(dictionaryMeasurementList):
                                if  dictionaryMeasurementList[i].tag == key[0]:
                                    if key[2] == 'false':
                                        propertiesv2.loopBlockValues[key[0],key[1],key[2]] = value  
                                    else:
                                        propertyMaster.headerBlockValues[key[0],key[1],key[2]] = value
 
                                    break  
                                
                     
                                 
                    
                    print propertyMaster.headerBlockValues  
                    print propertiesv2.loopBlockValues
 
                print "add to list"
                
                
                
                added = checkList(propertiesv2,propertyMaster.propertyList)
                if not 'dictionaryValues' in request.session or not request.session['dictionaryValues' ]:  
                    pass
                else:
                    del request.session['dictionaryValues' ] 
                
                if added == 0:
                    warning2 = "Property previously added"
                else:
                    if samepointgroup:
                        propertyMaster.propertyList.append(propertiesv2)  
                                     
                    lengthlist =len(propertyMaster.propertyList) 
                     
                 
                request.session['propertyMaster']= propertyMaster    
 

                validationbyform = 0
                #ShowBtnSend=0
                print "valid"
                
            #add       
            if lengthlist == 0 and sucess==0 and len(inputListReadOnly) > 0:
                ShowBtnSend=0
            elif lengthlist == 0 and sucess==0 and len(inputListReadOnly) == 0:
                ShowBtnSend=1
            #send  
            elif lengthlist != 0 and sucess==0 and len(inputListReadOnly) == 0:
                ShowBtnSend=2
            #disabled    
            elif lengthlist != 0 and sucess==1 and len(inputListReadOnly) == 0:
                ShowBtnSend=3
                
       
                
            #print "lengthlist: " + str(lengthlist) + " sucess: " + str(  sucess ) + " inputListReadOnly: " + str(len(inputListReadOnly))
        
   
                    
        else:

            ShowBtnSend=1
            validationbyform = 1
            propertiesv2=Propertiesv2(catalogproperty_name,crystalsystem_name,typeselected,datapropertytagselected, chkBoxmge,request.POST)
            propertiesv2.NewProperties(pointgroupselected_name,axisselected_name)
            
            pointgroupselected_name = propertiesv2.pointgroupselected_name

            if  len(inputList) > 0:                
                for cpd in inputList:
                    value =request.POST.get(cpd.name, False)
                    if value != False:
                        #if value != "" :
                        inputListValues[cpd.name] = value


                inputListReadOnly = propertiesv2.catalogPropertyDetailReadOnly
                    
                 
                for row  in inputListReadOnly:
                    for col  in row:
                        if col in form.fields:
                            for field  in form:
                                if  field.name == col:
                                    if   field.errors:
                                        for error in field.errors:                                           
                                            for key,value in inputListValues.items():
                                                if col == key:
                                                    #print "correcto " + col +"=" + str(value)
                                                    pass
        
                                    else:
                                        #print "correcto " + str(col )
                                        for key,value in inputListValues.items():
                                            if col == key:
                                                #print "correcto " + col +"=" + str(value)
                                                pass
                                     
                                else:
                                    pass 
                                
                            
                                      
                        else:
                            print "correcto " + str(col )

            
            else:
                print  inputList
                print "invalid"
 
            
 
            
        return render_to_response('newcasev2.html', {   "form":form,
                                                                                             "propertyCategoryName":propertyCategoryName,
                                                                                             "catalogproperty_name":catalogproperty_name,
                                                                                             "catalogCrystalSystemList":catalogCrystalSystemList,
                                                                                             "pointGroupList":propertiesv2.pointGroupList,
                                                                                             "questionGp":propertiesv2.questionGp,
                                                                                             "axisList":propertiesv2.axisList, 
                                                                                             "questionAxis":propertiesv2.questionAxis, 
                                                                                             'message':propertiesv2.message,
                                                                                             'warning':warning,
                                                                                             'warning2':warning2,
                                                                                            "read_write_inputs":propertiesv2.read_write_inputs,
                                                                                             "inputListReadOnly":inputListReadOnly,
                                                                                             "jquery" :propertiesv2.jquery,
                                                                                             "inputListValues":inputListValues,
                                                                                             "pointgroupselected_name":pointgroupselected_name,
                                                                                             "axisselected_name":axisselected_name,
                                                                                             "typeList":typeList,
                                                                                             "inputList":inputList,
                                                                                             "crystalsystem_name":crystalsystem_name,
                                                                                             "questiontype":questiontype,
                                                                                             "typeselected":typeselected,
                                                                                             "ShowBtnSend":ShowBtnSend,
                                                                                             "validationbyform":validationbyform,
                                                                                             "current":current,
                                                                                             "lengthlist":lengthlist,                                                                                               
                                                                                             "dictionaryList":dictionaryList,      
                                                                                             "dictionaryPhaseList":dictionaryPhaseList,   
                                                                                             "dictionaryPhaseCharacteristicList":dictionaryPhaseCharacteristicList,   
                                                                                             "dictionaryMeasurementList":dictionaryMeasurementList,                                                                               
                                                                                             #"propertaddedmessage":propertaddedmessage,
                                                                                             "experimentalparcond_name_selected":experimentalparcond_name_selected,
                                                                                             #'propertySessionList':propertySessionList,
                                                                                             'propertyMaster':propertyMaster,
                                                                                             'chkBoxMagnetoelectricity':chkBoxMagnetoelectricity,
                                                                                             'dataPropertyList':dataPropertyList,
                                                                                             'datapropertytagselected':int(datapropertytagselected),
                                                                                             'magnetoelectricity':magnetoelectricity
                                                                                       }, context_instance=RequestContext(request))
      
def checkList(customobject,listProperty):
    result = 0
    def containsproperty(listObject, obj):
        result = False
        for x in listObject:
            print x.catalogproperty_name + " == " + obj.catalogproperty_name
            if x.catalogproperty_name ==obj.catalogproperty_name :  # elastic, piezolectric, etc.?
                print x.crystalsystem_name + " == " + obj.crystalsystem_name 
                if x.crystalsystem_name == obj.crystalsystem_name: #Triclinic, monoclinic, cubic, etc.
                    print x.type + " == " + obj.type
                    if x.type == obj.type:   # s (compliance) o c (stiffness)?
                        print x.dataproperty + " == " + obj.dataproperty 
                        if  x.dataproperty  ==  obj.dataproperty:   #Data Property Tag id
                            result= True
                            break
                            """if N.array_equal(x.coefficientsmatrix, obj.coefficientsmatrix):
                                print x.coefficientsmatrix 
                                print  " == " 
                                print obj.coefficientsmatrix 
                                result= True
                                break"""
                    
        return result        
    
    is_in_list=containsproperty(listProperty, customobject)  
    if is_in_list == False:

        print "objeto agregado a la lista" 
        #print request.session[nameObjectOnSession]
        result = 1
    else:
        print "objeto no agregado a la lista" 
        #print request.session[nameObjectOnSession]
           
    return result
    
    
def addToSession(request,customobject,nameObjectOnSession):
    result = 0
    def containsproperty(listObject, obj):
        result = False
        for x in listObject:
            print x.catalogproperty_name + " == " + obj.catalogproperty_name
            if x.catalogproperty_name ==obj.catalogproperty_name :
                print x.crystalsystem_name + " == " + obj.crystalsystem_name
                if x.crystalsystem_name == obj.crystalsystem_name:
                    print x.type + " == " + obj.type
                    if x.type == obj.type:
                        result= True
                        break
                    
        return result          
        
    sessionList=[]
     
    if not nameObjectOnSession in request.session or not request.session[nameObjectOnSession ]:  
            print "lista no esta en session" 
            sessionList.append(customobject)
            request.session[nameObjectOnSession ] =sessionList  
            #print request.session['nameObjectOnSession']
            result = 1
            
    else:
        print "lista si esta en session" 
        sessionList = request.session[nameObjectOnSession ]
        #print  len(sessionList)
        #np=newProperties
        is_in_list=containsproperty(sessionList, customobject)  
        if is_in_list == False:
            sessionList .append(customobject)
            request.session[nameObjectOnSession]= sessionList
            print "objeto agregado a la lista" 
            #print request.session[nameObjectOnSession]
            result = 1
        else:
            print "objeto no agregado a la lista" 
            #print request.session[nameObjectOnSession]
           
    return result
            
        



                
                  
             
               
     
    

######################################################################################
#                              ''' DOCUMENTATION '''
######################################################################################
def docintroduction(request):
    return render_to_response('docintroduction.html', context_instance=RequestContext(request))

def docmpodfiles(request):
    return render_to_response('docmpodfiles.html', context_instance=RequestContext(request))

def docdictionary(request):
    return render_to_response('docdictionary.html', context_instance=RequestContext(request))



def references(request):
    return render_to_response('references.html', context_instance=RequestContext(request))
######################################################################################
#                               ''' ABOUT MPOD '''
######################################################################################

def introduction(request):
    return render_to_response('introduction.html', context_instance=RequestContext(request))

def mpodteam(request):
    return render_to_response('mpodteam.html', context_instance=RequestContext(request))

def terms(request):
    return render_to_response('terms.html', context_instance=RequestContext(request))





