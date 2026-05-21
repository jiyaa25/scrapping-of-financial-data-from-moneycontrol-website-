from playwright.sync_api import sync_playwright
import time

company_name = input("Enter Company Name: ")

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    # OPEN WEBSITE
    page.goto(
        "https://www.moneycontrol.com",
        timeout=60000
    )

    time.sleep(5)

    # SEARCH BOX (desktop)
    search_box = page.locator("#search_str").first

    search_box.click()
    search_box.clear()

    # TYPE LIKE HUMAN
    search_box.type(
        company_name,
        delay=100
    )

    # WAIT FOR DROPDOWN TO UPDATE
    time.sleep(3)

    # DEBUG: SEE ALL RESULTS
    results = page.locator("ul.suglist.scrollBar li a")

    print("\nDropdown Results:")

    for i in range(results.count()):

        text = results.nth(i).inner_text()

        print(i, text)

    # TAKE FIRST RESULT FROM VISIBLE DROPDOWN
    first_result = results.first

    # COMPANY NAME
    company = first_result.get_attribute("title")

    # URL
    company_url = first_result.get_attribute("onclick")
    company_url = company_url.split("'")[1]

    # NSE/BSE
    span_text = first_result.locator("span").inner_text()

    parts = span_text.split(",")

    nse_code = parts[1].strip()
    bse_code = parts[2].strip()

    print("\nCompany Name:")
    print(company)

    print("\nCompany URL:")
    print(company_url)

    print("\nNSE Code:")
    print(nse_code)

    print("\nBSE Code:")
    print(bse_code)

    browser.close()