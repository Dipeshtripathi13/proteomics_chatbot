import re
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from langchain_ollama import OllamaLLM
import vectorizer 

def retrieve_primary_accession(user_query):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    query_vector = model.encode([user_query])

    # Load the FAISS index
    index = faiss.read_index("protein_info_vectors.index")

   
    distances, indices = index.search(np.array(query_vector), k=1)

    
    if len(indices) > 0 and len(indices[0]) > 0 and distances < 0.85:
        idx = indices[0][0]
        matching_row = vectorizer.concatenated_rows[idx]
        print(distances)
        print(matching_row)

        
        match = re.search(r"primaryAccession:\s*(\S+)", matching_row)
        if match:
            return match.group(1)

    return "No match found" 

