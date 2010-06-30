from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
import datetime

today = datetime.date.today()
urlpatterns = patterns('',
     (r'^$', 'oa.work_note.views.event_index'),
     (r'^!edit$', 'oa.work_note.views.event_edit'),
     (r'^(?P<object_id>\d+)$', 'oa.work_note.views.event_detail'),
     
     (r'^(?P<year>\d{4})/(?P<month>\w{1,2})/$', 'oa.work_note.views.by_month'),
     
     (r'^will_do/$', 'oa.work_note.views.will_do'),
     
     (r'^(?P<object_id>\d+)!finish$', 'oa.work_note.views.event_finish'),
     
     
     (r'^(?P<event_id>\d+)/!edit$', 'oa.work_note.views.period_edit'),
     (r'^(?P<event_id>\d+)/!finish$', 'oa.work_note.views.period_finish'),
     (r'^(?P<event_id>\d+)/$', 'oa.work_note.views.period_create'),
      (r'^(?P<event_id>\d+)/(?P<object_id>\d+)$', 'oa.work_note.views.period_detail'),
)
