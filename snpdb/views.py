# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Individual, Variant, Chromosome, Species, Snp, Group
from .models import GroupSpecific, SpeciesSpecific

# Create your views here.
def index(request):
	return render(request, 'index.html')

def organism(request):
	samples = Individual.objects.all()
	return render(request, 'organism.html', {
		'samples': samples,
	})

def species(request, sid):
	one = Species.objects.get(id=sid)
	return render(request, 'species.html', {
		'species': one,
	})


def group(request, gid):
	one = Group.objects.get(id=gid)
	return render(request, 'group.html', {
		'group': one,
	})

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
		snps = snps.filter(snp__mutation__synonymous=paras['mutation'])

	if paras['feature']:
		snps = snps.filter(snp__annotation__feature=paras['feature'])

	if paras['chromosome']:
		snps = snps.filter(snp__chromosome=paras['chromosome'])

	snps = snps.order_by('id')

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

#Get snp by variant id
def snp(request, sid):
	one = Variant.objects.get(id=sid)
	genes = one.snp.annotation_set.all()
	transcripts = one.snp.comment_set.all()
	return render(request, 'snp.html', {
		'snp': one,
		'genes': genes,
		'transcripts': transcripts
	})

#get snp by mac snp id
def snpid(request, indiv, sid):
	one = Variant.objects.get(snp__id=int(sid), individual__id=int(indiv))
	return snp(request, one.id)

def search(request):
	tag = request.GET.get('search')
	if tag.startswith('MACSNP'):
		i = int(tag[6:9])
		s = int(tag[9:])
		return snpid(request, i, s)
	
	chr_id = int(tag[3:5])
	start, end = map(int,tag.split(':')[1].split('-'))

	species = Individual.objects.all()
	chrom = Chromosome.objects.get(id=chr_id)
	paras = dict(
		chrname = chrom.name,
		start = start,
		end = end,
		tag = request.GET.get('search'),
		page = int(request.GET.get('page', 1)),
		records = int(request.GET.get('records', 10)),
		sample = int(request.GET.get('sample', 0)),
		feature = int(request.GET.get('feature', 0)),
		genotype = int(request.GET.get('genotype', 0)),
		mutation = int(request.GET.get('mutation', 0))
	)

	snps = Variant.objects.filter(snp__chromosome=chr_id).filter(snp__position__range=(start, end))

	if paras['sample']:
		snps = snps.filter(individual=paras['sample'])

	if paras['genotype']:
		snps = snps.filter(genotype=paras['genotype'])

	if paras['mutation']:
		snps = snps.filter(snp__mutation__synonymous=paras['mutation'])

	if paras['feature']:
		snps = snps.filter(snp__annotation__feature=paras['feature'])


	paginator = Paginator(snps, paras['records'])

	try:
		snps = paginator.page(paras['page'])
	except PageNotAnInteger:
		snps = paginator.page(1)
	except EmptyPage:
		snps = paginator.page(paginator.num_pages)

	return render(request, 'search.html', {
		'snps': snps,
		'species': species,
		'paras': paras,
	})

def specific(request):
	chromos = Chromosome.objects.all()[:20]
	groups = Group.objects.all()
	species = Species.objects.all()
	paras = dict(
		page = int(request.GET.get('page', 1)),
		records = int(request.GET.get('records', 10)),
		chromosome = int(request.GET.get('chr', 0)),
		feature = int(request.GET.get('feature', 0)),
		mutation = int(request.GET.get('mutation', 0)),
		group = int(request.GET.get('group', -1)),
		species = int(request.GET.get('species', 0)),
	)

	if paras['group'] >= 0:
		if paras['group'] == 0:
			snps = GroupSpecific.objects.all()
		else:
			snps = GroupSpecific.objects.filter(group=paras['group'])
	elif paras['species'] >= 0:
		if paras['species'] == 0:
			snps = SpeciesSpecific.objects.all()
		else:
			snps = SpeciesSpecific.objects.filter(species=paras['species'])

	if paras['mutation']:
		snps = snps.filter(snp__mutation__synonymous=paras['mutation'])

	if paras['feature']:
		snps = snps.filter(snp__annotation__feature=paras['feature'])

	if paras['chromosome']:
		snps = snps.filter(snp__chromosome=paras['chromosome'])
	
	paginator = Paginator(snps, paras['records'])

	try:
		snps = paginator.page(paras['page'])
	except PageNotAnInteger:
		snps = paginator.page(1)
	except EmptyPage:
		snps = paginator.page(paginator.num_pages)

	return render(request, 'specific.html', {
		'snps': snps,
		'chromos': chromos,
		'groups': groups,
		'species': species,
		'paras': paras,
	})

def snpspec(request, cat, cid, sid):
	if cat == 'G':
		category = Group.objects.get(id=int(cid))
	else:
		category = Species.objects.get(id=int(cid))
	one = Snp.objects.get(id=int(sid))
	genes = one.annotation_set.all()
	transcripts = one.comment_set.all()
	return render(request, 'snpspec.html', {
		'cat': cat,
		'snp': one,
		'category': category,
		'genes': genes,
		'transcripts': transcripts
	})