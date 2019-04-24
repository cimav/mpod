'''
Created on Nov 25, 2014

@author: admin
'''

import os
import re
import string
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from data.models import  *

class JSUtils (object):
    def __init__(self):
        self.__jscode = ''
        self.htmlcode = ''
        self.simetricinputs = []
        self.simetricandnonzeroinputs = []
        self.counter = 0
        
        """self.__htmlcode += "<table>"
        self.__htmlcode += "<thead>"
        self.__htmlcode += "<tr>"
        self.__htmlcode += "<th scope='col'>
        self.__htmlcode += "<div class='text'>
        self.__htmlcode += "<span>Description</span>
        self.__htmlcode += "</div>
        self.__htmlcode += "<div class='clear'></div>
        self.__htmlcode += "</th>
        self.__htmlcode += "</tr>"
        self.__htmlcode += "</thead>"
        self.__htmlcode += "<tbody>"
        """
        
        
    def getrules(self, item,scij,source_target,setsymmetry):   
        keynotation = source_target['keynotation']
        del source_target['keynotation']
        size = 0
        classTR = ''
        if (self.counter % 2) == 0:
            classTR = 'row1'
        else:
            classTR = 'row2'
            
        
        self.counter += 1
        self.htmlcode += "<tr class='"+ classTR+ "'>"  
        self.htmlcode += "<td>"
        self.htmlcode += item
        self.htmlcode += "</td>"
        for key, value in source_target.items():
            if isinstance(key, tuple ):
                size = len(value) - 1     
                self.htmlcode += "<td>"
                for i,st in enumerate(value):
                    
                    if i < size:
                        self.htmlcode +=   st+ ', ' 
                    else:
                        self.htmlcode +=   st
              
                self.htmlcode += "</td>"
                    
            elif isinstance(key, basestring):
                targetList = source_target[item]
                if targetList:     
                    size = len(targetList) - 1             
                    self.htmlcode += "<td>"             
                    for i, target in  enumerate(targetList):      
                        if i < size:
                            self.htmlcode +=   target+ ', ' 
                        else:
                            self.htmlcode +=   target
                  
                    self.htmlcode += "</td>"
        
        self.htmlcode += "<td>"
        self.htmlcode += keynotation.description
        self.htmlcode += "</td>"
                        
        self.htmlcode += "</tr>"
 
 
    def getsimetricandnonzero(self, item,scij,source_target,setsymmetry):   
        
        targetList = source_target[item]

        simetricitem=self.getsimetric(item,scij )                                       
        if self.issimetric(item,simetricitem) and setsymmetry == True: 
            if simetricitem not in self.simetricandnonzeroinputs:
                self.simetricandnonzeroinputs.append(simetricitem )
 
 
            if targetList:                               
                for i, target in  enumerate(targetList):
                    simetrictarget = self.getsimetric(target,scij ) 
                    if item != target:
                        if target not in self.simetricandnonzeroinputs:
                            self.simetricandnonzeroinputs.append(target )
 
                        
                    if self.issimetric(target,simetrictarget): 
                        if simetricitem != simetrictarget:
                            if simetrictarget not in self.simetricandnonzeroinputs:
                                self.simetricandnonzeroinputs.append(simetrictarget )
 
           
            for key, value in source_target.items():
                if isinstance(key, tuple ):
                    for x,st in enumerate(value):
                        if st not in self.simetricandnonzeroinputs:
                            self.simetricandnonzeroinputs.append(st)
 
                            
                if isinstance(value, KeyNotation ):
                    print value.description
 

        
        else:
            if targetList:     
 
                size = len(targetList) - 1                                
                for i, target in  enumerate(targetList):
                    simetrictarget = self.getsimetric(target,scij ) 

                    if item != target:
                        if target not in self.simetricandnonzeroinputs:
                            self.simetricandnonzeroinputs.append(target )

                    if self.issimetric(target,simetrictarget ) and setsymmetry == True: 
                        if simetricitem != simetrictarget:
                            if simetrictarget not in self.simetricandnonzeroinputs:
                                self.simetricandnonzeroinputs.append(simetrictarget )
 
            
            for key, value in source_target.items():
                if isinstance(key, tuple ):
                    size = len(value) - 1        
                    for x,st in enumerate(value):
                        if st not in self.simetricandnonzeroinputs:
                            self.simetricandnonzeroinputs.append(st)
 
                #if isinstance(value, KeyNotation ):
                    #print value.description
   
          
 
 

            
    def getKeyNotation(self,catalogpropertydetail):
        keyNotationCatalogPropertyDetail = None
        try: 
            keyNotationCatalogPropertyDetail = KeyNotationCatalogPropertyDetail.objects.get(catalogpropertydetail = catalogpropertydetail)
        except (ObjectDoesNotExist, MultipleObjectsReturned) as error:      
            print "message in the function get_props for debug purposes. Message({0}): {1}".format(99, error.message)   

        if keyNotationCatalogPropertyDetail == None:
            try: 
                keyNotationCatalogPropertyDetail = KeyNotationCatalogPropertyDetail.objects.filter(catalogpropertydetail = catalogpropertydetail)
            except ObjectDoesNotExist as error:      
                print "message in the function get_props for debug purposes. Message({0}): {1}".format(99, error.message)   

        return keyNotationCatalogPropertyDetail
    
    def getKeyNotationCatalogPropertyDetail(self,catalogpropertydetail,keynotation):
        keyNotationCatalogPropertyDetail = None
        try: 
            keyNotationCatalogPropertyDetail = KeyNotationCatalogPropertyDetail.objects.get(keynotation=keynotation, catalogpropertydetail = catalogpropertydetail)
            #keyNotationCatalogPropertyDetail.keynotation=keynotation
        except ObjectDoesNotExist as error:      
            print "message in the function get_props for debug purposes. Message({0}): {1}".format(99, error.message)   
            print "Not exist"
        
        
        if keyNotationCatalogPropertyDetail == None:
            keyNotationCatalogPropertyDetail = KeyNotationCatalogPropertyDetail()
            keyNotationCatalogPropertyDetail.keynotation=keynotation
            keyNotationCatalogPropertyDetail.catalogpropertydetail=catalogpropertydetail
            
        return keyNotationCatalogPropertyDetail
        
        
    def jsrules(self, item,scij,source_target,setopositesing,setsymmetry):                            
        self.__jscode = ''
 
        self.__jscode=   self.__jscode + """$('#""" +item+ """').keyup(function (){\n"""

        #self.__jscode=   self.__jscode + """    var fullval = tolerance(this);\n"""
        #self.__jscode=   self.__jscode + """    if(Number($(this).val()).toPrecision() != 'NaN') {\n"""                                                
        #self.__jscode=   self.__jscode +     """    var value;\n"""
        #self.__jscode=   self.__jscode + """        if ( isScientificNotation($(this).val()) == 1 )\n""" 
        #self.__jscode=   self.__jscode + """        {\n""" 
        #self.__jscode=   self.__jscode + """            value = Number.parseFloat($(this).val()).toExponential();\n""" 
        #self.__jscode=   self.__jscode + """            $(this).val(value );  \n""" 
        #self.__jscode=   self.__jscode + """            alert(value );  \n""" 
        #self.__jscode=   self.__jscode + """        }\n""" 
        
        self.__jscode=   self.__jscode + """    var fullval = $(this).val();\n"""
        self.__jscode=   self.__jscode + """    var thisvalue = validateValue($(this)); \n""" 
        self.__jscode=   self.__jscode + """    if(thisvalue != '' )"""  
        self.__jscode=   self.__jscode + """    {\n""" 
        #self.__jscode=   self.__jscode + """        alert(validatedvar );  \n""" 
        #self.__jscode=   self.__jscode + """    }\n""" 
  
            
            
        targetList = source_target[item]
        simetricitem=self.getsimetric(item,scij )                                       
        if self.issimetric(item,simetricitem) and setsymmetry == True: 
            self.simetricinputs.append(simetricitem )
            self.__jscode=   self.__jscode +   """        $('#""" +simetricitem+"""').val(thisvalue);\n"""
            
            if setopositesing:
                self.__jscode=   self.__jscode +     """        var value;\n"""
                self.__jscode=   self.__jscode +     """        v = -thisvalue;\n"""   
                self.__jscode=   self.__jscode +     """        if ( isScientificNotation(thisvalue) == 1 )\n"""  
                self.__jscode=   self.__jscode +     """            value = Number.parseFloat(v).toExponential();\n"""  
                self.__jscode=   self.__jscode +     """        else\n"""                                                                           
                self.__jscode=   self.__jscode +     """            value = v;\n\n""" ; 
                
              
 
             
            if targetList:                               
                for i, target in  enumerate(targetList):
                    simetrictarget = self.getsimetric(target,scij ) 
                    if item != target:
                        self.simetricinputs.append(target )
                        
                    if self.issimetric(target,simetrictarget): 
                        if simetricitem != simetrictarget:
                            self.simetricinputs.append(simetrictarget )
                            if i== 0: #componet numerically equal but opposite sing      
                                if setopositesing:
                                    self.__jscode=   self.__jscode +   """        $('#""" + target +"""').val(value);\n"""  
                                    self.__jscode=   self.__jscode +   """        $('#""" +simetrictarget+"""').val(value );\n"""
                                else:                    
                                    self.__jscode=   self.__jscode +   """        $('#""" + target +"""').val(thisvalue);\n"""  
                                    self.__jscode=   self.__jscode +   """        $('#""" +simetrictarget+"""').val(thisvalue);\n"""

                                    
                            if i == 1: 
                                if 'c' in scij[0]: 
                                    self.__jscode=   self.__jscode +     """        v = thisvalue;\n"""   
                                    self.__jscode=   self.__jscode +     """        if ( isScientificNotation(thisvalue) == 1 )\n"""  
                                    self.__jscode=   self.__jscode +     """            value = Number.parseFloat(v).toExponential();\n"""  
                                    self.__jscode=   self.__jscode +     """        else\n"""                                                                           
                                    self.__jscode=   self.__jscode +     """            value = v;\n\n""" ; 
                          
                                    self.__jscode=   self.__jscode +   """        $('#""" + target +"""').val(value);\n"""                                      
                                    self.__jscode=   self.__jscode +   """        $('#""" +simetrictarget+"""').val(value);\n"""


                                elif 's' in scij[0]:  #twice the numerical equal         
                                    self.__jscode=   self.__jscode +     """        v = thisvalue;\n"""   
                                    self.__jscode=   self.__jscode +     """        if ( isScientificNotation(thisvalue) == 1)\n"""  
                                    self.__jscode=   self.__jscode +     """            value = Number.parseFloat(v).toExponential();\n"""  
                                    self.__jscode=   self.__jscode +     """        else\n"""                                                                           
                                    self.__jscode=   self.__jscode +     """            value = v;\n\n""" ; 
                                                             
                     
                                    self.__jscode=   self.__jscode +     """        $('#""" + target +"""').val(2 * (value) );\n"""                                    
                                    self.__jscode=   self.__jscode +     """        $('#""" +simetrictarget+"""').val(2 * (value) );\n"""

                            
                        else:
                            if item != target:                      
                                self.__jscode=   self.__jscode +        """        $('#""" + target +"""').val(thisvalue );  \n"""  
                                self.__jscode=   self.__jscode +        """        $('#""" + simetrictarget +"""').val(thisvalue );\n"""

                            

                                    
                                    
                                    
                    else:
                        if setopositesing:                  
                            self.__jscode=   self.__jscode +     """        $('#""" + target +"""').val(value);\n"""  

                                
                        else:
                            if item != target:
                                #self.__jscode=   self.__jscode +     """        $('#""" + target +"""').val($(this).val()  );\n"""  
                                self.__jscode=   self.__jscode +     """        $('#""" + target +"""').val(thisvalue);\n"""  
          
                                
                            
            for key, value in source_target.items():
                if isinstance(key, tuple ):
                     
                    self.__jscode=   self.__jscode +     """        if(Number(thisvalue).toPrecision() != 'NaN')\n"""   
                    self.__jscode=   self.__jscode +     """        { \n """     
  
                    
                    self.__jscode=   self.__jscode +     """          var key0;\n"""
                    self.__jscode=   self.__jscode +     """          var key1;\n"""
                    self.__jscode=   self.__jscode +     """          if($('#""" + key[0] + """').val().indexOf("(") != -1)\n"""
                    self.__jscode=   self.__jscode +     """          {\n"""
                    self.__jscode=   self.__jscode +     """            key0=$('#""" + key[0] + """').val() \n"""    
                    self.__jscode=   self.__jscode +     """            tolerance('#""" + key[0] + """')\n"""     
                    self.__jscode=   self.__jscode +     """           } \n"""
                    
                    self.__jscode=   self.__jscode +     """          if($('#""" + key[1] + """').val().indexOf("(") != -1)\n"""
                    self.__jscode=   self.__jscode +     """          {\n"""
                    self.__jscode=   self.__jscode +     """            key1=$('#""" + key[1] + """').val() \n"""    
                    self.__jscode=   self.__jscode +     """            tolerance('#""" + key[1] + """')\n"""     
                    self.__jscode=   self.__jscode +     """          }\n"""
                    
                    
                    if 'c' in scij[0]:      
                        self.__jscode=   self.__jscode +     """          v = 0.5 *($('#""" + key[0] + """').val() - $('#""" + key[1] + """').val() );\n"""
                    elif 's' in scij[0]:    
                        self.__jscode=   self.__jscode +     """          v = 2 *($('#""" + key[0] + """').val()- $('#""" + key[1] + """').val());\n"""
                    
                    self.__jscode=   self.__jscode +     """          if ( isScientificNotation(thisvalue) == 1 )\n"""
                    self.__jscode=   self.__jscode +     """              value = Number.parseFloat(v).toExponential(); \n"""
                    self.__jscode=   self.__jscode +     """          else \n"""
                    self.__jscode=   self.__jscode +     """              value = v; \n \n"""

                    self.__jscode=   self.__jscode +     """          if(key0 != undefined)\n"""
                    self.__jscode=   self.__jscode +     """             $('#""" + key[0] + """').val(key0);\n\n"""
                    
                    
                    self.__jscode=   self.__jscode +     """          if(key1 != undefined)\n"""
                    self.__jscode=   self.__jscode +     """             $('#""" + key[1] + """').val(key1);\n\n"""
                    
  
                    for x,st in enumerate(value):
                        self.__jscode=   self.__jscode + """          $('#"""+ st + """').val(value);\n""" 
                            
                    self.__jscode=   self.__jscode +     """      }\n"""        
                    self.__jscode=   self.__jscode +  """        else\n"""
                    self.__jscode=   self.__jscode +  """        { \n"""
                    for x,st in enumerate(value):
                        self.__jscode=   self.__jscode + """            $('#"""+ st + """').val('' );\n"""
                    self.__jscode=   self.__jscode +  """        }\n"""
                        
                                                   
            
                                            
            self.__jscode=   self.__jscode +  """   }\n"""
            self.__jscode=   self.__jscode +  """else\n"""
            self.__jscode=   self.__jscode +  """{ \n"""
                                                                      
                                                                                    
                                                                            
            self.__jscode=   self.__jscode +  """        $('#""" +simetricitem+"""').val('');\n"""
            
            if targetList:
                for i, target in  enumerate(targetList):
                    simetrictarget = self.getsimetric(target,scij ) 
                    if self.issimetric(target,simetrictarget): 
                        if setopositesing:
                            self.__jscode=   self.__jscode +     """        $('#""" + target +"""').val('');\n"""  
                            self.__jscode=   self.__jscode +     """        $('#""" +simetrictarget+"""').val('');\n """
                            
                        else:
                            if item != target:
                                self.__jscode=   self.__jscode +     """        $('#""" + target +"""').val('' );\n"""  
                                self.__jscode=   self.__jscode +     """        $('#""" + simetrictarget +"""').val('' );\n"""
              
                    else:
                        if setopositesing:
                            self.__jscode=   self.__jscode +     """        $('#""" + target +"""').val('' );\n"""  
                        else:
                            self.__jscode=   self.__jscode +     """        $('#""" + target +"""').val('' );\n"""  
                            
                            
            for key, value in source_target.items():
                if isinstance(key, tuple ):
                    for x,st in enumerate(value):
                        self.__jscode=   self.__jscode + """          $('#"""+ st + """').val('' );\n"""       
       
                                                                                    
                                                                                    
                                                                                    
             
                                                
        
        else:
            if targetList:                               
                for i, target in  enumerate(targetList):
                    simetrictarget = self.getsimetric(target,scij ) 
                    if item != target:
                        self.simetricinputs.append(target )
                  
                    if self.issimetric(target,simetrictarget ) and setsymmetry == True: 
                        if simetricitem != simetrictarget:
                            self.simetricinputs.append(simetrictarget )
                     
                        if setopositesing:
                            self.__jscode=   self.__jscode +     """      $('#""" + target +"""').val(-thisvalue  );  \n"""  
                            self.__jscode=   self.__jscode +     """      $('#""" +simetrictarget+"""').val(-thisvalue );  \n """
                            
                        else:
                            if item != target:
                                self.__jscode=   self.__jscode +     """      $('#""" + target +"""').val(thisvalue );  \n"""  
                                self.__jscode=   self.__jscode +     """      $('#""" + simetrictarget +"""').val(thisvalue );  \n"""
                            
                            
                            for key, value in source_target.items():
                                if isinstance(key, tuple ):
                                    pass
                    else:
                        if setopositesing:
                            if i == 0: 
                                self.__jscode=   self.__jscode +     """      $('#""" + target +"""').val(-thisvalue  );  \n"""  
                                
                            if i == 1: 
                                if scij[0] in ['d','e','g','h','k']: 
                                    self.__jscode=   self.__jscode +     """      $('#""" + target +"""').val(-2 * thisvalue);  \n"""  
                        else:
                            if item != target:
                                self.__jscode=   self.__jscode +     """      $('#""" + target +"""').val(thisvalue );  \n"""  
                                
            
            
            for key, value in source_target.items():
                if isinstance(key, tuple ):
                    self.__jscode=   self.__jscode +     """        if(Number(thisvalue).toPrecision() != 'NaN') \n"""   
                    self.__jscode=   self.__jscode +     """        { \n """     
                    
                    
                    self.__jscode=   self.__jscode +     """          var key0;\n"""
                    self.__jscode=   self.__jscode +     """          var key1;\n"""
                    self.__jscode=   self.__jscode +     """          if($('#""" + key[0] + """').val().indexOf("(") != -1)\n"""
                    self.__jscode=   self.__jscode +     """          {\n"""
                    self.__jscode=   self.__jscode +     """            key0=$('#""" + key[0] + """').val() \n"""    
                    self.__jscode=   self.__jscode +     """            tolerance('#""" + key[0] + """')\n"""     
                    self.__jscode=   self.__jscode +     """           } \n"""
                    
                    self.__jscode=   self.__jscode +     """          if($('#""" + key[1] + """').val().indexOf("(") != -1)\n"""
                    self.__jscode=   self.__jscode +     """          {\n"""
                    self.__jscode=   self.__jscode +     """            key1=$('#""" + key[1] + """').val() \n"""    
                    self.__jscode=   self.__jscode +     """            tolerance('#""" + key[1] + """')\n"""     
                    self.__jscode=   self.__jscode +     """          }\n"""
                    
                    
                    if 'c' in scij[0]:      
                        self.__jscode=   self.__jscode +     """          v = 0.5 *($('#""" + key[0] + """').val() - $('#""" + key[1] + """').val() );\n"""
                    elif 's' in scij[0]:    
                        self.__jscode=   self.__jscode +     """          v = 2 *($('#""" + key[0] + """').val()- $('#""" + key[1] + """').val());\n"""
                    
                    self.__jscode=   self.__jscode +     """          if ( isScientificNotation(thisvalue) == 1 )\n"""
                    self.__jscode=   self.__jscode +     """              value = Number.parseFloat(v).toExponential(); \n"""
                    self.__jscode=   self.__jscode +     """          else \n"""
                    self.__jscode=   self.__jscode +     """              value = v; \n \n"""

                    self.__jscode=   self.__jscode +     """          if(key0 != undefined)\n"""
                    self.__jscode=   self.__jscode +     """             $('#""" + key[0] + """').val(key0);\n\n"""
                    
                    
                    self.__jscode=   self.__jscode +     """          if(key1 != undefined)\n"""
                    self.__jscode=   self.__jscode +     """             $('#""" + key[1] + """').val(key1);\n\n"""
                    
  
                    for x,st in enumerate(value):
                        self.__jscode=   self.__jscode + """          $('#"""+ st + """').val(value);\n""" 
                            
                    self.__jscode=   self.__jscode +     """      }\n"""        
                    self.__jscode=   self.__jscode +  """        else\n"""
                    self.__jscode=   self.__jscode +  """        { \n"""
                    for x,st in enumerate(value):
                        self.__jscode=   self.__jscode + """            $('#"""+ st + """').val('' );\n"""
                        
                    self.__jscode=   self.__jscode +  """        }\n"""
                            
        
                                                                    
                                                                    
            self.__jscode=   self.__jscode +  """   }\n"""  
            self.__jscode=   self.__jscode +  """else\n"""  
            self.__jscode=   self.__jscode +  """  {\n"""  
                                                                                  
            if setsymmetry == True:                                                                
                self.__jscode=   self.__jscode +  """      $('#""" +simetricitem+"""').val('');\n"""
            else:
                self.__jscode=   self.__jscode +  """      $('#""" +item+"""').val('');\n"""  
                
                          
            if targetList:
                for i, target in  enumerate(targetList):
                    simetrictarget = self.getsimetric(target,scij ) 
                    if self.issimetric(target,simetrictarget) and setsymmetry == True: 
                        if setopositesing:
                            self.__jscode=   self.__jscode +     """      $('#""" + target +"""').val('');  \n"""  
                            self.__jscode=   self.__jscode +     """      $('#""" +simetrictarget+"""').val('');  \n """
                            
                        else:
                            if item != target:
                                self.__jscode=   self.__jscode +     """      $('#""" + target +"""').val('' );  \n"""  
                                self.__jscode=   self.__jscode +     """      $('#""" + simetrictarget +"""').val('' );  \n"""
                           
                            
                             
                    else:
                        if setopositesing:
                            self.__jscode=   self.__jscode +     """      $('#""" + target +"""').val('' );  \n"""  
                        else:
                            if item != target:
                                self.__jscode=   self.__jscode +     """      $('#""" + target +"""').val('' );  \n""" 
                            
            for key, value in source_target.items():
                if isinstance(key, tuple ):
                    for x,st in enumerate(value):
                        self.__jscode=   self.__jscode + """      $('#"""+ st + """').val('' );\n"""                
                            
                            
                            
       

        self.__jscode=   self.__jscode +"""}  \n"""
        
                    
    
        
                                              
        self.__jscode=   self.__jscode +"""if(fullval != '') \n"""
        self.__jscode=   self.__jscode +"""{ \n"""
        self.__jscode=   self.__jscode +"""    $(this).val(fullval)\n""" 
        self.__jscode=   self.__jscode +"""}\n"""
        self.__jscode=   self.__jscode +"""inputpop($(this));\n"""
        self.__jscode=   self.__jscode +"""});\n"""
        
        
        
                                          
        self.__jscode= self.__jscode + """ 
                                                                    $('#""" +item+ """').focusout(function (){
                                                                   
                                                                    var fullval = $(this).val();
                                                                    var thisvalue = validateValue($(this)); 
        
                                                                    if(thisvalue != ''){
                                                                        //inputpop($(this));
                                                                    }else
                                                                    {
                                                                       $(this).val('');
                                                                       inputpopclear($(this));
                                                                    }
                                                                    
                                                                    if(fullval != '')
                                                                    {
                                                                         $(this).val(fullval) 
                                                                    }
                                                                    inputpop($(this));
                                                                 });  
                                                                                                                            
                                                """                         
                             
         

        return self.__jscode
    
    
    def getsimetric(self,item,scij):
        item1= item.replace(scij[0], '')
        item2=item1.replace(scij[1], '')
        index = list(item2)

        source= (scij[0]+ str(index[1]) + str(index[0]) +scij[1])
        
        return source
    
    def issimetric(self,item,target):
        if target == item:
            return False
        else:
            return True
        
        
 