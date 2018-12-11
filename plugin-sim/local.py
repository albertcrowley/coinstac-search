#!/usr/bin/python

import sys
import json
import rdflib
import re
from argparse import ArgumentParser



def get_metadata (query, nidm_file, debug = False):
    metadata = []

    # pull in the whole ttl file so we can search for aliases
    with open(nidm_file, 'r') as content_file:
        content = content_file.read()

    qres = g.query( query )
    for row in qres:
        if (debug):
            print (row)
        short_name = row[0] # default to the full URI if we don't find a match
        prefix_pattern = re.compile("prefix ([^:]*):.<" + re.escape(row[0]) + ">") #make a regex that will match any alias for the URI
        groups = prefix_pattern.findall(content)
        if len(groups) > 0:
            short_name = groups[0]

        metadata.append(short_name)
    return metadata


in_str = sys.stdin.read()

f = open("/mnt/data/local-log.txt", "a")
f.write("\n")
f.write("\n")
f.write(in_str)
f.write("\n")



doc = json.loads(in_str)

search_string = doc['input']['search-string']
operation = doc['input']['operation']
my_client_id = doc['state']['clientId']

#if 'start' in doc['input']:
#    sums = 1
#else:
#    sums = doc['input']['sum'] + 1


nidm_file = my_client_id + '.nidm.ttl'
g=rdflib.Graph()
g.parse(nidm_file, format='ttl')




if operation == "search":
    qres = g.query( search_string)

    result = ""
    hit_count = 0
    for row in qres:
    #    result += ("%s - %s - %s" % row)
        hit_count = hit_count + 1
        print (row)

    result = "client %s has %s hits  -- " %  (my_client_id, hit_count)

    output = { "output": { "hits": result,
                           "search-string" : search_string,
                           "metadata" : "",
                           "operation" : "search"
                          }
             }

if operation == "metadata":
    q1 = "SELECT DISTINCT ?property WHERE { ?s a  nidm:assessment-instrument  . ?s ?property ?o  } "
    q2 = "SELECT DISTINCT ?property WHERE { ?s a  sio:file  . ?s ?property ?o  } "


    metadata = []
    result = ""
    hit_count = 0

    metadata += get_metadata(q1, nidm_file)
    metadata += get_metadata(q2, nidm_file)

    hit_count = len(metadata)


    result = "client %s has %s categoris of metadata -- " %  (my_client_id, hit_count)

    output = { "output": { "hits": result,
                           "search-string" : "",
                           "metadata" :  metadata, # ', '.join( str(m) for m in metadata)
                           "operation" : "metadata"
                          }
             }

f.write("\n")
f.write(json.dumps(output))
f.write("\n")


sys.stdout.write(json.dumps(output))
