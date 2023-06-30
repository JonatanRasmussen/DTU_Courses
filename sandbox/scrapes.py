from bs4 import BeautifulSoup

from webdriver import Webdriver
from urls import Urls

class Scrapes:

    @staticmethod
    def get_names(academic_year):
        """ Loop over each of the pagesources that contain a table
            of course number and titles, and then combine the scraped
            course number - course name pairs into a single dct"""
        list_of_urls = Urls.locate_names(academic_year)
        list_of_page_sources = Webdriver.run_webdriver(list_of_urls)
        course_names = {}
        for page_source in list_of_page_sources:
            course_names.update(Scrapes._scrape_names(page_source))
        sorted_course_names = {key: course_names[key] for key in sorted(course_names)}
        return sorted_course_names

    @staticmethod
    def get_hrefs(course_numbers):
        """ Loop over each of the pagesources that contain a table
            of course number and titles, and then combine the scraped
            course number - course name pairs into a single dct"""
        list_of_page_sources = Webdriver.search_for_evaluation_hrefs(course_numbers)
        hrefs = {}
        for page_source in list_of_page_sources:
            hrefs.update(Scrapes._scrape_hrefs_needed_for_evals(page_source))
        # Format from "'E-18-13': '/kursus/01005/168580'" to "'E18_01005': '168580'"
        formatted_hrefs = {key.replace('-',"")[:3]+'_'+value.split('/')[-2]: value.split('/')[-1] for key, value in hrefs.items()}
        return formatted_hrefs

    @staticmethod
    def get_grades(course_numbers, course_term):
        """ Loop over each of the pagesources that contain a table
            of course number and titles, and then combine the scraped
            course number - course name pairs into a single dct"""
        list_of_urls = Urls.locate_names(course_numbers, course_term)
        list_of_page_sources = Webdriver.run_webdriver(list_of_urls)
        pass


    @staticmethod
    def _scrape_grades(page_source):
        """Create list of urls to be scraped"""
        pass

    @staticmethod
    def _scrape_hrefs_needed_for_evals(page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        div_elements = soup.find_all('div', class_='Term')
        hrefs = {}
        for div_element in div_elements:
            term = div_element.text.strip()
            if term != "Semester": #The Semester-key has a NoneType parent
                href = div_element.find_parent('a')['href']
                hrefs[term] = href
        return hrefs

    @staticmethod
    def _scrape_names(page_source):
        """Extract course codes from page source and return them as a list"""
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', {'class': 'table'})
        course_names = {}
        if table != None:
            rows = table.find_all('tr')[1:]
            for row in rows:
                course_number = row.find('td').text
                course_title = row.find_all('td')[1].text
                course_names[course_number] = course_title
        return course_names


#%%
if __name__ == "__main__":
    pass
    # Quick testing
    #academic_year = '2021-2022'
    #course_codes = Scrapes.get_names(academic_year)
    #print(course_codes)

    # Test 2
    #hrefs = Scrapes.get_hrefs(['01005','02806'])
    #print(hrefs)