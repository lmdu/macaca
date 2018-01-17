#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

input_dir = sys.argv[1]

species_out = open(os.path.join(input_dir, 'table/species.table'), 'w')
indivi_out = open(os.path.join(input_dir, 'table/individual.table'), 'w')

group_mapping = {}
with open(os.path.join(input_dir, 'table/group.table')) as fp:
	for line in fp:
		cols = line.strip().split()
		group_mapping[cols[1]] = cols[0]

count = 0
species_mapping = {}

with open(os.path.join(input_dir, 'data/species_info.txt')) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		if cols[0] not in species_mapping:
			species_mapping[cols[0]] = len(species_mapping) + 1
			species_out.write("%s\t%s\t%s\t%s\t%s\n" % (species_mapping[cols[0]], cols[0], cols[2], cols[3], group_mapping[cols[1]]))

		count += 1

		res = (count, cols[5], cols[6], cols[4], cols[7].replace(',',''), cols[8].replace(',',''), cols[9].replace(',',''), cols[10].replace(',',''), cols[11].replace(',',''), cols[12], cols[13], cols[14], cols[15], species_mapping[cols[0]])

		indivi_out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % res)

species_out.close()
indivi_out.close()

