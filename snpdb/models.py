# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Chromosome(models.Model):
	name = models.CharField(max_length=10)
	size = models.IntegerField()

class Snp(models.Model):
	chrom = models.ForeignKey('Chromosome')
	position = models.IntegerField()
	reference = models.CharField(max_length=1)
	alteration = models.CharField(max_length=1)
	five = models.CharField(max_length=100)
	three = models.CharField(max_length=100)

class Variant(models.Model):
	NONMUTATION = 0
	HOMOZYGOTE = 1
	HETEROZYGOTE = 2
	GENOTYPES = (
		(NONMUTATION, '0/0'),
		(HETEROZYGOTE, '0/1'),
		(HOMOZYGOTE, '1/1'),
	)
	snp = models.ForeignKey('Snp')
	species = models.ForeignKey('Species')
	genotype = models.IntegerField(choices=GENOTYPES)

class Species(models.Model):
	common = models.CharField(max_length=50)
	scientific = models.CharField(max_length=50)
	code = models.CharField(max_length=5)
	sample = models.CharField(max_length=20)
	location = models.CharField(max_length=100)
	taxonomy = models.IntegerField()

class GeneAnnotation(models.Model):
	CDS = 1
	EXON = 2
	THREE_UTR = 3
	INTRON = 4
	FIVE_UTR = 5
 	FEATURES = (
		(INTRON, 'Intron')
		(CDS, 'CDS'),
		(EXON, 'Exon'),
		(THREE_UTR, "3'UTR"),
		(FIVE_UTR, "5'UTR")
	)
	snp = models.ForeignKey('Snp')
	gene = models.ForeignKey('Gene')
	relpos = models.IntegerField()
	feature = models.IntegerField(choices=FEATURES)

class TanscriptAnnotation(models.Model):
	snp = models.ForeignKey('Snp')
	transcript = models.ForeignKey('Transcript')
	trelpos = models.IntegerField()
	codon = models.CharField(max_length=3)
	prelpos = models.IntegerField()
	aa = models.CharField(max_length=1)

class Gene(models.Model):
	gid = models.CharField(max_length=30)
	name = models.CharField(max_length=20)
	description = models.CharField(max_length=200)
	strand = models.CharField(max_length=1)
	

class Transcript(models.Model):
	tid = models.CharField(max_length=30)
	parent = models.ForeignKey('Gene')
	protein = models.CharField(max_length=30)

