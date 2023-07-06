from term import Term


class Grades:
    """ A class to handles the relation between DTU's semesters, academic years and exam periods """

    def __init__(self: 'Grades', course_id: str, term: 'Term'):
        """ Calender year is a 4-digit int and semester must be 'E' or 'F' (Efterår / Forår) """
        self._COURSE_ID: str = course_id
        self._TERM: 'Term' = term

    @classmethod
    def in_spring(cls: 'Grades', course_id: str, term: 'Term') -> 'Grades':
        """ Instantiate class as a term of semester type 'F' (Forår) """
        return cls(course_id, term)

    def get_term_name(self: 'Term'):
        """ Return the term in the format 'EXX' or 'FXX', commonly used at DTU.
            If _year is 2018, then 'E' becomes 'E18' and 'F' becomes 'F18' """



if __name__ == "__main__":
    # Test code, remove later
    pass
