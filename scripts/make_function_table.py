#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

join = os.path.join

input_dir = sys.argv[1]

func_out = open(join(input_dir, 'table/function.table'), 'w')
annot_out = open(join(input_dir, 'table/funcannot.table'), 'w')

annot_count = 0
func_count = 0

gene_mapping = {}
with open(join(input_dir, 'table/gene.table')) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		gene_mapping[cols[1]] = cols[0]

#Gene ontology information
goterm_mapping = {}
with open(join(input_dir, 'data/goterm_info.txt')) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')

		if not cols[1]:
			continue

		if cols[0] not in gene_mapping:
			continue

		if cols[1] not in goterm_mapping:
			func_count += 1
			func_out.write("%s\t%s\t%s\t%s\t%s\n" % (func_count, 1, cols[1], cols[2], cols[3]))
			goterm_mapping[cols[1]] = func_count

		annot_count += 1
		annot_out.write("%s\t%s\t%s\n" % (annot_count, gene_mapping[cols[0]], goterm_mapping[cols[1]]))

#KEGG pathways
pathway_info = {}
with open(join(input_dir, 'data/kegg_class.txt')) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		pathway_info[cols[0]] = cols[1:]

relations = {}
with open(join(input_dir, 'data/pathway_mapping.txt')) as fh:
	for line in fh:
		cols = line.strip().split()
		if cols[0] not in relations:
			relations[cols[0]] = set()
		relations[cols[0]].add(cols[1])

genes = {}
with open(join(input_dir, 'data/kegg_ensembl_mapping.txt')) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		
		if cols[1] not in gene_mapping:
			continue

		for e in cols[1].split():
			if e not in genes:
				genes[e] = set()
			genes[e].add(cols[0])

pathway_mapping = {}
for g in genes:
	for ko in genes[g]:
		pathes = set()

		if ko not in relations:
			continue

		for path in relations[ko]:
			pathes.add(path)

	for p in pathes:
		if p not in pathway_mapping:
			func_count += 1
			pathway_mapping[p] = func_count
			func_out.write("%s\t%s\t%s\t%s\n" % (pathway_mapping[p], 2, pathway_info[p][0], pathway_info[p][1]))

		annot_count += 1
		annot_out.write("%s\t%s\t%s\n" % (annot_count, gene_mapping[g], pathway_mapping[p]))

#pfam table
pfam_class = {}
pfam_mapping = {}
with open(join(input_dir, 'data/Pfam-A.clans.tsv')) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		pfam_class[cols[0]] = (cols[-1].strip(), cols[1])

with open(join(input_dir, 'data/pfam_info.txt')) as fh:
	fh.readline()
	for line in fh:
		cols = line.strip('\n').split('\t')
		if not cols[1]:
			continue

		if cols[0] not in gene_mapping:
			continue

		if cols[1] not in pfam_mapping:
			func_count += 1
			pfam_mapping[cols[1]] = func_count

			if cols[1] in pfam_class:
				func_out.write("%s\t%s\t%s\t%s\n" % (pfam_mapping[cols[1]], 3, pfam_class[cols[1]][0], pfam_class[cols[1]][1]))
			else:
				func_out.write("%s\t%s\t%s\t%s\n" % (pfam_mapping[cols[1]], 3, '', ''))

		annot_count += 1
		annot_out.write("%s\t%s\t%s\n" % (annot_count, gene_mapping[cols[0]], pfam_mapping[cols[1]]))

#interpro table
interpro_entry = {}
interpro_mapping = {}
with open(join(input_dir, 'data/interpro_entry.list')) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		interpro_entry[cols[0]] = cols[1]

with open(join(input_dir, 'data/interpro_info.txt')) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')

		if not cols[1]:
			continue

		if cols[0] not in gene_mapping:
			continue

		if cols[1] not in interpro_mapping:
			func_count += 1
			interpro_mapping[cols[1]] = func_count

			if cols[1] in interpro_entry:
				func_out.write("%s\t%s\t%s\t%s\n" % (interpro_mapping[cols[1]], 4, cols[1], interpro_entry[cols[1]]))
			else:
				func_out.write("%s\t%s\t%s\t%s\n" % (interpro_mapping[cols[1]], 4, cols[1], ''))

		annot_count += 1
		annot_out.write("%s\t%s\t%s\n" % (annot_count, gene_mapping[cols[0]], interpro_mapping[cols[1]]))

