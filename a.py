import re

def extract_numeric_value(sparql_query):
    """
    Extracts a numeric value from a SPARQL query using a regular expression.
    Returns the extracted value or None if no match is found.
    """
    # Use regex to extract the value
    match = re.search(r"contains\(\?x,'(-?\d+(\.\d+)?)'\)|contains\(YEAR\(\?x\),'(\d+)'\)", sparql_query)

    # Check if a match is found
    if match:
        # Return the first group that is not None
        extracted_value = next((group for group in match.groups() if group is not None), None)
        if float(extracted_value):
            if '.' not in extracted_value:
                return int(extracted_value)
            else:
                return float(extracted_value)
    return None

# Example usage:
sparql_query_1 = """
SELECT ?answer WHERE { wd:Q1674067 wdt:P131 ?answer . MINUS { ?answer wdt:P1082 ?x FILTER(contains(?x,'6801')) }}
"""

sparql_query_2 = """
SELECT ?answer WHERE { wd:Q310777 wdt:P1412 ?answer . MINUS { ?answer wdt:P580 ?x FILTER(contains(YEAR(?x),'1350')) }}
"""

sparql_query_3 = """
SELECT ?answer WHERE { wd:Q12206 wdt:P1542 ?answer . MINUS { ?answer wdt:P1692 ?x FILTER(contains(?x,'362.0')) }}
"""

sparql_query_4 = """
SELECT ?answer WHERE { wd:Q181875 wdt:P69 ?answer . MINUS { ?answer wdt:P625 ?x FILTER(contains(?x,'-1.8132')) }}
"""

extracted_value_1 = extract_numeric_value(sparql_query_1)
extracted_value_2 = extract_numeric_value(sparql_query_2)
extracted_value_3 = extract_numeric_value(sparql_query_3)
extracted_value_4 = extract_numeric_value(sparql_query_4)


def convert_sparql(ques, input_sparql, extracted):
    l = extracted * 0.7
    r = extracted * 1.3
    q = []
    q.append((input_sparql, ques))
    for i in range(3):
        if type(extracted) == type(1):
            l1 = extracted - (i + 1)*(extracted - int(l))//10
            r1 = extracted + (i + 1)*(int(r) - extracted)//10
        else:
            l1 = extracted - (i + 1)*(extracted - l)/10
            r1 = extracted + (i + 1)*(r - extracted)/10

        if 'YEAR' in input_sparql:
            s1 = f'YEAR(?x) >= {l1} && YEAR(?x) <={r1}'
            s2 = f'YEAR(?x) >= {r1}'
            s3 = f'YEAR(?x) <={l1}'
        else:
            s1 = f'xsd:float(?x) >= {l1} && xsd:float(?x) <={r1}'
            s2 = f'xsd:float(?x) >= {r1}'
            s3 = f'xsd:float(?x) <={l1}'
        quer = re.sub('contains\(.*\)', f'{s1})', input_sparql)
        ques1 = re.sub(' [0-9]+[ \.]*[0-9]* *[0-9]*', f' between {l1} and {r1} ', ques)
        q.append((quer, ques1))
        quer = re.sub('contains\(.*\)', f'{s2})', input_sparql)
        if 'YEAR' in input_sparql:
            ques1 = re.sub(' [0-9]+[ \.]*[0-9]* *[0-9]*', f' after {r1} ', ques)
        else:
            ques1 = re.sub(' [0-9]+[ \.]*[0-9]* *[0-9]*', f' greater than {r1} ', ques)
        q.append((quer, ques1))
        quer = re.sub('contains\(.*\)', f'{s3})', input_sparql)
        if 'YEAR' in input_sparql:
            ques1 = re.sub(' [0-9]+[ \.]*[0-9]* *[0-9]*', f' before {l1} ', ques)
        else:
            ques1 = re.sub(' [0-9]+[ \.]*[0-9]* *[0-9]*', f' less than {l1} ', ques)
        q.append((quer, ques1))
    for i in q:
        print(i[0])
        print(i[1])
        print()
        


# convert_sparql("What City of Isla Grande de Tierra del Fuego doesn't have 6801 inhabitants" ,sparql_query_1,extract_numeric_value(sparql_query_1))
# convert_sparql("What doesn't make use of the organism with an index of refraction of 1 33432", "SELECT ?answer WHERE { wd:Q7239 wdt:P2283 ?answer . MINUS { ?answer wdt:P1109 ?x FILTER(contains(?x,'1.33432')) }}", extract_numeric_value("SELECT ?answer WHERE { wd:Q7239 wdt:P2283 ?answer . MINUS { ?answer wdt:P1109 ?x FILTER(contains(?x,'1.33432')) }}"))
# convert_sparql("What is being claimed by Alexandre Island That doesn't have a total fertility rate of 2 322", "SELECT ?answer WHERE { wd:Q200223 wdt:P1336 ?answer . MINUS { ?answer wdt:P4841 ?x FILTER(contains(?x,'2. MINUS { 322')) }}", extract_numeric_value("SELECT ?answer WHERE { wd:Q200223 wdt:P1336 ?answer . MINUS { ?answer wdt:P4841 ?x FILTER(contains(?x,'2.322')) }}"))
convert_sparql("What is the etymology of the CNO cycle That doesn't have a date of discovery as 1772 0 0","SELECT ?answer WHERE { wd:Q222971 wdt:P138 ?answer . MINUS { ?answer wdt:P575 ?x FILTER(contains(YEAR(?x),'1772')) }}", extract_numeric_value("SELECT ?answer WHERE { wd:Q222971 wdt:P138 ?answer . MINUS { ?answer wdt:P575 ?x FILTER(contains(YEAR(?x),'1772')) }}"))