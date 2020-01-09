import sys
import pyfaidx

#input files
genome_fasta = sys.argv[1]

fa = pyfaidx.Fasta(genome_fasta)

for i in range(1, 21):
	print("{}\tchr{}\t{}".format(i, i, len(fa[str(i)])))
