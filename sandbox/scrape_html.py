from abc import ABC, abstractmethod


class ScrapeHtml(ABC):
    """ Abstract class for webscraping, parsing and storing html """

    @abstractmethod
    def run_code(self: 'ScrapeHtml', hey: str) -> list:
        """ Run all methods in this class, performing the following actions: 
            1) Locate the html
            2) Scrape the html
            3) Parse the html
            4) Save the html """

    @abstractmethod
    def _locate(self: 'ScrapeHtml', time_period: str) -> set[str]:
        """ Generate a set of urls that the scraping tool should access 
            Input: A time period (custom class) 
            Output: A set of urls (a Set containing Strings)"""

    @abstractmethod
    def _scrape(self: 'ScrapeHtml', urls: str) -> list:
        """ Return a set of urls to be accessed
            Input: A time period (custom class) 
            Output: A set of urls (a Set containing Strings)"""

    @abstractmethod
    def _parse(self: 'ScrapeHtml', page_source):
        """ temp """

    @abstractmethod
    def _save(self: 'ScrapeHtml'):
        """ Locally store the html """
