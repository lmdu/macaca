# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Species
from .models import Variant

# Create your views here.
def index(request):
	variants = Variant.objects.all()[:10]
	return render(request, 'snpdb/index.html', {'snps': variants})
	
