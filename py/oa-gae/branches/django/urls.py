from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template,redirect_to
from django.shortcuts import render_to_response
from django.template import RequestContext

def _404(request):
    return render_to_response('404.html', context_instance=RequestContext(request))
def _500():
    return render_to_response('500.html', context_instance=RequestContext(request))

handler404 = 'oa.urls._404'
handler500 = 'oa.urls._500'

url_prefix = ''
if settings.CONTEXT_PATH:
    url_prefix = (settings.CONTEXT_PATH)[1:]+'/'  

urlpatterns = patterns('',
    # Example:
    # (r'^oa/', include('oa.foo.urls')),

    # Uncomment this for admin:
    (r'^%sadmin/'%url_prefix, include('django.contrib.admin.urls')),
    
    (r'^%si18n.js$'%url_prefix, direct_to_template, {'template': 'js_i18n.html', 'mimetype':'text/javascript'}),
    
    (r'^%scontext_path.js$'%url_prefix, direct_to_template, {'template': 'js_context_path.html', 'mimetype':'text/javascript'}),
    
    (r'^%saccounts/login$'%url_prefix, 'django.contrib.auth.views.login',{'template_name': 'accounts/login.html'}),
    
    (r'^%saccounts/logout$'%url_prefix, 'django.contrib.auth.views.logout',{'next_page': settings.LOGOUT_REDIRECT_URL}),
    (r'^%saccounts/password_change$'%url_prefix, 'django.contrib.auth.views.password_change',{'template_name': 'accounts/password_change_form.html'}),
    (r'^%saccounts/password_changedone/$'%url_prefix, 'django.contrib.auth.views.password_change_done',{'template_name': 'accounts/password_change_done.html'}),
    (r'^%si18n/setlang'%url_prefix, 'django.views.i18n.set_language'),
   
    (r'^%s$'%url_prefix, redirect_to,{'url': 'work_note/'}),
    
    (r'^%swork_note/'%url_prefix, include('oa.work_note.urls')),
    (r'^%ssite_improve/'%url_prefix, include('oa.site_improve.urls')),
    
)

if settings.CONTEXT_PATH:
    urlpatterns += patterns('',
        (r'^$', redirect_to, {'url': settings.CONTEXT_PATH+'/    '}),
    )



if settings.MEDIA_ROOT and settings.DEBUG:
    urlpatterns += patterns('',
        (r'^s/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
