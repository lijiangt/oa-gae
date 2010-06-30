# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from google.appengine.api import users
from google.appengine.ext.db import djangoforms
from google.appengine.ext import db
from redirect import models

import logging as logger

def redirect(request,uri):
    uri = request.get_full_path()
    domain = request.META['SERVER_NAME']
    
    log = models.VisitLog(domain = domain,visit_url = request.build_absolute_uri(),visitor = users.get_current_user())
#    log = models.VisitLog(domain = domain,visit_url = 'http://%s%s'%(domain,request.get_full_path()),visitor = users.get_current_user())
    log.request_method = request.method
    log.client_ip = request.META.get('REMOTE_ADDR',None)
    log.referrer_url = request.META.get('HTTP_REFERER',None)
#    log.session_id = request.session
    headers = ''
    for key in request.META.keys():
        headers += '%s: %s\n'%(str(key),str(request.META[key]))
    log.headers = headers
    results = models.RedirectDomain.gql("WHERE domain = :domain",domain=domain).fetch(3)
    if results:
        if len(results) >1:
            logger.warn('have more than one domain named %s.'%domain)
        redirectDomain = results[0]
        target_url = None
        if uri and redirectDomain.full_path_redirect:
            target_url = '%s%s'%(redirectDomain.full_path_redirect,uri)
        else:
            target_url = redirectDomain.target_url
        log.target_url = target_url
        log.save()
        return HttpResponseRedirect(target_url)
        
#        if domain.endswith('appspot.com') or domain == 'localhost' or domain == '127.0.0.1':
    log.save()
    return HttpResponse("URL Redirector Site!");



