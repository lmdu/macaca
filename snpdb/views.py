# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Individual
from .models import Variant
from .models import Chromosome

# Create your views here.
def index(request):
	pass

def variants(request):
	chromos = Chromosome.objects.all()[:20]
	species = Individual.objects.all()

	paras = dict(
		page = int(request.GET.get('page', 1)),
		per = int(request.GET.get('per', 10)),
		chrom = int(request.GET.get('chr', 0)),
		indiv = int(request.GET.get('indiv', 0)),
		feat = int(request.GET.get('feat', 0))
	)

	snps = Variant.objects
	if paras['indiv']:
		snps = snps.filter(individual=paras['indiv'])

	if paras['feat']:
		snps = snps.filter(snp__geneannot__feature=paras['feat'])

	if paras['chrom']:
		snps = snps.filter(snp__chrom=paras['chrom'])


	

	paginator = Paginator(snps, paras['per'])

	try:
		snps = paginator.page(paras['page'])
	except PageNotAnInteger:
		snps = paginator.page(1)
	except EmptyPage:
		snps = paginator.page(paginator.num_pages)

	return render(request, 'variants.html', {
		'snps': snps,
		'chromos': chromos,
		'species': species,
		'paras': paras
	})



def snp(request, sid):
	one = Variant.objects.get(id=int(sid))
	genes = one.snp.geneannot_set.all()
	return render(request, 'snp.html', {'snp': one, 'genes': genes})
	
