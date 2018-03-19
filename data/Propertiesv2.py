

import os
import numpy as N
from django.db import models
from data.models import *
from django.db.models import Count

 

class Propertiesv2(object):

    def __init__(self,catalogproperty_name, csn ,typesc,  *args,  **kwargs):
            self.title =  ""
            self.authors =  ""
            self.journal =  ""
            self.volume =  ""
            self.year = ""
            self.page_first =  ""
            self.page_last = ""
        
            self.catalogproperty_name = catalogproperty_name
            self.type = typesc # s (compliance) o c (stiffness)?
            self.crystalsystem_name = csn
            self.puntualgroupselected_name =None
            self.axisselected_name =None
            
            self.message=''
            self.questionAxis=''
            self.questionGp =''
            self.objCatalogPointGroupSelected =None            
            self.objProperty  =None
            self.objTypeSelected  =None
            self.objCatalogCrystalSystemSelected  =None
            self.objAxisSelected=None
            self.dictionaryValues = None
            self.catalogPropertyDetail=[]
            self.catalogPropertyDetailReadOnly = []
            self.puntualGroupList=[]
            self.axisList =[]
            self.listofemptyInputs =[]
            
            self.jquery= """
                                    function isScientificNotation(value)
                                   {
                                        var n = value.indexOf("e");
                                        if(n == -1)
                                        {
                                            n = value.indexOf("E");
                                            if(n == -1)
                                                return 0; 
                                            else
                                                return 1;
                                        }
                                         return 1; 
                                   }
                                   
                                   function inputpop(obj)
                                   {
                                         if(obj.val().length > 3)
                                        {
                                            obj.attr('data-content', obj.val());                                                                             
                                            obj.popover('show');
                                        }
                                        else
                                        {
                                           obj.popover('hide');
                                           obj.attr('data-content', '');    
                                        }
                                 }
                                 
                                 function inputpopclear(obj)
                                 {
                                    obj.popover('hide');
                                    obj.attr('data-content', '');    
                                 }
                                   
                            """
            self.__inputList = None
            
            #self.inputList =[]
            self.s = N.zeros([6,6])
            self.c = N.zeros([6,6])
            self.d = N.zeros([3,6])
            self.__request = None
            
            if 'rq' in kwargs:
                self.__request = kwargs.pop('rq' )
            
            if 'inputList' in kwargs:
                self.__inputList  = kwargs.pop('inputList' )
                
                
                
            self.__dict = {}
            self.read_write_inputs = {}
            
            
            self.sucess = 0
            

                        
    def NewProperties(self,pgn,aname):
        self.objProperty=CatalogProperty.objects.get(name=self.catalogproperty_name) 
        
        if self.catalogproperty_name !='p':
            if self.type != '':
                self.objTypeSelected = Type.objects.get(catalogproperty=self.objProperty,name=self.type)   
            else:
                self.objTypeSelected = Type.objects.get(catalogproperty=self.objProperty,name='s')   
        else: 
            self.type = 'd'           
            self.objTypeSelected = Type.objects.get(catalogproperty=self.objProperty,name=self.type) 
            
        if self.catalogproperty_name !='p':        
            self.objCatalogCrystalSystemSelected= CatalogCrystalSystem.objects.get(name=self.crystalsystem_name,catalogproperty=self.objProperty) 
        else:
            if  self.crystalsystem_name == 'iso':
                self.crystalsystem_name='tc'
            else:
                pass
            
            self.objCatalogCrystalSystemSelected= CatalogCrystalSystem.objects.get(name=self.crystalsystem_name,catalogproperty=self.objProperty)
            


        self.puntualgroupselected_name =pgn
        self.axisselected_name =aname
        
        if self.catalogproperty_name == 'e':
            if self.crystalsystem_name == 'iso':  
                if  self.__request != None and len(self.__inputList) > 0:
                                           
                    for p in self.__inputList :
                        value = self.__request.POST.get(p.name, False)  
                        if str(p.name) == "s11":
                            self.s[0,0] = self.s[1,1] = self.s[2,2] =float(value) 
                        elif str(p.name)  == "s12": 
                            self.s[0,1] = self.s[0,2] = self.s[1,2] = self.s[1,0] = self.s[2,0] = self.s[2,1] = float(value) 
                        elif str(p.name)  == "c11": 
                            self.c[0,0] = self.c[1,1] = self.c[2,2] = float(value)  
                        elif str(p.name)  =="c12": 
                            self.c[0,1] = self.c[0,2] = self.c[1,2] = self.c[1,0] = self.c[2,0] = self.c[2,1] = float(value) 
                            
                    if self.type == 's':
                        self.s[3,3] = self.s[4,4] = self.s[5,5] = 2*(self.s[0,0] - self.s[0,1])
                        print (self.s)
                    elif self.type == 'c':
                        self.c[3,3] = self.c[4,4] = self.c[5,5] = (self.c[0,0] - self.c[0,1])/2
                        print (self.c)
                        
                    self.sucess = 1;
                    return
                else:
                     
                    if  self.puntualgroupselected_name == '':
                        self.message= 'All the point groups of this crystal system have the same matrix'
                        self.questionGp = 'Point Group?'    
                        self.setPointGroup()
                        return
                
                    self.message= 'All the point groups of this crystal system have the same matrix'
                    self.questionGp = 'Point Group?'    
                    self.setPointGroup()
                    self.setCatalogPropertyDetail()
                    self.preparedataforjQuery(self.type );
                    if self.type == 's':
                        self.listofemptyInputs.append("s44");
                        self.listofemptyInputs.append("s55");
                        self.listofemptyInputs.append("s66");
                        self.listofemptyInputs.append("s22");
                        self.listofemptyInputs.append("s33");
                        self.listofemptyInputs.append("s12");
                        self.listofemptyInputs.append("s13");
                        self.listofemptyInputs.append("s23");
                        self.listofemptyInputs.append("s21");
                        self.listofemptyInputs.append("s31");
                        self.listofemptyInputs.append("s32");
                       
 
                                  
                        self.jquery= self.jquery +  """$(document).ready(
                                                                                    function() 
                                                                                    {
                                                                                
                                                                                         $('#s11').change(function() {   
         
                                                                                             if(Number($(this).val()).toPrecision() != 'NaN')
                                                                                            {
                                                                                                 v = 2 *($('#s11').val()- $('#s12').val());
                                                                                                                                                 
                                                                                                 if ( isScientificNotation($(this).val()) == 1 )
                                                                                                    value = Number.parseFloat(v).toExponential();
                                                                                                else
                                                                                                   value = v
                            
                                                                                              
                                                                                                  $('#s44').val(value) ;
                                                                                                  $('#s55').val(value) ;
                                                                                                  $('#s66').val(value) ;
                                                                                             }
                                                                                            else 
                                                                                            {
                                                                                                $('#s44').val('' ) ;
                                                                                                $('#s55').val('' ) ;
                                                                                                $('#s66').val('' ) ;
                                                                                                
                                                                                            }
                                                                                            
                                                                                         });
                                                                     
                                                                                         $('#divwarningpropertyvalues').hide();
                                                                                         
                                                                                        $('#s11').keyup(function ()
                                                                                        {                                                            

                                                                                            if(Number($(this).val()).toPrecision() != 'NaN')
                                                                                            {
                                                                                                inputpop($(this));
                                                                                                $('#s22').val($(this).val()) ;
                                                                                                $('#s33').val($(this).val()) ;
                                                                                            }
                                                                                            else 
                                                                                            {
                                                                                                $('#s22').val('') ;
                                                                                                $('#s33').val('') ;
                                                                                                 
                                                                                                inputpopclear($(this));
                                                                                            }
                                                                                         });
                                                        
                                                                                         $('#s12').keyup(function ()
                                                                                        {                        
                                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {                                                                                                  
                                                                                                inputpop($(this));                                                                                                 
                                                                                                $('#s13').val($(this).val() ) ;
                                                                                                $('#s23').val($(this).val() ) ;
                                                                                                $('#s21').val($(this).val() ) ;
                                                                                                $('#s31').val($(this).val() ) ;
                                                                                                $('#s32').val($(this).val() ) ;
                                                                                                                           
                                                                                                 v = 2 *($('#s11').val()- $(this).val());
                                                                         
                                                                                                 if ( isScientificNotation($(this).val()) == 1 )
                                                                                                    value = Number.parseFloat(v).toExponential();
                                                                                                else
                                                                                                   value = v
                                                                                                   
                                                                                                $('#s44').val(value) ;
                                                                                                $('#s55').val(value) ;
                                                                                                $('#s66').val(value) ;
                                                                                           
                                                                                                
                                                                                            }
                                                                                            else
                                                                                            {
                                                                                                 
                                                                                                $('#s13').val('') ;
                                                                                                $('#s23').val('') ;
                                                                                                $('#s21').val('') ;
                                                                                                $('#s31').val('') ;
                                                                                                $('#s32').val('') ;;
                                                                                                $('#s44').val('') ;
                                                                                                $('#s55').val('') ;
                                                                                                $('#s66').val('') ;
                                                                                                inputpopclear($(this)); 
                                                                                            }
                                        
                                                                                         });
                                                  
                                                                             """
                    elif self.type == 'c': 
                        self.listofemptyInputs.append("c44");
                        self.listofemptyInputs.append("c55");
                        self.listofemptyInputs.append("c66");
                        self.listofemptyInputs.append("c22");
                        self.listofemptyInputs.append("c33");
                        self.listofemptyInputs.append("c12");
                        self.listofemptyInputs.append("c13");
                        self.listofemptyInputs.append("c23");
                        self.listofemptyInputs.append("c21");
                        self.listofemptyInputs.append("c31");
                        self.listofemptyInputs.append("c32");
                        
                                                
                                
                        self.jquery= self.jquery +  """$(document).ready(
                                                                            function() 
                                                                            {
                                                                               $('#c11').change(function() {
                                                                                   
                                                                                    if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                         v = ($('#c11').val()- $('#c12').val())/2;
                                                                                                     
                                                                                         if ( isScientificNotation($(this).val()) == 1 )
                                                                                            value = Number.parseFloat(v).toExponential();
                                                                                        else
                                                                                           value = v
                                                                      
                                                                                          $('#c44').val(value) ;
                                                                                          $('#c55').val(value) ;
                                                                                          $('#c66').val(value) ;
                                                                                      }
                                                                                      else
                                                                                      {
                                                                                         $('#c44').val('') ;
                                                                                         $('#c55').val('') ;
                                                                                         $('#c66').val('') ;
                                                                                      }
                                                                                 });
                                
                                                                                  
                                                                                $('#c11').keyup(function ()
                                                                                {
                                                                                    inputpop($(this));
                                                                                    if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                        $('#divwarningpropertyvalues').hide();
                                                                                        $('#c22').val($(this).val() ) ;
                                                                                        $('#c33').val($(this).val() ) ;
                                
                                                                                    }else
                                                                                    {
                                                                                        $('#c22').val('') ;
                                                                                        $('#c33').val('') ;
                                                                                        inputpopclear($(this));
                                                                                    }
                                                                                 });
                                                
                                                                                 $('#c12').keyup(function ()
                                                                                {
                                                                                   if(Number($(this).val()).toPrecision() != 'NaN')  {     
                                                                                        inputpop($(this));                                                                                   
                                                                                        $('#c13').val($(this).val() ) ;
                                                                                        $('#c23').val($(this).val() ) ;
                                                                                        $('#c21').val($(this).val() ) ;
                                                                                        $('#c31').val($(this).val() ) ;
                                                                                        $('#c32').val($(this).val() ) ;
                                                                                                                   
                                                                                         v = ($('#c11').val()- $(this).val())/2;
                                                                                         if ( isScientificNotation($(this).val()) == 1 )
                                                                                            value = Number.parseFloat(v).toExponential();
                                                                                        else
                                                                                           value = v
                                                                                   
                                                                                        $('#c44').val(value) ;
                                                                                        $('#c55').val(value) ;
                                                                                        $('#c66').val(value) ;
                                                                                        
                                                                                    }
                                                                                    else
                                                                                    {
                                                                                        $('#c13').val('' ) ;
                                                                                        $('#c23').val('') ;
                                                                                        $('#c21').val('') ;
                                                                                        $('#c31').val('') ;
                                                                                        $('#c32').val('') 
                                                                                        $('#c44').val('') ;
                                                                                        $('#c55').val('') ;
                                                                                        $('#c66').val('') ;
                                                                                        inputpopclear($(this));
                                                                                    }
                                                                         });
                                             
                                                     """
    
                    self.jquery= self.jquery+"\n"   
    
      
                    for key in sorted(self.read_write_inputs.keys()):
                            if  self.read_write_inputs[key] == 'r':
                                if  self.contains(self.listofemptyInputs,key):
                                    self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val('');" +"\n"     
                                else:
                                    self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n"         
                                
 
                    self.jquery=  self.jquery+ "\n"  + "\n"  +  " });"
                    
                    print self.jquery

    
            elif self.crystalsystem_name == 'c': 
                if  self.__request != None and len(self.__inputList) > 0:
                    for p in self.__inputList :
                        value = self.__request.POST.get(p.name, False)  
                        if str(p.name) == "s11":
                            self.s[0,0] = self.s[1,1] = self.s[2,2] = float (self.__request.POST.get(p.name, False))
                        elif str(p.name)  == "s12": 
                            self.s[0,1] =self.s[0,2] =self.s[1,2] = self.s[1,0] = self.s[2,0] = self.s[2,1] = float (self.__request.POST.get(p.name, False))
                        elif str(p.name)  == "s44": 
                            self.s[3,3] = self.s[4,4] = self.s[5,5] =float (self.__request.POST.get(p.name, False))
                            
                        elif str(p.name) == "c11":
                            self.s[0,0] = self.s[1,1] = self.s[2,2] = float (self.__request.POST.get(p.name, False))
                        elif str(p.name)  == "c12": 
                            self.c[0,1] = self.c[0,2] = self.c[1,2] = self.c[1,0] = self.c[2,0] = self.c[2,1] = float (self.__request.POST.get(p.name, False))
                        elif str(p.name)  == "c44": 
                            self.s[3,3] = self.s[4,4] = self.s[5,5] =float (self.__request.POST.get(p.name, False))

                    if self.type == 's':
                        print (self.s)
                    elif self.type == 'c':
                        print (self.c)
                        
                        
                    self.sucess = 1;                       
                    return
                else:
                    if  self.puntualgroupselected_name == '':
                        self.message= 'All the point groups of this crystal system have the same matrix'
                        self.questionGp = 'Point Group?'    
                        self.setPointGroup()
                        return
                
                    self.message= 'All the point groups of this crystal system have the same matrix'
                    self.questionGp = 'Point Group?'    
                    self.setPointGroup()
                    
                    self.setCatalogPropertyDetail()
                    self.preparedataforjQuery(self.type )
                    self.listofemptyInputs.append(self.type+"22");
                    self.listofemptyInputs.append(self.type+"33");
                    self.listofemptyInputs.append(self.type+"12");
                    self.listofemptyInputs.append(self.type+"13");
                    self.listofemptyInputs.append(self.type+"23");
                    self.listofemptyInputs.append(self.type+"21");
                    self.listofemptyInputs.append(self.type+"31");
                    self.listofemptyInputs.append(self.type+"32");
                    #self.listofemptyInputs.append(self.type+"44");
                    self.listofemptyInputs.append(self.type+"55");
                    self.listofemptyInputs.append(self.type+"66");
                        
                    self.jquery= self.jquery + """
                                                                    $('#divwarningpropertyvalues').hide();
                                                                    $(document).ready(
                                                                        function() 
                                                                        {
                                                                 """
                    self.jquery= self.jquery + """                    
                                                                     
                                                                     
                                                                     $('#""" +self.type+ """11').keyup(function() {
                                                                             
                                                                             if(Number($(this).val()).toPrecision() != 'NaN') 
                                                                                {
                                                                                    inputpop($(this));
                                                                                    $('#""" +self.type+ """22').val($(this).val() ) ;
                                                                                    $('#""" +self.type+ """33').val($(this).val() ) ;
                                                                                }
                                                                            else
                                                                               {
                                                                                    $('#""" +self.type+ """22').val('') ;
                                                                                    $('#""" +self.type+ """33').val('') ;
                                                                                     inputpopclear($(this));
                                                                               }
                                                                        });
                                                                             
                                                                     $('#""" +self.type+ """12').keyup(function() {
                                                                        
                                                                        if(Number($(this).val()).toPrecision() != 'NaN') 
                                                                            {
                                                                                 inputpop($(this));
                                                                                $('#""" +self.type+ """13').val($(this).val() );
                                                                                $('#""" +self.type+ """23').val($(this).val() );
                                                                                $('#""" +self.type+ """21').val($(this).val() );
                                                                                $('#""" +self.type+ """31').val($(this).val() );
                                                                                $('#""" +self.type+ """32').val($(this).val() );
                                                                            }
                                                                        else
                                                                            {
                                                                               $('#""" +self.type+ """13').val('');
                                                                                $('#""" +self.type+ """23').val('');
                                                                                $('#""" +self.type+ """21').val('');
                                                                                $('#""" +self.type+ """31').val('');
                                                                                $('#""" +self.type+ """32').val('');
                                                                                inputpopclear($(this));
                                                                            }
                                                                      });
                                                                      
                                      
                                                                     $('#""" +self.type+ """44').keyup(function() {
                                                                         
                                                                         if(Number($(this).val()).toPrecision() != 'NaN') 
                                                                            {
                                                                                inputpop($(this));   
                                                                                $('#""" +self.type+ """55').val($(this).val());
                                                                                $('#""" +self.type+ """66').val($(this).val());              
                                                                             }
                                                                        else
                                                                            {
                                                                                $('#""" +self.type+ """55').val('');
                                                                                $('#""" +self.type+ """66').val('');  
                                                                                inputpopclear($(this));
                                                                            }     
                                                                                                                                        
                                                                      });"""                                                  
                                                                      
                    self.jquery= self.jquery+"\n" 
                    
   
                    for key in sorted(self.read_write_inputs.keys()):
                        if  self.read_write_inputs[key] == 'r':
                            if  self.contains(self.listofemptyInputs,key):
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val('');" +"\n"     
                            else:
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n"
                                
                                
 
                    self.jquery=  self.jquery+ "\n"  + "\n"  +  " });"
                    
                    print self.jquery
                    
            elif self.crystalsystem_name == 'h': 
                    #print self.crystalsystem_name
                if  self.__request != None and len(self.__inputList) > 0:
                   
                    for p in self.__inputList :
                        
                        if str(p.name) == "s11":
                            self.s[0,0] = self.s[1,1] = float (self.__request.POST.get(p.name, False))
                        elif str(p.name) == "s12":
                            self.s[0,1] = self.s[1,0] = float (self.__request.POST.get(p.name, False))
                        elif str(p.name) == "s13":
                            self.s[0,2] = self.s[1,2] = self.s[2,0] = self.s[2,1] = float (self.__request.POST.get(p.name, False)) 
                        elif str(p.name) == "s33":
                            self.s[2,2] = float (self.__request.POST.get(p.name, False))
                        elif str(p.name) == "s44":
                            self.s[3,3] = self.s[4,4] =  float (self.__request.POST.get(p.name, False))
                        elif str(p.name) == "c11":
                            self.c[0,0] = self.c[1,1] =  float (self.__request.POST.get(p.name, False))
                        elif str(p.name) == "c12":
                            self.c[0,1] = self.c[1,0] = float (self.__request.POST.get(p.name, False))
                        elif str(p.name) == "c13":
                            self.c[0,2] = self.c[1,2] = self.c[2,0] = self.c[2,1] = float (self.__request.POST.get(p.name, False))
                        elif str(p.name) == "c33":    
                            self.c[2,2] =  float (self.__request.POST.get(p.name, False))
                        elif str(p.name) == "c44":    
                            self.c[3,3] = self.c[4,4] =  float (self.__request.POST.get(p.name, False))
                            
                            
                    if self.type == 's':
                        self.s[5,5] = 2*(self.s[0,0] - self.s[0,1])
                        print (self.s)
                    elif self.type == 'c':
                        self.c[5,5] = (self.c[0,0] - self.c[0,1])/2
                        print (self.c)

                    self.sucess = 1;
                    return
                else:
                    if  self.puntualgroupselected_name == '':
                        self.message= 'All the point groups of this crystal system have the same matrix'
                        self.questionGp = 'Point Group?'    
                        self.setPointGroup()
                        return
                
                    self.message= 'All the point groups of this crystal system have the same matrix'
                    self.questionGp = 'Point Group?'    
                    self.setPointGroup()
                    
                    self.setCatalogPropertyDetail()
                    self.preparedataforjQuery(self.type )
                    self.listofemptyInputs.append(self.type+"13");
                    self.listofemptyInputs.append(self.type+"21");
                    self.listofemptyInputs.append(self.type+"22");
                    self.listofemptyInputs.append(self.type+"23");
                    self.listofemptyInputs.append(self.type+"31");
                    self.listofemptyInputs.append(self.type+"32");
                    self.listofemptyInputs.append(self.type+"55");
                    self.listofemptyInputs.append(self.type+"66");
                    
 

                    
                    self.jquery=self.jquery + """
                                                                    // inicio de codigo jQuery
                                                                    $('#divwarningpropertyvalues').hide();
                                                                    $(document).ready(
                                                                        function() 
                                                                        {
                                                                 """
                    self.jquery= self.jquery + """                    
                                                                     $('#""" +self.type+ """11').change(function() {
                                                                      
                                                                 """   
                    if self.type == 's':
                        self.jquery= self.jquery + """ v = 2 *  ($(this).val()- $('#""" +self.type+ """12').val());"""
                    elif self.type == 'c':
                        self.jquery= self.jquery + """ v =  ($(this).val()- $('#""" +self.type+ """12').val())/2;"""
                        
                        
                    self.jquery= self.jquery +"""   
                                                                        if ( isScientificNotation($(this).val()) == 1 )
                                                                            value = Number.parseFloat(v).toExponential();
                                                                         else
                                                                            value = v       
                                 
                                                                        if(Number($(this).val()).toPrecision() != 'NaN')
                                                                          {
                                                                               $('#""" +self.type+ """66').val(value) 
                                                                          }
                                                                        else
                                                                         {                                 
                                                                              $('#""" +self.type+ """66').val('') ;
                                                                          }
                                                                        });
                                                                             
                                                                 """
                                                 
                                                 
                    self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """11').keyup(function ()
                                                                            {
                                                                                
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                inputpop($(this));
                                                                                $('#""" +self.type+ """22').val($(this).val() ) ;
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """22').val('') ;
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                        """
                                                                        
                    self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """12').keyup(function ()
                                                                            {
                                                                               if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                               
                                                                                inputpop($(this));
                                                                                 
                                                                                $('#""" +self.type+ """21').val($(this).val() ) ;
                                                                  """
                    if self.type == 's':
                        self.jquery= self.jquery + """ v = 2 *  ($(""" +self.type+ """11).val()- $(this).val());"""
                    elif self.type == 'c':
                        self.jquery= self.jquery + """ v =  ($(""" +self.type+ """11).val()- $(this).val())/2;"""
                                                                    
                    self.jquery= self.jquery +     """
                                                                                
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                        value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                        value = v       
                                                                            
                                                                                
                                                                                    $('#""" +self.type+ """66').val(value ) ;
                                                                                    }
                                                                                else
                                                                                  {
                                                                                       $('#""" +self.type+ """66').val('') ;
                                                                                       inputpopclear($(this));
                                                                                  }
                                                                             });
                                                                        """
                    
                    self.jquery= self.jquery + """
                                                                     $('#""" +self.type+ """13').keyup(function ()
                                                                        {
                                                                            
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));                                                                                
                                                                                $('#""" +self.type+ """23').val($(this).val() ) ;
                                                                                $('#""" +self.type+ """31').val($(this).val() ) ;
                                                                                $('#""" +self.type+ """32').val($(this).val() ) ;
                                                                            }else
                                                                            {
                                                                                $('#""" +self.type+ """23').val('') ;
                                                                                $('#""" +self.type+ """31').val('') ;
                                                                                $('#""" +self.type+ """32').val('') ;
                                                                                 inputpopclear($(this));
                                                                            }
                                                                         });
                                                                    """
                    self.jquery= self.jquery + """ 
                                                                         $('#""" +self.type+ """33').focusout(function ()
                                                                        {                                                                             
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                $('#divwarningpropertyvalues').hide();
                                                                            }else
                                                                            {                                                                               
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """33').keyup(function ()
                                                                            {
                                                                                inputpop($(this));                                                                         
                                                                            });
                                                                    """
                    self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """44').keyup(function ()
                                                                            {
                                                                                
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                inputpop($(this));
                                                                                $('#divwarningpropertyvalues').hide();
                                                                                $('#""" +self.type+ """55').val($(this).val() ) ;
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """55').val('') ;
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                        """
                    self.jquery= self.jquery+"\n" 
                    
                    
                    """
                    for key in sorted(self.read_write_inputs.keys()):
                            #print self.read_write_inputs[key] 
                            if  self.read_write_inputs[key] == 'r':
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n" 
                    """
                    for key in sorted(self.read_write_inputs.keys()):
                        if  self.read_write_inputs[key] == 'r':
                            if  self.contains(self.listofemptyInputs,key):
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val('');" +"\n"     
                            else:
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n"
                                
                                
 
                    self.jquery=  self.jquery+ "\n"  + "\n"  +  " });"
                    
                    print self.jquery
                    
            elif self.crystalsystem_name == 'o': 
                    if  self.__request != None and len(self.__inputList) > 0:
                        for p in self.__inputList :
                            if str(p.name) == "s11":    
                                self.s[0,0] =float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s12":
                                self.s[0,1] = self.s[1,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s13":
                                self.s[0,2] = self.s[2,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s22":
                                self.s[1,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s23":
                                self.s[1,2] = self.s[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s33":
                                self.s[2,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s44":
                                self.s[3,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s55":
                                self.s[4,4] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s66":
                                self.s[5,5] = float (self.__request.POST.get(p.name, False))    
                            if str(p.name) == "c11":    
                                self.c[0,0] =float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c12":
                                self.c[0,1] = self.c[1,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c13":
                                self.c[0,2] = self.c[2,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c22":
                                self.c[1,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c23":
                                self.c[1,2] = self.c[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c33":
                                self.c[2,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c44":
                                self.c[3,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c55":
                                self.c[4,4] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c66":
                                self.c[5,5] = float (self.__request.POST.get(p.name, False))   

                        if self.type == 's':
                            print (self.s)
                        elif self.type == 'c':
                            print (self.c)
                            
                        self.sucess = 1;                            
                        return
                    else:
                        if  self.puntualgroupselected_name == '':
                            self.message= 'All the point groups of this crystal system have the same matrix'
                            self.questionGp = 'Point Group?'    
                            self.setPointGroup()
                            return
                    
                        self.message= 'All the point groups of this crystal system have the same matrix'
                        self.questionGp = 'Point Group?'    
                        self.setPointGroup()
                    
                        self.setCatalogPropertyDetail()
                        self.preparedataforjQuery(self.type )
                        self.listofemptyInputs.append(self.type+"21");
                        self.listofemptyInputs.append(self.type+"31");
                        self.listofemptyInputs.append(self.type+"32");
                        
                        self.jquery= self.jquery + """
                                                                        // inicio de codigo jQuery
                                                                        $('#divwarningpropertyvalues').hide();
                                                                        $(document).ready(
                                                                            function() 
                                                                            {
                                                                         """
                                             
                        self.jquery= self.jquery + """ $('#""" +self.type+ """11').focusout(function ()
                                                                                {
                                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                        $('#divwarningpropertyvalues').hide();
                                                                                    }else
                                                                                    {
                                                                                       $(this).val('');
                                                                                       inputpopclear($(this));
                                                                                    }
                                                                                 });
                                                                                 
                                                                                 $('#""" +self.type+ """11').keyup(function ()
                                                                                {
                                                                                    inputpop($(this));                                                                                   
                                                                                 });
                                                                    """
                                             
                        self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """12').keyup(function ()
                                                                            {
                                                                                 
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    $('#divwarningpropertyvalues').hide();
                                                                                    $('#""" +self.type+ """21').val($(this).val() ) ;
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """21').val('') ;
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                        """
                        self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """13').keyup(function ()
                                                                            {
                                                                            
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                   inputpop($(this));
                                                                                   $('#divwarningpropertyvalues').hide();
                                                                                   $('#""" +self.type+ """31').val($(this).val() ) ;
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """31').val('') ;
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                        """
                        self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """23').keyup(function ()
                                                                            {
                                                                                
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    $('#divwarningpropertyvalues').hide();
                                                                                    $('#""" +self.type+ """32').val($(this).val() ) ;
                                                                             
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """32').val('') ;
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                
                                                                             $('#""" +self.type+ """22').focusout(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    $('#divwarningpropertyvalues').hide();
                                                                                }else
                                                                                {
                                                                                   $(this).val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });      
                                                                              
                                                                            $('#""" +self.type+ """33').focusout(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    $('#divwarningpropertyvalues').hide();
                                                                                }else
                                                                                {
                                                                                   $(this).val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });   
                                                                             
                                                                            $('#""" +self.type+ """44').focusout(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    $('#divwarningpropertyvalues').hide();
                                                                                }else
                                                                                {
                                                                                   $(this).val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });   
                                                                             
                                                                            $('#""" +self.type+ """55').focusout(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    $('#divwarningpropertyvalues').hide();
                                                                                }else
                                                                                {
                                                                                   $(this).val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });   
                                                                             
                                                                            $('#""" +self.type+ """66').focusout(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    $('#divwarningpropertyvalues').hide();
                                                                                }else
                                                                                {
                                                                                   $(this).val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });   
                                                                             
                                                                             $('#""" +self.type+ """22').keyup(function ()
                                                                            {
                                                                                inputpop($(this));                                                                                   
                                                                             });   
                                                                                                                                
                                                                             $('#""" +self.type+ """33').keyup(function ()
                                                                            {
                                                                                inputpop($(this));                                                                                   
                                                                             });
                                                                             
                                                                             $('#""" +self.type+ """44').keyup(function ()
                                                                            {
                                                                                inputpop($(this));                                                                                   
                                                                             });
                                                                             
                                                                             $('#""" +self.type+ """55').keyup(function ()
                                                                            {
                                                                                inputpop($(this));                                                                                   
                                                                             });
                                                                             
                                                                             $('#""" +self.type+ """66').keyup(function ()
                                                                            {
                                                                                inputpop($(this));                                                                                   
                                                                             });
                                                                        """     
                        self.jquery= self.jquery+"\n"     
                        """                                                                                       
                        for key in sorted(self.read_write_inputs.keys()):
                            #print self.read_write_inputs[key] 
                            if  self.read_write_inputs[key] == 'r':
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n" 
                        """
                                
                                
                        for key in sorted(self.read_write_inputs.keys()):
                            if  self.read_write_inputs[key] == 'r':
                                if  self.contains(self.listofemptyInputs,key):
                                    self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val('');" +"\n"     
                                else:
                                    self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n"
                                
 
                        self.jquery=  self.jquery+ "\n"  + "\n"  +  " });"
                        
                        print self.jquery                                               
                    
            elif self.crystalsystem_name == 'tc':
                if  self.__request != None and len(self.__inputList) > 0:
                        for p in self.__inputList :
                            if str(p.name) == "s11":    
                                self.s[0,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s12":
                                self.s[0,1] = self.s[1,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s13":
                                self.s[0,2] = self.s[2,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s14":
                                self.s[0,3] = self.s[3,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s15":
                                self.s[0,4] = self.s[4,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s16":
                                self.s[0,5] = self.s[5,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s22":
                                self.s[1,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s23":
                                self.s[1,2] = self.s[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s24":
                                self.s[1,3] = self.s[3,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s25":
                                self.s[1,4] = self.s[4,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s26":
                                self.s[1,5] = self.s[5,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s33":
                                self.s[2,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s34":
                                self.s[2,3] = self.s[3,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s35":
                                self.s[2,4] = self.s[4,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s36":
                                self.s[2,5] = self.s[5,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s44":
                                self.s[3,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s45":
                                self.s[3,4] = self.s[4,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s46":
                                self.s[3,5] = self.s[5,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s55":
                                self.s[4,4] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s56":
                                self.s[4,5] = self.s[5,4] =float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s66":
                                self.s[5,5] = float (self.__request.POST.get(p.name, False))
                                
                            if str(p.name) == "c11":    
                                self.c[0,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c12":
                                self.c[0,1] = self.c[1,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c13":
                                self.c[0,2] = self.c[2,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c14":
                                self.c[0,3] = self.c[3,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c15":
                                self.c[0,4] = self.c[4,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c16":
                                self.c[0,5] = self.c[5,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c22":
                                self.c[1,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c23":
                                self.c[1,2] = self.c[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c24":
                                self.c[1,3] = self.c[3,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c25":
                                self.c[1,4] = self.c[4,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c26":
                                self.c[1,5] = self.c[5,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c33":
                                self.c[2,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c34":
                                self.c[2,3] = self.c[3,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c35":
                                self.c[2,4] = self.c[4,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c36":
                                self.c[2,5] = self.c[5,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c44":
                                self.c[3,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c45":
                                self.c[3,4] = self.c[4,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c46":
                                self.c[3,5] = self.c[5,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c55":
                                self.c[4,4] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c56":
                                self.c[4,5] = self.c[5,4] =float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c66":
                                self.c[5,5] = float (self.__request.POST.get(p.name, False))
                            

                        if self.type == 's':
                            print (self.s)
                        elif self.type == 'c':
                            print (self.c)
                            
                        self.sucess = 1;
                        return
                else:
                    """if  self.puntualgroupselected_name == '':
                        self.message= 'All the point groups of this crystal system have the same matrix'
                        self.questionGp = 'Point Group?'    
                        self.setPointGroup()
                        return"""
                
                    self.message= 'All the point groups of this crystal system have the same matrix'
                    self.questionGp = 'Point Group?'    
                    self.setPointGroup()   
                    
                    self.setCatalogPropertyDetail()
                    self.preparedataforjQuery(self.type )
                    self.listofemptyInputs.append(self.type+"21");
                    self.listofemptyInputs.append(self.type+"31");
                    self.listofemptyInputs.append(self.type+"41");
                    self.listofemptyInputs.append(self.type+"51");
                    self.listofemptyInputs.append(self.type+"61");
                    self.listofemptyInputs.append(self.type+"32");
                    self.listofemptyInputs.append(self.type+"42");
                    self.listofemptyInputs.append(self.type+"52");
                    self.listofemptyInputs.append(self.type+"62");
                    self.listofemptyInputs.append(self.type+"43");
                    self.listofemptyInputs.append(self.type+"53");
                    self.listofemptyInputs.append(self.type+"63");
                    self.listofemptyInputs.append(self.type+"54");
                    self.listofemptyInputs.append(self.type+"64");
                    self.listofemptyInputs.append(self.type+"65");
                    
                    self.jquery= self.jquery +  """
                                        // inicio de codigo jQuery
                                        $('#divwarningpropertyvalues').hide();
                                        $(document).ready(
                                            function() 
                                            {
                                         """
                    self.jquery= self.jquery + """
                                                         $('#""" +self.type+ """11').focusout(function ()
                                                            {
                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                    inputpop($(this));
                                                                }else
                                                                {
                                                                   $(this).val('');
                                                                   inputpopclear($(this));
                                                                }
                                                             });
                                                             
                                                             $('#""" +self.type+ """11').keyup(function ()
                                                            {
                                                                inputpop($(this));                                                                                   
                                                             });
                                                                         
                                                             $('#""" +self.type+ """12').keyup(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                        inputpop($(this));
                                                                        $('#""" +self.type+ """21').val($(this).val() ) ;
                                                                    }else
                                                                    {
                                                                       $('#""" +self.type+ """21').val('') ;
                                                                       inputpopclear($(this));
                                                                    }
                                                                 });
                                                                 
                                                                $('#""" +self.type+ """13').keyup(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                        inputpop($(this));
                                                                        $('#""" +self.type+ """31').val($(this).val() ) ;
                                                                 
                                                                    }else
                                                                    {
                                                                       $('#""" +self.type+ """31').val('') ;
                                                                       inputpopclear($(this));
                                                                    }
                                                                 });
                                                                 
                                                                 $('#""" +self.type+ """14').keyup(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                         inputpop($(this));
                                                                        $('#""" +self.type+ """41').val($(this).val() ) ;
                                                                 
                                                                    }else
                                                                    {
                                                                       $('#""" +self.type+ """41').val('') ;
                                                                       inputpopclear($(this));
                                                                    }
                                                                 });
                                                                 
                                                                 
                                                                $('#""" +self.type+ """15').keyup(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                        inputpop($(this));
                                                                        $('#""" +self.type+ """51').val($(this).val() ) ;
                                                                 
                                                                    }else
                                                                    {
                                                                       $('#""" +self.type+ """51').val('') ;
                                                                       inputpopclear($(this));
                                                                    }
                                                                 });
                                                                 
                                                                 
                                                                $('#""" +self.type+ """16').keyup(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                        inputpop($(this));
                                                                        $('#""" +self.type+ """61').val($(this).val() ) ;
                                                                 
                                                                    }else
                                                                    {
                                                                       $('#""" +self.type+ """61').val('') ;
                                                                       inputpopclear($(this));
                                                                    }
                                                                 });
                                                                 
                                                                 
                                                                                          
                                                                $('#""" +self.type+ """23').keyup(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                        inputpop($(this));
                                                                        $('#""" +self.type+ """32').val($(this).val() ) ;
                                                                    }else
                                                                    {
                                                                       $('#""" +self.type+ """32').val('') ;
                                                                       inputpopclear($(this));
                                                                    }
                                                                 });
                                                                 
                                                                $('#""" +self.type+ """24').keyup(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                        inputpop($(this));
                                                                        $('#""" +self.type+ """42').val($(this).val() ) ;
                                                                    }else
                                                                    {
                                                                       $('#""" +self.type+ """42').val('') ;
                                                                       inputpopclear($(this));
                                                                    }
                                                                 });  
                                                                 
                                                                $('#""" +self.type+ """25').keyup(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                        inputpop($(this));
                                                                        $('#""" +self.type+ """52').val($(this).val() ) ;
                                                                    }else
                                                                    {
                                                                       $('#""" +self.type+ """52').val('') ;
                                                                       inputpopclear($(this));
                                                                    }
                                                                 }); 
                                                                 
                                                                $('#""" +self.type+ """26').keyup(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                        inputpop($(this));
                                                                        $('#""" +self.type+ """62').val($(this).val() ) ;
                                                                 
                                                                    }else
                                                                    {
                                                                       $('#""" +self.type+ """62').val('') ;
                                                                       inputpopclear($(this));
                                                                    }
                                                                 }); 
                                                                 
                                                                 $('#""" +self.type+ """34').keyup(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                        inputpop($(this));
                                                                        $('#""" +self.type+ """43').val($(this).val() ) ;
                                                                 
                                                                    }else
                                                                    {
                                                                       $('#""" +self.type+ """43').val('') ;
                                                                       inputpopclear($(this));
                                                                    }
                                                                 }); 
                                                                $('#""" +self.type+ """35').keyup(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                        inputpop($(this));
                                                                        $('#""" +self.type+ """53').val($(this).val() ) ;
                                                                 
                                                                    }else
                                                                    {
                                                                       $('#""" +self.type+ """53').val('') ;
                                                                       inputpopclear($(this));
                                                                    }
                                                                 }); 
                                                                 
                                                                $('#""" +self.type+ """36').keyup(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                        inputpop($(this));
                                                                        $('#""" +self.type+ """63').val($(this).val() ) ;
                                                                 
                                                                    }else
                                                                    {
                                                                       $('#""" +self.type+ """63').val('') ;
                                                                       inputpopclear($(this));
                                                                    }
                                                                 }); 
                                                                 
                                                               $('#""" +self.type+ """45').keyup(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                        inputpop($(this));
                                                                        $('#""" +self.type+ """54').val($(this).val() ) ;
                                                                 
                                                                    }else
                                                                    {
                                                                       $('#""" +self.type+ """54').val('');
                                                                       inputpopclear($(this));
                                                                    }
                                                                 }); 
                                                                 
                                                                $('#""" +self.type+ """46').keyup(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                        inputpop($(this));
                                                                        $('#""" +self.type+ """64').val($(this).val() ) ;
                                                                 
                                                                    }else
                                                                    {
                                                                       $('#""" +self.type+ """64').val('') ;
                                                                       inputpopclear($(this));
                                                                    }
                                                                 }); 
                                                                 
                                                                $('#""" +self.type+ """56').keyup(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                        inputpop($(this));
                                                                        $('#""" +self.type+ """65').val($(this).val() ) ;
                                                                 
                                                                    }else
                                                                    {
                                                                       $('#""" +self.type+ """65').val('') ;
                                                                       inputpopclear($(this));
                                                                    }
                                                                 }); 
                                                                 
                                                                 $('#""" +self.type+ """22').focusout(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                        inputpop($(this));
                                                                    }else
                                                                    {
                                                                       $(this).val('');
                                                                       inputpopclear($(this));
                                                                    }
                                                                 });
                                                                 
                                                                
                                                                 
                                                                 
                                                                 
                                                                 $('#""" +self.type+ """33').focusout(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                        inputpop($(this));
                                                                    }else
                                                                    {
                                                                       $(this).val('');
                                                                       inputpopclear($(this));
                                                                    }
                                                                 });
                                                                 
                                                                 $('#""" +self.type+ """44').focusout(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                        inputpop($(this));
                                                                    }else
                                                                    {
                                                                       $(this).val('');
                                                                       inputpopclear($(this));
                                                                    }
                                                                 });
                                                                 
                                                                 $('#""" +self.type+ """55').focusout(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                        inputpop($(this));
                                                                    }else
                                                                    {
                                                                       $(this).val('');
                                                                       inputpopclear($(this));
                                                                    }
                                                                 });
                                                                 
                                                                 $('#""" +self.type+ """66').focusout(function ()
                                                                {
                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                        inputpop($(this));
                                                                    }else
                                                                    {
                                                                       $(this).val('');
                                                                       inputpopclear($(this));
                                                                    }
                                                                 });
                                                                 
                                                                $('#""" +self.type+ """22').keyup(function ()
                                                                {
                                                                    inputpop($(this));                                                                                   
                                                                 });
                                                                 
                                                                 $('#""" +self.type+ """33').keyup(function ()
                                                                {
                                                                    inputpop($(this));                                                                                   
                                                                 });
                                                                 
                                                                $('#""" +self.type+ """44').keyup(function ()
                                                                {
                                                                    inputpop($(this));                                                                                   
                                                                 });
                                                                 
                                                                 $('#""" +self.type+ """55').keyup(function ()
                                                                {
                                                                    inputpop($(this));                                                                                   
                                                                 });
                                                                 
                                                                 $('#""" +self.type+ """66').keyup(function ()
                                                                {
                                                                    inputpop($(this));                                                                                   
                                                                 });
                                                                 
                                                            """                         
                                             
                    self.jquery= self.jquery+"\n"  
                    
                    """
                    for key in sorted(self.read_write_inputs.keys()):
                            #print self.read_write_inputs[key] 
                            if  self.read_write_inputs[key] == 'r':
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n" 
                                
                    """
                    
                    for key in sorted(self.read_write_inputs.keys()):
                        if  self.read_write_inputs[key] == 'r':
                            if  self.contains(self.listofemptyInputs,key):
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val('');" +"\n"     
                            else:
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n"
                                
 
                    self.jquery=  self.jquery+ "\n"  + "\n"  +  " });"
                        
                    print self.jquery    

 
                    
            elif self.crystalsystem_name == 'te':                     
                if  self.puntualgroupselected_name == '' or self.puntualgroupselected_name not in '4, -4, 4/m, 422, 4mm, -42m, 4/mmm':
                    self.questionGp = 'Point Group?'    
                    self.setPointGroup()
                    return
                    
                if  self.__request != None and len(self.__inputList) > 0:
                    for p in self.__inputList :
                        if self.puntualgroupselected_name in ('4mm', '-42m', '422', '4/mmm'):
                            if str(p.name) == "s11":       
                                self.s[0,0] = self.s[1,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s12":  
                                self.s[0,1] = self.s[1,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s13":  
                                self.s[0,2] = self.s[1,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s33":  
                                self.s[2,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s44":  
                                self.s[3,3] = self.s[4,4] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s66":  
                                self.s[5,5] = float (self.__request.POST.get(p.name, False))
                                
                            if str(p.name) == "c11":  
                                self.c[0,0] = self.c[1,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c12":  
                                self.c[0,1] = self.c[1,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c13":  
                                self.c[0,2] = self.c[1,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c33":  
                                self.c[2,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c44":  
                                self.c[3,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c66":  
                                self.c[5,5] = float (self.__request.POST.get(p.name, False))
                        elif self.puntualgroupselected_name in ('4', '-4', '4/m'): 
                            if str(p.name) == "s11": 
                                self.s[0,0] = self.s[1,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s12": 
                                self.s[0,1] = self.s[1,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s13": 
                                self.s[0,2] = self.s[1,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s16": 
                                self.s[0,5] = self.s[5,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s33": 
                                self.s[2,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s44": 
                                self.s[3,3] = self.s[4,4] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s66": 
                                self.s[5,5] = float (self.__request.POST.get(p.name, False))
                                
                            if str(p.name) == "c11":    
                                self.c[0,0] = self.c[1,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c12":    
                                self.c[0,1] = self.c[1,0] =  float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c13":    
                                self.c[0,2] = self.c[1,2] = self.c[2,0] = self.c[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c16":    
                                self.c[0,5] = self.c[5,0] =  float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c33":    
                                self.c[2,2] =  float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c44":    
                                self.c[3,3] = self.c[4,4] =  float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c66":    
                                self.c[5,5] = float (self.__request.POST.get(p.name, False))
    
                    if self.type == 's':
                        self.s[1,5] = self.s[5,1] = -self.s[0,5]
                        print (self.s)
                    elif self.type == 'c':
                        self.c[1,5] = self.c[5,1] = -self.c[0,5]
                        print (self.c)
                        
                        
                    self.sucess = 1;                        
                    return
                else:
                    self.questionGp = 'Point Group?'    
                    self.setPointGroup()
                    self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(name__exact=self.puntualgroupselected_name)     
                    self.setCatalogPropertyDetail() 
                    self.preparedataforjQuery(self.type )
                    self.jquery= self.jquery + """
                                                                    // inicio de codigo jQuery
                                                                    $('#divwarningpropertyvalues').hide();
                                                                    $(document).ready(
                                                                        function() 
                                                                        {
                                                                     """
                     
                    if self.puntualgroupselected_name in ('4mm', '-42m', '422', '4/mmm'):
                        self.listofemptyInputs.append(self.type+"22");
                        self.listofemptyInputs.append(self.type+"21");
                        self.listofemptyInputs.append(self.type+"23");
                        self.listofemptyInputs.append(self.type+"31");
                        self.listofemptyInputs.append(self.type+"32");
                        self.listofemptyInputs.append(self.type+"55");
                        self.jquery= self.jquery + """
                        
                                                                 $('#""" +self.type+ """11').keyup(function ()
                                                                    {
                                                                        if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                        inputpop($(this));
                                                                        $('#""" +self.type+ """22').val($(this).val() );
                                                                     
                                                                        }else
                                                                        {
                                                                           $('#""" +self.type+ """22').val('');
                                                                           inputpopclear($(this));
                                                                        }
                                                                     });
                                                                     
                                                                     
                                                                     $('#""" +self.type+ """12').keyup(function ()
                                                                    {
                                                                        if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """21').val($(this).val() ) ;
                                                                        }else
                                                                        {
                                                                           $('#""" +self.type+ """21').val('');
                                                                           inputpopclear($(this));
                                                                        }
                                                                     });
                                                                     
                                                                     
                                                                   $('#""" +self.type+ """13').keyup(function ()
                                                                    {
                                                                        if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """23').val($(this).val() ) ;
                                                                            $('#""" +self.type+ """31').val($(this).val() ) ;
                                                                            $('#""" +self.type+ """32').val($(this).val() ) ;
                                                                     
                                                                        }else
                                                                        {
                                                                            $('#""" +self.type+ """23').val('') ;
                                                                            $('#""" +self.type+ """31').val('') ;
                                                                            $('#""" +self.type+ """32').val('') ;
                                                                            inputpopclear($(this));
                                                                        }
                                                                     });
                                                                     
                                                                     $('#""" +self.type+ """33').focusout(function ()
                                                                    {
                                                                        if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                            inputpop($(this));
                                                                        }else
                                                                        {
                                                                           $(this).val('');
                                                                           inputpopclear($(this));
                                                                        }
                                                                     });
                                                                                 
                                                                     $('#""" +self.type+ """66').focusout(function ()
                                                                    {
                                                                        if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                            inputpop($(this));
                                                                        }else
                                                                        {
                                                                           $(this).val('');
                                                                           inputpopclear($(this));
                                                                        }
                                                                 });
                                                                     $('#""" +self.type+ """44').keyup(function ()
                                                                    {
                                                                        if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """55').val($(this).val());
                                                                     
                                                                        }else
                                                                        {
                                                                           $('#""" +self.type+ """55').val('');
                                                                           inputpopclear($(this));
                                                                        }
                                                                     });
                                                                     
                                                                    $('#""" +self.type+ """33').keyup(function ()
                                                                    {
                                                                        inputpop($(this));
                                                                    });
                                                                    
                                                                     
                                                                    
                                                                     $('#""" +self.type+ """66').keyup(function ()
                                                                    {
                                                                        inputpop($(this));
                                                                    });
                                                                     
                                                                     
                                                                     """                    
                                         
                    elif self.puntualgroupselected_name in ('4', '-4', '4/m'):
                        self.listofemptyInputs.append(self.type+"22");
                        self.listofemptyInputs.append(self.type+"21");
                        self.listofemptyInputs.append(self.type+"23");
                        self.listofemptyInputs.append(self.type+"31");
                        self.listofemptyInputs.append(self.type+"32");
                        self.listofemptyInputs.append(self.type+"61");
                        self.listofemptyInputs.append(self.type+"62");
                        self.listofemptyInputs.append(self.type+"26");
                        self.listofemptyInputs.append(self.type+"55");
                        self.jquery= self.jquery + """
                                                                 $('#""" +self.type+ """11').keyup(function ()
                                                                    {
                                                                        if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """22').val($(this).val());
                                                                        }else
                                                                        {
                                                                           $('#""" +self.type+ """22').val('');
                                                                           inputpopclear($(this));
                                                                        }
                                                                     });
                                                                     
                                                                     $('#""" +self.type+ """12').keyup(function ()
                                                                    {
                                                                        if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """21').val($(this).val());
                                                                        }else
                                                                        {
                                                                            $('#""" +self.type+ """21').val('');
                                                                            inputpopclear($(this));
                                                                        }
                                                                     });
                                                                     
                                                                     
                                                                   $('#""" +self.type+ """13').keyup(function ()
                                                                    {
                                                                        if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """23').val($(this).val());
                                                                            $('#""" +self.type+ """31').val($(this).val());
                                                                            $('#""" +self.type+ """32').val($(this).val());
                                                                        }else
                                                                        {
                                                                            $('#""" +self.type+ """23').val('');
                                                                            $('#""" +self.type+ """31').val('');
                                                                            $('#""" +self.type+ """32').val('');
                                                                            inputpopclear($(this));
                                                                        }
                                                                     });
                                                                     
                                   
                                                                     
                                                                     
                                                                    $('#""" +self.type+ """16').keyup(function ()
                                                                    {
                                                                        if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                            inputpop($(this));
                                                                            v = $(this).val()
                                                                             if ( isScientificNotation($(this).val()) == 1 )
                                                                                value = Number.parseFloat(v).toExponential();
                                                                            else
                                                                                value = v 
  
                                                                            $('#""" +self.type+ """61').val(value);
                                                                            $('#""" +self.type+ """62').val(-value);
                                                                            $('#""" +self.type+ """26').val(-value);
                                                                     
                                                                        }else
                                                                        {
                                                                            $('#""" +self.type+ """61').val('');
                                                                            $('#""" +self.type+ """62').val('');
                                                                            $('#""" +self.type+ """26').val('');
                                                                            inputpopclear($(this));
                                                                        }
                                                                     });
                                                                     
                                                                     $('#""" +self.type+ """33').focusout(function ()
                                                                    {
                                                                        if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                            inputpop($(this));
                                                                        }else
                                                                        {
                                                                           $(this).val('');
                                                                           inputpopclear($(this));
                                                                        }
                                                                     });
                                                                     
                                                                     
                                                                     
                                                                     
                                                                    $('#""" +self.type+ """44').keyup(function ()
                                                                    {
                                                                        if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                        inputpop($(this));
                                                                        $('#""" +self.type+ """55').val($(this).val());
                                                                     
                                                                        }else
                                                                        {
                                                                           $('#""" +self.type+ """55').val('');
                                                                           inputpopclear($(this));
                                                                        }
                                                                     });
                                                                     
                                                                     $('#""" +self.type+ """66').focusout(function ()
                                                                    {
                                                                        if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                            inputpop($(this));
                                                                        }else
                                                                        {
                                                                           $(this).val('');
                                                                           inputpopclear($(this));
                                                                        }
                                                                     });
                                                                     
                                                                    $('#""" +self.type+ """33').keyup(function ()
                                                                    {
                                                                        inputpop($(this));
                                                                    });
                                                                    
                                                                     $('#""" +self.type+ """66').keyup(function ()
                                                                    {
                                                                        inputpop($(this));
                                                                    });
                                                                     
                                                                     
                                                                     
                                                                     
                                                                     """
                   
                    self.jquery= self.jquery+"\n" 
                    """for key in sorted(self.read_write_inputs.keys()):
                            #print self.read_write_inputs[key] 
                            if  self.read_write_inputs[key] == 'r':
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n" 
                    """
                    for key in sorted(self.read_write_inputs.keys()):
                        if  self.read_write_inputs[key] == 'r':
                            if  self.contains(self.listofemptyInputs,key):
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val('');" +"\n"     
                            else:
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n"
                                
                                
 
                    self.jquery=  self.jquery+ "\n"  + "\n"  +  " });"
                        
                    print self.jquery 
                    
                    
            elif self.crystalsystem_name == 'm':   

                if  self.__request != None and len(self.__inputList) > 0:
                    
                    for p in self.__inputList :
                        if self.axisselected_name  == 'x2':
                            if str(p.name) == "s11":  
                                self.s[0,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s12": 
                                self.s[0,1] = self.s[1,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s13": 
                                self.s[0,2] = self.s[2,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s15": 
                                self.s[0,4] = self.s[4,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s22": 
                                self.s[1,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s23": 
                                self.s[1,2] = self.s[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s25": 
                                self.s[1,4] = self.s[4,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s33": 
                                self.s[2,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s35": 
                                self.s[2,4] = self.s[4,2] =float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s44": 
                                self.s[3,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s46": 
                                self.s[3,5] = self.s[5,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s55": 
                                self.s[4,4] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s66": 
                                self.s[5,5] = float (self.__request.POST.get(p.name, False))
                              
                            
                            
                            if str(p.name) == "c11":    
                                self.c[0,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c12":  
                                self.c[0,1] = self.c[1,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c13":  
                                self.c[0,2] = self.c[2,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c15":  
                                self.c[0,4] = self.c[4,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c22":  
                                self.c[1,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c23":  
                                self.c[1,2] = self.c[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c25":  
                                self.c[1,4] = self.c[4,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c33":  
                                self.c[2,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c35":  
                                self.c[2,4] = self.c[4,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c44":  
                                self.c[3,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c46":  
                                self.c[3,5] = self.c[5,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c55":  
                                self.c[4,4] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c66":  
                                self.c[5,5] = float (self.__request.POST.get(p.name, False))
                             
                        elif self.axisselected_name  == 'x3':
                            print self.axisselected_name
                            print p.name
                            print self.__request.POST.get(p.name, False)
                            if str(p.name) == "s11":  
                                self.s[0,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s12":
                                self.s[0,1] = self.s[1,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s13":
                                self.s[0,2] = self.s[2,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s16":
                                self.s[0,5] = self.s[5,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s22":
                                self.s[1,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s23":
                                self.s[1,2] = self.s[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s26":
                                self.s[1,5] = self.s[5,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s33":
                                self.s[2,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s36":
                                self.s[2,5] = self.s[5,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s44":
                                self.s[3,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s45":
                                self.s[3,4] = self.s[4,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s55":
                                self.s[4,4] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s66":
                                self.s[5,5] = float (self.__request.POST.get(p.name, False))
                            
                            
                            if str(p.name) == "c11":  
                                self.c[0,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c12":  
                                self.c[0,1] = self.c[1,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c13":  
                                self.c[0,2] = self.c[2,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c16":  
                                self.c[0,5] = self.c[5,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c22":  
                                self.c[1,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c23":  
                                self.c[1,2] = self.c[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c26":  
                                self.c[1,5] = self.c[5,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c33":  
                                self.c[2,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c36":  
                                self.c[2,5] = self.c[5,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c44":  
                                self.c[3,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c45":  
                                self.c[3,4] = self.c[4,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c55":  
                                self.c[4,4] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c66":  
                                self.c[5,5] = float (self.__request.POST.get(p.name, False))

                            
                    if self.type == 's':    
                        print self.s
                    elif self.type == 'c': 
                        print self.c 
                        
                    self.sucess = 1;  
                else:    
                    """if  self.puntualgroupselected_name == '':
                        self.message= 'All the point groups of this crystal system have the same matrix'
                        self.questionGp = 'Point Group?'    
                        self.setPointGroup()
                        return"""
                
                    self.message= 'All the point groups of this crystal system have the same matrix'
                    self.questionGp = 'Point Group?'    
                    self.setPointGroup()       
                
                    
                    if  self.axisselected_name   == '' or self.axisselected_name  not in 'x2, x3':
                        self.questionAxis = 'Where is the special axis?' 
                        self.setAxis()
                        return    
                    
                    self.questionAxis = 'Where is the special axis?' 
                    self.setAxis()
                    self.objAxisSelected=CatalogAxis.objects.get(name__exact=self.axisselected_name )  
                    self.setCatalogPropertyDetail() 
                    self.preparedataforjQuery(self.type )
                    
                    self.jquery= self.jquery + """
                                                                // inicio de codigo jQuery
                                                                $('#divwarningpropertyvalues').hide();
                                                                $(document).ready(
                                                                    function() 
                                                                    {
                                                                 """
                    if self.axisselected_name  == 'x2':
                        self.listofemptyInputs.append(self.type+"21");
                        self.listofemptyInputs.append(self.type+"31");
                        self.listofemptyInputs.append(self.type+"51");
                        self.listofemptyInputs.append(self.type+"32");
                        self.listofemptyInputs.append(self.type+"52");
                        self.listofemptyInputs.append(self.type+"53");
                        self.listofemptyInputs.append(self.type+"64");
                        self.jquery= self.jquery + """
                                                                      $('#""" +self.type+ """11').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                     $('#""" +self.type+ """12').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """21').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """21').val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """13').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """31').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """31').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """15').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """51').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                                $('#""" +self.type+ """51').val('') ;
                                                                                inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """22').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """23').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """32').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """32').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                        $('#""" +self.type+ """25').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """52').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """52').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """33').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """35').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));;
                                                                            $('#""" +self.type+ """53').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """53').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """44').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """46').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """64').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """64').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """55').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                                 
                                                                         $('#""" +self.type+ """66').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         
                                                                         $('#""" +self.type+ """11').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """22').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """33').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """44').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """55').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """66').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                       
                                                                         
                                                                         """
                    elif self.axisselected_name  == 'x3':
                        self.listofemptyInputs.append(self.type+"21");
                        self.listofemptyInputs.append(self.type+"31");
                        self.listofemptyInputs.append(self.type+"61");
                        self.listofemptyInputs.append(self.type+"32");
                        self.listofemptyInputs.append(self.type+"62");
                        self.listofemptyInputs.append(self.type+"63");
                        self.listofemptyInputs.append(self.type+"54");
                        self.jquery= self.jquery + """
                                                                        $('#""" +self.type+ """11').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                     $('#""" +self.type+ """12').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """21').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """21').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """13').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """31').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """31').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """16').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """61').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """61').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """23').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                             inputpop($(this));
                                                                            $('#""" +self.type+ """32').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """32').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                        $('#""" +self.type+ """26').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """62').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """62').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """36').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """63').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                                $('#""" +self.type+ """63').val('') ;
                                                                                inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """45').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """54').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """54').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """22').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         $('#""" +self.type+ """33').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         $('#""" +self.type+ """44').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         $('#""" +self.type+ """55').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         $('#""" +self.type+ """66').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                        $('#""" +self.type+ """11').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                        $('#""" +self.type+ """22').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                        $('#""" +self.type+ """33').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                        $('#""" +self.type+ """44').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                        $('#""" +self.type+ """55').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                        $('#""" +self.type+ """66').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                         """
                    self.jquery= self.jquery+"\n"                                                      
                    """for key in sorted(self.read_write_inputs.keys()):
                        #print self.read_write_inputs[key] 
                        if  self.read_write_inputs[key] == 'r':
                            self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n" 
                    """
                    for key in sorted(self.read_write_inputs.keys()):
                        if  self.read_write_inputs[key] == 'r':
                            if  self.contains(self.listofemptyInputs,key):
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val('');" +"\n"     
                            else:
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n"
                                
 
                    self.jquery=  self.jquery+ "\n"  + "\n"  +  " });"
                        
                    print self.jquery 

                
            elif self.crystalsystem_name == 'tg':       
                print self.crystalsystem_name
               
                if  self.puntualgroupselected_name == '' or self.puntualgroupselected_name not in '3, -3, 32, 3m, -3m':
                    self.questionGp = 'Point Group:'     
                    self.setPointGroup() 
                    #self.ShowBtnSend = 1                        
                    return
                
                if  self.__request != None and len(self.__inputList) > 0:
                    for p in self.__inputList :
                        if self.puntualgroupselected_name in ('32', '-3m', '3m'):
                            if str(p.name) == "s11":     
                                self.s[0,0] = self.s[1,1] =  float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s12": 
                                self.s[0,1] = self.s[1,0] = float (self.__request.POST.get(p.name, False))
                                self.s[5,5] = 2*(self.s[0,0] - self.s[0,1])
                            if str(p.name) == "s13": 
                                self.s[0,2] = self.s[1,2] = self.s[2,0] = self.s[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s14": 
                                self.s[0,3] = self.s[3,0] = float (self.__request.POST.get(p.name, False))
                                self.s[1,3] = self.s[3,1] = -self.s[0,3]
                                self.s[4,5] = self.s[5,4] = 2*self.s[0,3]         
                            if str(p.name) == "s33": 
                                self.s[2,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s44": 
                                self.s[3,3] = self.s[4,4] = float (self.__request.POST.get(p.name, False))
                                
                            if str(p.name) == "c11":    
                                self.c[0,0] = self.c[1,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c12":
                                self.c[0,1] = self.c[1,0] = float (self.__request.POST.get(p.name, False))
                                self.c[5,5] = (self.c[0,0] - self.c[0,1])/2
                            if str(p.name) == "c13":
                                self.c[0,2] = self.c[1,2] = self.c[2,0] = self.c[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c14":
                                self.c[0,3] = self.c[3,0] = self.c[4,5] = self.c[5,4] = float (self.__request.POST.get(p.name, False))
                                self.c[1,3] = self.c[3,1] = -self.c[0,3]
                            if str(p.name) == "c33":
                                self.c[2,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c44":
                                self.c[3,3] = self.c[4,4] = float (self.__request.POST.get(p.name, False))
                                
                        elif self.puntualgroupselected_name in ('3', '-3'):
                            if str(p.name) == "s11":    
                                self.s[0,0] = self.s[1,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s12":
                                self.s[0,1] = self.s[1,0] = float (self.__request.POST.get(p.name, False))
                                self.s[5,5] = 2*(self.s[0,0] - self.s[0,1])  
                            if str(p.name) == "s13":
                                self.s[0,2] = self.s[1,2] = self.s[2,0] = self.s[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s14":
                                self.s[0,3] = self.s[3,0] = float (self.__request.POST.get(p.name, False))
                                self.s[1,3] = self.s[3,1] = -self.s[0,3]
                                self.s[4,5] = self.s[5,4] = 2*self.s[0,3]
                            if str(p.name) == "s25":
                                self.s[1,4] = self.s[4,1] = float (self.__request.POST.get(p.name, False))
                                self.s[0,4] = self.s[4,0] = -self.s[1,4]
                                self.s[3,5] = self.s[5,3] = 2*self.s[1,4]
                            if str(p.name) == "s33":
                                self.s[2,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "s44":
                                self.s[3,3] = self.s[4,4] = float (self.__request.POST.get(p.name, False))
                                
                                
                                
                            if str(p.name) == "c11":       
                                self.c[0,0] = self.c[1,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c12":  
                                self.c[0,1] = self.c[1,0] = float (self.__request.POST.get(p.name, False))
                                self.c[5,5] = (self.c[0,0] - self.c[0,1])/2
                            if str(p.name) == "c13":  
                                self.c[0,2] = self.c[1,2] = self.c[2,0] = self.c[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c14":  
                                self.c[0,3] = self.c[3,0] = self.c[4,5] = self.c[5,4] = float (self.__request.POST.get(p.name, False))
                                self.c[1,3] = self.c[3,1] = -self.c[0,3]
                            if str(p.name) == "c25":  
                                self.c[1,4] = self.c[4,1] = self.c[3,5] = self.c[5,3] = float (self.__request.POST.get(p.name, False))
                                self.c[0,4] = self.c[4,0] = -self.c[1,4]
                            if str(p.name) == "c33":  
                                self.c[2,2] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "c44":  
                                self.c[3,3] = self.c[4,4] = float (self.__request.POST.get(p.name, False))
                
                    if self.type == 's':    
                        print self.s
                    elif self.type == 'c': 
                        print self.c 
                                
                    self.sucess = 1;
                else:

                    self.questionGp = 'Point Group:'     
                    self.setPointGroup() 
                    self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(name__exact=self.puntualgroupselected_name)    
                    self.setCatalogPropertyDetail()
                    
                    self.preparedataforjQuery(self.type )
                    
                    self.jquery=self.jquery +  """
                                                                    // inicio de codigo jQuery
                                                                    $('#divwarningpropertyvalues').hide();
                                                                    $(document).ready(
                                                                        function() 
                                                                        {
                                                                     """
                    if self.puntualgroupselected_name in ('32', '-3m', '3m'):
                        self.listofemptyInputs.append(self.type+"22");
                        self.listofemptyInputs.append(self.type+"21");
                        self.listofemptyInputs.append(self.type+"66");
                        self.listofemptyInputs.append(self.type+"31");
                        self.listofemptyInputs.append(self.type+"32");
                        self.listofemptyInputs.append(self.type+"23");
                        self.listofemptyInputs.append(self.type+"41");
                        self.listofemptyInputs.append(self.type+"24");
                        self.listofemptyInputs.append(self.type+"42");
                        self.listofemptyInputs.append(self.type+"56");
                        self.listofemptyInputs.append(self.type+"65");
                        self.listofemptyInputs.append(self.type+"55");
                        self.jquery= self.jquery + """
                                                                      
                                                                     $('#""" +self.type+ """11').keyup(function ()
                                                                        { 
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            
                                                                            $('#""" +self.type+ """22').val($(this).val()) ;   
                                                                                                                                                    
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """22').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         
                                                                         $('#""" +self.type+ """11').change(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                             
                                                                            $('#""" +self.type+ """21').val($('#""" +self.type+ """12').val() ) ;
    
                                                                       """
                                            
                        if self.type=="s" :                                              
                            self.jquery= self.jquery + """
                                                                            v =2* ($(this).val()-$('#""" +self.type+ """12').val());
                                                                            """
                        if self.type=="c" : 
                            self.jquery= self.jquery + """
                                                                            v =($(this).val()-$('#""" +self.type+ """12').val()) / 2; 
                                                                            """
                                                                                                                       
                                                                            
                        self.jquery= self.jquery +  """
                                                                                if ( isScientificNotation($(this).val()) == 1 )
                                                                                     value = Number.parseFloat(v).toExponential();
                                                                                else
                                                                                    value = v  
                                                                                    
                                                                                $('#""" +self.type+ """66').val(value) ;
                                                                                
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """21').val('') ;
                                                                               $('#""" +self.type+ """66').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                          $('#""" +self.type+ """13').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """31').val($(this).val() ) ;
                                                                            $('#""" +self.type+ """32').val($(this).val() ) ;
                                                                            $('#""" +self.type+ """23').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                                $('#""" +self.type+ """31').val('') ;
                                                                                $('#""" +self.type+ """32').val('') ;
                                                                                $('#""" +self.type+ """23').val('') ;
                                                                                inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                          $('#""" +self.type+ """12').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """21').val($(this).val() ) ;
 
                                                                       """
                                            
                        if self.type=="s" :                                              
                            self.jquery= self.jquery + """
                                                                            v =2* ($('#""" +self.type+ """11').val()-$(this).val());
                                                                            """
                        if self.type=="c" : 
                            self.jquery= self.jquery + """
                                                                            v =($('#""" +self.type+ """11').val()-$(this).val()) / 2;
                                                                            """
                                                                                                                       
                                                                            
                        self.jquery= self.jquery +  """
                                                                                if ( isScientificNotation($(this).val()) == 1 )
                                                                                    value = Number.parseFloat(v).toExponential();
                                                                                else
                                                                                   value = v  
                                                                                   
                                                                                 $('#""" +self.type+ """66').val(value) ;
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """21').val('') ;
                                                                               $('#""" +self.type+ """66').val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                          $('#""" +self.type+ """13').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """31').val($(this).val() ) ;
                                                                            $('#""" +self.type+ """32').val($(this).val() ) ;
                                                                            $('#""" +self.type+ """23').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """31').val('') ;
                                                                               $('#""" +self.type+ """32').val('') ;
                                                                               $('#""" +self.type+ """23').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                       $('#""" +self.type+ """14').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """41').val($(this).val() ) ;
                                                                            
                                                                            
                                                                            v = $(this).val(); 
                                                                             if ( isScientificNotation($(this).val()) == 1 )
                                                                                value = Number.parseFloat(-v).toExponential();
                                                                            else
                                                                                  value = -v 
                                                                                  
                                                                         
                                                                            $('#""" +self.type+ """24').val(value ) ;
                                                                            $('#""" +self.type+ """42').val(value  ) ;

                                                                            """
                                                                            
                        if self.type =="s":                                                  
                            self.jquery= self.jquery + """  
                                                                            if ( isScientificNotation($(this).val()) == 1 )
                                                                                value = Number.parseFloat(2*$(this).val() ).toExponential();
                                                                            else                                                                          
                                                                                value = 2*$(this).val();
                                                                            
                                                                            $('#""" +self.type+ """56').val(value) ;
                                                                            $('#""" +self.type+ """65').val(value) ;
                                                                                
                                                                            """
                        elif self.type =="c":    
                            self.jquery= self.jquery + """  
                                                                            if ( isScientificNotation($(this).val()) == 1 )
                                                                                value = Number.parseFloat($(this).val() ).toExponential();
                                                                            else                                                                          
                                                                                value = $(this).val();
                                                                                
                                                                              $('#""" +self.type+ """56').val(value ) ;
                                                                              $('#""" +self.type+ """65').val(value ) ;
                                                                            """
                                                                            
                        self.jquery= self.jquery +  """
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """41').val('') ;
                                                                               $('#""" +self.type+ """24').val('') ;
                                                                               $('#""" +self.type+ """42').val('') ;
                                                                              $('#""" +self.type+ """56').val('') ;
                                                                              $('#""" +self.type+ """65').val('') ;
                                                                              inputpopclear($(this));
                                                                        
                                                                            }
                                                                         });
                                                                         """
  
                                                                        
                        self.jquery= self.jquery +"""
                                                                         
                                                                       $('#""" +self.type+ """44').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """55').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """55').val('' ) ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """33').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                $('#divwarningpropertyvalues').hide();
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         
                                                                         $('#""" +self.type+ """11').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """33').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                         
                                                                         """ 
                    
                    
                     
                        
                    elif self.puntualgroupselected_name in ('3', '-3'):
                        self.listofemptyInputs.append(self.type+"22");
                        self.listofemptyInputs.append(self.type+"21");
                        self.listofemptyInputs.append(self.type+"66");
                        self.listofemptyInputs.append(self.type+"31");
                        self.listofemptyInputs.append(self.type+"32");
                        self.listofemptyInputs.append(self.type+"23");
                        self.listofemptyInputs.append(self.type+"41");
                        self.listofemptyInputs.append(self.type+"24");
                        self.listofemptyInputs.append(self.type+"42");
                        self.listofemptyInputs.append(self.type+"56");
                        self.listofemptyInputs.append(self.type+"65");
                        self.listofemptyInputs.append(self.type+"52");
                        
                        
                        self.listofemptyInputs.append(self.type+"15");
                        self.listofemptyInputs.append(self.type+"51");
                        self.listofemptyInputs.append(self.type+"46");
                        self.listofemptyInputs.append(self.type+"64");
                        self.listofemptyInputs.append(self.type+"55");
                        
                        
                        
                        self.jquery= self.jquery + """
                                                                     $('#""" +self.type+ """11').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """22').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """22').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """11').change(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            $('#divwarningpropertyvalues').hide();
                                                                            $('#""" +self.type+ """21').val($('#""" +self.type+ """12').val()) ;

                                                                       """
                                            
                        if self.type=="s" :                                              
                            self.jquery= self.jquery + """
                                                                            v =2* ($(this).val()-$('#""" +self.type+ """12').val());
                                                                            
                                                                            if ( isScientificNotation($(this).val()) == 1 )
                                                                                value = Number.parseFloat(v ).toExponential();
                                                                            else                                                                          
                                                                                value = v;
                                                                                
                                                                            
                                                                            """
                        if self.type=="c" : 
                            self.jquery= self.jquery + """
                                                                            v =($(this).val()-$('#""" +self.type+ """12')) / 2;
                                                                            if ( isScientificNotation($(this).val()) == 1 )
                                                                                value = Number.parseFloat(v).toExponential();
                                                                            else                                                                          
                                                                                value = v;

                                                                            """
                                                                                                                       
                                                                            
                        self.jquery= self.jquery +  """
                                                                             
                                                                            if(Number(value).toPrecision() != 'NaN')
                                                                                $('#""" +self.type+ """66').val(value) ;                                                                     
                                                                            else                                                                          
                                                                                $('#""" +self.type+ """66').val('') ;
                                                                        
                                                                                
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """21').val('' ) ;
                                                                               $('#""" +self.type+ """66').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                          $('#""" +self.type+ """13').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """31').val($(this).val() ) ;
                                                                            $('#""" +self.type+ """32').val($(this).val() ) ;
                                                                            $('#""" +self.type+ """23').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """31').val('') ;
                                                                               $('#""" +self.type+ """32').val('') ;
                                                                               $('#""" +self.type+ """23').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         
                                                                         
                                                                          $('#""" +self.type+ """12').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """21').val($(this).val() ) ;     
                                                                       """
                                            
                        if self.type=="s" :                                              
                            self.jquery= self.jquery + """
                                                                            v =2* ($('#""" +self.type+ """11').val()-$(this).val());
                                                                             if ( isScientificNotation($(this).val()) == 1 )
                                                                                value = Number.parseFloat(v).toExponential();
                                                                            else                                                                          
                                                                                value = v;
                                                                             
                                                                            
                                                                            """
                        if self.type=="c" : 
                            self.jquery= self.jquery + """
                                                                            v =($('#""" +self.type+ """11').val()-$(this).val()) / 2;
                                                                             if ( isScientificNotation($(this).val()) == 1 )
                                                                                value = Number.parseFloat(v).toExponential();
                                                                            else                                                                          
                                                                                value = v;
                                                                           
                                                                            
                                                                            """
                                                                                                                       
                                                                            
                        self.jquery= self.jquery +  """
                                                                            if(Number(value).toPrecision() != 'NaN')
                                                                                $('#""" +self.type+ """66').val(value) ;                                                                     
                                                                            else                                                                          
                                                                                $('#""" +self.type+ """66').val('') ;
                                                                                  
                                                                            }else
                                                                            {
                                                                                $('#""" +self.type+ """21').val('') ;   
                                                                                $('#""" +self.type+ """66').val('') ;
                                                                                inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                          $('#""" +self.type+ """13').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """31').val($(this).val() ) ;
                                                                            $('#""" +self.type+ """32').val($(this).val() ) ;
                                                                            $('#""" +self.type+ """23').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """31').val('') ;
                                                                               $('#""" +self.type+ """32').val('') ;
                                                                               $('#""" +self.type+ """23').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                       $('#""" +self.type+ """14').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """41').val($(this).val() ) ;
                                                                            
                                                                            v = -$(this).val() 
                                                                             if ( isScientificNotation($(this).val()) == 1 )
                                                                                value = Number.parseFloat(v).toExponential();
                                                                            else                                                                          
                                                                                value = v;       
                                                                                
                                                                            $('#""" +self.type+ """24').val(value ) ;
                                                                            $('#""" +self.type+ """42').val(value ) ;
                                                                            """
                                                                            
                        if self.type =="s":                                                  
                            self.jquery= self.jquery + """  
                                                                            v = 2*value;
                                                                            if ( isScientificNotation($(this).val()) == 1 )
                                                                                value = Number.parseFloat(v).toExponential();
                                                                            else                                                                          
                                                                                value = v;
                                                                        
                                                                            """
                        elif self.type =="c":    
                            self.jquery= self.jquery + """  
                                                                            v = $(this).val();
                                                                            if ( isScientificNotation($(this).val()) == 1 )
                                                                                value = Number.parseFloat(v).toExponential();
                                                                            else                                                                          
                                                                                value = v;                                                                                
                                                                             
                                                                            """
                                                                            
                        self.jquery= self.jquery +  """
                                                                                if(Number(value).toPrecision() != 'NaN')
                                                                                {
                                                                                    $('#""" +self.type+ """56').val(value) ;
                                                                                    $('#""" +self.type+ """65').val(value) ;   
                                                                                 }                                                                 
                                                                                else                     
                                                                                {                                                     
                                                                                    $('#""" +self.type+ """56').val('') ;
                                                                                    $('#""" +self.type+ """65').val('') ;
                                                                                    inputpopclear($(this));
                                                                                }
                                                                        
                                                                                
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """41').val('') ;
                                                                               $('#""" +self.type+ """56').val('') ;
                                                                               $('#""" +self.type+ """65').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         """
                                                                         
                        self.jquery= self.jquery +"""
                                                                         $('#""" +self.type+ """25').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """52').val($(this).val() ) ;
                                                                            
                                                                            v = -$(this).val() 
                                                                             if ( isScientificNotation($(this).val()) == 1 )
                                                                                value = Number.parseFloat(v).toExponential();
                                                                            else                                                                          
                                                                                value = v;
                                                                                
                                                                            $('#""" +self.type+ """15').val(value ) ;
                                                                            $('#""" +self.type+ """51').val(value  ) ;
                                                                            """
                                                                            
                        if self.type =="s":                                                  
                            self.jquery= self.jquery + """  
                                                                            v =2*value;
                                                                            if ( isScientificNotation($(this).val()) == 1 )
                                                                                value = Number.parseFloat(v).toExponential();
                                                                            else                                                                          
                                                                                value = v;
                                                                                
                                                                            
                                                                            """
                        elif self.type =="c":    
                            self.jquery= self.jquery + """  
                                                                            v = $(this).val();
                                                                            if ( isScientificNotation($(this).val()) == 1 )
                                                                                value = Number.parseFloat(v).toExponential();
                                                                            else                                                                          
                                                                                value = v;
                                                                                
             
                                                                            """
                                                                            
                        self.jquery= self.jquery +  """
                                                                                if(Number(value).toPrecision() != 'NaN')
                                                                                {  
                                                                                    $('#""" +self.type+ """46').val(value) ;
                                                                                    $('#""" +self.type+ """64').val(value) ;   
                                                                                 }                                                                 
                                                                                else                     
                                                                                {                                                     
                                                                                    $('#""" +self.type+ """46').val('') ;
                                                                                    $('#""" +self.type+ """64').val('') ;
                                                                                    inputpopclear($(this));
                                                                                }
                                                                                
                                                                             
                                                                            
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """15').val('') ;
                                                                               $('#""" +self.type+ """51').val('') ;
                                                                               $('#""" +self.type+ """46').val('') ;
                                                                               $('#""" +self.type+ """64').val('' ) ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         """
                                                                         
                                                                         
                                                                         
                                                                                   
                                              
                                                                        
                        self.jquery= self.jquery +"""
                                                                       $('#""" +self.type+ """44').keyup(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                            inputpop($(this));
                                                                            $('#""" +self.type+ """55').val($(this).val() ) ;
                                                                         
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """55').val('') ;
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """33').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                 inputpop($(this));   
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """11').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """33').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                
                                                                         """ 
                                                                          
                    
                    self.jquery= self.jquery+"\n" 
                    """for key in sorted(self.read_write_inputs.keys()):
                        #print self.read_write_inputs[key] 
                        if  self.read_write_inputs[key] == 'r':
                            self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n" 
                    """
                    
                    for key in sorted(self.read_write_inputs.keys()):
                        if  self.read_write_inputs[key] == 'r':
                            if  self.contains(self.listofemptyInputs,key):
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val('');" +"\n"     
                            else:
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n"
                                
 
                    self.jquery=  self.jquery+ "\n"  + "\n"  +  " });"
                        
                    print self.jquery
                    
                    
                    
        if self.catalogproperty_name == 'p':
            if self.crystalsystem_name == 'tc':          
 
                if  self.puntualgroupselected_name == '' or self.puntualgroupselected_name  not in '1, -1':
                    self.questionGp = 'Point Group:'   
                    self.setPointGroup()     
                    return
              
                if self.puntualgroupselected_name == '-1':
                    self.message ='This point group does not have priezoelectricity'
                    self.questionGp = 'Point Group:'   
                    self.setPointGroup() 
                    return
                
                if  self.__request != None and len(self.__inputList) > 0:
                    for p in self.__inputList :
                        if self.puntualgroupselected_name =='1':
                            if str(p.name) == "d11":                                     
                                self.d[0,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d12":
                                self.d[0,1] = float (input ('d12 = '))
                            if str(p.name) == "d13":
                                self.d[0,2] = float (input ('d13 = '))
                            if str(p.name) == "d14":
                                self.d[0,3] = float (input ('d14 = '))
                            if str(p.name) == "d15":
                                self.d[0,4] = float (input ('d15 = '))
                            if str(p.name) == "d16":
                                self.d[0,5] = float (input ('d16 = '))
                            if str(p.name) == "d21":
                                self.d[1,0] = float (input ('d21 = '))
                            if str(p.name) == "d22":
                                self.d[1,1] = float (input ('d22 = '))
                            if str(p.name) == "d23":
                                self.d[1,2] = float (input ('d23 = '))
                            if str(p.name) == "d24":
                                self.d[1,3] = float (input ('d24 = '))
                            if str(p.name) == "d25":
                                self.d[1,4] = float (input ('d25 = '))
                            if str(p.name) == "d26":
                                self.d[1,5] = float (input ('d26 = '))
                            if str(p.name) == "d31":
                                self.d[2,0] = float (input ('d31 = '))
                            if str(p.name) == "d32":
                                self.d[2,1] = float (input ('d32 = '))
                            if str(p.name) == "d33":
                                self.d[2,2] = float (input ('d33 = '))
                            if str(p.name) == "d34":
                                self.d[2,3] = float (input ('d34 = '))
                            if str(p.name) == "d35":
                                self.d[2,4] = float (input ('d35 = '))
                            if str(p.name) == "d36":
                                self.d[2,5] = float (input ('d36 = ')) 
                    print self.d        
                    
                    self.sucess = 1;    
                    return
                                
                                
                          
                            
                else:    

                    self.questionGp = 'Point Group:'   
                    self.setPointGroup() 
                    self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(name__exact=self.puntualgroupselected_name)    
                    #print self.objCatalogPointGroupSelected.name
                    #print self.type 
                    self.preparedataforjQuery(self.type )
                    self.setCatalogPropertyDetail()
                    self.jquery=self.jquery + """
                                                                // inicio de codigo jQuery
                                                                $('#divwarningpropertyvalues').hide();
                                                                $(document).ready(
                                                                    function() 
                                                                    {
                                                                 """
                    
                    for p in self.catalogPropertyDetail :
                        self.jquery= self.jquery + """
                                                                         $('#""" +p.name+ """').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +p.name+ """').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                         """
                
               
                        self.jquery= self.jquery+"\n" 
                        
                    for key in sorted(self.read_write_inputs.keys()):
                        #print self.read_write_inputs[key] 
                        if  self.read_write_inputs[key] == 'r':
                            self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n" 
                   

                                
 
                    self.jquery=  self.jquery+ "\n"  + "\n"  +  " });"
                        
                    print self.jquery
                
                
            if self.crystalsystem_name == 'm':

                if (self.axisselected_name == '' or self.axisselected_name not in 'x2, x3') or  (self.puntualgroupselected_name == '' or self.puntualgroupselected_name not in  '2, m, 2/m'):
                    self.questionAxis = 'Where is the special axis?' 
                    self.questionGp = 'Point Group:'      
                    self.setPointGroup() 
                    self.setAxis()              
                    return
                
                if self.puntualgroupselected_name == '2/m':
                    self.questionAxis = 'Where is the special axis?' 
                    self.questionGp = 'Point Group:' 
                    self.message='This point group does not have priezoelectricity'
                    self.setPointGroup() 
                    self.setAxis()
                    print self.message
                    return
                
                
                if  self.__request != None and len(self.__inputList) > 0:
                    for p in self.__inputList :
                        if self.axisselected_name == 'x2':
                            if self.puntualgroupselected_name == '2':
                                if str(p.name) == "d14":
                                    self.d[0,3] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d16":
                                    self.d[0,5] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d21":
                                    self.d[1,0] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d22":
                                    self.d[1,1] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d23":
                                    self.d[1,2] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d25":
                                    self.d[1,4] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d34":
                                    self.d[2,3] =float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d36":
                                    self.d[2,5] = float (self.__request.POST.get(p.name, False))
                            elif self.puntualgroupselected_name == 'm':
                                if str(p.name) == "d11":
                                    self.d[0,0] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d12":
                                    self.d[0,1] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d13":
                                    self.d[0,2] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d15":
                                    self.d[0,4] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d24":
                                    self.d[1,3] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d26":
                                    self.d[1,5] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d31":
                                    self.d[2,0] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d32":
                                    self.d[2,1] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d33":
                                    self.d[2,2] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d35":
                                    self.d[2,4] = float (self.__request.POST.get(p.name, False))
                            
                            
                        elif self.axisselected_name  == 'x3':
                            if self.puntualgroupselected_name == '2':
                                if str(p.name) == "d14":
                                    self.d[0,3] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d15":
                                    self.d[0,4] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d24":
                                    self.d[1,3] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d25":
                                    self.d[1,4] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d31":
                                    self.d[2,0] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d32":
                                    self.d[2,1] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d33":
                                    self.d[2,2] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d36":
                                    self.d[2,5] = float (self.__request.POST.get(p.name, False))
                            elif self.puntualgroupselected_name == 'm':
                                if str(p.name) == "d11":
                                    self.d[0,0] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d12":
                                    self.d[0,1] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d13":
                                    self.d[0,2] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d16":
                                    self.d[0,5] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d21":
                                    self.d[1,0] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d22":
                                    self.d[1,1] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d23":
                                    self.d[1,2] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d26":
                                    self.d[1,5] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d34":
                                    self.d[2,3] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d35":
                                    self.d[2,4] = float (self.__request.POST.get(p.name, False))    
                    print self.d
                    
                    self.sucess = 1;
                    return
                else:

                    self.questionAxis = 'Where is the special axis?' 
                    self.questionGp = 'Point Group:'     
                    self.setPointGroup()   
                    self.setAxis() 
                     
                    self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(name__exact=self.puntualgroupselected_name)  
                    self.objAxisSelected = CatalogAxis.objects.get(name__exact=self.axisselected_name)
                    #self.setCatalogPropertyDetail()
                    
                    self.preparedataforjQuery(self.type )
                    self.setCatalogPropertyDetail()
                    self.jquery= self.jquery +  """
                                                                    // inicio de codigo jQuery
                                                                    $('#divwarningpropertyvalues').hide();
                                                                    $(document).ready(
                                                                        function() 
                                                                        {
                                                                     """
                    
                    for p in self.catalogPropertyDetail :
                        self.jquery= self.jquery + """
                                                                        $('#""" +p.name+ """').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                        $('#""" +p.name+ """').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                         """
                
               
                        self.jquery= self.jquery+"\n" 
                    
                    for key in sorted(self.read_write_inputs.keys()):
                        #print self.read_write_inputs[key] 
                        if  self.read_write_inputs[key] == 'r':
                            self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n" 
                    

 
                    self.jquery=  self.jquery+ "\n"  + "\n"  +  " });"
                        
                    print self.jquery
                    
                    
                
            if self.crystalsystem_name == 'o':
                if  self.puntualgroupselected_name == '' or self.puntualgroupselected_name not  in '222, 2mm, mmm' :
                    self.questionGp = 'Point Group:'        
                    self.setPointGroup() 
                    return
           
                if self.puntualgroupselected_name == 'mmm':
                    self.message ='This point group does not have priezoelectricity'
                    self.questionGp = 'Point Group:'        
                    self.setPointGroup() 
                    return
                
                if  self.__request != None and len(self.__inputList) > 0:
                    for p in self.__inputList :                         
                        if self.puntualgroupselected_name == '222':
                            if str(p.name) == "d14":
                                self.d[0,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d25":
                                self.d[1,4] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d36":
                                self.d[2,5] = float (self.__request.POST.get(p.name, False))
                        elif self.puntualgroupselected_name == '2mm':
                            if str(p.name) == "d15":
                                self.d[0,4] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d24":
                                self.d[1,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d31":
                                self.d[2,0] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d32":
                                self.d[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d33":
                                self.d[2,2] = float (self.__request.POST.get(p.name, False))
                        elif self.puntualgroupselected_name == '2mm':
                            self.message ='This point group does not have priezoelectricity'

                    print self.d
                    self.sucess = 1;
                    return
                else:
               
                    self.questionGp = 'Point Group:' 
                    self.setPointGroup()  
                    self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(name__exact=self.puntualgroupselected_name) 
                    self.preparedataforjQuery(self.type )
                    self.setCatalogPropertyDetail()
                    self.jquery= self.jquery + """
                                                                    // inicio de codigo jQuery
                                                                    $('#divwarningpropertyvalues').hide();
                                                                    $(document).ready(
                                                                        function() 
                                                                        {
                                                                     """
                    
                    for p in self.catalogPropertyDetail :
                        self.jquery= self.jquery + """                                                                       
                                                                        $('#""" +p.name+ """').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));                                                                          
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                        $('#""" +p.name+ """').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                         """
                
               
                        self.jquery= self.jquery+"\n" 
                        
                    for key in sorted(self.read_write_inputs.keys()):
                        #print self.read_write_inputs[key] 
                        if  self.read_write_inputs[key] == 'r':
                            self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n" 
                                
 
                    self.jquery=  self.jquery+ "\n"  + "\n"  +  " });"
                        
                    print self.jquery
                    
                    
                    
                   
            
            
            if self.crystalsystem_name == 'te':
                if  self.puntualgroupselected_name == '' or self.puntualgroupselected_name not in '4, -4, 4/m, 422, 4mm, -42m, 4/mmm':
                    self.questionGp = 'Point Group:'    
                    self.setPointGroup()           
                    return
               
                if self.puntualgroupselected_name in ('4/m', '4/mmm'):
                    self.message ='This point group does not have priezoelectricity'
                    self.questionGp = 'Point Group:'    
                    self.setPointGroup()   
                    return
                
                if  self.__request != None and len(self.__inputList) > 0:
                    for p in self.__inputList :         
                        if self.puntualgroupselected_name == '4': 
                            if str(p.name) == "d14":   
                                self.d[0,3] = float (self.__request.POST.get(p.name, False))
                                self.d[1,4] = -self.d[0,3]
                            if str(p.name) == "d15":
                                self.d[0,4] = self.d[1,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d31":
                                self.d[2,0] = self.d[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d33":
                                self.d[2,2] = float (self.__request.POST.get(p.name, False))
                        
                        elif self.puntualgroupselected_name == '-4':
                            if str(p.name) == "d14":
                                self.d[0,3] = self.d[1,4] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d15":
                                self.d[0,4] = float (self.__request.POST.get(p.name, False))
                                self.d[1,3] = -self.d[0,4]
                            if str(p.name) == "d31":
                                self.d[2,0] = float (self.__request.POST.get(p.name, False))
                                self.d[2,1] = -self.d[2,0]
                            if str(p.name) == "d36":
                                self.d[2,5] = float (self.__request.POST.get(p.name, False))
                        
                        elif self.puntualgroupselected_name == '422':
                            if str(p.name) == "d14":
                                self.d[0,3] = float (self.__request.POST.get(p.name, False))
                                self.d[1,4] = -self.d[0,3]
                        
                        elif self.puntualgroupselected_name == '4mm':
                            if str(p.name) == "d15":
                                self.d[0,4] = self.d[1,3] =float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d31":
                                self.d[2,0] = self.d[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d33":
                                self.d[2,2] = float (self.__request.POST.get(p.name, False))
                            
                        elif self.puntualgroupselected_name == '-42m':
                            if str(p.name) == "d14":
                                self.d[0,3] = self.d[1,4] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d36":
                                self.d[2,5] =  float (self.__request.POST.get(p.name, False))
                    
      

                    print self.d
                    self.sucess = 1;
                    return
                else:
                
                    self.questionGp = 'Point Group:'    
                    self.setPointGroup()   
                    self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(name__exact=self.puntualgroupselected_name) 
                    self.preparedataforjQuery(self.type )
                    self.setCatalogPropertyDetail() 
                    self.jquery= self.jquery + """
                                                                        // inicio de codigo jQuery
                                                                        $('#divwarningpropertyvalues').hide();
                                                                        $(document).ready(
                                                                            function() 
                                                                            {
                                                                         """
                    
                    if self.puntualgroupselected_name == '4':    
                        self.listofemptyInputs.append(self.type+"24");
                        self.listofemptyInputs.append(self.type+"25");
                        self.listofemptyInputs.append(self.type+"32");
                        self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """14').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));  
                                                                                     ;
                                                                                    v = -$(this).val()
                                                                                    
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                       value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                       value = v 
      
                                                                                    $('#""" +self.type+ """25').val(value);
                                                                                
                                                                             
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """25').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                             
                                                                             
                                                                            $('#""" +self.type+ """15').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    inputpop($(this));
                                                                                    v = $(this).val()
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                       value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                       value = v 
                                                                                       
                                                                                    $('#""" +self.type+ """24').val(value);
                                                                                
                                                                             
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """24').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                             
                                                                            $('#""" +self.type+ """31').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    v = $(this).val()
                                                                                    
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                       value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                       value = v 
                                                                                       
                                                                                    $('#""" +self.type+ """32').val(value);
                                                                             
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """32').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                        $('#""" +self.type+ """33').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this)); 
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """33').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                                 
                                                                             """
                    
                    elif self.puntualgroupselected_name == '-4':
                        self.listofemptyInputs.append(self.type+"24");
                        self.listofemptyInputs.append(self.type+"25");
                        self.listofemptyInputs.append(self.type+"32");
                        self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """14').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN')  {
                                                                                    inputpop($(this));
                                                                                    v = $(this).val();
                                                                                    
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                       value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                       value = v;
                                                                                       
                                                                                    $('#""" +self.type+ """25').val(value);
                                                                                
                                                                             
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """25').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                             
                                                                             
                                                                            $('#""" +self.type+ """15').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                   inputpop($(this));
                                                                                    v = -$(this).val();
                                                                                    
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                       value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                       value = v;
                                                                                       
                                                                                    $('#""" +self.type+ """24').val(value);
                                                                                
                                                                             
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """24').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                             
                                                                            $('#""" +self.type+ """31').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN')  {
                                                                                    inputpop($(this));
                                                                                    
                                                                                    v = $(this).val();
                                                                                    
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                       value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                       value = v;
                                                                                       
                                                                                    $('#""" +self.type+ """32').val(value);
                                                                                
                                                                             
                                                                                }else
                                                                                {                                                                                    
                                                                                   $('#""" +self.type+ """32').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                             $('#""" +self.type+ """36').focusout(function ()
                                                                                {
                                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                        inputpop($(this));   
                                                                                    }else
                                                                                    {
                                                                                       $(this).val('');
                                                                                       inputpopclear($(this));
                                                                                    }
                                                                                 });
                                                         
                                                                                $('#""" +self.type+ """36').keyup(function ()
                                                                                {                                                                            
                                                                                    inputpop($(this));                                                                          
                                                                                 });
                                                                             
                                                                             
                                                                             
                                                                             """
                    
                    elif self.puntualgroupselected_name == '422':
                        self.listofemptyInputs.append(self.type+"25");
                        self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """14').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    v = -$(this).val();
                                                                                    
                                                                                     if ( isScientificNotation($(this).val()) == 1 )
                                                                                       value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                       value = v;
                                                                                       
                                                                                    $('#""" +self.type+ """25').val(value);
                                                                                
                                                                             
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """25').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             """
                    
                    elif self.puntualgroupselected_name == '4mm':
                        self.listofemptyInputs.append(self.type+"24");
                        self.listofemptyInputs.append(self.type+"32");
                        self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """15').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    
                                                                                    v = $(this).val();                   
                                                                                                                                                 
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                       value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                       value = v;
                                                                                       
                                                                                    $('#""" +self.type+ """24').val(value);
                                                                                
                                                                             
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """24').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                             
                                                                             $('#""" +self.type+ """31').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN')  {
                                                                                    inputpop($(this));
                                                                                    
                                                                                    v = $(this).val();                                                                                
                                                                                     if ( isScientificNotation($(this).val()) == 1 )
                                                                                       value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                       value = v;
                                                                                    
                                                                                    $('#""" +self.type+ """32').val(value);
                                                                                
                                                                             
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """32').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                        $('#""" +self.type+ """33').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                                                                                                   
                                                                         $('#""" +self.type+ """33').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                             """
                        
                    elif self.puntualgroupselected_name == '-42m':
                        self.listofemptyInputs.append(self.type+"25");
                        self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """14').keyup(function ()
                                                                            {
                                                                                if($.isNumeric($(this).val())) {
                                                                                inputpop($(this));
                                                                                
                                                                                v = $(this).val();                                                                                
                                                                                if ( isScientificNotation($(this).val()) == 1 )
                                                                                   value = Number.parseFloat(v).toExponential();
                                                                                else
                                                                                   value = v;
                                                                                   
                                                                                $('#""" +self.type+ """25').val(value);
                                                                                
                                                                             
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """25').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                       $('#""" +self.type+ """36').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this));
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """36').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                         
                                                                             """
                    
                    
                    self.jquery= self.jquery+"\n" 
                    """    
                    for key in sorted(self.read_write_inputs.keys()):
                        #print self.read_write_inputs[key] 
                        if  self.read_write_inputs[key] == 'r':
                            self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n" 
                    """
                    
                    
                    #self.listofemptyInputs.append(self.type+"55");
                    for key in sorted(self.read_write_inputs.keys()):
                        if  self.read_write_inputs[key] == 'r':
                            if  self.contains(self.listofemptyInputs,key):
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val('');" +"\n"     
                            else:
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n"
                    
                                
 
                    self.jquery=  self.jquery+ "\n"  + "\n"  +  " });"
                        
                    print self.jquery
            
            
            
            if self.crystalsystem_name == 'c':
                if  self.puntualgroupselected_name == ''  or self.puntualgroupselected_name not in '23, m3, 432, -43m, m3m':
                    self.questionGp = 'Point Group:'         
                    self.setPointGroup()    
                    return
               
                if self.puntualgroupselected_name in ('m3', '432', 'm3m'):
                    self.message ='This point group does not have priezoelectricity'
                    self.questionGp = 'Point Group:'    
                    self.setPointGroup()    
                    return
                
                if  self.__request != None and len(self.__inputList) > 0:
                    for p in self.__inputList : 
                        if self.puntualgroupselected_name in ('23', '-43m'):
                            if str(p.name) == "d14":   
                                self.d[0,3] = self.d[1,4] = self.d[2,5] = float (self.__request.POST.get(p.name, False))
                    print self.d
                    self.sucess = 1;
                    return
                else:
                               
                    self.questionGp = 'Point Group:'    
                    self.setPointGroup()   
                    self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(name__exact=self.puntualgroupselected_name) 
                    self.preparedataforjQuery(self.type )
                    self.setCatalogPropertyDetail() 
                    self.listofemptyInputs.append(self.type+"25");
                    self.listofemptyInputs.append(self.type+"36");
                    self.jquery=self.jquery +  """
                                                                    // inicio de codigo jQuery
                                                                    $('#divwarningpropertyvalues').hide();
                                                                    $(document).ready(
                                                                        function() 
                                                                        {
                                                                     """
                    self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """14').keyup(function ()
                                                                            {
                                                                             
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    v = $(this).val();
                                                                                    
                                                                                     if ( isScientificNotation($(this).val()) == 1 )
                                                                                       value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                       value = v;
                                                                                       
                                                                                    $('#""" +self.type+ """25').val(value);
                                                                                    $('#""" +self.type+ """36').val(value);
                                                                                
                                                                                
                                                                             
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """25').val('');
                                                                                   $('#""" +self.type+ """36').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             """
                                             
                    self.jquery= self.jquery+"\n" 
                      
                    """  
                    for key in sorted(self.read_write_inputs.keys()):
                        #print self.read_write_inputs[key] 
                        if  self.read_write_inputs[key] == 'r':
                            self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n" 
                    """
                    #self.listofemptyInputs.append(self.type+"55");
                    for key in sorted(self.read_write_inputs.keys()):
                        if  self.read_write_inputs[key] == 'r':
                            if  self.contains(self.listofemptyInputs,key):
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val('');" +"\n"     
                            else:
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n"
                                
 
                    self.jquery=  self.jquery+ "\n"  + "\n"  +  " });"
                        
                    print self.jquery
                
                
                
            elif self.crystalsystem_name == 'tg':
                if  self.puntualgroupselected_name == '' or self.puntualgroupselected_name not in '3, -3, 32, 3m, -3m':
                    self.questionGp = 'Point Group:'       
                    self.setPointGroup()    
                    return
               
                if self.puntualgroupselected_name in ('-3', '-3m'):
                    self.message ='This point group does not have priezoelectricity'
                    self.questionGp = 'Point Group:'       
                    self.setPointGroup()     
                    return
                
                if self.puntualgroupselected_name == '3m':
                    if  self.axisselected_name == '' or self.axisselected_name not in 'x1, x2':
                        self.questionAxis = 'Where is the special axis?' 
                        self.questionGp = 'Point Group:'     
                        self.setPointGroup()   
                        self.setAxis() 
                        return 
                    
                    self.questionAxis = 'Where is the special axis?' 
                    self.setAxis() 
                    self.objAxisSelected = CatalogAxis.objects.get(name__exact=self.axisselected_name)
                
                
                if  self.__request != None and len(self.__inputList) > 0:
                    for p in self.__inputList : 
                        if self.puntualgroupselected_name == '3':  
                            if str(p.name) == "d11":   
                                self.d[0,0] = float (self.__request.POST.get(p.name, False))
                                self.d[0,1] = -self.d[0,0]
                                self.d[1,5] = -2*self.d[0,0]
                            if str(p.name) == "d14":   
                                self.d[0,3] = float (self.__request.POST.get(p.name, False))
                                self.d[1,4] = -self.d[0,3]
                            if str(p.name) == "d15":   
                                self.d[0,4] = self.d[1,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d22":   
                                self.d[1,1] = float (self.__request.POST.get(p.name, False))
                                self.d[1,0] = -self.d[1,1]
                                self.d[0,5] = -2*self.d[1,1]
                            if str(p.name) == "d31":   
                                self.d[2,0] = self.d[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d33":   
                                self.d[2,2] = float (self.__request.POST.get(p.name, False))
                                
                        if self.puntualgroupselected_name == '32':  
                            if str(p.name) == "d11":   
                                self.d[0,0] = float (self.__request.POST.get(p.name, False))
                                self.d[0,1] = -self.d[0,0]
                                self.d[1,5] = -2*self.d[0,0]
                            if str(p.name) == "d14":   
                                self.d[0,3] = float (self.__request.POST.get(p.name, False))
                                self.d[1,4] = -self.d[0,3]
                                
                        elif self.puntualgroupselected_name == '3m':
                            if self.axisselected_name == 'x1':
                                if str(p.name) == "d14":   
                                    self.d[0,3] = float (self.__request.POST.get(p.name, False))
                                    self.d[1,4] = -self.d[0,3]
                                if str(p.name) == "d15":   
                                    self.d[0,4] = self.d[1,3] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d22":   
                                    self.d[1,1] = float (input ('d22 = '))
                                    self.d[1,0] = -self.d[1,1]
                                    self.d[0,5] = -2*self.d[1,1]
                                if str(p.name) == "d31":   
                                    self.d[2,0] = self.d[2][1] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d33":   
                                    self.d[2,2] = float (self.__request.POST.get(p.name, False))
                                    
                            elif self.axisselected_name == 'x2':
                                if str(p.name) == "d11":   
                                    self.d[0,0] = float (self.__request.POST.get(p.name, False))
                                    self.d[0,1] = -self.d[0,0]
                                    self.d[1,5] = -2*self.d[0,0]
                                if str(p.name) == "d14":   
                                    self.d[0,3] = float (self.__request.POST.get(p.name, False))
                                    self.d[1,4] = -self.d[0,3]
                                if str(p.name) == "d15":   
                                    self.d[0,4] = self.d[1,3] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d31":   
                                    self.d[2,0] = self.d[2,1] = float (self.__request.POST.get(p.name, False))
                                if str(p.name) == "d33":   
                                    self.d[2,2] = float (self.__request.POST.get(p.name, False))
                            
                        
                    print self.d
                    self.sucess = 1;
                    return
                else:
                    

                    
                    self.questionGp = 'Point Group:'     
                    self.setPointGroup()   
                    self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(name__exact=self.puntualgroupselected_name)  
                    self.preparedataforjQuery(self.type )
                    self.setCatalogPropertyDetail() 
                    self.jquery=self.jquery +  """
                                                                // inicio de codigo jQuery
                                                                $('#divwarningpropertyvalues').hide();
                                                                $(document).ready(
                                                                    function() 
                                                                    {
                                                                 """
                                             
                                             
                    if self.puntualgroupselected_name == '3':  
                        self.listofemptyInputs.append(self.type+"12");
                        self.listofemptyInputs.append(self.type+"26");
                        self.listofemptyInputs.append(self.type+"25");
                        self.listofemptyInputs.append(self.type+"24");
                        self.listofemptyInputs.append(self.type+"21");
                        self.listofemptyInputs.append(self.type+"16");
                        self.listofemptyInputs.append(self.type+"32");
                        self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """11').keyup(function ()
                                                                            {
                                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                        inputpop($(this));
                                                                                        v = -$(this).val();
                                                                                       
                                                                                        if ( isScientificNotation($(this).val()) == 1 )
                                                                                        {
                                                                                          value = Number.parseFloat(v).toExponential();                                                                              
                                                                                          $('#""" +self.type+ """26').val( Number.parseFloat(  2*(value)  ).toExponential() );
                                                                                        }
                                                                                        else
                                                                                        {
                                                                                          value = v                                                                                   
                                                                                          $('#""" +self.type+ """26').val(2*(value));
                                                                                        }
                                                                                        
                                                                                        $('#""" +self.type+ """12').val(value);
  
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """12').val('');                                                                                   
                                                                                   $('#""" +self.type+ """26').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                             
                                                                            $('#""" +self.type+ """14').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    v = -$(this).val();
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                      value = v 
      
                                                                                    $('#""" +self.type+ """25').val(value);
                                                                                 
                                                                                }else
                                                                                {
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                            $('#""" +self.type+ """15').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    inputpop($(this));
                                                                                    value = $(this).val();
                                                                                    
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                      value = v 
                                                                                      
                                                                                    $('#""" +self.type+ """24').val(value);
                                                                                 
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """24').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                            $('#""" +self.type+ """22').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    value = -$(this).val();
                                                                                    
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                    {
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                      $('#""" +self.type+ """16').val( Number.parseFloat(2*(value) ).toExponential() );
                                                                                    }
                                                                                    else
                                                                                    {
                                                                                      value = v;
                                                                                      $('#""" +self.type+ """16').val(2*(value));
                                                                                    }
                                                                                      
                                                                                    $('#""" +self.type+ """21').val(value);

                                                                                 
                                                                                }else
                                                                                {
                                                                                    $('#""" +self.type+ """21').val('');
                                                                                    $('#""" +self.type+ """16').val('');        
                                                                                    inputpopclear($(this));                                                                            
                                                                                }
                                                                             });
                                                                             
                                                                             
                                                                            $('#""" +self.type+ """31').keyup(function ()
                                                                            {
                                                                               if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                   
                                                                                    v = $(this).val();
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                      value = v 
                                                                                      
                                                                                    $('#""" +self.type+ """32').val(value);
                                                                                 
                                                                                }
                                                                                else
                                                                                {
                                                                                   $('#""" +self.type+ """32').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                                
                                                                             });
                                                                             
                                                                             $('#""" +self.type+ """33').focusout(function ()
                                                                                {
                                                                                    if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                        $('#divwarningpropertyvalues').hide();
                                                                                    }else
                                                                                    {
                                                                                       $(this).val('');
                                                                                    }
                                                                                 });
                                                                             
                                                                             $('#""" +self.type+ """33').keyup(function ()
                                                                            {                                                                            
                                                                                inputpop($(this));                                                                          
                                                                             });
                                                                             
                                                                             """
                    if self.puntualgroupselected_name == '32':  
                        self.listofemptyInputs.append(self.type+"12");
                        self.listofemptyInputs.append(self.type+"26");
                        self.listofemptyInputs.append(self.type+"25");
                        self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """11').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    
                                                                                    v = -$(this).val();
                                                                                    
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                    {
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                      $('#""" +self.type+ """26').val(Number.parseFloat( 2*(value) ).toExponential() );
                                                                                    }
                                                                                    else
                                                                                    {
                                                                                      value = v;
                                                                                      $('#""" +self.type+ """26').val(2*(value));
                                                                                    }
                                                                                      
                                                                                    $('#""" +self.type+ """12').val(value);
                                                                                 
    
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """12').val('');
                                                                                   $('#""" +self.type+ """26').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                             
                                                                            $('#""" +self.type+ """14').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    v = -$(this).val();
                                                                                    
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                      value = v 
                                                                                   
                                                                                    $('#""" +self.type+ """25').val(value);
    
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """25').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                             
                                                                             """
                    elif self.puntualgroupselected_name == '3m':
                        if self.axisselected_name == 'x1':
                            self.listofemptyInputs.append(self.type+"25");
                            self.listofemptyInputs.append(self.type+"24");
                            self.listofemptyInputs.append(self.type+"21");
                            self.listofemptyInputs.append(self.type+"16");
                            self.listofemptyInputs.append(self.type+"32");
                            self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """14').keyup(function ()
                                                                            {
                                                                               if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    inputpop($(this));
                                                                                    
                                                                                    s = -$(this).val();
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                      value = v
      
                                                                                    $('#""" +self.type+ """25').val(value);
            
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """25').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                             
                                                                            $('#""" +self.type+ """15').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    inputpop($(this));
                                                                                    
                                                                                    v = $(this).val();
                                                                                    
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                      value = v
      
                                                                                    $('#""" +self.type+ """24').val(value);
            
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """24').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                            $('#""" +self.type+ """22').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    inputpop($(this));
                                                                                    v = -$(this).val();
                                                                                    
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                    {
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                      $('#""" +self.type+ """16').val(Number.parseFloat( 2*(value) ).toExponential() );
                                                                                    }
                                                                                    else
                                                                                    {
                                                                                      value = v;
                                                                                      $('#""" +self.type+ """16').val(2*(value));
                                                                                    }
    
                                                                                    
                                                                                    $('#""" +self.type+ """21').val(value);
                                                                                 
            
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """21').val('');
                                                                                   $('#""" +self.type+ """21').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                             
                                                                            $('#""" +self.type+ """31').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    inputpop($(this));
                                                                                    
                                                                                    v = -$(this).val();
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                      value = v 
                                                                                      
                                                                                    $('#""" +self.type+ """32').val(value);
                   
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """32').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                            $('#""" +self.type+ """33').focusout(function ()
                                                                           {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                $('#divwarningpropertyvalues').hide();
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });  
                                                                             
                                                                        $('#""" +self.type+ """33').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this)); 
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """33').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                             
                                                                             """
                        elif self.axisselected_name == 'x2':
                            self.listofemptyInputs.append(self.type+"12");
                            self.listofemptyInputs.append(self.type+"26");
                            self.listofemptyInputs.append(self.type+"25");
                            self.listofemptyInputs.append(self.type+"24");
                            self.listofemptyInputs.append(self.type+"32");
                            self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """11').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    
                                                                                    v = -$(this).val();
                                                                                    
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                    {
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                      $('#""" +self.type+ """26').val(Number.parseFloat(2*(v) ).toExponential());
                                                                                    }
                                                                                    else
                                                                                    {
                                                                                      value = v 
                                                                                      $('#""" +self.type+ """26').val(2*(value));
                                                                                    }
      
                                                                                    $('#""" +self.type+ """12').val(value);
                                                                                    
                                                                                
                                                                                
                                                                             
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """12').val('');
                                                                                   $('#""" +self.type+ """26').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                             
                                                                            $('#""" +self.type+ """14').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    v = -$(this).val();
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                      value = v 
                                                                                    
                                                                                    $('#""" +self.type+ """25').val(value);
   
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """25').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                            $('#""" +self.type+ """15').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    inputpop($(this));
                                                                                    v = $(this).val();
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                      value = v 
                                                                                    
                                                                                    $('#""" +self.type+ """24').val(value);
   
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """24').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                             
                                                                             $('#""" +self.type+ """31').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    inputpop($(this));
                                                                                    v = $(this).val();
                                                                                    
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                      value = v
                                                                                    
                                                                                    $('#""" +self.type+ """32').val(value);
   
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """32').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                       
                                                                         
                                                                         $('#""" +self.type+ """33').focusout(function ()
                                                                        {
                                                                            if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                inputpop($(this)); 
                                                                            }else
                                                                            {
                                                                               $(this).val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                         
                                                                         $('#""" +self.type+ """33').keyup(function ()
                                                                        {                                                                            
                                                                            inputpop($(this));                                                                          
                                                                         });
                                                                             
                                                                             
                                                                             """
                                
                    
                                             
                    self.jquery= self.jquery+"\n" 
                    """     
                    for key in sorted(self.read_write_inputs.keys()):
                        #print self.read_write_inputs[key] 
                        if  self.read_write_inputs[key] == 'r':
                            self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n" 
                            
                    """
                    
                    #self.listofemptyInputs.append(self.type+"55");
                    for key in sorted(self.read_write_inputs.keys()):
                        if  self.read_write_inputs[key] == 'r':
                            if  self.contains(self.listofemptyInputs,key):
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val('');" +"\n"     
                            else:
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n"
                                
 
                    self.jquery=  self.jquery+ "\n"  + "\n"  +  " });"
                        
                    print self.jquery
                    
                    

                    
            elif self.crystalsystem_name == 'h':
                if  self.puntualgroupselected_name == '' or self.puntualgroupselected_name not in '6, -6, 6/m, 6mm, 622, -6m2, 6/mmm' :
                    self.questionGp = 'Point Group:'       
                    self.setPointGroup()    
                    return    

                if self.puntualgroupselected_name  in ('6/m', '6/mmm'):
                    self.message ='This point group does not have priezoelectricity' 
                    self.questionGp = 'Point Group:'       
                    self.setPointGroup()    
                    return
                
                if self.puntualgroupselected_name == '-6m2':
                    if  self.axisselected_name == '' or self.axisselected_name not in 'x1, x2':
                        self.questionAxis = 'Where is the special axis?' 
                        self.questionGp = 'Point Group:'     
                        self.setPointGroup()   
                        self.setAxis() 
                        return 
                    
                    self.questionAxis = 'Where is the special axis?' 
                    self.setAxis() 
                    self.objAxisSelected = CatalogAxis.objects.get(name__exact=self.axisselected_name)
                
                
                if  self.__request != None and len(self.__inputList) > 0:
                    for p in self.__inputList : 
                        if self.puntualgroupselected_name == '6':
                            if str(p.name) == "d14":   
                                self.d[0,3] = float (self.__request.POST.get(p.name, False))
                                self.d[1,4] = -self.d[0,3]
                            if str(p.name) == "d15":
                                self.d[0,4] = self.d[1,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d31":
                                self.d[2,0] = self.d[2,1] =float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d33":
                                self.d[2,2] = float (self.__request.POST.get(p.name, False))
                        
                        elif self.puntualgroupselected_name == '6mm':
                            if str(p.name) == "d15":                            
                                self.d[0,4] = self.d[1,3] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d31":
                                self.d[2,0] = self.d[2,1] = float (self.__request.POST.get(p.name, False))
                            if str(p.name) == "d33":
                                self.d[2,2] = float (self.__request.POST.get(p.name, False))
                        
                        elif self.puntualgroupselected_name == '622':
                            if str(p.name) == "d14":
                                self.d[0,3] = float (self.__request.POST.get(p.name, False))
                                self.d[1,4] = -self.d[0,3]
                        
                        elif self.puntualgroupselected_name == '-6':
                            if str(p.name) == "d11":
                                self.d[0,0] = float (self.__request.POST.get(p.name, False))
                                self.d[0,1] = -self.d[0,0]
                                self.d[1,5] = -2*self.d[0,0]
                            if str(p.name) == "d22":
                                self.d[1,1] = float (self.__request.POST.get(p.name, False))
                                self.d[1,0] = -self.d[1,1]
                                self.d[0,5] = -2*self.d[1,1]
                        
                        elif self.puntualgroupselected_name == '-6m2':
                            if self.axisselected_name == 'x1':
                                if str(p.name) == "d22":
                                    self.d[1,1] = float (self.__request.POST.get(p.name, False))
                                    self.d[1,0] = -self.d[1,1]
                                    self.d[0,5] = -2*self.d[1,1]
                            elif self.axisselected_name == 'x2':
                                if str(p.name) == "d11":
                                    self.d[0,0] = float (self.__request.POST.get(p.name, False))
                                    self.d[0,1] = -self.d[0,0]
                                    self.d[1,5] = -2*self.d[0,0]
                            
                        
                    print self.d
                    self.sucess = 1;
                    return
                else:

                    self.questionGp = 'Point Group:'     
                    self.setPointGroup()   
                    self.objCatalogPointGroupSelected = CatalogPointGroup.objects.get(name__exact=self.puntualgroupselected_name)  
                    self.preparedataforjQuery(self.type )
                    self.setCatalogPropertyDetail() 
                    self.jquery= self.jquery + """
                                                                    // inicio de codigo jQuery
                                                                    $('#divwarningpropertyvalues').hide();
                                                                    $(document).ready(
                                                                        function() 
                                                                        {
                                                                     """
                    
                    if self.puntualgroupselected_name == '6':
                        self.listofemptyInputs.append(self.type+"25");
                        self.listofemptyInputs.append(self.type+"24");
                        self.listofemptyInputs.append(self.type+"32");
                        self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """14').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    inputpop($(this));
                                                                                    v = -$(this).val();
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                      value = v; 
      
                                                                                    $('#""" +self.type+ """25').val(value);
                                            
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """25').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                            $('#""" +self.type+ """15').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    
                                                                                    v = $(this).val();
                                                                                    
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                      value = v;
                                                                                      
                                                                                    $('#""" +self.type+ """24').val(value);
                       
                                                                             
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """24').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                             $('#""" +self.type+ """31').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    
                                                                                    v = $(this).val();
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                      value = v;
                                                                                      
                                                                                    $('#""" +self.type+ """32').val(value);
        
                                                                             
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """32').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                            $('#""" +self.type+ """33').focusout(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    inputpop($(this));
                                                                                }else
                                                                                {
                                                                                   $(this).val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });  
                                                                             
                                                                             $('#""" +self.type+ """33').keyup(function ()
                                                                            {                                                                            
                                                                                inputpop($(this));                                                                          
                                                                             });

                                                                             """
                    
                    elif self.puntualgroupselected_name == '6mm':
                        self.listofemptyInputs.append(self.type+"24");
                        self.listofemptyInputs.append(self.type+"32");
                        self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """15').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    
                                                                                    v = $(this).val();
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                      value = v;
                                                                                      
                                                                                    $('#""" +self.type+ """24').val(value);
                                            
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """24').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                            $('#""" +self.type+ """31').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    inputpop($(this));
                                                                                    v = $(this).val();
                                                                                     if ( isScientificNotation($(this).val()) == 1 )
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                      value = v;
                                                                                      
                                                                                    $('#""" +self.type+ """32').val(value);
            
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """32').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
                                                                            $('#""" +self.type+ """33').focusout(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    inputpop($(this));
                                                                                }else
                                                                                {
                                                                                   $(this).val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });  
                                                                             
                                                                             $('#""" +self.type+ """33').keyup(function ()
                                                                            {                                                                            
                                                                                inputpop($(this));                                                                          
                                                                             });
                   
                                                                             """
                    
                    elif self.puntualgroupselected_name == '622':
                        self.listofemptyInputs.append(self.type+"25");
                        self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """14').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    v = -$(this).val();
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                    else
                                                                                      value = v;
                                                                                      
                                                                                    $('#""" +self.type+ """25').val(value);
                                            
                                                                                }else
                                                                                {
                                                                                   $('#""" +self.type+ """25').val('');
                                                                                   inputpopclear($(this));
                                                                                }
                                                                             });
                                                                             
        
                   
                                                                             """
                    
                    elif self.puntualgroupselected_name == '-6':
                        self.listofemptyInputs.append(self.type+"12");
                        self.listofemptyInputs.append(self.type+"26");
                        self.listofemptyInputs.append(self.type+"21");
                        self.listofemptyInputs.append(self.type+"16");
                        self.jquery= self.jquery + """
                                                                         $('#""" +self.type+ """11').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    inputpop($(this));
                                                                                    v = -$(this).val();
                                                                                    
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                    {
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                      $('#""" +self.type+ """26').val(Number.parseFloat(2*(v) ).toExponential());
                                                                                    }
                                                                                    else
                                                                                    {
                                                                                      value = v;
                                                                                    }
                                                                                      
                                                                                    $('#""" +self.type+ """12').val(value);
                                                                                 
                                                                                 
                                            
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """12').val('');
                                                                                $('#""" +self.type+ """26').val('')
                                                                                inputpopclear($(this));
                                                                            }
                                                                         });
                                                                             
                                                                        $('#""" +self.type+ """22').keyup(function ()
                                                                        {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    inputpop($(this));
                                                                                    value = -$(this).val();
                                                                                     if ( isScientificNotation($(this).val()) == 1 )
                                                                                    {
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                      $('#""" +self.type+ """16').val(Number.parseFloat(2*(v) ).toExponential());
                                                                                    }
                                                                                    else
                                                                                    {
                                                                                      value = v;
                                                                                    }
                                                                                    
                                                                                    $('#""" +self.type+ """21').val(value);
                                                                                 
            
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """21').val('');
                                                                                $('#""" +self.type+ """16').val('');
                                                                                inputpopclear($(this));
                                                                            }
                                                                         });
               
                                                                             """
                    
                    elif self.puntualgroupselected_name == '-6m2':
                        if self.axisselected_name == 'x1':
                            self.listofemptyInputs.append(self.type+"21");
                            self.listofemptyInputs.append(self.type+"16");
                            self.jquery= self.jquery + """
                                                                          $('#""" +self.type+ """22').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN') {
                                                                                    inputpop($(this));
                                                                                    v = -$(this).val();
                                                                                    if ( isScientificNotation($(this).val()) == 1 )
                                                                                    {
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                      $('#""" +self.type+ """16').val(Number.parseFloat(2*(v) ).toExponential());
                                                                                    }
                                                                                    else
                                                                                    {
                                                                                      value = v;
                                                                                    }
                     
                                                                                    
                                                                                    $('#""" +self.type+ """21').val(value);
                                                                                
                                            
                                                                            }else
                                                                            {
                                                                               $('#""" +self.type+ """21').val('');
                                                                               $('#""" +self.type+ """16').val('');
                                                                               inputpopclear($(this));
                                                                            }
                                                                         });
                                                                             """
                        elif self.axisselected_name == 'x2':
                            self.listofemptyInputs.append(self.type+"12");
                            self.listofemptyInputs.append(self.type+"26");
                            self.jquery= self.jquery + """
                                                                          $('#""" +self.type+ """11').keyup(function ()
                                                                            {
                                                                                if(Number($(this).val()).toPrecision() != 'NaN'){
                                                                                    inputpop($(this));
                                                                                    v = -$(this).val();
                                                                                     if ( isScientificNotation($(this).val()) == 1 )
                                                                                    {
                                                                                      value = Number.parseFloat(v).toExponential();
                                                                                      $('#""" +self.type+ """26').val(Number.parseFloat(2*(v) ).toExponential());
                                                                                    }
                                                                                    else
                                                                                    {
                                                                                      value = v;
                                                                                    }
                                                                                    
                                                                                    $('#""" +self.type+ """12').val(value);
                                                                                 
                                            
                                                                            }else
                                                                            {
                                                                                $('#""" +self.type+ """12').val('');
                                                                                $('#""" +self.type+ """26').val('');
                                                                                inputpopclear($(this));
                                                                            }
                                                                         });
                                                                             """
                
                    self.jquery= self.jquery+"\n" 
                    """
                    for key in sorted(self.read_write_inputs.keys()):
                        #print self.read_write_inputs[key] 
                        if  self.read_write_inputs[key] == 'r':
                            self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n" 
                    """
                    #self.listofemptyInputs.append(self.type+"55");
                    for key in sorted(self.read_write_inputs.keys()):
                        if  self.read_write_inputs[key] == 'r':
                            if  self.contains(self.listofemptyInputs,key):
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val('');" +"\n"     
                            else:
                                self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n"
                                
 
                    self.jquery=  self.jquery+ "\n"  + "\n"  +  " });"
                        
                    print self.jquery   
                    

                         
    #start setCatalogPropertyDetail
    def setCatalogPropertyDetail(self):
        '''print 'Property:'  + self.objProperty.name 
        print 'crystalsystem_id=' + str(self.objCatalogCrystalSystemSelected.pk)
        print 'type_id='  +  str(self.objTypeSelected.pk)
        print  'catalogaxis_id=' + str( self.objAxisSelected.pk)
        print  'catalogpointgroup_id=' +  str(self.objCatalogPointGroupSelected.pk)'''
        
        if self.catalogproperty_name == 'e':
            if (self.crystalsystem_name == 'iso') or ( self.crystalsystem_name == 'c') or (self.crystalsystem_name == 'h' ) or ( self.crystalsystem_name == 'o') or ( self.crystalsystem_name == 'tc'  ): 
                propertyDetail = CatalogPropertyDetail.objects.filter(type=self.objTypeSelected,crystalsystem=self.objCatalogCrystalSystemSelected).order_by('name')
                for obj in propertyDetail:
                    cpd=CatalogPropertyDetail()
                    cpd = obj
                    self.read_write_inputs[cpd.name] = 'w'
                    self.catalogPropertyDetail.append(cpd) 
                    del cpd   
             
            if (self.crystalsystem_name == 'm'):   
                propertyDetail = CatalogPropertyDetail.objects.filter(type=self.objTypeSelected,crystalsystem=self.objCatalogCrystalSystemSelected,catalogaxis=self.objAxisSelected).order_by('name')
                for obj in propertyDetail: 
                    cpd=CatalogPropertyDetail()
                    cpd=obj        
                    self.read_write_inputs[cpd.name] = 'w'        
                    self.catalogPropertyDetail.append(cpd)        
        
                return   
            
               
            if(self.crystalsystem_name == 'tg') or (self.crystalsystem_name == 'te'):                                                                                                                                                                                                                    
                propertyDetail = CatalogPropertyDetail.objects.filter(type=self.objTypeSelected,crystalsystem=self.objCatalogCrystalSystemSelected,catalogpointgroup=self.objCatalogPointGroupSelected).order_by('name')
                if not propertyDetail:  
                    objPuntualGroupGroups=PuntualGroupGroups.objects.filter(catalogpointgroup=self.objCatalogPointGroupSelected)          
                    for obj in objPuntualGroupGroups:
                        pgg=  PuntualGroupGroups()
                        pgg = obj   
                        propertyDetail = CatalogPropertyDetail.objects.filter(type=self.objTypeSelected,crystalsystem=self.objCatalogCrystalSystemSelected,puntualgroupnames=pgg.puntualgroupnames).order_by('name')
                        if  propertyDetail:
                            for obj in propertyDetail:
                                cpd=CatalogPropertyDetail()
                                cpd = obj
                                self.read_write_inputs[cpd.name] = 'w'
                                self.catalogPropertyDetail.append(cpd) 
                                del cpd                 
                    return  
                else:                 
                    for obj in propertyDetail:
                        cpd=CatalogPropertyDetail()
                        cpd = obj
                        self.read_write_inputs[cpd.name] = 'w'
                        self.catalogPropertyDetail.append(cpd) 
                        del cpd     
                    return 
        
        if self.catalogproperty_name == 'p':

                
            if  ( self.crystalsystem_name == 'tc'  or self.crystalsystem_name == 'o'  or self.crystalsystem_name == 'te'  or self.crystalsystem_name == 'c' ) or (self.crystalsystem_name == 'tg' and self.puntualgroupselected_name != '3m' ) or (self.crystalsystem_name == 'h' and self.puntualgroupselected_name != '-6m2' ):

                print 'Property:'  + self.objProperty.name 
                print 'crystalsystem_id=' + str(self.objCatalogCrystalSystemSelected.pk)
                print 'type_id='  +  str(self.objTypeSelected.pk)                 
                print  'catalogpointgroup_id=' +  str(self.objCatalogPointGroupSelected.pk)
                propertyDetail = CatalogPropertyDetail.objects.filter(type=self.objTypeSelected,crystalsystem=self.objCatalogCrystalSystemSelected,catalogpointgroup=self.objCatalogPointGroupSelected).order_by('name')
                
                if not propertyDetail:  
                    objPuntualGroupGroups=PuntualGroupGroups.objects.filter(catalogpointgroup=self.objCatalogPointGroupSelected)          
                    for obj in objPuntualGroupGroups:
                        pgg=  PuntualGroupGroups()
                        pgg = obj   
                        propertyDetail = CatalogPropertyDetail.objects.filter(type=self.objTypeSelected,crystalsystem=self.objCatalogCrystalSystemSelected,puntualgroupnames=pgg.puntualgroupnames).order_by('name')
                        if  propertyDetail:
                            for obj in propertyDetail:
                                cpd=CatalogPropertyDetail()
                                cpd = obj
                                self.read_write_inputs[cpd.name] = 'w'
                                print self.read_write_inputs[cpd.name]
                                self.catalogPropertyDetail.append(cpd) 
                                del cpd                 
                    return  
                else:                 
                    for obj in propertyDetail:
                        cpd=CatalogPropertyDetail()
                        cpd = obj
                        self.read_write_inputs[cpd.name] = 'w'
                        print cpd.name + "="+self.read_write_inputs[cpd.name]
                        self.catalogPropertyDetail.append(cpd) 
                        del cpd     
                    return 
                
            if  ( self.crystalsystem_name == 'm' ) or (self.crystalsystem_name == 'tg' and self.puntualgroupselected_name == '3m' ) or (self.crystalsystem_name == 'h' and self.puntualgroupselected_name == '-6m2' ):
                '''print 'Property:'  + self.objProperty.name 
                print 'crystalsystem_id=' + str(self.objCatalogCrystalSystemSelected.pk)
                print 'type_id='  +  str(self.objTypeSelected.pk)
                print  'catalogaxis_id=' + str( self.objAxisSelected.pk)
                print  'catalogpointgroup_id=' +  str(self.objCatalogPointGroupSelected.pk)'''
                
                propertyDetail = CatalogPropertyDetail.objects.filter(type=self.objTypeSelected, crystalsystem=self.objCatalogCrystalSystemSelected, catalogaxis=self.objAxisSelected, catalogpointgroup=self.objCatalogPointGroupSelected).order_by('name')
                for obj in propertyDetail: 
                    cpd=CatalogPropertyDetail()
                    cpd=obj  
                    self.read_write_inputs[cpd.name] = 'w'           
                    self.catalogPropertyDetail.append(cpd)       
                    del cpd       
                return    
        
        
    #end setCatalogPropertyDetail    
        
                
                
    def setPointGroup(self):  
        propertyDetail = CatalogPropertyDetail.objects.filter(type=self.objTypeSelected,crystalsystem=self.objCatalogCrystalSystemSelected).values('catalogpointgroup').annotate(total=Count('catalogpointgroup'))
       
        for d in propertyDetail:  
            if d['catalogpointgroup'] != 0:       
                #print d['catalogpointgroup']  
                objCatalogPointGroup=CatalogPointGroup.objects.filter(id__exact=d['catalogpointgroup'])         
                for obj in  objCatalogPointGroup:
                    cpg=CatalogPointGroup()
                    cpg=obj        
                    
                    if self.puntualgroupselected_name == '':
                        self.puntualgroupselected_name=cpg.name
               
                    self.puntualGroupList.append(cpg)
       
       
        propertyDetail = CatalogPropertyDetail.objects.filter(type=self.objTypeSelected,crystalsystem=self.objCatalogCrystalSystemSelected).values('puntualgroupnames').annotate(total=Count('puntualgroupnames'))
         
        for d in propertyDetail:
            if d['puntualgroupnames'] != 0:   
                #print d['puntualgroupnames']              
                objPuntualgroupnames=PuntualGroupNames.objects.filter(id__exact=d['puntualgroupnames']) 
                objPuntualGroupGroups = PuntualGroupGroups.objects.filter(puntualgroupnames=objPuntualgroupnames)    
                for obj in objPuntualGroupGroups:
                    pgg=PuntualGroupGroups()
                    pgg=obj
                    #print pgg.catalogpointgroup.name
                    if self.puntualgroupselected_name == '':
                        self.puntualgroupselected_name=pgg.catalogpointgroup.name
             
                    self.puntualGroupList.append(pgg.catalogpointgroup)
                    
    def setAxis(self):
        propertyDetail = CatalogPropertyDetail.objects.filter(type=self.objTypeSelected,crystalsystem=self.objCatalogCrystalSystemSelected).values('catalogaxis').annotate(total=Count('catalogaxis'))
         
        for d in propertyDetail:  
            if d['catalogaxis'] != 0:       
                #print d['catalogaxis']  
                objCatalogAxis=CatalogAxis.objects.filter(id=d['catalogaxis'] )
                for obj in objCatalogAxis:
                    ca=CatalogAxis()
                    ca=obj
                    #print ca.name
                    self.axisList.append(ca)
                        
        
    def preparedataforjQuery(self,t):
        if t == "s" or t == "c":
            x = 0
            row = []
            for r in self.s:
                x=x+ 1
                y=1   
                for c in r: 
                    col=t+str(x) + str(y)
                    if col in self.read_write_inputs:
                        pass
                    else: 
                        self.read_write_inputs[col] = "r"  
                    row.append(col)
                    y= y + 1 
                self.catalogPropertyDetailReadOnly.append(row)     
                row = []  
        elif t == "d":
            x = 0
            row = []
            for r in self.d:
                x=x+ 1
                y=1   
                for c in r: 
                    col=t+str(x) + str(y)
                    if col in self.read_write_inputs:
                        pass
                    else: 
                        self.read_write_inputs[col] = "r"  
                    row.append(col)
                    y= y + 1 
                self.catalogPropertyDetailReadOnly.append(row)     
                row = []  
        


                    
    def contains(self,listObject, obj):
        result = False
        for x in listObject:
            #print x.catalogproperty_name + " == " + obj.catalogproperty_name
            if x == obj :         
                result = True
                break       

        return result
            

    def releaseRequet(self):
        self.__request =None
        
        
    def __del__(self):
        print "delete object"