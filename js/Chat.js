var timout = 100;
var timerId = 0;

$.ajaxSetup ({  
	cache: false  
});  

function send(){
	if($("#chatTextBox").val() != ""){
		$("#chatSpace").load("/chatajaxhandler?type=post&id="+$("#id").val()+"&room="+$("#room").val()+"&message="+prepare($("#chatTextBox").val()),scrollDown);
		$("#chatTextBox").val("");
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
	$("#chatSpace").load("/chatajaxhandler?type=get&room="+$("#room").val()+"&id="+$("#id").val(),scrollDown);
	timout--;
	if(timout <= 0){
		clearInterval(timerID);
		alert("Idle for to long, please refresh page");
	}
}

function scrollDown(){
	$("#chatSpace").scrollTop($("#chatSpace")[0].scrollHeight);
}

function getUsers(){
	$("#userSpace").load("/chatajaxhandler?type=users&room="+$("#room").val()+"&id="+$("#id").val());
}

function updateChat(){
	getMessages();
	getUsers();
}

$(document).ready(function() {
	$("#userSpace").load("/chatajaxhandler?type=join&room="+$("#room").val()+"&id="+$("#id").val());
	getMessages();
	getUsers();
	timerID = setInterval("updateChat()",5000);
});

$(window).unload(function() {
	$("#userSpace").load("/chatajaxhandler?type=quit&room="+$("#room").val()+"&id="+$("#id").val());
});

$(document).keypress(function(e) {
    if(e.keyCode == 13) {
        send();
		$("#chatTextBox").val("");
    }
});
