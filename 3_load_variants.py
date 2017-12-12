#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macaca.settings")
import django
if django.VERSION >= (1, 7):
	django.setup()

data_dir = sys.argv[1]

#load snp genotype information
print("load snp genotype information")
from django.db import connection, transaction
from snpdb.models import Chromosome
from snpdb.models import Snp
from snpdb.models import Variant
from snpdb.models import Species
genotype_file = os.path.join(data_dir, 'genotype_table.txt')

chromos = {c.name:c.id for c in Chromosome.objects.all()}
genotypes = {'1/1': 1, '0/1': 2}
species = {s.code: s.id for s in Species.objects.all()}

with connection.cursor() as c:
	snps = {(row[2], row[1]): row[0] for row in c.execute("SELECT id, position, chrom_id FROM snpdb_snp")}

variants = []
progress = 0
with transaction.atomic():
	with connection.cursor() as c:
		with open(genotype_file) as fh:
			codes = fh.readline().strip().split('\t')[4:-1]
			cc = len(codes)
			for line in fh:
				cols = line.strip().split()
				snp = snps[(chromos[cols[0]], int(cols[1]))]
				types = cols[4:-1]
				for i in range(cc):
					if types[i] == '.' or types[i] == '0/0':
						continue
					variants.append((genotypes[types[i]], snp, species[codes[i]]))

				progress += 1
				if progress % 10000 == 0:
					c.executemany("INSERT INTO snpdb_variant (genotype, snp_id, species_id) VALUES (?,?,?)", variants)
					variants = []
					print("Variants: %s" % progress)

		if variants:
			c.executemany("INSERT INTO snpdb_variant (genotype, snp_id, species_id) VALUES (?,?,?)", variants)
		print("Variants: %s" % progress)
