#!/usr/bin/env python
import os
import sys

data_dir = sys.argv[1]

descripts = {}
with open(os.path.join(data_dir, 'macaca_genes.txt')) as fh:
	fh.readline()
	for line in fh:
		cols = line.strip('\n').split('\t')

		if cols[1]:
			descripts[cols[0]] = cols[1].split('[')[0].strip()
		else:
			descripts[cols[0]] = cols[1]

with open(os.path.join(data_dir, 'gene_info.txt')) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		cols.append(descripts[cols[1]])

		print "\t".join(cols)
