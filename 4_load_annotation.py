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
					tannots.append((None, int(cols[3]), cols[4], int(cols[5]), cols[6], cols[7], cols[8], int(cols[9]), int(cols[10]), snp, transcripts[cols[2]]))
				else:
					gannots.append((None, int(cols[3]), int(cols[4]), genes[cols[2]], snp))

		c.executemany("INSERT INTO snpdb_geneannot VALUES (?,?,?,?,?)", gannots)
		c.executemany("INSERT INTO snpdb_transannot VALUES (?,?,?,?,?,?,?,?,?,?,?)", tannots)

#load genes
from snpdb.models import Gene
gene_mapping = {g.ensembl_id: g for g in Gene.objects.all()}

print("load go term information")
go_file = os.path.join(data_dir, 'goterm_table.txt')
from snpdb.models import Function
GOS = {}
with open(go_file) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		if not cols[1]:
			continue

		if cols[1] not in GOS:
			go = Function(
				source = 1,
				accession = cols[1],
				descript = cols[2],
				supplement = cols[3]
			)
			GOS[cols[1]] = go
Function.objects.bulk_create(GOS.values())

GOS = {go.accession: go for go in Function.objects.filter(source=1)}

from snpdb.models import Funcannot
annots = []
with open(go_file) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		if not cols[1]:
			continue

		if cols[0] not in gene_mapping:
			continue

		a = Funcannot(
			gene = gene_mapping[cols[0]],
			function = GOS[cols[1]]
		)
		annots.append(a)
Funcannot.objects.bulk_create(annots)
del GOS

print("load kegg pathway information")
kegg_file = os.path.join(data_dir, 'kegg_table.txt')
KEGGS = {}
with open(kegg_file) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		if cols[1] not in KEGGS:
			kegg = Function(
				source = 2,
				accession = cols[1],
				descript = cols[2],
				supplement = cols[3]
			)
			KEGGS[cols[1]] = kegg
Function.objects.bulk_create(KEGGS.values())

KEGGS = {kegg.accession: kegg for kegg in Function.objects.filter(source=2)}

annots = []
with open(kegg_file) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')

		if cols[0] not in gene_mapping:
			continue

		a = Funcannot(
			gene = gene_mapping[cols[0]],
			function = KEGGS[cols[1]]
		)
		annots.append(a)
Funcannot.objects.bulk_create(annots)
del KEGGS

print("load interpro information")
ipro_file = os.path.join(data_dir, 'interpro_table.txt')
IPROS = {}
with open(ipro_file) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		if not cols[1]:
			continue

		if cols[1] not in IPROS:
			ipro = Function(
				source = 3,
				accession = cols[1],
				descript = cols[2],
				supplement = ''
			)
			IPROS[cols[1]] = ipro
Function.objects.bulk_create(IPROS.values())

IPROS = {ipro.accession: ipro for ipro in Function.objects.filter(source=3)}

annots = []
with open(ipro_file) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		if not cols[1]:
			continue

		if cols[0] not in gene_mapping:
			continue

		a = Funcannot(
			gene = gene_mapping[cols[0]],
			function = IPROS[cols[1]]
		)
		annots.append(a)
Funcannot.objects.bulk_create(annots)
del IPROS

print("load pfam information")
pfam_file = os.path.join(data_dir, 'pfam_table.txt')
PFAMS = {}
with open(pfam_file) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		if not cols[1]:
			continue

		if cols[1] not in PFAMS:
			pfam = Function(
				source = 4,
				accession = cols[1],
				descript = cols[2],
				supplement = ''
			)
			PFAMS[cols[1]] = pfam
Function.objects.bulk_create(PFAMS.values())

PFAMS = {pfam.accession: pfam for pfam in Function.objects.filter(source=4)}

annots = []
with open(pfam_file) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		if not cols[1]:
			continue
		
		if cols[0] not in gene_mapping:
			continue

		a = Funcannot(
			gene = gene_mapping[cols[0]],
			function = PFAMS[cols[1]]
		)
		annots.append(a)
Funcannot.objects.bulk_create(annots)
del PFAMS


