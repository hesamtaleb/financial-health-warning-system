# This script converts our raw JSON files into a readable CSV
# So we can see all companies and their financial attributes in a table

import json
import os
import pandas as pd  # pandas is our Excel-like tool in Python

# 20 financial metrics covering all 3 pillars:
# Profitability, Debt/Solvency, Cash Flow, Size, Efficiency
METRICS = [
    # PROFITABILITY — is the company making money?
    "Revenues",
    "NetIncomeLoss",
    "OperatingIncomeLoss",
    "GrossProfit",
    "EarningsPerShareBasic",

    # DEBT & SOLVENCY — can it pay what it owes?
    "LongTermDebt",
    "ShortTermBorrowings",
    "LiabilitiesCurrent",
    "Liabilities",
    "StockholdersEquity",

    # CASH FLOW — is it running out of cash?
    "CashAndCashEquivalentsAtCarryingValue",
    "NetCashProvidedByUsedInOperatingActivities",
    "NetCashProvidedByUsedInFinancingActivities",
    "NetCashProvidedByUsedInInvestingActivities",

    # SIZE & ASSETS — how big is the company?
    "Assets",
    "AssetsCurrent",
    "RetainedEarningsAccumulatedDeficit",

    # EFFICIENCY — how well does it use resources?
    "AccountsReceivableNetCurrent",
    "InventoryNet",
    "InterestExpense",
]


def extract_latest_value(facts, metric_name):
    # This function digs into the JSON and finds the most recent value
    # for a given metric
    try:
        # The data is nested inside us-gaap → metric → units → USD
        values = facts["facts"]["us-gaap"][metric_name]["units"]["USD"]

        # Filter for annual reports only (10-K forms)
        annual = [v for v in values if v.get("form") == "10-K"]

        if annual:
            # Return the most recent value
            latest = sorted(annual, key=lambda x: x["end"])[-1]
            return latest["val"]
        return None
    except:
        return None


# This is where the script starts
if __name__ == "__main__":

    rows = []  # We'll collect all companies here

    # Loop through all JSON files in data/raw
    for filename in os.listdir("data/raw"):
        if not filename.endswith(".json"):
            continue

        filepath = f"data/raw/{filename}"

        with open(filepath) as f:
            data = json.load(f)

        # Start building a row for this company
        row = {
            "company": data.get("company_name", filename),
            "label": data.get("label"),
            "status": "Healthy" if data.get("label") == 0 else "Distressed"
        }

        # Extract each of the 20 financial metrics
        for metric in METRICS:
            row[metric] = extract_latest_value(data, metric)

        rows.append(row)

    # Convert to a pandas DataFrame — like an Excel table in Python
    df = pd.DataFrame(rows)

    # Sort by status so healthy and distressed are grouped
    df = df.sort_values("status")

    # Save as CSV
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/companies_overview.csv", index=False)

    print("CSV saved to data/processed/companies_overview.csv")
    print(f"\nShape: {df.shape[0]} companies, {df.shape[1]} columns")
    print(f"\nMissing values per metric:")
    print(df[METRICS].isnull().sum().to_string())