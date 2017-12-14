#!/usr/bin/env python
import os
import sys

data_dir = sys.argv[1]

class_file = os.path.join(data_dir, 'kegg_class.txt')

pathways = {}
with open(class_file) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		pathways[cols[0]] = cols[1:]

relations = {}
relation_file = os.path.join(data_dir, 'pathway_mapping.txt')
with open(relation_file) as fh:
	for line in fh:
		cols = line.strip().split()

		if cols[0] not in relations:
			relations[cols[0]] = set()
		relations[cols[0]].add(cols[1])

genes = {}
mapping_file = os.path.join(data_dir, 'kegg_ensembl_mapping.txt')
with open(mapping_file) as fh:
	for line in fh:
		cols = line.strip().split('\t')

		for e in cols[1].split():
			if e not in genes:
				genes[e] = set()
			genes[e].add(cols[0])

for gene in genes:
	for ko in genes[gene]:
		pathes = set()

		if ko not in relations:
			continue

		for path in relations[ko]:
			pathes.add(path)

	for path in pathes:
		print("%s\t%s\t%s\t%s" % (gene, path, pathways[path][0], pathways[path][1]))

