function init(){
    ws = new WebSocket("ws://" + location.hostname + ":8000");
    ws.onopen = function() {
        ws.send('hi');
    }
    ws.onmessage = function(e) {
//        document.getElementById("holder").innerHTML += '<p>'+e.data+'</p>';
    }
}
