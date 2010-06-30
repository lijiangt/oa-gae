from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('work_note.views',
     (r'^$', 'event_index'),
     (r'^!edit$', 'event_edit'),
     (r'^(?P<id>[0-9a-zA-Z-_]+)$', 'event_detail'),
     
     (r'^(?P<year>\d{4})/(?P<month>\w{1,2})/$', 'by_month'),
     
     (r'^will_do/$', 'will_do'),
     
     (r'^(?P<id>[0-9a-zA-Z-_]+)!finish$', 'event_finish'),
     (r'^!import_export$', 'event_import_page'),
     (r'^!import$', 'event_import'),
     (r'^!export$', 'event_export'),
     (r'^(?P<event_id>[0-9a-zA-Z-_]+)/!edit$', 'period_edit'),
     (r'^(?P<event_id>[0-9a-zA-Z-_]+)/!finish$', 'period_finish'),
     (r'^(?P<event_id>[0-9a-zA-Z-_]+)/$', 'period_create'),
     (r'^(?P<event_id>[0-9a-zA-Z-_]+)/(?P<id>[0-9a-zA-Z-_]+)$', 'period_detail'),
)
