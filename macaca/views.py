# -*- coding: utf-8 -*-
import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import *

# Create your views here.
def home(request):
	return render(request, 'macaca/home.html')

def organism(request):
	samples = Individual.objects.all()
	return render(request, 'macaca/organism.html', {
		'samples': samples,
	})

def species(request, sid):
	one = Species.objects.get(id=sid)
	return render(request, 'macaca/species.html', {
		'species': one,
	})


def group(request, gid):
	one = Groups.objects.get(id=gid)
	return render(request, 'macaca/group.html', {
		'group': one,
	})

def individual_snps(request):
	chromos = Chromosome.objects.all()[:20]
	species = Individual.objects.all()

	paras = dict(
		page = int(request.GET.get('page', 1)),
		records = int(request.GET.get('records', 10)),
		chromosome = int(request.GET.get('chr', 1)),
		sample = int(request.GET.get('sample', 0)),
		feature = int(request.GET.get('feature', 0)),
		genotype = int(request.GET.get('genotype', 0)),
		mutation = int(request.GET.get('mutation', 0)),
	)

	Snps.shard(paras['chromosome'])
	
	snps = Variants.shard(paras['chromosome']).objects.all()

	if paras['sample']:
		snps = snps.filter(individual=paras['sample'])

	if paras['mutation']:
		snps = snps.filter(snp__mutation__synonymous=paras['mutation'])

	if paras['feature']:
		snps = snps.filter(snp__gannot__feature=paras['feature'])

	if paras['genotype']:
		snps = snps.filter(genotype=paras['genotype'])

	paginator = Paginator(snps, paras['records'])

	try:
		snps = paginator.page(paras['page'])
	except PageNotAnInteger:
		snps = paginator.page(1)
	except EmptyPage:
		snps = paginator.page(paginator.num_pages)

	return render(request, 'macaca/isnps.html', {
		'snps': snps,
		'chromos': chromos,
		'species': species,
		'paras': paras
	})

@csrf_exempt
def nrsnps(request):
	if request.method == 'GET':
		chromos = Chromosome.objects.all()[:20]
		species = Individual.objects.all()
		labels = [s.code for s in species]

		paras = dict(
			page = int(request.GET.get('page', 1)),
			records = int(request.GET.get('records', 10)),
			chromosome = int(request.GET.get('chr', 1)),
			feature = int(request.GET.get('feature', 0)),
			mutation = int(request.GET.get('mutation', 0)),
			samples = request.GET.getlist('samples'),
		)

		return render(request, 'macaca/nrsnps.html', {
			'species': species,
			'labels': labels,
			'paras': paras
		})

	elif request.method == 'POST':
		paras = json.loads(request.body)

		snps = Snps.shard(paras['chromosome']).objects.all()

		if paras['mutation']:
			snps = snps.filter(mutation__synonymous=paras['mutation'])

		if paras['feature']:
			snps = snps.filter(gannot__feature=paras['feature'])

		paginator = Paginator(snps, paras['records'])

		try:
			snps = paginator.page(paras['page'])
		except PageNotAnInteger:
			snps = paginator.page(1)
		except EmptyPage:
			snps = paginator.page(paginator.num_pages)

		paras['total'] = snps.paginator.count
		paras['page'] = snps.number
		paras['pages'] = snps.paginator.num_pages
		paras['prev'] = snps.previous_page_number() if snps.has_previous() else 0
		paras['next'] = snps.next_page_number() if snps.has_next() else 0

		variants = [{'id': snp.pk, 'chr': snp.chromosome.pk, 'pos': snp.position, 'ref': snp.reference, 'alt': snp.alteration} for snp in snps]
		snp_ids = [snp.id for snp in snps]

		genotypes = {}
		vs = Variants.shard(paras['chromosome']).objects.filter(snp__in=snp_ids)
		ns = Nonvariants.shard(paras['chromosome']).objects.filter(snp__in=snp_ids)
		for v in vs:
			genotypes[(v.snp.id, v.individual.id)] = v.genotype

		for n in ns:
			genotypes[(n.snp.id, n.individual.id)] = 3

		matrix = []
		for i in range(20):
			matrix.append([])
			for j, sid in enumerate(snp_ids):
				g = genotypes.get((sid, i+1), 0)
				matrix[i].append({'x': j, 'y': i, 'g': g})

		species = [s.species.common for s in Individual.objects.all()]

		return JsonResponse({'variants': variants, 'matrix': matrix, 'species': species, 'paras': paras})

