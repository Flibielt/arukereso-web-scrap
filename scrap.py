from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
import json
from datetime import datetime

data = []
chrome_options = Options()
chrome_options.add_argument("--headless")

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

driver = webdriver.Chrome(desired_capabilities=caps, options=chrome_options)


def _get_old_prices(product_name, product_type, pid):
    url = "https://www.arukereso.hu/Ajax.GetChartData.php?pt=p&pid=" + str(pid)
    
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    html = html.replace('ak.chart.response = ', '')
    html = html.replace('ak.chart.formatYTick', '""')
    html = html.replace('ak.chart.chartTooltip', '""')
    html = html.replace('ak.chart.formatLabel', '""')
    html = html.replace('ak.chart.formatTitle', '""')
    html = html.replace('ak.chart.buildTooltipBody', '""')

    json_data = json.loads(html)
    avarage_prices = json_data['chartData']['data']['datasets'][1]['data']

    for avarage_price in avarage_prices:
        price = avarage_price['y']
        timestamp = avarage_price['t'] / 1e3
        time = datetime.fromtimestamp(timestamp)

        data.append([product_name, product_type, price, time])


def get_price_history(url):
    product_name = ''
    driver.get(url)

    chart = driver.find_element(By.ID, 'chartnormal')
    pid = chart.get_attribute("data-pid")
    
    name = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[2]/h1')
    product_name = name.text

    product_type_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/a[3]')
    product_type = product_type_element.text

    _get_old_prices(product_name, product_type, pid)


if __name__ == "__main__":
    get_price_history("https://www.arukereso.hu/videokartya-c3142/asus/geforce-gtx-1050-ti-4gb-gddr5-128bit-ph-gtx1050ti-4g-p350966029/")

print(data)

driver.quit()
