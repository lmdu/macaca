#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macaca.settings")
import django
if django.VERSION >= (1, 7):
	django.setup()

data_dir = sys.argv[1]

#load reference genome chromosome information
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
from snpdb.models import Gene
genes = []
gene_file = os.path.join(data_dir, 'gene_table.txt')
with open(gene_file) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		gene = Gene(
			ensembl_id = cols[1],
			name = cols[2],
			description = cols[-1],
			start = int(cols[3]),
			end = int(cols[4]),
			strand = int(cols[5])
		)
		genes.append(gene)
Gene.objects.bulk_create(genes)

#load transcript information
from snpdb.models import Transcript




def main():
	from blog.models import Blog
	f = open('oldblog.txt')
	BlogList = []
	for line in f:
		title,content = line.split('****')
		blog = Blog(title=title,content=content)
		BlogList.append(blog)
	f.close()

	Blog.objects.bulk_create(BlogList)

if __name__ == '__main__':
	main() 