def nonredundant_snp(request, chrom, sid):
	chrom = int(chrom)
	sid = int(sid)
	try:
		snp = Snps.shard(chrom).objects.get(id=sid)
	except ObjectDoesNotExist:
		raise Http404('MACSNVR%02d%09d does not exists in this database' % (chrom, sid))

	genes = snp.gannot_set.all()
	transcripts = snp.tannot_set.all()
	vs = Variants.shard(snp.chromosome.id).objects.filter(snp__pk=sid)
	ns = Nonvariants.shard(snp.chromosome.id).objects.filter(snp__pk=sid)

	genotypes = {}
	for v in vs:
		genotypes[v.individual.id] = v.genotype
	for n in ns:
		genotypes[n.individual.id] = 3

	samples = Individual.objects.all()

	return render(request, 'macaca/nrsnp.html', {
		'snp': snp,
		'genes': genes,
		'transcripts': transcripts,
		'genotypes': genotypes,
		'samples': samples,
	})


#get snp by mac snp id
def individual_snp(request, indiv, sid):
	indiv = int(indiv)
	sid = int(sid)
	try:
		snp = Snp.objects.get(id=sid)
		Snps.shard(snp.chromosome.id)
		one = Variants.shard(snp.chromosome.id).objects.get(individual__id=indiv,snp__id=sid)
	except ObjectDoesNotExist:
		raise Http404('MACSNV%03d%09d does not exists in this database' % (indiv, sid))
	genes = one.snp.gannot_set.all()
	transcripts = one.snp.tannot_set.all()
	vs = Variants.shard(snp.chromosome.id).objects.filter(snp__pk=sid).exclude(individual__id=indiv)
	ns = Nonvariants.shard(snp.chromosome.id).objects.filter(snp__pk=sid)
	genotypes = {}
	for v in vs:
		genotypes[v.individual.id] = v.genotype
	for n in ns:
		genotypes[n.individual.id] = 3

	samples = Individual.objects.exclude(pk=indiv)

	return render(request, 'macaca/snp.html', {
		'snp': one,
		'genes': genes,
		'transcripts': transcripts,
		'genotypes': genotypes,
		'samples': samples,
	})


def search(request):
	q = request.GET.get('q')
	q = q.strip()

	if not q:
		return HttpResponse("Please input search content")
	
	if q.startswith(('MACSNVG', 'MACSNVS')) and len(q) == 18:
		cat, cid, sid = q[6], q[7:9], q[9:]

		cid = int(cid)
		sid = int(sid)
		if cat == 'G' and GroupSpecific.objects.filter(snp=sid).exists():
			return redirect('macsnvdb:ssnp', cat, cid, sid)
		elif cat == 'S' and SpeciesSpecific.objects.filter(snp=sid).exists():
			return redirect('macsnvdb:ssnp', cat, cid, sid)

	if q.startswith('MACSNV') and len(q) == 18:
		indiv, sid= q[6:9], q[9:]
		if Variant.objects.filter(individual=int(indiv), snp=int(sid)).exists():
			return redirect('macsnvdb:isnp', indiv, sid)

	if q.startswith('MACSNVC') and len(q) == 18:
		chrom, sid = q[7:9], q[9:]

		if Snp.objects.filter(pk=int(sid)).exists():
			return redirect('macsnvdb:nrsnp', chrom, sid)

	if q.startswith('ENSMMUG') and len(q) == 18:
		if Gene.objects.filter(ensembl=q).exists():
			return redirect('macsnvdb:gene', q)

	if q.startswith('DB') and len(q) == 7:
		if Drug.objects.filter(drug_id=q).exists():
			return redirect('macsnvdb:drug', q)

	if q.isdigit() and len(q) == 6:
		if Disease.objects.filter(pomim=q).exists():
			return redirect('macsnvdb:disease', q)
	
	genes = Gene.objects.filter(Q(ensembl__icontains=q)
		| Q(name__icontains=q)
		| Q(description__icontains=q)
	)

	paras = dict(
		page = int(request.GET.get('page', 1)),
		records = int(request.GET.get('records', 10)),
		tag = q
	)

	paginator = Paginator(genes, paras['records'])

	try:
		genes = paginator.page(paras['page'])
	except PageNotAnInteger:
		genes = paginator.page(1)
	except EmptyPage:
		genes = paginator.page(paginator.num_pages)

	return render(request, 'macaca/search.html', {
		'paras': paras,
		'genes': genes
	})

