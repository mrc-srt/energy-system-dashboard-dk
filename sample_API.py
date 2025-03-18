import requests
import json
import pandas as pd


API_URL = 'https://api.energidataservice.dk/dataset/DeclarationProduction'
PARAMS = {
    "start": "2025-01-01",
    "end": "2025-01-27",
    "limit": 0,
    "filter": '{ "PriceArea": "DK2" }'
}

def fetch_data(url, params):
    """Fetch data from API with error handling."""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

result = fetch_data(API_URL, PARAMS)

# Extract records
records = result.get("records", [])
    
# Convert to DataFrame for easier manipulation
df = pd.DataFrame(records)
print(df)