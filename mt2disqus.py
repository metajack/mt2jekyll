#!/usr/bin/env python

import sys

import mt
from disqus import Disqus

		    
def make_url(base, entry):
    url = '%s/%s/%s/' % \
	(base, 
	 entry['metadata']['date'].strftime('%Y/%m/%d'),
	 entry['metadata']['basename'])
    return url
	
    
def convert(mtfile, urlbase, forum):
    entries = mt.parse_export(mtfile)
    
    disqus = Disqus()
    for e in entries:
        if 'comment' in e:
	    for c in e['comment']:
		url = make_url(urlbase, e)
		title = e['metadata']['title']
                
		thread = disqus.get_thread_by_url(forum, url)
		if not thread:
		    thread = disqus.thread_by_identifier(forum, title, title)
		disqus.update_thread(forum, thread['id'], 
				     title=title,
				     slug=e['metadata']['basename'],
				     url=url)
		
		disqus.create_post(forum, thread['id'], c['data'],
				   c['author'], c.get('email', 'anonymous'),
				   c.get('url'), c['ip'], c['date'])


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "usage: %s <export file> <url base> <disqus forum short name>"
        sys.exit(1)

    convert(sys.argv[1], sys.argv[2], sys.argv[3])
