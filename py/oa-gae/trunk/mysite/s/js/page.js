function DynamicLayerSelect(sSelectId,sElementName,sSingle,sOnchangeCallback){
	var single = sSingle||false;
	var selectId = sSelectId; 
	var onchangeCallback = sOnchangeCallback;
	var htmlSelect = BupticetDom.$(selectId);
	var initValue = new Array();
	for(var i = 0;i<htmlSelect.options.length;i++){
		initValue[initValue.length] = {text:htmlSelect.options[i].text,value:htmlSelect.options[i].value};
	}
	var elementName = sElementName;
	var displaySpanId = DynamicLayerSelect.DisplaySpanIdPrefix + selectId;
	var endDisplaySpanId = DynamicLayerSelect.EndDisplaySpanIdPrefix + selectId;
	var self = this;
	var getInitResultHtml = function(entities,inner){
		var html = '';
		for(var i = 0;i<entities.length;i++){
			html += getElementHtml(entities[i].text,entities[i].value);
		}
		if(inner){
			return html+'<span id="'+endDisplaySpanId+'"></span>';
		}else{
			return '<span id="'+displaySpanId+'">'+html+'<span id="'+endDisplaySpanId+'"></span></span>';
		}
	};
	var getEmptyResultHtml = function(inner){
		if(inner){
			return '<span id="'+endDisplaySpanId+'">'+DynamicLayerSelect.NotSelectDisplayInfoPrefix+elementName+'</span>';
		}else{
			return '<span id="'+displaySpanId+'"><span id="'+endDisplaySpanId+'">'+DynamicLayerSelect.NotSelectDisplayInfoPrefix+elementName+'</span></span>';
		}
	};
	var getInitInnerHtml = function(notDisplayInfo){
		return '<span id="'+endDisplaySpanId+'">'+(notDisplayInfo?'':(DynamicLayerSelect.NotSelectDisplayInfoPrefix+elementName))+'</span>';
	};
	var getElementHtml = function(display,value){
		var spanId = DynamicLayerSelect.getId();
		var html = '  <span id="'+spanId+'">'+display+'<a href="Javascript:bupticetLayer.deleteElement(\''+selectId+'\',\''+value+'\',\''+spanId+'\');void(0);" title="'+DynamicLayerSelect.CancelSelectDisplayInfoPrefix+display+'"><img src="'+DynamicLayerSelect.DeletePicUrl+'" border="0"/></a></span>';
		return html;
	};
	var addToHtmlSelect = function(entity,notExecuteCallback){
		var flag = bupticetForm.htmlSelect.addOption(htmlSelect,entity.value,entity.text);
		if(!notExecuteCallback&&flag&&onchangeCallback&&typeof onchangeCallback == 'function'){
			onchangeCallback(entity.value);
		}
		return flag;
	};
	var deleteFromHtmlSelect = function(value,notExecuteCallback){
		var flag = bupticetForm.htmlSelect.deleteElement(htmlSelect,value);
		if(!notExecuteCallback&&flag&&onchangeCallback&&typeof onchangeCallback == 'function'){
			onchangeCallback(value);
		}
		return flag;
	};
	var deleteAllFromHtmlSelect = function(notExecuteCallback){
		bupticetForm.htmlSelect.deleteAllElements(htmlSelect);
		if(!notExecuteCallback&&bupticetForm.htmlSelect.getCount(htmlSelect)>0&&onchangeCallback&&typeof onchangeCallback == 'function'){
			onchangeCallback(htmlSelect.option,true);
		}
	};
	this.getSelectedCount = function(){
		return bupticetForm.htmlSelect.getCount(htmlSelect);
	}
	createResultDisplay = function(){
		var html = null;
		//alert(this.getSelectedCount());
		if(self.getSelectedCount()==0){
			html = getEmptyResultHtml();
		}else{
			html = getInitResultHtml(htmlSelect.options);
		}
		htmlSelect.style.display = 'none';
		BupticetDom.insertHtmlBefore(html,htmlSelect);
	}
	this.formReset = function(){
		if(initValue.length==0){
			deleteAllFromHtmlSelect();
			BupticetDom.$(displaySpanId).innerHTML = getEmptyResultHtml(true);
		}else{
			BupticetDom.$(displaySpanId).innerHTML = getInitResultHtml(initValue,true);
			deleteAllFromHtmlSelect();
			for(var i = 0;i<initValue.length;i++){
				addToHtmlSelect(initValue[i],true);				
			}
		}
	}
	this.deleteAllElement = function(notDisplayInfo){
		BupticetDom.$(displaySpanId).innerHTML = getInitInnerHtml(notDisplayInfo);
		deleteAllFromHtmlSelect();
	}
	this.deleteElement = function(value,spanId){
		BupticetDom.$(spanId).innerHTML = '';
		deleteFromHtmlSelect(value);
		if(self.getSelectedCount()==0){
			BupticetDom.$(displaySpanId).innerHTML = getInitInnerHtml();
		}
	}
	this.addElements = function(entities){
		if(entities.length==0){
			return;
		}
		if(single){
			this.deleteAllElement(true);
		}
		if(this.getSelectedCount()==0){
			BupticetDom.$(endDisplaySpanId).innerHTML = '';
		}
		var newAdded = new Array();
		for(var i = 0;i<entities.length;i++){
			var position = entities[i].indexOf(':');
			var o = {text:(entities[i].substring(position+1)), value:(entities[i].substring(0,position))};
			if(addToHtmlSelect(o)){
				newAdded[newAdded.length] = o;
			}
		}
		var html = '';
		for(var i = 0;i<newAdded.length;i++){
			html += getElementHtml(newAdded[i].text,newAdded[i].value);
		}
		BupticetDom.insertHtmlBefore(html,BupticetDom.$(endDisplaySpanId));
	}
	this.getSelectId = function(){
		return selectId;
	}
	createResultDisplay();
}





