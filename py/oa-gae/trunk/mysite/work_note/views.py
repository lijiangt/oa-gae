# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext
from models import Event,Period
from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _lazy
from django.utils import simplejson

from google.appengine.api import users
from google.appengine.ext.db import djangoforms
from google.appengine.ext import db
from urllib import urlencode
import datetime
import logging
from commons.forms.widgets import JsDateTimeWidget
from commons.templatetags import title_field_html
from commons.utils import date
from commons.utils import collection

class EventForm(djangoforms.ModelForm):
    start = forms.DateTimeField(widget=JsDateTimeWidget(),label=_lazy('Start Time'))
    finish = forms.DateTimeField(widget=JsDateTimeWidget(),label=_lazy('Finish Time'),required=False)
    class Meta:
        model=Event
        exclude = ('owner', 'last_period','total_work_time','last_modified', 'created',)
    def clean_finish(self):
        start = self.cleaned_data.get('start',None)
        finish = self.cleaned_data.get('finish',None)
        if start and finish and start>finish:
            raise forms.ValidationError('完成时间必须要在开始时间之后！')
        if finish:
            return finish


def event_edit(request):
    if request.GET and request.GET.has_key('id'):
        id = request.GET['id']
        event = db.get(db.Key(id))
        if not event or event.owner != users.get_current_user():
            raise Http404
        f = EventForm(instance=event)
        return render_to_response('work_note/event_form.html', {
                'form':           f,
                "submit_times":   -1,
                'display_cancel':'true',
                'ext_query_str': request.GET.get('extQueryString',''),
                'id':             str(event.key()),
                },context_instance=RequestContext(request))
    else:
#        return create_update.create_object(request,model=Event,extra_context={"submit_times":1})
        f = EventForm()
        return render_to_response('work_note/event_form.html', {
                'form':            f,
                "submit_times":   -1,
                'display_cancel':'true',
        },context_instance=RequestContext(request))
 
   
