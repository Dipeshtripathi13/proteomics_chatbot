

from langchain_ollama import OllamaLLM
import requests
import json

import response_process

llm = OllamaLLM(model="llama3.1")
query_from_user = "Give me short information about the protein P69905?"

# Step 1: Extract protein name using LLM
query_first = f"""The provided sentence is "{query_from_user}". Extract the protein name from the given.
Note: only give the protein name, only one word for the protein name, and do not give any other words in the response."""
print(f"Query to extract protein name: {query_first}")
response = llm.invoke(query_first)
protein_name = response.strip()
print(f"Extracted protein name: {protein_name}")

# Step 2: Fetch data from UniProt API
api_end_point_prot1 = f"https://rest.uniprot.org/uniprotkb/{protein_name}"
print(f"API Endpoint is: {api_end_point_prot1}")

try:
    response_data = requests.get(api_end_point_prot1)
    
    if response_data.status_code == 200:
        # Parse the JSON response
        response_json = response_data.json()
        
        # Extract required fields
        required_fields = {
    "entryType": response_json.get("entryType"),
    "primaryAccession": response_json.get("primaryAccession"),
    "secondaryAccessions": response_json.get("secondaryAccessions", []),
    "uniProtkbId": response_json.get("uniProtkbId"),
    "entryAudit": response_json.get("entryAudit"),
    "organism": response_json.get("organism"),
    "proteinExistence": response_json.get("proteinExistence"),
    "proteinDescription": response_json.get("proteinDescription"),
    "genes": response_json.get("genes", []),
    "Functions": [
        comment.get("texts", [{}])[0].get("value", "N/A")
        for comment in response_json.get("comments", [])
        if comment.get("commentType") == "FUNCTION" and comment.get("texts")
    ],
    "Miscellaneous": [
        comment.get("texts", [{}])[0].get("value", "N/A")
        for comment in response_json.get("comments", [])
        if comment.get("commentType") == "MISCELLANEOUS" and comment.get("texts")
    ],
}
        context = response_process.preprocess_protein_data(required_fields)
        print(f"context is : {context}")
        followup_query = f"""Given the following context about a protein:
{context}

Answer the question: "{query_from_user}"."""
        print(f"Follow-up Query:\n{followup_query}")
        
        # Get the answer from LLM
        answer = llm.invoke(followup_query)
        print("Answer from LLM:")
        print(answer)
    else:
        print(f"Failed to fetch data. HTTP Status Code: {response_data.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error occurred while fetching data: {e}")

    

if __name__ == "__main__":
    print("This is model.py being executed directly.")
