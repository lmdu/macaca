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
				start = cols[3],
				end = cols[4],
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
	operator = sys.argv[1]

	parser =  gtf_parser('Macaca_mulatta.MMUL_1.85.gtf')

	if operator == 'gene':
		for row in parser:
			if row.feature == 'gene':
				print "\t".join((row.seqid, row.attrs.gene_id, row.attrs.gene_name, row.start, row.end, row.strand))

	elif operator == 'transcript':
		for row in parser:
			if row.feature == 'transcript':
				print "\t".join((row.seqid, row.attrs.transcript_id, row.attrs.gene_id, row.start, row.end, row.strand))
