import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# Load CSV file
df = pd.read_csv("proteins_info.csv")

# Fields to include
fields = [
    "primaryAccession",
    "uniProtkbId",
    "proteinDescription",
]

# Concatenate fields with their names
concatenated_rows = df[fields].apply(
    lambda x: " | ".join(f"{field}: {x[field]}" for field in fields if pd.notna(x[field])),
    axis=1
).tolist()

# Vectorize rows
model = SentenceTransformer("all-MiniLM-L6-v2")
row_vectors = model.encode(concatenated_rows)

dim = row_vectors.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(np.array(row_vectors))


faiss.write_index(index, "protein_info_vectors.index")
