# -*- mode: python; coding: utf-8; -*-

from django.conf.urls.defaults import *

from ovobot.ovolog import views

urlpatterns = patterns(
    '',
    url(r'^/$', views.index, name="index"),
#    url(r'^invite/(?P<hashstr>[a-z0-9]{56})/$', views.invite_click, name="invite_click"),
    )

