#!/usr/bin/env python
import sys

snp_file = sys.argv[1]
genotypes={0:'0/0', 1: '1/1', 2:'0/1'}

with open(snp_file) as fh:
	species = fh.readline().strip().split('\t')[4:]

	for line in fh:
		cols = line.strip().split('\t')[4:]

		 for idx, typ in enumerate(cols):
			print ()
