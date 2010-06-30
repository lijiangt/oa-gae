from django.conf.urls.defaults import *


urlpatterns = patterns('',
     (r'^$', 'oa.site_improve.views.bug_index'),
     (r'^!edit$', 'oa.site_improve.views.bug_edit'),
     (r'^(?P<object_id>\d+)$', 'oa.site_improve.views.bug_detail'),
     
     (r'^my/$', 'oa.site_improve.views.bug_my'),
     (r'^open/$', 'oa.site_improve.views.bug_open'),
)
