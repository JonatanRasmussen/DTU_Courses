class Urls:

    def __init__(self, name):
        list_of_urls = []
        self.name = name
        url_hostname = ''
        url_path = ''

    @staticmethod
    def course_code_urls(academic_year):
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
    def course_code_urls(academic_year):
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
    def course_code_urls(course_list, exam_period):
        urls = []
        for course in course_list:
            url_hostname = "https://karakterer.dtu.dk"
            url_path = f'/Histogram/1/{course}/{exam_period}'
            urls.append(url_hostname + url_path)

    def exam_period_from_semester(course_semesters):
        """ Convert each semester in a list to its corresponding exam period,
            'F18' becomes 'Summer-2018', and
            'E20' becomes 'Winter-2020', etc. """
        exam_periods = []
        for semester in course_semesters:
            # F stands for Forår, and "Summer" is the corresponding exam period
            if semester[0] == 'F':
                exam_periods.append('Summer-20'+str(semester[-2:]))
            # E stands for Efterår, and "Winter" is the corresponding exam period
            elif semester[0] == 'E':
                exam_periods.append('Winter-20'+str(semester[-2:]))
            # This should never happen
            else:
                exam_periods.append('XXXXXX-20'+str(semester[-2:]))
                message = f"{file_name}: Invalid semester: {course_semesters}"
                Utils.logger(message, "Error", FileNameConsts.scrape_log_name)