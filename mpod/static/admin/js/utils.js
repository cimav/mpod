 
var $ = django.jQuery;
loaded = false;
divs = null;
length = 0;
var divformrowfield= null;
var fields=[]
var fieldsnames=[]
 

function updatecoefficient(param,prop_id,datafile_id)
{
        //console.log(param);
	    item=  param.split("&");
	    datasend = {};
	    for(var i=0; i < item.length; i++)
	    {
	    	coeff = item[i].split("=");
	    	n = 'coeff_' + coeff[0];
	    	datasend[coeff[0]] = $('input[name=' + n +']').val();
	    }
	     
	    datasend['datafile_id'] = datafile_id;


	    
	      $.ajax({
				url:   'updatecoefficient/' + prop_id,
				type: "POST",
				dataType: "json",
				data: datasend,
				success: function (data) {
						//$( "#" + idtd ).append(data.html);
						
					      /*$('#' +e.data.id).empty();
					      $('#' +e.data.id).append(data.html);

					 
					      $('#' +e.data.id).show();*/

					},
					error: function (data) {
			       		if(data.status == 500)
			       			alert("Resource not found");
			          	 },
			});

	
}


$(function(){
 

 for (i = 0; i < $('input[type=hidden]').length; i++) 
  {
         fields[i] = $('input[type=hidden]')[i].value;
         fieldsnames[i] = $('input[type=hidden]')[i].name
         
         if($('input[type=hidden]')[i].id != '')
         {
	         labels = 'label[for=' +  $('input[type=hidden]')[i].id + '] ,' + 'input#' + $('input[type=hidden]')[i].id ;
	         $(labels).hide();
	     }
   }
 
 
 $( "select" ).change(function () {
    var str = "";
    $( "select option:selected" ).each(function() {
      str += $( this ).text() + " ";
    });

 
  }).change();
 

	 
	 $(document).mousemove(function (event ) {
		     divs = document.getElementsByClassName("selector-chosen");
		     datafile_tempid = ""
		     if(!loaded)
		     {
		          
			      for (i = 0; i < divs.length; i++) 
			       {
			    		  for (j = 0; j < divs[i].childNodes.length;j++) 
					       {
					    	  if (divs[i].childNodes[j].className=='filtered')
					    	  {
					    		 for(x=0; x< fields.length; x++)
								 {
								      field = "id_" + fields[x] + "_to"
								      divformrowfield = "div.form-row.field-" + fields[x]
								      iddivformrowfield = "iddivformrowfield" + fields[x]
								      
								      
							         if (  fieldsnames[x] =="datafile_tempid")
					    	          {
					    	        	  datafile_tempid= fields[x];
					    	          }
								    
					    	         
								    	        

								       if(divs[i].childNodes[j].id == field)
								       {   
								  
								    	       $(divformrowfield).append('<div id="' + iddivformrowfield+ '" style="display:none;" >' +
								    	   													      ' </div>');

								    		   url = "showmatrix";
								    	      
								    		  
								    	       $( divs[i].childNodes[j]).bind('click',{id: iddivformrowfield,url:url, datafile_id:datafile_tempid }, function (e ) {
								    	       
											      datasend = {'datafile_id':e.data.datafile_id}
											       
  
											      $.ajax({
														url:  e.data.url + '/' + this.value,
														type: "POST",
														dataType: "json",
														data: datasend,
														success: function (data) {
															      $('#' +e.data.id).empty();
															      $('#' +e.data.id).append(data.html);
															      $('#' +e.data.id).show();

															},
															error: function (data) {
													       		if(data.status == 500)
													       			alert("Resource not found");
													          	 },
													});

											            e.stopPropagation(); 
							       		          });
			
								       }
								 }
					    	}
					     }
					        
					        loaded = true;
					 }
					 
			}
	    
	  }).mousemove();		 

 
 });





 