def specific_snps(request):
	groups = Groups.objects.all()
	species = Species.objects.all()
	paras = dict(
		page = int(request.GET.get('page', 1)),
		records = int(request.GET.get('records', 10)),
		chromosome = int(request.GET.get('chr', 1)),
		feature = int(request.GET.get('feature', 0)),
		mutation = int(request.GET.get('mutation', 0)),
		group = int(request.GET.get('group', -1)),
		species = int(request.GET.get('species', 0)),
	)

	Snps.shard(paras['chromosome'])

	if paras['group'] >= 0:
		if paras['group'] == 0:
			snps = GroupSpecific.objects.filter(chromosome=paras['chromosome'])
		else:
			snps = GroupSpecific.objects.filter(group=paras['group'], chromosome=paras['chromosome'])
	elif paras['species'] >= 0:
		if paras['species'] == 0:
			snps = SpeciesSpecific.objects.filter(chromosome=paras['chromosome'])
		else:
			snps = SpeciesSpecific.objects.filter(species=paras['species'], chromosome=paras['chromosome'])

	if paras['mutation']:
		snps = snps.filter(snp__mutation__synonymous=paras['mutation'])

	if paras['feature']:
		snps = snps.filter(snp__gannot__feature=paras['feature'])
	
	paginator = Paginator(snps, paras['records'])

	try:
		snps = paginator.page(paras['page'])
	except PageNotAnInteger:
		snps = paginator.page(1)
	except EmptyPage:
		snps = paginator.page(paginator.num_pages)

	return render(request, 'macaca/specific.html', {
		'snps': snps,
		'groups': groups,
		'species': species,
		'paras': paras,
	})

def specific_snp(request, cat, cid, sid):
	cid = int(cid)
	sid = int(sid)
	if cat == 'G':
		category = Groups.objects.get(id=cid)
	else:
		category = Species.objects.get(id=cid)
	
	snp = Snp.objects.get(id=sid)
	snp = Snps.shard(snp.chromosome.id).objects.get(id=sid)

	genes = snp.gannot_set.all()
	transcripts = snp.tannot_set.all()

	vs = Variants.shard(snp.chromosome.id).objects.filter(snp__pk=sid)
	ns = Nonvariants.shard(snp.chromosome.id).objects.filter(snp__pk=sid)

	genotypes = {}
	for v in vs:
		genotypes[v.individual.id] = v.genotype
	for n in ns:
		genotypes[n.individual.id] = 3

	samples = Individual.objects.all()

	return render(request, 'macaca/snpspec.html', {
		'cat': cat,
		'snp': snp,
		'category': category,
		'genes': genes,
		'transcripts': transcripts,
		'genotypes': genotypes,
		'samples': samples,
	})

