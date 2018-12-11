#!/usr/bin/python

import sys
import json

instr = sys.stdin.read()
f = open ("/mnt/data/remote-log.txt", "a")
f.write (instr)
f.write ("\n")



doc = json.loads(instr)
hits = ""
metadata = []
operation = ""
for site, output in doc['input'].items():
    f.write("\n")
    f.write(site)
    f.write(json.dumps(output['hits']))
    hits = hits + output['hits'];
    operation = output['operation']
    if operation == 'metadata':
        metadata += output['metadata']

# de-duplicate
metadata = list(set(metadata))


output = { "output": { "hits": hits, "metadata" : metadata, "operation" : operation }, "success": True }
sys.stdout.write(json.dumps(output))

f.close()

#finished
