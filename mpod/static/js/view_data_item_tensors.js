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
  var spanid = null;
  var spangraphid = null;
  var tensor_category = null;
  var jsondatasend = null;
  var jsonurl= null;
  var property_tag = null;
  var property_id = null;
  var res = "";
  
  function parseTensorTag(tags)
  {

		   b = fingandreplace(tags,'&quot;',"\"");
		   obj = JSON.parse(b);

		   
		   list_tensor_tags[list_tensor_tags_counter]=obj;
		   list_tensor_tags_counter++;
		   
	
  }
  
  
   function parseTensorValue(propertyid, propertytag,matrixString,codefile)
	{
	   
	   property_id = propertyid;
	   property_tag= propertytag
	   var coeffi = null
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
							jsonurl = 'celasfib'
							break;
						case 2:
							tensor_category = "compliance";
							jsonurl = 'selasfib'
							break;
						case 3:
							tensor_category = "thirdranktensordg";
							jsonurl = 'dpiezofib' 
							break;
						case 7:
							tensor_category = "thirdranktensoreh";
							jsonurl = 'epiezofib' 
							break;
						case 4:
							tensor_category = "secondranktensor";
							jsonurl = 'dielecfib'
							break;
						case 11:
							tensor_category = "secondranktensor";
							jsonurl = 'dielecfib'
							break;
							
						case 5:
							tensor_category = "fourthranktensor";
							jsonurl = 'fourthranktensor'
							break;
						case 6:
							tensor_category = "fourthranktensor";
							jsonurl =  'fourthranktensor'
							break;
						
					
 

							
				      }
				      

				      dim = Array.from ( list_tensor_tags[i].tensor_dimensions)
				      coeffi= dim[0] * dim[1]

				      
				      
				   }
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
		
	   	  
       
	   
	   list_tensor_filename_counter++;
	   var decodedtext =htmlentities.decode(matrixString);
	   var res= linkgen(decodedtext,coeffi);
	    
	   

	   select_color_id= "color" + tensor_file_name;
	   
	   inline_form_input_id= "inlineforminput" + tensor_file_name;
	   
	   
	   lblHinline_form_input_id= 'lblH'+ inline_form_input_id;
	   lblKinline_form_input_id= 'lblK'+ inline_form_input_id;
	   lblLinline_form_input_id= 'lblL'+ inline_form_input_id;
	   lblOmegainline_form_input_id= 'lblOmega'+ inline_form_input_id;
	   
	   inputHinline_form_input_id= 'inputH'+ inline_form_input_id;
	   inputKinline_form_input_id= 'inputH'+ inline_form_input_id;
	   inputLinline_form_input_id= 'inputH'+ inline_form_input_id;
	   inputOmegainline_form_input_id= 'inputOmega'+ inline_form_input_id;
	   
		btnid='btn' + inline_form_input_id;
	    spanid='span' + inline_form_input_id;
	    spangraphid='spangraph' + inline_form_input_id;
	   
	   /*
	   console.log("id: " + property_id);
	   console.log("tag: " + property_tag);
	   console.log("tensor_category: " + tensor_category);
	   console.log("url: " + jsondatasend.url);
	   console.log("values:" + res);
	   console.log("type: " + type_id); 
	   console.log(tensor_file_name);
	   console.log(inline_form_input_id);
	   console.log(lblHinline_form_input_id);
	   console.log(lblKinline_form_input_id);
	   console.log(lblLinline_form_input_id);
	   console.log(lblOmegainline_form_input_id);
	   console.log(inputHinline_form_input_id);
	   console.log(inputKinline_form_input_id);
	   console.log(inputLinline_form_input_id);
	   console.log(inputOmegainline_form_input_id);
	   console.log(btnid);
	   console.log(spanid);
	   console.log(spangraphid);
       */
 
		
	   

	  return;

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
	  
	   
	   var  length = string.length;
	  
	   for (var i=0; i < length; i++) 
	   {
		   s= string[i];
		   first_char=s.charAt(0);
			   if ((first_char == '[') || (first_char  == ']' ) || (first_char  == "'" )  )
		      {
				   //
		      }
			  else
			  {
				   
				   res = res + string[i];
			 }
		     
	   }
       
	   var counterElements=0;
	   var partsOfStr = res.split(',');
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
