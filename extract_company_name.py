import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# =========================
# CREATE DATA FOLDER
# =========================

os.makedirs("data", exist_ok=True)

# =========================
# HEADERS
# =========================

headers = {
    "User-Agent": "Mozilla/5.0"
}

# =========================
# STORAGE
# =========================

nse_data = []

# =========================
# SCRAPE A-Z
# =========================

#for letter in string.ascii_uppercase:
for letter in ["A", "B", "C"]:  # Test with first 3 letters
    url = f"https://www.moneycontrol.com/india/stockpricequote/{letter}"

    print(f"Scraping {letter}...")

    try:
        response = requests.get(url, headers=headers, timeout=15)

        soup = BeautifulSoup(response.text, "lxml")

        rows = soup.find_all("a", class_="bl_12")

        for row in rows:
            company_name = row.text.strip()
            company_url = row.get("href")
          #  parts = company_url.split("/")
          #  scid = parts[-1]    
            ''' try:

                company_response = requests.get(
                    company_url,
                    headers=headers,
                    timeout=15
                )

                company_soup = BeautifulSoup(
                    company_response.text,
                    "lxml"
                )

                industry = company_soup.find( "a",
                                title=lambda x: x and "Industry Details" in x
                            )
                print(industry)

            except Exception as e:
                print("Company page error:", e)'''

            nse_data.append({
                        "Company": company_name,
                        "URL": company_url
                    })

            #print(company_name)
            
        time.sleep(1)

    except Exception as e:
        print("Main page error:", e)

# SAVE CSV

df = pd.DataFrame(nse_data)

df.drop_duplicates(inplace=True)

df.to_csv(
    "data/nse_companies2.csv",
    index=False
)

print("\nSaved NSE company list")
print(df.head())