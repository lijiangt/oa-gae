
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as gettext_lazy
import datetime
# Create your models here.

class Event(models.Model):
    summary = models.CharField(gettext_lazy('Summary'), max_length=200)
    owner = models.ForeignKey(User)
    start = models.DateTimeField(gettext_lazy('Start Time'), help_text=gettext_lazy('Example: 2008-06-01 13:30:00'))
    finish = models.DateTimeField(gettext_lazy('Finish Time'), blank=True, null=True, help_text=gettext_lazy('Example: 2008-06-02 13:30:00'))
    cooperation_dep = models.CharField(gettext_lazy('Cooperation Department'), max_length=200, blank=True, null=True)
    content = models.TextField(gettext_lazy('Content'), blank=True, null=True)
    aim =  models.TextField(gettext_lazy('Aim'), blank=True, null=True)
    resolved_problem=models.TextField(gettext_lazy('Resolved Problem'), blank=True, null=True)
    leave_problem=models.TextField(gettext_lazy('Leave Problem'), blank=True, null=True)
    total_work_time=models.FloatField(default=0)
    last_period = models.ForeignKey('Period',null=True,related_name='ref_event')
    last_modified=models.DateTimeField(gettext_lazy('Last Modify Time'), auto_now=True, editable=False)
    created=models.DateTimeField(gettext_lazy('Create Time'), auto_now_add=True, editable=False)
    def __unicode__(self):
        return self.summary
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
            for period in self.period_set.all():
                delta += period.get_period_delta()
            self.total_work_time = delta.days * 24*3600+delta.seconds
    class Admin:
        pass;
    class Meta:
        verbose_name = gettext_lazy('Event');
        verbose_name_plural = gettext_lazy('Events');
        ordering = ['-start']
        
class Period(models.Model):
    event= models.ForeignKey(Event)
    start = models.DateTimeField(gettext_lazy('Start Time'), help_text=gettext_lazy('Example: 2008-06-01 13:30:00'))
    finish = models.DateTimeField(gettext_lazy('Finish Time'), blank=True, null=True, help_text=gettext_lazy('Example: 2008-06-02 13:30:00'))
    content = models.TextField(gettext_lazy('Content'), blank=True, null=True)
    last_modified=models.DateTimeField(gettext_lazy('Last Modify Time'), auto_now=True, editable=False)
    created=models.DateTimeField(gettext_lazy('Create Time'), auto_now_add=True, editable=False)
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