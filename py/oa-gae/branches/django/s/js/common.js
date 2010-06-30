var bupticetCommon = {
	encode:function(str){
		var enStr="~!*()_-.'";
		var strTemp=encodeURIComponent(str);
		var strEncoded="";
		for(var i=0;i<strTemp.length;i++){
			if(enStr.indexOf(strTemp.charAt(i))!=-1){
				strEncoded+="%"+strTemp.charCodeAt(i).toString(16).toUpperCase();
			}else{
				strEncoded+=strTemp.charAt(i);
			}
		}
		return strEncoded;
	},
	deleteConfirm:function(url,errorInfo){
		var msg = errorInfo||bupticetLang.deleteConfirm;
		if(confirm(msg)){
			location.href=url;
		}
	},
	deleteConfirmUseForm:function(url,errorInfo){
		var msg = errorInfo||bupticetLang.deleteConfirm;
		if(confirm(msg)){
			var f = document.forms['deleteForm'];
			f.action=url;
			f.submit();
		}
	},
	operateConfirm:function(url,errorInfo){
		var msg = errorInfo||bupticetLang.operateConfirm;
		if(confirm(msg)){
			location.href=url;
		}
	},
	operateConfirmNotBack:function(url,errorInfo){
		var msg = errorInfo||bupticetLang.operateConfirmNotBack;
		if(confirm(msg)){
			location.href=url;
		}
	},
	cancelConfirm:function(i,errorInfo){
		var msg = errorInfo||bupticetLang.cancelConfirm;
		if(confirm(msg)){
		try{
			this.emptyOnUnload();
			history.go(i);
		}catch(e){}
		}
	},
	appendFormReset:function(){
	},
	resetConfirm:function(form,errorInfo){
		var msg = errorInfo||bupticetLang.resetConfirm;
		if(confirm(msg)){
			form.reset();
			this.appendFormReset();
		}
	},	
	goOptionValueUrl:function(which){
		var links=which.options[which.selectedIndex].value
		if(links!=""){
			location.href=links
		}
	},
	emptyOnUnload:function(){
		window.onbeforeunload = function(){};
	},
	// Trim whitespace from left and right sides of s.
	trim:function(s){
		if(s==null){return "";}
		if(typeof(s)!="string"){return s;}
		return s.replace( /^\s*/, "" ).replace( /\s*$/, "" );
	},
	// replace the \r\n with \n
	handleNewlineChar:function(str) {
		str = str.replace(/\r\n/g, "\n");
		return str.replace(/\r/g, "\n");
		//return str.replace(/\n+/g, "\n");
	},
	decode:function(str){
		return decodeURIComponent(str);
	},
	customEncode:function(url){
		return this.encode(url).replace(/%/g,"_");
	},
	customDecode:function(str){
		return this.decode(str.replace(/_/g,"%"));
	},
	enableDisabled:function(o){
		if(o.disabled){
			o.disabled = false;
		}
	},
	disableSubmit:function(submitId,resetId,cancelId,errorInfo){
		var id1 = submitId||"formSubmit";
		var id2 = resetId||"formReset";
		var id3 = cancelId||"formCancel";
		var msg = errorInfo||bupticetLang.submitting;
		var node1 = document.getElementById(id1);
		var node2 = document.getElementById(id2); 
		var node3 = document.getElementById(id3);
		if(node1){  
			node1.disabled = "disabled";
			node1.value = msg;
		}
		if(node2){
			node2.disabled = "disabled";
		}
		if(node3){
			node3.disabled = "disabled";
		}
	}
}

