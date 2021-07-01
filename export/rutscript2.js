function visa(id,over,text) {
	//https://bubblogging.wordpress.com/2013/01/30/js-mouse-position/
	var x;
	var y;
	id='masterruta';
	Element = document.getElementById(id);
	Element.innerHTML = text;
	over=false;
    	x = window.event.x-125;		//window.event.clientX/window.event.x
	y = window.event.y+document.documentElement.scrollTop+25;
	Element.style.bottom = '';
	Element.style.top = y.toString()+'px';
	var top = Element.style.top;
	top = top.slice(0,top.length-2);
	//Element.innerHTML='';
	nummer = (Number(top)+Number(Element.scrollHeight))
	Element.innerHTML = text;

	if (nummer>740) {
		y = window.innerHeight - window.event.y-document.documentElement.scrollTop+25;
		Element.style.top = '';
		Element.style.bottom = y.toString()+'px';}

    	xs = x.toString();
    	ys = y.toString();

    	Element.style.left = xs+'px';
	Element.style.display = 'block';
	}

function ovisa(id) {
	id = 'masterruta';
	document.getElementById(id).style.display = 'none';
	}