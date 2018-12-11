#!/usr/bin/python

import sys
import json
import rdflib
import pprint
from operator import itemgetter
from reprosearch.PropMapper import PropMapper
from reprosearch.util import update_meta_data_structure

blacklist_props = [
    'http://www.w3.org/ns/prov#wasGeneratedBy',
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
    'FILE_ID'
]

blacklist_vals = [
    'nan'
]

# def print_sparql(query):
#     g = rdflib.Graph()
#     g.parse("local5.nidm.ttl", format='ttl')
#     qres = g.query( query )
#     for row in qres:
#       print (row)


#
# Pull all the values out of the assessment and put them in a list of prop/value pairs
#
def accumulate_values(nidm_file):
    querries = [
        "SELECT DISTINCT ?property ?o WHERE { ?s a  nidm:assessment-instrument  . ?s ?property ?o  }",
        "SELECT DISTINCT ?property ?o WHERE { ?s a  sio:file  . ?s ?property ?o  }"
    ]
    data = []

    mapper = PropMapper(nidm_file)

    for query in querries:
        qres = g.query( query )
        for row in qres:
            pair = []
            prop = mapper.map(str(row[0]))
            val = str(row[1])
            # if (not prop) or (prop in blacklist_props):
            #     print ("didn't find " + str(row[0]) + "\n  val " + str(row[1]) )

            if prop:
                if prop not in blacklist_props and val not in blacklist_vals:
                    pair.append(prop)
                    pair.append(val)
                    data.append(pair)


    # pprint.pprint ( sorted(data, key=itemgetter(0)) )
    return sorted(data, key=itemgetter(0))

#
# Reads in a list of key/value pairs and calculates min/max for each pair
# or if a key has non-numeric values, builds a set of acceptable values
#
def build_ranges (pairs):
    result = {}
    for pair in pairs:
        key = pair[0]
        val = pair[1]
        update_meta_data_structure(result, key, val)
    return result





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

    metadata = []

    result = ""
    hit_count = 0

    all_values = accumulate_values(nidm_file)
    metadata = build_ranges(all_values)

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
