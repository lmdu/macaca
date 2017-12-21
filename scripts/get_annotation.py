#!/usr/bin/env python
import os
import sys
import math
import pyfaidx
import intersection

from Bio.Seq import Seq

ref_dir, data_dir = sys.argv[1:]

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

gtf_file = os.path.join(ref_dir, 'Macaca_mulatta.MMUL_1.85.gtf')
cds_file = os.path.join(ref_dir, 'Macaca_mulatta.MMUL_1.85.cds.fa')
protein_file = os.path.join(ref_dir, 'Macaca_mulatta.MMUL_1.85.pep.fa')

snp_file = os.path.join(data_dir, 'snp_sites.txt')
tp_file = os.path.join(data_dir, 'trasncript_to_protein.txt')

transcript_to_protein = {}
with open(tp_file) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')
		transcript_to_protein[cols[0]] = cols[1]

cds_seq = pyfaidx.Fasta(cds_file, key_function=lambda x: x.split('.')[0])
protein_seq = pyfaidx.Fasta(protein_file, key_function=lambda x: x.split('.')[0])

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
			strand = row.strand,
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

	for start, end in es:
		if start <= position <= end:
			break

	#if strand == '-':
	#	es.reverse()

	idx = es.index((start, end))
	rpos = sum([ e[1]-e[0]+1 for i, e in enumerate(es) if i < idx])
	if strand == '+':
		rpos += position - start + 1
	else:
		rpos += end - position + 1

	return rpos

def get_codon_info(transcript, position):
	#chrom = transcripts[transcript].chrom
	strand = transcripts[transcript].strand
	cs = cds[transcript]

	for start, end in cs:
		if start <= position <= end:
			break

	#if strand == '-':
	#	cs.reverse()

	idx = cs.index((start, end))

	rpos = sum([ e[1]-e[0]+1 for i, e in enumerate(cs) if i < idx])

	if strand == '+':
		rpos += position - start + 1
	else:
		rpos += end - position + 1

	codon_pos = rpos % 3
	if codon_pos == 0:
		codon_pos += 3

	if codon_pos == 1:
		codon = str(cds_seq[transcript][rpos-1:rpos+2])
	elif codon_pos == 2:
		codon = str(cds_seq[transcript][rpos-2:rpos+1])
	elif codon_pos == 3:
		codon = str(cds_seq[transcript][rpos-3:rpos])

	protein_pos = int(math.ceil(rpos/3.0))

	aa = str(protein_seq[transcript_to_protein[transcript]][protein_pos-1])

	return (codon, codon_pos, aa, protein_pos)

def reverse_complement(codon):
	bases = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}
	codon_list = list(codon)
	codon_list.reverse()
	return "".join([bases[b] for b in codon_list])

feat_types = dict(
	CDS = 1,
	exon = 2,
	three_prime_utr = 3,
	intron = 4,
	five_prime_utr = 5
)

with open(snp_file) as fh:
	#fh.readline()
	for line in fh:
		cols = line.strip().split('\t')
		pos = int(cols[1])
		res = gene_tree[cols[0].strip('chr')].find(pos, pos)
		for r in res:
			gene_pos = calc_gene_relative_position(r, pos)

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

					tpos = calc_trasncript_relative_position(locus.transcript, pos)
					strand = transcripts[locus.transcript].strand
					ref_codon, codon_pos, ref_aa, protein_pos = get_codon_info(locus.transcript, pos)

					alt_codon = list(ref_codon)
					if strand == '-':
						alt_codon[codon_pos-1] = reverse_complement(cols[3])
					else:
						alt_codon[codon_pos-1] = cols[3]
					alt_codon = "".join(alt_codon)

					if ref_aa != Seq(ref_codon).translate():
						raise Exception("CDS codon error")


					alt_aa = Seq(alt_codon).translate(stop_symbol='stop_codon')

					if ref_aa == alt_aa:
						mutation = 1
					else:
						mutation = 2
					
					record = [cols[0], pos, locus.transcript, tpos, ref_codon, codon_pos, alt_codon, ref_aa, alt_aa, protein_pos, mutation]

					print "\t".join(map(str,record))

				elif locus.feature == 'stop_codon':
					locations.append('CDS')
					tpos = calc_trasncript_relative_position(locus.transcript, pos)
					strand = transcripts[locus.transcript].strand
					if strand == '+':
						codon_pos = pos - locus.start + 1
					else:
						codon_pos = locus.end - pos + 1

					codon_tmp_pos = codon_pos
					if strand == '-':
						if codon_pos == 1:
							codon_tmp_pos = 3
						elif codon_pos == 3:
							codon_tmp_pos = 1


					if codon_tmp_pos == 1:
						codon = cols[2] + cols[5][:2]
					elif codon_tmp_pos == 2:
						codon = cols[4][-1] + cols[2] + cols[5][0]
					elif codon_tmp_pos == 3:
						codon = cols[4][-2:] + cols[2]

					if strand == '-':
						codon = reverse_complement(codon)

					protein_pos = len(protein_seq[transcript_to_protein[locus.transcript]])+1

					alt_codon = list(codon)
					if strand == '+':
						alt_codon[codon_pos-1] = cols[3]
					else:
						alt_codon[codon_pos-1] = reverse_complement(cols[3])
					alt_codon = "".join(alt_codon)

					ref_aa = Seq(codon).translate(stop_symbol='stop_codon')
					alt_aa = Seq(alt_codon).translate(stop_symbol='stop_codon')

					#print pos, codon_pos, codon, alt_codon, ref_aa, alt_aa

					if ref_aa != 'stop_codon':
						#print pos, locus.start, locus.end, locus.strand, ref_aa, codon
						raise Exception("Error stop codon")

					if ref_aa == alt_aa:
						mutation = 1
					else:
						mutation = 2

					record = [cols[0], pos, locus.transcript, tpos, codon, codon_pos, alt_codon, ref_aa, alt_aa, protein_pos, mutation]

					print "\t".join(map(str, record))

				elif locus.feature == 'exon':
					in_exon = True

			if not locations and in_exon:
				locations = ['exon']


			for feat in set(locations):
				print "%s\t%s\t%s\t%s\t%s" % (cols[0], pos, r.geneid, gene_pos, feat_types[feat])

