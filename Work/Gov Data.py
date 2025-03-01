import requests
import pandas as pd
import time

# List of inauguration years we want to check (January of each)
inauguration_years = [2013, 2017, 2021, 2025]
wayback_api_url = "https://web.archive.org/cdx/search/cdx"

# List to store snapshot data
snapshot_data = []

for year in inauguration_years:
    for day in range(1, 32):  # Loop through January 1st to 31st
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

        try:
            response = requests.get(wayback_api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if len(data) > 1:  # Ensure we got snapshot data
                timestamps = [entry[0] for entry in data[1:]]  # Extract timestamps
                urls = [entry[1] for entry in data[1:]]  # Extract snapshot URLs
                
                first_snapshot = f"https://web.archive.org/web/{timestamps[0]}/{urls[0]}"
                last_snapshot = f"https://web.archive.org/web/{timestamps[-1]}/{urls[-1]}"

                # Store snapshot details
                snapshot_data.append([timestamps[0][:8], first_snapshot, last_snapshot])
                
                print(f"{timestamps[0][:8]} | First: {first_snapshot} | Last: {last_snapshot}")
        
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving snapshots for {year}-{day:02d}: {e}")
        
        time.sleep(1.5)  # Pause to prevent rate limits

# Convert data to a DataFrame
df = pd.DataFrame(snapshot_data, columns=["Snapshot Date", "First Snapshot", "Last Snapshot"])

# Save to Excel
excel_filename = "C:/Code/Output/data_gov_snapshots.xlsx"
df.to_excel(excel_filename, index=False)

print(f"\nData saved to {excel_filename}")
