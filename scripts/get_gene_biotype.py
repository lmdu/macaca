#!/usr/bin/env python
import sys
class Data(dict):
	def __getattr__(self, name):
		return self.get(name, 'N/A')

	def __setattr__(self, name, val):
		self[name] = val

def gtf_parser(annot_file):
	"""
	parse GFF, GTF, comparessed gz annotation file
	"""
	with open(annot_file) as fh:
		for line in fh:
			if line[0] == '#':
				continue
			cols = line.strip().split('\t')
			record = Data(
				seqid = cols[0],
				feature = cols[2],
				start = int(cols[3]),
				end = int(cols[4]),
				strand = cols[6],
				attrs = Data()
			)
			
			for item in cols[-1].split(';'):
				if not item:
					continue
				name, value = item.strip().strip('"').split('"')
				record.attrs[name.strip()] = value
			
			yield record

if __name__ == '__main__':
	infile = sys.argv[1]
	biotypes = set()
	for row in gtf_parser(infile):
		if row.feature == 'gene':
			biotypes.add(row.attrs.gene_biotype)

	for b in biotypes:
		print b
