var timout = 100;
var timerId = 0;

$.ajaxSetup ({  
	cache: false  
});  

function send(){
	if($("#chatTextBox").val() != ""){
		$("#chatSpace").load("/chatajaxhandler?type=post&id="+$("#id").val()+"&room="+$("#room").val()+"&message="+prepare($("#chatTextBox").val()),scrollDown);
		timout = 100;
	}
	getMessages();
}

function prepare(str){
	while(str.indexOf(" ") != -1){
		str = str.replace(" ", "_");
	}
	return str;
}

function getMessages(){
	$("#chatSpace").load("/chatajaxhandler?type=get&room="+$("#room").val(),scrollDown);
	timout--;
	if(timout <= 0){
		clearInterval(timerID);
		alert("Idle for to long, please refresh page");
	}
}

function scrollDown(){
	$("#chatSpace").scrollTop($("#chatSpace")[0].scrollHeight);
}

$(document).ready(function() {
	getMessages();
	timerID = setInterval("getMessages()",5000);
});

$(document).keypress(function(e) {
    if(e.keyCode == 13) {
        send();
		$("#chatTextBox").val("");
    }
});
