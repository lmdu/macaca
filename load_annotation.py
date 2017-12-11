#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macaca.settings")
import django
if django.VERSION >= (1, 7):
	django.setup()

data_dir = sys.argv[1]

#load annotation information
print("load annotation information")
from django.db import connection, transaction
from snpdb.models import Chromosome
from snpdb.models import Gene
from snpdb.models import Transcript
annot_file = os.path.join(data_dir, 'annotation_table.txt')

chromos = {c.name:c.id for c in Chromosome.objects.all()}
genes = {g.ensembl_id:g.id for g in Gene.objects.all()}
transcripts = {t.ensembl_id:t.id for t in Transcript.objects.all()}

with connection.cursor() as c:
	snps = {(row[2], row[1]): row[0] for row in c.execute("SELECT id, position, chrom_id FROM snpdb_snp")}

gannots = []
tannots = []

with transaction.atomic():
	with connection.cursor() as c:
		with open(annot_file) as fh:
			for line in fh:
				cols = line.strip().split('\t')
				snp = snps[(chromos[cols[0]], int(cols[1]))]
				if len(cols) > 5:
					tannots.append((None, int(cols[3]), cols[4], int(cols[5]), cols[6], int(cols[7]), transcripts[cols[2]], snp))
				else:
					gannots.append((None, int(cols[3]), int(cols[4]), genes[cols[2]], snp))

		c.executemany("INSERT INTO snpdb_geneannot VALUES (?,?,?,?,?)", gannots)
		c.executemany("INSERT INTO snpdb_transannot VALUES (?,?,?,?,?,?,?,?)", tannots)