var bupticetForm = {
		htmlSelect:{
			//返回结构：Array,元素属性index：位置，entity：option对象
			getSelected:function(targetObj){
				var selected = new Array();
				var count = targetObj.length;
		  	for (var x=0; x < count ;x++) {
		  	   if( targetObj.options[x].selected ) {
		   				var obj = new Object();
		   				obj.index = x;
		   				obj.entity = targetObj.options[x];
		   				selected[selected.length] = obj;
		   				}
		    	}
		    return selected;
			},
			getDomSelected:function(domId){
				return getSelected(document.getElementById(domId));
			},
			deleteSelectElements:function(targetObj){
				var count = targetObj.length;
		  	for (var x=count; x > 0 ;x--) {
		  	   if( targetObj.options[x-1].selected ) {
		   				targetObj.options[x-1] = null;
		   				count--;
		   				}
		    	}
			},
			deleteDomSelectElements:function(domId){
				this.deleteSelectElements(document.getElementById(domId));
			},
			deleteAllElements:function(targetObj){
			  var count = targetObj.length;
				for (var x=count; x > 0 ;x--) {
					targetObj.options[x-1] = null;
					count--;
		    		}
			},
			deleteDomAllElements:function(domId){
				this.deleteAllElements(document.getElementById(domId));
			},
			deleteElement:function(targetObj,value){
				var o = targetObj.options;
				var count = targetObj.length;
				for(var i = 0;i<o.length;i++){
					if(o[i].value == value){
						o[i] = null;
						count--;
						return true;
					}
				}
				return false;
			},
			deleteDomElement:function(domId,value){
				return this.deleteElement(document.getElementById(domId),value);
			},
			selectAllOptions:function(targetObj){
				for ( var i=0;i<targetObj.length;i++){
					targetObj.options[i].selected = true;
				}
			},
			selectDomAllOptions:function(domId){
				this.selectAllOptions(document.getElementById(domId));
			},
			addOption:function(targetObj,value,display,selected){
				var o = targetObj.options;
				for(var i = 0;i<o.length;i++){
					if(o[i].value == value){
						return false;
					}
				}
				var newOption = new Option(display, value, 0, 0);
				targetObj.options[o.length] = newOption;
				if(selected){
					newOption.selected = true;
				}
				return true;
			},
			addDomOption:function(domId,value,display,selected){
				return this.addOption(document.getElementById(domId),value,display,selected);
			},
			getCount:function(targetObj){
				return targetObj.length;
			},
			getDomCount:function(domId){
				return getCount(document.getElementById(domId));
			},
			moveOptions:function(src,target,moveAll){
				var o = src.options;
				if(moveAll){
					for(var i = 0;i<o.length;i++){
						this.addOption(target,o[i].value,o[i].text,true);
					}
					this.deleteAllElements(src);
				}else{
					for(var i = 0;i<o.length;i++){
						if(o[i].selected){
							this.addOption(target,o.value,o.text,true);
							this.deleteElement(src,o.value);
						}
					}				
				}
			},
			moveDomOptions:function(srcDomId,targetDomId,moveAll){
				this.moveOptions(document.getElementById(srcDomId),document.getElementById(targetDomId),moveAll);
			},
	    upOrDownSelectedOption:function(src,down,thorough){
				var selected = this.getSelected(src);
				if(selected.length==0){
					alert('请至少选择一个元素！');
					return;
				}
				for(var i = 1;i<selected.length;i++){
					if(selected[i].index != selected[i-1].index+1){
						alert('请一个元素或者选择多个连续的的元素！');
						return;
					}
				}
				var newOptions = new Array();
				var length = src.length;
				if(down){
					if(selected[selected.length].index==src.length){
						alert('您所选择的元素已经在最底端了，不能再往下移动了！');
						return;
					}
					if(thorough){
						if(selected[0].index!=0){
							for(var i = 0;i<selected[0].index-1;i++){
								newOption[newOption.length] = src.options[i];
							}
						}
						for(var i = selected[selected.length].index+1;i<length;i++){
							newOption[newOption.length] = src.options[i];
						}
						for(var i = 0;i<selected.length;i++){
							newOption[newOption.length] = selected[i].entity;
						}
					}else{
						if(selected[0].index!=0){
							for(var i = 0;i<selected[0].index-1;i++){
								newOption[newOption.length] = src.options[i];
							}
						}
						newOption[newOption.length] = src.options[selected[selected.length].index+1];
						for(var i = 0;i<selected.length;i++){
							newOption[newOption.length] = selected[i].entity;
						}
						if(length>selected[selected.length].index+1){
							for(var i = selected[selected.length].index+2;i<length;i++){
								newOption[newOption.length] = src.options[i];
							}
						}
					}
				}else{
					if(selected[0].index==0){
						alert('您所选择的元素已经在最顶端了，不能再往上移动了！');
						return;
					}
					if(thorough){
						for(var i = 0;i<selected.length;i++){
							newOption[newOption.length] = selected[i].entity;
						}
						if(selected[0].index!=0){
							for(var i = 0;i<selected[0].index-1;i++){
								newOption[newOption.length] = src.options[i];
							}
						}
						for(var i = selected[selected.length].index+1;i<length;i++){
							newOption[newOption.length] = src.options[i];
						}
					}else{
						if(selected[0].index-2>0){
							for(var i = 0;i<selected[0].index-2;i++){
								newOption[newOption.length] = src.options[i];
							}
						}
						for(var i = 0;i<selected.length;i++){
							newOption[newOption.length] = selected[i].entity;
						}
						newOption[newOption.length] = src.options[selected[0].index-1];
						if(length>selected[selected.length].index){
							for(var i = selected[selected.length].index+1;i<length;i++){
								newOption[newOption.length] = src.options[i];
							}
						}
					}
				}
				src.options = newOptions;
	        },
	    downSelectedOptions:function(src,thorough){
	        upOrDownSelectedOption(src,true,thorough);
	        },
	    downDomSelectedOptions:function(srcDomId,thorough){
	        downSelectedOptions(document.getElementById(srcDomId),thorough);
	        },
	    upSelectOptions:function(src,thorough){
	        upOrDownSelectedOption(src,false,thorough);
	    	},
	    upDomSelectOptions:function(srcDomId,thorough){
	        upSelectedOptions(document.getElementById(srcDomId),thorough);
	        }
		},
		changeAllCheckbox:function(boxName){
				var allCheckboxs = document.getElementsByName(boxName);
				if(allCheckboxs[0].checked == false){
					for(var i=0;i<allCheckboxs.length;i++){
							allCheckboxs[i].checked = false; 
					}
				}else{
					for(var i=0;i<allCheckboxs.length;i++){
							allCheckboxs[i].checked = true; 
					}
				}
		},
		doWhenCheckPass:function(o,elementName){
			var node = o.submit;
			if(elementName){
				node = o.elements[element]
			}
			node.value='处理中，请稍候...';
			node.disabled=true;
		}
	}