def retrieve(request):
	if not request.GET:
		individuals = Individual.objects.all()
		groups = Groups.objects.all()
		species = Species.objects.all()
		return render(request, 'macaca/retrieve.html', {
			'individuals': individuals,
			'groups': groups,
			'species': species,
		})

	
	#print(request.GET.getlist('individuals'))
	#return HttpResponse()
	paras = dict(
		page = int(request.GET.get('page', 1)),
		records = int(request.GET.get('records', 10)),
		chromosome = int(request.GET.get('chr')),
		start = request.GET.get('start', 0),
		end = request.GET.get('end', 0),
		category = request.GET.get('category', 'individual'),
		individual = int(request.GET.get('individual')),
		group = int(request.GET.get('group')),
		species = int(request.GET.get('species')),
		feature = int(request.GET.get('feature')),
		genotype = int(request.GET.get('genotype')),
		mutation = int(request.GET.get('mutation')),
		samples = request.GET.getlist('samples'),
		gene_type = request.GET.get('idtype'),
		gene_id = request.GET.get('gene'),
	)
	
	sample_ids = list(map(int, paras['samples']))
	
	paras['start'] = int(paras['start']) if paras['start'] else 0
	paras['end'] = int(paras['end']) if paras['end'] else 0

	Snps.shard(paras['chromosome'])

	if paras['category'] == 'group':
		snps = GroupSpecific.objects.filter(group=paras['group'], chromosome=paras['chromosome'])
		organism = Groups.objects.get(pk=paras['group'])
	elif paras['category'] == 'species':
		snps = SpeciesSpecific.objects.filter(species=paras['species'], chromosome=paras['chromosome'])
		organism = Species.objects.get(pk=paras['species'])
	elif paras['category'] == 'individual':
		snps = Variants.shard(paras['chromosome']).objects.filter(individual=paras['individual'])
		organism = Individual.objects.get(pk=paras['individual'])

		if paras['genotype']:
			snps = snps.filter(genotype=paras['genotype'])
	
	elif paras['category'] == 'nrsnps':
		snps = Snps.shard(paras['chromosome']).objects.all()
		organism = Individual.objects.filter(pk__in=sample_ids)

	if paras['start'] and paras['end']:
		if paras['category'] == 'nrsnps':
			snps = snps.filter(position__range=(paras['start'], paras['end']))
		else:
			snps = snps.filter(snp__position__range=(paras['start'], paras['end']))

	if paras['feature']:
		if paras['category'] == 'nrsnps':
			snps = snps.filter(gannot__feature=paras['feature'])
		else:
			snps = snps.filter(snp__gannot__feature=paras['feature'])

	if paras['mutation']:
		if paras['category'] == 'nrsnps':
			snps = snps.filter(mutation__synonymous=paras['mutation'])
		else:
			snps = snps.filter(snp__mutation__synonymous=paras['mutation'])

	if paras['gene_id']:
		if paras['category'] == 'nrsnps':
			if paras['gene_type'] == 'ensembl':
				snps = snps.filter(gannot__gene__ensembl=paras['gene_id'])
			elif paras['gene_type'] == 'drug':
				snps = snps.filter(gannot__gene__orthology__drug__drug_id=paras['gene_id'])
			elif paras['gene_type'] == 'disease':
				snps = snps.filter(gannot__gene__orthology__disease__pomim=paras['gene_id'])
		else:

			if paras['gene_type'] == 'ensembl':
				snps = snps.filter(snp__gannot__gene__ensembl=paras['gene_id'])
			elif paras['gene_type'] == 'drug':
				snps = snps.filter(snp__gannot__gene__orthology__drug__drug_id=paras['gene_id'])
			elif paras['gene_type'] == 'disease':
				snps = snps.filter(snp__gannot__gene__orthology__disease__pomim=paras['gene_id'])


	paginator = Paginator(snps, paras['records'])
	try:
		snps = paginator.page(paras['page'])
	except PageNotAnInteger:
		snps = paginator.page(1)
	except EmptyPage:
		snps = paginator.page(paginator.num_pages)

	variants = {}
	if paras['category'] == 'nrsnps':
		snp_ids = [snp.id for snp in snps]
		vs = Variants.shard(paras['chromosome']).objects.filter(snp__in=snp_ids, individual__in=sample_ids)
		ns = Nonvariants.shard(paras['chromosome']).objects.filter(snp__in=snp_ids, individual__in=sample_ids)
		for v in vs:
			variants[(v.snp.id, v.individual.id)] = v.genotype
		for n in ns:
			variants[(n.snp.id, n.individual.id)] = 3

	if paras['category'] == 'nrsnps':
		tpl = 'macaca/download_nrsnps.html'
	else:
		tpl = 'macaca/download.html'

	return render(request, tpl, {
		'snps': snps,
		'organism': organism,
		'paras': paras,
		'variants': variants,
	})

