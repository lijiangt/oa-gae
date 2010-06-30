var $j=jQuery.noConflict();
$j(document).ready(function() {
   $j("#listBody tbody tr").hover(function(){$j(this).addClass("over");},function(){$j(this).removeClass("over");});
   $j("#listBody tbody tr:even").addClass("alt");
});