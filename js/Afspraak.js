function selectCheckbox(checkbox, afspraakNummer, docentNaam){
	
	if(checkbox.checked){
		checkbox.parentNode.bgColor = "#0000FF";
		for(i = 0;i < 99;++i){
			if(afspraakNummer != i){
				var cb = document.getElementById(docentNaam+""+i);
				if(cb != null){
					cb.disabled = true;
				}	
			}
		}
	} else {
		checkbox.parentNode.bgColor = "#00FF00";
		for(i = 0;i < 99;++i){
			if(afspraakNummer != i){
				var cb = document.getElementById(docentNaam+""+i);
				if(cb != null){
					cb.disabled =false;
				}
			}
		}
	}
}