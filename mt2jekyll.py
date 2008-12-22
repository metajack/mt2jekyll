#!/usr/bin/env python

import os
import re
import sys

import mt

def convert(mtfile, postpath):
    entries = mt.parse_export(mtfile)
    
    # convert posts to jekyll format
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
	    f.write('tags: [%s]\n' % e['metadata']['tags'].replace(',', ', '))
	f.write('time: "%s"\n' % e['metadata']['date'].strftime('%H:%M'))
	if 'extended body' in e:
	    f.write('extended: ":EXTENDED:"\n')
	f.write('---\n\n')

	f.write(e['body']['data'])

	if 'extended body' in e:
	    f.write('\n:EXTENDED:\n\n')
	    f.write(e['extended body']['data'])

	f.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
	print "usage: %s <export file> <posts path>"
	sys.exit(1)

    convert(sys.argv[1], sys.argv[2])
