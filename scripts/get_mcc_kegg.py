#!/usr/bin/env python
import re
import sys
import requests

class_pattern = re.compile(r'^CLASS\s+(.*)', re.M)
ensmb_pattern = re.compile(r'^\s+Ensembl:\s(.*)', re.M)

pathways = {}
url = 'http://rest.kegg.jp/get/%s'
r = requests.get(u'http://rest.kegg.jp/list/pathway/mcc')
content = r.text.split('\n')
for line in content:
	if not line: break
	path, info = line.strip().split('\t')
	r = requests.get(url % path)
	m = class_pattern.search(r.text)
	if m:
		pathways[path] = (info.split('-')[0].strip(), m.group(1))
	else:
		pathways[path] = (info.split('-')[0].strip(), '')

genes = {}
relationships = {}

r = requests.get(u'http://rest.kegg.jp/list/mcc')
content = r.text.split('\n')
count = 0
for line in content:
	if not line: break

	gene = line.strip().split()[0]

	while 1:
		r = requests.get(url % gene)
		if r.status_code == 200:
			break
		
	m = ensmb_pattern.search(r.text)
	
	if not m: continue

	ensembl_id = m.group(1)

	if ensembl_id not in genes:
		genes[ensembl_id] = set()
	genes[ensembl_id].add(gene)

	while 1:
		r = requests.get('http://rest.kegg.jp/link/pathway/%s' % gene)
		if r.status_code == 200:
			break

	if gene not in relationships:
		relationships[gene] = set()

	for row in r.text.split('\n'):
		if not row: break
		relationships[gene].add(row.strip().split()[1])

	count += 1

	sys.stderr.write("%s out of %s\n" % (count, len(content)))
	sys.stderr.flush()


for gene in genes:
	for ko in genes[gene]:
		pathes = set()
		for path in relationships[ko]:
			pathes.add(path)

	if path in pathes:
		print("%s\t%s\t%s\t%s" % (gene, path, pathways[path][0], pathways[path][1]))

