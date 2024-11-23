import re
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd
from langchain_ollama import OllamaLLM

import vectorizer
llm = OllamaLLM(model="llama3.1")
# Example user query
user_query = "Give me the information of the following protein: A0A0C5B5G6"

# def extract_protein_name(query_from_user):
#     """
#     Extracts protein name or keywords from the given user query using the LLM.

#     Args:
#         query_from_user (str): The user query which contains protein information.

#     Returns:
#         str: The extracted keywords, joined by commas if multiple.
#     """
#     query_first = f"""The provided sentence is "{query_from_user}". Extract only the keywords from the given sentence.
#     Note: only give the keywords, do not give unnecessary words."""
#     print(f"Query to LLM: {query_first}")

#     # Invoke the LLM to extract keywords
#     response = llm.invoke(query_first)
#     print(f"Response from LLM: {response}")

#     # Split the response into words, strip whitespace, and join with commas
#     keywords = ", ".join(word.strip() for word in response.split() if word.strip())
#     print(f"Extracted Keywords: {keywords}")

#     return keywords

# keywords = extract_protein_name(user_query)

keywords = """
primaryAccession: A0A1B0GTW7 | secondaryAccessions: ["A0A2R8Y3T5"] 
"""
# Step 1: Load the SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Step 2: Vectorize the keywords
query_vector = model.encode([keywords])

# Step 3: Load the FAISS index
index = faiss.read_index("protein_vectors.index")

# Search FAISS for the closest match
distances, indices = index.search(np.array(query_vector), k=5)

# # Retrieve the corresponding concatenated row
# if len(indices) > 0 and indices[0][0] < len(vectorizer.concatenated_rows):
#     most_relevant_row = vectorizer.concatenated_rows[indices[0][0]]
#     print("Most Relevant Concatenated Row:")
#     print(most_relevant_row)
# else:
#     print("No matching result found in the index.")
# Step 5: Retrieve the most relevant rows using the indices
if len(indices) > 0:
    print("Top 3 Matching Rows and Their Scores:")
    for i in range(5):
        idx = indices[0][i]
        distance = distances[0][i]
        # Retrieve the corresponding concatenated row from the list
        matching_row = vectorizer.concatenated_rows[idx]
        print(f"Score: {distance}")
        print(f"Row {i + 1}: {matching_row}")  # Directly print the concatenated row
        print("-" * 50)
else:
    print("No matching result found in the index.")

