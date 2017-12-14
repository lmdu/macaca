#!/usr/bin/env python
import re
import sys
import queue
import requests
import threading

ensmb_pattern = re.compile(r'^\s+Ensembl:\s(.*)', re.M)

task_queue = queue.Queue()
Lock = threading.Lock()

r = requests.get(u'http://rest.kegg.jp/list/mcc')
content = r.text.split('\n')

for line in content:
	if not line: break
	gene = line.split()[0]

	task_queue.put(gene)

def get_ensembl_id(gene):
	url = 'http://rest.kegg.jp/get/%s'
	while 1:
		try:
			r = requests.get(url % gene)
			if r.status_code == 200:
				break
		except:
			pass
		
	m = ensmb_pattern.search(r.text)

	if not m:
		return None

	return m.group(1)

class Worker(threading.Thread):
	def __init__(self, tasks, **kwargs):
		super(Worker, self).__init__(**kwargs)
		self.setDaemon(True)
		self.tasks = tasks
		self.start()

	def run(self):
		while 1:
			try:
				gene = self.tasks.get_nowait()
			except queue.Empty:
				break
			else:
				en_id = get_ensembl_id(gene)

				if en_id:
					Lock.acquire()
					print("%s\t%s" % (gene, en_id))
					Lock.release()

threads = []
for i in range(100):
	thread = Worker(task_queue)
	threads.append(thread)

for thread in threads:
	if thread.isAlive():
		thread.join()

