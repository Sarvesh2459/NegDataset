import requests

def get_entity_name(qid):
    # SPARQL query to retrieve the entity name for a given QID
    sparql_query = """
    SELECT ?entityLabel WHERE {
        wd:""" + qid + """ rdfs:label ?entityLabel.
        FILTER(LANG(?entityLabel) = "en")
    }
    """

    # SPARQL endpoint URL
    sparql_endpoint = "https://query.wikidata.org/sparql"

    # Headers with User-Agent information
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
        "Accept": "application/json"
    }

    # Parameters for the SPARQL query
    params = {
        "query": sparql_query,
        "format": "json"
    }

    # Sending the SPARQL query to the endpoint
    response = requests.get(sparql_endpoint, headers=headers, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()

        # Check if there are results
        if "results" in data and "bindings" in data["results"]:
            bindings = data["results"]["bindings"]

            # Check if there is at least one binding
            if len(bindings) > 0:
                # Extract and return the entity name
                return bindings[0]["entityLabel"]["value"]
            else:
                return f"No entity name found for {qid}"
        else:
            return "No results found"
    else:
        return f"Error: {response.status_code}"

# Example usage for Q1234
qid = "Q550219"
entity_name = get_entity_name(qid)
print(f"Entity name for {qid}: {entity_name}")
