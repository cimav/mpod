  var type_id= null;
  var select_color_id = null;
  var inline_form_input_id = null;
  var tensor_file_name = null
  var lblHinline_form_input_id = null;
  var lblKinline_form_input_id = null;
  var lblLinline_form_input_id = null;
  var inputHinline_form_input_id = null;
  var inputKinline_form_input_id = null;
  var inputLinline_form_input_id = null;
  var lblOmegainline_form_input_id = null;
  var inputOmegainline_form_input_id = null;
  var btnid = null;
  var ohklspanid = null;
  var spangraph = null;
  var span_btn = null
  var tensor_category = null;
  var jsondatasend = null;
  var array_jsondatasend = [];
  var array_datasend = [];
  var array_values = [];
  var jsonurl= null;
  var property_tag = null;
  var property_id = null;
  var res = "";
  var valuesGET =""
  var btngraphrotated_id = null;
  var html_select_colorb_btngraph = [];
  var html_colorandbtngraph = '';
  var html_btn_polycrystalline = [];
  var html_btnpolycrystalline = '';
  var html_inputs_h = [];
  var html_input_h = '';
  var html_lbls_h = [];
  var html_lbl_h = '';
  var html_lbls_k = [];
  var html_lbl_k = '';
  var html_inputs_k = [];
  var html_input_k = '';
  var html_lbls_l = [];
  var html_lbl_l = '';
  var html_inputs_l =[];
  var html_input_l = '';
  var html_lbls_omega = [];
  var html_lbl_omega = '';
  var html_inputs_omega = [];
  var html_input_omega = '';
  var html_tds_separatorpaddingleft =[];
  var html_tdseparatorpaddingleft = "";
  var html_tds_rotated_matrix = [];
  var html_tdrotated_matrix = "";
  var html_spans_graph = [];
  var html_spangraph = "";
  var html_spans_bnt = [];
  var html_spanbnt = "";  
  var btnPolycrystallinelbl ="Polycrystalline";
  var btnpolycrystalline = null;
  var totalProperties = 0;
  var sendatacounter =0;
  var datasendarray = [];
  var valuearray;
  var valuearrayrotated;
  var file_name ="";
  var valueTen = "";
  var promertyname="";
  var value = "";
  var type = "";
  var tdbuttonpaddingleft = 100;
  var tdseparatorpaddingleft = 50;
  var propertyid= [];
  var propertycounter= 0;
  var counterElements = 0;
  var pathname = window.location.pathname.split( '/' );
  var w = (window.innerWidth/2)-255;
  var wcs = (window.innerWidth/2)-760;
  
  var h = (window.innerHeight/2)-255;
  var options="toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=no,resizable=false,width=525,height=700,top="+h+",left="+w+"";
  var optionscs="toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=no,resizable=false,width=760,height=600,top="+h+",left="+wcs+"";
  var expr = "Firefox";
  
  
  
  var incompletematrix = false
  
  
  navigator.sayswho= (function(){
    var ua= navigator.userAgent, tem, 
    M= ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
    if(/trident/i.test(M[1])){
        tem=  /\brv[ :]+(\d+)/g.exec(ua) || [];
        return 'IE '+(tem[1] || '');
    }
    if(M[1]=== 'Chrome'){
        tem= ua.match(/\b(OPR|Edge)\/(\d+)/);
        if(tem!= null) return tem.slice(1).join(' ').replace('OPR', 'Opera');
    }
    M= M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
    if((tem= ua.match(/version\/(\d+)/i))!= null) M.splice(1, 1, tem[1]);
    return M.join(' ');
})();

 

  function PopupCenter(url, title, w, h) {
   var dualScreenLeft =  0;
   var dualScreenTop =  0;
   var width = 0;
    var height = 0;
    var left = 0;
    var top = 0;
    
    if (navigator.sayswho.includes(expr) == true )
    {
        dualScreenLeft = window.screenLeft != undefined ? window.screenLeft : window.screenX;
        dualScreenTop = window.screenTop != undefined ? window.screenTop : window.screenY;

        width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
        height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;

        
        
        left = ((width / 2) - (w / 2)) + dualScreenLeft;
        top = ((height / 2) - (h / 2)) + dualScreenTop;
       
        w= (w + 200);
        h = (h + 100);
    }
    else
    {
         dualScreenLeft = window.screenLeft != undefined ? window.screenLeft : window.screenX;
        dualScreenTop = window.screenTop != undefined ? window.screenTop : window.screenY;

        width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
        height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;

        left = ((width / 2) - (w / 2)) + dualScreenLeft;
        top = ((height / 2) - (h / 2)) + dualScreenTop;
          left =  left - 50;
         top = top - 50;
    }
    
    var newWindow = window.open(url, title, 'scrollbars=yes, width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);

    // Puts focus on the newWindow
	    if (window.focus) {
	        newWindow.focus();
	    }
    }
    
  function checktype_id(element) {
	  	value = null;
	     item=  element.split("=");
	     if (item[0] =="type_id" )
	    	 value = item[1] 
	     
	    return value ;
	}
  
  function clusterurl(element) {
	  	value = null;
	     item=  element.split("=");
	     if (item[0] =="clusterurl" )
	    	 value = item[1] 
	     
	    return value ;
	}
  
  function tensor(element) {
	  	value = null;
	     item=  element.split("=");
	     if (item[0] =="tensor" )
	    	 value = item[1] 
	     
	    return value ;
	}
  
  function filename(element) {
	  	value = null;
	     item=  element.split("=");
	     if (item[0] =="filename" )
	    	 value = item[1] 
	     
	    return value ;
	}
  
  function dataitem(element) {
	  	value = null;
	     item=  element.split("=");
	     if (item[0] =="dataitem_id" )
	    	 value = item[1] 
	     
	    return value ;
	}

  
  
	function ranktensor(clicked_id, values, selectedid, filename,valuearrayrotated,tensor,incompletematrix,idtd) {			    
	    selectedColor = document.getElementById(selectedid).selectedIndex;	  
		var url = values + "&color=" + selectedColor+ "&"+ valuearrayrotated; 
		if (incompletematrix == 'false')
		{
			 if(tensor != 'undefined' )
			    {
			    	urlGraph = "/dataitem/" + pathname[2] + "/"+ tensor + "/" + url;
			    	PopupCenter(urlGraph, tensor, 760, 600);
			    }
		}
		else
		{
			$( "#" + idtd ).html("");
	         var error=  '<div class="alert alert-danger" role="alert">'
	        	 
		     error= error + 'Incomplete Matrix';
				 
		     error= error + '</div>'
		     $( "#" + idtd ).append(error);
		     return;
				 
			 
		}
	   
	}
  
  function setValuesGET(values,url)
  {
       
	   v=htmlentities.decode(values);
	   var string = fingandreplace(v,'&amp;',"&");
	   var  length =string.length;
	   var stringGET =""
	   for (var i=0; i < length; i++) 
	   {
		   s= string[i];
		   first_char=s.charAt(0);
			   if ((first_char == '[') || (first_char  == ']' ) || (first_char  == "'" )  )
		      {
				   //pass
		      }
			  else
			  {
				  stringGET = stringGET + string[i];
			 } 
	   }
	   
	  
	  listvalues = stringGET.split(",")
	  listvaluestemp = []
	  var mat = "";
	  type_id = null;
	  var tensor_category = "";
	  var jsonurl = '';
	  var found = false;
	   for (var i=0; i < listvalues.length; i++) 
	   {
		   list=listvalues[i].replace(/\s/g, '');
		   spl = list.split("&");
		   if (type_id == null)
		  {
			   a = spl.find(checktype_id);
			   index = spl.indexOf(a);
			   type = a.split("=");
			   type_id = parseInt(type[1]);
			   spl.splice(index, 1);
			   
			   itemurl =spl.find(clusterurl);
			   index = spl.indexOf(itemurl);
			   urlitem = itemurl.split("=");
			   jsonurl = urlitem[1];
			   spl.splice(index, 1);
			   
			   itemcategory= spl.find(tensor);
			   index = spl.indexOf(itemcategory);
			   category = itemcategory.split("=");
			   tensor_category = category[1];
			   spl.splice(index, 1);
			   
			   itemfilename= spl.find(filename);
			   index = spl.indexOf(itemfilename);
			   file = itemfilename.split("=");
			   tensor_file_name = file[1];
			   spl.splice(index, 1);
			   
			   itemdataitem= spl.find(dataitem);
			   index = spl.indexOf(itemdataitem);
			   dataitemid  = itemdataitem.split("=");
			   dataitem_id = dataitemid[1];
			   spl.splice(index, 1);
			   
			   
		  }
		   
		   spl2=list.split("&");
		   listvaluestemp = ""
		 
		   for (var j=0; j < spl2.length; j++) 
		      {
				  val = spl2[j].split("=");
				
				  if (j == (spl2.length - 1))
				  {
					  v = validateValue(val[1]);
					  listvaluestemp  = listvaluestemp + val[0] + "=" + v
					  
				  }
			     else
				  {
			    	 v = validateValue(val[1]);
			    	 listvaluestemp=  listvaluestemp + val[0] + "=" + v +"&";
				  }
		      }
		 
		   
		   
		   //array_values[i] = "?" + listvalues[i]
		   array_values[i] = "?" + listvaluestemp
		   for (var j=0; j < spl.length; j++) 
	      {
			  val = spl[j].split("=");
			  
			  if (val[1] == '?')
				  incompletematrix = true
				  
			  if (j == (spl.length - 1))
			  {
				  v = validateValue(val[1]);
				  mat = mat + v;
			  }
		     else
			  {
		    	 v = validateValue(val[1]);
		    	 mat = mat + v +",";
			  }
	      }
		   
		   //temporary until a type is assigned
		   
		   if (tensor_file_name.indexOf('magnetocrystallineanisotropy') !== -1)
			{
				tensor_category = "magnetocrystallineanisotropy";
			    type_id = 8;
			    jsonurl = 'magnetic';
			}
				
		   //temporary until a type is assigned
			if (tensor_file_name.indexOf('magnetostrictionlambda') !== -1)
			{
				tensor_category = "magnetostriction";
				type_id = 9;	
				jsonurl = 'magneto';
			}
			
		   jsondatasend = { 'mh':0,
										'mk':0,
										'ml':1,
										'omeg':0,
										'mat': mat ,
										'url':jsonurl, //parameter for urlcluster
										'incompletematrix': incompletematrix
										}
		   
		   
		   
		   array_datasend[i] = jsondatasend
		   type_id = null;  
		   mat = "";
		   jsonurl = "";
		    
		   jsondatasend = null;
		   select_color_id= "color" + tensor_file_name;
		   inline_form_input_id= "inlineforminput" + tensor_file_name;
		   lblHinline_form_input_id= 'lblH'+ inline_form_input_id;
		   lblKinline_form_input_id= 'lblK'+ inline_form_input_id;
		   lblLinline_form_input_id= 'lblL'+ inline_form_input_id;
		   lblOmegainline_form_input_id= 'lblOmega'+ inline_form_input_id;
		   inputHinline_form_input_id= 'inputH'+ inline_form_input_id;
		   inputKinline_form_input_id= 'inputK'+ inline_form_input_id;
		   inputLinline_form_input_id= 'inputL'+ inline_form_input_id;
		   inputOmegainline_form_input_id= 'inputOmega'+ inline_form_input_id;
		   btnid='btn' + inline_form_input_id;
		   ohklspanid='span' + inline_form_input_id;
		   spangraph='spangraph' + tensor_file_name;
		   span_btn='span_btn' + tensor_file_name;
		   btnpolycrystalline = 'btnpolycrystalline' + tensor_file_name;
		   tdrotated_matrix_id = 'td' + tensor_file_name;
		   tdseparatorpaddingleft_id = 'tdseparator' + tensor_file_name;
		   btngraphrotated_id='btngraphrotated' + tensor_file_name;
		    
		   if(tensor_category != "undefined")
		    {
		    	//vals = "?" + list;
		    	vals =   array_values[i];
		    	console.log(vals);
		    	
		    	html_colorandbtngraph = '<select id="'+select_color_id+'"><option>Jet</option><option>Hot</option><option>Cool</option><option>Gray</option></select> <button class="btn btn-warning" onclick="ranktensor(this.id,\'' +  vals  + '\',\'' + select_color_id + '\',\'' + tensor_file_name + '\',\'' + valuearray + '\',\'' + tensor_category + '\',\'' + incompletematrix + '\',\'' + tdseparatorpaddingleft_id + '\')" id="'+i+'">Graph</button> ';		     
		    	incompletematrix = false
		    	html_select_colorb_btngraph[i] = html_colorandbtngraph;
			    html_btnpolycrystalline = '<button class="btn btn-warning" onclick="showfields(this.id)" id="'+tensor_file_name+'">' + btnPolycrystallinelbl + '</button>';
			    html_btn_polycrystalline[i] = html_btnpolycrystalline
				html_lbl_h = '<label  id="'+ lblHinline_form_input_id +'"  for="'+ inputHinline_form_input_id+'" style="display: none;" >&nbsp;H: </label>';
				html_input_h = '<input id="'+ inputHinline_form_input_id+'"  type="text" name="h" style="display: none;" value="0" maxlength="4" size="2" disabled>';
				html_lbls_h[i] = html_lbl_h
				html_inputs_h[i] = html_input_h
				html_lbl_k = '<label  id="'+ lblKinline_form_input_id+'"  for="'+ inputKinline_form_input_id+'" style="display: none;" >&nbsp;K: </label>';
				html_input_k = '<input id="'+ inputKinline_form_input_id+'"  type="text" name="k" style="display: none;"  value="0" maxlength="4" size="2"  disabled>';
				html_lbls_k[i] = html_lbl_k
				html_inputs_k[i] = html_input_k
				html_lbl_l = '<label  id="'+ lblLinline_form_input_id+'"  for="'+ inputLinline_form_input_id+'" style="display: none;" >&nbsp;L: </label>';
				html_input_l = '<input id="'+ inputLinline_form_input_id+'"  type="text" name="l" style="display: none;"  value="1" maxlength="4" size="2" disabled>';
				html_lbls_l[i] = html_lbl_l
				html_inputs_l[i] = html_input_l
				html_lbl_omega = '<label  id="'+ lblOmegainline_form_input_id+'"  for="'+ inputOmegainline_form_input_id+'" style="display: none;"  >&nbsp;Omega: </label>';
				html_input_omega = '<input id="'+ inputOmegainline_form_input_id+'"  type="text" name="omega" style="display: none;" maxlength="4" size="4">';
				html_lbls_omega[i] = html_lbl_omega
				html_inputs_omega[i] = html_input_omega
				html_tdseparatorpaddingleft = " <td  style='padding: 0px 0px 0px "+ tdseparatorpaddingleft + "px;'  id='"+  tdseparatorpaddingleft_id +"' > </td>" ;
				html_tds_separatorpaddingleft[i] = html_tdseparatorpaddingleft ;
				html_tdrotated_matrix = " <td  id='"+  tdrotated_matrix_id +"' ></td>" ;
				html_tds_rotated_matrix[i] = html_tdrotated_matrix;
				html_spanbnt = '<span  id="'+ span_btn + '" style="display: none;" ><button class="btn btn-warning"  onclick="callajax(this.id,\'' + tdseparatorpaddingleft_id + '\',\''  + i +'\',\'' +spangraph +'\',\'' + tensor_file_name + '\',\'' + vals + '\',\'' + tensor_category + '\',\'' + inputOmegainline_form_input_id + '\',\'' + select_color_id + '\',\'' + btngraphrotated_id + '\',\'' + url + '\')" id="'+ btnpolycrystalline + '">Apply Texture</button></span>';
				html_spans_graph[i] = html_spanbnt;	
				html_spangraph = '<span  id="'+ spangraph + '"  ></span>';
				html_spans_bnt[i] = html_spangraph;	   
		    }
		    else
	    	{
			    html_colorandbtngraph= "";
				html_btnpolycrystalline= "";						
				html_lbl_h= "";
				html_input_h= "";				
				html_lbl_k = "";
				html_input_k= "";	
				html_lbl_l= "";
				html_input_l = "";
				html_lbl_omega = "";
				html_input_omega = "";
				html_spanbnt = "";
			    html_select_colorb_btngraph[i] = html_colorandbtngraph;			    
				html_btn_polycrystalline[i] = html_btnpolycrystalline;				
			    html_lbls_h[i] = html_lbl_h;
				html_inputs_h[i] = html_input_h;
				html_lbls_k[i] = html_lbl_k;
				html_inputs_k[i] = html_input_k;				
			 	html_lbls_l[i] = html_lbl_l;
				html_inputs_l[i] = html_input_l;				
			 	html_lbls_omega[i] = html_lbl_omega;
				html_inputs_omega[i] = html_input_omega;		
				html_tdseparatorpaddingleft = " <td  style='padding: 0px 0px 0px "+ tdseparatorpaddingleft + "px;'  id='"+  tdseparatorpaddingleft_id +"' > </td>" ;
				html_tds_separatorpaddingleft[i] = html_tdseparatorpaddingleft ;
				html_tdrotated_matrix = " <td  id='"+  tdrotated_matrix_id +"' ></td>" ;
				html_tds_rotated_matrix[i] = html_tdrotated_matrix;
			    html_spans_graph[i] = html_spanbnt;
				html_spangraph = '<span  id="'+ spangraph + '"  ></span>';
				html_spans_bnt[i] = html_spangraph;
	    	}
	   }
  }
	
   function showfields(clicked_id) {
		$( "#inputOmegainlineforminput" + clicked_id ).show();
		$( "#lblOmegainlineforminput" + clicked_id ).show();
		$( "#inputHinlineforminput" + clicked_id ).show();
		$( "#lblHinlineforminput" + clicked_id ).show();
		$( "#inputKinlineforminput" + clicked_id ).show();
		$( "#lblKinlineforminput" + clicked_id ).show();
		$( "#inputLinlineforminput" + clicked_id ).show();
		$( "#lblLinlineforminput" + clicked_id ).show();
		$( "#span_btn" + clicked_id ).show();
	}
   
   function callajax(clicked_id,idtd,arrayindex,spanid, filename,values,tensor,omegid,selectid,btngraphrotated_id,url) {
		$( "#" + idtd ).html("");
		$( "#" + spanid ).html("");
		omeg=  $("#" + omegid ).val();
		data =array_datasend[arrayindex]
		incompletematrix = data.incompletematrix
		if (data.incompletematrix == true)
		{
			$( "#" + idtd ).html("");
	         var error=  '<div class="alert alert-danger" role="alert">'
	 
	         error= error + 'Incomplete Matrix: can not be solved';
			 
	         error= error + '</div>'
			 $( "#" + idtd ).append(error);
			 return;
		}
 
	   
		
		datasend = {'mh':data.mh,
								'mk':data.mk,
								'ml':data.ml,
								'omeg':omeg,
								'mat': data.mat,
								'url':data.url
								}
		
		$.ajax({
       	type: "POST",
           url: url,
           data: datasend,
           dataType: 'json',
           success: function (data) {
           		$( "#" + idtd ).append(data.html);
           		$( "#" + spanid ).append('<button class="btn btn-warning" onclick="ranktensor(this.id,\'' +  values + '\',\'' + selectid + '\',\'' + filename + '\',\'' + data.valuearrayrotated + '\',\'' + tensor + '\',\'' + incompletematrix + '\',\'' + idtd + '\');" id="'+btngraphrotated_id+'">Graph</button>' );
        	 },
		 	error: function (data) {
       		if(data.status == 500)
       			alert("Resource not found");
          	 },
       }); 
	}

   (function(window){
		window.htmlentities = {
			/**
			 * Converts a string to its html characters completely.
			 *
			 * @param {String} str String with unescaped HTML characters
			 **/
			encode : function(str) {
				var buf = [];
				
				for (var i=str.length-1;i>=0;i--) {
					buf.unshift(['&#', str[i].charCodeAt(), ';'].join(''));
				}				
				return buf.join('');
			},
			/**
			 * Converts an html characterSet into its original character.
			 *
			 * @param {String} str htmlSet entities
			 **/
			decode : function(str) {
				return str.replace(/&#(\d+);/g, function(match, dec) {
					return String.fromCharCode(dec);
				});
			}
		};
	})(window);
   
   function fingandreplace(string,target,newchar) 
   {
	   var stringlocal = string
	   var  length = stringlocal.length;
	   //var res = "";
	   for (var i=0; i < length; i++) 
	   {		   
		   stringlocal = stringlocal.replace(target, newchar);
	   }
	   //console.log("listtensortags: " + stringlocal);
	   return stringlocal
   }
   
   
   function validateValue(value) {
       var str = value
       var expreg =         /^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)$|^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)\([-+]?\d+(\.\d+)?\)$|^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)\([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)\)$|^[-+]?\d+(\.\d+)?$|^[-+]?\d+(\.\d+)?\([-+]?\d+(\.\d+)?\)$|^[-+]?\d+(\.\d+)?\([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)\)$/;
       var val = '';
     
       var result = str.match(expreg);
       if(result != null)
       {
         val=parseFloat(result[0].replace(/ *\([^)]*\) */g, "") );
         return  val;
       }
       else
       {
           return value;
       }
     }
   
  