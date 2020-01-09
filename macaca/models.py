from django.apps import apps
from django.db import models

# Create your models here.
class Chromosome(models.Model):
	name = models.CharField(max_length=5, help_text="Chromosome name, chr1-chr20")
	size = models.IntegerField(help_text="Chromosome sequence length")

	class Meta:
		db_table = 'chromosome'

class Groups(models.Model):
	name = models.CharField(max_length=15, help_text="Group name that species belongs to")

	class Meta:
		db_table = 'groups'

class Species(models.Model):
	taxonomy = models.IntegerField(help_text="NCBI taxonomy number")
	scientific = models.CharField(max_length=50, help_text="Scientific name")
	common = models.CharField(max_length=50, help_text="Common name")
	code = models.CharField(max_length=10, help_text="species code")
	group = models.ForeignKey(Groups, on_delete=models.CASCADE, help_text="Species group information")

	class Meta:
		db_table = 'species'

class Individual(models.Model):
	code = models.CharField(max_length=5, help_text="Custom code number for species")
	sample = models.CharField(max_length=20, help_text="sample seria number")
	location = models.CharField(max_length=100, help_text="Where the sample collected")
	non_variant = models.BigIntegerField(help_text="The number of non-variant sites")
	heterozygous = models.IntegerField(help_text="The number of heterozygous sites")
	homozygous = models.IntegerField(help_text="The number of homozygous sites")
	variants = models.IntegerField(help_text="The number of total variant sites")
	useable = models.BigIntegerField(help_text="The number of total useable sites")
	heterozygosity = models.FloatField(help_text="heterozygosity")
	snv_rate = models.FloatField(help_text="SNV rate")
	pcr_duplicate = models.FloatField(help_text="PCR duplicates (%)")
	mean_coverage = models.FloatField(help_text="Mean coverage")
	species = models.ForeignKey(Species, on_delete=models.CASCADE, help_text="Species information")

	class Meta:
		db_table = 'individual'

class Snp(models.Model):
	position = models.IntegerField(db_index=True, help_text="Position in chromosome sequence")
	reference = models.CharField(max_length=1, help_text="Reference base")
	alteration = models.CharField(max_length=1, help_text="SNP alteration base")
	five = models.CharField(max_length=50, help_text="Five flanking sequence 50 bp")
	three = models.CharField(max_length=50, help_text="Three flanking sequence 50 bp")
	chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)

	class Meta:
		db_table = 'snp'
		ordering = ['id']
		index_together = ['position', 'chromosome']

class Snps(Snp):
	@classmethod
	def shard(cls, chrom):
		cls._meta.db_table = 'snp{}'.format(chrom)
		return cls

	class Meta:
		proxy = True

class Variant(models.Model):
	GENOTYPES = (
		(1, 'Homozygote'),
		(2, 'Heterozygote')
	)
	genotype = models.PositiveSmallIntegerField(choices=GENOTYPES, db_index=True, help_text="Alteration genotype")
	chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)
	individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
	snp = models.ForeignKey(Snps, on_delete=models.CASCADE)

	class Meta:
		db_table = 'variant'
		ordering = ['id']
		index_together = [
			['genotype', 'snp'],
			['genotype', 'individual'],
			['individual', 'snp'],
			['genotype', 'individual', 'snp']
		]

class Variants(Variant):
	@classmethod
	def shard(cls, chrom):
		cls._meta.db_table = 'variant{}'.format(chrom)
		return cls

	class Meta:
		proxy = True

class Nonvariant(models.Model):
	individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
	snp = models.ForeignKey(Snps, on_delete=models.CASCADE)

	class Meta:
		db_table = 'nonvariant'
		ordering = ['id']
		index_together = ['individual', 'snp']

