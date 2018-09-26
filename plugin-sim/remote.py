#!/usr/bin/python

import sys
import json

instr = sys.stdin.read()
f = open ("/mnt/data/remote-log.txt", "a")
f.write (instr)
f.write ("\n")



doc = json.loads(instr)
hits = 0
for site, output in doc['input'].items():
    f.write("\n")
    f.write(site)
    f.write(json.dumps(output['hit-count']))
    hits += output['hit-count'];

output = { "output": { "hit-count": hits }, "success": True }
sys.stdout.write(json.dumps(output))

f.close()
