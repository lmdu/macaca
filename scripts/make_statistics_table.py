import os
import sys

os.chdir('/var/website/bioinfo')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bioinfo.settings")
import django
if django.VERSION >= (1, 7):
	django.setup()

from macaca.models import Variants

fw = open('/home/ming/macaca/snvs/tables/statistics.table', 'w')

n = 0
for i in range(1, 21):
	for j in range(1, 21):
		filters = {'individual': j}

		for f in range(6):
			for g in range(3):
				for m in range(3):
					if f:
						filters['snp__gannot__feature'] = f
					else:
						if 'snp__gannot__feature' in filters:
							 del filters['snp__gannot__feature']

					if g:
						filters['genotype'] = g
					else:
						if 'genotype' in filters:
							del filters['genotype']

					if m:
						filters['snp__mutation__synonymous'] = m
					else:
						if 'snp__mutation__synonymous' in filters:
							del filters['snp__mutation__synonymous']

					
					c = Variants.shard(i).objects.filter(**filters).count()

					n += 1
					fw.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (n, f, g, m, c, i, j))

fw.close()