class Nonvariants(Nonvariant):
	@classmethod
	def shard(cls, chrom):
		cls._meta.db_table = 'nonvariant{}'.format(chrom)
		return cls

	class Meta:
		proxy = True

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
	ensembl = models.CharField(max_length=18, db_index=True, help_text="Ensembl gene id")
	name = models.CharField(max_length=20, help_text="Gene symbol")
	description = models.CharField(max_length=200, help_text="Gene description")
	#biotype = models.PositiveSmallIntegerField(choices=CODING_TYPES, help_text="Gene coding types")
	biotype = models.CharField(max_length=30, help_text="gene coding type")
	start = models.IntegerField(help_text="Gene start position")
	end = models.IntegerField(help_text="Gene end position")
	strand = models.CharField(max_length=1, help_text="Gene strand")
	chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)

	class Meta:
		db_table = 'gene'

class Transcript(models.Model):
	ensembl = models.CharField(max_length=18, help_text="Transcript ensembl id")
	protein = models.CharField(max_length=18, help_text="Protein ensembl id")
	start = models.IntegerField(help_text="Transcript start position")
	end = models.IntegerField(help_text="Transcript end position")
	strand = models.CharField(max_length=1, help_text="Transcript strand")
	gene = models.ForeignKey(Gene, on_delete=models.CASCADE, help_text="which gene for this transcript")

	class Meta:
		db_table = 'transcript'

class Gannot(models.Model):
	'''Gene annotation'''
	FEATURE_TYPES = (
		(1, 'CDS'),
		(2, 'Exon'),
		(3, "3'UTR"),
		(4, 'Intron'),
		(5, "5'UTR")
	)
	gene_pos = models.IntegerField(help_text="Relative position in gene")
	feature = models.PositiveSmallIntegerField(choices=FEATURE_TYPES, db_index=True, help_text="Gene features")
	gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
	snp = models.ForeignKey(Snps, on_delete=models.CASCADE)

	class Meta:
		db_table = 'gannot'
		ordering = ['id']
		index_together = [
			['feature', 'snp'],
			['feature', 'gene'],
			['feature', 'gene', 'snp'],
		]

class Tannot(models.Model):
	'''Transcript annotation'''
	MUTATION_TYPES = (
		(1, 'Synonymous'),
		(2, 'Non-synonymous'),
	)
	transcript_pos = models.IntegerField(help_text="Relative position in transcript")
	ref_codon = models.CharField(max_length=3, help_text="SNP site reference codon")
	codon_pos = models.IntegerField(help_text="The SNP base position in codon")
	alt_codon = models.CharField(max_length=3, help_text="Altered SNP site codon")
	ref_aa = models.CharField(max_length=10, help_text="The reference amino acid for SNP codon")
	alt_aa = models.CharField(max_length=10, help_text="The alteration amino acid for SNP codon")
	protein_pos = models.IntegerField(help_text="Relative position of codon in protein")
	synonymous = models.PositiveSmallIntegerField(choices=MUTATION_TYPES, db_index=True, help_text="Mutation type")
	snp = models.ForeignKey(Snps, on_delete=models.CASCADE)
	transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE)

	class Meta:
		db_table = 'tannot'

class Mutation(models.Model):
	'''Synonymous or non-synonymous mutations'''
	MUTATION_TYPES = (
		(1, 'Synonymous'),
		(2, 'Non-synonymous'),
	)
	synonymous = models.PositiveSmallIntegerField(choices=MUTATION_TYPES, db_index=True, help_text="Mutation type")
	snp = models.ForeignKey(Snps, on_delete=models.CASCADE)

	class Meta:
		db_table = 'mutation'
		ordering = ['id']
		index_together = ['synonymous', 'snp']

class Function(models.Model):
	'''Functional Terms'''
	FUNC_TYPES = (
		(1, 'GO'),
		(2, 'KEGG'),
		(3, 'Pfam'),
		(4, 'InterPro')
	)
	source = models.PositiveSmallIntegerField(choices=FUNC_TYPES, db_index=True, help_text="The function source database name")
	accession = models.CharField(max_length=15, help_text="Functional database accession id")
	description = models.CharField(max_length=200, help_text="Function description")
	supplement = models.CharField(max_length=80, help_text="Other information")

	class Meta:
		db_table = 'function'

