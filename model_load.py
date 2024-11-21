from langchain_ollama import OllamaLLM


llm = OllamaLLM(model="llama3.1")
query_from_user = "What is the protein 1011?"
query_first = f"Extract the protein name from following sentence: sentence: {query_from_user}, Note: just give protein name that is only one word"
print(query_first)
response = llm.invoke(query_first)
print(response)