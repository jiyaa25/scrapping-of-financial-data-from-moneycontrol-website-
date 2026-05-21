import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time

# LOAD CSV
df = pd.read_csv("data/nse_companies2.csv")

# OPTIONAL TESTING
df = df.head(1)

# HEADERS
headers = {
    "User-Agent": "Mozilla/5.0"
}

# CREATE OUTPUT FOLDERS
os.makedirs("data/profit_loss", exist_ok=True)
os.makedirs("data/balance_sheet", exist_ok=True)
os.makedirs("data/cash_flow", exist_ok=True)
os.makedirs("data/ratios", exist_ok=True)

# LOOP THROUGH COMPANIES
for index, row in df.iterrows():

    try:

        # COMPANY NAME + URL
        company_name = row["Company"]
        url = row["URL"]
        print(f"\nProcessing: {company_name}")

        # SPLIT URL
        parts = url.split("/")
        company_slug = parts[-2]
        company_code = parts[-1]
        #print("Slug:", company_slug)
        #print("Code:", company_code)

        # INDUSTRY EXTRACTION
        try:
            company_response = requests.get(
                url,
                headers=headers,
                timeout=20
            )
            company_soup = BeautifulSoup(
                company_response.text,
                "lxml"
            )
            industry = company_soup.find(
                "a",
                title=lambda x: x and "Industry Details" in x
            )
            if industry:
                industry_name = industry.text.strip()
            else:
                industry_name = None

            print("Industry:", industry_name)

        except Exception as e:
            print("Industry extraction error:", e)
            industry_name = None

        # FINANCIAL URLS

        financial_urls = {
            "profit_loss":
            f"https://www.moneycontrol.com/financials/{company_slug}/profit-lossVI/{company_code}#{company_code}",

            "balance_sheet":
            f"https://www.moneycontrol.com/financials/{company_slug}/balance-sheetVI/{company_code}#{company_code}",

            "cash_flow":
            f"https://www.moneycontrol.com/financials/{company_slug}/cash-flowVI/{company_code}#{company_code}",

            "ratios":
            f"https://www.moneycontrol.com/financials/{company_slug}/ratiosVI/{company_code}#{company_code}"
        }

        # LOOP THROUGH FINANCIAL STATEMENTS
        for statement_name, financial_url in financial_urls.items():

            try:

                print(f"Scraping {statement_name}")
                response = requests.get(
                    financial_url,
                    headers=headers,
                    timeout=15
                )
                soup = BeautifulSoup(
                    response.text,
                    "lxml"
                )
                # FIND ALL TABLES                
                tables = soup.find_all("table")
                #print("Tables Found:", len(tables))

                if len(tables) <= 1:
                    print("Table index 1 not found")
                    continue

                table = tables[1]
                rows = table.find_all("tr")
                table_data = []

                # EXTRACT ROWS
                for tr in rows:
                    cells = tr.find_all(["td", "th"])
                    row_data = []
                    for cell in cells:
                        text = cell.text.strip()
                        row_data.append(text)

                    if row_data:
                        table_data.append(row_data)

                # DATAFRAME
                financial_df = pd.DataFrame(table_data)

                # SAFE FILE NAME
                safe_company_name = (
                    company_name
                    .replace("/", "_")
                    .replace("\\", "_")
                    .replace(":", "_")
                    .replace("*", "_")
                    .replace("?", "_")
                    .replace('"', "_")
                    .replace("<", "_")
                    .replace(">", "_")
                    .replace("|", "_")
                )

                # OUTPUT PATH
                if statement_name == "profit_loss":
                    output_path = (
                        f"data/profit_loss/"
                        f"{safe_company_name}_profitloss.csv"
                    )
                elif statement_name == "balance_sheet":
                    output_path = (
                        f"data/balance_sheet/"
                        f"{safe_company_name}_balancesheet.csv"
                    )
                elif statement_name == "cash_flow":
                    output_path = (
                        f"data/cash_flow/"
                        f"{safe_company_name}_cashflow.csv"
                    )
                elif statement_name == "ratios":
                    output_path = (
                        f"data/ratios/"
                        f"{safe_company_name}_ratios.csv"
                    )

                # SAVE CSV
                financial_df.to_csv(
                    output_path,
                    index=False
                )

                print("Saved:", output_path)

                # DELAY
                time.sleep(1)

            except Exception as e:
                print(
                    f"{statement_name} scraping error:",
                    e
                )

    except Exception as e:
        print("Company processing error:", e)

