from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class WebScrapingTool:
    """ Return page_source from target url via Selenium Webdriver """

    def __init__(self: 'WebScrapingTool'):
        """ temp """
        self._driver: type[WebDriver] = self._launch_webdriver()
        self._is_running: bool = True

    def _launch_webdriver(self) -> type[WebDriver]:
        """Initialize selenium webdriver and return driver"""
        service: type[Service] = Service(ChromeDriverManager().install())
        options: type[Options] = Options()
        options.add_argument("--log-level=3")
        options.add_argument('--disable-logging')
        driver: type[WebDriver] = webdriver.Chrome(service=service, options=options)
        return driver

    def terminate_webdriver(self: 'WebScrapingTool'):
        """Terminate an existing selenium webdriver"""
        self._driver.quit()
        self._is_running = False

    def get_page_source(self: 'WebScrapingTool', url: str) -> str:
        """Return page source from url. Raise error after 10-second timeout"""
        driver: type[WebDriver] = self._driver
        driver.get(url)
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, "viewport")))
            page_source: str = driver.page_source
            return page_source
        except TimeoutException as exc:
            return ""
            #raise TimeoutError(f"Timeout exception at url: {url}") from exc


    def paginate_to_evaluation_hrefs(self, course_id: str) -> str:
        """ Unique pagination required to obtain urls for Evaluation data """
        driver: type[WebDriver] = self._driver
        URL = 'https://evaluering.dtu.dk/CourseSearch'
        SEARCH_INPUT_BOX = '//*[@id="CourseCodeTextbox"]'
        SEARCH_SUBMIT_BUTTON = '//*[@id="SearchButton"]'
        driver.get(URL)
        driver.find_element(By.XPATH, SEARCH_INPUT_BOX).send_keys(course_id)
        driver.find_element(By.XPATH, SEARCH_SUBMIT_BUTTON).click()
        page_source: str =  driver.page_source
        return page_source

#%%

if __name__ == "__main__":
    # Test code, remove later
    my_scraping_tool = WebScrapingTool()
    source_a = my_scraping_tool.get_page_source("https://kurser.dtu.dk/archive/2019-2020/letter/A")
    source_b = my_scraping_tool.paginate_to_evaluation_hrefs('01005')
    my_scraping_tool.terminate_webdriver()
    print(len(source_a))
    print(len(source_b))
