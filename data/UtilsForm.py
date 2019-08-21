'''
Created on 06/07/2019

@author: Jorge Torres
'''
from django import forms  
import os
import sys
from django.contrib.admin.widgets import AdminTextInputWidget
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode


class JQueryCustomFieldWidget(AdminTextInputWidget):
    def render(self, name, value, attrs=None):
        jquery = super(JQueryCustomFieldWidget, self).render(name, value, attrs)
        if value:
            pass
        else:
            value = ""    
 
 
        jq =  force_unicode( jquery) 
        jq =   force_unicode( """<div class='divjscode' id='"""+attrs['id'] +"""'>"""+ value + """</div>""") 
        return mark_safe(jq)  
    
 
    


class HTMLCustomFieldWidget(AdminTextInputWidget):
    def render(self, name, value, attrs=None):
        html = super(HTMLCustomFieldWidget, self).render(name, value, attrs)
        if value:
            pass
        else:
            value = ""    
            
        #html =   force_unicode( """    <div class='results' id='"""+attrs['id'] +"""'>"""+ value + """</div>""") 
        html =   force_unicode( """ <div class='results' id='"""+attrs['id'] +"""'>"""+ value + """</div>""") 
        return mark_safe(html)  
    
class ParrafReadonlyFieldWidget(AdminTextInputWidget):
    def render(self, name, value, attrs=None):
        html = super(ParrafReadonlyFieldWidget, self).render(name, value, attrs)
        if value:
            pass
        else:
            value = ""    
            
        #html =   force_unicode( """    <div class='results' id='"""+attrs['id'] +"""'>"""+ value + """</div>""") 
        html =   force_unicode( """ <div class='results'  id='"""+attrs['id'] +"""'>"""+ value + """</div>""") 
        return mark_safe(html)  

