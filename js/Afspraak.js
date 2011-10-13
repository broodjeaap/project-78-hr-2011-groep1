var aantalDagen = 0;
var aantalTijden = 0;
var keuzes = 0;

function load(){
	aantalDagen = parseInt(document.getElementById("aantalDagen").value);
	aantalTijden = parseInt(document.getElementById("aantalTijden").value);
}

function selectCheckbox(checkbox, dag, afspraakNummer, docentNaam){
	if(checkbox.checked){
		checkbox.parentNode.bgColor = "#0000FF";
		for(dagloop = 0;dagloop < aantalDagen;++dagloop){
			for(tijd = 0;tijd < aantalTijden;++tijd){
				var cb = document.getElementById(docentNaam+"_"+dagloop+"_"+tijd);
				cb.disabled = true;
			}
		}
		checkbox.disabled = false;
		keuzes++;
	} else {
		checkbox.parentNode.bgColor = "#00FF00";
		for(dagloop = 0;dagloop < aantalDagen;++dagloop){
			for(tijd = 0;tijd < aantalTijden;++tijd){
				var cb = document.getElementById(docentNaam+"_"+dagloop+"_"+tijd);
				cb.disabled = false;
			}
		}
		keuzes--;
	}
}