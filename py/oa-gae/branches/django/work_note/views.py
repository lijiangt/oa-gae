# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.views.generic import list_detail,create_update,date_based
from django.http import HttpResponse  
import datetime
from django.template import RequestContext
from oa.work_note.models import Event,Period
from django import newforms as forms
from django.http import Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _lazy
from urllib import urlencode

from oa.commons.forms.widgets import JsDateTimeWidget
from oa.templatetags import title_field_html

class EventForm(forms.ModelForm):
    start = forms.DateTimeField(widget=JsDateTimeWidget(),label=_lazy('Start Time'))
    finish = forms.DateTimeField(widget=JsDateTimeWidget(),label=_lazy('Finish Time'),required=False)
    class Meta:
        model=Event
        exclude = ('owner', 'last_period','total_work_time',)
    def clean_finish(self):
        start = self.cleaned_data.get('start',None)
        finish = self.cleaned_data.get('finish',None)
        if start and finish and start>finish:
            raise forms.ValidationError('完成时间必须要在开始时间之后！')
        if finish:
            return finish

@login_required
def event_edit(request):
    if request.GET and request.GET.has_key('id'):
        object_id = request.GET['id']
        event = get_object_or_404(Event,pk=object_id)
        if event.owner.id != request.user.id:
            raise Http404
        f = EventForm(instance=event)
        return render_to_response('work_note/event_form.html', {
                'form':           f,
                "submit_times":   -1,
                'display_cancel':'true',
                'ext_query_str': request.GET.get('extQueryString',''),
                'id':             object_id,
                },context_instance=RequestContext(request))
    else:
#        return create_update.create_object(request,model=Event,extra_context={"submit_times":1})
        f = EventForm()
        return render_to_response('work_note/event_form.html', {
                'form':            f,
                "submit_times":   -1,
                'display_cancel':'true',
        },context_instance=RequestContext(request))
 
@login_required   
def event_index(request):
    if request.method == 'GET':
        pageSize = int(request.GET.get('pageSize',settings.DEFAUTL_PAGE_SIZE))
        pageNum = long(request.GET.get('pageNum',1))
        order_str = title_field_html.get_order_str(request)
        queryset = Event.objects.filter(owner=request.user)
        if order_str:
            queryset = queryset.order_by(order_str)
        return list_detail.object_list(request, 
                   queryset = queryset,
                   paginate_by=pageSize,
                   page=pageNum)  
    elif request.method == 'POST':
        f = EventForm(request.POST, request.FILES)
        if f.is_valid():
            event = f.save(commit=False)
            event.owner = request.user
            period = Period(start=event.start,finish=event.finish)
            if event.finish:
                delta = event.finish - event.start
                event.total_work_time = delta.days*24*3600 + delta.seconds
            event.save()
            period.event = event
            period.save()
            event.last_period = period
            event.save()
            return HttpResponseRedirect(event.id)
        else:
            return render_to_response('work_note/event_form.html', {
                    'form':        f,
                    "submit_times":int(request.POST['submit_times']) - 1,
                    'display_cancel':request.POST.get('display_cancel','true'),
                    },context_instance=RequestContext(request))
    raise Http404

@login_required
def will_do(request):
    pageSize = int(request.GET.get('pageSize',settings.DEFAUTL_PAGE_SIZE))
    pageNum = long(request.GET.get('pageNum',1))
    order_str = title_field_html.get_order_str(request)
    queryset = Event.objects.filter(owner=request.user,finish=None)
    if order_str:
        queryset = queryset.order_by(order_str)
    return list_detail.object_list(request,
                queryset = queryset,
                paginate_by=pageSize,
                page=pageNum)

@login_required
def by_month(request,year,month):
    pageSize = int(request.GET.get('pageSize',settings.DEFAUTL_PAGE_SIZE))
    pageNum = long(request.GET.get('pageNum',1))
    order_str = title_field_html.get_order_str(request)
    queryset = Event.objects.filter(owner=request.user)
    if order_str:
        queryset = queryset.order_by(order_str)
    return date_based.archive_month(request,
                                year,
                                month,
                                queryset=queryset,
                                date_field='finish',
                                month_format='%m',
                                template_name='work_note/event_list.html')

@login_required
def event_detail(request,object_id):
    if request.method == 'GET':
        return list_detail.object_detail(request,
                                 queryset= Event.objects.filter(owner=request.user),
                                 object_id=object_id)
    elif request.method == 'POST':
        method = request.POST.get(settings.EXTEND_HTTP_METHOD,None) 
        if method == 'PUT':
            event = get_object_or_404(Event,pk=object_id)
#            event = Event.objects.get(id__exact=int(object_id))
            if event.owner.id != request.user.id:
                raise Http404
            f = EventForm(request.POST, request.FILES,instance=event)
            if f.is_valid():
                f.save()
                ext_query_str = request.POST.get('ext_query_str','')
                if ext_query_str:
                    ext_query_str = '%s%s'%('?',urlencode({'extQueryString':ext_query_str}))
                return HttpResponseRedirect('%s%s'%(object_id,ext_query_str))
            else:
                return render_to_response('work_note/event_form.html', {
                                        'form':       f,
                                        "submit_times":int(request.POST['submit_times'])-1,
                                        'id':object_id,
                                        'display_cancel':request.POST.get('display_cancel','true'),
                                        'ext_query_str':request.POST.get('ext_query_str',''),
                                    },context_instance=RequestContext(request))
        elif method == 'DELETE':
            ext_query_str = request.POST.get('ext_query_str','')
            if ext_query_str:
                ext_query_str = '?'+ext_query_str
            return create_update.delete_object(request,
                               model=Event,
                               object_id=object_id,
                               post_delete_redirect='./%s'%ext_query_str)
    raise Http404
    
