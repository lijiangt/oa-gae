from django import template

register = template.Library()


@register.simple_tag
def media_url():
    """
    Returns the string contained in the setting MEDIA_URL.
    """
    try:
        from django.conf import settings
    except ImportError:
        return ''
    return settings.MEDIA_URL
