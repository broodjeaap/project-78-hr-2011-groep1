var keuzes = 0;

function selectCheckbox(checkbox, dag, afspraakNummer, docentNaam, datum){
	aantalDagen = parseInt(document.getElementById(docentNaam+"_aantalDagen").value);
	aantalTijden = parseInt(document.getElementById(docentNaam+"_aantalTijden").value);
	
	if(checkbox.checked){
		for(dagloop = 0;dagloop < aantalDagen;++dagloop){
			for(tijd = 0;tijd < aantalTijden;++tijd){
				var cb = document.getElementById(docentNaam+"_"+dagloop+"_"+tijd);
				if(cb != null){
					cb.disabled = true;
					cb.parentNode.bgColor = "#00FE00";
				}
			}
		}
		document.getElementById(docentNaam+"_afspraak").value = datum+"_"+afspraakNummer;
		checkbox.disabled = false;
		checkbox.parentNode.bgColor = "#0000FF";
		++keuzes;
		if(keuzes >= 3){
			disableAllCheckbox();
		}
	} else {
		for(dagloop = 0;dagloop < aantalDagen;++dagloop){
			for(tijd = 0;tijd < aantalTijden;++tijd){
				var cb = document.getElementById(docentNaam+"_"+dagloop+"_"+tijd);
				if(cb != null){
					cb.disabled = false;
					cb.parentNode.bgColor = "#00FF00";
				}
			}
		}
		document.getElementById(docentNaam+"_afspraak").value = "";
		--keuzes;
		if(keuzes < 3){
			enableAllCheckbox();
		}
		
	}
}

function disableAllCheckbox(){
	boxes = document.getElementsByName("checkbox");
	for(a = 0;a < boxes.length;++a){
		if(!boxes[a].checked){
			boxes[a].disabled = true;
		}
	}
}

function enableAllCheckbox(){
	boxes = document.getElementsByName("checkbox");
	for(a = 0;a < boxes.length;++a){
		if(boxes[a].parentNode.bgColor != "#00FE00"){
			boxes[a].disabled = false;
		}
	}
}