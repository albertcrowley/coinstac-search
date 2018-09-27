import rdflib
from argparse import ArgumentParser

parser = ArgumentParser()
# parse command line arguments
parser.add_argument('-nidm', dest='nidm_file', required=True, help="NIDM-Exp RDF File to import")
args = parser.parse_args()


g=rdflib.Graph()
g.parse(args.nidm_file, format='ttl')


qres = g.query(
    """SELECT DISTINCT ?id ?age ?assessment   
       WHERE {
          ?assessment prov:wasGeneratedBy ?acq .
          ?acq prov:wasAssociatedWith ?person .
          ?assessment ncicb:Age ?age .
          ?person ndar:src_subject_id ?id
       }""")


for row in qres:
    print("%s - %s - %s" % row)
