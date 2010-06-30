from django.template import Library

register = Library()

@register.simple_tag
def login_url():
    """
    Returns the string contained in the setting LOGIN_URL.
    """
    try:
        from django.conf import settings
    except ImportError:
        return ''
    return settings.LOGIN_URL
