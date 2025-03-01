import requests
import pandas as pd
import time
from bs4 import BeautifulSoup

# Load snapshot URLs from the Excel file
input_excel = "C:/Code/Output/data_gov_snapshots.xlsx"
df = pd.read_excel(input_excel)

# Prepare storage for scraped results
scraped_data = []

# Function to scrape dataset count from an archived page
def scrape_dataset_count(url):
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Primary Selector: Dataset count in <h4>
            dataset_count_element = soup.find("h4", string=lambda text: text and "datasets available" in text.lower())
            if dataset_count_element:
                dataset_count = int("".join(filter(str.isdigit, dataset_count_element.text)))
                return dataset_count
            
            # Fallback Selector: Dataset count in <li>
            dataset_count_li = soup.find("li", string=lambda text: text and any(c.isdigit() for c in text))
            if dataset_count_li:
                dataset_count = int("".join(filter(str.isdigit, dataset_count_li.text)))
                return dataset_count

            return "Not Found"
        else:
            return f"Failed ({response.status_code})"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Loop through all snapshot URLs and scrape dataset count
for index, row in df.iterrows():
    snapshot_date = row["Snapshot Date"]
    snapshot_url = row["First Snapshot"]  # Only scrape the first snapshot

    print(f"Scraping {snapshot_date} - {snapshot_url}")
    dataset_count = scrape_dataset_count(snapshot_url)

    # Store the results
    scraped_data.append([snapshot_date, snapshot_url, dataset_count])

    # Wait 22 seconds between requests to prevent rate-limiting
    time.sleep(22)

# Convert scraped data to a DataFrame
scraped_df = pd.DataFrame(scraped_data, columns=["Snapshot Date", "Snapshot URL", "Dataset Count"])

# Save to a new Excel file
output_excel = "C:/Code/Output/data_gov_dataset_counts.xlsx"
scraped_df.to_excel(output_excel, index=False)

print(f"\nData scraping complete. Results saved to {output_excel}")
