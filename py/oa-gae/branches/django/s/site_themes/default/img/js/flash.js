var imgWidth=978;              //图片宽
var imgHeight=175;             //图片高
var textFromHeight=0;         //焦点字框高度 (单位为px)
var buttonLineOn="#f60";           //button下划线on的颜色
var buttonLineOff="#000";          //button下划线off的颜色
var TimeOut=3000;              //每张图切换时间 (单位毫秒);
var canChange=true;
var theTimer;
var count=0;
var playingNo=0;
var preI=[];
function changeimg(n){
	 window.clearInterval(theTimer);
	 nextAd(n);
}
function goUrl(){
	window.open(imgArr[playingNo].split('|')[2],'_blank');
}
function imgLink(object){
	var str1=object.src;
    var index=str1.indexOf('//');
    var str2=str1.substring(index+2);
    var index2=str2.indexOf('/');
    var str3=str2.substring(index2,str1.length);
     if(str3==imgArr[0].split('|')[1]||str3==imgArr[1].split('|')[1]){
    	 window.open("/virexp",'_blank');
	 }else if(str3==imgArr[2].split('|')[1]){
		 window.open("/prepare_login",'_blank');
	 }else{
		 window.open("http://sl.bupticet.com",'_blank');
	 }
} 
function nextAd(skipToNo){
	   if (canChange == true){//alert(count);return;
		 var playingNoPre=playingNo;
		 var imgObj=GetObj('imgInit');
		 if(playingNo>=count-1)playingNo=0;else playingNo++ ;
		 if(typeof(skipToNo)!=='undefined'){playingNo=skipToNo;}
		 if(document.all){
			imgObj.filters.revealTrans.Transition=23;
			imgObj.filters.revealTrans.apply();
			imgObj.filters.revealTrans.play();
		 }
		 imgObj.src=imgArr[playingNo].split('|')[1];
		 imgObj.alt=imgArr[playingNo].split('|')[0];
		 GetObj('link'+playingNo).style.background=buttonLineOn;
		 if(playingNoPre!=playingNo)GetObj('link'+playingNoPre).style.background=buttonLineOff;		 
		 theTimer=setTimeout("nextAd()", TimeOut);
	}else {
		 theTimer=setTimeout("nextAd()", TimeOut);
	}

}//结束ie function nextAd()
function indexBarInit(){
	count=imgArr.length;
	
	//for(var j=0;j<imgArr.length;j++)alert(j+":"+imgArr[j]);
	//焦点字框高度样式表 开始
	document.write('<style type="text/css">');
	document.write('#focuseFrom{width:'+(imgWidth+2)+';margin: 0px; padding:0px;height:'+(imgHeight+textFromHeight)+'px; overflow:hidden;}');
	document.write('#txtFrom{height:'+textFromHeight+'px;line-height:'+textFromHeight+'px;width:'+imgWidth+'px;overflow:hide;}');
	document.write('#imgTitle{width:'+imgWidth+';top:-'+(textFromHeight+18)+'px;height:18px;}');
	document.write('</style>');	
	//焦点字框高度样式表 结束
	document.write('<div id="focuseFrom" >');//focuseFrom begin
	document.write('<a target=_self ><img onclick="javascript:imgLink(this);" onMouseOver="canChange=false;" onMouseOut="canChange=true;"  style="FILTER: revealTrans(duration=1,transition=5); cursor:pointer;"  width='+imgWidth+' height='+imgHeight+' border=0 vspace="0" id=imgInit class="imgClass"></a><br>');
	document.write('<div id="imgTitle">');//imgTitle
	document.write('<div id="imgTitle_down"> <a class="trans"></a>');
	//数字按钮代码开始
	 
	for(var i=0;i<count;i++){
		preI[i]=new Image;//预加载图片
		preI[i].src=(imgArr[i]).split('|')[2];
		document.write('<a onmouseover="changeimg('+i+');canChange=false;" onMouseOut="canChange=true;" id="link'+i+'" class="button" style="cursor:pointer;display:none;" title="'+(imgArr[i]).split('|')[0]+'"  onFocus="this.blur()">'+(imgArr[i]).split('|')[0]+'</a>');
	}
	//数字按钮代码结束
	document.write('</div>');
	document.write('</div>');//imgTitle end 
	document.write('</div>');//focuseFrom end 
	changeimg(0);
}
function GetObj(objName){
	if(document.getElementById){
		return eval('document.getElementById("' + objName + '")');
	}else{
		return eval('document.all.' + objName);
	}
}
function bindEventListener(target,type,handler){		
		if(window.document.all){
			target.attachEvent("on" + type, handler );
		}else{
			target.addEventListener(type, handler, false);
         }
		}
indexBarInit();


 
