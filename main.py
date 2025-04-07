from sample_API import fetch_data, process_data


# API endpoint for 5-minute electricity production data in Denmark
api_url = 'https://api.energidataservice.dk/dataset/ElectricityProdex5MinRealtime'

# Query parameters: time range, area (DK2), no row limit, sorted ascending by time
query_params = {
    "start": "2015-01-01",
    "end": "2025-01-27",
    "limit": 0,
    "filter": '{ "PriceArea": "DK2" }',
    "sort": "Minutes5UTC ASC"
}


raw_df = fetch_data(api_url, query_params, write_csv=True)

df = process_data()