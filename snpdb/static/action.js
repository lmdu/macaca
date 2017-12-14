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
$('.ui.feature a').click(function(e){
	e.preventDefault();
	$('#feature').val($(this).data('num'));
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


});


