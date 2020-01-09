#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

data_dir = '/home/ming/macaca/snvs/tables'

snp_file = os.path.join(data_dir, 'snp.table')
var_file = os.path.join(data_dir, 'variant.table')
non_file = os.path.join(data_dir, 'non_variant.table')

print('split snp table')
outs = [None]
#nums = [None]
for i in range(1,21):
	op = open("%s.%s" % (snp_file, i), 'w')
	outs.append(op)
	#nums.append(0)

with open(snp_file) as fh:
	for line in fh:
		cols = line.strip().split()
		idx = int(cols[-1])
		#nums[idx] += 1
		outs[idx].write(line)

for op in outs[1:]:
	op.close()

print('split variant table')
outs = [None]
for i in range(1,21):
	op = open("%s.%s" % (var_file, i), 'w')
	outs.append(op)

with open(var_file) as fh:
	for line in fh:
		cols = line.strip().split()
		idx = int(cols[2])

		outs[idx].write(line)

for op in outs[1:]:
	op.close()

print('split non_variant table')
outs = [None]
for i in range(1,21):
	op = open("%s.%s" % (non_file, i), 'w')
	outs.append(op)

with open(non_file) as fh:
	for line in fh:
		cols = line.strip().split()
		idx = int(cols[1])

		outs[idx].write("%s\t%s\t%s\n" % (cols[0], cols[2], cols[3]))

for op in outs[1:]:
	op.close()