class CustomForm(forms.Form):
    '''
    classdocs
    '''


    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        self.fieldsets =None
        self.indexhd = 0
        self.fieldsetIndex = {}
        self.currentdata = None
        #self.readonly_fields = {}
        self.symmetry_point_group_name_H_M = ''
        self.js_jq= {}
        self.rules=None
        
        super(CustomForm, self).__init__(*args, **kwargs)
         

    def addFormFields(self,li,section,value,wgt):    
        try:
            line =li.split()
            val= None
            label = None
            fieldname = None
            #print len(line) 
            if len(line) >= 3 and value == None:
                fieldnamelist=  (line[:2])
                fieldname =' '.join(str(e) for e in fieldnamelist)
                fn = ((fieldnamelist[1:])[0]).replace('_prop_',' ')
                fieldlbl = (fn).replace('_',' ').strip().strip("'").strip()
                label= fieldlbl.capitalize()
                value = line[2:]     
    
                val = ' '.join(str(e) for e in value)
                
            elif  len(line) == 1 and value:
                fn = li.replace('_prop_',' ')
                line =(fn.replace('_',' ')).split()
                fieldname = li
                fieldnamelist = (line[1:])
                fieldlbl = ' '.join(str(e) for e in fieldnamelist)
                label= fieldlbl.capitalize()
                val = value
 
           
            if section == 'undefined':
                fieldname+='_undefined'
                self.fields[fieldname] = forms.CharField(label=label,widget = ParrafReadonlyFieldWidget, required=False)
                self.fields[fieldname].initial = '<p id="'+ fieldname +'"> '+val.strip().strip("'").strip()+'</p> '
            else:
                if wgt=='char':
                    v = val.strip().strip("'").strip()
                    size=len(v)
                    self.fields[fieldname] = forms.CharField(label=label, required=False)
                    self.fields[fieldname].widget = forms.TextInput(attrs={'size':str(size + 5), }) 
                    self.fields[fieldname].initial = v 
                elif wgt=='p':
                    self.fields[fieldname] = forms.CharField(label=label,widget = ParrafReadonlyFieldWidget, required=False)
                    self.fields[fieldname].initial = '<p id="'+ fieldname +'"> '+val.strip().strip("'").strip()+'</p> '

                elif wgt=='jq':
                    fieldname+='_'+wgt
                    self.fields[fieldname] = forms.CharField(label='',widget = JQueryCustomFieldWidget, required=False)
                    #html = '<p id="'+ fieldname +'" ></p>'
                    html = ' '
                    jquery = ''
                    jquery += '<script>'
                    if self.rules:
                        jquery += 'django.jQuery(function($) {'
                    jquery += value
                    
                    if self.rules:
                        jquery += '});'
                        
                    jquery += '</script>'
                    jquery +=  "\n\n"   

        
                    html = html  + jquery
                    self.fields[fieldname].initial = html
                    #self.addJsJquery(fieldname,value)
 
            
            self.addAdminField(section,fieldname)
            fieldname = ''
            
            return True
        except  Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            self.error = err
            return False
 
            

            
    def createAdminFields(self,section):
    
        if not self.fieldsets:  
            self.fieldsets = ((section.capitalize(), {'classes': ('collapse',),'fields': []}),)
        else:
            self.fieldsets += ((section.capitalize(), {'classes': ('collapse',),'fields': []}),)
            
        self.fieldsetIndex[section] = self.indexhd
        self.indexhd += 1
 
        
    
    def addAdminField(self,section,fieldname):
        index= self.fieldsetIndex[section]
        self.fieldsets[index][1]['fields'] += [fieldname] 
        
 
          
    def conditionLooped(self, cond, section):
        
        try:
            if isinstance(cond, list):
                for item in cond:
                    print item
        
            return True
        except  Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            self.error = err
            return False
        
          
    def extractTensors(self,prop,coefficents,inputs,index,section):
        propid=str(index) + '_' + prop[0] + prop[1]
 
        tagcoeff= prop[2].strip().strip("'").strip()
        #print coefficents[index]
        id= ''
        nline = {}
         

            
        tensorvalueslist=coefficents[index]
        dimensions=[]
        if isinstance(tensorvalueslist, list):
            dimensions.append(len(tensorvalueslist))
            if isinstance(tensorvalueslist[0], list):
                dimensions.append(len(tensorvalueslist[0]))
            else:
                pass
            
        if len(dimensions) ==2:
            for k2, v2 in inputs[index].iteritems():
                #print k2,v2
                lv=((inputs[index][k2][0]).split('_'))  
                nline[lv[1]] =lv[0]
                id += str(k2)
        elif len(dimensions) ==1:
            for k2, v2 in inputs[index].iteritems():
                lv=((inputs[index][k2][0]).split('_'))  
                if nline.has_key(lv[1]):
                    nline[lv[1]] +=[int(lv[0])]
                else:
                    nline[lv[1]] =[int(lv[0])]
            
        paramslist =[]
        paramslist.append('div_'+ str(propid) )
        table = "<table id='table_"+ str(propid) + "' style='border-collapse: collapse;'> <tbody>"
        tableu = "<table id='table_"+ str(propid) + "' style='border-collapse: collapse;'> <tbody>"
        vartableinputs = "tableinputs_"+ str(propid) 
        paramslist.append(vartableinputs)
        
        paramslist.append(str( prop[0] + prop[1])  + "_jq" )
        input = ''
        
        if len(dimensions) ==2:
 
            paramslist.append("dimensions=2")
            for i in range(int(dimensions[0])):
                trlabels =   "<tr >"
                trvalues =   "<tr >"
                trlabelsu =   "<tr >"
                trvaluesu =   "<tr >"
                
                for j in range(int(dimensions[1])):
                    tagindex = str(i +1 )  + str(j + 1)
                    tag = tagcoeff.replace('ij',tagindex);
                    if nline.has_key(tag):
                        #print nline[tag], tag, str(tensorvalueslist[i][j])
                        coefftoedit= nline[tag] + '_'+ tag

                        paramslist.append(coefftoedit)
                        htmlLabel = "<label style='width: 53px;' for='" +tag +"'   id='lbl_" +coefftoedit+"'>"  + tag +"</label>"  
                        if self.rules:
                            input = "<input type='text' id='"+ tag+"' name='"+ tag+ "' value='"+ str(tensorvalueslist[i][j])+"'   placeholder=''  style='width: 53px;' data-toggle='popover' data-content=''  />"
                        else:
                            input = "<input type='text' id='"+ tag+"' name='"+ tag+ "' value='"+ str(tensorvalueslist[i][j])+"'   placeholder=''  style='width: 53px;' onkeyup='validateField(this)'; data-toggle='popover' data-content='' />"

                    else:
                        coefftoedit= ''
                        htmlLabel = ''
                        htmlLabel = "<label style='width: 53px;' for='" +tag +"' >"  + tag +"</label> "  
                        
                        if self.rules:
                            input = "<input type='text' id='"+ tag+"' name='"+ tag+ "' value='"+ str(tensorvalueslist[i][j])+"'   placeholder=''  style='width: 53px;'  data-toggle='popover'  data-content='' data-content=''  />"
                        else:
                            input = "<input type='text' id='"+ tag+"' name='"+ tag+ "' value='"+ str(tensorvalueslist[i][j])+"'   placeholder=''  style='width: 53px;'  data-toggle='popover'  data-content='' data-content=''  onkeyup='validateField(this);'   />"
                        
                    
 
                    trlabels += " <td>"  +htmlLabel +"</td>" 
 
                    
                    trvalues += " <td  id='"+ coefftoedit+"' >" + str(tensorvalueslist[i][j])+"</td>" 
                    trvaluesu += " <td>" + input +"</td>" 
                       
                
                trlabelsu +=   "</tr>"
                trvaluesu +=   "</tr>"
                
                trlabels +=   "</tr>"
                trvalues +=   "</tr>"
                
                
                tableu += trlabels
                tableu += trvaluesu
                
                table +=  trlabels
                table +=  trvalues
            
        elif len(dimensions) == 1:
            paramslist.append("dimensions=1")
            nline[tagcoeff].sort()
            for i in range(int(dimensions[0])):
                trlabels =   "<tr >"
                trvalues =   "<tr >"
                trlabelsu =   "<tr >"
                trvaluesu =   "<tr >"
                #print tagcoeff, tensorvalueslist[i]
                coefftoedit= str(nline[tagcoeff][i]) + '_'+ tagcoeff
                paramslist.append(coefftoedit)
                htmlLabel = ''
 
                htmlLabel = "<label style='width: 53px;' for='" +tagcoeff +"'   id='lbl_" +coefftoedit+"'>"  + tagcoeff +"</label>"  
                input = "<input type='text' id='"+ coefftoedit+"' name='"+ coefftoedit+ "' value='"+ str(tensorvalueslist[i])+"'   placeholder=''  style='width: 53px;'  onkeyup='validateField(this);'   />"
 
                trlabels += "<td> "+htmlLabel + "</td>"
                trlabels +=  "</tr>'"
                
                
                trvalues += "<td> "+ str(tensorvalueslist[i])+ "</td>"
                trvalues +=   "</tr>"
                table  +=    trlabels      
                table  +=   trvalues  
                
                
                trvaluesu += "<td> "+ input + "</td>"
                trvaluesu +=   "</tr>"
                tableu  +=    trlabels     
                tableu  +=   trvaluesu  
 
        params =   ",".join(  str(e) for e in paramslist) 
        params += "," + "edit"
        function  = "updatecoefficientv2(\"" + params + "\");"
        
        
        table +=   "<tr>"        
        tableu +=   "<tr>"    
        
        table += "<td  style='font-family:Arial; font-size: 12px;'> <p><a href='#' class='submit-row'  onclick='"+ function +"'  >Edit</a></p> </td>"   
        
 
        params=""
        params =   ",".join(  str(e) for e in paramslist) 
        params += "," + "update"
        function2  = "updatecoefficientv2(\\\"" + params + "\\\");"
        
        tableu+= "<td  style='font-family:Arial; font-size: 12px;'> <p><a href='#' class='submit-row'  onclick='"+ function2 +"'  >Update</a></p> </td>"   
        
        tableu +="</tr>"
        tableu +=  "</tbody></table>"
       
        table +="</tr>"
        table +=  "</tbody></table>"
        table +=   "\n\n"   
 
        js = "<script>"
        js +=  "var " + vartableinputs +" = \""  +tableu + "\";"
        js += "</script>"
        js +=  "\n\n"   
        table += js
        
 
        
 
        self.fields['div_'+ str(propid)] = forms.CharField(label=str(index + 1),widget = HTMLCustomFieldWidget, required=False) 
        self.fields['div_'+ str(propid)].initial = table
        
        self.addAdminField(section,'div_'+ str(propid))
 
   
    
    
    def extractOther(self, other, section):
        try:
            und = None
            otherlist = []
            valuesDict = {}
            tagName = ''
            val = []
            objecToSave = None
            pline = None
            vline = None
            counternestedField = None
            for item in other:
                oth = (item.split()) 
                
                if oth[1].startswith('_') :
                    pline = oth[0]
                    if len(oth) == 2:
                        tagName=  (oth[1])
                        counternestedField = 1
                    elif len(oth) > 2:
                        tagName=  (oth[1])
                        #counternestedField = 1
                        vline = oth[0]
                        val= ' '.join(str(e) for e in oth[2:])
                        nl = pline+'_'+vline +' ' +tagName #+ '_' +str(counternestedField)
                        line= nl +' ' +val
                        print line
                        self.addFormFields(line, section, None,'char')
     
                else:
                    vline = oth[0]
                    val= ' '.join(str(e) for e in oth[1:])
                    #fieldnamelist=  (oth[:2])
                    nl = pline+'_'+vline +' ' +tagName + '_' +str(counternestedField)
                    line= nl +' ' +val
                    print line
                    self.addFormFields(line, section, None,'char')
                    counternestedField += 1

            return True
 
                
                
        except  Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            self.error = err
            return False
        
  
    def addJsJquery(self,fieldname, value):    
        try:
            self.js_jq[fieldname] = value
     
        except  Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err= {}
            err['file']=fname
            err['line']=exc_tb.tb_lineno
            err['error']="Error: {1}".format( e.message, e.args) 
            self.error = err
            return False