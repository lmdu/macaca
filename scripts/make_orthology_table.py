import os

work_dir = '/home/ming/macaca/snvs'
data_dir = os.path.join(work_dir, 'data')
table_dir = os.path.join(work_dir, 'tables')

orth_table = open(os.path.join(table_dir, 'orthology.table'), 'w')

idmapping = {}
with open(os.path.join(table_dir, 'gene.table')) as fh:
	for line in fh:
		cols = line.strip().split()
		idmapping[cols[1]] = cols[0]

human_gene = {}
mac_gene = {}
with open(os.path.join(data_dir, 'human_macaque_orthology.tsv')) as fh:
	fh.readline()
	for line in fh:
		cols = line.strip().split('\t')
		if cols[4] == '-':
			continue

		human_gene[cols[0]] = human_gene.get(cols[0], 0) + 1
		mac_gene[cols[4]] = mac_gene.get(cols[4], 0) + 1

count = 0
with open(os.path.join(data_dir, 'human_macaque_orthology.tsv')) as fh:
	fh.readline()
	for line in fh:
		cols = line.strip().split('\t')
		if cols[4] == '-':
			continue

		if human_gene[cols[0]] == 1 and mac_gene[cols[4]] == 1:
			if cols[4] not in idmapping:
				continue
			
			count += 1
			orth_table.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (count, cols[0], cols[1], cols[2], cols[3], cols[5], idmapping[cols[4]]))

orth_table.close()
