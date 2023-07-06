from bs4 import BeautifulSoup


class HtmlParser:
    """ temp """

    @staticmethod
    def parse_course_archive(page_source: str) -> dict[str,str]:
        """ Extract pairs of course IDs and Names from page source and return them as a dict """
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', {'class': 'table'})
        dct: dict[str,str] = {}
        if table is not None:
            rows = table.find_all('tr')[1:]
            for row in rows:
                course_id: str = row.find('td').text
                course_name: str = row.find_all('td')[1].text
                dct[course_id] = course_name
        sorted_dct: dict[str,str] = {key: dct[key] for key in sorted(dct)}
        return sorted_dct


    @staticmethod
    def parse_evaluations(page_source: str):
        """ temp """
        a = page_source
        b = "ø"
        return a+b

    @staticmethod
    def parse_grades(page_source: str) -> dict[str,int]:
        """ temp """
        a = page_source
        b = "ø"
        return a+b

    @staticmethod
    def parse_search_for_evaluation_urls(page_source: str):
        """ Extract and return a dict of each semester and the url pointing to its evaluations """
        soup = BeautifulSoup(page_source, 'html.parser')
        div_elements = soup.find_all('div', class_='Term')
        dct: dict[str,str] = {}
        for div_element in div_elements:
            term: str = div_element.text.strip()
            if term != "Semester": #The Semester-key has a NoneType parent
                href: str = div_element.find_parent('a')['href']
                dct[term] = href
        formatted_dct: dict[str,str] = HtmlParser._format_evaluation_urls(dct)
        return formatted_dct

    @staticmethod
    def _format_evaluation_urls(dct: dict[str,str]):
        """ SHOULD ONLY BE USED BY parse_pagination_to_evaluations() 
            Performs the following formatting:
            'E-18-13': '/kursus/01005/168580'
            'E18': '168580' """
        formatted_dct: dict[str,str] = {}
        for key, value in dct.items():
            formatted_key: str = key.replace('-', "")[:3] #Format 'E-18-13' to 'E18'
            formatted_value: str = value.split('/')[-1] #Format '/kursus/01005/168580' to '168580'
            formatted_dct[formatted_key] = formatted_value
        #formatted_dct = {key.replace('-',"")[:3]+'_'+value.spl
        #it('/')[-2]: value.split('/')[-1] for key, value in dct.items()}
        return formatted_dct