def download(request):
	if request.method == 'GET':
		raise Http404('Can not be accessed!')
	snp_ids = list(map(int,request.POST.getlist('snps')))
	sample_ids = list(map(int,request.POST.getlist('samples')))
	category = request.POST.get('category')
	chromosome = int(request.POST.get('chromosome'))
	individual = int(request.POST.get('individual'))
	
	if category == 'group':
		snps = GroupSpecific.objects.filter(snp__in=snp_ids)
	elif category == 'species':
		snps = SpeciesSpecific.objects.filter(snp__in=snp_ids)
	elif category == 'individual':
		snps = Variants.shard(chromosome).objects.filter(snp__in=snp_ids, individual=individual)
	elif category == 'nrsnps':
		variants = {}
		snps = Snps.shard(chromosome).objects.filter(pk__in=snp_ids)
		vs = Variants.shard(chromosome).objects.filter(snp__in=snp_ids, individual__in=sample_ids)
		ns = Nonvariants.shard(chromosome).objects.filter(snp__in=snp_ids, individual__in=sample_ids)
		for v in vs:
			variants[(v.snp.id, v.individual.id)] = v.genotype
		for n in ns:
			variants[(n.snp.id, n.individual.id)] = 3

	samples = Individual.objects.filter(pk__in=sample_ids)

	sample_info =  " (" + " ".join([s.code for s in samples]) + ")\n"
	contents = ["ID\tChromosome\tPosition\tRef\tAlt\t5'flank\t3'flank\tGene:Location\tGenotype" + sample_info]

	out_formats = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
	for snp in snps:
		if category == 'group':
			sid = "MACSNVG%02d%09d" % (snp.group.id, snp.snp.id)
			genotype = '1/1'
		
		elif category == 'species':
			sid = "MACSNVS%02d%09d" % (snp.species.id, snp.snp.id)
			genotype = '1/1'
		
		elif category == 'individual':
			sid = "MACSNV%03d%09d" % (snp.individual.id, snp.snp.id)
			genotype = '1/1' if snp.genotype == 1 else '0/1'
		
		elif category == 'nrsnps':
			types = {1: '1/1', 2: '0/1', 3: '0/0', 4: '.'}
			sid = "MACSNVR%02d%09d" % (snp.chromosome.pk, snp.id)
			genotype = " ".join([types.get(variants.get((snp.pk, s.id), 4)) for s in samples])

		if category == 'nrsnps':
			genes = "|".join(["%s:%s" % (gene.gene.ensembl, gene.get_feature_display()) for gene in snp.gannot_set.all()])
		else:
			genes = "|".join(["%s:%s" % (gene.gene.ensembl, gene.get_feature_display()) for gene in snp.snp.gannot_set.all()])
		
		if not genes:
			genes = 'Intergenic'

		if category == 'nrsnps':
			contents.append(out_formats % (
				sid, snp.chromosome.name, snp.position, snp.reference,
				snp.alteration, snp.five, snp.three, genes, genotype
			))

		else:
			contents.append(out_formats % (
				sid, snp.snp.chromosome.name, snp.snp.position,
				snp.snp.reference, snp.snp.alteration,
				snp.snp.five, snp.snp.three, genes, genotype
			))

	return HttpResponse('<pre>'+''.join(contents)+'</pre>')

def gene(request, gid):
	gene = Gene.objects.get(ensembl=gid)
	transcripts = gene.transcript_set.all()
	orthologys = gene.orthology_set.all()
	gos = gene.funcannot_set.filter(function__source=1)
	keggs = gene.funcannot_set.filter(function__source=2)
	ips = gene.funcannot_set.filter(function__source=3)
	pfams = gene.funcannot_set.filter(function__source=4)
	
	return render(request, 'macaca/gene.html', {
		'gene': gene,
		'transcripts': transcripts,
		'orthologys': orthologys,
		'gos': gos,
		'keggs': keggs,
		'ips': ips,
		'pfams': pfams,
	})

