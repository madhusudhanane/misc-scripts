#!/usr/bin/env python
"""
Script to dump all URLs and their status codes from a JSON
HTTP Archive (HAR - http://www.softwareishard.com/blog/firebug/http-archive-specification/)
file, such as those generated by the Firebug NetExport extension (http://getfirebug.com/wiki/index.php/Firebug_Extensions#NetExport)

Copyright 2014 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
Free for any use provided that patches are submitted back to me.

The latest version of this script can be found at:
https://github.com/jantman/misc-scripts/blob/master/har_urls.py

CHANGELOG:

2014-09-23 jantman:
- initial script
"""

import sys
import optparse
import logging
import os
import json

FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.ERROR, format=FORMAT)
logger = logging.getLogger(__name__)


def main(harfile):
    """ read the file, list URLs """
    if not os.path.exists(harfile):
        raise SystemExit("ERROR: file {h} does not exist.".format(h=harfile))
    with open(harfile, 'r') as fh:
        raw = fh.read()
    j = json.loads(raw)
    s = get_url_statuses(j)
    for i in sorted(s):
        print("{status}\t{req}".format(req=i, status=s[i]))

def get_url_statuses(j):
    """ return dict of URLs to their statuses """
    entries = {}
    for req in j['log']['entries']:
        k = '{m} {u}'.format(m=req['request']['method'], u=req['request']['url'])
        entries[k] = req['response']['status']
    return entries

def parse_args(argv):
    """ parse arguments/options """
    p = optparse.OptionParser(usage="har_urls.py <file>")

    options, args = p.parse_args(argv)

    return (options, args)


if __name__ == "__main__":
    opts, args = parse_args(sys.argv[1:])

    if len(args) < 1:
        raise SystemExit("USAGE: har_urls.py <file>")

    main(args[0])
