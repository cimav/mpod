  var list_tensor_tags = new Array()
  var list_tensor_tags_counter = 0;
  var list_tensor_filename_counter = 0;
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
  var jsonurl= null;
  var property_tag = null;
  var property_id = null;
  var res = "";
  var valuesGET =""
  var btngraphrotated_id = null;
  
  var html_colorandbtngraph = ''
  var html_btnpolycrystalline = ''
  var html_input_h = ''
  var html_lbl_h = ''
  var html_lbl_k = ''
  var html_input_k = ''
  var html_lbl_l = ''
  var html_input_l = ''
  var html_lbl_omega = ''
  var html_input_omega = ''
  var html_tdseparatorpaddingleft = "";
  var html_tdrotated_matrix = "";
  var html_spangraph = null;
  var html_spanbnt = null
	  
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
  var wcs = (window.innerWidth/2)-525;
  var h = (window.innerHeight/2)-255;
  var options="toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=no,resizable=false,width=525,height=700,top="+h+",left="+w+"";
  var optionscs="toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=no,resizable=false,width=1070,height=700,top="+h+",left="+wcs+"";
  
  
  function parseTensorTag(tags)
  {

		   b = fingandreplace(tags,'&quot;',"\"");
		   obj = JSON.parse(b);

		   
		   list_tensor_tags[list_tensor_tags_counter]=obj;
		   list_tensor_tags_counter++;
		   
	
  }
  
  
   function parseTensorValue(propertyid, propertytag,matrixString,codefile,url)
	{
	    
	   property_id = propertyid;
	   property_tag= propertytag
	   var coeffi = null
	   var found = false;
	   for (var i = 0; i < list_tensor_tags.length; i++)
		{
         
		   for (var j = 0; j < list_tensor_tags[i].dataproperty_ids.length; j++)
			{   
			      tensor_file_name =codefile + propertytag.replace(/\s/g,'').replace(/,/g , '') + list_tensor_filename_counter.toString(); 
			      
			      if( list_tensor_tags[i].dataproperty_ids[j] == propertyid )
				   {  
			    	  type_id = list_tensor_tags[i].type_id
				      switch(type_id)
				      {
						case 1:
							tensor_category = "stiffness";
							jsonurl = 'celasfib';
							found = true;
							break;
						case 2:
							tensor_category = "compliance";
							jsonurl = 'selasfib';
							found = true;
							break;
						case 3:
							tensor_category = "thirdranktensordg";
							jsonurl = 'dpiezofib'; 
							found = true;	
							break;
						case 7:
							tensor_category = "thirdranktensoreh";
							jsonurl = 'epiezofib' ;
							found = true;
							break;
						case 4:
							tensor_category = "secondranktensor";
							jsonurl = 'dielecfib';
							found = true;								
							break;
						case 11:
							tensor_category = "secondranktensor";
							jsonurl = 'dielecfib';
							found = true;								
							break;
							
						case 5:
							tensor_category = "fourthranktensor";
							jsonurl = 'fourthranktensor';
							found = true;								
							break;
						case 6:
							tensor_category = "fourthranktensor";
							jsonurl =  'fourthranktensor';
							found = true;
							break;
				      }
				      
                      if(found)
                      {
                    	  dim = Array.from ( list_tensor_tags[i].tensor_dimensions);
    				      coeffi= dim[0] * dim[1];
    				      break;
                      }

				      
				   }
			      
			    
			}
		   
		   if(found)
           {
		    	  break;
           }
	    }
	   
	   
	  
		if (propertytag =='magnetocrystalline anisotropy k1, k2')
		{
			coeffi = 1;
			tensor_category = "magnetic";
		    type_id = 8;
		    jsonurl = 'magnetic';
		}
			
	    
		if (propertytag =='magnetostriction lambda 100, lambda 111' )
		{
			coeffi = 1;
			tensor_category = "magneto";
			type_id = 9;	
			jsonurl = 'magneto';
		}
		
	   	  
       
	   
		
	   var decodedtext =htmlentities.decode(matrixString);
	   //var res= linkgen(decodedtext,coeffi);
	   valuesGET = linkgen(decodedtext,coeffi);
	   
	   array_jsondatasend[list_tensor_filename_counter] = jsondatasend
	   console.log(array_jsondatasend[list_tensor_filename_counter] );
	   

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
	    
       
	    html_colorandbtngraph = '<select id="'+select_color_id+'"><option>Jet</option><option>Hot</option><option>Cool</option><option>Gray</option></select> <button class="btn btn-warning" onclick="' + tensor_category + '(this.id,\'' + valuesGET + '\',\'' + select_color_id + '\',\'' + tensor_file_name + '\',\'' + valuearray + '\')" id="'+list_tensor_tags_counter+'">Graph</button> ';
	    //console.log(html_colorandbtngraph);
	    
	    html_btnpolycrystalline = '<button class="btn btn-warning" onclick="showfields(this.id)" id="'+tensor_file_name+'">' + btnPolycrystallinelbl + '</button>';


		html_lbl_h = '<label  id="'+ lblHinline_form_input_id +'"  for="'+ inputHinline_form_input_id+'" style="display: none;" >&nbsp;H: </label>';
		html_input_h = '<input id="'+ inputHinline_form_input_id+'"  type="text" name="h" style="display: none;" value="0" maxlength="4" size="2" disabled>';
		
		html_lbl_k = '<label  id="'+ lblKinline_form_input_id+'"  for="'+ inputKinline_form_input_id+'" style="display: none;" >&nbsp;K: </label>';
		html_input_k = '<input id="'+ inputKinline_form_input_id+'"  type="text" name="k" style="display: none;"  value="0" maxlength="4" size="2"  disabled>';
		
		html_lbl_l = '<label  id="'+ lblLinline_form_input_id+'"  for="'+ inputLinline_form_input_id+'" style="display: none;" >&nbsp;L: </label>';
		html_input_l = '<input id="'+ inputLinline_form_input_id+'"  type="text" name="l" style="display: none;"  value="1" maxlength="4" size="2" disabled>';
		
		
		html_lbl_omega = '<label  id="'+ lblOmegainline_form_input_id+'"  for="'+ inputOmegainline_form_input_id+'" style="display: none;"  >&nbsp;Omega: </label>';
		html_input_omega = '<input id="'+ inputOmegainline_form_input_id+'"  type="text" name="omega" style="display: none;" maxlength="4" size="4">';
		
		
		html_tdseparatorpaddingleft = " <td  style='padding: 0px 0px 0px "+ tdseparatorpaddingleft + "px;'  id='"+  tdseparatorpaddingleft_id +"' > </td>" ;
		html_tdrotated_matrix = " <td  id='"+  tdrotated_matrix_id +"' ></td>" ;
		
		html_spanbnt = '<span  id="'+ span_btn + '" style="display: none;" ><button class="btn btn-warning"  onclick="callajax(this.id,\'' + tdseparatorpaddingleft_id + '\',\''  +list_tensor_filename_counter +'\',\'' +spangraph +'\',\'' + tensor_file_name + '\',\'' + valuesGET + '\',\'' + tensor_category + '\',\'' + inputOmegainline_form_input_id + '\',\'' + select_color_id + '\',\'' + btngraphrotated_id + '\',\'' + url + '\')" id="'+ btnpolycrystalline + '">Apply Texture</button></span>';

		html_spangraph = '<span  id="'+ spangraph + '"  ></span>';
		
		
		list_tensor_filename_counter++;
	}
   
   function thirdranktensordg(clicked_id, values, selectedid, filename,valuearrayrotated) {
		 selectedColor = document.getElementById(selectedid).selectedIndex;
		 var url = values + "&color=" + selectedColor+"&filename="+ filename + "&"+ valuearrayrotated; 
	     urlGraph = "/dataitem/" + pathname[2] + "/thirdranktensordg/" + url;

		    if (valuearrayrotated == 'undefined' )
        window.open(urlGraph,"",options);
     else
  	  window.open(urlGraph,"",optionscs);
	}
	
	
	function thirdranktensoreh(clicked_id, values, selectedid, filename,valuearrayrotated) {
		  selectedColor = document.getElementById(selectedid).selectedIndex;
		  var url = values + "&color=" + selectedColor+"&filename="+ filename + "&"+ valuearrayrotated; 
		  urlGraph = "/dataitem/" + pathname[2] + "/thirdranktensoreh/" + url;

	      if (valuearrayrotated == 'undefined' )
	          window.open(urlGraph,"",options);
	       else
	    	  window.open(urlGraph,"",optionscs);
	}
	

	function secondranktensor(clicked_id, values, selectedid, filename,valuearrayrotated) {			    
	    selectedColor = document.getElementById(selectedid).selectedIndex;	  
		var url = values + "&color=" + selectedColor+"&filename="+ filename + "&"+ valuearrayrotated; 
	    urlGraph = "/dataitem/" + pathname[2] + "/secondranktensor/" + url;
	    
	    if (valuearrayrotated == 'undefined' )
	       window.open(urlGraph,"",options);
	    else
	    	window.open(urlGraph,"",optionscs);

	}
	
	function compliance(clicked_id, values, selectedid, filename,valuearrayrotated) {
	    selectedColor = document.getElementById(selectedid).selectedIndex;							    
	    var url = values + "&color=" + selectedColor+"&filename="+ filename + "&"+ valuearrayrotated; 
	    urlGraph = "/dataitem/" + pathname[2] + "/compliance/" + url;
	    
		 window.open(urlGraph,"",optionscs);
	    
	} 
	
	function stiffness(clicked_id, values, selectedid, filename,valuearrayrotated) {
	    selectedColor = document.getElementById(selectedid).selectedIndex;							    
	    var url = values + "&color=" + selectedColor+"&filename="+ filename + "&"+ valuearrayrotated; 
	    urlGraph = "/dataitem/" + pathname[2] + "/stiffness/" + url;
	    
	    window.open(urlGraph,"",optionscs);

	}
	
	function fourthranktensor(clicked_id, values, selectedid, filename,valuearrayrotated) {
	    selectedColor = document.getElementById(selectedid).selectedIndex;
		var url = values + "&color=" + selectedColor+"&filename="+ filename + "&"+ valuearrayrotated; 
		urlGraph = "/dataitem/" + pathname[2] + "/fourthranktensor/" + url;

	    if (valuearrayrotated == 'undefined' )
  	       window.open(urlGraph,"",options);
		    else
		    	window.open(urlGraph,"",optionscs);
		
	}
	
	function magnetic(clicked_id, values, selectedid, filename,valuearrayrotated) {
	    selectedColor = document.getElementById(selectedid).selectedIndex;					
		var url = values + "&color=" + selectedColor+"&filename="+ filename + "&"+ valuearrayrotated; 
	    urlGraph = "/dataitem/" + pathname[2] + "/magnetocrystallineanisotropy/" + url;
	    
	    if (valuearrayrotated == 'undefined' )
  	       window.open(urlGraph,"",options);
		 else
		    	window.open(urlGraph,"",optionscs);

	}
	
	function magneto(clicked_id, values, selectedid, filename,valuearrayrotated) {
	    selectedColor = document.getElementById(selectedid).selectedIndex;
		var url = values + "&color=" + selectedColor+"&filename="+ filename + "&"+ valuearrayrotated; 
	    urlGraph = "/dataitem/" + pathname[2] + "/magnetostriction/" + url;
	    if (valuearrayrotated == 'undefined' )
  	       window.open(urlGraph,"",options);
		 else
		    	window.open(urlGraph,"",optionscs);

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

		data =array_jsondatasend[arrayindex]

		datasend = {'mh':data.mh,
								'mk':data.mk,
								'ml':data.ml,
								'omeg':omeg,
								'mat': data.mat,
								'url':data.url
								}
		
		/*url = "{% url rotatematrix 0000000 -1%}";
		url = url.replace(/0/, codefile.toString());
		
		alert(url);*/
		
		$.ajax({
       	type: "POST",
           url: url,
           data: datasend,
           dataType: 'json',
           success: function (data) {
           	 
           	$( "#" + idtd ).append(data.html);
           	
               if (tensor == 'thirdranktensordg')
           	    $( "#" + spanid ).append('<button class="btn btn-warning" onclick="thirdranktensordg(this.id,\'' +  values + '\',\'' + selectid + '\',\'' + filename + '\',\'' + data.valuearrayrotated + '\');" id="'+btngraphrotated_id+'">Graph</button>' );
               else if (tensor == 'thirdranktensoreh')
           	    $( "#" + spanid ).append('<button class="btn btn-warning" onclick="thirdranktensoreh(this.id,\'' +  values + '\',\'' + selectid + '\',\'' + filename + '\',\'' + data.valuearrayrotated + '\');" id="'+btngraphrotated_id+'">Graph</button>' );
               else if (tensor == 'secondranktensor')
               	$( "#" + spanid ).append('<button class="btn btn-warning" onclick="secondranktensor(this.id,\'' +  values + '\',\'' + selectid + '\',\'' + filename + '\',\'' + data.valuearrayrotated + '\');" id="'+btngraphrotated_id+'">Graph</button>' );
               else if (tensor == 'compliance')
               	$( "#" + spanid ).append('<button class="btn btn-warning" onclick="compliance(this.id,\'' +  values + '\',\'' + selectid + '\',\'' + filename + '\',\'' + data.valuearrayrotated + '\');" id="'+btngraphrotated_id+'">Graph</button>' );
               else if (tensor == 'stiffness')
               	 $( "#" + spanid ).append('<button class="btn btn-warning" onclick="stiffness(this.id,\'' +  values + '\',\'' + selectid + '\',\'' + filename + '\',\'' + data.valuearrayrotated + '\');" id="'+btngraphrotated_id+'">Graph</button>' );
               else if (tensor == 'fourthranktensor')
               	$( "#" + spanid ).append('<button class="btn btn-warning" onclick="fourthranktensor(this.id,\'' +  values + '\',\'' + selectid + '\',\'' + filename + '\',\'' + data.valuearrayrotated + '\');" id="'+btngraphrotated_id+'">Graph</button>' );
               else if (tensor == 'magnetic')
               	$( "#" + spanid ).append('<button class="btn btn-warning" onclick="magnetic(this.id,\'' +  values + '\',\'' + selectid + '\',\'' + filename + '\',\'' + data.valuearrayrotated + '\');" id="'+btngraphrotated_id+'">Graph</button>' );
               else if (tensor == 'magneto')
               	$( "#" + spanid ).append('<button class="btn btn-warning" onclick="magneto(this.id,\'' +  values + '\',\'' + selectid + '\',\'' + filename + '\',\'' + data.valuearrayrotated + '\');" id="'+btngraphrotated_id+'">Graph</button>' );

           	
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
   
   
   function linkgen(string,coeffi) 
   {
	  
	   valuesGET = "";
	   var  length = string.length;
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
				   
				  valuesGET = valuesGET + string[i];
			 }
		   
	 
		     
	   }
       
	   var counterElements=0;
	   var partsOfStr = valuesGET.split(',');
	   //alert(partsOfStr);
	   for (var i=0; i < partsOfStr.length; i++) 
		   {
		        
				if(isNaN(partsOfStr[i]))
				{ 
					//console.log(valueTen);
					var end = partsOfStr[i].indexOf("(");
					if(end > 0)
					{
						valueTen = partsOfStr[i].slice(0,end);
						 
					}
					else
					{
						valueTen = 0;
					}
	
				}
				else
				{ 
					valueTen = partsOfStr[i].trim();
					
				}
				
				
				counterElements++;
		   		switch(counterElements){
				case 1:
					var val1 = valueTen;
					break;
				case 2:
					var val2 = valueTen;
					break;
				case 3:
					var val3 = valueTen;
					break;
				case 4:
					var val4 = valueTen;
					break;
				case 5:
					var val5 = valueTen;
					break;
				case 6:
					var val6 = valueTen;
					break;
				case 7:
					var val7 = valueTen;
					break;
				case 8:
					var val8 = valueTen;
					break;
				case 9:
					var val9 = valueTen;
					break;
				case 10:
					var val10 = valueTen;
					break;
				case 11:
					var val11 = valueTen;
					break;
				case 12:
					var val12 = valueTen;
					break;
				case 13:
					var val13 = valueTen;
					break;
				case 14:
					var val14 = valueTen;
					break;
				case 15:
					var val15 = valueTen;
					break;
				case 16:
					var val16 = valueTen;
					break;
				case 17:
					var val17 = valueTen;
					break;
				case 18:
					var val18 = valueTen;
					break;
				case 19:
					var val19 = valueTen;
					break;
				case 20:
					var val20 = valueTen;
					break;
				case 21:
					var val21 = valueTen;
					break;
				case 22:
					var val22 = valueTen;
					break;
				case 23:
					var val23 = valueTen;
					break;
				case 24:
					var val24 = valueTen;
					break;
				case 25:
					var val25 = valueTen;
					break;
				case 26:
					var val26 = valueTen;
					break;
				case 27:
					var val27 = valueTen;
					break;
				case 28:
					var val28 = valueTen;
					break;
				case 29:
					var val29 = valueTen;
					break;
				case 30:
					var val30 = valueTen;
					break;
				case 31:
					var val31 = valueTen;
					break;
				case 32:
					var val32 = valueTen;
					break;
				case 33:
					var val33 = valueTen;
					break;
				case 34:
					var val34 = valueTen;
					break;
				case 35:
					var val35 = valueTen;
					break;
				case 36:
					var val36 = valueTen;
					break;
			}
		}
	   var values = null;
	   if (coeffi==9)
	   {
		   values = "?value11="+val1+"&value12="+val2+"&value13="+val3+"&value21="+val4+"&value22="+val5+"&value23="+val6+"&value31="+val7+"&value32="+val8+"&value33="+val9 ;
		   values = values.replace(/\s/g, '');
		   mat = val1+","+val2+","+val3+","+val4+","+val5+","+val6+","+val7+","+val8+","+val9
		   mat = mat.replace(/\s/g, '');
		   jsondatasend = { 'mh':0,
											'mk':0,
											'ml':1,
											'omeg':0,
											'mat': mat ,
											'url':jsonurl   
											}
			
	   } else if (coeffi==18)
	   {
		   values = "?value11="+val1+"&value12="+val2+"&value13="+val3+"&value14="+val4+"&value15="+val5+"&value16="+val6+"&value21="+val7+"&value22="+val8+"&value23="+val9+"&value24="+val10+"&value25="+val11+"&value26="+val12+"&value31="+val13+"&value32="+val14+"&value33="+val15+"&value34="+val16+"&value35="+val17+"&value36="+val18;
		   values = values.replace(/\s/g, '');
		   mat = val1+","+val2+","+val3+","+val4+","+val5+","+val6+","+val7+","+val8+","+val9+","+val10+","+val11+","+val12+","+val13+","+val14+","+val15+","+val16+","+val17+","+val18;
		   mat = mat.replace(/\s/g, '');
		   values = values.replace(/\undefined/g, '');
		   jsondatasend = { 'mh':0,
											'mk':0,
											'ml':1,
											'omeg':0,
											'mat': mat ,
											'url':jsonurl  //parameter for urlcluster
											}
		   
	   }else if (coeffi==36)
	   {
		   values = "?value11="+val1+"&value12="+val2+"&value13="+val3+"&value14="+val4+"&value15="+val5+"&value16="+val6+"&value21="+val7+"&value22="+val8+"&value23="+val9+"&value24="+val10+"&value25="+val11+"&value26="+val12+"&value31="+val13+"&value32="+val14+"&value33="+val15+"&value34="+val16+"&value35="+val17+"&value36="+val18+"&value41="+val19+"&value42="+val20+"&value43="+val21+"&value44="+val22+"&value45="+val23+"&value46="+val24+"&value51="+val25+"&value52="+val26+"&value53="+val27+"&value54="+val28+"&value55="+val29+"&value56="+val30+"&value61="+val31+"&value62="+val32+"&value63="+val33+"&value64="+val34+"&value65="+val35+"&value66="+val36;
		   values = values.replace(/\s/g, '');
		   values = values.replace(/\undefined/g, '');
		   mat =  val1+","+val2+","+val3+","+val4+","+val5+","+val6+","+val7+","+val8+","+val9+","+val10+","+val11+","+val12+","+val13+","+val14+","+val15+","+val16+","+val17+","+val18+","+val19+","+val20+","+val21+","+val22+","+val23+","+val24+","+val25+","+val26+","+val27+","+val28+","+val29+","+val30+","+val31+","+val32+","+val33+","+val34+","+val35+","+val36;
		   mat = mat.replace(/\s/g, '');
		   jsondatasend = { 'mh':0,
											'mk':0,
											'ml':1,
											'omeg':0,
											'mat': mat ,
											'url':jsonurl //parameter for urlcluster
											}
	   }else if (coeffi==1)
	   {
		   values = "?value11="+val1+"&value12="+val2+"&value13="+val3+"&value14="+val4;
		   values = values.replace(/\s/g, '');
		   values = values.replace(/\undefined/g, '');
		     
		   
		   mat =  val1+","+val2+","+val3+","+val4;
		   mat = mat.replace(/\s/g, '');
		   jsondatasend = { 'mh':0,
											'mk':0,
											'ml':1,
											'omeg':0,
											'mat': mat ,
											'url':jsonurl   //parameter for urlcluster
											}
	   }
	   
	   
 
	     return values;
	   
}
