

class Term:
    """ A class to handles the relation between DTU's semesters, academic years and exam periods """

    def __init__(self: 'Term', calender_year: int, dtu_semester: str):
        """ Calender year is a 4-digit int and semester must be 'E' or 'F' (Efterår / Forår) """
        self._YEAR: int = calender_year
        self._SEMESTER: str = dtu_semester
        self._validate_term()

    @classmethod
    def in_autumn(cls: 'Term', calender_year: int) -> 'Term':
        """ Instantiate class as a term of semester type 'E' (Efterår) """
        return cls(calender_year, 'E')

    @classmethod
    def in_spring(cls: 'Term', calender_year: int) -> 'Term':
        """ Instantiate class as a term of semester type 'F' (Forår) """
        return cls(calender_year, 'F')

    def get_term_name(self: 'Term'):
        """ Return the term in the format 'EXX' or 'FXX', commonly used at DTU.
            If _year is 2018, then 'E' becomes 'E18' and 'F' becomes 'F18' """
        YEAR_LOWER_BOUND: int = 2000
        if self._YEAR > YEAR_LOWER_BOUND:
            return f'{self._SEMESTER}{self._YEAR-2000}'
        else:
            raise ValueError(f"Error: Invalid year, {self._YEAR} is older than {YEAR_LOWER_BOUND}")

    def get_exam_period(self: 'Term'):
        """ Return the terms corresponding exam period.
            If _year is 2018, then 'E' becomes 'Winter-2018' and 'F' becomes 'Summer-2018' """
        if self._SEMESTER == 'E':
            return f'Winter-{self._YEAR}'
        elif self._SEMESTER == 'F':
            return f'Summer-{self._YEAR}'
        else:  # This should never happen
            raise ValueError("Error: Invalid semester")

    def get_academic_year(self: 'Term'):
        """ Return the academic year that the term belongs to.
            If _year is 2018, then 'E' becomes '2018-2019' and 'F' becomes '2017-2018' """
        if self._SEMESTER == 'E':
            return f'{self._YEAR}-{1 + self._YEAR}'
        elif self._SEMESTER == 'F':
            return f'{self._YEAR - 1}-{self._YEAR}'
        else:  # This should never happen
            raise ValueError("Error: Invalid semester")

    @staticmethod
    def convert_term_names_to_academic_years(terms: set['Term']) -> set[str]:
        """ Apply get_academic_year() on an entire set of Term objects """
        academic_years: set[str] = set()
        for term in terms:
            academic_years.add(term.get_academic_year())
        return academic_years

    def _validate_term(self: 'Term'):
        """ Ensure that the term is instantiated with a valid year and semester """
        self._validate_year()
        self._validate_semester()

    def _validate_year(self: 'Term'):
        """ Ensure that the term is instantiated with a supported year """
        LOWER_BOUND: int = 2000 # Years 19XX break the shortened names E16 / F18 / E21 / F23 / etc.
        UPPER_BOUND: int = 2059 # 2060 and 1960 might collide when shortened to F60 or E60
        if (self._YEAR < LOWER_BOUND) or (self._YEAR > UPPER_BOUND):
            raise ValueError(f"Error: Invalid year, {self._YEAR} is not supported. "+
                              "Please choose a year within the following bounds: "+
                             f"{LOWER_BOUND} - {UPPER_BOUND}")

    def _validate_semester(self: 'Term'):
        """ Ensure that the term is instantiated with a supported semester """
        SUPPORTED_SEMESTERS: set[str] = {'E', 'F'}
        if self._SEMESTER not in SUPPORTED_SEMESTERS:
            raise ValueError(f"Error: Invalid value, {self._SEMESTER} is not supported. "+
                              "Please set the semester as one of the following values: "+
                             f"{SUPPORTED_SEMESTERS}")


if __name__ == "__main__":
    # Test code, remove later
    my_term = Term(2020, 'E')
    my_new_term = Term(2011, 'F')
    print(my_term.get_term_name())
    print(my_term.get_exam_period())
    print(my_term.get_academic_year())
    Term.convert_term_names_to_academic_years({my_term, my_new_term})
    #my_fake_term = Term(30, 'G')
