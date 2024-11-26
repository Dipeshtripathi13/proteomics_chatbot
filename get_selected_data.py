import requests
import json
import pandas as pd

# Define the API endpoint
url = "https://rest.uniprot.org/uniprotkb/search?query=*&size=500&format=json"

# Send the GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    data = response.json()
    
    # Extract relevant information
    extracted_data = []
    for entry in data['results']:
        protein_info = {
            'primaryAccession': entry.get('primaryAccession', 'N/A'),
            'uniProtkbId': entry.get('uniProtkbId', 'N/A'),
            'proteinDescription': entry.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', 'N/A')
        }
        extracted_data.append(protein_info)
    
    # Convert the extracted data to a DataFrame
    df = pd.DataFrame(extracted_data)

    # Save the DataFrame to a CSV file
    df.to_csv('proteins_info.csv', index=False)
    print("Data saved to proteins_info.csv")

else:
    print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
