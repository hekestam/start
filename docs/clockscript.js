function startTime() {
    var d=new Date();
    var h=d.getHours();
    var m=d.getMinutes();
    var s=d.getSeconds();
    h = checkTime(h);
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('klocka').innerHTML = h + ":" + m + ":" + s;
}

function checkTime(i) {
    var j = i;
    if (i < 10) {
        j = "0" + i;
    }
    return j;
}

setInterval(function() {
    startTime();
}, 500);