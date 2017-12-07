#!/usr/bin/env python

proteins = {}
with open('trasncript_to_protein.txt') as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		proteins[cols[0]] = cols[1]

with open('transcript_info.txt') as fh:
	for line in fh:
		cols = line.strip().split('\t')

		cols.append(proteins[cols[1]])

		print "\t".join(cols)

