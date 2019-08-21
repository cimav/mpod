var listOfSelectMultiple = []
django.jQuery(function($) {
	$( window ).load(function() {     
		
		//console.log($('input[type=hidden]'));
		 
		$('.divjscode').each(function(){
			element = $(this)
			var label = $("label[for='"+element.attr('id')+"']")
			label.text('')
		}); 
		
		
		
		$('input[type=hidden]').each(function(){
			element = $(this)
			var label = $("label[for='"+element.attr('id')+"']")
			label.text('')
		}); 
		
		fieldsetcount = 0;
		$('fieldset').each(function(){
			element = $(this)
			if (fieldsetcount== 0)
			{
				//element.removeClass( "collapsed" ).addClass( "collapse" );
				//$('#fieldsetcollapser'+fieldsetcount).text('Hide');
				
				console.log( element.attr('class'));
				$('#fieldsetcollapser'+fieldsetcount ).click(function() {
			 
					console.log( element.attr('class'))
		 
	 
	            });
			 }
			else
				{
					$('#fieldsetcollapser'+fieldsetcount ).click(function() {
						 
						console.log( $(this).attr('class'));
						 
		 
		            });
				
				}
			 
			//console.log( fieldsetcount)
			fieldsetcount++;
			
			
			
	
		}); 
		 
		
		/*
		$( "select" ).each(function( index ) {
              if($( this ).attr('multiple'))
              {
                    //console.log( index + ": " + $( this ).attr('name'));
                    //console.log( $( this ).attr('id'));
                    domId=$( this ).attr('id');
                    strId= "id_";
                    strFrom= "_from";
                    strTo= "_to";
                    var domName = domId.substring(strId.length, domId.length);
                    var url='';
                    var todo = '';
                    var fullUrl ='';
                    divformrowfield = "div.form-row.field-" ;
                 
                    if (domName.indexOf("_from") >= 0)
                    {
                        url = domName.substring(0 ,  domName.length - strFrom.length );
                        todo='from'
                    }
                   
                    if (domName.indexOf("_to") >= 0)
                    {
                        url = domName.substring(0 ,  domName.length - strTo.length );
                        todo='to'
                    }
                       
                    if(url == 'properties')
                    {
                       fullUrl = urlproperties;
                       listOfSelectMultiple[index] = $( this ).attr('id')
                    }
                       
                    if(url == 'experimentalcon')
                    {
                       fullUrl = urlexperimentalcon;
                    }

                    divformrowfield = divformrowfield + url;
                    iddivformrowfield = "divformrowfield" + url
                    //console.log($('#' + iddivformrowfield).html());
                    if  ($('#' + iddivformrowfield).html() == null)
                    {
                        //console.log(  $('#' + iddivformrowfield).html() == null )
                    
                        //$(divformrowfield).append('<div id="' + iddivformrowfield+ '" style="display:none;" > </div>');
                        $(divformrowfield).append('<div   id="' + iddivformrowfield+ '" style="border:0px solid black; width: 40%; float: left;  " > </div>');
                    }
 
                                                  //console.log( $( this ).attr('id'));
                  $( this ).click(function() {
                        iddivformrowfield = "divformrowfield" + url;        
                        datasend ={'todo': todo,
                                               'value':$(this).val()[0] 
                                              }
                         
                            callajax(fullUrl, datasend,iddivformrowfield);
                        });
                 }
            });*/

	});

   /* $(document).ready(function() {
      django.jQuery("[name=properties]").change(function() {
            console.log($(this).val());
        });

	});*/
    
    
 });
 
 
 
 function updatecondition(conditionId)
{
   var listParams= []
   datasend ={}
   listConditionId= conditionId.split(",")
   for (var i=0; i <  (listConditionId.length); i++) 
   {
       extra = listConditionId[i].split("=")
       if (extra.length > 1)
       {
          if (extra[0] =='labelmsgid')
          {
              django.jQuery('#' + extra[1]).text('');
              id_to_display_result =  extra[1]
          }
          else
          {
              datasend[extra[0]]= extra[1]
          }
       }
       else
       {
          datasend[listConditionId[i] ]=  django.jQuery('#' + listConditionId[i]).val();
        }
   }

   datasend['todo'] = 'update';                                    
   console.log(datasend)                                            
   fullUrl = urlupdatecondition;
   callajax(fullUrl, datasend,id_to_display_result)                                 
}
                                             
function updatecoefficient(coeffTags)
{
   var listParams= []
   datasend ={}
   listCoeffTags = coeffTags.split(",")
   for (var i=0; i <  (listCoeffTags.length); i++) 
   {
       extra = listCoeffTags[i].split("=")
       if (extra.length > 1)
       {
          if (extra[0] =='idupdatemessage_id')
          {
              django.jQuery('#' + extra[1]).text('');
              id_to_display_result =  extra[1]
          }
          else
          {
              datasend[extra[0]]= extra[1].replace(/\s/g, '');
           }

       }
       else
       {
          datasend[listCoeffTags[i] ]=  parseFloat(django.jQuery('#' + listCoeffTags[i]).val());
        }
   }

   datasend['todo'] = 'update';                                         
   fullUrl = urlupdatecoefficients;
   callajax(fullUrl, datasend,id_to_display_result)
   
                                                   
 }


