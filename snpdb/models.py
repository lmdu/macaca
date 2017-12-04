# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Chromosome(models.Model):
	name = models.CharField(max_length=10)
	size = models.IntegerField()

class Species(models.Model):
	common_name = models.CharField(max_length=50)
	scientific_name = models.CharField(max_length=50)
	identifier = models.CharField(max_length=5)
	sample = models.CharField(max_length=20)
	location = models.CharField(max_length=100)
	taxonomy = models.IntegerField()

class Snp(models.Model):
	chromosome = models.ForeignKey(Chromosome)
	position = models.IntegerField()
	reference = models.CharField(max_length=1)
	alteration = models.CharField(max_length=1)
	five_flank = models.CharField(max_length=50)
	three_flank = models.CharField(max_length=50)

class Variant(models.Model):
	NONMUTATION = 0
	HOMOZYGOTE = 1
	HETEROZYGOTE = 2
	GENOTYPES = (
		(NONMUTATION, '0/0'),
		(HETEROZYGOTE, '0/1'),
		(HOMOZYGOTE, '1/1'),
	)
	snp = models.ForeignKey(Snp)
	species = models.ForeignKey(Species)
	genotype = models.IntegerField(choices=GENOTYPES)

class Gene(models.Model):
	ensembl_id = models.CharField(max_length=18)
	name = models.CharField(max_length=20)
	description = models.CharField(max_length=200)
	start = models.IntegerField()
	end = models.IntegerField()
	strand = models.CharField(max_length=1)

class Transcript(models.Model):
	ensembl_id = models.CharField(max_length=18)
	parent = models.ForeignKey('Gene')
	protein = models.CharField(max_length=18)

class GeneAnnotation(models.Model):
	CDS = 1
	EXON = 2
	THREE_UTR = 3
	INTRON = 4
	FIVE_UTR = 5
 	FEATURES = (
		(INTRON, 'Intron'),
		(CDS, 'CDS'),
		(EXON, 'Exon'),
		(THREE_UTR, "3'UTR"),
		(FIVE_UTR, "5'UTR")
	)
	snp = models.ForeignKey(Snp)
	from_gene = models.ForeignKey(Gene)
	gene_relative_position = models.IntegerField()
	gene_feature = models.IntegerField(choices=FEATURES)

class TanscriptAnnotation(models.Model):
	snp = models.ForeignKey(Snp)
	from_transcript = models.ForeignKey(Transcript)
	transcript_relative_position = models.IntegerField()
	codon = models.CharField(max_length=3)
	protein_relative_position = models.IntegerField()
	amino_acid = models.CharField(max_length=1)



