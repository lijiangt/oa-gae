from django import template
from django.utils.translation import ugettext as _

register = template.Library()


@register.simple_tag
def site_name():
    """
    """
    try:
        from django.conf import settings
    except ImportError:
        return _('Work Notebook')
    return _(settings.SITE_NAME)

def module_list_html():
    """
    """
    try:
        from django.conf import settings
    except ImportError:
        return 'module_list.html'
    return settings.MODULE_LIST_HTML

@register.inclusion_tag(module_list_html())
def site_module():
    try:
        from django.conf import settings
        context_path = settings.CONTEXT_PATH
    except ImportError:
        context_path = ''
    return {'context_path': context_path}

def bottom_include_html():
    """
    """
    try:
        from django.conf import settings
    except ImportError:
        return 'bottom_include.html'
    return settings.BOTTOM_INCLUDE_HTML

@register.inclusion_tag(bottom_include_html())
def site_bottom_include():
    return {}

