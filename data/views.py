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
            #return redirect('home')
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
        return redirect('/home/')
    
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
    ogge = Property.objects.all()
    properties_list_table_html = view_linked_properties_list(oggetti=ogge, header=None)
    return render_to_response('sbproperty.html', {"properties_list_table" : properties_list_table_html}, context_instance=RequestContext(request))

#-------------------------------------------------------------------------------------------

def viewproperty(request, property_id):
    ogge = None
    html_res = None
    html_res2 = None
    try:
        ogge = Property.objects.get(id__exact = property_id)
    except:
        pass
    if ogge:
        datafiles = DataFile.objects.filter(properties__id__exact = property_id)
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
    value11 = (request.GET.get('value11', ''))
    value12 = (request.GET.get('value12', ''))
    value13 = (request.GET.get('value13', ''))
    value21 = (request.GET.get('value21', ''))
    value22 = (request.GET.get('value22', ''))
    value23 = (request.GET.get('value23', ''))
    value31 = (request.GET.get('value31', ''))
    value32 = (request.GET.get('value32', ''))
    value33 = (request.GET.get('value33', ''))
    color = (request.GET.get('color', ''))
    filename = (request.GET.get('filename', ''))
    if(value11 and value12 and value13 and value21 and value22 and value23 and value31 and value32 and value33 and color):
        val11 = float(value11)
        val12 = float(value12)
        val13 = float(value13)
        val21 = float(value21)
        val22 = float(value22)
        val23 = float(value23)
        val31 = float(value31)
        val32 = float(value32)
        val33 = float(value33)
        color = int(color)
        filename = re.sub('[\s+]', '', filename)
        filename1 =None
        filename2 =None
        
        surfacecolorSecondRankTensor= None
        surfacecolorSecondRankTensorRotated= None
       
        valuearrayrotated =request.GET.getlist("valuearrayrotated")
       
        if color == 0:
            colorscale='Jet';
        elif color == 1:
            colorscale='Hot';
        elif color == 2:
            colorscale='Cool'
        elif color == 3:
            colorscale='Greys'; 
        
    
        
        
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


           
        
        #stl_dir=".\\media\\stlfiles\\"
        #stl_dir="/var/www/MPOD/media/stlfiles/"
        
       
        filename1 = filename +"R2LowResolution" + ".stl"
        filepath=os.path.join(stl_dir, filename1)
        res=1;
        createstl = 0;
        if pathexist == 1:
            if os.path.isfile(filepath):
                createstl = 0          
            else:
                createstl = 1
       
        createdata =  1
      
        tensor = RankTensors()
        tensor.SecondRankTensor(val11,val12,val13,val21,val22,val23,val31,val32,val33,color,filename1,res,stl_dir,createstl,createdata)
        XEC=tensor.stringValsOfXEC
        YEC = tensor.stringValsOfYEC
        ZEC= tensor.stringValsOfZEC
        surfacecolorSecondRankTensor=tensor.surfacecolorSecondRankTensor
        
        if valuearrayrotated:
            tensor.SecondRankTensorRotated(valuearrayrotated,color,filename1,res,stl_dir,createstl,createdata)
            XEC2=tensor.stringValsOfXEC2
            YEC2 = tensor.stringValsOfYEC2
            ZEC2= tensor.stringValsOfZEC2
            surfacecolorSecondRankTensorRotated=tensor.surfacecolorSecondRankTensorRotated
            
        del tensor
       
        filename2 = filename+"R2MidleResolution" + ".stl"
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
            tensor = RankTensors()
            tensor.SecondRankTensor(val11,val12,val13,val21,val22,val23,val31,val32,val33,color,filename2,res,stl_dir,createstl,createdata)         
            del tensor


        if valuearrayrotated:               
            return render_to_response('secondranktensor.html',{"XEC": XEC,
                                                                                                        "YEC":YEC,
                                                                                                        "ZEC": ZEC,
                                                                                                        "LowResolutionFileName":filename1,
                                                                                                        "MiddleResolutionFileName":filename2,
                                                                                                        'colorscale':colorscale,
                                                                                                        'surfacecolorSecondRankTensor':surfacecolorSecondRankTensor,                    
                                                                                                        "XEC2": XEC2,
                                                                                                        "YEC2":YEC2,
                                                                                                        "ZEC2": ZEC2,
                                                                                                        'surfacecolorSecondRankTensorRotated':surfacecolorSecondRankTensorRotated,}, context_instance=RequestContext(request))
        else:             
            return render_to_response('secondranktensor.html',{"XEC": XEC,"YEC":YEC,"ZEC": ZEC,"LowResolutionFileName":filename1,"MiddleResolutionFileName":filename2,'colorscale':colorscale,'surfacecolorSecondRankTensor':surfacecolorSecondRankTensor}, context_instance=RequestContext(request))

        
    #return render_to_response('secondranktensor.html', context_instance=RequestContext(request))

