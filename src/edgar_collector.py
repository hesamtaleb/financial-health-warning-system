# This is our data collector from SEC EDGAR
# SEC EDGAR is the US government's free financial database
# Every public company must file their finances here by law

import requests  # lets us make internet requests (like a browser)
import json      # lets us read JSON data (how the internet sends data)
import time      # lets us add delays between requests (be polite to the server)
import os        # lets us interact with folders and files on our computer


# Our "identity card" when talking to SEC EDGAR
# The SEC requires you to identify yourself - it's their rule
# If you don't send this, they will block your requests
HEADERS = {
    "User-Agent": "Mohammad Hesam Zibasaztalebi tlbhesam@gmail.com",
    "Accept-Encoding": "gzip, deflate",
    "Host": "data.sec.gov"
}


# This function finds a company's unique ID number on SEC EDGAR
# Every company has a CIK number - like a passport number for companies
# We need this CIK to then go fetch their financial data
def get_company_cik(company_name):
    
    # We tell the user what we're doing
    print(f"Searching for {company_name} on SEC EDGAR...")
    
    # This endpoint is specifically designed for company search
    url = "https://www.sec.gov/cgi-bin/browse-edgar?company=apple+inc&CIK=&type=10-K&dateb=&owner=include&count=10&search_text=&action=getcompany&output=atom"
    
    # We use Apple's known CIK directly - more reliable
    # Apple Inc's CIK is 0000320193 - this is a fact, like Apple's passport number
    known_ciks = {
        "Apple": "0000320193",
        "Microsoft": "0000789019",
        "Amazon": "0001018724"
    }
    
    if company_name in known_ciks:
        cik = known_ciks[company_name]
        print(f"Found! CIK number: {cik}")
        return cik
    else:
        print(f"Company not found!")
        return None

# This function gets the actual financial data for a company
# using their CIK number that we found above
def get_company_facts(cik):

    # We tell the user what we're doing
    print(f"Fetching financial data for CIK: {cik}...")

    # This is the URL where SEC stores all financial facts for a company
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

    # We send the request with our identity card
    response = requests.get(url, headers=HEADERS)

    # If the request was successful (200 means OK in internet language)
    if response.status_code == 200:
        print("Successfully retrieved financial data!")
        return response.json()
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None


# This is where our script STARTS running
# Think of this as the "play button" of our script
if __name__ == "__main__":

    # Step 1 - Find Apple's CIK number
    cik = get_company_cik("Apple")

    # Step 2 - Use that CIK to get Apple's financial data
    if cik:
        data = get_company_facts(cik)

        # Step 3 - Save the data to our data/raw folder
        if data:
            os.makedirs("data/raw", exist_ok=True)
            with open("data/raw/apple_facts.json", "w") as f:
                json.dump(data, f)
            print("Data saved to data/raw/apple_facts.json!")