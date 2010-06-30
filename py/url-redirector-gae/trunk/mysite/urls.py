from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^__admin__/', include('redirect.urls')),
    (r'^', include('root.urls')),
)