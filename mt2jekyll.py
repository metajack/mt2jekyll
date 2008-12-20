#!/usr/bin/env python

import mt
import sys

if __name__ == '__main__':
    print len(mt.parse_export(sys.argv[1]))
