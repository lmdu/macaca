# Generated by Django 2.0 on 2017-12-20 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gene_pos', models.IntegerField(help_text='Relative position in gene')),
                ('feature', models.SmallIntegerField(choices=[(1, 'CDS'), (2, 'Exon'), (3, "3'UTR"), (4, 'Intron'), (5, "5'UTR")], help_text='Gene features')),
            ],
        ),
        migrations.CreateModel(
            name='Chromosome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Chromosome name, chr1-chr20', max_length=10)),
                ('size', models.BigIntegerField(help_text='Chromosome sequence length')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcript_pos', models.IntegerField(help_text='Relative position in transcript')),
                ('ref_codon', models.CharField(help_text='SNP site reference codon', max_length=3)),
                ('codon_pos', models.IntegerField(help_text='The SNP base position in codon')),
                ('alt_codon', models.CharField(help_text='Altered SNP site codon', max_length=3)),
                ('ref_aa', models.CharField(help_text='The reference amino acid for SNP codon', max_length=10)),
                ('alt_aa', models.CharField(help_text='The alteration amino acid for SNP codon', max_length=10)),
                ('protein_pos', models.IntegerField(help_text='Relative position of codon in protein')),
                ('synonymous', models.SmallIntegerField(choices=[(1, 'Non-synonymous'), (2, 'Synonymous')], help_text='Mutation type')),
            ],
        ),
        migrations.CreateModel(
            name='Funcannot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.SmallIntegerField(choices=[(1, 'GO'), (2, 'KEGG'), (3, 'Pfam'), (4, 'InterPro')], help_text='The function source database name')),
                ('accession', models.CharField(help_text='Functional database accession id', max_length=10)),
                ('description', models.CharField(help_text='Function description', max_length=200)),
                ('supplement', models.CharField(help_text='Other information', max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ensembl', models.CharField(help_text='Ensembl gene id', max_length=18)),
                ('name', models.CharField(help_text='Gene name', max_length=20)),
                ('description', models.CharField(help_text='Gene description', max_length=200)),
                ('biotype', models.SmallIntegerField(choices=[(1, 'protein coding'), (2, 'pseudogene'), (3, 'snRNA'), (4, 'rRNA'), (5, 'miRNA'), (6, 'miscRNA'), (7, 'snoRNA')], help_text='Gene coding types')),
                ('start', models.BigIntegerField(help_text='Gene start position')),
                ('end', models.BigIntegerField(help_text='Gene end position')),
                ('strand', models.CharField(help_text='Gene strand', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Group name that species belongs to', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='GroupSpecific',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Custom code number for species', max_length=5)),
                ('sample', models.CharField(help_text='sample seria number', max_length=20)),
                ('location', models.CharField(help_text='Where the sample collected', max_length=100)),
                ('non_variant', models.BigIntegerField(help_text='The number of non-variant sites')),
                ('heterozygous', models.IntegerField(help_text='The number of heterozygous sites')),
                ('homozygous', models.IntegerField(help_text='The number of homozygous sites')),
                ('variants', models.IntegerField(help_text='The number of total variant sites')),
                ('useable', models.BigIntegerField(help_text='The number of total useable sites')),
                ('heterozygosity', models.FloatField(help_text='heterozygosity')),
                ('snv_rate', models.FloatField(help_text='SNV rate')),
                ('pcr_duplicate', models.FloatField(help_text='PCR duplicates (%)')),
                ('mean_coverage', models.FloatField(help_text='Mean coverage')),
            ],
        ),
        migrations.CreateModel(
            name='Mutation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('synonymous', models.SmallIntegerField(choices=[(1, 'Non-synonymous'), (2, 'Synonymous')], help_text='Mutation type')),
            ],
        ),
        migrations.CreateModel(
            name='Snp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.BigIntegerField(help_text='Position in chromosome sequence')),
                ('reference', models.CharField(help_text='Reference base', max_length=1)),
                ('alteration', models.CharField(help_text='SNP alteration base', max_length=1)),
                ('five', models.CharField(help_text='Five flanking sequence 50 bp', max_length=50)),
                ('three', models.CharField(help_text='Three flanking sequence 50 bp', max_length=50)),
                ('chromosome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Chromosome')),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taxonomy', models.IntegerField(help_text='NCBI taxonomy number')),
                ('scientific', models.CharField(help_text='Scientific name', max_length=50)),
                ('common', models.CharField(help_text='Common name', max_length=50)),
                ('group', models.ForeignKey(help_text='Species group information', on_delete=django.db.models.deletion.CASCADE, to='snpdb.Group')),
            ],
        ),
        migrations.CreateModel(
            name='SpeciesSpecific',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Snp')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Species')),
            ],
        ),
        migrations.CreateModel(
            name='Transcript',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ensembl', models.CharField(help_text='Transcript ensembl id', max_length=18)),
                ('protein', models.CharField(help_text='Protein ensembl id', max_length=18)),
                ('start', models.IntegerField(help_text='Transcript start position')),
                ('end', models.IntegerField(help_text='Transcript end position')),
                ('strand', models.CharField(help_text='Transcript strand', max_length=1)),
                ('gene', models.ForeignKey(help_text='which gene for this transcript', on_delete=django.db.models.deletion.CASCADE, to='snpdb.Gene')),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genotype', models.SmallIntegerField(choices=[(1, 'Homozygote'), (2, 'Heterozygote')], help_text='Alteration genotype')),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Individual')),
                ('snp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Snp')),
            ],
        ),
        migrations.AddField(
            model_name='mutation',
            name='snp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Snp'),
        ),
        migrations.AddField(
            model_name='individual',
            name='species',
            field=models.ForeignKey(help_text='Species information', on_delete=django.db.models.deletion.CASCADE, to='snpdb.Species'),
        ),
        migrations.AddField(
            model_name='groupspecific',
            name='snp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Snp'),
        ),
        migrations.AddField(
            model_name='funcannot',
            name='function',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Function'),
        ),
        migrations.AddField(
            model_name='funcannot',
            name='gene',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Gene'),
        ),
        migrations.AddField(
            model_name='comment',
            name='snp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Snp'),
        ),
        migrations.AddField(
            model_name='comment',
            name='transcript',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Transcript'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='gene',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Gene'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='snp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snpdb.Snp'),
        ),
    ]
