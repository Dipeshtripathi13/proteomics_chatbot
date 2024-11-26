from langchain_ollama import OllamaLLM
import requests
import json
import exteract_index
import response_process
from langchain.memory import ConversationBufferMemory

# Initialize the LLM
llm = OllamaLLM(model="llama3.2:1b")

# Initialize memory for conversation history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
global previous_response

# Function to extract protein name from the user's query
def extract_protein_name(query_from_user):
    # user_query = "Give me the information of the following protein: O14967"
    primary_accession = exteract_index.retrieve_primary_accession(query_from_user)
    # print(f"Primary Accession: {primary_accession}")
    if primary_accession == "No match found":

        query_first = f"""The provided sentence is "{query_from_user}". Extract only the protein id from the given sentence if present.
        If the given sentence is refering to the previous chat history then provide the response as "TRUE"
        If the given sentence does not contain protin id then give "No Protin Id found" as response.
        Note: only give the protein ID, only one word for the protein Id, and do not give any other words in the response.
        """
        print(query_first)
        response = llm.invoke(query_first)
        # print(f"response is {response}")
        if response != "No Protin Id found" or response != "NAA" :
            protein_name = response.strip()
            print(f"protin name is {protein_name}")
        else:
            protein_name = response
        return protein_name
    else:
        protein_name = primary_accession
        return protein_name

# Function to fetch protein data from UniProt API
def fetch_protein_context(protein_name):
    global previous_response
    if protein_name != "No Protin Id found" or protein_name != "NAA" or protein_name != "TRUE":
        api_end_point_prot1 = f"https://rest.uniprot.org/uniprotkb/{protein_name}"
        try:
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
                previous_response = context
                print(f"context is {context}")
                return context
            elif(protein_name == "TRUE"):
                context = previous_response

            else:
                raise Exception(f"Failed to fetch data (HTTP {response_data.status_code})")

        except Exception as e:
            # Log the error and return a default context
            print(f"Error fetching protein context: {e}")
            return {
                "error": True,
                "message": "Exception has occurred. Can you specify the protein ID for more information?"
            }
    else:
        context = "The provided user query does not contains protein Id. Can you specify the protein Id for more information? The knowledge based for protein name is for just first 500 uniprot entry."


# Function to generate a response based on the user's query and protein context
def generate_response(query_from_user, context):
    followup_query = f"""Given the following context :{context}. 
Answer the following question: "{query_from_user}".
"""
    print(f"the follwo up query is: {followup_query}")
    response = llm.invoke(followup_query)
    return response

if __name__ == "__main__":
    print("This is model.py being executed directly.")
