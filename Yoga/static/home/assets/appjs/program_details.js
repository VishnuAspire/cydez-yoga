
$(".languageBox").click(function(){
	$(".languageList").toggleClass("active");
});

$(".moreDetails").click(function(){
	$(this).closest(".videoInfo").find(".infoMoreDetails").slideToggle();
});
