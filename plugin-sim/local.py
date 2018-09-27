#!/usr/bin/python

import sys
import json
import rdflib
from argparse import ArgumentParser



in_str = sys.stdin.read()

f = open("/mnt/data/local-log.txt", "a")
f.write("\n")
f.write("\n")
f.write(in_str)
f.write("\n")



doc = json.loads(in_str)

search_string = doc['input']['search-string']
my_client_id = doc['state']['clientId']

#if 'start' in doc['input']:
#    sums = 1
#else:
#    sums = doc['input']['sum'] + 1


nidm_file = my_client_id + '.nidm.ttl'
g=rdflib.Graph()
g.parse(nidm_file, format='ttl')


qres = g.query( search_string)

result = ""
hit_count = 0
for row in qres:
#    result += ("%s - %s - %s" % row)
    hit_count = hit_count + 1

result = "client %s has %s hits  -- " %  (my_client_id, hit_count)

output = { "output": { "hits": result, "search-string" : search_string } }

f.write("\n")
f.write(json.dumps(output))
f.write("\n")


sys.stdout.write(json.dumps(output))