@csrf_exempt
def drugs(request):
	if request.method == 'GET':
		return render(request, 'macaca/drugs.html')
	
	elif request.method == 'POST':
		order = int(request.POST.get('order[0][column]'))
		order_dir = request.POST.get('order[0][dir]')
		search = request.POST.get('search[value]')
		start = int(request.POST.get('start'))
		length = int(request.POST.get('length'))
		total_count = Drug.objects.count()
		filter_count = total_count
		
		drugs = Drug.objects.all()
		if search:
			drugs = drugs.filter(
				Q(orthology__gene__ensembl__contains=search)
				| Q(orthology__gene__name__contains=search)
				| Q(orthology__gene__description__contains=search)
				| Q(drug_id__contains=search)
			)
			filter_count = drugs.count()

		sign = '-' if order_dir == 'desc' else ''
		if order == 0:
			drugs = drugs.order_by('{}orthology__gene__ensembl'.format(sign))
		elif order == 1:
			drugs = drugs.order_by('{}orthology__gene__name'.format(sign))
		elif order == 2:
			drugs = drugs.order_by('{}orthology__gene__description'.format(sign))
		elif order == 3:
			drugs = drugs.order_by('{}drug_id'.format(sign))

		drugs = drugs[start:start+length]

		rows = []
		for drug in drugs:
			row = []
			snp_count = Gannot.objects.filter(feature=1, gene__ensembl=drug.orthology.gene.ensembl).count()
			row.append('<a href="{}">{}</a>'.format(reverse('macsnvdb:gene', kwargs={'gid':drug.orthology.gene.ensembl}), drug.orthology.gene.ensembl))
			row.append(drug.orthology.gene.name)
			row.append(drug.orthology.gene.description)
			row.append('<a href="{}">{}</a>'.format(reverse('macsnvdb:drug', kwargs={'did': drug.drug_id}), drug.drug_id))
			row.append('<a href="{}">{}</a>'.format(reverse('macsnvdb:csnps', kwargs={'gid':drug.orthology.gene.ensembl}), snp_count))
			rows.append(row)

		return JsonResponse({
			'draw': request.POST.get('draw'),
			'recordsTotal': total_count,
			'recordsFiltered': filter_count,
			'data': rows,
		})

def drug(request, did):
	try:
		drugs = Drug.objects.filter(drug_id=did)
	except ObjectDoesNotExist:
		raise Http404('No genes associated with drug {}'.format(did))

	return render(request, 'macaca/drug.html', {
		'drugs': drugs,
	})

@csrf_exempt
def diseases(request):
	if request.method == 'GET':
		return render(request, 'macaca/diseases.html')

	elif request.method == 'POST':
		order = int(request.POST.get('order[0][column]'))
		order_dir = request.POST.get('order[0][dir]')
		search = request.POST.get('search[value]')
		start = int(request.POST.get('start'))
		length = int(request.POST.get('length'))
		total_count = Disease.objects.count()
		filter_count = total_count
		
		diseases = Disease.objects.all()
		if search:
			diseases = diseases.filter(
				Q(orthology__gene__ensembl__contains=search)
				| Q(orthology__gene__name__contains=search)
				| Q(orthology__gene__description__contains=search)
				| Q(pomim__contains=search)
			)
			filter_count = diseases.count()

		sign = '-' if order_dir == 'desc' else ''
		if order == 0:
			diseases = diseases.order_by('{}orthology__gene__ensembl'.format(sign))
		elif order == 1:
			diseases = diseases.order_by('{}orthology__gene__name'.format(sign))
		elif order == 2:
			diseases = diseases.order_by('{}orthology__gene__description'.format(sign))
		elif order == 3:
			diseases = diseases.order_by('{}pomim'.format(sign))

		diseases = diseases[start:start+length]

		rows = []
		for disease in diseases:
			row = []
			snp_count = Gannot.objects.filter(feature=1, gene__ensembl=disease.orthology.gene.ensembl).count()
			row.append('<a href="{}">{}</a>'.format(reverse('macsnvdb:gene', kwargs={'gid':disease.orthology.gene.ensembl}), disease.orthology.gene.ensembl))
			row.append(disease.orthology.gene.name)
			row.append(disease.orthology.gene.description)
			row.append('<a href="{}">{}</a>'.format(reverse('macsnvdb:disease', kwargs={'did': disease.pomim}), disease.pomim))
			row.append('<a href="{}">{}</a>'.format(reverse('macsnvdb:csnps', kwargs={'gid':disease.orthology.gene.ensembl}), snp_count))
			rows.append(row)

		return JsonResponse({
			'draw': request.POST.get('draw'),
			'recordsTotal': total_count,
			'recordsFiltered': filter_count,
			'data': rows,
		})


def disease(request, did):
	did = int(did)
	try:
		diseases = Disease.objects.filter(pomim=did)
		phenotype = "; ".join(set([d.phenotype for d in diseases]))
	except ObjectDoesNotExist:
		raise Http404('No genes associated with disease {}'.format(did))

	return render(request, 'macaca/disease.html', {
		'diseases': diseases,
		'phenotype': phenotype,
	})	

