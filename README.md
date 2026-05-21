# scrapping-of-financial-data-from-moneycontrol-website-
This is a practice repository for scrapping financial data from money control using python , requests, beautifulsoup , playwright and other tools nessecary. 

The code in the file extract_company_name.py is for extracting the list of companies along with there url which are lited on money control . 

The code in 03_scrape_financials.py is for scraping the financial data of list of companies which we have extracted from the extract_company_name.py code. This file needs company name and its url for the required financial data scraping.   It gives information about profit loss, balance sheet , cash flow , ratios, and industry of company and store the scraped files in diffecnt folders respectively in csv format. 

The code in extract_single_company_info is for getting the company info for a single company , where the code ask user input for company name based on that gives company url , nse code and bse code for the company.This info can futher be used by the 03_scrape_financials.py code to extract financial data for the given company as the url is provided. 
