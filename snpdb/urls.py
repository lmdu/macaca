#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='home'),
	url(r'^organism/$', views.organism, name='organism'),
	url(r'^group/$', views.group, name='group'),
	url(r'^variants/$', views.variants, name='variants'),
	url(r'^snp/(?P<sid>[0-9]+)/$', views.snp, name='snp')
]