def viewthirdranktensordg(request):
    value11 = (request.GET.get('value11', ''))
    value12 = (request.GET.get('value12', ''))
    value13 = (request.GET.get('value13', ''))
    value14 = (request.GET.get('value14', ''))
    value15 = (request.GET.get('value15', ''))
    value16 = (request.GET.get('value16', ''))
    value21 = (request.GET.get('value21', ''))
    value22 = (request.GET.get('value22', ''))
    value23 = (request.GET.get('value23', ''))
    value24 = (request.GET.get('value24', ''))
    value25 = (request.GET.get('value25', ''))
    value26 = (request.GET.get('value26', ''))
    value31 = (request.GET.get('value31', ''))
    value32 = (request.GET.get('value32', ''))
    value33 = (request.GET.get('value33', ''))
    value34 = (request.GET.get('value34', ''))
    value35 = (request.GET.get('value35', ''))
    value36 = (request.GET.get('value36', ''))
    color = (request.GET.get('color', ''))
    filename = (request.GET.get('filename', ''))
    if(value11 and value12 and value13 and value14 and value15 and value16 and value21 and value22 and value23 and value24 and value25 and value26 and value31 and value32 and value33 and value34 and value35 and value36 and color):
        val11 = float(value11)
        val12 = float(value12)
        val13 = float(value13)
        val14 = float(value14)
        val15 = float(value15)
        val16 = float(value16)
        val21 = float(value21)
        val22 = float(value22)
        val23 = float(value23)
        val24 = float(value24)
        val25 = float(value25)
        val26 = float(value26)
        val31 = float(value31)
        val32 = float(value32)
        val33 = float(value33)
        val34 = float(value34)
        val35 = float(value35)
        val36 = float(value36)
        color = int(color)
        filename = re.sub('[\s+]', '', filename)
        filename1 =None
        filename2 =None
        
        
      
        
        valuearrayrotated =request.GET.getlist("valuearrayrotated")
        """for i,item in enumerate(valuearrayrotated):
            print valuearrayrotated[i]"""
        
         
        
 
        if color == 0:
            colorscale='Jet';
        elif color == 1:
            colorscale='Hot';
        elif color == 2:
            colorscale='Cool'
        elif color == 3:
            colorscale='Greys';
            
        tensor = RankTensors()    
        
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
      
      
        #stl_dir=".\\media\\stlfiles\\"
        #stl_dir="/var/www/MPOD/media/stlfile/"
    
        filename1 = filename+"R3LowResolution" + ".stl"
        filepath=os.path.join(stl_dir, filename1)
        
        res=1;
        createstl = 0;
        if pathexist == 1:
            if os.path.isfile(filepath):
                createstl = 0          
            else:
                createstl = 1
       
        createdata =  1
      
  
        tensor.ThirdRankTensordg(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,color,filename1,res,stl_dir,createstl,createdata)
        XEC=tensor.stringValsOfXEC
        YEC = tensor.stringValsOfYEC
        ZEC= tensor.stringValsOfZEC
        surfacecolorThirdRankTensor=tensor.surfacecolorThirdRankTensor
        
        if valuearrayrotated:
            tensor.ThirdRankTensorRotateddg(valuearrayrotated,color,filename1,res,stl_dir,createstl,createdata)
            XEC2=tensor.stringValsOfXEC2
            YEC2 = tensor.stringValsOfYEC2
            ZEC2= tensor.stringValsOfZEC2
            surfacecolorThirdRankTensorRotated=tensor.surfacecolorThirdRankTensorRotated
            
        
        del tensor
       
        filename2 = filename+"R3MidleResolution" + ".stl"
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
            tensor = RankTensors()
            tensor.ThirdRankTensordg(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,color,filename2,res,stl_dir,createstl,createdata)
            del tensor
         

        print filename1
        print filename2
        
        
        
        if valuearrayrotated:               
            return render_to_response('thirdranktensor.html',{"XEC": XEC,
                                                                                                        "YEC":YEC,
                                                                                                        "ZEC": ZEC,
                                                                                                        "LowResolutionFileName":filename1,
                                                                                                        "MiddleResolutionFileName":filename2,
                                                                                                        'colorscale':colorscale,
                                                                                                        'surfacecolorThirdRankTensor':surfacecolorThirdRankTensor,
                                                                                                        "XEC2": XEC2,
                                                                                                        "YEC2":YEC2,
                                                                                                        "ZEC2": ZEC2,
                                                                                                        'surfacecolorThirdRankTensorRotated':surfacecolorThirdRankTensorRotated,}, context_instance=RequestContext(request))
        else:
            return render_to_response('thirdranktensor.html',{"XEC": XEC,
                                                                                                        "YEC":YEC,
                                                                                                        "ZEC": ZEC,
                                                                                                        "LowResolutionFileName":filename1,
                                                                                                        "MiddleResolutionFileName":filename2,
                                                                                                        'colorscale':colorscale,
                                                                                                        'surfacecolorThirdRankTensor':surfacecolorThirdRankTensor,}, context_instance=RequestContext(request))


def viewthirdranktensoreh(request):
    value11 = (request.GET.get('value11', ''))
    value12 = (request.GET.get('value12', ''))
    value13 = (request.GET.get('value13', ''))
    value14 = (request.GET.get('value14', ''))
    value15 = (request.GET.get('value15', ''))
    value16 = (request.GET.get('value16', ''))
    value21 = (request.GET.get('value21', ''))
    value22 = (request.GET.get('value22', ''))
    value23 = (request.GET.get('value23', ''))
    value24 = (request.GET.get('value24', ''))
    value25 = (request.GET.get('value25', ''))
    value26 = (request.GET.get('value26', ''))
    value31 = (request.GET.get('value31', ''))
    value32 = (request.GET.get('value32', ''))
    value33 = (request.GET.get('value33', ''))
    value34 = (request.GET.get('value34', ''))
    value35 = (request.GET.get('value35', ''))
    value36 = (request.GET.get('value36', ''))
    color = (request.GET.get('color', ''))
    filename = (request.GET.get('filename', ''))
    if(value11 and value12 and value13 and value14 and value15 and value16 and value21 and value22 and value23 and value24 and value25 and value26 and value31 and value32 and value33 and value34 and value35 and value36 and color):
        val11 = float(value11)
        val12 = float(value12)
        val13 = float(value13)
        val14 = float(value14)
        val15 = float(value15)
        val16 = float(value16)
        val21 = float(value21)
        val22 = float(value22)
        val23 = float(value23)
        val24 = float(value24)
        val25 = float(value25)
        val26 = float(value26)
        val31 = float(value31)
        val32 = float(value32)
        val33 = float(value33)
        val34 = float(value34)
        val35 = float(value35)
        val36 = float(value36)
        color = int(color)
        filename = re.sub('[\s+]', '', filename)
        filename1 =None
        filename2 =None
        
        
      
        
        valuearrayrotated =request.GET.getlist("valuearrayrotated")
        """for i,item in enumerate(valuearrayrotated):
            print valuearrayrotated[i]"""
        
         
        
 
        if color == 0:
            colorscale='Jet';
        elif color == 1:
            colorscale='Hot';
        elif color == 2:
            colorscale='Cool'
        elif color == 3:
            colorscale='Greys';
            
        tensor = RankTensors()    
        
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
      
      
        #stl_dir=".\\media\\stlfiles\\"
        #stl_dir="/var/www/MPOD/media/stlfile/"
    
        filename1 = filename+"R3LowResolution" + ".stl"
        filepath=os.path.join(stl_dir, filename1)
        
        res=1;
        createstl = 0;
        if pathexist == 1:
            if os.path.isfile(filepath):
                createstl = 0          
            else:
                createstl = 1
       
        createdata =  1
      
  
        tensor.ThirdRankTensoreh(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,color,filename1,res,stl_dir,createstl,createdata)
        XEC=tensor.stringValsOfXEC
        YEC = tensor.stringValsOfYEC
        ZEC= tensor.stringValsOfZEC
        surfacecolorThirdRankTensor=tensor.surfacecolorThirdRankTensor
        
        if valuearrayrotated:
            tensor.ThirdRankTensorRotatedeh(valuearrayrotated,color,filename1,res,stl_dir,createstl,createdata)
            XEC2=tensor.stringValsOfXEC2
            YEC2 = tensor.stringValsOfYEC2
            ZEC2= tensor.stringValsOfZEC2
            surfacecolorThirdRankTensorRotated=tensor.surfacecolorThirdRankTensorRotated
            
        
        del tensor
       
        filename2 = filename+"R3MidleResolution" + ".stl"
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
            tensor = RankTensors()
            tensor.ThirdRankTensoreh(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,color,filename2,res,stl_dir,createstl,createdata)
            del tensor
 
        
        
        if valuearrayrotated:               
            return render_to_response('thirdranktensor.html',{"XEC": XEC,
                                                                                                        "YEC":YEC,
                                                                                                        "ZEC": ZEC,
                                                                                                        "LowResolutionFileName":filename1,
                                                                                                        "MiddleResolutionFileName":filename2,
                                                                                                        'colorscale':colorscale,
                                                                                                        'surfacecolorThirdRankTensor':surfacecolorThirdRankTensor,
                                                                                                        "XEC2": XEC2,
                                                                                                        "YEC2":YEC2,
                                                                                                        "ZEC2": ZEC2,
                                                                                                        'surfacecolorThirdRankTensorRotated':surfacecolorThirdRankTensorRotated,}, context_instance=RequestContext(request))
        else:
            return render_to_response('thirdranktensor.html',{"XEC": XEC,
                                                                                                        "YEC":YEC,
                                                                                                        "ZEC": ZEC,
                                                                                                        "LowResolutionFileName":filename1,
                                                                                                        "MiddleResolutionFileName":filename2,
                                                                                                        'colorscale':colorscale,
                                                                                                        'surfacecolorThirdRankTensor':surfacecolorThirdRankTensor,}, context_instance=RequestContext(request))

 
 