@login_required
def event_finish(request,object_id):
    event = get_object_or_404(Event,pk=object_id)
    if event.finish:
        raise Http500
    else:
        if not event.last_period.finish:
            event.last_period.finish = datetime.datetime.now()
            event.last_period.save()
        event.finish = event.last_period.finish
        event.update_total_work_time()
        event.save();
        ext_query_str = request.GET.get('extQueryString','')
        if ext_query_str:
            ext_query_str = '%s%s'%('?',urlencode({'extQueryString':ext_query_str}))
        return HttpResponseRedirect('%s%s'%(object_id,ext_query_str))

class PeriodForm(forms.ModelForm):
    start = forms.DateTimeField(widget=JsDateTimeWidget(),label=_lazy('Start Time'))
    finish = forms.DateTimeField(widget=JsDateTimeWidget(),label=_lazy('Finish Time'),required=False)
    class Meta:
        model=Period
        exclude = ('event',)
    def clean_finish(self):
        start = self.cleaned_data.get('start',None)
        finish = self.cleaned_data.get('finish',None)
        if start and finish and start>finish:
            raise forms.ValidationError('完成时间必须要在开始时间之后！')
        if finish:
            return finish
        
def period_finish(request,event_id):
    event = get_object_or_404(Event,pk=event_id)
    if event.last_period.finish:
        raise Http404
    event.last_period.finish = datetime.datetime.now()
    event.last_period.save()
    ext_query_str = request.GET.get('extQueryString','')
    print ext_query_str
    if ext_query_str:
        ext_query_str = '%s%s'%('?',urlencode({'extQueryString':ext_query_str}))
    return HttpResponseRedirect('%s%s'%('!edit',ext_query_str)) 
        
def period_edit(request,event_id):
    if request.GET and request.GET.has_key('id'):
        object_id = request.GET['id']
        period = get_object_or_404(Period,pk=object_id)
        if period.event.owner.id != request.user.id or period.event.id != int(event_id):
            raise Http404
        f = PeriodForm(instance=period)
        return render_to_response('work_note/period_form.html', {
                                     'form':            f,
                                     "submit_times":    -1,
                                     'id':              object_id,
                                     'display_cancel':  'true',
                                     'ext_query_str':   request.GET.get('extQueryString',''),
                             },context_instance=RequestContext(request))
    else:
        event = get_object_or_404(Event,pk=event_id)
        if event.owner.id != request.user.id:
            raise Http404
        f = PeriodForm()
        return render_to_response('work_note/period_form.html', {
                            'form':             f,
                            "submit_times":     -1,
                            'display_cancel':   'true',
                            'ext_query_str':    request.GET.get('extQueryString',''),
                },context_instance=RequestContext(request))

def period_create(request,event_id):
    if request.method == 'POST':
        f = PeriodForm(request.POST, request.FILES)
        if f.is_valid():
            event = get_object_or_404(Event,pk=event_id)
            period = f.save(commit=False)
            period.event = event
            period.save()
            event.last_period = period
            event.save()
            ext_query_str = request.POST.get('ext_query_str','')
            if ext_query_str:
                ext_query_str = '%s%s'%('?',urlencode({'extQueryString':ext_query_str}))
            return HttpResponseRedirect('../%s%s'%(event_id,ext_query_str))
        else:
            return render_to_response('work_note/period_form.html', {
                             'form':            f,
                             "submit_times":    int(request.POST['submit_times']) - 1,
                             'display_cancel':request.POST.get('display_cancel','true'),
                             'ext_query_str':request.POST.get('extQueryString','')
                     },context_instance=RequestContext(request))
    else:
        raise Http404
    
def period_detail(request,event_id,object_id):
    if request.method == 'POST':
        method = request.POST.get(settings.EXTEND_HTTP_METHOD,None) 
        if method == 'PUT':
            period = get_object_or_404(Period,pk=object_id)
            if period.event.owner.id != request.user.id:
                raise Http404
            f = PeriodForm(request.POST, request.FILES,instance=period)
            if f.is_valid():
                f.save()
                period.event.update_total_work_time()
                ext_query_str = request.POST.get('ext_query_str','')
                if ext_query_str:
                    ext_query_str = '%s%s'%('?',urlencode({'extQueryString':ext_query_str}))
                return HttpResponseRedirect('../%s%s'%(event_id,ext_query_str))
            else:
                return render_to_response('work_note/period_form.html', {
                             'form':             f,
                             "submit_times":    int(request.POST['submit_times'])-1,
                             'id':              object_id,
                             'display_cancel':  request.POST.get('display_cancel','true')
                     },context_instance=RequestContext(request))
            return None
        elif method == 'DELETE':
            ext_query_str = request.POST.get('ext_query_str','')
            if ext_query_str:
                ext_query_str = '%s%s'%('?',urlencode({'extQueryString':ext_query_str}))
            return create_update.delete_object(request,
                                   model=Period,
                                   object_id=object_id,
                                   post_delete_redirect='../%s%s'%(event_id,ext_query_str))
    raise Http404
        
    
    