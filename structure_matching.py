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

## load template file, graphs
# infile="template_store_df.pickle"
# pickle_handle = open(infile, 'rb')
# template_store_df = pickle.load(pickle_handle)
# pickle_handle.close()
infile="template_store_df.csv"
template_store_df = pd.read_csv(infile)

## load QALD combined queries
file_name = 'qald_combined_with_query.csv'
qald_queries_df = pd.read_csv(file_name)
queries = qald_queries_df['query']

## store the stats of the comparision in a dataframe
qald_stat_with_templates_df = pd.DataFrame(columns=["query_question", "template_question", "query_triples",
                                                    "template_triples", "question_type"])

query_row_index = 0
for query in queries:
    # query = queries[891]
    try:
        query = eval(query)['sparql']
        q_graph = QueryGraph(query, {})
        # print("Query Structure:")
        # for s, p, o in q_graph.processed_graph:
        #     print((s, p, o))
        # print("\n")
        template_row_index = 0
        for template_triples_list in template_store_df["template_processed_triples"]:
            # template_graph = template_store_df["template_structure_graph"][2]
            template_graph = triples_list_to_graph(eval(template_triples_list))
            # print("template structure")
            # for s, p, o in template_graph:
            # print("printing triples in the processed_graph")
            # print((s, p, o))
            try:
                if isomorphic(q_graph.processed_graph, template_graph):
                    # print("query_graph and template_graph are isomorphic", )
                    # print("template structure")
                    # for s, p, o in template_graph:
                    #     print("printing triples in the processed_graph")
                    #     print((s, p, o))
                    # print("\n")
                    qald_stat_with_templates_df = qald_stat_with_templates_df.append(
                        {"query_question": qald_queries_df.iloc[query_row_index]['sentence_en'],
                         "template_question": template_store_df.iloc[template_row_index]["question"],
                         "query_triples": q_graph.triples_list,
                         "template_triples": template_store_df.iloc[template_row_index]["triples_list"],
                         "question_type": template_store_df.iloc[template_row_index]["question_type"]},
                        ignore_index=True).fillna("tbd")
                    break

            except Exception as e:
                print('\n')
                print("for query index %d and template index %d" % (query_row_index, template_row_index))
                print("Query Structure:")
                for s, p, o in q_graph.processed_graph:
                    print((s, p, o))
                print("template structure")

                for s, p, o in template_graph:
                    print("printing triples in the processed_graph")
                    print((s, p, o))
                print("\n")
                print("exception during graph comparision or during append to dataframe", e)

            template_row_index += 1

    except Exception as e:
        print("exception during qald-query read at query index %d" % (query_row_index))
        print("exception is", e)

    query_row_index += 1

with open("stats_qaldCombined_vs_LCQUAD2.csv", 'w') as filename:
    qald_stat_with_templates_df.to_csv(filename)





