This file takes data from **nseindia.com** and formats it to print the option chain data of the 10 nearest strike prices.

Issues - 
  1. Hardcode edgeDriver file location
  2. needs an edgeDriver / chromeDriver to function
  3. request may sometimes be denied

The file **main.py** is the head running the functions from nse_scraper.py

It uses the library **selenium** to get data from **nseindia.com**

This requires:
  1. Selenium
  2. PrettyTable (for formatting the data)
  3. edgedriver / chromedriver needed to make nse accept the request

