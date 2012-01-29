var timeout;

function textboxchange(query){
	if(timeout != null){
		clearTimeout(timeout);
	}
	timeout = setTimeout("getleerlingen('"+query+"')",1000);
}

function getleerlingen(query){
	$("#leerlingenOutputDiv").load("/selector/leerlingget?q="+query);
}

function addleerling(query){
	$.ajax({
		type: "POST",
		url: "/selector/leerlingadd",
		data: "id="+query,
		succes: function(){
			alert("return");
		}
	});
}