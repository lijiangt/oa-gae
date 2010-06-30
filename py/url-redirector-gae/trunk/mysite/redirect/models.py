from google.appengine.ext import db
from appengine_django.models import BaseModel
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as gettext_lazy



import datetime

class RedirectDomain(BaseModel):
    domain = db.StringProperty(gettext_lazy('Domain'),required=True)
    target_url = db.StringProperty(gettext_lazy('Target URL'),required=True)
    full_path_redirect = db.StringProperty(gettext_lazy('Full Path Redirect'))
    desc = db.TextProperty(gettext_lazy('Description'))
    owner = db.UserProperty()
    last_modified=db.DateTimeProperty(gettext_lazy('Last Modify Time'), auto_now=True)
    created=db.DateTimeProperty(gettext_lazy('Create Time'), auto_now_add=True)
    
    
class VisitLog(BaseModel):
    domain = db.StringProperty(gettext_lazy('Domain'),required=True)
    visit_url = db.StringProperty(gettext_lazy('Visit URL'),required=True)
    target_url = db.StringProperty(gettext_lazy('Target URL'))
    referrer_url = db.StringProperty(gettext_lazy('Referrer URL'))
    session_id = db.StringProperty(gettext_lazy('Session ID'))
    request_method = db.StringProperty(gettext_lazy('Request Method'),default="GET")
    headers = db.TextProperty(gettext_lazy('Headers'))
    client_ip = db.StringProperty(gettext_lazy('Client IP'))
    visit_time =db.DateTimeProperty(gettext_lazy('Create Time'), auto_now_add=True)
    visitor = db.UserProperty()