var keuzes = 0;
var keuzeArray=[];

function afspraakInit(){
	keuzes = $("#aantalAfspraken").val();
}

$(document).ready(function() {

	var updateHidden = function (){
		$("#checkedDocenten").val($("input:checkbox:checked[docentCheckBox |='true']").map(function(i,n) {
			return $(n).val();
		}).get().join(','));
	}
	
	$("input:checkbox").change(updateHidden);
	
	$("#select_all").change(function() {
		$("input:checkbox").attr('checked', $('#select_all').is(':checked')); 
		updateHidden();
	});
});

function selectCheckbox(clickedCell, dag, afspraakNummer, docentNaam, datum){
	aantalDagen = $("#"+docentNaam+"_aantalDagen").val();
	aantalTijden = $("#"+docentNaam+"_aantalTijden").val();
	index = $("#"+docentNaam+"_docentIndex").val();
	
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
}