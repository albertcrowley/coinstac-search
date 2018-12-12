#!/usr/bin/python

import sys
import json
import pprint
import os

def merge_metadata(m1, m2):
    for key in m2:
        f.write ("trying key {} \n".format(key))
        val = m2[key]
        if key not in m1:
            m1[key] = val
        else:
            m1[key]['numeric'] =  m1[key]['numeric'] or m2[key]['numeric']
            m1[key]['min'] = min(m1[key]['min'], m2[key]['min'])
            m1[key]['max'] = max(m1[key]['max'], m2[key]['max'])
            m1[key]['enumeration'] = m1[key]['enumeration'] + m2[key]['enumeration']
            if m1[key]['has_nan']=="Yes" or m2[key]['has_nan'] == "Yes":
                m1[key]['has_nan'] = "Yes"
            else:
                m1[key]['has_nan'] = "NA"
    return m1

instr = sys.stdin.read()

if 'DEBUG' in os.environ and os.environ['DEBUG'] == "1":
    f=sys.stdout
else:
    f = open ("/mnt/data/remote-log.txt", "a")


f.write (instr)
f.write ("\n")
f.write ("-- begin computation -- \n\n")



doc = json.loads(instr)
hits = ""
metadata = {}
operation = ""
for site, output in doc['input'].items():
    f.write("\n")
    f.write(site)
    f.write(json.dumps(output['hits']))
    hits = hits + output['hits'];
    operation = output['operation']
    if operation == 'metadata':
        f.write("\n\n --- output['metadata'] ---\n")
        f.write (output['metadata'])
        jmeta = (output['metadata']).replace('\"', '"')
        f.write("\n\n --- jmeta ---\n")
        f.write(jmeta)
        f.write ("\n\ntype: ")
        # f.write(type(json.loads(jmeta)))
        f.write ("\n\n pretty printed: ")
        pprint.pprint(json.loads(jmeta), stream=f)
        merge_metadata(metadata, json.loads(jmeta))

jmeta = json.dumps(metadata)
jmeta.replace('"', "\"")

output = { "output": { "hits": hits, "metadata" : str(jmeta), "operation" : operation }, "success": True }
# pprint.pprint(json.dumps(output))
sys.stdout.write(json.dumps(output))

f.close()

#finished
