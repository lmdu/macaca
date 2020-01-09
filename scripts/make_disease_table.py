import os

work_dir = '/home/ming/macaca/snvs'
data_dir = os.path.join(work_dir, 'data')
table_dir = os.path.join(work_dir, 'tables')

outfh = open(os.path.join(table_dir, 'disease.table'), 'w')

idmapping = {}
with open(os.path.join(table_dir, 'orthology.table')) as fh:
	for line in fh:
		cols = line.strip().split('\t')
		idmapping[cols[1]] = cols[0]

count = 0
with open(os.path.join(data_dir, 'human_2_omim.tsv')) as fh:
	for line in fh:
		cols = line.strip('\n').split('\t')

		if cols[0] not in idmapping:
			continue

		count += 1

		outfh.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (count, cols[1], cols[2], cols[3], cols[4], cols[5], idmapping[cols[0]]))

outfh.close()
