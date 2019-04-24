/* un ejemplo con jquery */

 //id_properties_from
/*
function towclick(param)
{
 
	   console.log(  param );
	
}

 
 function oneclick(param)
{
  
 
	    console.log( param.id );
	
}*/


	
 
divs = document.getElementsByClassName("selector-chosen");
console.log(divs); 
console.log(divs.length);

console.log($( "select" ));

(function($) {
		$(document).ready(function(){

				/*$( "select" ).each(function( index ) {
					console.log( index + ": " + $( this ));
					
					  $( this ).bind('click', function (e) {
							    console.log(this.value);
							    e.stopPropagation(); 
							});
				});*/
				
				
				  /*  $( "select[name='properties']" ).click(function(e){
				    	console.log(this.value);
				    
				
				    });*/
				    
				   /* $( "select[name*='properties']").click(function(e){
				    	console.log(this.value);
				    });*/
    
				//console.log(document.getElementById("id_properties"));
				
				//console.log(document.getElementsByClassName("selector-chosen"));
			   
				

	        });
	        
	        
 
	        
          
 
})(django.jQuery);



 

