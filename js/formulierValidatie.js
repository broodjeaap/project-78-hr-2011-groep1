function formulierCheck(form){
	
	var valid = true;
	var feedbackReport = "";
	
	if(valueCheck(form)){
		feedbackReport += "<li>"+"Niet all velden ingevuld" + "</li>";
		valid = false;
	}
	
	if(wachtwoordCompareCheck(form, 21, 22)){
		feedbackReport += "<li>"+ "wachtwoorden zijn niet gelijk" + "</li>";
		valid = false;
	}
	
	if(wachtwoordLengteCheck(form, 21)){
		feedbackReport += "<li>" + "wachtwoord minimaal 6 tekens" + "</li>";
		valid = false;
	}
	
	if(postcodeCheck(form)){
		feedbackReport += "<li>" + "Geen geldige postcode" + "</li>";
		valid = false;
	}
	
	if(emailCheck(form, 10)){
		feedbackReport += "<li>" + "Geen geldig e-mailadres" + "</li>";
		valid = false;
	}
	
	if(valid){
		submitForm(form);
		feedbackReport += "<li style='color:green;'>Leerling succesvol toegevoegd </li>";
	}
	document.getElementById("messages").innerHTML = feedbackReport;
	
}

function formulierCheckDocent(form){
	
	var valid = true;
	var feedbackReport = "";
	
	for(var i = 0; i < 8; i++){
		if(!(form.elements[i].value.trim())){
			feedbackReport += "<li>"+"Niet all velden ingevuld" + "</li>";
			valid = false;
			break;
		}
	}
	
	if(wachtwoordCompareCheck(form, 7, 8)){
		feedbackReport += "<li>"+ "wachtwoorden zijn niet gelijk" + "</li>";
		valid = false;
	}
	
	if(wachtwoordLengteCheck(form, 7)){
		feedbackReport += "<li>" + "wachtwoord minimaal 6 tekens" + "</li>";
		valid = false;
	}
	
	if(emailCheck(form, 4)){
		feedbackReport += "<li>" + "Geen geldig e-mailadres" + "</li>";
		valid = false;
	}
	
	if(valid){
		submitForm(form);
		feedbackReport += "<li style='color:green;'>Docent succesvol toegevoegd </li>";
	}
	document.getElementById("messages").innerHTML = feedbackReport;
	
}

function formulierCheckBeheerder(form){
	
	var valid = true;
	var feedbackReport = "";
	
	for(var i = 0; i < 5; i++){
		if(!(form.elements[i].value.trim())){
			feedbackReport += "<li>"+"Niet all velden ingevuld" + "</li>";
			valid = false;
			break;
		}
	}
	
	if(wachtwoordCompareCheck(form, 1, 2)){
		feedbackReport += "<li>"+ "wachtwoorden zijn niet gelijk" + "</li>";
		valid = false;
	}
	
	if(wachtwoordLengteCheck(form, 1)){
		feedbackReport += "<li>" + "wachtwoord minimaal 6 tekens" + "</li>";
		valid = false;
	}
	   
	if(checkIfIdExist()){
		feedbackReport += "<li>" + "Gebruikersnaam bestaat al" + "</li>";
		valid = false;
	}

	if(valid){
		submitForm(form);
		feedbackReport += "<li style='color:green;'>Beheerder succesvol toegevoegd </li>";
	}
	document.getElementById("messages").innerHTML = feedbackReport;
}

function formulierCheckVak(form){
	
	var valid = true;
	var feedbackReport = "";
	
	for(var i = 0; i < 3; i++){
		if(!(form.elements[i].value.trim())){
			feedbackReport += "<li>"+"Niet all velden ingevuld" + "</li>";
			valid = false;
			break;
		}
	}

	if(valid){
		submitForm(form);
		feedbackReport += "<li style='color:green;'>Vak succesvol toegevoegd </li>";
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

function wachtwoordCompareCheck(form, x, y){

	if(form.elements[x].value.localeCompare(form.elements[y].value) == 0){
		return false;
	}
	return true;
}

function wachtwoordLengteCheck(form, x){

	if(form.elements[x].value.length < 6){
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

function emailCheck(form, y){
	var x = new RegExp(".+@+");
	if(form.elements[y].value.match(x)){
		return false;
	}
	return true;
}

function checkIfIdExist(){
	var x = document.formforid.id.options.length;
	var y = document.inputform.gebruikersnaam.value;
	for(var i = 0; i < x ; i++){
		if(document.formforid.id.options[i].value.toLowerCase().localeCompare(y.toLowerCase()) == 0){
			return true;
		}
	}
	return false;
}

function submitForm(form){
	form.submit();
}

function deleteFormStudent(form){
	form.action = "/datastore/deletestudent";
	form.submit();
}

function updateFormStudent(form){
	form.action = "/datastore/updatestudent";
	formulierCheck(form);
}

function deleteFormDocent(form){
	form.action = "/datastore/deletestudent";
	form.submit();
}

function updateFormDocent(form){
	form.action = "/datastore/updatedocent";
	formulierCheckDocent(form);
}

function deleteFormBeheerder(form){
	form.action = "/datastore/deletebeheerder";
	form.submit();

}

function updateFormBeheerder(form){
	form.action = "/datastore/beheerderpost";
	formulierCheckBeheerder(form);
}

function deleteFormVak(form){
	form.action = "/datastore/deletevak";
	form.submit();

}

function updateFormVak(form){
	form.action = "/datastore/vakpost";
	formulierCheckVak(form);
}


