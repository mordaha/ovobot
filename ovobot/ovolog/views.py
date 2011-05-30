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
from django.conf import settings

from ovobot.ovolog.models import *
from ovobot.captcha.fields import CaptchaField

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

#
#
#
def index(req):

    # TODO: rewrite this to token-based auth 
    if req.user.is_anonymous():
        ip = req.META.get('REMOTE_ADDR', '127.0.0.1')

        if settings.DEBUG:
            ip = settings.DEBUG_IP

        nick_list = LogEntry.objects.filter(user_ip=ip, timestamp__gte=datetime.date.today()).order_by('-id')
        nick = ''
        for obj in nick_list:
            nick = obj.get_nick()
            break

        if not nick:
            return HttpResponseRedirect('/nomercy/')

    channel = req.GET.get('channel', settings.IRC_CHANNELS[0])
    object_list = LogEntry.objects.filter(timestamp__gte=datetime.date.today(),
                        channel=channel).order_by('timestamp')

    chaannel_list = LogEntry.objects.all().values('channel').distinct()

    return render_to_response('ovolog/index.html', context_instance=RequestContext(req, locals()))


#
#
#
class  LoginForm(forms.Form):
    username = forms.CharField(label='Секретное имя:')
    password = forms.CharField(label='Секретное слово:', widget=forms.PasswordInput)
    captcha = CaptchaField(label=u'Капча:')


@cache_page(5)
@transaction.commit_on_success
def nomercy(req):

    if not req.user.is_anonymous():
        return HttpResponseRedirect('/')

    if req.POST:
        form = LoginForm(req.POST.copy())
        if form.is_valid():
            u = authenticate(username = form.cleaned_data.get('username'), password = form.cleaned_data.get('password'))
            if u is not None:
                auth_login(req, u)
                req.COOKIES['username'] = form.cleaned_data.get('username')
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('.')
    else:
        form = LoginForm( initial = {'username': req.COOKIES.get('username'), } )

    return render_to_response('ovolog/nomercy.html', context_instance=RequestContext(req, locals()))
