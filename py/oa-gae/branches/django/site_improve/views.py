# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import list_detail, create_update
from django.http import HttpResponse  
import datetime
from django.template import RequestContext
from oa.site_improve.models import Bug,Content
from django import newforms as forms
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

from oa.templatetags import title_field_html

class BugForm(forms.ModelForm):
    class Meta:
        model=Content
        exclude = ('bug','version','modifier',)

@login_required
def bug_edit(request):
    if request.GET and request.GET.has_key('id'):
        id = request.GET['id']
        bug = get_object_or_404(Bug, pk=id)
        f = BugForm(instance=bug.current_content)
        return render_to_response('site_improve/bug_form.html', {'form':f, "submit_times":-1, 'display_cancel':'true', 'id':id}, context_instance=RequestContext(request))
    else:
        f = BugForm()
        return render_to_response('site_improve/bug_form.html', {'form':f, "submit_times":-1, 'display_cancel':'true'}, context_instance=RequestContext(request))
    
@login_required
def bug_index(request):
    if request.method == 'GET':
        pageSize = int(request.GET.get('pageSize',settings.DEFAUTL_PAGE_SIZE))
        pageNum = long(request.GET.get('pageNum',1))
        order_str = title_field_html.get_order_str(request)
        queryset = Bug.objects.filter()
        if order_str:
            queryset = queryset.order_by(order_str)
        return list_detail.object_list(request, 
                               queryset = queryset,
                               paginate_by=pageSize,
                               page=pageNum)  
    elif request.method == 'POST':
        f = BugForm(request.POST, request.FILES)
        if f.is_valid():
            bug = Bug()
            bug.save()
            content = f.save(commit=False)
            content.modifier = request.user
            content.bug = bug
            content.save()
            bug.current_content = content
            bug.save()
            return HttpResponseRedirect(bug.id)
        else:
            return render_to_response('site_improve/bug_form.html', {'form':f,"submit_times":int(request.POST['submit_times']) - 1,'display_cancel':request.POST.get('display_cancel','true')},context_instance=RequestContext(request))
    raise Http404

@login_required
def bug_my(request):
    pageSize = int(request.GET.get('pageSize',settings.DEFAUTL_PAGE_SIZE))
    pageNum = long(request.GET.get('pageNum',1))
    order_str = title_field_html.get_order_str(request)
    queryset = Bug.objects.filter(current_content__modifier=request.user)
    if order_str:
        queryset = queryset.order_by(order_str)
    return list_detail.object_list(request, 
                           queryset = queryset,
                           paginate_by=pageSize,
                           page=pageNum)  

@login_required
def bug_open(request):
    pageSize = int(request.GET.get('pageSize',settings.DEFAUTL_PAGE_SIZE))
    pageNum = long(request.GET.get('pageNum',1))
    order_str = title_field_html.get_order_str(request)
    queryset = Bug.objects.filter(current_content__status='open')
    if order_str:
        queryset = queryset.order_by(order_str)
    return list_detail.object_list(request, 
                           queryset = queryset,
                           paginate_by=pageSize,
                           page=pageNum)  

@login_required
def bug_detail(request,object_id):
    if request.method == 'GET':
        return list_detail.object_detail(request,queryset= Bug.objects.all(),object_id=object_id)
    elif request.method == 'POST':
        method = request.POST.get(settings.EXTEND_HTTP_METHOD,None) 
        if method == 'PUT':
            bug = get_object_or_404(Bug,pk=object_id)
            f = BugForm(request.POST, request.FILES)
            if f.is_valid():
                content = f.save(commit=False)
                content.modifier = request.user
                content.bug = bug
                content.save()
                bug.current_content = content
                bug.save()
                return HttpResponseRedirect(object_id)
            else:
                return render_to_response('site_improve/bug_form.html', {'form':f,"submit_times":int(request.POST['submit_times'])-1,'id':object_id,'display_cancel':request.POST.get('display_cancel','true')},context_instance=RequestContext(request))
        elif method == 'DELETE':
            if not request.user.is_staff:
                raise Http404
            return create_update.delete_object(request,model=Bug,object_id=object_id,post_delete_redirect='./')
    raise Http404
        