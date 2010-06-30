from google.appengine.ext import db
from appengine_django.models import BaseModel
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as gettext_lazy
import datetime

class Event(BaseModel):
    summary = db.StringProperty(gettext_lazy('Summary'),required=True)
    owner = db.UserProperty()
    start = db.DateTimeProperty(gettext_lazy('Start Time'),required=True)
    finish = db.DateTimeProperty(gettext_lazy('Finish Time'))
    cooperation_dep = db.StringProperty(gettext_lazy('Cooperation Department'))
    content = db.TextProperty(gettext_lazy('Content'))
    aim =  db.TextProperty(gettext_lazy('Aim'))
    resolved_problem=db.TextProperty(gettext_lazy('Resolved Problem'))
    leave_problem=db.TextProperty(gettext_lazy('Leave Problem'))
    last_period = db.StringProperty()
    total_work_time=db.IntegerProperty(default=0)
    last_modified=db.DateTimeProperty(gettext_lazy('Last Modify Time'), auto_now=True)
    created=db.DateTimeProperty(gettext_lazy('Create Time'), auto_now_add=True)
    def __unicode__(self):
        return self.summary
    def get_period_set(self):
        return self.period_set.order('start')
    def get_last_period(self):
        return db.get(db.Key(self.last_period))
    def set_last_period(self,period):
        self.last_period = str(period.key())
    def get_period_delta(self):
        if self.finish:
            if not self.total_work_time:
                self.update_total_work_time()
                self.save()
            days = self.total_work_time//(24*3600)
            seconds = self.total_work_time % (24*3600)
            return datetime.timedelta(days,seconds)
    def get_period_delta_str(self):
        delta = self.get_period_delta();
        if delta:
            days = delta.days
            if days == 0:
                return delta
            delta = datetime.timedelta(0,delta.seconds)
            return str(days)+_('days')+' '+str(delta)
        else:
            return ''
    def update_total_work_time(self):
        if self.finish:
            delta = datetime.timedelta(0,0,0)
            for period in self.period_set:
                delta += period.get_period_delta()
            self.total_work_time = delta.days * 24*3600+delta.seconds
    class Admin:
        pass;
    class Meta:
        verbose_name = gettext_lazy('Event');
        verbose_name_plural = gettext_lazy('Events');
        ordering = ['-start']
        
class Period(BaseModel):
    event= db.ReferenceProperty(Event,collection_name='period_set')
    start = db.DateTimeProperty(gettext_lazy('Start Time'))
    finish = db.DateTimeProperty(gettext_lazy('Finish Time'))
    content = db.TextProperty(gettext_lazy('Content'))
    last_modified=db.DateTimeProperty(gettext_lazy('Last Modify Time'), auto_now=True)
    created=db.DateTimeProperty(gettext_lazy('Create Time'), auto_now_add=True)
    def __unicode__(self):
        if self.finish:
            return str(self.start) + ' ~ ' + str(self.finish)
        else:
            return str(self.start) + ' ~ ?'
    def get_period_delta(self):
        if self.finish:
            return self.finish - self.start
    class Admin:
        pass;
    class Meta:
        verbose_name = gettext_lazy('Period');
        verbose_name_plural = gettext_lazy('Periods');
        ordering = ['start']