#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import defaultfilters
from django.urls import reverse

from jinja2 import Environment

def format_codon(codon, pos):
	pos -= 1
	bs = []
	for i, b in enumerate(codon):
		if i == pos:
			bs.append(r'<span style="color:red;">%s</span>' % b)
		else:
			bs.append(b)
	return "".join(bs)

def format_seq(seq):
	return "".join([r'<span class="{0}">{0}</span>'.format(b) for b in seq])

def environment(**options):
	env = Environment(**options)
	env.globals.update({
		'static': staticfiles_storage.url,
		'url': reverse,
		'djfilters': defaultfilters,
	})
	env.filters['format_codon'] = format_codon
	env.filters['format_seq'] = format_seq
	return env

