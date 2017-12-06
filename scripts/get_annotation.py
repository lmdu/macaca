#!/usr/bin/env python
import sys
import math
import pyfaidx
import intersection

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

gtf_file, snp_file, genome_file = sys.argv[1:]

genome = pyfaidx.Fasta(genome_file)

gene_tree = {}
feat_tree = {}
transcripts = {}
exons = {}
cds = {}

for row in gtf_parser(gtf_file):
	if row.feature == 'gene':
		if row.seqid not in gene_tree:
			gene_tree[row.seqid] = intersection.IntervalTree()

		gene_tree[row.seqid].insert(row.start, row.end, Data(
			start = row.start,
			end = row.end,
			strand = row.strand,
			geneid = row.attrs.gene_id
		))

	elif row.feature == 'transcript':
		transcripts[row.attrs.transcript_id] = Data(
			chrom = row.seqid,
			strand = row.strand,
			geneid = row.attrs.gene_id
		)

	else:
		if row.feature == 'exon':
			if row.attrs.transcript_id not in exons:
				exons[row.attrs.transcript_id] = []
			exons[row.attrs.transcript_id].append((row.start, row.end))

		elif row.feature == 'CDS':
			if row.attrs.transcript_id not in cds:
				cds[row.attrs.transcript_id] = []
			cds[row.attrs.transcript_id].append((row.start, row.end))


		if row.attrs.gene_id not in feat_tree:
			feat_tree[row.attrs.gene_id] = intersection.IntervalTree()

		feat_tree[row.attrs.gene_id].insert(row.start, row.end, Data(
			start = row.start,
			end = row.end,
			feature = row.feature,
			transcript = row.attrs.transcript_id
		))

#get introns
for tid in exons:
	es = sorted(exons[tid], key=lambda x: x[0])
	for i in range(len(es)-1):
		start, end = (es[i][1]+1, es[i+1][0]-1)
		gene_id = transcripts[tid].geneid

		feat_tree[gene_id].insert(start, end, Data(
			feature = 'intron',
			transcript = tid
		))

def calc_gene_relative_position(gene, position):
	if gene.strand == '+':
		return position - gene.start + 1

	else:
		return gene.end - position + 1

def calc_trasncript_relative_position(transcript, position):
	strand = transcripts[transcript].strand
	es = exons[transcript]

	for start, end in exons:
		if start <= position <= end:
			break

	if strand == '-':
		es.reverse()

	idx = es.index((start, end))
	rpos = sum([ e[1]-e[0]+1 for i, e in enumerate(es) if i < idx])
	rpos += position - start + 1

	return rpos

def get_codon(transcript, position):
	chrom = transcripts[transcript].chrom
	strand = transcripts[transcript].strand
	cs = cds[transcript]

	for start, end in cs:
		if start <= position <= end:
			break

	if strand == '-':
		cs.reverse()

	idx = cs.index((start, end))

	rpos = sum([ e[1]-e[0]+1 for i, e in enumerate(es) if i < idx])
	rpos += position - start + 1

	codon_pos = rpos % 3
	if codon_pos == 0:
		codon_pos += 3

	if codon_pos == 1:
		codon = genome[chrom][position-1:position+2]
	elif codon_pos == 2:
		codon = genome[chrom][position-2:position+1]
	elif codon_pos == 3:
		codon = genome[chrom][position-3:position]

	protein_pos = int(math.ceil(rpos/3.0))


with open(snp_file) as fh:
	#fh.readline()
	for line in fh:
		cols = line.strip().split('\t')
		chrom = cols[0].strip('chr')
		pos = int(cols[1])
		res = gene_tree[chrom].find(pos, pos)
		for r in res:
			rpos = calc_gene_relative_position(r, pos)

			#print "%s\t%s\t%s\t%s" % (cols[0], cols[1], r.geneid, rpos)

			loci = feat_tree[r.geneid].find(pos, pos)

			locations = []
			in_exon = False
			for locus in loci:
				if locus.feature == 'intron':
					locations.append(locus.feature)
				elif locus.feature == 'five_prime_utr':
					locations.append(locus.feature)
				elif locus.feature == 'three_prime_utr':
					locations.append(locus.feature)
				elif locus.feature == 'CDS':
					locations.append(locus.feature)






				elif locus.feature == 'stop_codon':
					locations.append(locus.feature)
				elif locus.feature == 'exon':
					in_exon = True

			if not locations and in_exon:
				locations = ['exon']

			print "%s\t%s\t%s\t%s\t%s" % (cols[0], cols[1], r.geneid, rpos, ",".join(locations))










