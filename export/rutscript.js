function visa(id,text,over) {
	//https://bubblogging.wordpress.com/2013/01/30/js-mouse-position/
	var x;
	var y;
	id='masterruta';
	Element = document.getElementById(id);
    	x = window.event.clientX-125;		//window.event.clientX/window.event.x
	if (x<0) {x=0;}

	if (over) {y = window.innerHeight - window.event.y-document.documentElement.scrollTop+25;
			Element.style.top = '';} 
	else {y = window.event.clientY+document.documentElement.scrollTop+25;
			Element.style.bottom = '';}

    	xs = x.toString();
    	ys = y.toString();
	Element.innerHTML = text
	//Element.innerHTML = Element.clientHeight+text
    	Element.style.display = 'block';
    	if (over) {Element.style.bottom = ys+'px';}
	else {Element.style.top = ys+'px';}
    	Element.style.left = xs+'px';}
    
function ovisa() {
	id = 'masterruta';
	document.getElementById(id).style.display = 'none';
	}

function supervisa(e,text) {
	// http://www.quirksmode.org/js/events_properties.html
	var id = 'masterruta'
	var posx = 0;
	var posy = 0;
	var el = document.getElementById(id);
	if (!e) var e = window.event;

	if (e.pageX || e.pageY) {
		posx = e.pageX;
		posy = e.pageY;
	}
	else if (e.clientX || e.clientY) {
		posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
		posy = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
	}

	// posx and posy contain the mouse position relative to the document
	// Do something with this information

	el.style.display = 'block';
	el.style.top = '';
	el.style.bottom = '';

	el.style.top = posy+25+'px';
	// http://stackoverflow.com/questions/288699/get-the-position-of-a-div-span-tag
	var y = el.offsetTop+el.offsetHeight-document.body.scrollTop-window.innerHeight;
	el.innerHTML = text;

	if (y>-15) {
	el.style.top= '';
	el.style.bottom = window.innerHeight - posy+15+'px';
	}

	if (posx<125) {posx=125;}
	if (posx>window.innerWidth-147) {posx = window.innerWidth-147;}
	el.style.left = posx-125+'px';
}
