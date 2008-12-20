#!/usr/bin/env python

import os
import re
import sys

import mt


def convert(mtfile, postpath):
    entries = mt.parse_export(mtfile)
    
    for e in entries:
	if e['metadata']['status'] == 'Draft':
	    continue

	postname = '%s-%s' % (e['metadata']['date'].strftime("%Y-%m-%d"),
			      e['metadata']['basename'])
	postname += '.markdown'
	
	f = open(os.path.join(postpath, postname), 'w')

	f.write('---\n')
	f.write('layout: post\n')
	if re.search('[-:"]', e['metadata']['title']):
	    f.write('title: "%s"\n' % \
			e['metadata']['title'].replace('"', '\\"'))
	else:
	    f.write('title: %s\n' % e['metadata']['title'])
	if 'tags' in e['metadata']:
	    f.write('tags: %s\n' % e['metadata']['tags'])
	f.write('---\n\n')

	f.write(e['body']['data'])
	f.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
	print "usage: %s <export file> <posts path>"
	sys.exit(1)

    convert(sys.argv[1], sys.argv[2])
