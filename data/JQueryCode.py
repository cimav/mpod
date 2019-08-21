'''
Created on Nov 25, 2014

@author: Jorge Torres
'''

import os
import re
import string
from data.JScriptUtil import *
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models.query import QuerySet

from data.models import  *

class JQueryRules(object):
    def __init__(self):
        self.sourceList = []
        self.targetList = []
        self.jsutils = JSUtils()
        
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
                                   
                                   function inputpop(object)
                                   {
                                         try {
                                                 obj = $(object);
                                                 //val = $(object).val();
                                          }
                                          catch(error) {
                                              //obj = django.jQuery(object).val();
                                              obj = $(object);
                                          }
                                          
                                         if(obj.val().length > 3)
                                        {
                                            obj.attr('data-content', obj.val());          
                                            try{
                                               obj.popover('show');
                                               }
                                            catch(error) {
                                            console.log('Function not suported');
                                            }
                                            
                                        }
                                        else
                                        {
                                           try{
                                           obj.popover('hide');
                                           }
                                           catch(error) {
                                           console.log('Function not suported');
                                           }
                                           
                                           obj.attr('data-content', '');    
                                        }
                                 }
                                 
                                 function inputpopclear(obj)
                                 {
                                   
                                    obj.popover('hide');
                                    obj.attr('data-content', '');    
                                 }
                                 
                                 
                                 function tolerance(object)
                                 {
                                    val = ''
                                    var fullval= ''
                                      
                                    
                                     if($(object).val().indexOf("(") != -1)
                                     {
                                         if($(object).val().indexOf(")") != -1)
                                         {
                                             fullval = $(object).val().substring(0, $(object).val().indexOf(")") + 1);
                                             console.log( fullval);
                                         }
                                         else
                                         {
                                            fullval = $(object).val().substring(0, $(object).val().length);
                                        }
                                         
                                        val = $(object).val().substring(0, $(object).val().indexOf("("));
                                          
                                         $(object).val(val)     
  
                                     }
                                     
                                     return fullval;
                                 }
                                 
                                 function validateValue(object) {
                                 var str = ''
                                  
                                 try {
                                  
                                      str = $(object).val();
                                  }
                                  catch(error) {
                                      str = django.jQuery(object).val();
                                  }
                                  
                                  
                                  
                                  var expreg =         /^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)$|^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)\([-+]?\d+(\.\d+)?\)$|^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)\([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)\)$|^[-+]?\d+(\.\d+)?$|^[-+]?\d+(\.\d+)?\([-+]?\d+(\.\d+)?\)$|^[-+]?\d+(\.\d+)?\([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)\)$|^\?$/;
                                  var val = '';
                                
                                  var result = str.match(expreg);
                                  if(result != null)
                                  {
                                    val=result[0].replace(/ *\([^)]*\) */g, "");
                                    return  val;
                                  }
                                  else
                                  {
                                      return val;
                                  }
                                }
                                
                                
                                function validateField(object) {
                                //alert(field );
                                var fullval = django.jQuery(object).val();
                                var thisvalue  = validateValue(object);
                                console.log('#lbl_' +django.jQuery(object).attr('name'));
                                
                                
                                
                                if(thisvalue != '' )    
                                  {
                                    django.jQuery(object).val(fullval);
                                    django.jQuery('#lbl_' + django.jQuery(object).attr('name')).css("color", "black");
                                   }
                                else
                                  {
                                    //django.jQuery(object).val('');
                                    django.jQuery('#lbl_' + django.jQuery(object).attr('name')).css("color", "red");
                                 }  
                             
                                 
                            }
     
                            """
        
        
    def generateCode(self,symmetry,propertyDetail,read_write_inputs,scij,initialize):
        self.jquery= self.jquery +  """
                                                        // inicio de codigo jQuery
                                                        $('#divwarningpropertyvalues').hide();
                                                        $(document).ready(
                                                            function() 
                                                            {
                                                         """
        for i, obj in enumerate(propertyDetail):    
            keyNotationCatalogPropertyDetail= self.jsutils.getKeyNotation(obj)
            if isinstance(keyNotationCatalogPropertyDetail, QuerySet):
                
                source_target_Dic = {}
                size = len(keyNotationCatalogPropertyDetail) -1
                for x,knotationpropertydetail in enumerate(keyNotationCatalogPropertyDetail):

                    sourceList = [x.strip() for x in knotationpropertydetail.source.split(',')]
                    if len(sourceList) > 1:
                        targetList = [x.strip() for x in knotationpropertydetail.target.split(',')]
                        source_target_Dic[ tuple(sourceList)]=targetList
                    elif len(sourceList) == 1:
                        targetList = [x.strip() for x in knotationpropertydetail.target.split(',')]
                        source_target_Dic[obj.name]=targetList
 
                if source_target_Dic:
                    self.jquery= self.jquery +  self.jsutils.jsrules( obj.name,scij,source_target_Dic,False,symmetry)
 
            else:
                targetList = [x.strip() for x in keyNotationCatalogPropertyDetail.target.split(',')]
                source_target_Dic = {}
                source_target_Dic[obj.name]=targetList
                if source_target_Dic:
                    if keyNotationCatalogPropertyDetail.keynotation.id ==4 or keyNotationCatalogPropertyDetail.keynotation.id ==6 or keyNotationCatalogPropertyDetail.keynotation.id ==5 or keyNotationCatalogPropertyDetail.keynotation.id ==10:
                        
                        self.jquery= self.jquery + self.jsutils.jsrules( obj.name,scij,source_target_Dic,True,symmetry)
                    else:
                        self.jquery= self.jquery +  self.jsutils.jsrules( obj.name,scij,source_target_Dic, False,symmetry)

        self.listofemptyInputs = self.jsutils.simetricinputs

        for key in sorted(read_write_inputs.keys()):
            if  read_write_inputs[key] == 'r':
                if  self.contains(self.listofemptyInputs,key):
                    if  initialize== True:
                        self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val('');" +"\n"    
                    
                    self.jquery=self.jquery+ " $('#"+ key +"').css({'background-color': '#e8f7fc'});" +"\n"   
                     
                else:
                    if  initialize== True:
                        self.jquery=self.jquery+ " $('#"+ key +"').attr('readonly', true).val(0);" +"\n"
                    
                    self.jquery=self.jquery+ " $('#"+ key +"').css({'background-color': '#eeeeee'});" +"\n"   
                    
                   

        self.jquery=  self.jquery+ "\n"  + "\n"  +  " });"
        
        
        
 
    def contains(self,listObject, obj):
        result = False
        for x in listObject:
            #print x.catalogproperty_name + " == " + obj.catalogproperty_name
            if x == obj :         
                result = True
                break       

        return result   
    
        
        
 