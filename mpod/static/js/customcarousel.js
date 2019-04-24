/* un ejemplo con jquery */

div = document.getElementById("myCarousel");
alert(div);
 
$(function(){

div = document.getElementById("myCarousel");

divs = document.getElementsByClassName("item");
console.log(divs);	

if (divs.length> 0) {
 
	for (var i=0; i < divs.length; i++)
	{
		currentDiv = divs[i]
		if (currentDiv.firstElementChild.tagName == 'IMG')
		{
			console.log(currentDiv.firstElementChild.src);
			var width = currentDiv.firstElementChild.clientWidth;
			var height = currentDiv.firstElementChild.clientHeight;
			console.log(width); 	
			console.log(height); 	
		}
		
	}
}
 
/*console.log(div.parentNode.className);
console.log(div.parentNode.clientHeight);
console.log(div.parentNode.clientWidth);*/
//alert(div.parentNode.clientWidth);
div.parentNode.style.width = 589 + 'px' ; 	
//alert(div.parentNode.clientWidth); 
 
	

});
