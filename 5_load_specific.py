#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

data_dir = sys.argv[1]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macaca.settings")
import django
if django.VERSION >= (1, 7):
	django.setup()

#load specific snps
from django.db import connection, transaction
from snpdb.models import Snp, Group, Species, GroupSpecific, SpeciesSpecific
print("loading specific snps")
specific_file = os.path.join(data_dir, 'specific_table.txt')

group_map = {g.name: g.id for g in Group.objects.all()}
species_map = {s.taxonomy: s.id for s in Species.objects.all()}
snp_map = {("chr%s" % v.chromosome_id, v.position): v.id  for v in Snp.objects.all()}

group_spec = []
species_spec = []

with open(specific_file) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		snp = snp_map[(cols[1], int(cols[2]))]

		if cols[0] == 'group':
			group_spec.append((snp, group_map[cols[3]]))
		else:
			species_spec.append((snp, species_map[int(cols[3])]))

with transaction.atomic():
	with connection.cursor() as c:
		c.executemany("INSERT INTO snpdb_groupspecific (snp_id, group_id) VALUES (?,?)", group_spec)
		c.executemany("INSERT INTO snpdb_speciesspecific (snp_id, species_id) VALUES (?,?)", species_spec)
