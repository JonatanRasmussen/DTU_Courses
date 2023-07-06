from web_scraping_tool import WebScrapingTool
from url_locator import UrlLocator
from term import Term

class DataExtractor:
    """ Scrape a given url via chrome driver. Its methods return unparsed page sources """

    def __init__(self: 'DataExtractor'):
        """ It takes time to locate the url that contains evaluation data for a course
            To avoid duplicate lookups, previously located urls will be stored in a dict """
        self._evaluation_urls: dict[str,dict[str,str]] = {}
        self._scrape_tool: 'WebScrapingTool' = WebScrapingTool()

    def access_course_archive(self: 'DataExtractor', term: 'Term') -> str:
        """ Loop over each of the pagesources that contain a table
            of course number and titles, and then combine the scraped
            course number - course name pairs into a single dct """
        page_source: str = ""
        urls: list[str] = UrlLocator.locate_course_archive(term)
        for url in urls:
            page_source += self._scrape_tool.get_page_source(url)
        return page_source

    def access_evaluations(self: 'DataExtractor', course_id: str, term: 'Term') -> str:
        """ Given a course and semester, access its evaluations and scrape the page source """
        urls: dict[str,str] = self._get_evaluation_url(course_id)
        if term.get_term_name() in urls:
            url: str = urls[term.get_term_name()]
            page_source: str = self._scrape_tool.get_page_source(url)
            return page_source
        else:
            return ""

    def access_grades(self: 'DataExtractor', course_id: str, term: 'Term') -> str:
        """ Given a course and semester, access its grades and scrape the page source """
        url: str = UrlLocator.locate_grades(course_id, term)
        page_source = self._scrape_tool.get_page_source(url)
        return page_source

    def access_information(self: 'DataExtractor', course_id: str, term: 'Term') -> str:
        """ Given a course and year, access it via the course base and scrape its page source """
        url: str = UrlLocator.locate_information(course_id, term)
        page_source = self._scrape_tool.get_page_source(url)
        return page_source

    def _access_href_digits(self: 'DataExtractor', course_id: str) -> str:
        """ The evaluation urls can't be generated, they must be scraped 
            This method scrapes the href_digits needed to generate the urls """
        page_source = self._scrape_tool.paginate_to_evaluation_hrefs(course_id)
        return page_source

    def _get_evaluation_url(self: 'DataExtractor', course_id: str) -> dict[str,str]:
        """ Returns a dict containing evaluation urls. Scrape it if it hasn't already been done """
        dct = self._evaluation_urls
        if course_id in dct:
            urls: dict[str,str] = dct[course_id]
        else:
            href_page_source = self._access_href_digits(course_id)
            urls: dict[str,str] = UrlLocator.locate_evaluations(course_id, href_page_source)
            self._evaluation_urls[course_id] = urls
        return urls

#%%
if __name__ == "__main__":
    # Quick testing
    #academic_year = '2021-2022'
    #course_codes = Scrapes.get_names(academic_year)
    #print(course_codes)

    # Test 2
    #hrefs = Scrapes.get_hrefs(['01005','02806'])
    #print(hrefs)

    # Test 3
    testy = DataExtractor()
    E20 = Term.in_autumn(2020)
    F20 = Term.in_spring(2020)
    E21 = Term.in_autumn(2021)
    F21 = Term.in_spring(2021)
    c02402 = "02402"
    c01015 = "01015"
    my_ps = testy.access_evaluations(c02402, E20)
    my_ps = testy.access_evaluations(c02402, E21)
    my_ps = testy.access_evaluations(c02402, F20)
    my_ps = testy.access_evaluations(c01015, F21)
    my_ps = testy.access_evaluations(c01015, E20)
    my_ps = testy.access_evaluations(c02402, F21)
    print('done')
