from django import template

register = template.Library()

class TagNode(template.Node):
    def __init__(self,para_name,para_value):
        self.para_name = para_name
        self.para_value = para_value
        
    def render(self, context):
        name = self.para_name.resolve(context)
        value = self.para_value.resolve(context)
        para = context['request'].GET.copy()
        para[name]=value
        str  = '';
        if len(para):
            for item in para.items():
                if str:
                    str += '&%s=%s'%(item[0],item[1])
                else:
                    str += '?%s=%s'%(item[0],item[1])
            return str
        else:
            return ''

@register.tag
def action_uri(parser, token):
    paras = token.split_contents()
    num = len(paras)
    if num == 3:
        return TagNode(template.Variable(paras[1]),template.Variable(paras[2]))
    else:
        raise template.TemplateSyntaxError, "%r tag requires one or two argument" % paras[0]
    
