# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Chromosome(models.Model):
	name = models.CharField(max_length=10, help_text="Chromosome name, chr1-chr20")
	size = models.BigIntegerField(help_text = "Chromosome sequence length")

class Group(models.Model):
	name = models.CharField(max_length=15, help_text="Group name that species belongs to")

class Species(models.Model):
	taxonomy = models.IntegerField(help_text="NCBI taxonomy number")
	scientific = models.CharField(max_length=50, help_text="Scientific name")
	common = models.CharField(max_length=50, help_text="Common name")
	group = models.ForeignKey(Group, on_delete=models.CASCADE, help_text="Species group information")

class Individual(models.Model):
	species = models.ForeignKey(Species, on_delete=models.CASCADE, help_text="Species information")
	code = models.CharField(max_length=5,help_text="Custom code number for species")
	sample = models.CharField(max_length=20, help_text="sample seria number")
	location = models.CharField(max_length=100, help_text="Where the sample collected")
	non_variant = models.BigIntegerField(help_text = "The number of non-variant sites")
	heterozygous = models.IntegerField(help_text="The number of heterozygous sites")
	homozygous = models.IntegerField(help_text="The number of homozygous sites")
	variants = models.IntegerField(help_text="The number of total variant sites")
	useable = models.BigIntegerField(help_text="The number of total useable sites")
	heterozygosity = models.FloatField(help_text="heterozygosity")
	snv_rate = models.FloatField(help_text="SNV rate")
	pcr_duplicate = models.FloatField(help_text="PCR duplicates (%)")
	mean_coverage = models.FloatField(help_text="Mean coverage")

class Snp(models.Model):
	chrom = models.ForeignKey(Chromosome, on_delete=models.CASCADE)
	position = models.BigIntegerField(help_text="Position in chromosome sequence")
	reference = models.CharField(max_length=1, help_text="Reference base")
	alteration = models.CharField(max_length=1, help_text="SNP alteration base")
	five = models.CharField(max_length=50, help_text="Five flanking sequence 50 bp")
	three = models.CharField(max_length=50, help_text="Three flanking sequence 50 bp")

class Variant(models.Model):
	GENOTYPES = (
		(1, 'Homozygote'),
		(2, 'Heterozygote')
	)
	snp = models.ForeignKey(Snp, on_delete=models.CASCADE)
	individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
	genotype = models.SmallIntegerField(choices=GENOTYPES, help_text="Alteration genotype")

class Gene(models.Model):
	CODING_TYPES = (
		(1, 'protein coding'),
		(2, 'pseudogene'),
		(3, 'snRNA'),
		(4, 'rRNA'),
		(5, 'miRNA'),
		(6, 'miscRNA'),
		(7, 'snoRNA')
	)
	ensembl_id = models.CharField(max_length=18, help_text="Ensembl gene id")
	name = models.CharField(max_length=20, help_text="Gene name")
	description = models.CharField(max_length=200, help_text="Gene description")
	biotype = models.SmallIntegerField(choices=CODING_TYPES, help_text="Gene coding types")
	start = models.BigIntegerField(help_text="Gene start position")
	end = models.BigIntegerField(help_text="Gene end position")
	strand = models.CharField(max_length=1, help_text="Gene strand")

class Transcript(models.Model):
	ensembl_id = models.CharField(max_length=18, help_text="Transcript ensembl id")
	parent = models.ForeignKey(Gene, on_delete=models.CASCADE, help_text="which gene for this transcript")
	protein = models.CharField(max_length=18, help_text="Protein ensembl id")
	start = models.IntegerField(help_text="Transcript start position")
	end = models.IntegerField(help_text="Transcript end position")
	strand = models.CharField(max_length=1, help_text="Transcript strand")

class GeneAnnot(models.Model):
	FEATURES = (
		(1, 'CDS'),
		(2, 'Exon'),
		(3, "3'UTR"),
		(4, 'Intron'),
		(5, "5'UTR")
	)
	snp = models.ForeignKey(Snp, on_delete=models.CASCADE)
	gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
	gene_pos = models.IntegerField(help_text="Relative position in gene")
	feature = models.SmallIntegerField(choices=FEATURES, help_text="Gene features")

class TransAnnot(models.Model):
	MUTATION_TYPES = (
		(1, 'Non-synonymous'),
		(2, 'Synonymous'),
	)
	snp = models.ForeignKey(Snp, on_delete=models.CASCADE)
	transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE)
	transcript_pos = models.IntegerField(help_text="Relative position in transcript")
	ref_codon = models.CharField(max_length=3, help_text="SNP site reference codon")
	codon_pos = models.IntegerField(help_text="The SNP base position in codon")
	alt_codon = models.CharField(max_length=3, help_text="Altered SNP site codon")
	ref_aa = models.CharField(max_length=10, help_text="The reference amino acid for SNP codon")
	alt_aa = models.CharField(max_length=10, help_text="The alteration amino acid for SNP codon")
	protein_pos = models.IntegerField(help_text="Relative position of codon in protein")
	synonymous = models.SmallIntegerField(choices=MUTATION_TYPES, help_text="Mutation type")

class Function(models.Model):
	FUNC_TYPES = (
		(1, 'GO'),
		(2, 'KEGG'),
		(3, 'Pfam'),
		(4, 'InterPro')
	)
	source = models.SmallIntegerField(choices=FUNC_TYPES, help_text="The function source database name")
	accession = models.CharField(max_length=10, help_text="Functional database accession id")
	descript = models.CharField(max_length=200, help_text="Function description")
	supplement = models.CharField(max_length=80, help_text="Other information")

class Funcannot(models.Model):
	gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
	function = models.ForeignKey(Function, on_delete=models.CASCADE)

class GroupSpec(models.Model):
	snp = models.ForeignKey(Snp, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)

class SpecieSpec(models.Model):
	snp = models.ForeignKey(Snp, on_delete=models.CASCADE)
	species = models.ForeignKey(Species, on_delete=models.CASCADE)
	
