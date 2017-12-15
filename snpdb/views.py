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

def organism(request):
	pass

def group(request):
	pass

def variants(request):
	chromos = Chromosome.objects.all()[:20]
	species = Individual.objects.all()

	paras = dict(
		page = int(request.GET.get('page', 1)),
		records = int(request.GET.get('records', 10)),
		chromosome = int(request.GET.get('chr', 0)),
		sample = int(request.GET.get('sample', 0)),
		feature = int(request.GET.get('feature', 0)),
		genotype = int(request.GET.get('genotype', 0)),
		mutation = int(request.GET.get('mutation', 0))
	)

	snps = Variant.objects.all()

	if paras['sample']:
		snps = snps.filter(individual=paras['sample'])

	if paras['genotype']:
		snps = snps.filter(genotype=paras['genotype'])

	if paras['mutation']:
		snps = snps.filter(snp__transannot__synonymous=paras['mutation'])

	if paras['feature']:
		snps = snps.filter(snp__geneannot__feature=paras['feature'])

	if paras['chromosome']:
		snps = snps.filter(snp__chrom=paras['chromosome'])


	paginator = Paginator(snps, paras['records'])

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
	transcripts = one.snp.transannot_set.all()
	return render(request, 'snp.html', {
		'snp': one,
		'genes': genes,
		'transcripts': transcripts
	})
	