class Funcannot(models.Model):
	'''Functional annotations'''
	function = models.ForeignKey(Function, on_delete=models.CASCADE)
	gene = models.ForeignKey(Gene, on_delete=models.CASCADE)

	class Meta:
		db_table = 'funcannot'
		index_together = ['function', 'gene']

class GroupSpecific(models.Model):
	#the order of foreinkey field is sorted by alphabet
	chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)
	group = models.ForeignKey(Groups, on_delete=models.CASCADE)
	snp = models.ForeignKey(Snps, on_delete=models.CASCADE)

	class Meta:
		db_table = 'group_specific'
		ordering = ['id']
		index_together = [
			['snp', 'group'],
			['snp', 'chromosome'],
			['snp', 'group', 'chromosome']
		]

class SpeciesSpecific(models.Model):
	chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)
	snp = models.ForeignKey(Snps, on_delete=models.CASCADE)
	species = models.ForeignKey(Species, on_delete=models.CASCADE)
	
	class Meta:
		db_table = 'species_specific'
		ordering = ['id']
		index_together = [
			['snp', 'species'],
			['snp', 'chromosome'],
			['snp', 'species', 'chromosome']
		]

class Statistics(models.Model):
	feature = models.IntegerField(db_index=True)
	genotype = models.IntegerField(db_index=True)
	mutation = models.IntegerField(db_index=True)
	counts = models.IntegerField()
	chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)
	individual = models.ForeignKey(Individual, on_delete=models.CASCADE)

	class Meta:
		db_table = 'statistics'
		index_together = ['feature', 'genotype', 'mutation']

class Orthology(models.Model):
	human_ensembl = models.CharField(max_length=18, db_index=True, help_text="human ensembl gene id")
	human_hgnc = models.CharField(max_length=10, help_text="human gene hgnc id")
	human_name = models.CharField(max_length=200, help_text="human gene name")
	human_symbol = models.CharField(max_length=20, help_text="human gene symbol")
	support = models.CharField(max_length=255, help_text="orthology support database")
	gene = models.ForeignKey(Gene, on_delete=models.CASCADE)

	class Meta:
		db_table = 'orthology'
		index_together = ['human_ensembl', 'gene']

class Drug(models.Model):
	DRUG_TYPES = (
		(1, 'biotech'),
		(2, 'small molecule')
	)
	partner = models.CharField(max_length=10, help_text="drugbank target gene id")
	drug_id = models.CharField(max_length=7, db_index=True, help_text="drugbank durg id")
	drug_name = models.CharField(max_length=255, help_text="drugbank drug name")
	#drug_type = models.PositiveSmallIntegerField(choices=DRUG_TYPES, help_text="drugbank drug type")
	drug_type = models.CharField(max_length=20, help_text="drugbank drug type")
	orthology = models.ForeignKey(Orthology, on_delete=models.CASCADE)

	class Meta:
		db_table = 'drug'
		index_together = ['drug_id', 'orthology']

class Disease(models.Model):
	MAPPING_KEYS = (
		(1, "The disorder was positioned by mapping of the wildtype gene"),
		(2, "The disease phenotype itself was mapped"),
		(3, "The molecular basis of the disorder is known"),
		(4, "The disorder is a chromosome deletion or duplication syndrome")
	)
	gomim = models.IntegerField(help_text="gene omim accession")
	pomim = models.IntegerField(db_index=True, help_text="disease omim accession")
	phenotype = models.CharField(max_length=255, help_text="disease phenotype description")
	mapkey = models.PositiveSmallIntegerField(choices=MAPPING_KEYS, help_text="Phenotype mapping key")
	inheritance = models.CharField(max_length=80, help_text="Inheritance")
	orthology = models.ForeignKey(Orthology, on_delete=models.CASCADE)
	
	class Meta:
		db_table = 'disease'
		index_together = ['pomim', 'orthology']

