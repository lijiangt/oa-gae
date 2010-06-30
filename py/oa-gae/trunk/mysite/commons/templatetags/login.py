from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def login_url():
    """
    Returns the string contained in the setting LOGIN_URL.
    """
    if settings.DATABASE_ENGINE == 'appengine':
        from google.appengine.api import users
        return users.create_login_url("/")  # TODO: replace the path to the current visit uri
    else:
        return settings.LOGIN_URL

@register.simple_tag
def logout_url():
    if settings.DATABASE_ENGINE == 'appengine':
        from google.appengine.api import users
        return users.create_logout_url("/")
    else:
        return settings.LOGOUT_URL

class LoginNode(template.Node):
    def __init__(self):
        pass
    def render(self, context):
        if settings.DATABASE_ENGINE == 'appengine':
            from google.appengine.api import users
            user = users.get_current_user()
            if user:
                context['login'] = True
                context['user_name'] = user.nickname()
            else:
                context['login'] = False
        else:
            user = template.Variable('user').resolve(context)
            if user and user.is_authenticated:
                context['login'] = True
                if user.first_name:
                    context['user_name'] = '%s%s'%(user.last_name,user.first_name)
                else:
                    context['user_name'] = user.username
            else:
                context['login'] = False
        return ''

@register.tag
def login_status(parser, token):
    return LoginNode()