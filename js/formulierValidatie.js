function formulierCheck(form){
	
	var valid = true;
	var feedbackReport = "";
	
	if(valueCheck(form)){
		feedbackReport += "<li>"+"Niet all velden ingevuld" + "</li>";
		valid = false;
	}
	
	if(wachtwoordCompareCheck(form)){
		feedbackReport += "<li>"+ "wachtwoorden zijn niet gelijk" + "</li>";
		valid = false;
	}
	
	if(wachtwoordLengteCheck(form)){
		feedbackReport += "<li>" + "wachtwoord minimaal 6 tekens" + "</li>";
		valid = false;
	}
	
	if(postcodeCheck(form)){
		feedbackReport += "<li>" + "Geen geldige postcode" + "</li>";
		valid = false;
	}
	
	if(emailCheck(form)){
		feedbackReport += "<li>" + "Geen geldig e-mailadres" + "</li>";
		valid = false;
	}
	
	if(valid){
		submitForm(form);
		feedbackReport += "<li style='color:green;'>Leerling succesvol toegevoegd </li>";
	}
	document.getElementById("messages").innerHTML = feedbackReport;
	
}

function valueCheck(form){
	for(var i = 0; i < (form.length-1); i++){
		if(!(form.elements[i].value.trim())){
			return true;
		}
		if(i==2 || i==15){
			i++;
		}
	}
	return false;	
}

function wachtwoordCompareCheck(form){

	if(form.elements[21].value.localeCompare(form.elements[22].value) == 0){
		return false;
	}
	return true;
}

function wachtwoordLengteCheck(form){

	if(form.elements[21].value.length < 6){
		return true;
	}
	return false;
}

function postcodeCheck(form){
	var x = new RegExp("[1-9][0-9]{3}\\s?[a-z]{2}", "i");
	if(form.elements[8].value.match(x)){
		return false;
	}
	return true;
}

function emailCheck(form){
	var x = new RegExp(".+@+");
	if(form.elements[10].value.match(x)){
		return false;
	}
	return true;
}

function submitForm(form){
	form.submit();
}

function deleteForm(form){
	form.action = "/datastore/deletestudent";
	form.submit();


}

function updateForm(form){
	form.action = "/datastore/updatestudent";
	form.submit();
}
