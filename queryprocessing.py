import re
import os

def load_stopwords(file_path="stopwords.txt"):
    """
    Load stopwords from a file.
    """
    if not os.path.exists(file_path):
        print(f"{file_path} not found. Run download_and_save_stopwords() first.")
        return set()
    with open(file_path, "r") as f:
        return set(f.read().splitlines())

def process_query_in_first_place(query_from_user):
    """
    Process the query by removing punctuation, tokenizing, and removing stopwords.
    """
    stopwords_file="stopwords.txt"
    stop_words = load_stopwords(stopwords_file)
    if not stop_words:
        return

    # Step 1: Remove punctuation
    query_without_punctuation = re.sub(r'[^\w\s\-_\.]', '', query_from_user)
    
    # Step 2: Tokenize
    words = query_without_punctuation.split()
    
    # Step 3: Remove stopwords
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return filtered_words


query_from_user = "The protein name is 'Clarin-2'"
key_words = process_query_in_first_place(query_from_user)
print(key_words)
