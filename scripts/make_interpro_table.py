# coding: utf-8
import os
import sys

data_dir = sys.argv[1]

entries = {}
entry_file = os.path.join(data_dir, 'interpro_entry.list')
with open(entry_file) as fh:
	fh.readline()
	for line in fh:
		cols = line.strip('\n').split('\t')
		entries[cols[0]] = cols[1]

inter_file = os.path.join(data_dir, 'interpro_info.txt')
with open(inter_file) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		if cols[1]:
			cols.append(entries.get(cols[1], ''))
			print("\t".join(cols))
