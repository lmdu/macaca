#!/usr/bin/env python

max_name = 0
max_desc = 0
with open('macaca_genes.txt') as fh:
	fh.readline()
	for line in fh:
		cols = line.split('\t')

		if cols[1]:
			l = len(cols[1].split('[')[0].strip())
			if l > max_desc:
				max_desc = l

		if cols[2]:
			l = len(cols[2].strip())
			if l > max_name:
				max_name = l

print max_name, max_desc

