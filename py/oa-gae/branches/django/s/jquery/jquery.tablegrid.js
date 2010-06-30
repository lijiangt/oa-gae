(function($) {
$.fn.tablegrid = function(options){
    $.fn.tablegrid.defaults = {
        oddColor   : '',
        evenColor  : '',
        overColor  : '',
        selColor   : '',
        useClick   : true,
        useDblClick:false,
        col_border : ""
    };
    var opts = $.extend({}, $.fn.tablegrid.defaults, options);
    var resize_columns = function(root)
      {                   
        var tbl = root.children("table");    
        var tr  = tbl.find("thead tr:first");    
        var header,newwidth;
        var resize = false;
        
        root.width(tbl.width());  
        tr.children("th").css("border-right",opts.col_border);   
        var left_pos = root.offset().left;
    
        endresize = function()
        {
            if(resize == true && header != null)
            {
                document.onselectstart=new Function ("return true");
                resize = false;
                root.children("table").css("cursor","");
            }   
        };
        
        tbl.mousemove(function(e)
        {
            var left = (e.clientX - left_pos);
    
            if(resize)
            {
                var width = left - (header.offset().left - left_pos)
                    - parseInt(header.css("padding-left"))
                    - parseInt(header.css("padding-right"));
    
                if(width > 1)
                {
                    var current_width = header.width();
                    if(width > current_width)
                    {
                        var total = root.width() + ((width - header.width()));
                        root.width(total);
                        header.width(width);
                    }
                    else
                    {
                        header.width(width);
                        if(header.width() == width)
                        {
                            var total = root.width() + ((width - current_width));
                            root.width(total);
                        }
                    }
                    newwidth = width;
                }
            }
            else
            {
                if(e.target.nodeName == "TH")
                {
                    var tgt = $(e.target);
                    var dosize = (left-(tgt.offset().left-left_pos) 
                        > tgt.width()-2);
                    $(this).css("cursor",dosize?"col-resize":"");
                }
            }                   
        });
        
        tbl.mouseup(function(e) 
        {
            endresize();
        });
                
        tbl.bind("mouseleave",function(e)
        {
            endresize();
            return false; 
        });
        
        tr.mousedown(function(e) 
        {
            if(e.target.nodeName == "TH" 
                && $(this).css("cursor") ==  "col-resize")
            {
                header = $(e.target);                    
                resize = true;
                document.onselectstart=new Function ("return false");
            }    
            return false;
        });
        
        tr.bind('mouseleave',function(e)
        {
            if(!resize)
                root.children("table").css("cursor","");
        });
    };
    
    return this.each(function() {
        var root = $(this).wrap("<div class='roottbl' />").parent();
        resize_columns(root);
        
        
        $(this).find('tr:odd > td').css('backgroundColor', opts.oddColor);
        $(this).find('tr:even > td').css('backgroundColor', opts.evenColor);        
        
        $(this).find('tr').each(function(){
             
            this.origColor = $(this).find('td').css('backgroundColor');     
            this.clicked = false;   
            if (opts.useClick) {
                $(this).click(function(){   
                    if (this.clicked) {
                        $(this).find('td').css('backgroundColor', this.origColor);
                        this.clicked = false;
                    } else {
                        $(this).find('td').css('backgroundColor', opts.selColor);
                        this.clicked = true;
                    }
                    //$(this).find('td > input[@type=checkbox]').attr('checked', this.clicked);
                });
            }
         });
    });
};
})(jQuery);