#!/usr/bin/env python

descripts = {}
with open('macaca_genes.txt') as fh:
	fh.readline()
	for line in fh:
		cols = line.strip('\n').split('\t')

		if cols[1]:
			descripts[cols[0]] = cols[1].split('[')[0].strip()
		else:
			descripts[cols[0]] = cols[1]

with open('gene_info.txt') as fh:
	for line in fh:
		cols = line.strip().split('\t')
		cols.append(descripts[cols[1]])

		print "\t".join(cols)
