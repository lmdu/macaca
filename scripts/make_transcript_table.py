#!/usr/bin/env python
import os
import sys

data_dir = sys.argv[1]

proteins = {}
with open(os.path.join(data_dir, 'trasncript_to_protein.txt')) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		proteins[cols[0]] = cols[1]

with open(os.path.join(data_dir, 'transcript_info.txt')) as fh:
	for line in fh:
		cols = line.strip().split('\t')

		cols.append(proteins[cols[1]])

		print "\t".join(cols)