def viewcompliance(request):

    valuearrayrotated =request.GET.getlist("valuearrayrotated")
    poly ="0"
    if not valuearrayrotated:
    
        val11 = float(request.GET.get('value11', ''))
        val12 = float(request.GET.get('value12', ''))
        val13 = float(request.GET.get('value13', ''))
        val14 = float(request.GET.get('value14', ''))
        val15 = float(request.GET.get('value15', ''))
        val16 = float(request.GET.get('value16', ''))
        val21 = float(request.GET.get('value21', ''))
        val22 = float(request.GET.get('value22', ''))
        val23 = float(request.GET.get('value23', ''))
        val24 = float(request.GET.get('value24', ''))
        val25 = float(request.GET.get('value25', ''))
        val26 = float(request.GET.get('value26', ''))
        val31 = float(request.GET.get('value31', ''))
        val32 = float(request.GET.get('value32', ''))
        val33 = float(request.GET.get('value33', ''))
        val34 = float(request.GET.get('value34', ''))
        val35 = float(request.GET.get('value35', ''))
        val36 = float(request.GET.get('value36', ''))
        val41 = float(request.GET.get('value41', ''))
        val42 = float(request.GET.get('value42', ''))
        val43 = float(request.GET.get('value43', ''))
        val44 = float(request.GET.get('value44', ''))
        val45 = float(request.GET.get('value45', ''))
        val46 = float(request.GET.get('value46', ''))
        val51 = float(request.GET.get('value51', ''))
        val52 = float(request.GET.get('value52', ''))
        val53 = float(request.GET.get('value53', ''))
        val54 = float(request.GET.get('value54', ''))
        val55 = float(request.GET.get('value55', ''))
        val56 = float(request.GET.get('value56', ''))
        val61 = float(request.GET.get('value61', ''))
        val62 = float(request.GET.get('value62', ''))
        val63 = float(request.GET.get('value63', ''))
        val64 = float(request.GET.get('value64', ''))
        val65 = float(request.GET.get('value65', ''))
        val66 = float(request.GET.get('value66', ''))
        filename = (request.GET.get('filename', ''))    
        filename = re.sub('[\s+]', '', filename)   
 
    else:
        val11 = float(valuearrayrotated[0])
        val12 = float(valuearrayrotated[1])
        val13 = float(valuearrayrotated[2])
        val14 = float(valuearrayrotated[3])
        val15 = float(valuearrayrotated[4])
        val16 = float(valuearrayrotated[5])
        val21 = float(valuearrayrotated[6])
        val22 = float(valuearrayrotated[7])
        val23 = float(valuearrayrotated[8])
        val24 = float(valuearrayrotated[9])
        val25 = float(valuearrayrotated[10])
        val26 = float(valuearrayrotated[11])
        val31 = float(valuearrayrotated[12])
        val32 = float(valuearrayrotated[13])
        val33 = float(valuearrayrotated[14])
        val34 = float(valuearrayrotated[15])
        val35 = float(valuearrayrotated[16])
        val36 = float(valuearrayrotated[17])
        val41 = float(valuearrayrotated[18])
        val42 = float(valuearrayrotated[19])
        val43 = float(valuearrayrotated[20])
        val44 = float(valuearrayrotated[21])
        val45 = float(valuearrayrotated[22])
        val46 = float(valuearrayrotated[23])
        val51 = float(valuearrayrotated[24])
        val52 = float(valuearrayrotated[25])
        val53 = float(valuearrayrotated[26])
        val54 = float(valuearrayrotated[27])
        val55 = float(valuearrayrotated[28])
        val56 = float(valuearrayrotated[29])
        val61 = float(valuearrayrotated[30])
        val62 = float(valuearrayrotated[31])
        val63 = float(valuearrayrotated[32])
        val64 = float(valuearrayrotated[33])
        val65 = float(valuearrayrotated[34])
        val66 = float(valuearrayrotated[35])
        filename = (request.GET.get('filename', ''))
        filename = re.sub('[\s+]', '', filename) + "policrystal"
        poly = "1"
        
        
    color = int(request.GET.get('color', ''))

        
        
    if color == 0:
        colorscale='Jet';
    elif color == 1:
        colorscale='Hot';
    elif color == 2:
        colorscale='Cool'
    elif color == 3:
        colorscale='Greys';

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
        
    
    filename1 = filename + "LowResolution" + ".stl"
    print filename1
    filepath=os.path.join(stl_dir, filename1)
    res=1;
    createstl = 0;
    if pathexist == 1:
        if os.path.isfile(filepath):
            createstl = 0          
        else:
            createstl = 1
  
    createdata =  1
    compliance = ComplianceT4()
    compliance.Compliance(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,val41,val42,val43,val44,val45,val46,val51,val52,val53,val54,val55,val56,val61,val62,val63,val64,val65,val66,color,filename1,res,stl_dir,createstl,createdata) 
    XEC=compliance.stringValsOfXEC
    YEC = compliance.stringValsOfYEC
    ZEC= compliance.stringValsOfZEC
   
    surfacecolorcompliance=   compliance.surfacecolorcompliance
    #colorscale=compliance.colorscale

    filenameYoungModulus = filename + "YoungModulusLowResolution" + ".stl"
    print filenameYoungModulus
    filepath=os.path.join(stl_dir, filenameYoungModulus)
    res=1;
    createstl = 0;
    if pathexist == 1:
        if os.path.isfile(filepath):
            createstl = 0          
        else:
            createstl = 1
  
    compliance.YoungModulus(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,val41,val42,val43,val44,val45,val46,val51,val52,val53,val54,val55,val56,val61,val62,val63,val64,val65,val66,color,filenameYoungModulus,res,stl_dir,createstl,createdata)
    youngModulusXEC=compliance.stringValsOfXEC2
    youngModulusYEC = compliance.stringValsOfYEC2
    youngModulusZEC= compliance.stringValsOfZEC2    
    surfacecolorYoungModulus=   compliance.surfacecolorYoungModulus 
    del compliance

  
    filename2 = filename + "MidleResolution" + ".stl"
    print filename2
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
        compliance = ComplianceT4()
        compliance.Compliance(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,val41,val42,val43,val44,val45,val46,val51,val52,val53,val54,val55,val56,val61,val62,val63,val64,val65,val66,color,filename2,res,stl_dir,createstl,createdata)        
        del compliance


                  
    return render_to_response('compliance.html',{"XEC": XEC,"YEC":YEC,"ZEC": ZEC,"youngModulusXEC": youngModulusXEC,"youngModulusYEC": youngModulusYEC,"youngModulusZEC": youngModulusZEC,"LowResolutionFileName":filename1,"MiddleResolutionFileName":filename2,"LowResolutionFilenameYoungModulus":filenameYoungModulus,"surfacecolorcompliance":surfacecolorcompliance,"surfacecolorYoungModulus":surfacecolorYoungModulus,"colorscale":colorscale,"poly":poly}, context_instance=RequestContext(request))
        #return render_to_response('compliance.html', context_instance=RequestContext(request))

