# pip install selenium selenium-wire webdriver-manager fake-useragent

import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver as wiredriver
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
# options.add_argument("--headless")
options.add_argument("--incognito")
options.add_argument("--nogpu")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--enable-javascript")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)


def get_free_proxies():
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://sslproxies.org")

    table = driver.find_element(By.TAG_NAME, "table")
    thead = table.find_element(By.TAG_NAME, "thead").find_elements(By.TAG_NAME, "th")
    tbody = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

    headers = []
    for th in thead:
        headers.append(th.text.strip())

    proxies = []
    for tr in tbody:
        proxy_data = {}
        tds = tr.find_elements(By.TAG_NAME, "td")
        for i in range(len(headers)):
            proxy_data[headers[i]] = tds[i].text.strip()
        proxies.append(proxy_data)
    driver.quit()
    return proxies


def get_watch(proxies):
    ua = UserAgent()
    userAgent = ua.random
    market_data = {}
    competidor_names = []
    performance = {}
    url = "https://www.marketwatch.com/investing/stock/aapl"
    for proxy in proxies:
        proxy_url = f"http://{proxy['IP Address']}:{proxy['Port']}"
        print(proxy_url)
        seleniumwire_options = {
            "proxy": {"http": proxy_url, "https": proxy_url},
        }
        driver = wiredriver.Chrome(
            service=service,
            # seleniumwire_options=seleniumwire_options,
            options=options,
        )

        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": userAgent})
        try:
            driver.get(url)
            time.sleep(5)
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        ('//*[@id="maincontent"]/div[6]/div[3]/div/div/table/tbody'),
                    )
                )
            )
            competidor_table = driver.find_element(
                by=By.XPATH,
                value='//*[@id="maincontent"]/div[6]/div[3]/div/div/table',
            )
            tbody = competidor_table.find_element(By.TAG_NAME, "tbody").find_elements(
                By.TAG_NAME, "tr"
            )
            for tr in tbody:
                competidor = tr.find_element(By.CLASS_NAME, "link")
                competidor_name = competidor.text.strip()
                print(competidor_name)
                competidor_names.append(competidor_name)
            print(competidor_names)
            market_data["competidors"] = competidor_names

            performance_table = driver.find_element(
                by=By.XPATH,
                value='//*[@id="maincontent"]/div[6]/div[1]/div[2]/div[1]/table',
            )
            performance_tbody = performance_table.find_element(
                By.TAG_NAME, "tbody"
            ).find_elements(By.TAG_NAME, "tr")
            for tr in performance_tbody:
                cells = tr.find_elements(By.TAG_NAME, "td")
                key = cells[0].text.strip()
                cell_value = (
                    cells[1]
                    .find_element(By.TAG_NAME, "ul")
                    .find_elements(By.TAG_NAME, "li")
                )
                value = cell_value[0].text.strip()
                performance[key] = value
            print(performance)
            market_data["performance"] = performance
            maket_cap_data = driver.find_element(
                By.XPATH, "/html/body/div[4]/div[6]/div[1]/div[1]/div/ul/li[4]/span[1]"
            )
            market_cap_value = maket_cap_data.text.split()
            market_data["market_cap"] = market_cap_value
            driver.close()
            break
        except Exception as e:
            print(e)
            driver.close()
    return market_data


if __name__ == "__main__":  # noqa
    try:
        free_proxies = get_free_proxies()
        competidors = get_watch(free_proxies)
        print(competidors)
    except Exception as e:
        print(e)