var currenthtmljs_id = null
var tableinputs_id =null
var  currenthtmljs_content = null
var propertyjq_content = null
var propertyjq_id = null
function updatecoefficientv2(parameters)
{
   var listParams= []
   datasend ={}
   listparameters = parameters.split(",")
   
   
   if (currenthtmljs_id == null)
	 {
	    currenthtmljs_id = listparameters[0]
   		tableinputs_id = listparameters[1]
	    propertyjq_id =  listparameters[2]
	    propertyjq_content = django.jQuery('#id_' + propertyjq_id).html()
	 }
   else if (currenthtmljs_id != listparameters[0])
    {	   
	   htmltablejq = django.jQuery('#id_' + currenthtmljs_id).html()
	   htmlinputsjq = window[tableinputs_id] 
	   
	   currenthtmljs_id = listparameters[0]
	   tableinputs_id = listparameters[1]
	   
	   if (propertyjq_id == listparameters[2])
		{
		   		//propertyjq_content
		}   
		else
		{
			propertyjq_id =  listparameters[2]
			propertyjq_content = django.jQuery('#id_' + propertyjq_id).html()
		}
    }
 
   coeffiparameterindexinit=4
   coeffiparameterindexend=listparameters.length-1
   todo=listparameters[coeffiparameterindexend]
   dimension =(( listparameters[3]).split("="))[1];
   if(todo == 'edit'){
	   currenthtmljs_content = django.jQuery('#id_' + currenthtmljs_id).html()
	   django.jQuery('#id_' + currenthtmljs_id).html('')
	   varjs=window[tableinputs_id] 
	   django.jQuery('#id_' + currenthtmljs_id).html(window[tableinputs_id] )
	   django.jQuery('#id_' + propertyjq_id).html(propertyjq_content);
	  }
   else
   {

	    for (var i=coeffiparameterindexinit; i <  coeffiparameterindexend; i++) 
	    {
	    	if (dimension == '2')
	    	{
	    		datasend[listparameters[i] ]=  django.jQuery('#' + listparameters[i].split("_")[1] ).val();
	    	}
	    	else
	    	{
	    		datasend[listparameters[i] ]=  django.jQuery('#' + listparameters[i] ).val();
	    	}
	    }
	    
	   var htmljs = django.jQuery('#id_' + currenthtmljs_id).html()
	   django.jQuery('#id_' + currenthtmljs_id).html(currenthtmljs_content)
	   

	   window[listparameters[1]] = htmljs

	   for (var i=coeffiparameterindexinit; i <  coeffiparameterindexend; i++) 
	    {
	    	django.jQuery('#' + listparameters[i] ).html(datasend[listparameters[i] ]);
	    }

	}

   datasend['todo'] = listparameters[coeffiparameterindexend];    
   datasend['dimension'] =dimension
   //console.log(datasend);
   fullUrl = urlupdatecoefficients;
   id_to_display_result = ''
   if(todo == 'update')
   {
	 callajax(fullUrl, datasend,id_to_display_result)
   }
   
    
                                                   
 }

                                         
function  callajax(url, datasend,id_to_display_result)
{
	var csrftoken = django.jQuery("[name=csrfmiddlewaretoken]").val();
	function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
                                               
       // start django.jQuery
	django.jQuery(function($) {
           // prepare ajax
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
           
           /*for (var i=0; i <  (listOfSelectMultiple.length); i++) 
           {
                if($('#' + listOfSelectMultiple[i]).val() != null)
                {
                   //console.log(listOfSelectMultiple[i]);
                   //console.log($('#' + listOfSelectMultiple[i]).val());
                   datasend[listOfSelectMultiple[i]] = $('#' + listOfSelectMultiple[i]).val()[0];
               }
           }*/
           
           console.log(datasend);
           // start ajax
            $.ajax({
            url : url,  
            type: "POST",  
            dataType: 'json',
                    data : datasend, 
                    success: function (data) 
                    {
		                 console.log("success"); // another sanity check                                      
		                /*html = django.jQuery('#' + id_to_display_result).html( );
		                if(django.jQuery('#' + id_to_display_result).html( ) == null) 
		                {
		                    django.jQuery('#' + id_to_display_result).text( data.result );  
		                }
		                else
		                {
		                    django.jQuery('#' + id_to_display_result).empty();
		                    django.jQuery('#' + id_to_display_result).html( data.result );
		                    django.jQuery('#' + id_to_display_result).show();
		                }*/
                    },
    
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
        
        //end ajax
     });
     // end django.jQuery

}