def viewstiffness(request):
    valuearrayrotated =request.GET.getlist("valuearrayrotated")
    poly = "0"
    if not valuearrayrotated:
        val11 = float(request.GET.get('value11', ''))
        val12 = float(request.GET.get('value12', ''))
        val13 = float(request.GET.get('value13', ''))
        val14 = float(request.GET.get('value14', ''))
        val15 = float(request.GET.get('value15', ''))
        val16 = float(request.GET.get('value16', ''))
        val21 = float(request.GET.get('value21', ''))
        val22 = float(request.GET.get('value22', ''))
        val23 = float(request.GET.get('value23', ''))
        val24 = float(request.GET.get('value24', ''))
        val25 = float(request.GET.get('value25', ''))
        val26 = float(request.GET.get('value26', ''))
        val31 = float(request.GET.get('value31', ''))
        val32 = float(request.GET.get('value32', ''))
        val33 = float(request.GET.get('value33', ''))
        val34 = float(request.GET.get('value34', ''))
        val35 = float(request.GET.get('value35', ''))
        val36 = float(request.GET.get('value36', ''))
        val41 = float(request.GET.get('value41', ''))
        val42 = float(request.GET.get('value42', ''))
        val43 = float(request.GET.get('value43', ''))
        val44 = float(request.GET.get('value44', ''))
        val45 = float(request.GET.get('value45', ''))
        val46 = float(request.GET.get('value46', ''))
        val51 = float(request.GET.get('value51', ''))
        val52 = float(request.GET.get('value52', ''))
        val53 = float(request.GET.get('value53', ''))
        val54 = float(request.GET.get('value54', ''))
        val55 = float(request.GET.get('value55', ''))
        val56 = float(request.GET.get('value56', ''))
        val61 = float(request.GET.get('value61', ''))
        val62 = float(request.GET.get('value62', ''))
        val63 = float(request.GET.get('value63', ''))
        val64 = float(request.GET.get('value64', ''))
        val65 = float(request.GET.get('value65', ''))
        val66 = float(request.GET.get('value66', ''))
        filename = (request.GET.get('filename', ''))
        filename = re.sub('[\s+]', '', filename)
        
    else:
        val11 = float(valuearrayrotated[0])
        val12 = float(valuearrayrotated[1])
        val13 = float(valuearrayrotated[2])
        val14 = float(valuearrayrotated[3])
        val15 = float(valuearrayrotated[4])
        val16 = float(valuearrayrotated[5])
        val21 = float(valuearrayrotated[6])
        val22 = float(valuearrayrotated[7])
        val23 = float(valuearrayrotated[8])
        val24 = float(valuearrayrotated[9])
        val25 = float(valuearrayrotated[10])
        val26 = float(valuearrayrotated[11])
        val31 = float(valuearrayrotated[12])
        val32 = float(valuearrayrotated[13])
        val33 = float(valuearrayrotated[14])
        val34 = float(valuearrayrotated[15])
        val35 = float(valuearrayrotated[16])
        val36 = float(valuearrayrotated[17])
        val41 = float(valuearrayrotated[18])
        val42 = float(valuearrayrotated[19])
        val43 = float(valuearrayrotated[20])
        val44 = float(valuearrayrotated[21])
        val45 = float(valuearrayrotated[22])
        val46 = float(valuearrayrotated[23])
        val51 = float(valuearrayrotated[24])
        val52 = float(valuearrayrotated[25])
        val53 = float(valuearrayrotated[26])
        val54 = float(valuearrayrotated[27])
        val55 = float(valuearrayrotated[28])
        val56 = float(valuearrayrotated[29])
        val61 = float(valuearrayrotated[30])
        val62 = float(valuearrayrotated[31])
        val63 = float(valuearrayrotated[32])
        val64 = float(valuearrayrotated[33])
        val65 = float(valuearrayrotated[34])
        val66 = float(valuearrayrotated[35])
        filename = (request.GET.get('filename', ''))
        filename = re.sub('[\s+]', '', filename) + "polycrystal"
        poly = "1"
    
    
    color = int(request.GET.get('color', ''))
    
                            
    if color == 0:
        colorscale='Jet'
    elif color == 1:
        colorscale='Hot'
    elif color == 2:        
        colorscale='Cool'
    elif color == 3:
        colorscale='Greys'
            
            
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
           
                  
    #stl_dir=".\\media\\stlfiles\\"    
    
    
    filename1 =  filename +"LowResolution" + ".stl"
    filepath=os.path.join(stl_dir, filename1)
    res=1;
    createstl = 0;
    if pathexist == 1:
        if os.path.isfile(filepath):
            createstl = 0          
        else:
            createstl = 1
   
    createdata =  1
    stiffness = StiffnessT4()
    stiffness.Stiffness(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,val41,val42,val43,val44,val45,val46,val51,val52,val53,val54,val55,val56,val61,val62,val63,val64,val65,val66,color,filename1,res,stl_dir,createstl,createdata) 
    XEC=stiffness.stringValsOfXEC
    YEC = stiffness.stringValsOfYEC
    ZEC= stiffness.stringValsOfZEC
    surfacecolorstiffness=   stiffness.surfacecolorstiffness
    
    
    filenameYoungModulus = filename + "YoungModulusLowResolution" + ".stl"
    print filenameYoungModulus
    filepath=os.path.join(stl_dir, filenameYoungModulus)
    res=1;
    createstl = 0;
    if pathexist == 1:
        if os.path.isfile(filepath):
            createstl = 0          
        else:
            createstl = 1 
            
            
    stiffness.YoungModulus(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,val41,val42,val43,val44,val45,val46,val51,val52,val53,val54,val55,val56,val61,val62,val63,val64,val65,val66,color,filenameYoungModulus,res,stl_dir,createstl,createdata)
    youngModulusXEC=stiffness.stringValsOfXEC2
    youngModulusYEC = stiffness.stringValsOfYEC2
    youngModulusZEC= stiffness.stringValsOfZEC2    
    surfacecolorYoungModulus=   stiffness.surfacecolorYoungModulus 
    del stiffness

 
    #filename = "ejemplo7StiffnessMidleResolution" + ".stl"
    filename2=  filename+"MiddleResolution" + ".stl"
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
        stiffness = StiffnessT4()
        stiffness.Stiffness (val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,val41,val42,val43,val44,val45,val46,val51,val52,val53,val54,val55,val56,val61,val62,val63,val64,val65,val66,color,filename2,res,stl_dir,createstl,createdata)        
        del stiffness
    
    
  
    return render_to_response('stiffness.html',{"XEC": XEC,"YEC":YEC,"ZEC": ZEC,"youngModulusXEC": youngModulusXEC,"youngModulusYEC": youngModulusYEC,"youngModulusZEC": youngModulusZEC,"LowResolutionFileName":filename1,"MiddleResolutionFileName":filename2,"LowResolutionFilenameYoungModulus":filenameYoungModulus,"surfacecolorstiffness":surfacecolorstiffness,"surfacecolorYoungModulus":surfacecolorYoungModulus,"colorscale":colorscale,"poly":poly}, context_instance=RequestContext(request))
        

