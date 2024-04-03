# -*- coding:utf-8 -*-
from seleniumwire import webdriver
from pathlib import Path


class BasePage(object):
    # driver_path = str(Path(__file__).resolve().parent.parent/ 'resources' / 'chromedriver-mac-arm64' / 'chromedriver')
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()

# from selenium.webdriver.chrome.service import Service
# svc = Service(BasePage.driver_path)
# self.driver = webdriver.Chrome(service=svc, options=chrome_options)
##