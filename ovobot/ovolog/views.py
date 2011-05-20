#!python
# coding: utf8

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.decorators import permission_required
from django import forms
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import *
from django.utils.datastructures import *
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import datetime

from ovobot.ovolog.models import *


def index(req):
    object_list = LogEntry.objects.filter(timestamp__gte=datetime.date.today()).order_by('-timestamp')
    
    return render_to_response('ovolog/index.html', context_instance=RequestContext(req, locals()))
