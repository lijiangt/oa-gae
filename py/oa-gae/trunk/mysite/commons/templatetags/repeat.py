from django import template

register = template.Library()

class RepeatNode(template.Node):
    def __init__(self, nodelist, time, existing=None):
        self.nodelist = nodelist
        self.time = time
        self.existing = existing
    def render(self, context):
        try:
            time = int(self.time.resolve(context))
        except ValueError:
            raise template.TemplateSyntaxError(u"The first argument to '%r' must be an integer (got '%s')." % ('repeat', self.time_str))
        if self.existing:
            try:
                time -= int(self.existing.resolve(context))
            except ValueError:
                raise template.TemplateSyntaxError(u"The second argument to '%r' must be an integer (got '%s')." % ('repeat', self.existing_str))
        output = self.nodelist.render(context)
        result = ''
        for i in range(time):
            result += output
        return result

@register.tag
def repeat(parser, token):
    nodelist = parser.parse(('endrepeat',))
    parser.delete_first_token()
    paras = token.split_contents()
    num = len(paras)
    if num==2:
        return RepeatNode(nodelist,parser.compile_filter(paras[1]))
    elif num==3:
        return RepeatNode(nodelist,parser.compile_filter(paras[1]),parser.compile_filter(paras[2]))
    else:
        raise template.TemplateSyntaxError, "%r tag requires one or two argument" % paras[0]    