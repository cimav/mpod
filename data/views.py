# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from data.models import *

from django.db import models
from django.db.models import Q
from django.db.models import Count
from my_forms import *
from requests.sessions import session
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_exempt
from WebT4 import * 
from WebRankTensors import *
from Magnetic import *
from Properties import *
import gc
from forms import *

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required





######################################################################################
#                                 ''' GLOBAL FUNCTIONS '''
######################################################################################

######################################################################################
#                                 ''' HOME '''
######################################################################################
def home(request):
    return render_to_response('home.html', context_instance=RequestContext(request))

######################################################################################
#                                 ''' USER '''
######################################################################################
@csrf_exempt 
def viewsignup(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home')
                          
                     
    else:
        form = MyRegistrationForm()
    return render(request, 'signup.html', {'form': form})

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
                 return redirect('/home')
            else:
                return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
        
               
    else:
        form = ValidationForm()
        
    return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
        
      
     


def viewlogin(request):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})
            

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
        #filename = filename.Trim()
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
      
        tensor.SecondRankTensor(val11,val12,val13,val21,val22,val23,val31,val32,val33,color,filename1,res,stl_dir,createstl,createdata)
        XEC=tensor.stringValsOfXEC
        YEC = tensor.stringValsOfYEC
        ZEC= tensor.stringValsOfZEC
        surfacecolorSecondRankTensor=tensor.surfacecolorSecondRankTensor
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


                        
        return render_to_response('secondranktensor.html',{"XEC": XEC,"YEC":YEC,"ZEC": ZEC,"LowResolutionFileName":filename1,"MiddleResolutionFileName":filename2,'colorscale':colorscale,'surfacecolorSecondRankTensor':surfacecolorSecondRankTensor}, context_instance=RequestContext(request))

        
    #return render_to_response('secondranktensor.html', context_instance=RequestContext(request))

def viewthirdranktensor(request):
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
      
  
        tensor.ThirdRankTensor(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,color,filename1,res,stl_dir,createstl,createdata)
        XEC=tensor.stringValsOfXEC
        YEC = tensor.stringValsOfYEC
        ZEC= tensor.stringValsOfZEC
        surfacecolorThirdRankTensor=tensor.surfacecolorThirdRankTensor
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
            tensor.ThirdRankTensor(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,color,filename2,res,stl_dir,createstl,createdata)
            del tensor
         

        print filename1
        print filename2
                        
        return render_to_response('thirdranktensor.html',{"XEC": XEC,"YEC":YEC,"ZEC": ZEC,"LowResolutionFileName":filename1,"MiddleResolutionFileName":filename2,'colorscale':colorscale,'surfacecolorThirdRankTensor':surfacecolorThirdRankTensor}, context_instance=RequestContext(request))
        
        '''
        ThirdRankTensor(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,color)
    return render_to_response('thirdranktensor.html', context_instance=RequestContext(request))'''

def viewcompliance(request):
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
        filename = (request.GET.get('filename', ''))
        filename = re.sub('[\s+]', '', filename)   
        
        
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

       
        compliance.YoungModulus(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,val41,val42,val43,val44,val45,val46,val51,val52,val53,val54,val55,val56,val61,val62,val63,val64,val65,val66,color,"",res,stl_dir,createstl,createdata)
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


                       
        return render_to_response('compliance.html',{"XEC": XEC,"YEC":YEC,"ZEC": ZEC,"youngModulusXEC": youngModulusXEC,"youngModulusYEC": youngModulusYEC,"youngModulusZEC": youngModulusZEC,"LowResolutionFileName":filename1,"MiddleResolutionFileName":filename2,"surfacecolorcompliance":surfacecolorcompliance,"surfacecolorYoungModulus":surfacecolorYoungModulus,"colorscale":colorscale}, context_instance=RequestContext(request))
        #return render_to_response('compliance.html', context_instance=RequestContext(request))