var bupticetDom= {
	$:function(id){
		return document.getElementById(id);
	},
	insertHtmlBefore:function( html, element ){
		if ( element.insertAdjacentHTML ){	// IE
			element.insertAdjacentHTML( 'beforeBegin', html ) ;
		}else{								// Gecko such as firefox and mozilla
			var oRange = document.createRange() ;
			oRange.setStartBefore( element ) ;
			var oFragment = oRange.createContextualFragment( html );
			element.parentNode.insertBefore( oFragment, element ) ;
		}
	}
}

var bupticetEvent ={
	attachBefore:function(src,event,fun){
		var oldFun = src[event];
		src[event] = function(){
			if(typeof fun == "function"){
				fun();
			}
			if(typeof oldFun == "function"){
				oldFun();
			}
		}
	},
	attachBeforeWithReturn:function(src,event,fun){
		var oldFun = src[event];
		src[event] = function(){
			if(typeof fun == "function"){
				var result = fun();
				if(typeof result!='undefined'){
					if(!result){
						return false;
					}
				}
			}
			if(typeof oldFun == "function"){
				return oldFun();
			}else{
				return true;
			}
		}
	},
	attachAfter:function(src,event,fun){
		var oldFun = src[event];
		src[event] = function(){
			if(typeof oldFun == "function"){
				oldFun();
			}
			if(typeof fun == "function"){
				fun();
			}
		}
	}
}