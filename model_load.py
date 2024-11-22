

# from langchain_ollama import OllamaLLM
# import requests
# import json

# import response_process

# llm = OllamaLLM(model="llama3.1")
# query_from_user = "Give me short information about the protein P69905?"

# # Step 1: Extract protein name using LLM
# query_first = f"""The provided sentence is "{query_from_user}". Extract the protein name from the given.
# Note: only give the protein name, only one word for the protein name, and do not give any other words in the response."""
# print(f"Query to extract protein name: {query_first}")
# response = llm.invoke(query_first)
# protein_name = response.strip()
# print(f"Extracted protein name: {protein_name}")

# # Step 2: Fetch data from UniProt API
# api_end_point_prot1 = f"https://rest.uniprot.org/uniprotkb/{protein_name}"
# print(f"API Endpoint is: {api_end_point_prot1}")

# try:
#     response_data = requests.get(api_end_point_prot1)
    
#     if response_data.status_code == 200:
#         # Parse the JSON response
#         response_json = response_data.json()
        
#         # Extract required fields
#         required_fields = {
#     "entryType": response_json.get("entryType"),
#     "primaryAccession": response_json.get("primaryAccession"),
#     "secondaryAccessions": response_json.get("secondaryAccessions", []),
#     "uniProtkbId": response_json.get("uniProtkbId"),
#     "entryAudit": response_json.get("entryAudit"),
#     "organism": response_json.get("organism"),
#     "proteinExistence": response_json.get("proteinExistence"),
#     "proteinDescription": response_json.get("proteinDescription"),
#     "genes": response_json.get("genes", []),
#     "Functions": [
#         comment.get("texts", [{}])[0].get("value", "N/A")
#         for comment in response_json.get("comments", [])
#         if comment.get("commentType") == "FUNCTION" and comment.get("texts")
#     ],
#     "Miscellaneous": [
#         comment.get("texts", [{}])[0].get("value", "N/A")
#         for comment in response_json.get("comments", [])
#         if comment.get("commentType") == "MISCELLANEOUS" and comment.get("texts")
#     ],
# }
#         context = response_process.preprocess_protein_data(required_fields)
#         print(f"context is : {context}")
#         followup_query = f"""Given the following context about a protein:
# {context}

# Answer the question: "{query_from_user}"."""
#         print(f"Follow-up Query:\n{followup_query}")
        
#         # Get the answer from LLM
#         answer = llm.invoke(followup_query)
#         print("Answer from LLM:")
#         print(answer)
#     else:
#         print(f"Failed to fetch data. HTTP Status Code: {response_data.status_code}")
# except requests.exceptions.RequestException as e:
#     print(f"Error occurred while fetching data: {e}")

    

# if __name__ == "__main__":
#     print("This is model.py being executed directly.")

from langchain_ollama import OllamaLLM
import requests
import json
import response_process
from langchain.memory import ConversationBufferMemory

# Initialize the LLM
llm = OllamaLLM(model="llama3.1")

# Initialize memory for conversation history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Function to extract protein name from the user's query
def extract_protein_name(query_from_user):
    """
    Extracts protein name from the given user query using the LLM.

    Args:
        query_from_user (str): The user query which contains protein information.

    Returns:
        str: The extracted protein name.
    """
    query_first = f"""The provided sentence is "{query_from_user}". Extract the protein name from the given.
    Note: only give the protein name, only one word for the protein name, and do not give any other words in the response."""
    
    response = llm.invoke(query_first)
    protein_name = response.strip()
    return protein_name

# Function to fetch protein data from UniProt API
def fetch_protein_context(protein_name):
    """
    Fetch and preprocess context for a given protein name from UniProt.

    Args:
        protein_name (str): Name of the protein.
        
    Returns:
        str: Preprocessed context containing relevant protein information.
    """
    api_end_point_prot1 = f"https://rest.uniprot.org/uniprotkb/{protein_name}"
    response_data = requests.get(api_end_point_prot1)

    if response_data.status_code == 200:
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
        
        # Preprocess the context data
        context = response_process.preprocess_protein_data(required_fields)
        return context
    else:
        raise Exception(f"Failed to fetch data for protein {protein_name} (HTTP {response_data.status_code})")

# Function to generate a response based on the user's query and protein context
def generate_response(query_from_user, context):
    """
    Generates a response based on the user query and protein context using the LLM.

    Args:
        query_from_user (str): The user query.
        context (str): The context data about the protein.

    Returns:
        str: The generated response from the LLM.
    """
    followup_query = f"""Given the following context about a protein:
{context}

Answer the question: "{query_from_user}"."""
    
    response = llm.invoke(followup_query)
    return response

# Main function for testing purposes
if __name__ == "__main__":
    print("This is model.py being executed directly.")
    # query_from_user = "Give me short information about the protein P69905?"
    
    # # Step 1: Extract protein name
    # protein_name = extract_protein_name(query_from_user)
    # print(f"Extracted Protein Name: {protein_name}")
    
    # # Step 2: Fetch protein data and preprocess it
    # try:
    #     context = fetch_protein_context(protein_name)
    #     print(f"Context for {protein_name}: {context}")
        
    #     # Step 3: Generate a response
    #     response = generate_response(query_from_user, context)
    #     print(f"Response: {response}")
    
    # except Exception as e:
    #     print(f"Error: {e}")