def viewstiffness(request):
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
    filename = (request.GET.get('filename', ''))
    filename = re.sub('[\s+]', '', filename)
                            
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
    
    

    stiffness.YoungModulus(val11,val12,val13,val14,val15,val16,val21,val22,val23,val24,val25,val26,val31,val32,val33,val34,val35,val36,val41,val42,val43,val44,val45,val46,val51,val52,val53,val54,val55,val56,val61,val62,val63,val64,val65,val66,color,"",res,stl_dir,createstl,createdata)
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
             
    return render_to_response('stiffness.html',{"XEC": XEC,"YEC":YEC,"ZEC": ZEC,"youngModulusXEC": youngModulusXEC,"youngModulusYEC": youngModulusYEC,"youngModulusZEC": youngModulusZEC,"LowResolutionFileName":filename1,"MiddleResolutionFileName":filename2,"surfacecolorstiffness":surfacecolorstiffness,"surfacecolorYoungModulus":surfacecolorYoungModulus,"colorscale":colorscale}, context_instance=RequestContext(request))
        

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
    list_obj = CatalogProperty.objects.all()
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
def newcase(request): 
   
    list_Property=get_catalog_propertyv2();
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
   
    typeList =  [];
    list_Type = Type.objects.filter(catalogproperty=list_Property[0])
    for register_type in list_Type: 
        objType=Type();
        objType = register_type
        typeList.append(objType)
        del objType
         
    catalogCrystalSystemList = [];
    list_CatalogCrystalSystem= CatalogCrystalSystem.objects.filter(catalogproperty=list_Property[0])
    for register_catalogCrystalSystem in list_CatalogCrystalSystem: 
        objCatalogCrystalSystem=CatalogCrystalSystem();
        objCatalogCrystalSystem = register_catalogCrystalSystem
        catalogCrystalSystemList.append(objCatalogCrystalSystem)
        del objCatalogCrystalSystem
 
    crystalsystem_name= "tc"
    questiontype =""
    
    typeselected = "c"   
    if catalogproperty_name == "e":
        questiontype = "s (compliance) o c (stiffness)?"
         
    
    compliancessi = range(0, 0)
    compliancessj = range(0, 0)
    stiffnessci = range(0, 0)
    stiffnesscj = range(0, 0)
    resultdi = range(0, 0)
    resultdj = range(0, 0)
 
 
    results = N.zeros([6,6])
    resultc = N.zeros([6,6])
    resultd = N.zeros([3,6])
    
    printtableresult = 0
    printingc=0
    printings=0
    printingd=0
    
    ShowBtnProcess=0
    ShowBtnSend = 1
    
   

    error = ""
    
 
    return render_to_response('newcase.html', {    "error":error,
                                                                                       "results":results,     
                                                                                         "resultc":resultc,     
                                                                                         "resultd":resultd,    
                                                                                         "printtableresult":printtableresult, 
                                                                                        "printingc":printingc, 
                                                                                        "printings":printings, 
                                                                                        "printingd":printingd,  
                                                                                        "ShowBtnSend":ShowBtnSend,
                                                                                        "ShowBtnProcess":ShowBtnProcess,
                                                                                         "compliancessi":compliancessi,    
                                                                                         "compliancessj":compliancessj,    
                                                                                         "stiffnessci":stiffnessci,    
                                                                                         "stiffnesscj":stiffnesscj,                                
                                                                                         "resultdi":resultdi,    
                                                                                         "resultdj":resultdj,     
                                                                                        "message":message,
                                                                                        "catalogproperty_name": catalogproperty_name, "error":error,
                                                                                         "questiontype":questiontype,
                                                                                         "typeList":typeList,
                                                                                         "typeselected":typeselected,
                                                                                         "axisList":axisList,
                                                                                         "axisselected_name":axisselected_name,
                                                                                         "questionAxis":questionAxis, 
                                                                                         "questionGp":questionGp, 
                                                                                         "puntualGroupList":puntualGroupList,
                                                                                         "inputList":inputList,
                                                                                         "crystalsystem_name":crystalsystem_name,
                                                                                         "catalogCrystalSystemList":catalogCrystalSystemList,                                                                                           
                                                                                         "list_Property":list_Property}, context_instance=RequestContext(request))

