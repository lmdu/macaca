#!/usr/bin/env python
descs = {}
with open('Pfam-A.clans.tsv') as fh:
	for line in fh:
		cols = line.split('\t')
		descs[cols[0]] = cols[-1].strip()

with open('pfam_info.txt') as fh:
	fh.readline()
	for line in fh:
		cols = line.strip('\n').split('\t')
		cols.append(descs.get(cols[1], ''))
		print "\t".join(cols)

