#!/usr/bin/env python
import os
import sys

work_dir = '/home/ming/macaca/snvs'
data_dir = os.path.join(work_dir, 'data')
table_dir = os.path.join(work_dir, 'tables')

gene_out = open(os.path.join(table_dir, 'gene.table'), 'w')
tran_out = open(os.path.join(table_dir, 'transcript.table'), 'w')

descripts = {}
with open(os.path.join(data_dir, 'gene_description.tsv')) as fh:
	fh.readline()
	for line in fh:
		cols = line.strip('\n').split('\t')

		if cols[1]:
			descripts[cols[0]] = cols[1].split('[')[0].strip()
		else:
			descripts[cols[0]] = cols[1]

gene_mapping = {}
with open(os.path.join(data_dir, 'gene_info.tsv')) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		
		gene_mapping[cols[1]] = len(gene_mapping) + 1
		if cols[2] == 'N/A':
			cols[2] = ''
		row = (gene_mapping[cols[1]], cols[1], cols[2], descripts[cols[1]], cols[3], cols[4], cols[5], cols[6], cols[0])

		gene_out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % row)


protein_mapping = {}
with open(os.path.join(data_dir, 'transcript_to_protein.tsv')) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		protein_mapping[cols[0]] = cols[1]

count = 0
with open(os.path.join(data_dir, 'transcript_info.tsv')) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		count += 1
		row = (count, cols[1], protein_mapping[cols[1]], cols[3], cols[4], cols[5], gene_mapping[cols[2]])

		tran_out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % row)