def event_index(request):
    if request.method == 'GET':
        page_size = int(request.GET.get('pageSize',settings.DEFAUTL_PAGE_SIZE))
        page_num = long(request.GET.get('pageNum',1))
        order_str = title_field_html.get_order_str(request)
        query = Event.all().filter('owner =',users.get_current_user())
        if order_str:
            query = query.order(order_str)
        else:
            query = query.order('-start')
        context = title_field_html.pagination_context(query.count(),page_num,page_size)
        context['object_list'] = query.fetch(page_size,offset=(page_num-1)*page_size)
        return render_to_response('work_note/event_list.html',context,
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        f = EventForm(request.POST)
        if f.is_valid():
            event = f.save(commit=False)
            event.owner = users.get_current_user()
            period = Period(start=event.start,finish=event.finish)
            if event.finish:
                delta = event.finish - event.start
                event.total_work_time = delta.days*24*3600 + delta.seconds
            event.put()
            period.event = event
            period.put()
            event.set_last_period(period)
            event.put()
            logging.info('%s created event named %s.'%(users.get_current_user(),event.summary))
            return HttpResponseRedirect(str(event.key()))
        else:
            return render_to_response('work_note/event_form.html', {
                    'form':        f,
                    "submit_times":int(request.POST['submit_times']) - 1,
                    'display_cancel':request.POST.get('display_cancel','true'),
                    },context_instance=RequestContext(request))
    raise Http404


def will_do(request):
    page_size = int(request.GET.get('pageSize',settings.DEFAUTL_PAGE_SIZE))
    page_num = long(request.GET.get('pageNum',1))
    order_str = title_field_html.get_order_str(request)
    query = Event.all().filter('owner =',users.get_current_user())
    query = query.filter('finish =',None)
    if order_str:
        query = query.order(order_str)
    else:
        query = query.order('-start')
    context = title_field_html.pagination_context(query.count(),page_num,page_size)
    context['object_list'] = query.fetch(page_size,offset=(page_num-1)*page_size)
    return render_to_response('work_note/event_list.html',context,
                              context_instance=RequestContext(request))


def by_month(request,year,month):
    try:
        page_size = int(request.GET.get('pageSize',settings.DEFAUTL_PAGE_SIZE))
        page_num = long(request.GET.get('pageNum',1))
        order_str = title_field_html.get_order_str(request)
        query = Event.all().filter('owner =',users.get_current_user())
        datetime_interval = date.get_datetime_interval(int(year),int(month))
        query = query.filter('finish >=',datetime_interval[0])  
        query = query.filter('finish <',datetime_interval[1])
        query = query.order('finish')
        if order_str:
            query = query.order(order_str)
        else:
            query = query.order('-start')
        context = title_field_html.pagination_context(query.count(),page_num,page_size)
        context['object_list'] = query.fetch(page_size,offset=(page_num-1)*page_size)
        return render_to_response('work_note/event_list.html',context,
                                  context_instance=RequestContext(request))
    except BaseException,e:
        return HttpResponse(e.message)

def event_detail(request,id):
    if request.method == 'GET':
        event = db.get(db.Key(id))
        if not event or event.owner != users.get_current_user():
            raise Http404
        return render_to_response('work_note/event_detail.html', {
                    'object':        event,
                    },context_instance=RequestContext(request))
    elif request.method == 'POST':
        method = request.POST.get(settings.EXTEND_HTTP_METHOD,None) 
        if method == 'PUT':
            event = db.get(db.Key(id))
#            event = Event.objects.get(id__exact=int(id))
            if not event or event.owner != users.get_current_user():
                raise Http404
            f = EventForm(request.POST,instance=event)
            if f.is_valid():
                f.save()
                ext_query_str = request.POST.get('ext_query_str','')
                if ext_query_str:
                    ext_query_str = '%s%s'%('?',urlencode({'extQueryString':ext_query_str}))
                return HttpResponseRedirect('%s%s'%(id,ext_query_str))
            else:
                return render_to_response('work_note/event_form.html', {
                                        'form':       f,
                                        "submit_times":int(request.POST['submit_times'])-1,
                                        'id': str(event.key()),
                                        'display_cancel':request.POST.get('display_cancel','true'),
                                        'ext_query_str':request.POST.get('ext_query_str',''),
                                    },context_instance=RequestContext(request))
        elif method == 'DELETE':
            event = db.get(db.Key(id))
            if not event or event.owner != users.get_current_user():
                raise Http404
            for period in event.period_set:
                period.delete()
            event.delete()
            ext_query_str = request.POST.get('ext_query_str','')
            if ext_query_str:
                ext_query_str = '?'+ext_query_str
            return HttpResponseRedirect('./%s'%ext_query_str)
    raise Http404
    

def event_finish(request,id):
    event = db.get(db.Key(id))
    if not event or event.owner != users.get_current_user():
        raise Http404
    if event.finish:
        raise Http500
    else:
        last_period = event.get_last_period() 
        if not last_period.finish:
            last_period.finish = datetime.datetime.now()
            last_period.save()
        event.finish = last_period.finish
        event.update_total_work_time()
        event.save();
        ext_query_str = request.GET.get('extQueryString','')
        if ext_query_str:
            ext_query_str = '%s%s'%('?',urlencode({'extQueryString':ext_query_str}))
        return HttpResponseRedirect('%s%s'%(id,ext_query_str))

class PeriodForm(djangoforms.ModelForm):
    start = forms.DateTimeField(widget=JsDateTimeWidget(),label=_lazy('Start Time'))
    finish = forms.DateTimeField(widget=JsDateTimeWidget(),label=_lazy('Finish Time'),required=False)
    class Meta:
        model=Period
        exclude = ('event','last_modified','created',)
    def clean_finish(self):
        start = self.cleaned_data.get('start',None)
        finish = self.cleaned_data.get('finish',None)
        if start and finish and start>finish:
            raise forms.ValidationError('完成时间必须要在开始时间之后！')
        if finish:
            return finish
        
def period_finish(request,event_id):
    event = db.get(db.Key(event_id))
    if not event or event.owner != users.get_current_user():
        raise Http404
    last_period = event.get_last_period()
    if last_period.finish: 
        raise Http404
    last_period.finish = datetime.datetime.now()
    last_period.save()
    ext_query_str = request.GET.get('extQueryString','')
    if ext_query_str:
        ext_query_str = '%s%s'%('?',urlencode({'extQueryString':ext_query_str}))
    return HttpResponseRedirect('%s%s'%('!edit',ext_query_str)) 
        
def period_edit(request,event_id):
    if request.GET and request.GET.has_key('id'):
        id = request.GET['id']
        period = db.get(db.Key(id))
        if not period or period.event.owner != users.get_current_user() or str(period.event.key()) != event_id:
            raise Http404
        f = PeriodForm(instance=period)
        return render_to_response('work_note/period_form.html', {
                                     'form':            f,
                                     "submit_times":    -1,
                                     'id':              str(period.key()),
                                     'display_cancel':  'true',
                                     'ext_query_str':   request.GET.get('extQueryString',''),
                             },context_instance=RequestContext(request))
    else:
        event = db.get(db.Key(event_id))
        if not event or event.owner != users.get_current_user():
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
        f = PeriodForm(request.POST)
        if f.is_valid():
            event = db.get(db.Key(event_id))
            if not event or event.owner != users.get_current_user():
                raise Http404
            period = f.save(commit=False)
            period.event = event
            period.save()
            event.set_last_period(period)
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
    
def period_detail(request,event_id,id):
    if request.method == 'POST':
        method = request.POST.get(settings.EXTEND_HTTP_METHOD,None) 
        if method == 'PUT':
            period = db.get(db.Key(id))
            if not period or period.event.owner != users.get_current_user() or str(period.event.key()) != event_id:
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
                             'id':              str(period.key()),
                             'display_cancel':  request.POST.get('display_cancel','true')
                     },context_instance=RequestContext(request))
            return None
        elif method == 'DELETE':
            period = db.get(db.Key(id))
            if not period or period.event.owner != users.get_current_user() or str(period.event.key()) != event_id:
                raise Http404
            period.delete()
            ext_query_str = request.POST.get('ext_query_str','')
            if ext_query_str:
                ext_query_str = '%s%s'%('?',urlencode({'extQueryString':ext_query_str}))
            return HttpResponseRedirect('../%s%s'%(event_id,ext_query_str)) 
    raise Http404

