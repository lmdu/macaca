#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^snp/(?P<sid>[0-9]+)/$', views.snp, name="snp")
]