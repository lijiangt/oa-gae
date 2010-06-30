$(document).ready(function(){
	isIndex=document.getElementById("detail");
	if(isIndex){	
		$("#detail").html($("#s1").html());
	}
	$("#product #tab ul li#t1").addClass('s1');
	$("#product #tab ul li#t2").addClass('s2');
	$("#product #tab ul li#t3").addClass('s2');
	$("#product #tab ul li#t1 ").css('color','#000000');
	$("#product #tab ul li#t2 ").css('color','#FFFFFF');
	$("#product #tab ul li#t3 ").css('color','#FFFFFF');
	isList=document.getElementById("list");
	if(isList){
		$("#list table.courselist tbody tr:even").addClass("alt");
	}
});
function displaySubMenu(li) {
	 var seLevel=li.getElementsByTagName("ul")[0];
     var seLevelLength="";
     var titleLength=new Array();
     var maxValue=0;
    if(seLevel.hasChildNodes()){
        for(var i=0;i<seLevel.childNodes.length;i++){
           if(seLevel.childNodes[i].nodeName=="#text"){
    		  continue;
           }
        titleLength[i]=seLevel.childNodes[i].childNodes[0].childNodes[0].nodeValue.length;
         }
          maxValue=titleLength[1];
        for(var j=0;j<titleLength.length;j++){
    	       if(titleLength[j]>maxValue){
    	    	  maxValue=titleLength[j];
    	    	}
    	    }
        for(var k=0;k<seLevel.childNodes.length;k++){
               if(seLevel.childNodes[k].nodeName=="#text"){
        		  continue;
               }
             var widthValue = maxValue*15;
             seLevel.childNodes[k].style.width = widthValue + "px";
             seLevel.childNodes[k].childNodes[0].style.width = widthValue + "px";
           }
       }
            var subMenu = li.getElementsByTagName("ul")[0];
            subMenu.style.display = "block";
        }
function hideSubMenu(li) {
            var subMenu = li.getElementsByTagName("ul")[0];
            subMenu.style.display = "none";
}
function cd(p){
	  for(var i=1;i<4;i++){
		$("#product #tab ul li#t"+i).removeClass('s1');
		$("#product #tab ul li#t"+i).removeClass('s2');
		$("#product #tab ul li#t"+i).removeClass('s3');
		if(p==i){
			$("#product #tab ul li#t"+i).addClass('s1');
			$("#product #tab ul li#t"+i).css('color');
			$("#product #tab ul li#t"+i).css('color','#000000'); 
		}else{
			$("#product #tab ul li#t"+i).addClass('s2');
			$("#product #tab ul li#t"+i).css('color');
			$("#product #tab ul li#t"+i).css('color','#FFFFFF'); 
	    }
	}
	  $("#detail").html($("#s"+p).html());
 }
  function addBookmark(title,url) {
  if (window.sidebar) {
	window.sidebar.addPanel(title, url,"");
} else if( document.all ) {
	window.external.AddFavorite( url, title);
} else if( window.opera && window.print ) {
	return true;
}
}
function sethome(url){
	if (document.all){
        document.body.style.behavior='url(#default#homepage)';
  		document.body.setHomePage(url); 
    }else if (window.sidebar){
    	if(window.netscape){
        	try{  
            	netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");  
         	}catch (e){  
    			alert( "该操作被浏览器拒绝，如果想启用该功能，请在地址栏内输入 about:config,然后将项 signed.applets.codebase_principal_support 值该为true" );  
         	}
    	} 
    	var prefs = Components.classes['@mozilla.org/preferences-service;1'].getService(Components. interfaces.nsIPrefBranch);
    	prefs.setCharPref('browser.startup.homepage',url);
 	}
}