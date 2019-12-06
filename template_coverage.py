import re
import json
import pandas as pd

re_variables = re.compile(r"[?$]\w+\.?")
# re_blank_node = re.compile(r"^_:\w+")
re_predicate = re.compile(r'<.*?>\.?')
re_key_words = re.compile(r"(?:select|where)", re.IGNORECASE)

file_name="lc-quad2.0_nitpicks.json"
templates = json.load(open(file_name, 'r'))
template_type_df = pd.DataFrame(columns=["result_type", "result_variables", "bgp_type", "bgp_facts", "bgp_triples",
                                         "bgp_doubles",
                                         "bgp_constraints"])

# SELECT distinct WHERE {}
for template in templates:
    # test template
    # template = {"question": "Who is the developer of Free Software Foundation?",
	# 	"sparql_dbpedia18": "select distinct ?answer where { ?statement <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject>  ?answer. ?statement <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <http://www.wikidata.org/entity/P178> . ?statement <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> <http://wikidata.dbpedia.org/resource/Q48413>. }"}

    template = template["sparql_dbpedia18"]
    query_result, query_bgp = re.compile("(?:where|WHERE)").split(template)
    bgp_type = ""+"WHERE"

    count_target_variables = 0
    for token in query_result.split(" "):
        if re_variables.match(token):
            count_target_variables += 1
        elif re.compile(r'(?:select|SELECT)').match(token):
            result_type = ""+"SELECT"
        elif re.compile(r'(?:distinct|DISTINCT)').match(token):
            result_type = result_type + "_" + token
    result_variables = count_target_variables


    # vraibale predicate entity
    re_triple_pattern_vpe = re.compile(r'([?$]\w+\s+<.*?>\s+<.*?>)')

    # entity predicate variable
    re_triple_pattern_epv = re.compile(r'(<.*?>\s+<.*?>\s+[?$]\w+)')

    #vraibale predicate variable
    re_triple_pattern_vpv = re.compile(r'([?$]\w+\s+<.*?>\s+[?$]\w+)')

    #vraibale predicate
    re_double_pattern_vp = re.compile(r'([?$]\w+\s+<.*?>)$')

    count_bgp_triples = 0
    count_bgp_doubles = 0
    count_bgp_facts = 0

    query_bgp_tokenized=[]
    bgp_facts = []
    bgp_fact = ""
    token_count_3 = 0
    for token in query_bgp.split(" "):
        if re.compile(r'\{').match(token):
            continue

        elif re.compile(r'\}').match(token):
            if token_count_3 == 2 or token_count_3 == 3:
                bgp_facts.append(bgp_fact)
                bgp_fact = ""
                token_count_3 = 0
            else: # to_do to be made an incomplete sparql query.
                continue

        elif re.compile(r'"').match(token):
            continue

        elif token == ".":
            if token_count_3 == 3 or token_count_3 == 2:
                bgp_facts.append(bgp_fact)
                bgp_fact = ""
                token_count_3 = 0
            else:
                continue

        elif re_variables.match(token) or re_predicate.match(token):
            bgp_fact = bgp_fact + token + " "
            token_count_3 += 1
            if token_count_3 == 3:
                bgp_facts.append(bgp_fact)
                bgp_fact = ""
                token_count_3 =0

    for bgp_fact in bgp_facts:
        if re_triple_pattern_epv.match(bgp_fact):
            count_bgp_triples += 1
            count_bgp_facts += 1
        elif re_triple_pattern_vpe.match(bgp_fact):
            count_bgp_triples += 1
            count_bgp_facts += 1
        elif re_triple_pattern_vpv.match(bgp_fact):
            count_bgp_triples += 1
            count_bgp_facts += 1
        elif re_double_pattern_vp.match(bgp_fact) and (len(bgp_fact.split(' '))):
            count_bgp_doubles += 1
            count_bgp_facts += 1
        else:
            continue

    template_type_df = template_type_df.append({"result_type": result_type, "result_variables": result_variables,
                                                "bgp_type": bgp_type, "bgp_facts": count_bgp_facts, "bgp_triples": count_bgp_triples,
                                                "bgp_doubles": count_bgp_doubles, "bgp_constraints": ""},
                                               ignore_index=True).fillna("tbd")

    template_type_df.to_csv(("triple_count_based_classification.csv"), index=False)