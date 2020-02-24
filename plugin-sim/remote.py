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

if len(sys.argv) > 1:
    infile = open(sys.argv[1])
    instr = infile.read()
    infile.close()
else:
    instr = sys.stdin.read()

log (instr)

result = []
operation = ""
doc = json.loads(instr)

sub_counts = []
avg_vals = []
i = 0

for site, site_output in doc['input'].items():
    log("\n" + site + "\n ***** \n")
    log (json.dumps(site_output['result']))

    if 'DEBUG' in os.environ and os.environ['DEBUG'] == "1":
        parsed = json.loads(site_output['result'])
    else:
        parsed = site_output['result']

    operation = site_output['operation']
    if 'subjects' in parsed:
        sub_counts.append(len(parsed['subjects']))
        avg_vals.append(parsed['fs_000003']['mean'])
    else:
        sub_counts.append(0)
        avg_vals.append(0)

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

total_mean = 0
total_subs = 0
for i in range(len(sub_counts)):
    total_subs += sub_counts[i] or 0
    total_mean += (sub_counts[i] or 0)  *  (avg_vals[i] or 0)

if total_subs == 0:
    total_mean = "NaN"
else:
    total_mean = total_mean / total_subs

output = {"output": {"result" : json.dumps(total_mean), "operation" : operation }, "success": True}


sys.stdout.write(json.dumps(output))

