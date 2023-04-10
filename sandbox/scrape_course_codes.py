from bs4 import BeautifulSoup

from webdriver import Webdriver

class ScrapeCourseCodes:

    @staticmethod
    def get(academic_year):
        list_of_urls = ScrapeCourseCodes._create_list_of_urls(academic_year)
        list_of_page_sources = Webdriver.run_webdriver(list_of_urls)
        course_codes = []
        for page_source in list_of_page_sources:
            extracted_course_codes = ScrapeCourseCodes._extract_course_codes(page_source)
            course_codes.append(extracted_course_codes)
        return course_codes.sort()

    @staticmethod
    def _create_list_of_urls(academic_year):
        """Create list of urls to be scraped"""
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z', 'Æ', 'Ø', 'Å']
        urls = []
        for letter in alphabet:
            url_hostname = "https://kurser.dtu.dk"
            url_path = f'/archive/{academic_year}/letter/{letter}'
            urls.append(url_hostname + url_path)
        return urls

    @staticmethod
    def _extract_course_codes(page_source):
        """Extract course codes from page source and return them as a list"""
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', {'class': 'table'})
        course_codes = []
        course_dict = {}
        if table != None:
            rows = table.find_all('tr')[1:]
            for row in rows:
                course_code = row.find('td').text
                course_title = row.find_all('td')[1].text
                course_dict[course_code] = course_title
                course_codes.append(course_code)
        return course_codes


#%%
if __name__ == "__main__":
    # Testing
    ScrapeCourseCodes.get('2022-2023')