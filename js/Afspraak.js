var keuzes = 0;
var keuzeArray=[];

function init(){
	keuzes = parseInt(document.getElementById("aantalAfspraken").value);
}

function selectCheckbox(clickedCell, dag, afspraakNummer, docentNaam, datum){
	aantalDagen = parseInt(document.getElementById(docentNaam+"_aantalDagen").value);
	aantalTijden = parseInt(document.getElementById(docentNaam+"_aantalTijden").value);
	index = parseInt(document.getElementById(docentNaam+"_docentIndex").value);
	
	if(keuzeArray[index] == clickedCell){
		keuzeArray[index].bgColor  = "#00FF00";
		keuzeArray[index]  = null;
		document.getElementById(docentNaam+"_afspraak").value = "";
		keuzes--;
		return;
	}
	if (keuzeArray[index] == null) {
		if(keuzes >= 3){
			alert("U heeft al 3 afspraken gemaakt");
			return;
		}
		keuzeArray[index] = clickedCell;
		keuzeArray[index].bgColor = "#0000FF";
		document.getElementById(docentNaam+"_afspraak").value = datum+"_"+afspraakNummer;
		keuzes++;
		return;
	} else {
		keuzeArray[index].bgColor = "#00FF00";
		keuzeArray[index] = clickedCell;
		keuzeArray[index].bgColor = "#0000FF";
		document.getElementById(docentNaam+"_afspraak").value = datum+"_"+afspraakNummer;
		return;
	}
	
	
	
	/*
	if(clickedCell.bgColor == "#00FF00"){

		for(dagloop = 0;dagloop < aantalDagen;++dagloop){
			for(tijd = 0;tijd < aantalTijden;++tijd){
				var cell = document.getElementById(docentNaam+"_"+dagloop+"_"+tijd);
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
	*/
}

function arraySum(array){
	sum = 0;
	for(var a = 0;a < array.length;++a){
		sum += array[a];
	}
	return sum;
}