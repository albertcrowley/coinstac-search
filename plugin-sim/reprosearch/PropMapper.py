import rdflib
import re
import json

class PropMapper:

    USE_WHITELIST = True
    WHITELIST_FILE_NAME = "term_whitelist.json"

    def __init__(self, nidm_file):
        self.nidm_file = nidm_file
        self.g = rdflib.Graph()
        self.g.parse(nidm_file, format='ttl')

        if PropMapper.USE_WHITELIST:
            with open(PropMapper.WHITELIST_FILE_NAME, 'r') as f:
                self.mapping = json.load(f)


        self.load_metadata()


    #
    # Create a mapping of URIs to short names
    #
    def load_metadata (self):
        self.metadata_dict = {}

        # pull in the whole ttl file so we can search for aliases
        with open(self.nidm_file, 'r') as content_file:
            content = content_file.read()

        for object in ['nidm:assessment-instrument', 'sio:file']:
            query = 'SELECT DISTINCT ?property WHERE {{ ?s a {obj} . ?s ?property ?o }}'.format(obj=object)
            qres = self.g.query( query )
            for row in qres:
                prefix_pattern = re.compile("prefix ([^:]*):.<" + re.escape(row[0]) + ">") #make a regex that will match any alias for the URI
                groups = prefix_pattern.findall(content)
                if len(groups) > 0:
                    short_name = groups[0]
                    self.metadata_dict[str(row[0])] = str(short_name)



    def map(self, uri: str) -> str:
        """
        Map a RDF graph URI to a short human readable name

        :param uri:  long URI returned by RDF query
        :return: short name for the URI str
        """

        if PropMapper.USE_WHITELIST:
            terms = self.mapping['terms']
            if uri in self.mapping['terms']:
                return self.mapping['terms'][uri]['description']

            return None

        else:

            if uri in self.metadata_dict:
                return self.metadata_dict[uri]

            for prefix in ['http://purl.org/nidash/nidm#', "http://neurolex.org/wiki/Category:DICOM_term/"]:
                if uri.startswith(prefix):
                    short_term = uri[len(prefix):]
                    return short_term


        return None

