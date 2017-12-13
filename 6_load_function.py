#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

data_dir = sys.argv[1]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macaca.settings")
import django
if django.VERSION >= (1, 7):
	django.setup()

#load 