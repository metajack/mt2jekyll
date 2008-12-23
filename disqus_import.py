#!/usr/bin/env python

import simplejson as json
import sys
from datetime import datetime

from disqus import Disqus

		    
def post(comfile, urlbase, forum):
    disqus = Disqus()
    comments = json.loads(open(comfile).read())

    for comment in comments:
	url = '%s/%s/%s/' % \
	    (urlbase, comment['post']['date'], comment['post']['slug'])
	title = comment['post']['title']
        date = datetime.strptime(comment["date"],
				 "%Y-%m-%dT%H:%M:%S")
        
	thread = disqus.get_thread_by_url(forum, url)
	if not thread:
	    thread = disqus.thread_by_identifier(forum, title, title)
	disqus.update_thread(forum, thread['id'], 
			     title=title,
			     slug=comment['post']['slug'],
			     url=url)
		
	disqus.create_post(forum, thread['id'], comment['body'],
			   comment['author'], comment['email'],
			   comment.get('url'), comment['ip'], date)
	

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "usage: %s <comments json> <url base> <disqus forum short name>"
        sys.exit(1)

    post(sys.argv[1], sys.argv[2], sys.argv[3])
