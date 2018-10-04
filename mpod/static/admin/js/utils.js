/* un ejemplo con jquery */

 //id_properties_from
function getProperty(param)
{
 // alert(param.id);
 
  //alert('#'+param.id);
	collection = param.selectedOptions;
	 output = "";
	for (let i=0; i<collection.length; i++) {
	    
	   // output += collection[i].label ;
	    console.log(  collection[i].label );
 
	  }
   
	//win=window.open('','Edit Window',  'directories=no,titlebar=no,toolbar=no,location=no,status=no,menubar=no,height=200,width=400,resizable=no,scrollbars=no');
	 
	/*win.document.body.innerHTML ='<div class="modal-dialog">' +															
															          '<button type="button" class="btn btn-default" data-dismiss="modal" onclick="window.close();">Close</button>' +															
															          '</div>';*/
	
 
 
 /*
	win.document.write('<div class="modal-dialog">' +		
			'<a title="Remove" href="' +js +'" id="id_properties_remove_link" class="selector-remove">Remove</a>' +
	          '<button type="button" class="btn btn-default" data-dismiss="modal" onclick="window.close();">Close</button>' +															
	          '</div>');

	
	win.focus();*/
  
	

 
}

//id_properties_to

