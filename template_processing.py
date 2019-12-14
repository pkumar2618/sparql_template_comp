import pandas as pd
from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.sparql.algebra import pprintAlgebra, translateQuery
from query_graph import *
import pickle


template_store_df= pd.DataFrame(columns=["question", "template", "template_id", "question_type", "query_type", "query_variables",
                                         "bgp_variables", "template_structure_graph", "triples_list"])


wiki_prefixes = {"wd": "http://www.wikidata.org/entity/",
                 "wdv": "http://www.wikidata.org/value/",
                 "wdt": "http://www.wikidata.org/prop/direct/",
                 "p": "http://www.wikidata.org/prop/",
                 "ps": "http://www.wikidata.org/prop/statement/",
                 "pq": "http://www.wikidata.org/prop/qualifier/"}

# template_count = 0
# file_name="lc-quad2.0_nitpicks.json"
files=["extracted_templates_test.json", "extracted_templates_train.json", "lc-quad2.0_nitpicks.json"]
unique_templates = []
for filename in files:
    if filename == "lc-quad2.0_nitpicks.json":
        templates = json.load(open(filename, 'r'))

        for template_temp in templates:
            # Create Template-graph tg
            try:
                # template = templates[18]["sparql_wikidata"]
                template = template_temp["sparql_wikidata"]

                try:
                    q_graph = QueryGraph(template, wiki_prefixes)
                    # for s, p, o in q_graph.processed_graph:
                    #     print("printing triples in the processed_graph")
                    #     print((s, p, o))
                    # print("eqality of g1 and g1:", q_graph.compare_for_equality(q_graph))
                    # template_count += 1
                    # print("template %d processed/parsed so far" %template_count)
                    template_store_df = template_store_df.append(
                        {"question": template_temp["question"], "query_type": q_graph.query_type,
                         "query_variables": q_graph.parameter_variables, "bgp_variables": q_graph.bgp_variables,
                         "template_structure_graph": q_graph.processed_graph, "triples_list": q_graph.triples_list},
                        ignore_index=True).fillna("tbd")
                except Exception as e:
                    print("exception encountered")
            except Exception as e:
                print("KeyError: %s not found" % e)

    else:
        templates = json.load(open(filename, 'r'))
        templates = templates["templates"]
        for template_temp in templates:
            if template_temp["template_id"] not in unique_templates:
                unique_templates.append(template_temp["template_id"])
                # Create Template-graph tg
                try:
                    # template = templates[18]["sparql_wikidata"]
                    template = template_temp["sparql_wikidata"]

                    try:
                        q_graph = QueryGraph(template, wiki_prefixes)
                        # for s, p, o in q_graph.processed_graph:
                        #     print("printing triples in the processed_graph")
                        #     print((s, p, o))
                        # print("eqality of g1 and g1:", q_graph.compare_for_equality(q_graph))
                        # template_count += 1
                        # print("template %d processed/parsed so far" %template_count)
                        template_store_df = template_store_df.append(
                            {"question": template_temp["question"], "template": template_temp["template"],
                             "template_id": template_temp["template_id"], "query_type": q_graph.query_type,
                             "query_variables": q_graph.parameter_variables, "bgp_variables": q_graph.bgp_variables,
                             "template_structure_graph": q_graph.processed_graph, "triples_list": q_graph.triples_list},
                            ignore_index=True).fillna("tbd")
                    except Exception as e:
                        print("exception encountered")
                except Exception as e:
                    print("KeyError: %s not found" %e)
            else:
                continue



# filename = "template_store_df.pickle"
# pickle_handle = open(filename, 'wb')
# pickle.dump(template_store_df,pickle_handle)
# pickle_handle.close()

filename = "template_store_df.csv"
template_store_df.to_csv(filename)

# print("run_finished")
