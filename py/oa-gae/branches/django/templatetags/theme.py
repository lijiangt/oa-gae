from django import template
from django.conf import settings

register = template.Library()

THEME_KEY = 'custom_theme'

class ThemeNode(template.Node):
    def __init__(self):
        pass
        
    def render(self, context):
        custom = context.get('custom',None)
        if custom and custom.has_key(THEME_KEY):
            return custom[THEME_KEY]
        else:
            return settings.DEFAULT_THEME

@register.tag
def theme(parser, token):
    """
    Returns the string contained in the setting site theme.
    """
    return ThemeNode()
