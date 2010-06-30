# -*- coding: utf-8 -*-
from django.conf import settings
import django.forms as forms
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.translation import ugettext

class JsDateTimeWidget(forms.DateTimeInput):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        elif hasattr(value, 'strftime'):
            value = value.strftime(self.format)
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(value)
        id = final_attrs['id']
#        final_attrs['onfocus']='Calendar.show();'
        final_attrs['size']=16
        final_attrs['maxlength']=20
        append =  '''<img src="'''+settings.MEDIA_URL+'''/jscalendar/img.gif" id="'''+id+'''_date_selector" class="dateSelector"/>  &lt;- ''' +ugettext('Click this picture to select date and time.')+'''
<script type="text/javascript">
    Calendar.setup({
        inputField     :    "'''+id+'''",
        ifFormat       :    "%Y-%m-%d %H:%M:00",
        showsTime      :    true,
        button         :    "'''+id+'''_date_selector",
        timeFormat     :    24,
        singleClick    :    true
    });
</script>
'''
#        return s[:-2] + insert + s[-2:] + append
        return mark_safe(u'<input%s />' % flatatt(final_attrs))+force_unicode(append)
    
class JsDateWidget(forms.DateTimeInput):
    def __init__(self, attrs=None, format='%Y-%m-%d'):
        super(JsDateWidget, self).__init__(attrs,format)
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        elif hasattr(value, 'strftime'):
            value = value.strftime(self.format)
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(value)
        id = final_attrs['id']
#        final_attrs['onfocus']='Calendar.show();'
        final_attrs['size']=8
        final_attrs['maxlength']=12
        append =  '''<img src="'''+settings.MEDIA_URL+'''/jscalendar/img.gif" id="'''+id+'''_date_selector" class="dateSelector"/>  &lt;- ''' +ugettext('Click this picture to select date.')+'''
<script type="text/javascript">
    Calendar.setup({
        inputField     :    "'''+id+'''",
        ifFormat       :    "%Y-%m-%d",
        showsTime      :    false,
        button         :    "'''+id+'''_date_selector",
        singleClick    :    true
    });
</script>
'''
#        return s[:-2] + insert + s[-2:] + append
        return mark_safe(u'<input%s />' % flatatt(final_attrs))+force_unicode(append)