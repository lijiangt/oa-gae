# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from google.appengine.api import users
from google.appengine.ext.db import djangoforms
from google.appengine.ext import db
import models
def test(request):
#    domain = models.RedirectDomain(domain = 'test.lijiangt.cn',target_url = 'http://blog.lijiangt.cn',owner = users.get_current_user())
#    domain.save()
    return HttpResponse("Admin Test OK!")
    
    