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


# Our 60 companies — 30 healthy, 30 distressed
# Label 0 = healthy, Label 1 = distressed
# CIK numbers are verified on SEC EDGAR
COMPANIES = {
    # ── HEALTHY COMPANIES (label 0) ──
    "Apple":             {"cik": "0000320193", "label": 0},
    "Microsoft":         {"cik": "0000789019", "label": 0},
    "Google":            {"cik": "0001652044", "label": 0},
    "Amazon":            {"cik": "0001018724", "label": 0},
    "Johnson&Johnson":   {"cik": "0000200406", "label": 0},
    "Berkshire":         {"cik": "0001067983", "label": 0},
    "Visa":              {"cik": "0001403161", "label": 0},
    "Mastercard":        {"cik": "0001141391", "label": 0},
    "CocaCola":          {"cik": "0000021344", "label": 0},
    "Pepsi":             {"cik": "0000077476", "label": 0},
    "Walmart":           {"cik": "0000104169", "label": 0},
    "Procter&Gamble":    {"cik": "0000080424", "label": 0},
    "IBM":               {"cik": "0000051143", "label": 0},
    "Intel":             {"cik": "0000050863", "label": 0},
    "Nike":              {"cik": "0000320187", "label": 0},
    "McDonald's":        {"cik": "0000063908", "label": 0},
    "3M":                {"cik": "0000066740", "label": 0},
    "Honeywell":         {"cik": "0000773840", "label": 0},
    "Caterpillar":       {"cik": "0000018230", "label": 0},
    "Boeing":            {"cik": "0000012927", "label": 0},
    "UnitedHealth":      {"cik": "0000731766", "label": 0},
    "Pfizer":            {"cik": "0000078003", "label": 0},
    "Abbott":            {"cik": "0000001800", "label": 0},
    "Medtronic":         {"cik": "0001613103", "label": 0},
    "Costco":            {"cik": "0000909832", "label": 0},
    "HomeDepot":         {"cik": "0000354950", "label": 0},
    "Starbucks":         {"cik": "0000829224", "label": 0},
    "Texas Instruments": {"cik": "0000097476", "label": 0},
    "Qualcomm":          {"cik": "0000804328", "label": 0},
    "Cisco":             {"cik": "0000858877", "label": 0},

    # ── DISTRESSED COMPANIES (label 1) ──
    "Enron":             {"cik": "0001024401", "label": 1},
    "Lehman Brothers":   {"cik": "0000806648", "label": 1},
    "Toys R Us":         {"cik": "0001005414", "label": 1},
    "Kodak":             {"cik": "0000031235", "label": 1},
    "Blockbuster":       {"cik": "0001085734", "label": 1},
    "Sears":             {"cik": "0000089375", "label": 1},
    "JCPenney":          {"cik": "0001166928", "label": 1},
    "Hertz":             {"cik": "0000047987", "label": 1},
    "Chesapeake Energy": {"cik": "0000895126", "label": 1},
    "Pacific Gas":       {"cik": "0001004440", "label": 1},
    "Frontier Comm":     {"cik": "0000020286", "label": 1},
    "Pier 1 Imports":    {"cik": "0000078166", "label": 1},
    "RadioShack":        {"cik": "0000096289", "label": 1},
    "Gymboree":          {"cik": "0000786110", "label": 1},
    "Payless Shoes":     {"cik": "0000075111", "label": 1},
    "Nine West":         {"cik": "0000070858", "label": 1},
    "Bon Ton Stores":    {"cik": "0000878560", "label": 1},
    "Charming Shoppes":  {"cik": "0000768835", "label": 1},
    "Circuit City":      {"cik": "0000200406", "label": 1},
    "Borders Group":     {"cik": "0000865436", "label": 1},
    "Washington Mutual": {"cik": "0000933136", "label": 1},
    "CIT Group":         {"cik": "0001171825", "label": 1},
    "Conseco":           {"cik": "0000723254", "label": 1},
    "WorldCom":          {"cik": "0000723527", "label": 1},
    "Adelphia Comm":     {"cik": "0000796343", "label": 1},
    "Refco":             {"cik": "0001304421", "label": 1},
    "Delphi Corp":       {"cik": "0001072271", "label": 1},
    "Dana Holding":      {"cik": "0000026780", "label": 1},
    "Nortel Networks":   {"cik": "0000072572", "label": 1},
    "MF Global":         {"cik": "0001266717", "label": 1},
    # ── REPLACEMENT DISTRESSED COMPANIES ──
    "General Motors":    {"cik": "0000040987", "label": 1},
    "iHeartMedia":       {"cik": "0000739708", "label": 1},
    "Avaya":             {"cik": "0001418100", "label": 1},
    "Caesars":           {"cik": "0000858339", "label": 1},
    "Ambac Financial":   {"cik": "0000874215", "label": 1},
    "Residential Cap":   {"cik": "0001378454", "label": 1},
    "Patriot Coal":      {"cik": "0001376812", "label": 1},
    "Smurfit Stone":     {"cik": "0000093676", "label": 1},
    "Sbarro":            {"cik": "0000086120", "label": 1},
    "Filene's":          {"cik": "0000036270", "label": 1},
    "Palm Inc":          {"cik": "0001100644", "label": 1},
    "Sunedison":         {"cik": "0001341439", "label": 1},
    "Verso Corp":        {"cik": "0001421461", "label": 1},
    "Momentive":         {"cik": "0001138118", "label": 1},
}


# This function gets the actual financial data for a company
# using their CIK number
def get_company_facts(company_name, cik):

    # We tell the user what we're doing
    print(f"Fetching data for {company_name} (CIK: {cik})...")

    # This is the URL where SEC stores all financial facts for a company
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

    # We send the request with our identity card
    response = requests.get(url, headers=HEADERS)

    # If the request was successful (200 means OK in internet language)
    if response.status_code == 200:
        print(f"  ✓ Success!")
        return response.json()
    else:
        print(f"  ✗ Failed. Status code: {response.status_code}")
        return None


# This is where our script STARTS running
if __name__ == "__main__":

    # Create the output folder if it doesn't exist
    os.makedirs("data/raw", exist_ok=True)

    # Keep track of how many succeeded and failed
    success = 0
    failed = 0

    # Loop through ALL 60 companies
    for company_name, info in COMPANIES.items():

        cik = info["cik"]
        label = info["label"]

        # Get the financial data
        data = get_company_facts(company_name, cik)

        if data:
            # Add our label to the data (0=healthy, 1=distressed)
            data["label"] = label
            data["company_name"] = company_name

            # Save each company as its own JSON file
            filename = company_name.replace(" ", "_").replace("&", "and")
            filepath = f"data/raw/{filename}.json"

            with open(filepath, "w") as f:
                json.dump(data, f)

            success += 1
        else:
            failed += 1

        # Wait 0.5 seconds between requests - be polite to SEC server
        time.sleep(0.5)

    # Final summary
    print(f"\n{'='*40}")
    print(f"DONE! Successfully collected: {success}/60 companies")
    print(f"Failed: {failed} companies")
    print(f"Data saved in data/raw/ folder")