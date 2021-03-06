import os
import simplejson as json
import urllib, urllib2


class Disqus:
    def __init__(self, user_key=None):
        if not user_key:
            self.user_key = os.environ.get('DISQUS_API_KEY', None)
        else:
            self.user_key = user_key
        if not self.user_key:
            raise Exception('No Disqus user key provided.')

        self.forums = self._get_forums()

    def _get_forums(self):
	forums = {}
	flist = self._get('get_forum_list',
			  {'user_api_key': self.user_key})
	for f in flist:
	    fkey = self._get('get_forum_api_key',
			     {'user_api_key': self.user_key,
			      'forum_id': f['id']})
	    f['key'] = fkey
	    forums[f['name']] = f
	    
	return forums

    def _prepare_args(self, data):
	args = []
	for k, v in data.iteritems():
	    args.append('%s=%s' % (k, urllib.quote_plus(v)))
	return '&'.join(args)

    def _call(self, func, data, post=False):
	if post:
	    url = 'http://disqus.com/api/%s/' % func
	    u = urllib2.urlopen(url, urllib.urlencode(data))
	else:
	    url = 'http://disqus.com/api/%s/?%s' % (func, self._prepare_args(data))
	    u = urllib2.urlopen(url)

	page = u.read()
	result = json.loads(page)
	if not result['succeeded']:
	    raise Exception("Disqus API call failed: %s" % str(result))
	return result['message']

    def _get(self, func, data):
	return self._call(func, data)
	
    def _post(self, func, data):
	return self._call(func, data, post=True)

    def get_thread_by_url(self, forum, url):
	return self._get('get_thread_by_url',
			 {'forum_api_key': self.forums[forum]['key'],
			  'url': url})

    def thread_by_identifier(self, forum, ident, title):
	return self._post('thread_by_identifier',
			  {'forum_api_key': self.forums[forum]['key'],
			   'identifier': ident,
			   'title': title})['thread']

    def update_thread(self, forum, thread, title=None, slug=None, url=None):
	data = {'forum_api_key': self.forums[forum]['key'],
		'thread_id': thread}
	if title: data['title'] = title
	if slug: data['slug'] = slug
	if url: data['url'] = url
	self._post('update_thread', data)

    def create_post(self, forum, thread, message, name, email, 
		    url=None, ip=None, created=None):
	data = {'forum_api_key': self.forums[forum]['key'],
		'thread_id': thread,
		'message': message,
		'author_name': name,
		'author_email': email}
	if url: data['author_url'] = url
	if ip: data['ip_address'] = ip
	if created: data['created_at'] = created.strftime('%Y-%m-%dT%H:%M')
	return self._post('create_post', data)
