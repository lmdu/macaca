import sys
import gzip

class Data(dict):
	def __getattr__(self, name):
		return self.get(name, 'N/A')

	def __setattr__(self, name, val):
		self[name] = val

def gtf_parser(annot_file):
	"""
	parse GFF, GTF, comparessed gz annotation file
	"""
	with gzip.open(annot_file, 'rt') as fh:
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

	chroms = {str(i) for i in range(1,21)}

	parser =  gtf_parser('/home/ming/macaca/snvs/ref/Macaca_mulatta.Mmul_8.0.1.97.gtf.gz')

	if operator == 'gene':
		for row in parser:
			if row.feature == 'gene' and row.seqid in chroms:
				print("\t".join((row.seqid, row.attrs.gene_id, row.attrs.gene_name, row.attrs.gene_biotype, row.start, row.end, row.strand)))

	elif operator == 'transcript':
		for row in parser:
			if row.feature == 'transcript' and row.seqid in chroms:
				print("\t".join((row.seqid, row.attrs.transcript_id, row.attrs.gene_id, row.start, row.end, row.strand)))
