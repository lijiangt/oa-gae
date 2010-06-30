# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.utils.translation import ugettext
from django.utils.encoding import force_unicode
import theme

IS_ASC_PARA='isAsc'
ORDER_FIELD_PARA='orderField'

register = template.Library()
def get_url(para):
    str = ''
    for item in para.items():
        if str:
            str += '&amp;%s=%s'%(item[0],item[1])
        else:
            str += '?%s=%s'%(item[0],item[1])
    return str

def get_order_str(request):
    para = request.GET
    field = para.get(ORDER_FIELD_PARA,None)
    if field:
        if 'True' == para.get(IS_ASC_PARA,False):
            return field
        else:
            return '-%s'%field
    else:
        return None

def pagination_context(count,page_num,page_size):
    if page_num==0:
        page_num = 1
    d = {'results_per_page':page_size,
         'has_previous':page_num!=1,
         'page':page_num,
         'next':page_num+1,
         'previous':page_num-1,
         'first_on_page':(page_num-1)*page_size+1,
         'hits':count,
         }
    if page_num*page_size<count:
        d['has_next']=True
        d['last_on_page']=page_num*page_size
    else:
        d['has_next']=False
        d['last_on_page']=count
    if count%page_size == 0:
        if count ==0:
            d['pages'] = 1
        else:
            d['pages'] = count/page_size
    else:
        d['pages'] = count/page_size+1
    d['page_range']=range(1,d['pages']+1)
    return d

class TagNode(template.Node):
    def __init__(self,field,name_key,default_asc=None):
        self.field = field
        self.name_key = name_key
        self.default_asc = default_asc
        
    def render(self, context):
        para = context['request'].GET.copy()
        field = self.field.resolve(context)
        name = force_unicode(ugettext(self.name_key.resolve(context)))
        if field == para.get(ORDER_FIELD_PARA,None) or (not para.has_key(ORDER_FIELD_PARA) and self.default_asc != None):
            if field == para.get(ORDER_FIELD_PARA,None):
                asc =  False
                if para.has_key(IS_ASC_PARA):
                    asc = para[IS_ASC_PARA]=='True'
            elif not para.has_key(ORDER_FIELD_PARA) and self.default_asc != None:
                para[ORDER_FIELD_PARA]=field
                asc = self.default_asc
            para[IS_ASC_PARA] = not asc
            reverse_order_name=force_unicode('正向')
            order_alt = force_unicode('降序 ')
            order = 'desc'
            if asc:
                order = 'asc'
                reverse_order_name=force_unicode('反向')
                order_alt = force_unicode('升序 ')
            return force_unicode('<a href="%(url)s" title="点击此处按%(name)s%(reverse_order_name)s排序">\
%(name)s<img src="%(media_url)s/themes/%(theme)s/button/sort_%(order)s.gif" alt="降序">\
</a>')%{'url':get_url(para),
                     'name':name,
                     'reverse_order_name':reverse_order_name,
                     'media_url':settings.MEDIA_URL,
                     'theme':theme.ThemeNode().render(context),
                     'order':order,
                     'order_alt':order_alt,
                     }
        else:
            para[ORDER_FIELD_PARA]=field
            para[IS_ASC_PARA] = True
            return force_unicode('<a href="%(url)s" title="点击此处按%(name)s%(order_name)s排序">%(name)s</a>')%{'url':get_url(para),
                         'name':name,
                         'order_name':force_unicode('正向')}

@register.tag
def title_field_html(parser, token):
    paras = token.split_contents()
    if len(paras) == 4:
        if paras[3] in ['+','-']:
            return TagNode(parser.compile_filter(paras[1]),parser.compile_filter(paras[2]),paras[3]=='+')
        else:
            raise template.TemplateSyntaxError, "%r tag argument must be '+' or '-'" % paras[0]
    elif len(paras) == 3:
        return TagNode(parser.compile_filter(paras[1]),parser.compile_filter(paras[2]))
    else:
        raise template.TemplateSyntaxError, "%r tag requires two or three arguments" % paras[0]    
