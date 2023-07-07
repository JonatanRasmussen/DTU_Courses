from persistence import Persistence
from html_scraper import HtmlScraper

class HtmlManager:
    """ A high-level class that orchestrate the scraping operation
        by managing the html-scraper class that carries out the
        actual scraping. This class organizes the scraped page sources
        into dicts and stores them locally via the persistence class """

    def __init__(self: 'HtmlManager', term: str) -> None:
        """ The HtmlManager is meant to only be instantiated from
            within the class. Instantiate one manager per term """
        self._scraper: 'HtmlScraper' = HtmlScraper()
        self._course_list: list[str] = []
        self._evaluation_dct: dict[str:str] = {}
        self._grades_dct: dict[str:str] = {}
        self._information_dct: dict[str:str] = {}
        self._term: str = term

    @staticmethod
    def scrape_all_term_data(terms: list[str]) -> None:
        """ Iterate over each term and scrape all data related to the
            term. The 'manager' must be reset between each term """
        for term in terms:
            manager: 'HtmlManager' = HtmlManager(term)
            manager.scrape_course_data_for_term()
            manager.store_html()

    def scrape_course_data_for_term(self: 'HtmlManager') -> None:
        """ Iterate over each course for a given term and scrape all
            course-related data (evaluations, grades and information) """
        self._course_list = self._scraper.obtain_course_list(self._term)
        for course in self._course_list:
            self.add_scraped_evaluations_to_dict(course)
            self.add_scraped_grades_to_dict(course)
            self.add_scraped_information_to_dict(course)

    def add_scraped_evaluations_to_dict(self: 'HtmlManager', course: str) -> None:
        """ Obtain page source via href-scraper and add it to dict """
        for course in self._course_list:
            page_source: str = self._scraper.scrape_evaluations(course, self._term)
            self._evaluation_dct[course] = page_source

    def add_scraped_grades_to_dict(self: 'HtmlManager', course: str) -> None:
        """ Obtain page source via href-scraper and add it to dict """
        for course in self._course_list:
            page_source: str = self._scraper.scrape_grades(course, self._term)
            self._evaluation_dct[course] = page_source

    def add_scraped_information_to_dict(self: 'HtmlManager', course: str) -> None:
        """ Obtain page source via href-scraper and add it to dict """
        for course in self._course_list:
            page_source: str = self._scraper.scrape_information(course, self._term)
            self._evaluation_dct[course] = page_source

    def store_html(self: 'HtmlManager') -> None:
        """ Store the scraped html via the persistence class """
        Persistence.store_evaluation_html(self._evaluation_dct, self._term)
        Persistence.store_grade_html(self._evaluation_dct, self._term)
        Persistence.store_information_html(self._evaluation_dct, self._term)

if __name__ == "__main__":
    term_list: list[str] = ['F17', 'E17', 'F23']
    """
                            'F18', 'E18',
                            'F19', 'E19',
                            'F20', 'E20',
                            'F21', 'E21',
                            'F22', 'E22',
                            'F23']
    """
    HtmlManager.scrape_all_term_data(term_list)