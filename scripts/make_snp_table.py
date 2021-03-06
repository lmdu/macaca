import os
import sys
import gzip
import glob
import pyfaidx

work_dir = '/home/ming/macaca/snvs'
table_dir = os.path.join(work_dir, 'tables')
data_dir = os.path.join(work_dir, 'data')
ref_dir = os.path.join(work_dir, 'ref')

genome_file = os.path.join(ref_dir, 'Macaca_mulatta.Mmul_8.0.1.dna.fa')
snp_files = glob.glob(os.path.join(data_dir, 'liftsorted', '*.tsv.gz'))

#get species information
groups = {}
with open(os.path.join(table_dir, 'group.table')) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		groups[cols[1]] = cols[0]

species = {}
species_mapping = {}
with open(os.path.join(table_dir, 'species.table')) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		species[cols[1]] = cols[0]
		species_mapping[cols[0]] = cols[5]

samples = {}
with open(os.path.join(table_dir, 'individual.table')) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		samples[cols[1]] = (cols[0], cols[-1], species_mapping[cols[-1]])

snp_out = open(os.path.join(table_dir, 'snp.table'), 'w')
var_out = open(os.path.join(table_dir, 'variant.table'), 'w')
non_out = open(os.path.join(table_dir, 'non_variant.table'), 'w')
gsp_out = open(os.path.join(table_dir, 'group_specific.table'), 'w')
ssp_out = open(os.path.join(table_dir, 'species_specific.table'), 'w')
sdp_out = open(os.path.join(table_dir, 'shared_variant.table'), 'w')

genotypes = {'1/1': 1, '0/1': 2, '0/0': 3}
genome = pyfaidx.Fasta(genome_file)
snp_id = 0
var_id = 0
non_id = 0
gsp_id = 0
ssp_id = 0
sdp_id = 0

codes = ["CR1","CR2","CR3","JM1","JM2","TW1","CE1",
		 "CE2","CE3","CE4","CE5","TM1","TM2","AM1",
		 "SM1","SM2","PM1","PM2","LM1","BM1"]

for snp_file in snp_files:
	chrom = os.path.basename(snp_file).split('_')[1]
	chrom = chrom.lstrip('chr0')
	seq = str(genome[chrom])
	with gzip.open(snp_file, 'rt') as fh:
		#codes = fh.readline().strip().split()[4:-1]
		for line in fh:
			cols = line.strip().split('\t')
			if '0/1' not in cols[4:-1] and '1/1' not in cols[4:-1]:
				continue

			pos = int(cols[1])

			if pos == 0:
				continue

			snp_id += 1
			
			start = pos - 51
			if start<0:
				start = 0
			end = pos + 50

			left = seq[start:pos-1]
			right = seq[pos:end]

			snp_out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (snp_id, cols[1], cols[2], cols[3], left, right, chrom))

			types = cols[4:-1]
			for idx, t in enumerate(types):
				if t == '.':
					continue
				elif t == '0/0':
					non_id += 1
					non_out.write("%s\t%s\t%s\t%s\n" % (non_id, chrom, samples[codes[idx]][0], snp_id))
					continue

				var_id += 1
				var_out.write("%s\t%s\t%s\t%s\t%s\n" % (var_id, genotypes[t], chrom, samples[codes[idx]][0], snp_id))

			#check shared snp
			all_types = [1 if t == '0/1' or t == '1/1' else 0 for t in types]
			if all(all_types):
				sdp_id += 1
				sdp_out.write("%s\t%s\t%s\n" % (sdp_id, chrom, snp_id))

			#check specific snp
			if '.' in types or '0/1' in types:
				continue

			gmat = {g:[] for g in groups.values()}
			smat = {s:[] for s in species.values()}
			for idx, genotype in enumerate(types):
				_, species_id, group_id = samples[codes[idx]]
				n = 1 if genotype == '1/1' else 0

				gmat[group_id].append(n)
				smat[species_id].append(n)

			#process group specific snps
			r = [sum(gmat[g]) for g in gmat]

			if r.count(0) == len(r)-1:
				for g in gmat:
					if sum(gmat[g]) > 0:
						if all(gmat[g]):
							gsp_id += 1
							gsp_out.write("%s\t%s\t%s\t%s\n" % (gsp_id, chrom, g, snp_id))
						break

			#process species specific snps
			r = [sum(smat[s]) for s in smat]

			if r.count(0) == len(r)-1:
				for s in smat:
					if sum(smat[s]) > 0:
						if all(smat[s]):
							ssp_id += 1
							ssp_out.write("%s\t%s\t%s\t%s\n" % (ssp_id, chrom, snp_id, s))
						break

	print(snp_file)

snp_out.close()
var_out.close()
non_out.close()
gsp_out.close()
ssp_out.close()
sdp_out.close()
