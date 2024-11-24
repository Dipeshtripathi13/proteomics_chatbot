import pandas as pd
import numpy as np
import faiss
from transformers import AutoTokenizer, AutoModel
import torch

# Load ProtTrans model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("Rostlab/prot_bert_bfd")
model = AutoModel.from_pretrained("Rostlab/prot_bert_bfd")

def encode_prottrans(texts, max_length=128):
    """
    Encode a list of protein-related text using the ProtTrans model with truncation.
    Args:
        texts (list): List of strings to encode.
        max_length (int): Maximum token length for truncation.
    Returns:
        np.ndarray: Encoded embeddings.
    """
    embeddings = []
    for text in texts:
        inputs = tokenizer.batch_encode_plus(
            [text],
            add_special_tokens=True,
            padding="max_length",
            truncation=True,
            max_length=max_length,
            return_tensors="pt"
        )
        with torch.no_grad():
            outputs = model(**inputs)
        # Mean pooling to get a single vector representation
        embeddings.append(outputs.last_hidden_state.mean(dim=1).squeeze().numpy())
    return np.array(embeddings)

# Load and preprocess data
df = pd.read_csv("uniprot_data.csv")

fields = [
    "entryType",
    "primaryAccession",
    "secondaryAccessions",
    "uniProtkbId",
    "entryAudit",
    "organism",
    "proteinExistence",
    "proteinDescription",
    "genes",
    "Functions",
    "Miscellaneous"
]

def concatenate_fields(row, fields):
    """
    Concatenate row fields without any weights.
    Args:
        row (pd.Series): The row to concatenate.
        fields (list): List of fields to include.
    Returns:
        str: Concatenated string of fields.
    """
    concatenated = []
    for field in fields:
        if pd.notna(row[field]):  # Skip empty fields
            concatenated.append(f"{field}: {row[field]}")  # Concatenate field name with value
    return " | ".join(concatenated)

# Apply concatenation without weighting
concatenated_rows = df.apply(lambda row: concatenate_fields(row, fields), axis=1)

# Encode rows using ProtTrans with truncation
print("Encoding rows with ProtTrans...")
row_vectors = encode_prottrans(concatenated_rows)

# Normalize for cosine similarity
faiss.normalize_L2(row_vectors)

# Build FAISS index
dim = row_vectors.shape[1]  # This should now be consistent with the query dimension
index = faiss.IndexFlatIP(dim)
index.add(row_vectors)

# Save the index
faiss.write_index(index, "protein_vectors1.index")
print("FAISS index rebuilt and saved!")
