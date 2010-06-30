from django import template
from urllib import urlencode
from django.template.defaultfilters import stringfilter

register = template.Library()

EXT_QUERY_STRING_PARA ='extQueryString' 


class TagNode(template.Node):
    def __init__(self,separate,raw):
        self.separate = separate
        self.raw = raw
        
    def render(self, context):
        para = context['request'].GET
        str = ''
        if para:
            for item in para.items():
                if str:
                    str += '&%s=%s'%(item[0],item[1])
                else:
                    str += '%s=%s'%(item[0],item[1])
            if self.raw:
                return str
            else:
                return '%s%s'%(self.separate,urlencode({EXT_QUERY_STRING_PARA:str})) 
        else:
            return ''
def get_ext_query_string(parser, token, raw=False):
    paras = token.split_contents()
    if len(paras) == 2:
        if paras[1] in ['?','&amp;', '&']:
            return TagNode(paras[1],raw)
        else:
            raise template.TemplateSyntaxError, "%r tag argument must be '?' '&' or '&amp;'" % paras[0]
    elif len(paras) == 1:
        return TagNode('',raw)
    else:
        raise template.TemplateSyntaxError, "%r tag requires zero or one argument" % paras[0]    

@register.tag
def ext_query_string(parser, token):
    return get_ext_query_string(parser, token)

@register.tag
def ext_query_raw_string(parser, token):
    return get_ext_query_string(parser, token,True)

@register.filter
@stringfilter
def encode_ext_query_string(value,arg):
    if not value:
        return ''
    elif arg in ['?','&amp;', '&']:
        return '%s%s'%(arg,urlencode({EXT_QUERY_STRING_PARA:value})) 
    else:
        raise template.TemplateSyntaxError, "%r tag requires zero or one argument" % paras[0]