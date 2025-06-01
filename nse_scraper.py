# nse_scraper.py
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.edge.service import Service 
from selenium.webdriver.edge.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
import time

# 💻 Get necessary headers and cookies using Selenium

def get_headers_and_cookies(edge_driver_path: str):
    options = Options()
    # options.add_argument("--headless")  # Uncomment to run silently 😶‍🌫️
    service = Service(edge_driver_path)
    driver = webdriver.Edge(service=service, options=options)

    try:
        driver.get("https://www.nseindia.com/get-quotes/derivatives?symbol=NIFTY")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        selenium_cookies = driver.get_cookies()
        cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
    finally:
        driver.quit()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/get-quotes/derivatives?symbol=NIFTY",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest"
    }

    return headers, cookies

# 📊 Get the NIFTY underlying value

def get_underlying_value(headers, cookies):
    nifty_url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY 50"
    response = requests.get(nifty_url, headers=headers, cookies=cookies)
    response.raise_for_status()
    nifty_data = response.json()
    return nifty_data['data'][0]['lastPrice']

# 📦 Fetch the option chain data

def get_option_chain(headers, cookies):
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
    response.raise_for_status()
    return response.json()

# 🎨 Print the option chain in a table that makes Wall Street jealous

def print_option_table(option_data, underlying_value):
    table = PrettyTable()
    table.field_names = [
    "Calls OI", "Calls OI Chg%", "Calls Vol", "Calls LTP", "Calls LTP Chg%",
    "Strike Price",
    "Puts LTP", "Puts Vol", "Puts OI Chg%", "Puts OI"
    ]


    # Sort option data by proximity to underlying value for better readability
    sorted_data = sorted(
        option_data,
        key=lambda x: abs(x.get("strikePrice", 0) - underlying_value)
    )[:10]  # Just top 10 closest for that classy touch 🕶️

    for entry in sorted_data:
        ce = entry.get("CE", {})
        pe = entry.get("PE", {})

        table.add_row([
            f"{ce.get('openInterest', '-')}",
            f"{ce.get('changeinOpenInterest', '-')}",
            f"{ce.get('totalTradedVolume', '-')}",
            f"{ce.get('lastPrice', '-')}",
            f"{ce.get('change', '-')}",

            entry.get("strikePrice", "-"),

            f"{pe.get('lastPrice', '-')}",
            f"{pe.get('totalTradedVolume', '-')}",
            f"{pe.get('changeinOpenInterest', '-')}",
            f"{pe.get('openInterest', '-')}",
        ])

    print("\n🪙 NSE Nifty Option Chain Snapshot")
    print(f"📈 Underlying Index Value: {underlying_value}\n")
    print(table)
