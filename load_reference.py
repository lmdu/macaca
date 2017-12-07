#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macaca.settings")
import django
if django.VERSION >= (1, 7):
	django.setup()

data_dir = sys.argv[1]

#load reference genome chromosome information
print "load reference chromosome information"
from snpdb.models import Chromosome
chromos = []
chromo_file = os.path.join(data_dir, 'chromosome_table.txt')
with open(chromo_file) as fh:
	for line in fh:
		cols = line.strip().split()
		chromo = Chromosome(name="chr%s" % cols[0], size=int(cols[1]))
		chromos.append(chromo)
Chromosome.objects.bulk_create(chromos)

#load species information
print "load species information"
from snpdb.models import Species
species = []
species_file = os.path.join(data_dir, 'species_table.txt')
with open(species_file) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		s = Species(
			taxonomy = int(cols[0]),
			scientific_name = cols[2],
			common_name = cols[3],
			group = cols[1],
			code = cols[5],
			sample = cols[6],
			location = cols[4],
			non_variant = int(cols[7].replace(',','')),
			heterozygous = int(cols[8].replace(',','')),
			homozygous = int(cols[9].replace(',','')),
			total_variant = int(cols[10].replace(',','')),
			total_useable = int(cols[11].replace(',','')),
			heterozygosity = float(cols[12]),
			snv_rate = float(cols[13]),
			pcr_duplicates = float(cols[14]),
			mean_coverage = float(cols[15])
		)
		species.append(s)
Species.objects.bulk_create(species)

#load gene information
print "load reference gene information"
from snpdb.models import Gene
biotypes = dict(
	miRNA = 5,
	misc_RNA = 6,
	protein_coding= 1,
	pseudogene = 2,
	rRNA = 4,
	snoRNA = 7,
	snRNA = 3
)

genes = []
gene_file = os.path.join(data_dir, 'gene_table.txt')
with open(gene_file) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		gene = Gene(
			ensembl_id = cols[1],
			name = cols[2],
			description = cols[-1],
			biotype = biotypes[cols[3]],
			start = int(cols[4]),
			end = int(cols[5]),
			strand = cols[6]
		)
		genes.append(gene)
Gene.objects.bulk_create(genes)

#load transcript information
print "load reference transcript information"
gene_mapping = {g.ensembl_id: g for g in Gene.objects.all()}

from snpdb.models import Transcript
transcripts = []
transcript_file = os.path.join(data_dir, 'transcript_table.txt')
with open(transcript_file) as  fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		transcript = Transcript(
			ensembl_id = cols[1],
			protein = cols[6],
			start = int(cols[3]),
			end = int(cols[4]),
			strand = cols[5],
			parent = gene_mapping[cols[2]]
		)
		transcripts.append(transcript)
Transcript.objects.bulk_create(transcripts)
