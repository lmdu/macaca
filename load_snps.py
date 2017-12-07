#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macaca.settings")
import django
if django.VERSION >= (1, 7):
	django.setup()

data_dir = sys.argv[1]

#load snp site information
print "load snp site information"
from django.db import connection, transaction
from snpdb.models import Chromosome
from snpdb.models import Snp
snp_file = os.path.join(data_dir, 'snp_sites.txt')

chromos = {c.name: c.id for c in Chromosome.objects.all()}
snps = []
progress = 0

with transaction.atomic():
	with connection.cursor() as c:
		with open(snp_file) as fh:
			for line in fh:
				cols = line.strip().split('\t')
				snps.append((None, int(cols[1]), cols[2], cols[3], cols[4], cols[5], chromos[cols[0]]))
				progress += 1
				if progress % 100000 == 0:
					c.executemany("INSERT INTO snpdb_snp VALUES (?,?,?,?,?,?,?)", snps)
					snps = []
					print "SNPs: %s" % progress
		if snps:
			c.executemany("INSERT INTO snpdb_snp VALUES (?,?,?,?,?,?,?)", snps)

print "SNPs: %s" % progress


'''
#load snp genotype information
print "load snp genotype information"
from snpdb.models import Variant
from snpdb.models import Species
genotype_file = os.path.join(data_dir, 'genotype_table.txt')

genotypes = {'0/0': 0, '1/1': 1, '0/1': 2}
species = {s.code: s for s in Species.objects.all()}
variants = []
progress = 0
with open(genotype_file) as fh:
	codes = fh.readline().strip().split('\t')[4:-1]
	cc = len(codes)
	for line in fh:
		cols = line.strip().split()
		snp = Snp.objects.get(chromosome=chromos[cols[0]], position=int(cols[1]))
		types = cols[4:-1]
		for i in range(cc):
			if types[i] == '.':
				continue
			variant = Variant(
				snp = snp,
				species = species[codes[i]],
				genotype = genotypes[types[i]]
			)
			variants.append(variant)

		progress += 1

		if progress % 100000 == 0:
			Variant.objects.bulk_create(variants)
			variants = []
			print "Variants: %s" % progress

if variants:
	Variant.objects.bulk_create(variants)

print "Variants: %s" % progress
'''