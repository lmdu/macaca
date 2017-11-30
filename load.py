#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macaca.settings")
import django
if django.VERSION >= (1, 7):
	django.setup()

def main():
	from blog.models import Blog
	f = open('oldblog.txt')
	BlogList = []
	for line in f:
		title,content = line.split('****')
		blog = Blog(title=title,content=content)
		BlogList.append(blog)
	f.close()

	Blog.objects.bulk_create(BlogList)

if __name__ == '__main__':
	main()
	
