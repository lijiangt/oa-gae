//author  LJ-silver/lijt lijiangt@gmail.com
// 文本编辑器
//使用方法
//1,首先将原来的textarea的style设置为c，并给它设置一个id,最好以Id结尾,如contentTextAreaId
//2,然后再textarea上面添加一个链接<a href="JavaScript:bupticetEditor.toggle('contentTextAreaId');void(0);" id="'contentTextAreaButtonId'">可视化编辑器</a>
//3,在页面<head></head>中的script段中的window.onload的函数中添加bupticetEditor.create('contentTextAreaId','contentTextAreaButtonId');
//4,在表单的onsubmit=后添加bupticetEditor.processWhenSumbit();
//
//如果想使用其它html编辑器，请实现类似FckRichEditor的类。并修改RichTextArea.richEditor为该类的实例，然后修改inc/rich_editor.jsp中去掉fckeditor的js文件引用，添加其它html编辑器所需的js文件。
//更多高级用法请联系本人

//tinymce editor
function TinyMCEEditor(){}

TinyMCEEditor.prototype.canBackPlain = false;

TinyMCEEditor.prototype.getValue = function(textAreaId){
//TODO
}
TinyMCEEditor.prototype.setValue = function(textAreaId,value){
//TODO
}
FckRichEditor.prototype.exists = function(textAreaId){
//TODO
}
TinyMCEEditor.prototype.use = function(richObj,textAreaId,value,extConfig){
//TODO
}

TinyMCEEditor.prototype.unuse = function(textAreaId){
//TODO
}



//fckeditor impl
function FckRichEditor(){}
FckRichEditor.prototype.canBackPlain = true;
FckRichEditor.prototype.getValue = function(textAreaId){
	return FCKeditorAPI.GetInstance(textAreaId).GetXHTML();
}
FckRichEditor.prototype.setValue = function(textAreaId,value){
	if(FCKeditorAPI.GetInstance(textAreaId)){
		 FCKeditorAPI.GetInstance(textAreaId).SetHTML(value);
	}
}
FckRichEditor.prototype.exists = function(textAreaId){
	return FCKeditorAPI.GetInstance(textAreaId)!=null;
}
FckRichEditor.prototype.use = function(richObj,textAreaId,value,extConfig){
	if (!richObj) {
		richObj = new FCKeditor( textAreaId ) ;
		richObj.BasePath	= contextPath+"/s/fckeditor/" ;
		richObj.Config["CustomConfigurationsPath"] =  contextPath+'/s/fckeditor/oa_config.js';
		richObj.Height	= 280 ;
		richObj.Width = '95%';
		if(extConfig){
			if(extConfig.Width){
				richObj.Width	= extConfig.Width;
			}
			if(extConfig.Height){
				richObj.Height	= parseInt(extConfig.Height)+150;
			}
			if(extConfig.ToolbarSet){
				richObj.ToolbarSet	= extConfig.ToolbarSet;
			}
		}
		richObj.ReplaceTextarea();
	} else {
		var orichObjInstance = FCKeditorAPI.GetInstance(textAreaId);
		orichObjInstance.SetHTML(value);
		orichObjInstance.plain = false;
		var richObjframe = bupticetDom.$(textAreaId + '___Frame');
		richObjframe.style.display="";
	}
	return richObj;
}

FckRichEditor.prototype.unuse = function(textAreaId){
	var richObjframe = bupticetDom.$(textAreaId + '___Frame');
	richObjframe.style.display="none";
	FCKeditorAPI.GetInstance(textAreaId).plain = true;

}



