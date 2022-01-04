from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
import json
from datetime import datetime

chrome_options = Options()
chrome_options.add_argument("--headless")

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

driver = webdriver.Chrome(desired_capabilities=caps, options=chrome_options)


def _get_old_prices(pid):
    url = "https://www.arukereso.hu/Ajax.GetChartData.php?pt=p&pid=" + str(pid)
    print(url)
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    html = html.replace('ak.chart.response = ', '')
    html = html.replace('ak.chart.formatYTick', '""')
    html = html.replace('ak.chart.chartTooltip', '""')
    html = html.replace('ak.chart.formatLabel', '""')
    html = html.replace('ak.chart.formatTitle', '""')
    html = html.replace('ak.chart.buildTooltipBody', '""')

    data = json.loads(html)
    print(data['chartData']['data']['datasets'][1]['data'])

    return html


def get_price_history(product_name, url):
    print(product_name)
    driver.get(url)

    chart = driver.find_element(By.ID, 'chartnormal')
    pid = chart.get_attribute("data-pid")
    print(pid)
    _get_old_prices(pid)


if __name__ == "__main__":
    get_price_history("GTX1050ti", "https://www.arukereso.hu/videokartya-c3142/asus/geforce-gtx-1050-ti-4gb-gddr5-128bit-ph-gtx1050ti-4g-p350966029/")

driver.quit()
