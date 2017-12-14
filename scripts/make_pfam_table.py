#!/usr/bin/env python
import os
import sys

data_dir = sys.argv[1]

descs = {}

pfam_clan = os.path.join(data_dir, 'Pfam-A.clans.tsv')
with open(pfam_clan) as fh:
	for line in fh:
		cols = line.split('\t')
		descs[cols[0]] = cols[-1].strip()

pfam_info = os.path.join(data_dir, 'pfam_info.txt')
with open(pfam_info) as fh:
	fh.readline()
	for line in fh:
		cols = line.strip('\n').split('\t')
		cols.append(descs.get(cols[1], ''))
		print("\t".join(cols))

