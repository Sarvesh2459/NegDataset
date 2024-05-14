import json
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



def convert_sparql(ques, input_sparql, extracted):
    l = extracted * 0.3
    r = extracted * 1.7
    q = []
    # q.append({'sparql_neg': input_sparql, 'ques_neg': ques})
    for i in range(5):
        if type(extracted) == type(1):
            l1 = extracted - (i + 1)*(extracted - int(l))//10
            r1 = extracted + (i + 1)*(int(r) - extracted)//10
        else:
            l1 = extracted - (i + 1)*(extracted - l)/10
            r1 = extracted + (i + 1)*(r - extracted)/10

        if 'YEAR' in input_sparql:
            s1 = f'YEAR(?x) >= {l1} && YEAR(?x) <={r1}'
            s2 = f'YEAR(?x) >= {r1}'
            s3 = f'YEAR(?x) <= {l1}'
        else:
            s1 = f'xsd:float(?x) >= {l1} && xsd:float(?x) <={r1}'
            s2 = f'xsd:float(?x) >= {r1}'
            s3 = f'xsd:float(?x) <= {l1}'
        quer = re.sub('contains\(.*\)', f'{s1})', input_sparql)
        ques1 = re.sub(' [0-9]+[ \.]*[0-9]* *[0-9]*', f' between {l1} and {r1} ', ques)
        q.append({'sparql_neg': quer, 'ques_neg': ques1})
        quer = re.sub('contains\(.*\)', f'{s2})', input_sparql)
        if 'YEAR' in input_sparql:
            ques1 = re.sub(' [0-9]+[ \.]*[0-9]* *[0-9]*', f' after {r1} ', ques)
        else:
            ques1 = re.sub(' [0-9]+[ \.]*[0-9]* *[0-9]*', f' greater than {r1} ', ques)
        q.append({'sparql_neg': quer, 'ques_neg': ques1})
        quer = re.sub('contains\(.*\)', f'{s3})', input_sparql)
        if 'YEAR' in input_sparql:
            ques1 = re.sub(' [0-9]+[ \.]*[0-9]* *[0-9]*', f' before {l1} ', ques)
        else:
            ques1 = re.sub(' [0-9]+[ \.]*[0-9]* *[0-9]*', f' less than {l1} ', ques)
        q.append({'sparql_neg': quer, 'ques_neg': ques1})
    
    return q

f = open('test_final.json', 'r')
data=json.load(f)
res = []
for t in data:
    if extract_numeric_value(t['sparql_neg']):
        res.extend(convert_sparql(t['ques_neg'], t['sparql_neg'], extract_numeric_value(t['sparql_neg'])))

print(len(res))
with open("mydata.json", "w") as final:
    json.dump(res, final)