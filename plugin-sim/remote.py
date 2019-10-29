#!/usr/bin/python

import sys
import json
import pprint
import os

def log(s):
    if 'DEBUG' in os.environ and os.environ['DEBUG'] == "1":
        print(s)
    else:
        f = open("/mnt/data/remote-log.txt", "a")
        f.write(s)
        f.close()


def do_not_save_computation(result):
    if isinstance(result,dict):
        # check for an empty subject record
        if 'uuid' in result and result['uuid'] == "" and \
            'id' in result and result['id'] == "" and \
            'activity' in result and isinstance(result['activity'], list) and len(result['activity']) == 0 and \
            'instruments' in result and isinstance(result['instruments'], dict) and len(result['instruments']) == 0:
                return True

    return False

log("-- begin computation -- \n\n")
instr = sys.stdin.read()
log (instr)

result = []
operation = ""
doc = json.loads(instr)

for site, site_output in doc['input'].items():
    log(site + "\n")
    log (site_output['result'])
    parsed = json.loads(site_output['result'])
    operation = site_output['operation']

    if do_not_save_computation(parsed):
        log ("skipping result from " + str(site))
        continue

    if isinstance(parsed,list):
        for x in parsed:
            result.append(x)
    elif isinstance(parsed,dict):
        result.append(parsed)
        log (json.dumps(result))
    else:
        log ("received unexpected type from local computation")
        result.append({'error': 'unexpected type from local computation'})

    log(str(result))

output = {"output": {"result" : json.dumps(result), "operation" : operation }, "success": True}


sys.stdout.write(json.dumps(output))

