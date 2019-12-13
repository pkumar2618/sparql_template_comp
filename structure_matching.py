import pickle
from rdflib.compare import isomorphic, similar
import re
import pandas as pd
from query_graph import *
import rdflib
from rdflib import BNode, URIRef
from rdflib.namespace import XSD
from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.sparql.algebra import pprintAlgebra, translateQuery
from rdflib.plugins.sparql.parser import parseQuery
from rdflib.namespace import FOAF
from rdflib.graph import Graph, plugin
from rdflib.serializer import Serializer

from rdflib.tools.rdf2dot import rdf2dot

# re_variables = re.compile(r"[?$]\w+\.?")
# re_URIRef = re.compile(r'<([^\s"<>]+)>')
# # re_blank_node = re.compile(r"^_:\w+")
# re_predicate = re.compile(r'<.*?>\.?')
# re_key_words = re.compile(r"(?:select|where)", re.IGNORECASE)

infile="template_store_df.pickle"
pickle_handle = open(infile, 'rb')
template_store_df = pickle.load(pickle_handle)
pickle_handle.close()

file_name = 'qald_combined_with_query.csv'
qald_queries_df = pd.read_csv(file_name)
queries = qald_queries_df['query']

# re_qald_sparql = re.compile(r"[]\w+\.?")
count = 0
for query in queries:
    query = queries[8]
    query = eval(query)['sparql']
    q_graph = QueryGraph(query, {})
    count += 1
    for s, p, o in q_graph.processed_graph:
        print("printing triples in the processed_graph")
        print((s, p, o))
    print("query number %d parsed successfully:" %count)
    # for template_graph in template_store_df["template_structure_graph"]:
        # for s, p, o in template_graph:
        #     print("printing triples in the processed_graph")
        #     print((s, p, o))
        # print("eqality of g1 and g1:", isomorphic(template_graph, template_graph))










