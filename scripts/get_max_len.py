#!/usr/bin/env python
import sys

infile, column = sys.argv[1:]

column = int(column)

l = 0
with open(infile) as fh:
	for line in fh:
		cols = line.split('\t')
		if len(cols[column]) > l:
			l = len(cols[column])

print l

