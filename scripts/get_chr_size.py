#!/usr/bin/env python
import pyfaidx

genome = pyfaidx.Fasta('Macaca_mulatta.MMUL_1.85.dna.fa')

for seq in genome:
	print "%s\t%s" % (seq.name, len(seq))