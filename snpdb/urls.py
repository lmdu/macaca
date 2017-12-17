#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path, re_path

from . import views

urlpatterns = [
	path('', views.index, name='home'),
	path('organism/', views.organism, name='organism'),
	path('species/<int:sid>', views.species, name='species'),
	path('group/', views.group, name='group'),
	path('variants/', views.variants, name='variants'),
	path('snp/<int:sid>/', views.snp, name='snp'),
	re_path(r'^snp/MACSNP(?P<indiv>[0-9]{2})(?P<chrom>[0-9]{2})(?P<sid>[0-9]{8})/$', views.snpid, name='snpid'),
	path('search/', views.search, name='search')
]