def viewfourthranktensor(request):
    value11 = (request.GET.get('value11', ''))
    value12 = (request.GET.get('value12', ''))
    value13 = (request.GET.get('value13', ''))
    value14 = (request.GET.get('value14', ''))
    value15 = (request.GET.get('value15', ''))
    value16 = (request.GET.get('value16', ''))
    value21 = (request.GET.get('value21', ''))
    value22 = (request.GET.get('value22', ''))
    value23 = (request.GET.get('value23', ''))
    value24 = (request.GET.get('value24', ''))
    value25 = (request.GET.get('value25', ''))
    value26 = (request.GET.get('value26', ''))
    value31 = (request.GET.get('value31', ''))
    value32 = (request.GET.get('value32', ''))
    value33 = (request.GET.get('value33', ''))
    value34 = (request.GET.get('value34', ''))
    value35 = (request.GET.get('value35', ''))
    value36 = (request.GET.get('value36', ''))
    value41 = (request.GET.get('value41', ''))
    value42 = (request.GET.get('value42', ''))
    value43 = (request.GET.get('value43', ''))
    value44 = (request.GET.get('value44', ''))
    value45 = (request.GET.get('value45', ''))
    value46 = (request.GET.get('value46', ''))
    value51 = (request.GET.get('value51', ''))
    value52 = (request.GET.get('value52', ''))
    value53 = (request.GET.get('value53', ''))
    value54 = (request.GET.get('value54', ''))
    value55 = (request.GET.get('value55', ''))
    value56 = (request.GET.get('value56', ''))
    value61 = (request.GET.get('value61', ''))
    value62 = (request.GET.get('value62', ''))
    value63 = (request.GET.get('value63', ''))
    value64 = (request.GET.get('value64', ''))
    value65 = (request.GET.get('value65', ''))
    value66 = (request.GET.get('value66', ''))
    color = (request.GET.get('color', ''))
    filename = (request.GET.get('filename', ''))
    if(value11 and value12 and value13 and value14 and value15 and value16 and value21 and value22 and value23 and value24 and value25 and value26 and value31 and value32 and value33 and value34 and value35 and value36 and value41 and value42 and value43 and value44 and value45 and value46 and value51 and value52 and value53 and value54 and value55 and value56 and value61 and value62 and value63 and value64 and value65 and value66 and color):
        val11 = float(value11)
        val12 = float(value12)
        val13 = float(value13)
        val14 = float(value14)
        val15 = float(value15)
        val16 = float(value16)
        val21 = float(value21)
        val22 = float(value22)
        val23 = float(value23)
        val24 = float(value24)
        val25 = float(value25)
        val26 = float(value26)
        val31 = float(value31)
        val32 = float(value32)
        val33 = float(value33)
        val34 = float(value34)
        val35 = float(value35)
        val36 = float(value36)
        val41 = float(value41)
        val42 = float(value42)
        val43 = float(value43)
        val44 = float(value44)
        val45 = float(value45)
        val46 = float(value46)
        val51 = float(value51)
        val52 = float(value52)
        val53 = float(value53)
        val54 = float(value54)
        val55 = float(value55)
        val56 = float(value56)
        val61 = float(value61)
        val62 = float(value62)
        val63 = float(value63)
        val64 = float(value64)
        val65 = float(value65)
        val66 = float(value66)
        color = int(color)
        filename = re.sub('[\s+]', '', filename)
        
        if color == 0:
            colorscale='Jet';
        elif color == 1:
            colorscale='Hot';
        elif color == 2:
            colorscale='Cool'
        elif color == 3:
            colorscale='Greys';

        tensor = RankTensors()
        
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
           
        #stl_dir=".\\media\\stlfiles\\"
       
        filename1 = filename+"R4LowResolution" + ".stl"
        filepath=os.path.join(stl_dir, filename1)
        res=1;
        createstl = 0;
        if pathexist == 1:
            if os.path.isfile(filepath):
                createstl = 0          
            else:
                createstl = 1
      
        createdata =  1
        tensor.FourthRankTensor(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,val41,val42,val43,val44,val45,val46,val51,val52,val53,val54,val55,val56,val61,val62,val63,val64,val65,val66,color,filename1,res,stl_dir,createstl,createdata)
          

        XEC=tensor.stringValsOfXEC
        YEC = tensor.stringValsOfYEC
        ZEC= tensor.stringValsOfZEC
        surfacecolorFourthRankTensor= tensor.surfacecolorFourthRankTensor
      
        del tensor

        filename2 = filename+"R4MiddleResolution" + ".stl"
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
            tensor = RankTensors()
            tensor.FourthRankTensor(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,val41,val42,val43,val44,val45,val46,val51,val52,val53,val54,val55,val56,val61,val62,val63,val64,val65,val66,color,filename2,res,stl_dir,createstl,createdata)
            del tensor       


                        
        return render_to_response('fourthranktensor.html',{"XEC": XEC,"YEC":YEC,"ZEC": ZEC,"LowResolutionFileName":filename1,"MiddleResolutionFileName":filename2,'colorscale':colorscale,'surfacecolorFourthRankTensor':surfacecolorFourthRankTensor}, context_instance=RequestContext(request))
        
def viewmagnetocrystallineanisotropy(request):
        value11 = (request.GET.get('value11', ''))
        value12 = (request.GET.get('value12', ''))
        filename = (request.GET.get('filename', ''))
        color = (request.GET.get('color', ''))
        filename = (request.GET.get('filename', ''))
        promertyname=(request.GET.get('promertyname', ''))
        if(value11 and value12 and color):
            val11 = float(value11)
            val12 = float(value12)
        
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
        

        magneto.MagnetocrystallineAnisotropy(val11, val12, color, filename1, res, stl_dir, createstl, createdata);
        
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
            magneto.MagnetocrystallineAnisotropy(val11, val12, color, filename2, res, stl_dir, createstl, createdata);
            
            del magneto 
    
        return render_to_response('magneto.html',{"XEC": XEC,"YEC":YEC,"ZEC": ZEC,"LowResolutionFileName":filename1,"MiddleResolutionFileName":filename2,'promertyname':promertyname,'colorscale':colorscale,'surfacecolorMagnetic':surfacecolorMagnetic}, context_instance=RequestContext(request))

    