DynamicLayerSelect.NotSelectDisplayInfoPrefix = '尚未选择任何';
DynamicLayerSelect.CancelSelectDisplayInfoPrefix = '取消选择';
DynamicLayerSelect.DisplaySpanIdPrefix='dynamicSelectResult-';
DynamicLayerSelect.EndDisplaySpanIdPrefix='dynamicSelectResultEnd-';
DynamicLayerSelect.DisplaySpanIdPrefix='selectResult-';
DynamicLayerSelect.SelectedElementIdPrefix='selectedElement-';
DynamicLayerSelect.IdCounter=0;
DynamicLayerSelect.DeletePicUrl = '../../images/common/delete.gif';
DynamicLayerSelect.getId = function(){
	return DynamicLayerSelect.SelectedElementIdPrefix+DynamicLayerSelect.IdCounter++;
}





var bupticetLayer = {
	objectPrefix:'dynamicLayerSelect-',
	all : {},
	deleteElement:function(selectId,value,spanId){
		var o = this.all[this.objectPrefix+selectId];
		o.deleteElement(value,spanId);
	},
	deleteAllElement:function(selectId){
		var o = this.all[this.objectPrefix+selectId];
		o.deleteAllElement();
	},
	createDynamicSelect:function(selectId,elementName,single,onchangeCallback){
		var o = new DynamicLayerSelect(selectId,elementName,single,onchangeCallback);
		this.all[this.objectPrefix+selectId] = o;
	},
	addElements:function(selectId,values){
		var o = this.all[this.objectPrefix+selectId];
		o.addElements(values);
	},
	getSelectedCount:function(selectId){
		var o = this.all[this.objectPrefix+selectId];
		o.getSelectedCount();
	},
	getSelectValues : function(srcForm,srcField){
		var values = new Array();
		var selects = srcForm.elements[srcField]; 
	  if(!selects){
	  	return values;
	  	}
		if(!selects.length&&selects.checked){
			values[0] = selects.value;
		}else{
			for(var i=0;i < selects.length;i++){
				if(selects[i].checked){
					values[values.length] = selects[i].value;
				}
			}
		}
		return values;
	},
	formReset:function(){
		for(var p in this.all){
			if(typeof p == 'string'&&p.indexOf(this.objectPrefix)==0){
				var o = this.all[p];
				o.formReset();
			}
		}
	},
	processWhenSumbit:function(){
		for(var p in this.all){
			if(typeof p == 'string'&&p.indexOf(this.objectPrefix)==0){
				var o = this.all[p];
				bupticetForm.htmlSelect.selectDomAllOptions(o.getSelectId());
			}
		}
	}
}



