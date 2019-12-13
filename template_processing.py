import pandas as pd
from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.sparql.algebra import pprintAlgebra, translateQuery
from query_graph import *
import pickle

file_name="lc-quad2.0_nitpicks.json"
templates = json.load(open(file_name, 'r'))
template_store_df= pd.DataFrame(columns=["template_category", "query_type", "query_variables", "bgp_variables", "template_structure_graph"])


wiki_prefixes = {"wd": "http://www.wikidata.org/entity/",
                         "wdv": "http://www.wikidata.org/value/",
                         "wdt": "http://www.wikidata.org/prop/direct/",
                         "p": "http://www.wikidata.org/prop/",
                        "ps": "http://www.wikidata.org/prop/statement/",
                        "pq": "http://www.wikidata.org/prop/qualifier/"
                         }

template_count = 0
for template in templates:

    # Create Template-graph tg
    try:
        # template = templates[18]["sparql_wikidata"]
        template = template["sparql_wikidata"]

        try:
            q_graph = QueryGraph(template, wiki_prefixes)
            # for s, p, o in q_graph.processed_graph:
            #     print("printing triples in the processed_graph")
            #     print((s, p, o))
            # print("eqality of g1 and g1:", q_graph.compare_for_equality(q_graph))
            # template_count += 1
            # print("template %d processed/parsed so far" %template_count)
            template_store_df = template_store_df.append({"query_type": q_graph.query_type,
                                                    "query_variables": q_graph.parameter_variables, "bgp_variables": q_graph.bgp_variables,
                                                    "template_structure_graph": q_graph.processed_graph},
                                                   ignore_index=True).fillna("tbd")


        except Exception as e:
            print("exception encountered")
            query_algebra = prepareQuery(template)
            pprintAlgebra(query_algebra)


    except Exception as e:
        print("KeyError: %s not found" %e)

filename = "template_store_df.pickle"
pickle_handle = open(filename, 'wb')
pickle.dump(template_store_df,pickle_handle)
pickle_handle.close()

# print("run_finished")
