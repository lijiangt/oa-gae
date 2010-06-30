from django.template import Library

register = Library()

@register.simple_tag
def context_path():
    """
    Returns the string contained in the setting CONTEXT_PATH.
    """
    try:
        from django.conf import settings
    except ImportError:
        return ''
    return settings.CONTEXT_PATH