@csrf_exempt
def cds_snps(request, gid):
	if request.method == 'GET':
		gene = Gene.objects.get(ensembl=gid)
		labels = [s.code for s in Individual.objects.all()]

		return render(request, 'macaca/snpcds.html', {
			'geneid': gid,
			'genepk': gene.id,
			'chromosome': gene.chromosome.pk,
			'labels': labels,
			'mutation': 0
		})

	elif request.method == 'POST':
		paras = json.loads(request.body)
		#gene = Gene.objects.get(id=paras['geneid'])
		#Snps.shard(gene.chromosome.pk)
		#annots = Gannot.objects.filter(feature=1, gene=gene.id)
		#snp_ids = [annot.snp.id for annot in annots]
		#snps = Snps.shard(gene.chromosome.pk).objects.filter(pk__in=snp_ids)
		snps = Snps.shard(paras['chromosome']).objects.filter(gannot__gene=paras['geneid'], gannot__feature=1)

		if paras['mutation']:
			snps = snps.filter(mutation__synonymous=paras['mutation'])

		paginator = Paginator(snps, paras['records'])

		try:
			snps = paginator.page(paras['page'])
		except PageNotAnInteger:
			snps = paginator.page(1)
		except EmptyPage:
			snps = paginator.page(paginator.num_pages)

		paras['total'] = snps.paginator.count
		paras['page'] = snps.number
		paras['pages'] = snps.paginator.num_pages
		paras['prev'] = snps.previous_page_number() if snps.has_previous() else 0
		paras['next'] = snps.next_page_number() if snps.has_next() else 0

		variants = [{'id': snp.pk, 'chr': snp.chromosome.pk, 'pos': snp.position, 'ref': snp.reference, 'alt': snp.alteration} for snp in snps]
		snp_ids = [snp.id for snp in snps]

		genotypes = {}
		vs = Variants.shard(paras['chromosome']).objects.filter(snp__in=snp_ids)
		ns = Nonvariants.shard(paras['chromosome']).objects.filter(snp__in=snp_ids)
		for v in vs:
			genotypes[(v.snp.id, v.individual.id)] = v.genotype

		for n in ns:
			genotypes[(n.snp.id, n.individual.id)] = 3

		matrix = []
		for i in range(20):
			matrix.append([])
			for j, sid in enumerate(snp_ids):
				g = genotypes.get((sid, i+1), 0)
				matrix[i].append({'x': j, 'y': i, 'g': g})

		species = [s.code for s in Individual.objects.all()]

		return JsonResponse({'variants': variants, 'matrix': matrix, 'species': species, 'paras': paras})

def pileup(request, sid):
	snp = Snp.objects.get(id=sid)
	variants = Variant.objects.filter(snp__id=sid)
	header = ["#CHROM","POS","ID","REF","ALT","QUAL","FILTER","INFO","FORMAT"]
	line = [snp.chromosome.name, str(snp.position), str(snp.id), snp.reference, snp.alteration, '.', 'PASS', '.', 'GT']
	genotypes = ['0/0', '1/1', '0/1']
	for var in variants:
		header.append(var.individual.code)
		line.append(genotypes[var.genotype])

	#header = "\t".join(header)
	line = "\t".join(line)

	vcf = "{1}".format(header, line)

	return render(request, 'macaca/pileup.html', {
		'vcf': vcf,
		'chromosome': snp.chromosome.name,
		'position': snp.position,
	})

def statistics(request):
	paras = dict(
		feature = int(request.GET.get('feature', 0)),
		genotype = int(request.GET.get('genotype', 0)),
		mutation = int(request.GET.get('mutation', 0))
	)

	stat = Statistics.objects.filter(
		feature = paras['feature'],
		genotype = paras['genotype'],
		mutation = paras['mutation']
	).order_by('individual', 'chromosome')

	rows = []
	row = []
	indiv = 1
	for s in stat:
		if s.individual.id != indiv:
			rows.append(row)
			row = []
			indiv = s.individual.id

		if not row:
			row.append(s.individual.code)
		
		row.append(s.counts)

	rows.append(row)

	return render(request, 'macaca/statistics.html', {
		'paras': paras,
		'rows': rows,
	})

def help(request, page):
	return render(request, 'macaca/%s.html' % page)
	