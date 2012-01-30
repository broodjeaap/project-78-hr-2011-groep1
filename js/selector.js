var leerlingtimeout;
var klastimeout;
var busy = false;

$(document).ready(function() {
	getSelection();
});

function textboxchange(query,type){
	if(type == "leerling"){
		if(leerlingtimeout != null){
			clearTimeout(leerlingtimeout);
		}
		leerlingtimeout = setTimeout("getleerlingen('"+query+"')",1000);
	} else if (type == "klas"){
		if(klastimeout != null){
			clearTimeout(klastimeout);
		}
		klastimeout = setTimeout("getklassen('"+query+"')",1000);
	}
}

function getleerlingen(query){
	$("#leerlingenOutputDiv").load("/selector/leerlingget?q="+query);
}

function getklassen(query){
	$("#klassenOutputDiv").load("/selector/klassenget?q="+query);
}

function getSelection(){
	$("#selectedOutputDiv").load("/selector/selection");
}

function addleerling(query){
	if(!busy){
		busy = true;
		$("#"+query+"image").attr("src","/images/Spin-arrows.gif");
		$("#"+query+"row").attr("onclick","");
		$.ajax({
			type: "POST",
			url: "/selector/leerlingadd",
			data: "id="+query
		}).done( function(html){
			getSelection();
			$("#"+query+"image").attr("src","/images/greencheck.png");
			$("#"+query+"row").attr("onclick","removeleerling(\""+query+"\")");
			busy = false;
		});
	}
}

function removeleerling(query){
	if(!busy){
		busy = true;
		$("#"+query+"image").attr("src","/images/Spin-arrows.gif");
		$("#"+query+"row").attr("onclick","");
		$.ajax({
			type: "POST",
			url: "/selector/leerlingremove",
			data: "id="+query
		}).done( function(html){
			getSelection();
			getklassen($("#klasIDText").val());
			$("#"+query+"image").attr("src","/images/redcross.png");
			$("#"+query+"row").attr("onclick","addleerling(\""+query+"\")");
			busy = false;
		});
	}
}

function addklas(query){
	if(!busy){
		busy = true;
		$("#"+query+"image").attr("src","/images/Spin-arrows.gif");
		$("#"+query+"row").attr("onclick","");
		$.ajax({
			type: "POST",
			url: "/selector/klasadd",
			data: "id="+query
		}).done( function(html){
			getSelection();
			getleerlingen($("#leerlingIDText").val());
			$("#"+query+"image").attr("src","/images/greencheck.png");
			$("#"+query+"row").attr("onclick","removeklas(\""+query+"\")");
			busy = false;
		});
	}
}

function removeklas(query){
	if(!busy){
		busy = true;
		$("#"+query+"image").attr("src","/images/Spin-arrows.gif");
		$("#"+query+"row").attr("onclick","");
		$.ajax({
			type: "POST",
			url: "/selector/klasremove",
			data: "id="+query
		}).done( function(html){
			getSelection();
			getleerlingen($("#leerlingIDText").val());
			$("#"+query+"image").attr("src","/images/redcross.png");
			$("#"+query+"row").attr("onclick","addklas(\""+query+"\")");
			busy = false;
		});
	}
}
function clearselection(){
	$.ajax({
		type: "GET",
		url: "/selector/clear"
	}).done( function(html){
		getSelection();
		getleerlingen($("#leerlingIDText").val());
		getklassen($("#klasIDText").val());
		busy = false;
	});
}
