#!/usr/bin/env python
import sys
import pyfaidx

fasta_file, snp_file, chrom = sys.argv[1:]

genome = pyfaidx.Fasta(fasta_file)
seq = str(genome[chrom])

with open(snp_file) as fh:
	fh.readline()
	for line in fh:
		cols = line.strip().split('\t')
		pos = int(cols[1])
		start = pos - 51
		if start<0:
			start = 0
		end = pos + 50

		left = seq[start:pos-1]
		right = seq[pos:end]

		print "\t".join((cols[0], cols[1], cols[2], cols[3], left, right))
