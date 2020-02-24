#!/usr/bin/python
import subprocess
import sys
import json
import os

from nidm.experiment.tools.rest import RestParser


if 'DEBUG' in os.environ and os.environ['DEBUG'] == "1":
    directory = '/opt/project/'
else:
    directory = './'



#
# To run as a test:
#
#  docker run -e "DEBUG=1" -v /home/crowley/coinstac-search/plugin-sim:/opt/project -w /opt/project -v /tmp:/mnt/data/local.py pynidm  python local.py /opt/project/test_input.json


def log(s):
    if 'DEBUG' in os.environ and os.environ['DEBUG'] == "1":
        print(s)
    else:
        f = open("/mnt/data/local-log.txt", "a")
        f.write(s)
        f.write("\n")
        f.close()

if len(sys.argv) > 1:
    infile = open(sys.argv[1])
    in_str = infile.read()
    infile.close()
else:
    in_str = sys.stdin.read()

log ("\n\n\n------------------------------------------------------------------------\n")

doc = json.loads(in_str)

filter = doc['input']['operation']
my_client_id = doc['state']['clientId']
log ("\nMy client ID is " + my_client_id); # ex local0
log("\nInput:\n" + in_str)

ttl_file = directory + my_client_id + '.nidm.ttl'
log('TTL File={}'.format(ttl_file))

uri = '/projects/'
restParser = RestParser(output_format=RestParser.OBJECT_FORMAT)
out = restParser.run( [ttl_file], uri )
log (json.dumps(out))

for project in out:
    uri = '/statistics/projects/{}?{}'.format(project, filter)
    log("\n&&& URI: {}\n".format(uri))
    out = restParser.run( [ttl_file], uri)
    output = {"output": {"result": out, "operation": uri}}

log(json.dumps(output, indent=2))

sys.stdout.write(json.dumps(output))


exit (0)
cmd = ['pynidm', 'query', '-nl', ttl_file, '-u', uri, '-j']
log(str(cmd))
try:
    # we don't want the whole pipeline to break if this returns a non-zero exit code.
    result = subprocess.check_output(cmd)
    result = result.decode("utf-8")
except:
    result = ""

output = {"output": {"result": result, "operation" : uri } }

log(json.dumps(output))

sys.stdout.write(json.dumps(output))

