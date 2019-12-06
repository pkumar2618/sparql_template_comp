import re
import json
import pandas as pd
import rdflib
from rdflib import BNode, URIRef
from rdflib.namespace import XSD
from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.sparql.algebra import pprintAlgebra, translateQuery
from rdflib.plugins.sparql.parser import parseQuery
from rdflib.namespace import FOAF
from rdflib.graph import Graph, plugin
from rdflib.serializer import Serializer
from query_graph import *
from rdflib.tools.rdf2dot import rdf2dot

# re_variables = re.compile(r"[?$]\w+\.?")
# re_URIRef = re.compile(r'<([^\s"<>]+)>')
# # re_blank_node = re.compile(r"^_:\w+")
# re_predicate = re.compile(r'<.*?>\.?')
# re_key_words = re.compile(r"(?:select|where)", re.IGNORECASE)

file_name="lc-quad2.0_nitpicks.json"
templates = json.load(open(file_name, 'r'))
# template_type_df = pd.DataFrame(columns=["result_type", "result_variables", "bgp_type", "bgp_facts", "bgp_triples",
#                                          "bgp_doubles",
#                                          "bgp_constraints"])

template_graphs = {}
template_count = 1
# for template in templates:

    # Create Template-graph tg
template = templates[0]["sparql_dbpedia18"]
q1_graph = QueryGraph(template)

for s, p, o in q1_graph.processed_graph:
        print("printing triples in the processed_graph")
        print((s, p, o))

print("eqality of g1 and g1:", q1_graph.compare_for_equality(q1_graph))

# template1 = "select distinct ?ans where { ?statement <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> <http://wikidata.dbpedia.org/resource/Q204711> . ?statement <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <http://www.wikidata.org/entity/P1128> . ?statement <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> ?ans. }"
# template1 = "select distinct ?ans where { [] <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> <http://wikidata.dbpedia.org/resource/Q204711> . [] <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <http://www.wikidata.org/entity/P1128> . [] <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> ?ans. }"
# template1_s = "select distinct ?answer where { ?statement_s <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> <http://wikidata.dbpedia.org/resource/Q204711> . ?statement_s <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <http://www.wikidata.org/entity/P1128> . ?statement_s <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> ?answer. }"
# template1_s = "select distinct ?answer where { [] <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> <http://wikidata.dbpedia.org/resource/Q204711> . [] <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <http://www.wikidata.org/entity/P1128> . [] <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> ?answer. }"
# q1_graph = QueryGraph(template1)
# q1_s_graph = QueryGraph(template1_s)
# for s, p, o in q1_graph.graph:
#         print("printing triples in the graph1")
#         print((s, p, o))
#
# for s, p, o in q1_s_graph.graph:
#         print("printing triples in the graph1_s")
#         print((s, p, o))


# print("eqality of g1 and g1_s:", q1_graph.compare_for_equality(q1_s_graph))
# print("eqality of g1 and g1_s:", q1_graph.compare_for_isomorphism(q1_s_graph))
# print("similarity of g1 and g1_s:", q1_graph.compare_for_similarity(q1_s_graph))


template2 = templates[1]["sparql_dbpedia18"]
# template1_s = "select distinct ?answer where { ?statement <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> <http://wikidata.dbpedia.org/resource/Q204711> . ?statement <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <http://www.wikidata.org/entity/P1128> . ?statement <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> ?answer. }"
# q1_s_graph = QueryGraph(template1_s)
# template2 = "select distinct ?answer where { ?statement <http://www.w3.org/1999/02/22-rdf-syntax-ns#object>  ?answer. ?statement <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <http://www.wikidata.org/entity/P1128> . ?statement <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> <http://wikidata.dbpedia.org/resource/Q204711>. }"
q2_graph = QueryGraph(template2)
#
# for s, p, o in q1_s_graph.graph:
#         print("printing triples in the graph1")
#         print((s, p, o))
#
for s, p, o in q2_graph.processed_graph:
        print("printing triples in the graph2")
        print((s, p, o))
#
#
print("comparision of g1 and g2:", q1_graph.compare_for_equality(q2_graph))
print("similarity of g1 and g2:", q1_graph.compare_for_similarity(q2_graph))


print("debug_finished")
    # template_graphs["g" + template_count] = graph.parse(triple)

    # a_node1 = BNode()
    # a_node2 = BNode()
    # a_ref = URIRef('')
    # triple = (a_node1, a_ref, a_node2)
    ## using direct algebra

    # graph.add(triple)
    # for s in graph.subjects((None)):
    #     print("%s is a subject" % s)

    # for s, p, o in graph:
    #     print("printing triples in the graph")
    #     print((s, p, o))

    # template_graphs["g%s" %template_count] = graph
    # print(len(template_graphs["g1"]))

    # try:

        # print(g.serialize(format='json-ld', indent=4))
    # except Exception as e:
    #     print(e)

# g = rdflib.Graph()
# # g.load("foaf.rdf")

# for row in g.query('select ?s where { [] <http://xmlns.com/foaf/0.1/knows> ?s .}'):
#     print(row)