@login_required
@csrf_exempt 
def addcase(request): 

    list_Property=get_catalog_propertyv2();  
    title = request.POST.get('title', '')
    author = request.POST.get('author', '')
    journal = request.POST.get('journal', '')
    catalogproperty_name = request.POST.get('catalogproperty_name', False)
    catalogproperty_id =int( request.POST.get('catalogproperty_id', False) )
    crystalsystem_name= request.POST.get('crystalsystem_name', False)    
    typeselected=''
    typeselected = request.POST.get('type', False)  
    if typeselected == False:
        typeselected =''
   
    
    axisselected_name =''
    axisselected_name = request.POST.get('axisselected_name', False)   
    if axisselected_name == False:
        axisselected_name =''
    
    puntualgroupselected_name =''
    puntualgroupselected_name =  request.POST.get('puntualgroupselected_name', False)
    if puntualgroupselected_name == False:
        puntualgroupselected_name =''
        
    
      
    s11=  request.POST.get('s11', False)
    s12=  request.POST.get('s12', False)    
    s13=  request.POST.get('s13', False)  
    s14=  request.POST.get('s14', False)  
    s15=  request.POST.get('s15', False)  
    s16=  request.POST.get('s16', False)      
 
    s21=  request.POST.get('s21', False)
    s22=  request.POST.get('s22', False)    
    s23=  request.POST.get('s23', False)  
    s24=  request.POST.get('s24', False)  
    s25=  request.POST.get('s25', False)  
    s26=  request.POST.get('s26', False) 
    
    s31=  request.POST.get('s31', False)
    s32=  request.POST.get('s32', False)    
    s33=  request.POST.get('s33', False)  
    s34=  request.POST.get('s34', False)  
    s35=  request.POST.get('s35', False)  
    s36=  request.POST.get('s36', False)  
    
    
    s41=  request.POST.get('s41', False)
    s42=  request.POST.get('s42', False)    
    s43=  request.POST.get('s43', False)  
    s44=  request.POST.get('s44', False)  
    s45=  request.POST.get('s45', False)  
    s46=  request.POST.get('s46', False)  
    
    
    s51=  request.POST.get('s51', False)
    s52=  request.POST.get('s52', False)    
    s53=  request.POST.get('s53', False)  
    s54=  request.POST.get('s54', False)  
    s55=  request.POST.get('s55', False)  
    s56=  request.POST.get('s56', False)  
    
    s61=  request.POST.get('s61', False)
    s62=  request.POST.get('s62', False)    
    s63=  request.POST.get('s63', False)  
    s64=  request.POST.get('s64', False)  
    s65=  request.POST.get('s65', False)  
    s66=  request.POST.get('s66', False) 
    
    
    
        
    
    c11=  request.POST.get('c11', False)
    c12=  request.POST.get('c12', False)    
    c13=  request.POST.get('c13', False)  
    c14=  request.POST.get('c14', False)  
    c15=  request.POST.get('c15', False)  
    c16=  request.POST.get('c16', False)  
    
    c21=  request.POST.get('c21', False)
    c22=  request.POST.get('c22', False)    
    c23=  request.POST.get('c23', False)  
    c24=  request.POST.get('c24', False)  
    c25=  request.POST.get('c25', False)  
    c26=  request.POST.get('c26', False) 
    
    
    c31=  request.POST.get('c31', False)
    c32=  request.POST.get('c32', False)    
    c33=  request.POST.get('c33', False)  
    c34=  request.POST.get('c34', False)  
    c35=  request.POST.get('c35', False)  
    c36=  request.POST.get('c36', False) 
    
    c41=  request.POST.get('c41', False)
    c42=  request.POST.get('c42', False)    
    c43=  request.POST.get('c43', False)  
    c44=  request.POST.get('c44', False)  
    c45=  request.POST.get('c45', False)  
    c46=  request.POST.get('c46', False) 
    
    
    c51=  request.POST.get('c51', False)
    c52=  request.POST.get('c52', False)    
    c53=  request.POST.get('c53', False)  
    c54=  request.POST.get('c54', False)  
    c55=  request.POST.get('c55', False)  
    c56=  request.POST.get('c56', False) 
    
    
    c61=  request.POST.get('c61', False)
    c62=  request.POST.get('c62', False)    
    c63=  request.POST.get('c63', False)  
    c64=  request.POST.get('c64', False)  
    c65=  request.POST.get('c65', False)  
    c66=  request.POST.get('c66', False) 
    
    
    
    d11=  request.POST.get('d11', False)
    d12=  request.POST.get('d12', False)    
    d13=  request.POST.get('d13', False)  
    d14=  request.POST.get('d14', False)  
    d15=  request.POST.get('d15', False)  
    d16=  request.POST.get('d16', False)  
    
    d21=  request.POST.get('d21', False)
    d22=  request.POST.get('d22', False)    
    d23=  request.POST.get('d23', False)  
    d24=  request.POST.get('d24', False)  
    d25=  request.POST.get('d25', False)  
    d26=  request.POST.get('d26', False) 
    
    
    d31=  request.POST.get('d31', False)
    d32=  request.POST.get('d32', False)    
    d33=  request.POST.get('d33', False)  
    d34=  request.POST.get('d34', False)  
    d35=  request.POST.get('d35', False)  
    d36=  request.POST.get('d36', False) 
    
    d41=  request.POST.get('d41', False)
    d42=  request.POST.get('d42', False)    
    d43=  request.POST.get('d43', False)  
    d44=  request.POST.get('d44', False)  
    d45=  request.POST.get('d45', False)  
    d46=  request.POST.get('d46', False) 
    
    
    d51=  request.POST.get('d51', False)
    d52=  request.POST.get('d52', False)    
    d53=  request.POST.get('d53', False)  
    d54=  request.POST.get('d54', False)  
    d55=  request.POST.get('d55', False)  
    d56=  request.POST.get('d56', False) 
    
    
    d61=  request.POST.get('d61', False)
    d62=  request.POST.get('d62', False)    
    d63=  request.POST.get('d63', False)  
    d64=  request.POST.get('d64', False)  
    d65=  request.POST.get('d65', False)  
    d66=  request.POST.get('d66', False) 
        
        
        
        
        
        
    message=""
    error = ""
    questiontype =""
    questionAxis = ''        
    questionGp = ''    
     
    inputList = None
    
    eventonchange = request.POST.get('eventonchange', False)  
    proccesing = request.POST.get('proccesing', False)  
    
    typeList =  [];
    catalogCrystalSystemList = [];
    crystalSystemPuntualGroupList =[];
    crystalSystemAxisList  =[];
    axisList=[]
    puntualGroupList =[];
    
    propertySelected=CatalogProperty.objects.filter(name__exact=catalogproperty_name)
    for register_property in propertySelected: 
        objProperty=CatalogProperty();
        objProperty = register_property
        catalogproperty_name = objProperty.name
        catalogproperty_id =  objProperty.id
       
       
    list_Type = Type.objects.filter(catalogproperty=objProperty)
    for register_type in list_Type: 
        objType=Type();
        objType = register_type
        if objType.id != 0:
            typeList.append(objType)
     
   
   
    list_CatalogCrystalSystem= CatalogCrystalSystem.objects.filter(catalogproperty=objProperty)
    for register_catalogCrystalSystem in list_CatalogCrystalSystem: 
        objCatalogCrystalSystem=CatalogCrystalSystem();
        objCatalogCrystalSystem = register_catalogCrystalSystem
        catalogCrystalSystemList.append(objCatalogCrystalSystem)
    
          
               
                 
     
     
 
    if catalogproperty_name=='p':
        typeselected ='n'
      
      
    catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name__exact=crystalsystem_name,catalogproperty=propertySelected) 
    newProperties = Properties(catalogproperty_name,crystalsystem_name)    
    newProperties.s11=s11
    newProperties.s12=s12
    newProperties.s13=s13
    newProperties.s14=s14
    newProperties.s15=s15
    newProperties.s16=s16   
    
    newProperties.s21=s21
    newProperties.s22=s22
    newProperties.s23=s23
    newProperties.s24=s24
    newProperties.s25=s25
    newProperties.s26=s26

    newProperties.s31=s31
    newProperties.s32=s32
    newProperties.s33=s33
    newProperties.s34=s34
    newProperties.s35=s35
    newProperties.s36=s36
    
    newProperties.s41=s41
    newProperties.s42=s42
    newProperties.s43=s43
    newProperties.s44=s44
    newProperties.s45=s45
    newProperties.s46=s46
    
    newProperties.s51=s51
    newProperties.s52=s52
    newProperties.s53=s53
    newProperties.s54=s54
    newProperties.s55=s55
    newProperties.s56=s56
    
    newProperties.s61=s61
    newProperties.s62=s62
    newProperties.s63=s63
    newProperties.s64=s64
    newProperties.s65=s65
    newProperties.s66=s66
    
    
    newProperties.c11=c11
    newProperties.c12=c12
    newProperties.c13=c13
    newProperties.c14=c14
    newProperties.c15=c15
    newProperties.c16=c16   
    
    newProperties.c21=c21
    newProperties.c22=c22
    newProperties.c23=c23
    newProperties.c24=c24
    newProperties.c25=c25
    newProperties.c26=c26

    newProperties.c31=c31
    newProperties.c32=c32
    newProperties.c33=c33
    newProperties.c34=c34
    newProperties.c35=c35
    newProperties.c36=c36
    
    newProperties.c41=c41
    newProperties.c42=c42
    newProperties.c43=c43
    newProperties.c44=c44
    newProperties.c45=c45
    newProperties.c46=c46
    
    newProperties.c51=c51
    newProperties.c52=c52
    newProperties.c53=c53
    newProperties.c54=c54
    newProperties.c55=c55
    newProperties.c56=c56
    
    newProperties.c61=c61
    newProperties.c62=c62
    newProperties.c63=c63
    newProperties.c64=c64
    newProperties.c65=c65
    newProperties.c66=c66
    
    
    
    newProperties.d11=d11
    newProperties.d12=d12
    newProperties.d13=d13
    newProperties.d14=d14
    newProperties.d15=d15
    newProperties.d16=d16   
    
    newProperties.d21=d21
    newProperties.d22=d22
    newProperties.d23=d23
    newProperties.d24=d24
    newProperties.d25=d25
    newProperties.d26=d26

    newProperties.d31=d31
    newProperties.d32=d32
    newProperties.d33=d33
    newProperties.d34=d34
    newProperties.d35=d35
    newProperties.d36=d36
    
    newProperties.d41=d41
    newProperties.d42=d42
    newProperties.d43=d43
    newProperties.d44=d44
    newProperties.d45=d45
    newProperties.d46=d46
    
    newProperties.d51=d51
    newProperties.d52=d52
    newProperties.d53=d53
    newProperties.d54=d54
    newProperties.d55=d55
    newProperties.d56=d56
    
    newProperties.d61=d61
    newProperties.d62=d62
    newProperties.d63=d63
    newProperties.d64=d64
    newProperties.d65=d65
    newProperties.d66=d66
    
    if proccesing  != '0' :
      newProperties.process = 1
    
    
    newProperties.NewProperties(typeselected,puntualgroupselected_name,axisselected_name)
    
    objProperty=CatalogProperty.objects.filter(name__exact=catalogproperty_name) 

        
    objTypeSelected = Type.objects.filter(catalogproperty=objProperty,name__exact=typeselected)    
                 
    catalogCrystalSystemSelected= CatalogCrystalSystem.objects.filter(name__exact=crystalsystem_name,catalogproperty=objProperty)    
     
    #if newProperties.questionGp != '' :  
    questionGp =  newProperties.questionGp
   
    propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected).values('catalogpointgroup').annotate(total=Count('catalogpointgroup'))
    for d in propertyDetail:  
      if d['catalogpointgroup'] != 0:       
        print d['catalogpointgroup']  
        objCatalogPointGroup=CatalogPointGroup.objects.filter(id__exact=d['catalogpointgroup'])         
        for obj in  objCatalogPointGroup:
            cpg=CatalogPointGroup()
            cpg=obj        
            if puntualgroupselected_name == '':
               puntualgroupselected_name=cpg.name
           
            puntualGroupList.append(cpg)
   
   
    propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected).values('puntualgroupnames').annotate(total=Count('puntualgroupnames'))
    for d in propertyDetail:
      if d['puntualgroupnames'] != 0:   
       print d['puntualgroupnames']              
       objPuntualgroupnames=PuntualGroupNames.objects.filter(id__exact=d['puntualgroupnames']) 
       objPuntualGroupGroups = PuntualGroupGroups.objects.filter(puntualgroupnames=objPuntualgroupnames)    
       for obj in objPuntualGroupGroups:
          pgg=PuntualGroupGroups()
          pgg=obj
          print pgg.catalogpointgroup.name
          if puntualgroupselected_name == '':
             puntualgroupselected_name=pgg.catalogpointgroup.name
             
          puntualGroupList.append(pgg.catalogpointgroup)
       

    if newProperties.questionAxis != '' :  
        questionAxis =  newProperties.questionAxis 
        propertyDetail = CatalogPropertyDetail.objects.filter(type=objTypeSelected,crystalsystem=catalogCrystalSystemSelected).values('catalogaxis').annotate(total=Count('catalogaxis'))
        for d in propertyDetail:  
          if d['catalogaxis'] != 0:       
            print d['catalogaxis']  
            objCatalogAxis=CatalogAxis.objects.filter(id=d['catalogaxis'] )
            for obj in objCatalogAxis:
              ca=CatalogAxis()
              ca=obj
              print ca.name
              axisList.append(ca)
              
              
    
    message=newProperties.message 
    ShowBtnSend=newProperties.ShowBtnSend
    ShowBtnProcess=newProperties.ShowBtnProcess
    error = newProperties.error  
    results=newProperties.results
    resultc=newProperties.resultc
    resultd=newProperties.resultd
    compliancessi = range(0, newProperties.si)
    compliancessj = range(0, newProperties.sj)
    stiffnessci = range(0, newProperties.ci)
    stiffnesscj = range(0, newProperties.cj)
    resultdi = range(0, newProperties.di)
    resultdj = range(0, newProperties.dj)
    
    printtableresult = 1
    printingc=newProperties.printingc
    printings=newProperties.printings
    printingd=newProperties.printingd
    
    
    
    


    inputList=newProperties.catalogPropertyDetail
    
    del  newProperties


    gc.collect()
           

         

    
    if catalogproperty_name == "e":
         questiontype = "s (compliance) o c (stiffness)?"
        
    
    
    
    
    
    #error = propertie.error
    

    return render_to_response('newcase.html', {   "catalogproperty_name": catalogproperty_name,
                                                                                         "questiontype":questiontype,
                                                                                         "questionAxis":questionAxis, 
                                                                                         "axisselected_name":axisselected_name,
                                                                                         "questionGp":questionGp,
                                                                                         "ShowBtnProcess":ShowBtnProcess,
                                                                                         "ShowBtnSend":ShowBtnSend,
                                                                                         "error":error,
                                                                                         "axisList":axisList, 
                                                                                         "puntualGroupList":puntualGroupList, 
                                                                                         "typeList":typeList,
                                                                                         "typeselected":typeselected,
                                                                                         "crystalsystem_name":crystalsystem_name,
                                                                                         "catalogCrystalSystemList":catalogCrystalSystemList,     
                                                                                         "inputList":inputList,      
                                                                                         "puntualgroupselected_name":puntualgroupselected_name,
                                                                                         "message":message,                                                                                            
                                                                                         "results":results,     
                                                                                         "resultc":resultc,     
                                                                                         "resultd":resultd,      
                                                                                         "printtableresult":printtableresult,  
                                                                                        "printingc":printingc, 
                                                                                        "printings":printings, 
                                                                                        "printingd":printingd, 
                                                                                         "compliancessi":compliancessi,    
                                                                                         "compliancessj":compliancessj,    
                                                                                         "stiffnessci":stiffnessci,    
                                                                                         "stiffnesscj":stiffnesscj,                                
                                                                                         "resultdi":resultdi,    
                                                                                         "resultdj":resultdj,                                                                                         
                                                                                         "list_Property":list_Property}, context_instance=RequestContext(request))



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