def viewmagnetostriction(request):
    
    
        value11 = (request.GET.get('value11', ''))
        value12 = (request.GET.get('value12', ''))
        filename = (request.GET.get('filename', ''))
        color = (request.GET.get('color', ''))
        filename = (request.GET.get('filename', ''))
        promertyname=(request.GET.get('promertyname', ''))
        if(value11 and value12 and color):
            val11 = float(value11)
            val12 = float(value12)
        
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
        

        magneto.MagnetoStriction(val11, val12, color, filename1, res, stl_dir, createstl, createdata);
        
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
            magneto.MagnetoStriction(val11, val12, color, filename2, res, stl_dir, createstl, createdata);            
            del magneto 
            
            
            
    
        return render_to_response('magneto.html',{"XEC": XEC,"YEC":YEC,"ZEC": ZEC,"LowResolutionFileName":filename1,"MiddleResolutionFileName":filename2,'promertyname':promertyname,'colorscale':colorscale,'surfacecolorMagnetic':surfacecolorMagnetic}, context_instance=RequestContext(request))

 



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
    ogge = ExperimentalParCond.objects.filter(id__exact = exparcond_id).distinct()
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
        res_obj = DataFile.objects.filter(name_set)

    if formula_q:
        formula_set = Q(chemical_formula__icontains=formula_q)
        if res_obj:
            res_obj = res_obj.filter(formula_set)
        else:
            res_obj = DataFile.objects.filter(formula_set)
    
    if publ_author_q:
        author_set = Q(publication__authors__icontains=publ_author_q)
        if res_obj:
            res_obj = res_obj.filter(author_set)
        else:
            res_obj = DataFile.objects.filter(author_set)

    if mpod_code_q:
        try:
            mpod_code_set = Q(code__icontains = int(mpod_code_q))
            res_obj = DataFile.objects.filter(mpod_code_set)
        except:
            pass

    if cod_code_q:
        try:
            cod_code_set = Q(cod_code__exact = int(cod_code_q))
            res_obj = DataFile.objects.filter(cod_code_set)
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





@login_required(login_url="/login/")
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
    puntualGroupList=''
    inputList=''
    questionAxis=''
    message=""
    axisselected_name=""
    
    
    
    catalogCrystalSystemList = [];
    list_CatalogCrystalSystem= CatalogCrystalSystem.objects.filter(catalogproperty=propertyCategoryName[0],active=True)
    for register_catalogCrystalSystem in list_CatalogCrystalSystem: 
        objCatalogCrystalSystem=CatalogCrystalSystem();
        objCatalogCrystalSystem = register_catalogCrystalSystem
        catalogCrystalSystemList.append(objCatalogCrystalSystem)   
        del objCatalogCrystalSystem
        
    if 'catalogCrystalSystemListOnSession' not in request.session  or not request.session['catalogCrystalSystemListOnSession']:
        request.session['catalogCrystalSystemListOnSession']=catalogCrystalSystemList
   
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
    
    
     
    ids=CatalogProperty.objects.filter(active=True,name=catalogproperty_name).values_list('id', flat=True)    
    type_ids=Type.objects.filter(catalogproperty_id__in=ids,active=True, name=typeselected).values_list('id',flat=True)    
    data_property_ids=TypeDataProperty.objects.filter(type_id__in=type_ids).values_list('dataproperty_id',flat=True)    
    dataPropertyList=Property.objects.filter(id__in=data_property_ids)
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
    
    if todo == 'show' and int(index) == -2 :
        if not 'propertySessionList' in request.session or not request.session['propertySessionList']:
            pass
        elif  'propertySessionList' in request.session or  request.session['propertySessionList']:
            propertySessionList = request.session['propertySessionList']
            print "show "
            
            
    if todo == 'remove' and int(index)  > 0:
        if  'propertySessionList' in request.session or  request.session['propertySessionList']:
            propertySessionList = request.session['propertySessionList']
            try:
                print "remove: " + index
                #print propertySessionList[int(index)-1]
                del propertySessionList[int(index)-1]       
                request.session['propertySessionList']=propertySessionList              
            except ValueError:
                pass  
            
    if todo == 'removeall' and int(index)  == -1 :
        if  'propertySessionList' in request.session or  request.session['propertySessionList']:
                propertySessionList = request.session['propertySessionList']
                try:
                    print "removeall "
                    del request.session['propertySessionList']     
                    propertySessionList = []
                except ValueError:
                    pass  
        
        
        
                
    if todo == 'save' and  int(index) == -2:
        if not 'propertySessionList' in request.session or not request.session['propertySessionList']:
            propertySessionList=[]
        elif  'propertySessionList' in request.session or  request.session['propertySessionList']:
                propertySessionList = request.session['propertySessionList']
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
                                      
                    
                    if 'newDictionaryList' not in request.session  or not request.session['newDictionaryList']:
                        pass
                    else:
                        newDictionaryList =  request.session['newDictionaryList']
                        for d in newDictionaryList:
                            print d.tag
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
                            
                            
                    mpodutil=MPODUtil()
                    mpodutil.mpodwrite(filename,propertySessionList)
                    mpodutil.addinfo()
                    mpodutil.adddatavalue()                
                    mpodutil.savefile()
                    
 
                             
                        
                    
                    

                    
                    u= User()
                    u=user
                    fileuser = FileUser()
                    fileuser.filename=mpodutil.cif_created
                    fileuser.authuser=u 
                    fileuser.reportvalidation = mpodutil.reportValidation
                    fileuser.save()
                    
                    
                    
                    #uid= base64.b64encode(force_bytes(str(user.pk))),
                    #token= account_activation_token.make_token(user)
                    datafilescreated ="datafilescreated"
                    forwardslash="/"
                    #request.session['cif_created']=mpodutil.cif_created
    
                    #linkactivate = os.path.join(datafilescreated,forwardslash)
                   
                    
                    current_site = get_current_site(request)
                    
                    
                    messageCategoryDetailQuerySet1=MessageCategoryDetail.objects.filter(messagecategory=MessageCategory.objects.get(pk=3))#3 for category staff notification
                    #messageMailQuerySet1= MessageMail.objects.filter(pk=messageCategoryDetail1.message.pk)
                    
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
                            email.send()
                            
                            
                            
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
                            email.send()
                            
                            
                    del request.session['propertySessionList']     
                except ValueError:
                    pass
                
    
      
    if todo == 'removeall' and  int(index) == -1: 
        current ="New Case"           
        propertySessionList = []
  
        response = redirect('/newcasev2')
    
    if todo == 'save' and  int(index) == -2:    
        if len(propertySessionList)  > 0:
            
            current ="File created and sent"
            response = render_to_response('account/successfile.html', {"propertySessionList":propertySessionList,
                                                                                                                    "current":current, }, context_instance=RequestContext(request))        
  
            
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

