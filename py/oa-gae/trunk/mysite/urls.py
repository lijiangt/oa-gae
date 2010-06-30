from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template,redirect_to
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext

def _404(request):
    return render_to_response('404.html', context_instance=RequestContext(request))
def _500(request):
    return render_to_response('500.html', context_instance=RequestContext(request))
handler404 = 'urls._404'
handler500 = 'urls._500'

def redirect_to_default_module(request):
    if not settings.DEBUG and settings.FORCE_DOMAIN_VISIT and request.META['SERVER_NAME'] != settings.FORCE_DOMAIN_VISIT and not request.META['SERVER_NAME'].endswith('appspot.com') and request.META['SERVER_NAME']!='localhost' and request.META['SERVER_NAME']!='127.0.0.1':
        return HttpResponseRedirect('http://%s%s/work_note/'%(settings.FORCE_DOMAIN_VISIT,settings.CONTEXT_PATH))
    else:
        return HttpResponseRedirect('%s/work_note/'%settings.CONTEXT_PATH)

def redirect_to_context_path(request):
    if not settings.DEBUG and settings.FORCE_DOMAIN_VISIT and request.META['SERVER_NAME'] != settings.FORCE_DOMAIN_VISIT and not request.META['SERVER_NAME'].endswith('appspot.com') and request.META['SERVER_NAME']!='localhost' and request.META['SERVER_NAME']!='127.0.0.1':
        return HttpResponseRedirect('http://%s%s/'%(settings.FORCE_DOMAIN_VISIT,settings.CONTEXT_PATH))
    else:
        return HttpResponseRedirect('%s/'%settings.CONTEXT_PATH)

url_prefix = ''
if settings.CONTEXT_PATH:
    url_prefix = (settings.CONTEXT_PATH)[1:]+'/'  

urlpatterns = patterns('',
    # Example:
    # (r'^oa/', include('foo.urls')),

    # Uncomment this for admin:
#    (r'^%sadmin/'%url_prefix, include('django.contrib.admin.urls')),
    
    (r'^%si18n.js$'%url_prefix, direct_to_template, {'template': 'js_i18n.html', 'mimetype':'text/javascript'}),
    
    (r'^%scontext_path.js$'%url_prefix, direct_to_template, {'template': 'js_context_path.html', 'mimetype':'text/javascript'}),
    
#    (r'^%saccounts/login$'%url_prefix, 'django.contrib.auth.views.login',{'template_name': 'accounts/login.html'}),
    
#    (r'^%saccounts/logout$'%url_prefix, 'django.contrib.auth.views.logout',{'next_page': settings.LOGOUT_REDIRECT_URL}),
#    (r'^%saccounts/password_change$'%url_prefix, 'django.contrib.auth.views.password_change',{'template_name': 'accounts/password_change_form.html'}),
#    (r'^%saccounts/password_changedone/$'%url_prefix, 'django.contrib.auth.views.password_change_done',{'template_name': 'accounts/password_change_done.html'}),
    (r'^%si18n/setlang'%url_prefix, 'django.views.i18n.set_language'),
   
    (r'^%s$'%url_prefix, redirect_to_default_module),
    
    (r'^%swork_note/'%url_prefix, include('work_note.urls')),
    
)

if settings.CONTEXT_PATH:
    urlpatterns += patterns('',
        (r'^$', redirect_to_context_path),
    )



#if settings.MEDIA_ROOT and settings.DEBUG:
#    urlpatterns += patterns('',
#        (r'^s/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
#    )
