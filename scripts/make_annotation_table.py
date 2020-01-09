import os
import sys
import gzip
import math
import pyfaidx
import intersection

from Bio.Seq import Seq

work_dir = '/home/ming/macaca/snvs'
table_dir = os.path.join(work_dir, 'tables')
data_dir = os.path.join(work_dir, 'data')
ref_dir = os.path.join(work_dir, 'ref')

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

gtf_file = os.path.join(ref_dir, 'Macaca_mulatta.Mmul_8.0.1.97.gtf.gz')
cds_file = os.path.join(ref_dir, 'Macaca_mulatta.Mmul_8.0.1.cds.fa')
protein_file = os.path.join(ref_dir, 'Macaca_mulatta.Mmul_8.0.1.pep.fa')

snp_file = os.path.join(table_dir, 'snp.table')

gannot_out = open(os.path.join(table_dir, 'gene_annot.table'), 'w')
tannot_out = open(os.path.join(table_dir, 'transcript_annot.table'), 'w')
mutate_out = open(os.path.join(table_dir, 'mutation.table'), 'w')

gene_mapping = {}
with open(os.path.join(table_dir, 'gene.table')) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		gene_mapping[cols[1]] = cols[0]

transcript_mapping = {}
transcript_to_protein = {}
with open(os.path.join(table_dir, 'transcript.table')) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		transcript_mapping[cols[1]] = cols[0]
		transcript_to_protein[cols[1]] = cols[2]

stopcodon_mapping = {}
with open(os.path.join(ref_dir, 'incomplete_stop_codon.txt')) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		stopcodon_mapping[(int(cols[1]), int(cols[2]))] = (cols[3], int(cols[4]))

cds_seq = pyfaidx.Fasta(cds_file, key_function=lambda x: x.split('.')[0])
protein_seq = pyfaidx.Fasta(protein_file, key_function=lambda x: x.split('.')[0])

gene_tree = {}
feat_tree = {}
transcripts = {}
exons = {}
cds = {}
gannot_count = 0
tannot_count = 0
mutation_count = 0

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

progress = 0
with open(snp_file) as fh:
	#fh.readline()
	for line in fh:
		cols = line.strip().split('\t')
		#for debugging incomplete stop codon
		#if int(cols[0]) < 94800000:
		#	continue

		pos = int(cols[1])
		res = gene_tree[cols[6]].find(pos, pos)
		for r in res:
			gene_pos = calc_gene_relative_position(r, pos)

			loci = feat_tree[r.geneid].find(pos, pos)

			locations = []
			mutations = []
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
					
					tannot_count += 1
					record = (tannot_count, tpos, ref_codon, codon_pos, alt_codon, ref_aa, alt_aa, protein_pos, mutation, cols[0], transcript_mapping[locus.transcript])
					
					mutations.append(mutation)

					tannot_out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % record)

				elif locus.feature == 'stop_codon':
					locations.append('CDS')
					tpos = calc_trasncript_relative_position(locus.transcript, pos)
					strand = transcripts[locus.transcript].strand
					
					if locus.end - locus.start + 1 != 3:
						codon, order = stopcodon_mapping[(locus.start, locus.end)]

						if strand == '+':
							if order == 0:
								if pos == locus.start:
									codon_pos = 1
								else:
									codon_pos = 2
							else:
								if pos == locus.end:
									codon_pos = 3
								else:
									codon_pos = 2
						else:
							if order == 0:
								if pos == locus.end:
									codon_pos = 1
								else:
									codon_pos = 2
							else:
								if pos == locus.start:
									codon_pos = 3
								else:
									codon_pos = 2

					else:
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
						print(pos, locus.start, locus.end, locus.strand, ref_aa, codon)
						raise Exception("Error stop codon")

					if ref_aa == alt_aa:
						mutation = 1
					else:
						mutation = 2

					tannot_count += 1
					record = (tannot_count, tpos, codon, codon_pos, alt_codon, ref_aa, alt_aa, protein_pos, mutation, cols[0], transcript_mapping[locus.transcript])
					
					mutations.append(mutation)

					tannot_out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % record)

				elif locus.feature == 'exon':
					in_exon = True

			if not locations and in_exon:
				locations = ['exon']


			for feat in set(locations):
				gannot_count += 1
				gannot_out.write("%s\t%s\t%s\t%s\t%s\n" % (gannot_count, gene_pos, feat_types[feat], gene_mapping[r.geneid], cols[0]))

			for muta in set(mutations):
				mutation_count += 1
				mutate_out.write("%s\t%s\t%s\n" % (mutation_count, muta, cols[0]))

		progress += 1

		if progress % 100000 == 0:
			print("Processed SNPs: %s" % progress)

