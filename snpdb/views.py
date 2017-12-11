# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Species
from .models import Variant
from .models import Chromosome

# Create your views here.
def index(request):
	chromos = Chromosome.objects.all()[:20]
	species = Species.objects.all()

	snp_list = Variant.objects.all()
	paginator = Paginator(snp_list, 10)
	page = request.GET.get('page')

	try:
		snps = paginator.page(page)
	except PageNotAnInteger:
		snps = paginator.page(1)
	except EmptyPage:
		snps = paginator.page(paginator.num_pages)

	return render(request, 'index.html', {
		'snps': snps,
		'chromos': chromos,
		'species': species
	})

def snp(request, sid):
	one = Variant.objects.get(id=int(sid))
	genes = one.snp.geneannot_set.all()
	return render(request, 'snp.html', {'snp': one, 'genes': genes})
	
