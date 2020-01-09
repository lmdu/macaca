# Generated by Django 2.0.3 on 2018-05-16 07:07

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
                ('name', models.CharField(help_text='Chromosome name, chr1-chr20', max_length=5)),
                ('size', models.IntegerField(help_text='Chromosome sequence length')),
            ],
            options={
                'db_table': 'chromosome',
            },
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gomim', models.IntegerField(help_text='gene omim accession')),
                ('pomim', models.IntegerField(db_index=True, help_text='disease omim accession')),
                ('phenotype', models.CharField(help_text='disease phenotype description', max_length=255)),
                ('mapkey', models.PositiveSmallIntegerField(choices=[(1, 'The disorder was positioned by mapping of the wildtype gene'), (2, 'The disease phenotype itself was mapped'), (3, 'The molecular basis of the disorder is known'), (4, 'The disorder is a chromosome deletion or duplication syndrome')], help_text='Phenotype mapping key')),
                ('inheritance', models.CharField(help_text='Inheritance', max_length=50)),
            ],
            options={
                'db_table': 'disease',
            },
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner', models.CharField(help_text='drugbank target gene id', max_length=10)),
                ('drug_id', models.CharField(db_index=True, help_text='drugbank durg id', max_length=7)),
                ('drug_name', models.CharField(help_text='drugbank drug name', max_length=255)),
                ('drug_type', models.PositiveSmallIntegerField(choices=[(1, 'biotech'), (2, 'small molecule')], help_text='drugbank drug type')),
            ],
            options={
                'db_table': 'drug',
            },
        ),
        migrations.CreateModel(
            name='Funcannot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'funcannot',
            },
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.PositiveSmallIntegerField(choices=[(1, 'GO'), (2, 'KEGG'), (3, 'Pfam'), (4, 'InterPro')], db_index=True, help_text='The function source database name')),
                ('accession', models.CharField(help_text='Functional database accession id', max_length=15)),
                ('description', models.CharField(help_text='Function description', max_length=200)),
                ('supplement', models.CharField(help_text='Other information', max_length=80)),
            ],
            options={
                'db_table': 'function',
            },
        ),
        migrations.CreateModel(
            name='Gannot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gene_pos', models.IntegerField(help_text='Relative position in gene')),
                ('feature', models.PositiveSmallIntegerField(choices=[(1, 'CDS'), (2, 'Exon'), (3, "3'UTR"), (4, 'Intron'), (5, "5'UTR")], db_index=True, help_text='Gene features')),
            ],
            options={
                'db_table': 'gannot',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ensembl', models.CharField(db_index=True, help_text='Ensembl gene id', max_length=18)),
                ('name', models.CharField(help_text='Gene symbol', max_length=20)),
                ('description', models.CharField(help_text='Gene description', max_length=200)),
                ('biotype', models.PositiveSmallIntegerField(choices=[(1, 'protein coding'), (2, 'pseudogene'), (3, 'snRNA'), (4, 'rRNA'), (5, 'miRNA'), (6, 'miscRNA'), (7, 'snoRNA')], help_text='Gene coding types')),
                ('start', models.IntegerField(help_text='Gene start position')),
                ('end', models.IntegerField(help_text='Gene end position')),
                ('strand', models.CharField(help_text='Gene strand', max_length=1)),
                ('chromosome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Chromosome')),
            ],
            options={
                'db_table': 'gene',
            },
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Group name that species belongs to', max_length=15)),
            ],
            options={
                'db_table': 'groups',
            },
        ),
        migrations.CreateModel(
            name='GroupSpecific',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chromosome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Chromosome')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Groups')),
            ],
            options={
                'db_table': 'group_specific',
                'ordering': ['id'],
            },
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
            options={
                'db_table': 'individual',
            },
        ),
        migrations.CreateModel(
            name='Mutation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('synonymous', models.PositiveSmallIntegerField(choices=[(1, 'Synonymous'), (2, 'Non-synonymous')], db_index=True, help_text='Mutation type')),
            ],
            options={
                'db_table': 'mutation',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Orthology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('human_ensembl', models.CharField(db_index=True, help_text='human ensembl gene id', max_length=18)),
                ('human_hgnc', models.CharField(help_text='human gene hgnc id', max_length=10)),
                ('human_name', models.CharField(help_text='human gene name', max_length=200)),
                ('human_symbol', models.CharField(help_text='human gene symbol', max_length=20)),
                ('support', models.CharField(help_text='orthology support database', max_length=255)),
                ('gene', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Gene')),
            ],
            options={
                'db_table': 'orthology',
            },
        ),
        migrations.CreateModel(
            name='Snp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(db_index=True, help_text='Position in chromosome sequence')),
                ('reference', models.CharField(help_text='Reference base', max_length=1)),
                ('alteration', models.CharField(help_text='SNP alteration base', max_length=1)),
                ('five', models.CharField(help_text='Five flanking sequence 50 bp', max_length=50)),
                ('three', models.CharField(help_text='Three flanking sequence 50 bp', max_length=50)),
                ('chromosome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Chromosome')),
            ],
            options={
                'db_table': 'snp',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taxonomy', models.IntegerField(help_text='NCBI taxonomy number')),
                ('scientific', models.CharField(help_text='Scientific name', max_length=50)),
                ('common', models.CharField(help_text='Common name', max_length=50)),
                ('code', models.CharField(help_text='New code', max_length=5)),
                ('group', models.ForeignKey(help_text='Species group information', on_delete=django.db.models.deletion.CASCADE, to='macaca.Groups')),
            ],
            options={
                'db_table': 'species',
            },
        ),
        migrations.CreateModel(
            name='SpeciesSpecific',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chromosome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Chromosome')),
                ('snp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Snp')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Species')),
            ],
            options={
                'db_table': 'species_specific',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.IntegerField(db_index=True)),
                ('genotype', models.IntegerField(db_index=True)),
                ('mutation', models.IntegerField(db_index=True)),
                ('counts', models.IntegerField()),
                ('chromosome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Chromosome')),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Individual')),
            ],
            options={
                'db_table': 'statistics',
            },
        ),
        migrations.CreateModel(
            name='Tannot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcript_pos', models.IntegerField(help_text='Relative position in transcript')),
                ('ref_codon', models.CharField(help_text='SNP site reference codon', max_length=3)),
                ('codon_pos', models.IntegerField(help_text='The SNP base position in codon')),
                ('alt_codon', models.CharField(help_text='Altered SNP site codon', max_length=3)),
                ('ref_aa', models.CharField(help_text='The reference amino acid for SNP codon', max_length=10)),
                ('alt_aa', models.CharField(help_text='The alteration amino acid for SNP codon', max_length=10)),
                ('protein_pos', models.IntegerField(help_text='Relative position of codon in protein')),
                ('synonymous', models.PositiveSmallIntegerField(choices=[(1, 'Synonymous'), (2, 'Non-synonymous')], db_index=True, help_text='Mutation type')),
                ('snp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Snp')),
            ],
            options={
                'db_table': 'tannot',
            },
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
                ('gene', models.ForeignKey(help_text='which gene for this transcript', on_delete=django.db.models.deletion.CASCADE, to='macaca.Gene')),
            ],
            options={
                'db_table': 'transcript',
            },
        ),
        migrations.AddField(
            model_name='tannot',
            name='transcript',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Transcript'),
        ),
        migrations.AddField(
            model_name='mutation',
            name='snp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Snp'),
        ),
        migrations.AddField(
            model_name='individual',
            name='species',
            field=models.ForeignKey(help_text='Species information', on_delete=django.db.models.deletion.CASCADE, to='macaca.Species'),
        ),
        migrations.AddField(
            model_name='groupspecific',
            name='snp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Snp'),
        ),
        migrations.AddField(
            model_name='gannot',
            name='gene',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Gene'),
        ),
        migrations.AddField(
            model_name='gannot',
            name='snp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Snp'),
        ),
        migrations.AddField(
            model_name='funcannot',
            name='function',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Function'),
        ),
        migrations.AddField(
            model_name='funcannot',
            name='gene',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Gene'),
        ),
        migrations.AddField(
            model_name='drug',
            name='orthology',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Orthology'),
        ),
        migrations.AddField(
            model_name='disease',
            name='orthology',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Orthology'),
        ),
        migrations.AlterIndexTogether(
            name='statistics',
            index_together={('feature', 'genotype', 'mutation')},
        ),
        migrations.AlterIndexTogether(
            name='speciesspecific',
            index_together={('snp', 'species'), ('snp', 'chromosome'), ('snp', 'species', 'chromosome')},
        ),
        migrations.AlterIndexTogether(
            name='snp',
            index_together={('position', 'chromosome')},
        ),
        migrations.AlterIndexTogether(
            name='orthology',
            index_together={('human_ensembl', 'gene')},
        ),
        migrations.AlterIndexTogether(
            name='mutation',
            index_together={('synonymous', 'snp')},
        ),
        migrations.AlterIndexTogether(
            name='groupspecific',
            index_together={('snp', 'chromosome'), ('snp', 'group', 'chromosome'), ('snp', 'group')},
        ),
        migrations.AlterIndexTogether(
            name='gannot',
            index_together={('feature', 'snp'), ('feature', 'gene'), ('feature', 'gene', 'snp')},
        ),
        migrations.AlterIndexTogether(
            name='funcannot',
            index_together={('function', 'gene')},
        ),
        migrations.AlterIndexTogether(
            name='drug',
            index_together={('drug_id', 'orthology')},
        ),
        migrations.AlterIndexTogether(
            name='disease',
            index_together={('pomim', 'orthology')},
        ),
    ]