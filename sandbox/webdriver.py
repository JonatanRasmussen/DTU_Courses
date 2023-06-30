from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

class Webdriver:


    @staticmethod
    def run_webdriver(urls):
        """ Initialize selenium webdriver, access each url in 'urls' list
            and return a list of page sources, then exit webdriver"""
        driver = Webdriver._launch_webdriver()
        list_of_page_sources = []
        if isinstance(urls, str):
            urls = [urls]
        for url in urls:
            page_source = Webdriver._get_page_source(url, driver)
            list_of_page_sources.append(page_source)
        Webdriver._terminate_webdriver(driver)
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
        """Return page source from url. Raise error after 10-second timeout"""
        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "viewport")))
            page_source = driver.page_source
            return page_source
        except TimeoutException:
            raise TimeoutError(f"Timeout exception at url: {url}")


    @staticmethod
    def _terminate_webdriver(driver):
        """Terminate an existing selenium webdriver"""
        driver.quit


    @staticmethod
    def search_for_evaluation_hrefs(course_numbers):
        """ Initialize webdriver, go to url and input a search query, return a
            list of hrefs covering each course evaluation, exit webdriver"""
        driver = Webdriver._launch_webdriver()
        URL = 'https://evaluering.dtu.dk/CourseSearch'
        search_input_box = '//*[@id="CourseCodeTextbox"]'
        search_submit_button = '//*[@id="SearchButton"]'
        list_of_page_sources = []
        for course in course_numbers:
            driver.get(URL)
            driver.find_element(By.XPATH, search_input_box).send_keys(course)
            driver.find_element(By.XPATH, search_submit_button).click()
            page_source = driver.page_source
            list_of_page_sources.append(page_source)
        Webdriver._terminate_webdriver(driver)
        return list_of_page_sources


#%%
"""
if __name__ == "__main__":
    # Quick testing
    course_numbers = ['01005', '02806']
    course_codes = Webdriver.click_elements_with_webdriver(course_numbers)
    print(course_codes)
"""