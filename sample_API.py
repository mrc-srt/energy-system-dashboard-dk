import requests
import pandas as pd


api_url = 'https://api.energidataservice.dk/dataset/ElectricityProdex5MinRealtime'

query_params = {"start": "2025-01-01",
          "end": "2025-01-27",
          "limit": 0,
          "filter": '{ "PriceArea": "DK2" }',
          "sort" : "Minutes5UTC ASC"
          }

def fetch_data(url, params):
    """Fetch data from API with error handling."""
    try:
        response = requests.get(api_url, params=query_params, timeout=1000)
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

result = fetch_data(api_url, query_params)

# Extract records
records = result.get("records", [])
    
# Convert to DataFrame for easier manipulation
df = pd.DataFrame(records)
print(df)
