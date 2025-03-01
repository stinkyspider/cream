import requests
import pandas as pd
import time

# List of inauguration years we want to check (January 20-31 only)
inauguration_years = [2013, 2017, 2021, 2025]
wayback_api_url = "https://web.archive.org/cdx/search/cdx"

# List to store snapshot data
snapshot_data = []

# Function to fetch snapshots with retries and rate limiting
def get_snapshots(params):
    retries = 3  # Retry up to 3 times
    for attempt in range(retries):
        try:
            response = requests.get(wayback_api_url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(15)  # Wait 15 seconds before retrying
    print(f"Skipping {params['from']} due to repeated failures")
    return None  # Return None if all attempts fail

# Loop through only January 20-31 for each inauguration year
for year in inauguration_years:
    for day in range(20, 32):  # Loop through Jan 20-31 only
        date_prefix = f"{year}01{day:02d}"

        # Query Wayback Machine CDX API for all snapshots on this day
        params = {
            "url": "https://data.gov",
            "from": date_prefix,
            "to": date_prefix,
            "output": "json",
            "fl": "timestamp,original",
            "filter": "statuscode:200"  # Only return successful snapshots
        }

        data = get_snapshots(params)

        if data and len(data) > 1:  # Ensure we got snapshot data
            timestamps = [entry[0] for entry in data[1:]]  # Extract timestamps
            urls = [entry[1] for entry in data[1:]]  # Extract snapshot URLs
            
            first_snapshot = f"https://web.archive.org/web/{timestamps[0]}/{urls[0]}"
            last_snapshot = f"https://web.archive.org/web/{timestamps[-1]}/{urls[-1]}"

            # Store snapshot details
            snapshot_data.append([timestamps[0][:8], first_snapshot, last_snapshot])
            
            print(f"{timestamps[0][:8]} | First: {first_snapshot} | Last: {last_snapshot}")
        
        time.sleep(10)  # Longer delay to avoid getting blocked

# Convert data to a DataFrame
df = pd.DataFrame(snapshot_data, columns=["Snapshot Date", "First Snapshot", "Last Snapshot"])

# Save to Excel
excel_filename = "C:/Code/Output/data_gov_snapshots.xlsx"
df.to_excel(excel_filename, index=False)

print(f"\nData saved to {excel_filename}")
