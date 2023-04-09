from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

class Scrape:

    @staticmethod
    def run_webdriver(urls):
        driver = Scrape._launch_webdriver()
        list_of_page_sources = []
        for url in urls:
            page_source = Scrape._get_page_source(url, driver)
            list_of_page_sources.append(page_source)
        Scrape._terminate_webdriver(driver)
        return list_of_page_sources

    @staticmethod
    def _launch_webdriver():
        """Initialize selenium webdriver and return driver"""
        options = Options()
        options.add_argument("--log-level=3")
        options.add_argument('--disable-logging')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    @staticmethod
    def _get_page_source(url, driver):
        """Return page source from url. Return None if 10-second timeout"""
        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "viewport")))
            page_source = driver.page_source
            return page_source
        except TimeoutException:
            message = f"{''}, Timeout exception at url: {url}"
            return None

    @staticmethod
    def _terminate_webdriver(driver):
        """Terminate an existing selenium webdriver"""
        driver.quit
