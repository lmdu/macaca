# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-05 05:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chromosome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('size', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ensembl_id', models.CharField(max_length=18)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('strand', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='GeneAnnotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gene_relative_position', models.IntegerField()),
                ('gene_feature', models.IntegerField(choices=[(4, 'Intron'), (1, 'CDS'), (2, 'Exon'), (3, "3'UTR"), (5, "5'UTR")])),
                ('from_gene', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Gene')),
            ],
        ),
        migrations.CreateModel(
            name='Snp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('reference', models.CharField(max_length=1)),
                ('alteration', models.CharField(max_length=1)),
                ('five_flank', models.CharField(max_length=50)),
                ('three_flank', models.CharField(max_length=50)),
                ('chromosome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Chromosome')),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taxonomy', models.IntegerField()),
                ('scientific_name', models.CharField(max_length=50)),
                ('common_name', models.CharField(max_length=50)),
                ('group', models.CharField(max_length=15)),
                ('code', models.CharField(max_length=5)),
                ('sample', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=100)),
                ('non_variant', models.BigIntegerField()),
                ('heterozygous', models.IntegerField()),
                ('homozygous', models.IntegerField()),
                ('total_variant', models.IntegerField()),
                ('total_useable', models.BigIntegerField()),
                ('heterozygosity', models.FloatField()),
                ('snv_rate', models.FloatField()),
                ('pcr_duplicates', models.FloatField()),
                ('mean_coverage', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='TanscriptAnnotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcript_relative_position', models.IntegerField()),
                ('codon', models.CharField(max_length=3)),
                ('protein_relative_position', models.IntegerField()),
                ('amino_acid', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Transcript',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ensembl_id', models.CharField(max_length=18)),
                ('protein', models.CharField(max_length=18)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Gene')),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genotype', models.IntegerField(choices=[(0, '0/0'), (2, '0/1'), (1, '1/1')])),
                ('snp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Snp')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Species')),
            ],
        ),
        migrations.AddField(
            model_name='tanscriptannotation',
            name='from_transcript',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Transcript'),
        ),
        migrations.AddField(
            model_name='tanscriptannotation',
            name='snp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Snp'),
        ),
        migrations.AddField(
            model_name='geneannotation',
            name='snp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Snp'),
        ),
    ]