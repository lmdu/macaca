$(document).ready(function(){
//$('select.dropdown').dropdown();
$('.ui.dropdown').dropdown();
//$('.ui.checkbox').checkbox();

$('#function-annotation .menu .item').tab();

//set chromosome link
$('.ui.chromosome a').click(function(e){
	e.preventDefault();
	$('#chromosome').val($(this).data('num'));
	$('#page').val('1');
	$('#snps-filter').submit();
});

//set individual link
$('.ui.individual a').click(function(e){
	e.preventDefault();
	$('#individual').val($(this).data('num'));
	$('#page').val('1');
	$('#snps-filter').submit();
});

//set samples link
$('.ui.samples a').click(function(e){
	e.preventDefault();

	var sid = $(this).data('num').toString();
	var ids = $("#snps-filter input[name='samples']").map(function(){
		return $(this).val();
	}).get();

	if(sid==='0'){
		$("#snps-filter input[name='samples']").remove();
	} else {
		if($.inArray(sid, ids) != -1){
			$("#snps-filter input[name='samples']").each(function(){
				if($(this).val() === sid){
					$(this).remove();
				}
			});
		} else {
			var input = document.createElement('input');
			input.type = 'hidden';
			input.id = 'samples';
			input.name = 'samples';
			input.value = sid;
			$("#snps-filter").append(input);
		}
	}
	$('#page').val('1');
	$('#snps-filter').submit();

});

//set feature link
$('.ui.features').click(function(e){
	e.preventDefault();
	$('#feature').val($(this).data('num'));
	$('#page').val('1');
	$('#snps-filter').submit();
});

//set genotype link
$('.ui.genotypes').click(function(e){
	e.preventDefault();
	$('#genotype').val($(this).data('num'));
	$('#page').val('1');
	$('#snps-filter').submit();
});

//set mutation link
$('.ui.mutations').click(function(e){
	e.preventDefault();
	$('#mutation').val($(this).data('num'));
	$('#feature').val('1');
	$('#page').val('1');
	$('#snps-filter').submit();
});

//set page number
$('.ui.pager a').click(function(e){
	e.preventDefault();
	$('#page').val($(this).data('num'));
	$('#snps-filter').submit();
});

$('.ui.numperpage').change(function(){
	$('#records').val($(this).dropdown('get value'));
	$('#snps-filter').submit();
});

//set group or species specific snps
$('.ui.group').click(function(e){
	e.preventDefault();
	$('#group').val($(this).data('num'));
	$('#species').val(-1);
	$('#snps-filter').submit();
});

$('.ui.species').click(function(e){
	e.preventDefault();
	$('#species').val($(this).data('num'));
	$('#group').val(-1);
	$('#snps-filter').submit();
});

//start search SNPs
$('i.search.icon').click(function(){
	var tag = $('#search-input').val();
	var chrange = /^chr\d{1,2}:\d+\-\d+$/
	var snpid = /MACSNP\d{12}/
	if(chrange.test(tag) || snpid.test(tag)){
		$('#search').submit();
	}else{
		$('.ui.small.modal').modal('show');
	}	
});

//checkbox
$('.ui.master.checkbox').checkbox({
	onChecked: function(){
		$('.ui.child.checkbox').checkbox('check');
	},
	onUnchecked: function(){
		$('.ui.child.checkbox').checkbox('uncheck');
	}
});

$('.ui.child.checkbox').checkbox({
	fireOnInit: true,
	onChange: function(){
		var allChecked = true;
		var allUnchecked = true;

		$('.ui.child.checkbox').each(function(){
			if($(this).checkbox('is checked')){
				allUnchecked = false;
			}else{
				allChecked = false;
			}
		});

		if(allChecked){
			$('.ui.master.checkbox').checkbox('set checked');
		}
		else if(allUnchecked){
			$('.ui.master.checkbox').checkbox('set unchecked');
		}
		else{
			$('.ui.master.checkbox').checkbox('set indeterminate')
		}
	}
});


});


