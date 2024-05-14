import requests
import re, json

def check_property_in_sparql(property_qid):
    property_check_query = f"ASK WHERE {{ {property_qid} wdt:P131 ?place. }}"
    return run_sparql_query(property_check_query)

def get_hierarchy_list(location_qid):
    hierarchy_query = '''SELECT ?item ?itemLabel WHERE {{ %s wdt:P131* ?item. SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}}'''%location_qid
    # print(hierarchy_query)
    result = run_sparql_query(hierarchy_query)
    return [item['item']['value'].split('/')[-1] for item in result['results']['bindings']], [item['itemLabel']['value'].split('/')[-1] for item in result['results']['bindings']]

def generate_answers(sparql_query, location_qid):
    def convert_sparql(query, source_entity, property_id, loc_pred, location_qid):
        res = "SELECT ?item ?itemLabel WHERE" + '{' + " wd:{0} wdt:{1} ?item .".format(source_entity, property_id) + " MINUS { ?item " + "wdt:{0}/wdt:P131* wd:{1}".format(loc_pred, location_qid)+ '}.' + ' SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }' + '}'
        return res
    pattern1 = r"wd:(Q\d+)"
    pattern2 = r"wdt:(P\d+)"
    q_matches = re.finditer(pattern1, sparql_query)
    p_matches = re.finditer(pattern2, sparql_query)
    res = []
    for match in q_matches:
        res.append(match.group(1))
    for match in p_matches:
        res.append(match.group(1))

    converted_query = convert_sparql(sparql_query, res[0], res[2], res[3], location_qid)
    # print(converted_query)
    result = run_sparql_query(converted_query)
    return [item['itemLabel']['value'].split('/')[-1] for item in result['results']['bindings']]

def replace_location_in_sparql(sparql, ls,location_qid):
    return sparql.replace(ls, location_qid)

def replace_question(question, org, location_label):
    return question.replace(org, location_label)

def run_sparql_query(query):
    # print(query)
    endpoint_url = "https://query.wikidata.org/sparql"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    params = {'query': query, 'format': 'json'}

    response = requests.get(endpoint_url, headers=headers, params=params)
    # print(response.json())
    return response.json()

if __name__ == "__main__":
    # Input SPARQL and property QID to check
    f = open('test_final.json', 'r')
    data=json.load(f)
    res = []
    pattern = r"wd:(Q\d+)"
    for t in data:
        input_sparql = t['sparql_neg']
        input_question = t['ques_neg']
    
        matches = re.finditer(pattern, input_sparql)
        last_entity_id = None
        for match in matches:
            last_entity_id = match.group(1)
        # print("Last found entity ID:", last_entity_id)
        property_qid = 'wd:' + last_entity_id
        # print(input_question)
        # print(generate_answers(input_sparql, last_entity_id))
        # print()

        # Check if the property exists in the input SPARQL
        if check_property_in_sparql(property_qid)['boolean']:
            # print(f"The property {property_qid} is a Location type")

            # Get the hierarchy list for the given location
            hierarchy_list, name_list = get_hierarchy_list(property_qid)
            # print(f"Hierarchy list: {name_list}")

            # Replace Q22889 in the input SPARQL and the English question with each element from the hierarchy list
            for q in range(1, len(hierarchy_list)):
                modified_sparql = replace_location_in_sparql(input_sparql, last_entity_id, hierarchy_list[q])
                modified_question = replace_question(input_question, name_list[0], name_list[q])
                res.append({'ques_neg': modified_question, 'sparql_neg': modified_sparql})
                # print('\n' + str(q))
                # print(f"\nModified SPARQL for {hierarchy_list[q]}:")
                # print(modified_sparql)
                
                # print(f"\nModified English question for {name_list[q]}:")
                # print(modified_question)

                # print('\nNew Answers')
                # print(generate_answers(input_sparql, hierarchy_list[q]))
                
        # else:
        #     # print(f"The property {property_qid} does not exist in the input SPARQL.")
        #     continue

print(len(res))
print(res[0])
with open("mydataloc.json", "w") as final:
    json.dump(res, final)