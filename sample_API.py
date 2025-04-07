import requests
import pandas as pd
from pathlib import Path

def fetch_data(url, params, write_csv=False):
    """
    Fetches electricity production data from the EnergiDataService API.
    
    Parameters:
        url (str): The API endpoint.
        params (dict): Query parameters for the API.
        write_csv (bool): Whether to write the DataFrame to a CSV file.
        
    Returns:
        pd.DataFrame: Processed data with datetime index, or None if request fails.
    """
    try:
        # Make the API request
        response = requests.get(url, params=params, timeout=1000)
        response.raise_for_status()  # Raises an error for HTTP errors

        # Parse JSON response and convert to DataFrame
        response_dict = response.json()
        response_df = pd.DataFrame(response_dict["records"])

        # Convert 'Minutes5UTC' to datetime and set as index
        response_df['Minutes5UTC'] = pd.to_datetime(response_df['Minutes5UTC'])
        response_df.set_index('Minutes5UTC', inplace=True)

        # Drop DK local time column since we're indexing on UTC
        response_df.drop(columns=['Minutes5DK'], inplace=True)

        # Optionally write to CSV
        if write_csv:
            output_path = Path('data') / 'raw_data.csv'
            output_path.parent.mkdir(exist_ok=True)  # Ensure 'data' folder exists
            response_df.to_csv(output_path)

        return response_df

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

def get_data(file_dir='data/raw_data.csv'):
    """
    Reads the processed data from a CSV file and parses datetime index.

    Parameters:
        file_dir (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame with datetime index.
    """
    file_path = Path(file_dir)
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)
    return df