from grade import Grade

class GradeSheet:
    """ Grade distribution across DTU's different types of grades """

    def __init__(self: 'GradeSheet', course: str, term: str) -> 'GradeSheet':
        """ Instantiate each grade used at DTU """
        self.grade_types: dict[str:str] = {}
        self._course: str = course
        self._term: str = term

        # Numeric grades (seven-step scale)
        self._grade_dct: dict[str:int] = {}
        self._grade_12: 'Grade' = Grade.create_passed('12', 12)
        self._grade_10: 'Grade' = Grade.create_passed('12', 12)
        self._grade_7: 'Grade' = Grade.create_passed('12', 12)
        self._grade_4: 'Grade' = Grade.create_passed('12', 12)
        self._grade_02: 'Grade' = Grade.create_passed('12', 12)
        self._grade_00: 'Grade' = Grade.create_attended_but_failed('00', 0)
        self._grade_minus_3: 'Grade' = Grade.create_attended_but_failed('minus_3', -3)
        # Non-numeric grades (Custom grades used at DTU)
        self._grade_pass: 'Grade' = Grade.create_passed('pass', None)
        self._grade_fail: 'Grade' = Grade.create_attended_but_failed('fail', None)
        self._grade_not_met: 'Grade' = Grade.create_absent('absent')
        self._grade_ill: 'Grade' = Grade.create_absent('ill')
        self._grade_not_approved: 'Grade' = Grade.create_absent('not_approved')

        self._grades: list['Grade'] = [self._grade_12,
                                       self._grade_10,
                                       self._grade_7,
                                       self._grade_4,
                                       self._grade_02,
                                       self._grade_00,
                                       self._grade_minus_3,
                                       self._grade_pass,
                                       self._grade_fail,
                                       self._grade_not_met,
                                       self._grade_ill,
                                       self._grade_not_approved,]

    @staticmethod
    def instantiate_dtu_grades() -> list['Grade']:
        """ Instantiate a list containing each grade used at DTU """
        dtu_grades: list['Grade'] = []
        # Numeric grades (seven-step scale)
        dtu_grades.append(Grade.create_passed('12', 12))
        dtu_grades.append(Grade.create_passed('10', 10))
        dtu_grades.append(Grade.create_passed('7', 7))
        dtu_grades.append(Grade.create_passed('4', 4))
        dtu_grades.append(Grade.create_passed('02', 2))
        dtu_grades.append(Grade.create_attended_but_failed('00', 0))
        dtu_grades.append(Grade.create_attended_but_failed('minus_3', -3))
        # Non-numeric grades (Custom grades used at DTU)
        dtu_grades.append(Grade.create_passed('pass', None))
        dtu_grades.append(Grade.create_attended_but_failed('fail', None))
        dtu_grades.append(Grade.create_absent('absent'))
        dtu_grades.append(Grade.create_absent('ill'))
        dtu_grades.append(Grade.create_absent('not_approved'))
        return dtu_grades

    def calculate_average(self: 'GradeSheet') -> float | None:
        """ Calculate the mean of the numeric grades
            Return 'None' if there are no numeric grades """
        count: int = 0
        weighted_sum: int = 0
        for grade in self._grades:
            if grade.is_numeric():
                count += grade.get_quantity() 
                weighted_sum += grade.get_quantity() * grade.get_weight()
        if len(count) == 0:
            return None
        else:
            average: float = weighted_sum / len(count)
            return average
        
    def count_grades(self: 'GradeSheet') -> int:
        """ Count the total number of grades on the grade sheet """
        count: int = 0
        for grade in self._grades:
            count += grade.get_quantity()
        return count 

    '''def match_condition(self: 'GradeSheet', condition: any) -> int:
        """ Return the grades that are 'True' for the given condition """
        grade_list: list['Grade'] = []
        for grade in self._grades:
            if getattr(grade, condition):
                grade_list.append(grade)
        return grade_list    ''' 

    def convert_names_from_dtu_website_format(self):
        self.grade_types = {
            "12": "GRADE_12",
            "10": "GRADE_10",
            "7": "GRADE_7",
            "4": "GRADE_4",
            "02": "GRADE_02",
            "00": "GRADE_00",
            "-3": "GRADE_MINUS_3",
            "Bestået": "GRADE_PASSED",
            "Ikke bestået": "GRADE_FAILED",
            "Ej mødt": "GRADE_ABSENT",
            "Syg": "ILL",
            "Godkendt": "APPROVED",
            "Ikke Godkendt": "REJECTED"
        }
