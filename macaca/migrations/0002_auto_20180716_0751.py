# Generated by Django 2.0.3 on 2018-07-16 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('macaca', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nonvariant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Individual')),
            ],
            options={
                'db_table': 'nonvariant',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genotype', models.PositiveSmallIntegerField(choices=[(1, 'Homozygote'), (2, 'Heterozygote')], db_index=True, help_text='Alteration genotype')),
                ('chromosome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Chromosome')),
                ('individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Individual')),
            ],
            options={
                'db_table': 'variant',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Snps',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('macaca.snp',),
        ),
        migrations.RemoveField(
            model_name='species',
            name='code',
        ),
        migrations.AlterField(
            model_name='gannot',
            name='snp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Snps'),
        ),
        migrations.AlterField(
            model_name='groupspecific',
            name='snp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Snps'),
        ),
        migrations.AlterField(
            model_name='mutation',
            name='snp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Snps'),
        ),
        migrations.AlterField(
            model_name='speciesspecific',
            name='snp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Snps'),
        ),
        migrations.AlterField(
            model_name='tannot',
            name='snp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Snps'),
        ),
        migrations.AddField(
            model_name='variant',
            name='snp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Snps'),
        ),
        migrations.AddField(
            model_name='nonvariant',
            name='snp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='macaca.Snps'),
        ),
        migrations.CreateModel(
            name='Nonvariants',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('macaca.nonvariant',),
        ),
        migrations.CreateModel(
            name='Variants',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('macaca.variant',),
        ),
        migrations.AlterIndexTogether(
            name='variant',
            index_together={('genotype', 'individual', 'snp'), ('genotype', 'individual'), ('genotype', 'snp'), ('individual', 'snp')},
        ),
        migrations.AlterIndexTogether(
            name='nonvariant',
            index_together={('individual', 'snp')},
        ),
    ]