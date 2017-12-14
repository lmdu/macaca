#!/usr/bin/env python
import re
import requests

class_pattern = re.compile(r'^CLASS\s+(.*)', re.M)
url = 'http://rest.kegg.jp/get/%s'
r = requests.get(u'http://rest.kegg.jp/list/pathway/mcc')
content = r.text.split('\n')
for line in content:
	if not line: break
	path, info = line.strip().split('\t')
	name = info.split(' - ')[0].strip()

	while 1:
		r = requests.get(url % path)
		if r.status_code == 200:
			break

	m = class_pattern.search(r.text)

	if m:
		print("%s\t%s\t%s" % (path, name, m.group(1)))
	else:
		print("%s\t%s\t%s" % (path, name, ''))

	