#!/usr/bin/env python
import os
import sys

data_dir = sys.argv[1]

samples = {}
groups = set()
species = set()

species_file = os.path.join(data_dir, 'species_table.txt')
with open(species_file) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		samples[cols[5]] = (cols[0], cols[1])
		groups.add(cols[1])
		species.add(cols[0])

snp_file = os.path.join(data_dir, 'genotype_table.txt')


with open(snp_file) as fh:
	codes = fh.readline().strip().split()[4:-1]
	for line in fh:
		if '.' in line:
			continue
		if '0/1' in line:
			continue
		
		cols = line.strip().split()
		gmat = {g:[] for g in groups}
		smat = {s:[] for s in species}
		for idx, genotype in enumerate(cols[4:-1]):
			taxonomy, group = samples[codes[idx]]
			n = 1 if genotype == '1/1' else 0

			gmat[group].append(n)
			smat[taxonomy].append(n)

		#process group specific snps
		r = [sum(gmat[g]) for g in gmat]

		if r.count(0) == len(r)-1:
			for g in gmat:
				if sum(gmat[g]) > 0:
					if all(gmat[g]):
						print("group\t%s\t%s\t%s" % (cols[0], cols[1], g))
					break

		#process species specific snps
		r = [sum(smat[s]) for s in smat]

		if r.count(0) == len(r)-1:
			for s in smat:
				if sum(smat[s]) > 0:
					if all(smat[s]):
						print("species\t%s\t%s\t%s" % (cols[0], cols[1], s))
					break

