#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

data_dir = sys.argv[1]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macaca.settings")
import django
if django.VERSION >= (1, 7):
	django.setup()

#load snp site information
print("load snp site information")
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
					print("SNPs: %s" % progress)
		if snps:
			c.executemany("INSERT INTO snpdb_snp VALUES (?,?,?,?,?,?,?)", snps)

print("SNPs: %s" % progress)

