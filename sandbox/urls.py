

class Urls:

    def __init__(self, name):
        list_of_urls = []
        self.name = name
        url_hostname = ''
        url_path = ''


    @staticmethod
    def access_hrefs_needed_for_evals(academic_year):
        """Create list of urls to be scraped"""
    # Constants that specifies how Selenium can find the correct elements
        pass

    @staticmethod
    def locate_names(academic_year):
        """Get urls that contain the course list for {academic_year}"""
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z', 'Æ', 'Ø', 'Å']
        urls = []
        for char in alphabet:
            url_hostname = "https://kurser.dtu.dk"
            url_path = f'/archive/{academic_year}/letter/{char}'
            urls.append(url_hostname + url_path)
        return urls

    @staticmethod
    def _convert_term_to_exam_period(term):
        """ Convert each semester in a list to its corresponding exam period,
            'F18' becomes 'Summer-2018', and
            'E20' becomes 'Winter-2020', etc. """
        # F stands for Forår, and "Summer" is the corresponding exam period
        if term[0] == 'F':
            return ('Summer-20'+str(term[-2:]))
        # E stands for Efterår, and "Winter" is the corresponding exam period
        elif term[0] == 'E':
            return ('Winter-20'+str(term[-2:]))
        # Code does not work for terms before 1999
        elif (term[1] == '9') or (term[1] == '8'):
            raise ValueError(f"Error: Second char of {term} is 8 or 9. Term must be 00 or newer")
        # This should never happen
        else:
            raise ValueError(f"Error: First char of {term} should be E or F.")

    @staticmethod
    def locate_grades(course_list, course_term):
        """Get urls that contain grades for all courses in {academic_year}"""
        urls = []
        exam_period = Urls._convert_term_to_exam_period(course_term)
        for course in course_list:
            url_hostname = "https://karakterer.dtu.dk"
            url_path = f'/Histogram/1/{course}/{exam_period}'
            urls.append(url_hostname + url_path)
        return urls