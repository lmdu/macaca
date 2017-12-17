$(document).ready(function(){

$('select.dropdown').dropdown();

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


});