@login_required
@csrf_exempt 
def adddictionaryphase(request,pk): 
    response = None
    todo  = request.POST.get('todo', False)
    dicvalue = request.POST.get('phasevalue', False)
    in_list = False
    error =""
    dictionary_pk =  request.POST.get('dictionary_pk', False) 
    objDictionarySelected = Dictionary.objects.get(pk=dictionary_pk) 
    if dicvalue != "":
        if objDictionarySelected.type == "numb":
            if not isnumber(dicvalue):
                error ="The value must be numeric" 
            elif objDictionarySelected.type == "char":
                pass
    else:
        error ="the field can not be empty"

    if error!= "":
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
        pass
    elif  pk == '-1' and todo == "addphase":
        if not 'dictionaryValues' in request.session or not request.session['dictionaryValues' ]:                 
            dictionaryValues = {}
            dictionaryValues[objDictionarySelected.tag.encode("ascii"),objDictionarySelected.type]=dicvalue.encode("ascii")
            request.session['dictionaryValues' ] = dictionaryValues
        else:
            dictionaryValues=request.session['dictionaryValues' ] 
            if objDictionarySelected.tag.encode("ascii") in dictionaryValues:
                in_list = True
            else:
                in_list = False
                dictionaryValues[objDictionarySelected.tag.encode("ascii"),objDictionarySelected.type]=dicvalue.encode("ascii")
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

@csrf_exempt 
def rotatematrix(request,pk): 
 
    
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
        print len(rowrotated)  
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


