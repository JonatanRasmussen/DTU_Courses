from bs4 import BeautifulSoup

class HttpParser:

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