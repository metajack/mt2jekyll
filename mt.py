"""Small library for parsing MovableType export files.
"""

import re
from datetime import datetime

METADATA_FIELDS = (
    'author',
    'title',
    'date',
    'primary category',
    'category',
    'status',
    'allow comments',
    'allow pings',
    'convert breaks',
    'no entry',
    'basename',
    'tags',
)
 
MULTILINE_FIELDS = {
    'body': tuple(),
    'extended body': tuple(),
    'excerpt': tuple(),
    'keywords': tuple(),
    'comment': ('author', 'email', 'url', 'ip', 'date'),
    'ping': ('title', 'url', 'ip', 'blog name', 'date'),
}

ENTRY_SEP = '--------\n'
MULTILINE_SEP = '-----\n'

KEYLINE_RE = re.compile('^[A-Z ]+:')

def parse_date(s):
    return datetime.strptime(s, '%m/%d/%Y %I:%M:%S %p') 

def make_metadata_block(lines):
    metadata = {}
    for l in lines:
	key, val = l.strip().split(':', 1)
	if key.lower() not in METADATA_FIELDS:
	    raise Exception('Got bad key (%s) in metadata block.' % key)
	if key.lower() == 'date':
	    metadata[key.lower()] = parse_date(val.lstrip())
	elif key.lower() == 'tags':
	    metadata[key.lower()] = val.lstrip().replace('"', '')
	else:
	    metadata[key.lower()] = val.lstrip()
    return 'metadata', metadata

def make_normal_block(lines):
    block = {}
    keys = True
    first = True
    btype = ''
    body = []
    for l in lines:
	if keys and KEYLINE_RE.match(l):
	    key, val = l.strip().split(':', 1)
	    if first:
		first = False
		if key.lower() not in MULTILINE_FIELDS.keys():
		    raise Exception('Got unknown block type (%s).' % key)
		btype = key.lower()
		continue
	    if key.lower() not in MULTILINE_FIELDS[btype]:
		raise Exception('Got unknown key (%s) for %s block.' % \
				    (key, btype))
	    if key.lower() == 'date':
		block[key.lower()] = parse_date(val.lstrip())
	    else:
		block[key.lower()] = val.lstrip()
	    continue
	elif first:
	    continue
	else:
	    keys = False
	    body.append(l)

    block['data'] = ''.join(body)
    return btype, block

def make_block(lines, first=False):
    if first:
	return make_metadata_block(lines)
    else:
	return make_normal_block(lines)

def parse_entry(lines):
    first = True
    entry = {}
    block_lines = []
    for l in lines:
	if l == MULTILINE_SEP:
	    btype, block = make_block(block_lines, first=first)
	    first = False
	    if btype == 'comment':
		if btype in entry:
		    entry[btype].append(block)
		else:
		    entry[btype] = [block]
	    else:
		entry[btype] = block
	    block_lines = []
	    continue
	block_lines.append(l)
    return entry

def parse_export(fname):
    f = open(fname)

    entries = []
    lines = []
    for l in f.xreadlines():
	if l == ENTRY_SEP:
	    entries.append(parse_entry(lines))
	    lines = []
	    continue
	lines.append(l)

    return entries
