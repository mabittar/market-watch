# pip install selenium selenium-wire webdriver-manager fake-useragent

# import time

# from fake_useragent import UserAgent
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from seleniumwire import webdriver as wiredriver
# from webdriver_manager.chrome import ChromeDriverManager

# service = Service(ChromeDriverManager().install())
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--incognito")
# options.add_argument("--nogpu")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("--enable-javascript")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option("useAutomationExtension", False)


# def get_watch(stock_symbol: str) -> dict:
#     ua = UserAgent()
#     userAgent = ua.random
#     market_data = {}
#     competitor_names = []
#     performance = {}
#     url = f"https://www.marketwatch.com/investing/stock/{stock_symbol}"
#     driver = wiredriver.Chrome(
#         service=service,
#         options=options,
#     )

#     driver.execute_script(
#         "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
#     )
#     driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": userAgent})
#     try:
#         driver.get(url)
#         time.sleep(5)
#         WebDriverWait(driver, 20).until(
#             EC.visibility_of_element_located(
#                 (
#                     By.XPATH,
#                     ('//*[@id="maincontent"]/div[6]/div[3]/div/div/table/tbody'),
#                 )
#             )
#         )
#         competidor_table = driver.find_element(
#             by=By.XPATH,
#             value='//*[@id="maincontent"]/div[6]/div[3]/div/div/table',
#         )
#         tbody = competidor_table.find_element(By.TAG_NAME, "tbody").find_elements(
#             By.TAG_NAME, "tr"
#         )
#         for tr in tbody:
#             competitor = tr.find_element(By.CLASS_NAME, "link")
#             competitor_name = competitor.text.strip()
#             print(competitor_name)
#             competitor_names.append(competitor_name)
#         market_data["competitors"] = competitor_names

#         performance_table = driver.find_element(
#             by=By.XPATH,
#             value='//*[@id="maincontent"]/div[6]/div[1]/div[2]/div[1]/table',
#         )
#         performance_tbody = performance_table.find_element(
#             By.TAG_NAME, "tbody"
#         ).find_elements(By.TAG_NAME, "tr")
#         for tr in performance_tbody:
#             cells = tr.find_elements(By.TAG_NAME, "td")
#             key = cells[0].text.strip()
#             cell_value = (
#                 cells[1]
#                 .find_element(By.TAG_NAME, "ul")
#                 .find_elements(By.TAG_NAME, "li")
#             )
#             value = cell_value[0].text.strip()
#             performance[key] = value
#         market_data["performance"] = performance
#         maket_cap_data = driver.find_element(
#             By.XPATH, "/html/body/div[4]/div[6]/div[1]/div[1]/div/ul/li[4]/span[1]"
#         )
#         market_cap_value = maket_cap_data.text.split()
#         market_data["market_cap"] = market_cap_value
#         cmp_data = driver.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div[2]/div/div[2]/h1')
#         market_data["company_name"] = cmp_data.text.split()
#         driver.close()
#     except Exception as e:
#         print(e)
#         driver.close()
#     return market_data


fakedata = {
    "competitors": [
        "Microsoft Corp.",
        "Alphabet Inc. Cl C",
        "Alphabet Inc. Cl A",
        "Amazon.com Inc.",
        "Meta Platforms Inc.",
        "Samsung Electronics Co. Ltd.",
        "Samsung Electronics Co. Ltd. Pfd. Series 1",
        "Sony Group Corp.",
        "Dell Technologies Inc. Cl C",
        "HP Inc.",
    ],
    "performance": {
        "5 Day": "-1.65%",
        "1 Month": "-6.20%",
        "3 Month": "18.13%",
        "YTD": "12.31%",
        "1 Year": "21.63%",
    },
    "market_cap": "$3.29T",
    "company_name": 'Apple Inc.'
}


class MarketWatchClient:
    def get_maktet_data(self, stock_symbol: str) -> dict:
        print(f"fake_data for: {stock_symbol}")
        return fakedata


if __name__ == "__main__":  # noqa
    try:
        data = MarketWatchClient().get_maktet_data("AAPL")
        print(data)
    except Exception as e:
        print(e)
