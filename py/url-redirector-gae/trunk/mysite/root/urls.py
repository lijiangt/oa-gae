from django.conf.urls.defaults import *

urlpatterns = patterns('root.views',
   (r'^(?P<uri>.*)$','redirect'),
)