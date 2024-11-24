import requests

# Define the SPARQL endpoint
endpoint_url = "https://sparql.uniprot.org/sparql"

# Define the SPARQL query
sparql_query = """
PREFIX up: <http://purl.uniprot.org/core/>
SELECT ?taxon
FROM <http://sparql.uniprot.org/taxonomy>
WHERE
{
    ?taxon a up:Taxon .
}
"""

# Define headers and parameters for the request
headers = {
    "Accept": "application/json"  # Request results in JSON format
}
params = {
    "query": sparql_query,  # The SPARQL query
    "format": "json"        # Desired response format
}

# Send the GET request
response = requests.get(endpoint_url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    results = response.json()
    for result in results["results"]["bindings"]:
        print(result["taxon"]["value"])
else:
    print(f"Failed to execute SPARQL query. HTTP Status Code: {response.status_code}")
    print(f"Error: {response.text}")
