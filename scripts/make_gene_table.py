#!/usr/bin/env python
import os
import sys

input_dir = sys.argv[1]

gene_out = open(os.path.join(input_dir, 'table/gene.table'), 'w')
tran_out = open(os.path.join(input_dir, 'table/transcript.table'), 'w')

descripts = {}
with open(os.path.join(input_dir, 'data/macaca_genes.txt')) as fh:
	fh.readline()
	for line in fh:
		cols = line.strip('\n').split('\t')

		if cols[1]:
			descripts[cols[0]] = cols[1].split('[')[0].strip()
		else:
			descripts[cols[0]] = cols[1]

gene_mapping = {}
biotypes = dict(
	miRNA = 5,
	misc_RNA = 6,
	protein_coding= 1,
	pseudogene = 2,
	rRNA = 4,
	snoRNA = 7,
	snRNA = 3
)
with open(os.path.join(input_dir, 'data/gene_info.txt')) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		
		gene_mapping[cols[1]] = len(gene_mapping) + 1
		if cols[2] == 'N/A':
			cols[2] = ''
		row = (gene_mapping[cols[1]], cols[1], cols[2], descripts[cols[1]], biotypes[cols[3]], cols[4], cols[5], cols[6])

		gene_out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % row)


protein_mapping = {}
with open(os.path.join(input_dir, 'data/trasncript_to_protein.txt')) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		protein_mapping[cols[0]] = cols[1]

count = 0
with open(os.path.join(input_dir, 'data/transcript_info.txt')) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		count += 1
		row = (count, cols[1], protein_mapping[cols[1]], cols[3], cols[4], cols[5], gene_mapping[cols[2]])

		tran_out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % row)

