#!/usr/bin/python

import sys
import json

in_str = sys.stdin.read()

f = open("/mnt/data/local-log.txt", "a")
f.write("\n")
f.write("\n")
f.write(in_str)
f.write("\n")



doc = json.loads(in_str)

search_string = doc['input']['search-string']

#if 'start' in doc['input']:
#    sums = 1
#else:
#    sums = doc['input']['sum'] + 1

output = { "output": { "hit-count": len(search_string), "search-string" : search_string } }

f.write("\n")
f.write(json.dumps(output))
f.write("\n")



sys.stdout.write(json.dumps(output))
