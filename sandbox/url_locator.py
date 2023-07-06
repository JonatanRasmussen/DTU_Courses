from html_parser import HtmlParser
from term import Term



class UrlLocator:
    """ Get the urls where grades, evaluations and information are stored for DTU courses """

    @staticmethod
    def locate_course_archive(term: 'Term') -> list[str]:
        """ Get a list of urls that covers the full course archive for a given school year.
            The complete course list is split across several urls, one for each starting letter:
            https://kurser.dtu.dk/archive/2022-2023/letter/A
            https://kurser.dtu.dk/archive/2022-2023/letter/B
            ...
            https://kurser.dtu.dk/archive/2022-2023/letter/Z.
            The complete course list for a given year is obtained by accessing each letter """
        URL_HOSTNAME: str = "https://kurser.dtu.dk"
        ALPHABET: tuple[str] = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                                'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                                'U', 'V', 'W', 'X', 'Y', 'Z', 'Æ', 'Ø', 'Å')
        academic_year: str = term.get_academic_year()
        urls: list[str] = []
        for char in ALPHABET:
            url_path: str = f'/archive/{academic_year}/letter/{char}'
            urls.append(URL_HOSTNAME + url_path)
        return urls

    @staticmethod
    def locate_evaluations(course_id: str, page_source: 'str') -> dict[str:str]:
        """ Uniquely, the evaluation urls can't be generated; they must be scraped instead. 
            Each scrape returns multiple urls, which is why this method returns a dict of urls """
        URL_HOSTNAME: str = "https://evaluering.dtu.dk"
        href_digits_dct: dict[str:str] = HtmlParser.parse_search_for_evaluation_urls(page_source)
        urls: dict[str:str] = {}
        for semester, href_digits in href_digits_dct.items():
            url_path: str = f'/kursus/{course_id}/{href_digits}'
            urls[semester] = URL_HOSTNAME + url_path
        return urls

    @staticmethod
    def locate_grades(course_id: str, term: 'Term') -> str:
        """ Given a course and semester, generate the url for the corresponding grades """
        exam_period: str = term.get_exam_period()
        URL_HOSTNAME = "https://karakterer.dtu.dk"
        url_path = f'/Histogram/1/{course_id}/{exam_period}'
        return URL_HOSTNAME + url_path

    @staticmethod
    def locate_information(course_id: str, term: 'Term') -> str:
        """ Given a course and academic year, generate the url for its course base page """
        academic_year: str = term.get_academic_year()
        URL_HOSTNAME = "https://kurser.dtu.dk"
        url_path = f'/course/{academic_year}/{course_id}'
        return URL_HOSTNAME + url_path