def event_export(request):
    user = users.get_current_user()
    query = Event.all().filter('owner =',user).order('start')
    results = []
    for e in query.fetch(1000): # TODO:
        d = {'summary':e.summary,
              'start':e.start,
              'finish':e.finish, 
              'cooperation_dep':e.cooperation_dep,
              'content':e.content,
              'aim':e.aim,
              'resolved_problem':e.resolved_problem,
              'leave_problem':e.leave_problem,
              'total_work_time':e.total_work_time,
              'last_modified':e.last_modified,
              'created':e.created,}
        period_set = []
        for period in e.period_set:
            period_set.append({
                   'start':period.start,
                   'finish':period.finish,
                   'content':period.content,
                   'last_modified':period.last_modified,
                   'created':period.created,
                   'current':str(period.key())==e.last_period})
        d['period_set'] = period_set
        results.append(d)
    from django.core.serializers.json import DjangoJSONEncoder
    response = HttpResponse(simplejson.dumps(results,cls=DjangoJSONEncoder,sort_keys=True,indent=4),mimetype="text/plain")
    response['Content-Disposition'] = 'attachment; filename=%s_export.json'%user.email()
    return response

class ImportForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea,label=_lazy('JSON Format'))

def event_import_page(request):
    f = ImportForm()
    return render_to_response('work_note/import_export.html', {
            'form':            f,
            "submit_times":   -1,
            'display_cancel':'true',
    },context_instance=RequestContext(request))

def event_import(request):
    if request.method == 'POST':
        f = ImportForm(request.POST)
        if f.is_valid():
            content = request.POST.get('content',None)
            if content:
                l = simplejson.loads(content)
                user = users.get_current_user()
                for e in l:
                    event = EventForm(e).save(commit=False)
                    event.owner = user
                    event.last_modified = date.get_date_by_str(e['last_modified'],settings.DATETIME_FORMAT)
                    event.created = date.get_date_by_str(e['created'],settings.DATETIME_FORMAT)
                    event.total_work_time = e['total_work_time']
                    event.put()
                    logging.info('import event, its summary is %s.'%event.summary)
                    for p in e['period_set']:
                        period = PeriodForm(p).save(commit=False)
                        period.event = event
                        period.last_modified = date.get_date_by_str(p['last_modified'],settings.DATETIME_FORMAT)
                        period.created = date.get_date_by_str(p['created'],settings.DATETIME_FORMAT)
                        period.put()
                        if p['current']:
                            event.last_period = str(period.key())
                            event.put()
                return HttpResponseRedirect('./')
        else:
            return render_to_response('work_note/import_export.html', {
                             'form':             f,
                             "submit_times":    int(request.POST['submit_times'])-1,
                             'display_cancel':  request.POST.get('display_cancel','true')
                     },context_instance=RequestContext(request))
    raise Http404