function RichTextArea(sTextAreaId,sButtonId,sExtConfig,isRich){
	var isPlain = true;
	if(!sTextAreaId){
		alert("您必须指定文本域的id!");
	}
	var textAreaId = sTextAreaId;
	var buttonId = null;
	if(sButtonId){
		buttonId = sButtonId;
	}else{
		var node = null;
		if(textAreaId.length>2&&textAreaId.substring(textAreaId.length-2,textAreaId.length)=='Id'){
			if(textAreaId.length>10){
				node = bupticetDom.$(textAreaId.substring(0,textAreaId.length-10)+'ButtonId');
			}
			if(node==null){
				node = bupticetDom.$(textAreaId.substring(0,textAreaId.length-2)+'ButtonId');
			}
			if(node!=null){
				buttonId = node.id;
			}
		}else{
			node = bupticetDom.$(textAreaId+'ButtonId');
			if(node!=null){
				buttonId = node.id;
			}else{
				node = bupticetDom.$(textAreaId+'Button');
				if(node!=null){
					buttonId = node.id;
				}else{
					//alert("无法查找到切换编辑器的操作链接/按钮的id!");
					//return;
				}
			}
		}
	}
	if(isRich){
		isPlain = false;
	}
	var area = bupticetDom.$(textAreaId);
	//alert(this.area);
	var richObj = null;
	var extConfig = sExtConfig;
	var anotherArea = null;
	var anotherAreaId = null;
	if(extConfig&&extConfig.DisplayTextAreaId){
		anotherAreaId = extConfig.DisplayTextAreaId;
	}
	var self = this;
	var init = function(){
		if(RichTextArea.useAnotherTextArea){
			area.style.display = 'none';
			//id = textAreaId;
			if(!anotherAreaId){
				anotherId = RichTextArea.textAreaPrefix+textAreaId;
			}
			textAreaId = anotherId;
			if(RichTextArea.autoInsertTextArea){
				var areaWidth = '95%';
				var areaHeight = '100px';
				if(extConfig){
					if(extConfig.Width){
						areaWidth = extConfig.Width;
					}
					if(extConfig.Height){
						areaHeight = extConfig.Height;
					}
				}				
				var html = '<textarea id="'+anotherId +'" style="WIDTH: '+areaWidth+'; HEIGHT: '+areaHeight+';display:\'\';"></textarea>';
				bupticetDom.insertHtmlBefore(html,area);
			}
			anotherArea = bupticetDom.$(anotherId);
		}
		if(!isPlain){
			toRich(true);
			return;
		}
		var str = area.value;
		
		if(str&&str.length!=0){
			var str = str.replace(/<br[^<>]*?>/ig, '\n');
			if(str.search(/<[^<>]*?>/)!=-1){
				toRich(true);
				return;
			}
		}
		str = str.replace(/&gt;/ig, ">")
				 .replace(/&lt;/ig, "<")
				.replace(/&#039;/ig, "'")
				.replace(/&acute;/ig, "'")
				.replace(/&quot;/ig, '"')
				 .replace(/&nbsp;/ig, ' ')
		if(containOtherHtmlChar(str)){
			toRich(true);
			return;
		}
		str = str.replace(/&amp;/ig, '&');
		if(RichTextArea.useAnotherTextArea){
			anotherArea.value = str;
		}else{
			area.value = str;
		}
	}
	var containOtherHtmlChar = function(s){
				var position = s.search(/&#?[a-zA-Z0-9]{3,8};/);
				if(position==-1){
					return false;
				}else{
					if(s.length>=position+5&&s.substring(position,position+5).toLowerCase()=='&amp;'){
						return containOtherHtmlChar(s.substring(position+4,s.length));
					}else{
						return true;
					}
				}
			}
	var toRich = function(whenInit) {
		if(!RichTextArea.richEditor.canBackPlain){
			if (!confirm(RichTextArea.ToRichCanNotBackWarning)){
				return;
			}
		}
		var value = whenInit?area.value:self.getValue();
		
		if(!whenInit){
			value = value.replace(/&/g, "&amp;").
				   replace(/"/g, "&quot;").
				   replace(/  /g, "&nbsp;&nbsp;").
				   replace(/'/g, "&#039;").
				   replace(/</g, "&lt;").
				   replace(/>/g, "&gt;").
					replace(/\r\n/ig, "<br />").
					replace(/\r/ig, "<br />").
					replace(/\n/ig, "<br />");
		}
		
		
		area.style.display = "none";
		if(anotherArea){
			anotherArea.value = value;
			anotherArea.style.display = "none";
		}else{
			area.value = value;
		}
		var o = RichTextArea.richEditor.use(richObj,textAreaId,value,extConfig);
		if(o){
			richObj = o;
		}
		isPlain = false;
		if(buttonId){
			if(RichTextArea.richEditor.canBackPlain){
				bupticetDom.$(buttonId).innerHTML = RichTextArea.TextToPlain;
			}else{
				bupticetDom.$(buttonId).innerHTML = '';
			}
		}
	}
	var toPlain = function() {
			var str = self.getValue();
	//		alert(str);
			if(str&&str.length!=0){
				str = str.replace(/<br[^<>]*?>/ig, '\n');
				if(str.search(/<[^<>]*?>/)!=-1){
					if (!confirm(RichTextArea.ToPlainWarning)){
						return;
					}
				}
			}
			
		//strip html, and keep some format
		//var value = getValue();
		var value = str//.replace(/<br \/>/ig, "\n")
					 .replace(/<\/p>/ig, "\n")
					 .replace(/<[^<>]*?>/ig, '');
		value =	value.replace(/&gt;/ig, ">")
					 .replace(/&lt;/ig, "<")
					 .replace(/&quot;/ig, '"')
					 .replace(/&nbsp;/ig, ' ');
			if(containOtherHtmlChar(value)){
				if(RichTextArea.EnableSpecialHtmlCharConvert){
					if (!confirm(RichTextArea.ToPlainWithSpecialHtmlCharWarning)){
						return;
					}else{
						var charPairs = {'&euro;':'€','&lsquo;':'‘','&rsquo;':'’','&ldquo;':'“','&rdquo;':'”',
'&ndash;':'–','&mdash;':'—','&iexcl;':'¡','&cent;':'¢','&pound;':'£','&curren;':'¤','&yen;':'¥','&brvbar;':'¦',
'&sect;':'§','&uml;':'¨','&copy;':'©','&ordf;':'ª','&laquo;':'«','&not;':'¬','&reg;':'®','&macr;':'¯','&deg;':'°',
'&plusmn;':'±','&sup2;':'²','&sup3;':'³','&acute;':'´','&micro;':'µ','&para;':'¶','&middot;':'·','&cedil;':'¸',
'&sup1;':'¹','&ordm;':'º','&raquo;':'»','&frac14;':'¼','&frac12;':'½','&frac34;':'¾','&iquest;':'¿','&agrave;':'à',
'&aacute;':'á','&acirc;':'â','&atilde;':'ã','&auml;':'ä','&aring;':'å','&aelig;':'æ','&ccedil;':'ç','&egrave;':'è',
'&eacute;':'é','&ecirc;':'ê','&euml;':'ë','&igrave;':'ì','&iacute;':'í','&icirc;':'î','&iuml;':'ï','&eth;':'ð',
'&ntilde;':'ñ','&ograve;':'ò','&oacute;':'ó','&ocirc;':'ô','&otilde;':'õ','&ouml;':'ö','&times;':'×','&oslash;':'ø',
'&ugrave;':'ù','&uacute;':'ú','&ucirc;':'û','&yacute;':'ü','&thorn;':'ý','&szlig;':'þ','&agrave;':'ß','&aacute;':'à',
'&acirc;':'á','&atilde;':'â','&auml;':'ã','&aring;':'ä','&aelig;':'å','&ccedil;':'æ','&egrave;':'ç','&eacute;':'è',
'&ecirc;':'é','&euml;':'ê','&igrave;':'ë','&iacute;':'ì','&icirc;':'í','&iuml;':'î','&eth;':'ï','&ntilde;':'ð',
'&ograve;':'ñ','&oacute;':'ò','&ocirc;':'ó','&otilde;':'ô','&ouml;':'õ','&divide;':'ö','&oslash;':'÷','&ugrave;':'ø',
'&uacute;':'ù','&ucirc;':'ú','&uuml;':'û','&uuml;':'ü','&yacute;':'ý','&thorn;':'þ','&yuml;':'ÿ','&oelig;':'œ',
'&oelig;':'œ','&sbquo;':'‚','&bdquo;':'„','&hellip;':'…','&trade;':'™','&bull;':'•','&rarr;':'→',
'&rarr;':'⇒','&harr;':'⇔','&diams;':'♦','&asymp;':'≈'};
						var target = '';
						for(var i = 0;i<value.length;i++){
							if(value.charAt(i)!='&'){
								target += value.charAt(i);
								continue;
							}else{
								var part = /^&[a-zA-Z0-9]{3,8};/i.exec(value.substring(i));
								if(part&&part.length>0){
									part = part[0];
									if(/^&#(\xhex){4};$/i.exec(part)){
										target += unescape('%u'+part.substring(2,6));
									}else if(part!='&amp;'){
										var originalChar = charPairs[part.toLowerCase()];
										if(originalChar){
											target += originalChar;
										}else{
											target+=part;
										}
									}else{
										target += '&amp;';
									}
									i += part.length-1;
								}else{
									target += '&';
									continue;
								}
							}
						}
						value = target;
					}
				}else{
					if (!confirm(RichTextArea.ToPlainWarning)){
						return;
					}
				}
			}
			value =	value.replace(/&amp;/ig, '&');
			RichTextArea.richEditor.unuse(textAreaId);
		if(RichTextArea.useAnotherTextArea){
			anotherArea.value = value;
			anotherArea.style.display = "";
		}else{
			area.value = value;
			area.style.display = "";
		}
		isPlain = true;
		if(buttonId){
			bupticetDom.$(buttonId).innerHTML = RichTextArea.TextToRich;
		}
	}
	this.getValue = function(){
		if(isPlain){
			if(RichTextArea.useAnotherTextArea&&anotherArea){
				return anotherArea.value;
			}
			if(area){
				return area.value;
			}else{
				return null;
			}
		}else{
			return RichTextArea.richEditor.getValue(textAreaId);
		}
	}
	this.setValue = function(value){
		if(isPlain){
			if(RichTextArea.useAnotherTextArea&&anotherArea){
				anotherArea.value = value;
			}else{
				if(area){
					erea.value = value;
				}
			}
		}else{
			RichTextArea.richEditor.setValue(textAreaId,value);
		}
	}
	
	this.formReset = function(){
		var initValue = area.value;
		if(!isPlain){
				RichTextArea.richEditor.setValue(textAreaId,initValue);
				return;
		}else{
			if(initValue&&initValue!=''){
				var initValue = initValue.replace(/<br[^<>]*?>/ig, '\n');
				if(initValue.search(/<[^<>]*?>/)!=-1){
					toRich(true);
					return;
				}
			initValue = initValue.replace(/&gt;/ig, ">")
					 .replace(/&lt;/ig, "<")
					.replace(/&#039;/ig, "'")
					.replace(/&acute;/ig, "'")
					.replace(/&quot;/ig, '"')
					 .replace(/&nbsp;/ig, ' ')
					 .replace(/&amp;/ig, '&');	
					 this.setValue(initValue);
				}
		}
	}
	this.processWhenSumbit = function(){
		if(isPlain){
			var v =  this.getValue().
				   replace(/&/g, "&amp;").
				   replace(/"/g, "&quot;").
				   replace(/'/g, "&#039;").
				   replace(/</g, "&lt;").
				   replace(/>/g, "&gt;").
					replace(/  /g, "&nbsp;&nbsp;").
					replace(/\r\n/ig, "<br />").
					replace(/\r/ig, "<br />").
					replace(/\n/ig, "<br />");
			area.value = v;
			//if(!RichTextArea.useAnotherTextArea&&RichTextArea.richEditor.exists(textAreaId)){
			//	RichTextArea.richEditor.setValue(textAreaId,v); //TODO
			//}
		}else{
			//alert(getValue());
			area.value = this.getValue();
			//alert(bupticetDom.$(textAreaId).value);
		}
	}
	
	this.toggle = function(){
				if(isPlain){
				toRich();
			}else{
				toPlain();
			}
	}	
	init();
}



//可修改配置
RichTextArea.richEditor = new FckRichEditor();//change this to change rich editor type,such as tinymce
RichTextArea.useAnotherTextArea = true;
RichTextArea.autoInsertTextArea = true;
RichTextArea.EnableSpecialHtmlCharConvert = true;

RichTextArea.textAreaPrefix = 'bupticetTextArea-';

RichTextArea.TextToPlain = '纯文本编辑器';
RichTextArea.TextToRich = '可视化编辑器';
RichTextArea.ToPlainWarning =  "转换为纯文本将会遗失某些格式。 您确定要继续吗？"
RichTextArea.ToPlainWithSpecialHtmlCharWarning =  "当前编辑器区存在一些特殊HTML字符，若转换为纯文本需要较长时间处理这些字符， 您确定要继续吗？"
RichTextArea.ToRichCanNotBackWarning =  "使用"+RichTextArea.TextToRich+"后，将不能再返回"+RichTextArea.TextToPlain+"， 您确定要继续吗？"



var bupticetEditor = {
	textAreas:new Object(),
	submitProcess:false,
	addSubmitProcess:false,
	addFormResetProcess:false,
	textAreaPrefix:RichTextArea.textAreaPrefix,
//切换编辑器 
//textAreaId:文本域的dom id
	toggle:function(textAreaId){
		var t = this.textAreas[this.textAreaPrefix+textAreaId];
		if(t){
			t.toggle();
		}
	},
//创建可切换的编辑器
//textAreaId:文本域的dom id  必须指定
//buttonId:切换编辑器的操作链接/按钮的dom id  可自动查找,最好指定
//extConfig:扩展配置 例如： {Width:'100%',Height:'300',ToolbarSet,'Default'} 可以不指定,也可以为空 {}
//isRich:是否创建默认为Rich Editor的编辑器，缺省值为false 可不指定
	create:function(textAreaId,buttonId,extConfig,isRich){
		var obj = this.textAreas[this.textAreaPrefix+textAreaId];
		if(!obj){
			var t = new RichTextArea(textAreaId,buttonId,extConfig,isRich);
		//	t.init();
			this.textAreas[this.textAreaPrefix+textAreaId] = t;
		}else{
			alert("已经存在文本框id为："+textAreaId+"的编辑器对象，请检查是否重复定义!");
			return;
		}
	},
	processWhenSumbit:function(){
		if(this.submitProcess){
			return;
		}
		for(var o in this.textAreas){
			if(typeof o == 'string'&&o.indexOf(this.textAreaPrefix)==0){
				var t = this.textAreas[o];
				t.processWhenSumbit();
			}
		}
		this.submitProcess = true;
	},
	setValue:function(id,v){
		var t = this.textAreas[this.textAreaPrefix+id];
		t.setValue(v);
	},
	formReset:function(){
		for(var o in this.textAreas){
			if(typeof o == 'string'&&o.indexOf(this.textAreaPrefix)==0){
				var t = this.textAreas[o];
				t.formReset();
			}
		}
	}
}
