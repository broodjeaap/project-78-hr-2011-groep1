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