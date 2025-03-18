import requests
from bs4 import BeautifulSoup
import csv
import time

# List of dimmer models
dimmer_models = [
    "DVCL-253P", "DVCL-153P", "CTCL-153P", "SCL-153P", "AYCL-153P", "AYCL-253P", "NTCL-250",
    "RCL-153PNL", "PD-6WCL", "PD-10NXD", "MACL-153M", "MACL-LFQ", "MSCL-OP153M", "STCL-153PR",
    "NTRP-250", "DVRP-253P", "CTRP-253P", "RRST-PRO-N", "PD-5NE", "IPE04-1LZ", "VPE06-1LZ",
    "DSE06", "MRF2S-6ELV120", "RRD-PRO", "HQRD-PRO", "MA-PRO"
]

# Function to search Lutron website and get product link
def get_product_link(dimmer_model):
    search_url = f"https://www.lutron.com/en-US/Products/Pages/Search/SearchResults.aspx?search={dimmer_model}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve results for {dimmer_model}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    # Look for product links on the search result page
    product_links = soup.find_all("a", class_="search-result-product-title")

    if product_links:
        # Return the first matching product link
        product_url = "https://www.lutron.com" + product_links[0].get("href")
        return product_url
    else:
        print(f"No product found for {dimmer_model}")
        return None

# Prepare CSV file to save the results
with open("dimmer_models_with_links.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Dimmer Model", "Manufacturer Link", "Dimming Protocol"])

    # Loop through each dimmer model and search for its link
    for dimmer_model in dimmer_models:
        print(f"Searching for {dimmer_model}...")
        link = get_product_link(dimmer_model)

        if link:
            # If link found, write to CSV (You can manually add the dimming protocol based on your data)
            writer.writerow([dimmer_model, link, "N/A"])  # Replace "N/A" with actual dimming protocol if available
        time.sleep(2)  # Sleep to avoid overwhelming the server

print("Finished saving dimmer links to 'dimmer_models_with_links.csv'")
