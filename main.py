from nse_scraper import *  #type: ignore

edgeDriver = "C:/Users/ADMIN/Downloads/edgedriver_win64/msedgedriver.exe"

headers, cookies = get_headers_and_cookies(edgeDriver)

underlyingValue = get_underlying_value(headers, cookies) 

optionData = get_option_chain(headers, cookies)
strike_data = optionData['records']['data']


print_option_table(strike_data, underlyingValue)

