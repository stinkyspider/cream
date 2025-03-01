import requests

ckan_api_url = "https://catalog.data.gov/api/3/action/package_search"

# Fetch metadata for datasets
response = requests.get(ckan_api_url, params={"rows": 1})  # We only need metadata, so limit results

if response.status_code == 200:
    data = response.json()
    dataset_count = data["result"]["count"]  # Extract the total number of datasets
    print(f"Total datasets on Data.gov: {dataset_count}")
else:
    print(f"Error fetching dataset count: {response.status_code}")
