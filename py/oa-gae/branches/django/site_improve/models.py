
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as gettext_lazy
# Create your models here.

bug_status_choices = (('open', gettext_lazy('open')), ('fixed', gettext_lazy('fixed')), ('reopen', gettext_lazy('reopen')), ('closed', gettext_lazy('closed')),)

class Bug(models.Model):
    current_content = models.ForeignKey('Content',null=True,related_name='ref_bug')
    def __unicode__(self):
        return self.current_content.summary;
    class Admin:
        pass;
    class Meta:
        verbose_name = gettext_lazy('Bug');
        verbose_name_plural = gettext_lazy('Bugs');
        ordering = ['-current_content']
    
class Content(models.Model):
    summary = models.CharField(gettext_lazy('Summary'), max_length=200)
    type=models.CharField(gettext_lazy('Type'), max_length=20, choices=(('defect', gettext_lazy('defect')), ('enhancement', gettext_lazy('enhancement')), ('task', gettext_lazy('task')),), default='defect')
    content = models.TextField(gettext_lazy('Content'), blank=True, null=True)
    priority=models.CharField(gettext_lazy('Priority'), max_length=20, choices=(('blocker', gettext_lazy('blocker')), ('critical', gettext_lazy('critical')), ('major', gettext_lazy('major')), ('minor', gettext_lazy('minor')), ('trivial', gettext_lazy('trivial')),), default='major')
    assign_to =  models.CharField(gettext_lazy('Assign to'), max_length=200, blank=True, null=True)
    cc =  models.CharField(gettext_lazy('Cc'), max_length=200, blank=True, null=True)
    keywords = models.CharField(gettext_lazy('Keywords'), max_length=200, blank=True, null=True)
    component = models.CharField(gettext_lazy('Component'), max_length=200, choices=(('work_note', gettext_lazy('work_note')), ('site_improve', gettext_lazy('site_improve')),), default='work note')
#    version = models.CharField(gettext_lazy('Version'), max_length=200, choices=(('trunk', gettext_lazy('trunk'))), default='trunk')
    version = models.CharField(gettext_lazy('Version'), max_length=200, default='trunk')
    status = models.CharField(gettext_lazy('Status'), max_length=20, choices=bug_status_choices, default='open')
    modifier = models.ForeignKey(User)
    bug = models.ForeignKey(Bug)
    last_modified=models.DateTimeField(gettext_lazy('Last Modify Time'), auto_now=True, editable=False)
    created=models.DateTimeField(gettext_lazy('Create Time'), auto_now_add=True, editable=False)
    def __unicode__(self):
        return self.summary+' - ' + str(self.created);
    class Admin:
        pass;
    class Meta:
        verbose_name = gettext_lazy('Content');
        verbose_name_plural = gettext_lazy('Contents');
        ordering = ['-last_modified']