@login_required
@csrf_exempt 
def adddictionaryphasecharacteristic(request,pk): 
    response = None
    todo  = request.POST.get('todo', False)
    dicvalue = request.POST.get('phasecharacteristicvalue', False)
    in_list = False
    error =""
    dictionary_pk =  request.POST.get('dictionary_pk', False)     
    objDictionarySelected = Dictionary.objects.get(pk=dictionary_pk) 
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

    if pk == '-1' and todo == "phasecharacteristicchange":
        pass
    elif  pk == '-1' and todo == "addphasecharacteristic":
        if not 'dictionaryValues' in request.session or not request.session['dictionaryValues' ]:                 
            dictionaryValues = {}
            dictionaryValues[objDictionarySelected.tag.encode("ascii"),objDictionarySelected.type]=dicvalue.encode("ascii")
            request.session['dictionaryValues' ] = dictionaryValues
        else:
            dictionaryValues=request.session['dictionaryValues' ] 
            if objDictionarySelected.tag.encode("ascii") in dictionaryValues:
                in_list = True
            else:
                in_list = False
                dictionaryValues[objDictionarySelected.tag.encode("ascii"),objDictionarySelected.type]=dicvalue.encode("ascii")
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
def adddictionarymeasurement(request,pk): 
    response = None
    todo  = request.POST.get('todo', False)
    dicvalue = request.POST.get('measurementvalue', False)
    in_list = False
    error =""
    dictionary_pk =  request.POST.get('dictionary_pk', False) 
    objDictionarySelected = Dictionary.objects.get(pk=dictionary_pk) 
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

    if pk == '-1' and todo == "measurementchange":
        pass
    elif  pk == '-1' and todo == "addmeasurement":
        if not 'dictionaryValues' in request.session or not request.session['dictionaryValues' ]:                 
            dictionaryValues = {}
            dictionaryValues[objDictionarySelected.tag.encode("ascii"),objDictionarySelected.type]=dicvalue.encode("ascii")
            request.session['dictionaryValues' ] = dictionaryValues
        else:
            dictionaryValues=request.session['dictionaryValues' ] 
            if objDictionarySelected.tag.encode("ascii") in dictionaryValues:
                in_list = True
            else:
                in_list = False
                dictionaryValues[objDictionarySelected.tag.encode("ascii"),objDictionarySelected.type]=dicvalue.encode("ascii")
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
def adddictionaryproperty(request,pk):
    #response= None
    todo  = request.POST.get('todo', False)
    dicvalue = request.POST.get('dicvalue', False)
    in_list = False
    error =""
    dictionary_pk =  request.POST.get('dictionary_pk', False) 
    objDictionarySelected = Dictionary.objects.get(pk=dictionary_pk) 
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
            dictionaryValues[objDictionarySelected.tag.encode("ascii"),objDictionarySelected.type]=dicvalue.encode("ascii")
            request.session['dictionaryValues' ] = dictionaryValues
        else:
            dictionaryValues=request.session['dictionaryValues' ] 
            if objDictionarySelected.tag.encode("ascii") in dictionaryValues:
                in_list = True
            else:
                in_list = False
                dictionaryValues[objDictionarySelected.tag.encode("ascii"),objDictionarySelected.type]=dicvalue.encode("ascii")
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
        coefficientsparts = []
        if 'inputList' not in request.session  or not request.session['inputList']:
            pass
        else:
            selectChange = request.POST.get('selectChange', False)  
            #print selectChange
            if selectChange == "0":
                inputList=request.session['inputList']
            else:
                del request.session['inputList']
                
 
        if 'coefficientsparts' not in request.session  or not request.session['coefficientsparts']:
            pass
        else:
            selectChange = request.POST.get('selectChange', False)  
            #print selectChange
            if selectChange == "0":
                coefficientsparts=request.session['coefficientsparts']
            else:
                del request.session['coefficientsparts']
 
 
            
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
                typeselected='d'
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
        
        puntualgroupselected_name =''
        puntualgroupselected_name =  request.POST.get('puntualgroupselected_name', False)
        if puntualgroupselected_name == False:
            puntualgroupselected_name =''
        
        
        if 'propertyCategoryNameListOnSession' not in request.session  or not request.session['propertyCategoryNameListOnSession']:
            propertyCategoryName=CatalogProperty.objects.filter(active= True)
            request.session['propertyCategoryNameListOnSession'] =propertyCategoryName
        else:
            propertyCategoryName =request.session['propertyCategoryNameListOnSession']
          
          
        list_CatalogCrystalSystem= CatalogCrystalSystem.objects.filter(catalogproperty=CatalogProperty.objects.get(name__exact=catalogproperty_name),active=True)
        for register_catalogCrystalSystem in list_CatalogCrystalSystem: 
            objCatalogCrystalSystem=CatalogCrystalSystem();
            objCatalogCrystalSystem = register_catalogCrystalSystem
            catalogCrystalSystemList.append(objCatalogCrystalSystem)

        if 'catalogCrystalSystemListOnSession' not in request.session  or not request.session['catalogCrystalSystemListOnSession']:
            pass
        else:
            del request.session['catalogCrystalSystemListOnSession']

        """if (chkBoxmge == False or str(chkBoxmge[0]) == '1'  and catalogproperty_name == "2nd") or catalogproperty_name != "2nd":
            request.session['catalogCrystalSystemListOnSession']=catalogCrystalSystemList
        else:
            catalogCrystalSystemList=[]"""
            
        request.session['catalogCrystalSystemListOnSession']=catalogCrystalSystemList
            
            
        if 'dataPropertyListOnSession' not in request.session  or not request.session['dataPropertyListOnSession']:
            pass
        else:
            del request.session['dataPropertyListOnSession']
            
         
        ids=CatalogProperty.objects.filter(name=catalogproperty_name,active=True).values_list('id', flat=True)    
        type_ids=Type.objects.filter(catalogproperty_id__in=ids,active=True, name=typeselected).values_list('id',flat=True)    
        data_property_ids=TypeDataProperty.objects.filter(type_id__in=type_ids).values_list('dataproperty_id',flat=True)    
        dataPropertyList=Property.objects.filter(id__in=data_property_ids)
        request.session['dataPropertyListOnSession']=dataPropertyList


        dictionaryList=[]
        dictionaryQuerySet= Dictionary.objects.filter(category = Category.objects.get(pk=9), deploy = 1)
        for dictionary in dictionaryQuerySet: 
            objDictionary =Dictionary();
            objDictionary = dictionary
            dictionaryList.append(objDictionary)
            del objDictionary
            
        request.session['dictionaryList'] =dictionaryList
        
        
        dictionaryPhaseList=[]
        
        dictionaryPhaseQuerySet1= Dictionary.objects.filter(category = Category.objects.get(pk=4), deploy = 1)
        dictionaryPhaseQuerySet2= Dictionary.objects.filter(category = Category.objects.get(pk=8), deploy = 1)
        dictionaryPhaseQuerySet= (dictionaryPhaseQuerySet1 | dictionaryPhaseQuerySet2).distinct()
        for dictionary in dictionaryPhaseQuerySet: 
            objDictionary =Dictionary();
            objDictionary = dictionary
            dictionaryPhaseList.append(objDictionary)
            del objDictionary  
            
        request.session['dictionaryPhaseList'] =dictionaryPhaseList
        
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

        
        ShowBtnSend=0

        form =ValidateAddCaseFormv2(request.POST,inputList=inputList)
         
        validationbyform = 0
        propertiesv2=None
        
        #inicializacion
        lengthlist = 0
        propertySessionList =[]
        if not 'propertySessionList' in request.session or not request.session['propertySessionList' ]:  
            pass
        else:
            propertySessionList = request.session['propertySessionList' ]
            print propertySessionList
            lengthlist =len(propertySessionList) 


        propertaddedmessage =""
        sucess = 0
        added = 0
        inputListReadOnly = [] 
        inputListValues = {}
      
             
        if form.is_valid():
            propertiesv2=Propertiesv2(catalogproperty_name, crystalsystem_name, typeselected,datapropertytagselected, chkBoxmge, rq=request,inputList=inputList,coefficientsparts=coefficientsparts)
            propertiesv2.NewProperties(puntualgroupselected_name,axisselected_name)

            sucess=propertiesv2.sucess  

            
            if  sucess  == 0:
                inputList=propertiesv2.catalogPropertyDetail
                request.session['inputList']=inputList
                request.session['coefficientsparts']=propertiesv2.coefficientsparts
                
                inputListReadOnly=propertiesv2.catalogPropertyDetailReadOnly
 
                print "continue"
            else:
                
                propertiesv2.releaseRequet()
                propertiesv2.title = request.POST.get('title', False)
                propertiesv2.authors = request.POST.get('author', False)
                propertiesv2.journal = request.POST.get('journal', False)
                propertiesv2.year = request.POST.get('year', False)
                propertiesv2.volume = request.POST.get('volume', False)
                propertiesv2.page_first = request.POST.get('page_first', False)
                propertiesv2.page_last = request.POST.get('page_last', False)
 
     
                if not 'dictionaryValues' in request.session or not request.session['dictionaryValues' ]:                 
                    pass 
                else:
                    dictionaryValues =request.session['dictionaryValues' ] 
                    propertiesv2.dictionaryValues=dictionaryValues   
                    
                 
         
                
                print "add to list"
                added =addToSession(request,propertiesv2,'propertySessionList')
                propertySessionList= request.session['propertySessionList'];
                
 
                if added == 0:
                    propertaddedmessage = "Property previously added"
                else:
                    lengthlist =len(propertySessionList) 

                validationbyform = 0
                #ShowBtnSend=0
                print "valid"
                
                
            if lengthlist == 0 and sucess==0 and len(inputListReadOnly) > 0:
                ShowBtnSend=0
            elif lengthlist == 0 and sucess==0 and len(inputListReadOnly) == 0:
                ShowBtnSend=1
            elif lengthlist == 1 and sucess==1 and len(inputListReadOnly) == 0:
                ShowBtnSend=2
                
                
            """
            print "sucess: " + str(sucess )   
            print "lengthlist: " + str(lengthlist)
            print "inputListReadOnly: " + str( len(inputListReadOnly) ) 
           """
            
        else:

            ShowBtnSend=1
            validationbyform = 1
            propertiesv2=Propertiesv2(catalogproperty_name,crystalsystem_name,typeselected,datapropertytagselected, chkBoxmge)
            propertiesv2.NewProperties(puntualgroupselected_name,axisselected_name)

            if  len(inputList) > 0:                
                for cpd in inputList:
                    value =request.POST.get(cpd.name, False)
                    if value != False:
                        if value != "" :
                            inputListValues[cpd.name] = value

                print inputListValues
                inputListReadOnly = propertiesv2.catalogPropertyDetailReadOnly
            else:
                print  inputList
                print "invalid"
 
            
 
            
        return render_to_response('newcasev2.html', {   "form":form,
                                                                                             "propertyCategoryName":propertyCategoryName,
                                                                                             "catalogproperty_name":catalogproperty_name,
                                                                                             "catalogCrystalSystemList":catalogCrystalSystemList,
                                                                                             "puntualGroupList":propertiesv2.puntualGroupList,
                                                                                             "questionGp":propertiesv2.questionGp,
                                                                                             "axisList":propertiesv2.axisList, 
                                                                                             "questionAxis":propertiesv2.questionAxis, 
                                                                                             'message':propertiesv2.message,
                                                                                            "read_write_inputs":propertiesv2.read_write_inputs,
                                                                                             "inputListReadOnly":inputListReadOnly,
                                                                                             "jquery" :propertiesv2.jquery,
                                                                                             "inputListValues":inputListValues,
                                                                                             "puntualgroupselected_name":puntualgroupselected_name,
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
                                                                                             "propertaddedmessage":propertaddedmessage,
                                                                                             "experimentalparcond_name_selected":experimentalparcond_name_selected,
                                                                                             'propertySessionList':propertySessionList,
                                                                                             'chkBoxMagnetoelectricity':chkBoxMagnetoelectricity,
                                                                                             'dataPropertyList':dataPropertyList,
                                                                                             'datapropertytagselected':int(datapropertytagselected),
                                                                                             'magnetoelectricity':magnetoelectricity
                                                                                       }, context_instance=RequestContext(request))
      
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





