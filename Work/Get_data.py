import requests
import json
from datetime1 import datetime

# List of inauguration years we want to check (January of each)
inauguration_years = [2009, 2013, 2017, 2021, 2025]
wayback_api_url = "https://archive.org/wayback/available"

# Dictionary to store snapshot URLs for each day in January of each year
snapshot_urls = {}

for year in inauguration_years:
    snapshot_urls[year] = {}
    
    for day in range(1, 32):  # Loop through January 1st to 31st
        timestamp = f"{year}01{day:02d}"  # Format YYYYMMDD
        
        # Query Wayback Machine API
        response = requests.get(wayback_api_url, params={"url": "https://data.gov", "timestamp": timestamp})
        
        if response.status_code == 200:
            data = response.json()
            if "archived_snapshots" in data and "closest" in data["archived_snapshots"]:
                snapshot_url = data["archived_snapshots"]["closest"]["url"]
                snapshot_urls[year][day] = snapshot_url
                print(f"{year}-{day:02d} Snapshot URL: {snapshot_url}")
            else:
                print(f"No snapshot found for {year}-{day:02d}")
        else:
            print(f"Failed to fetch data for {year}-{day:02d}")

# Output the snapshot URLs for manual verification
print("\nRetrieved Snapshot URLs:")
for year, days in snapshot_urls.items():
    print(f"\n{year}:")
    for day, url in days.items():
        print(f"  {year}-{day:02d}: {url}")
