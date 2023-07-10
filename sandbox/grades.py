class GradeSheet:
    """ Grade distribution across DTU's different types of grades """

    def __init__(self: 'GradeSheet', course: str, term: str) -> 'GradeSheet':
        """ Instantiate each grade used at DTU """
        self._course: str = course
        self._term: str = term
        self._grades: list['Grade'] = GradeSheet.instantiate_dtu_grades()
        # Numeric grades (seven-step scale)
        self._grade_12: 'Grade' = Grade.create_passed('12', 12)
        self._grade_10: 'Grade' = Grade.create_passed('10', 10)
        self._grade_7: 'Grade' = Grade.create_passed('7', 7)
        self._grade_4: 'Grade' = Grade.create_passed('4', 4)
        self._grade_02: 'Grade' = Grade.create_passed('02', 2)
        self._grade_00: 'Grade' = Grade.create_failed('00', 0)
        self._grade_minus_3: 'Grade' = Grade.create_failed('minus_3', -3)
        # Non-numeric grades (Custom grades used at DTU)
        self._grade_pass: 'Grade' = Grade.create_passed('pass', None)
        self._grade_fail: 'Grade' = Grade.create_failed('fail', None)
        self._grade_absent: 'Grade' = Grade.create_not_attended('absent')
        self._grade_ill: 'Grade' = Grade.create_not_attended('ill')
        self._grade_unqualified: 'Grade' = Grade.create_not_attended('unqualified')

        self.grade_types: dict[str:str] = {}

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
        dtu_grades.append(Grade.create_failed('00', 0))
        dtu_grades.append(Grade.create_failed('minus_3', -3))
        # Non-numeric grades (Custom grades used at DTU)
        dtu_grades.append(Grade.create_passed('pass', None))
        dtu_grades.append(Grade.create_failed('fail', None))
        dtu_grades.append(Grade.create_not_attended('absent'))
        dtu_grades.append(Grade.create_not_attended('ill'))
        dtu_grades.append(Grade.create_not_attended('not_approved'))
        return dtu_grades


    def calculate_average(self: 'GradeSheet')-> float | None:
        """ Sum each grade on the seven-step scale and calculate the average """
        weighted_sum: int = 0
        weighted_sum += self.get_12(), (12 * self.get_12())
        weighted_sum += self.get_10(), (10 * self.get_10())
        weighted_sum += self.get_7(), (7 * self.get_7())
        weighted_sum += self.get_4(), (4 * self.get_4())
        weighted_sum += self.get_02(), (2 * self.get_02())
        weighted_sum += self.get_00(), (0 * self.get_00())
        weighted_sum += self.get_minus_3(), (-3 * self.get_minus_3())
        total_grades: int = self.count_numeric()
        if len(total_grades) == 0:
            return None  # Return None for an empty list (or you can choose to raise an exception)
        else:
            average: float = weighted_sum / len(total_grades)
            return average
        

    def get_12(self: 'GradeSheet') -> int:
        return self._grade_12

    def get_10(self: 'GradeSheet') -> int:
        return self._grade_10

    def get_7(self: 'GradeSheet') -> int:
        return self._grade_7

    def get_4(self: 'GradeSheet') -> int:
        return self._grade_4

    def get_02(self: 'GradeSheet') -> int:
        return self._grade_02

    def get_00(self: 'GradeSheet') -> int:
        return self._grade_00

    def get_minus_3(self: 'GradeSheet') -> int:
        return self._grade_minus_3

    def get_pass(self: 'GradeSheet') -> int:
        return self._grade_pass

    def get_fail(self: 'GradeSheet') -> int:
        return self._grade_fail

    def get_not_met(self: 'GradeSheet') -> int:
        return self._grade_absent

    def get_ill(self: 'GradeSheet') -> int:
        return self._grade_ill

    def get_unqualified(self: 'GradeSheet') -> int:
        return self._grade_unqualified

    def count_passed(self: 'GradeSheet') -> int:
        count: int = 0
        count += self.get_12()
        count += self.get_10()
        count += self.get_7()
        count += self.get_4()
        count += self.get_02()
        count += self.get_pass()

    def count_failed(self: 'GradeSheet') -> int:
        count: int = 0
        count += self.get_00()
        count += self.get_minus_3()
        count += self.get_fail()

    def count_absent(self: 'GradeSheet') -> int:
        count: int = 0
        count += self.get_not_met()
        count += self.get_unqualified()
        count += self.get_ill()
        return count

    def count_numeric(self: 'GradeSheet') -> int:
        count: int = 0
        count += self.get_12()
        count += self.get_10()
        count += self.get_7()
        count += self.get_4()
        count += self.get_02()
        count += self.get_00()
        count += self.get_minus_3()
        return count
        
    def count_binary(self: 'GradeSheet') -> int:
        count: int = 0
        count += self.get_pass()
        count += self.get_fail()
        return count

    def format_scraped_dict(self, scraped_dict, course_number, course_semester):
        """ Extract grades from the dict scraped from URL by pandas """


    def find_grade_average(self):
        """ Calculate and return average value of grades in the grade_counts dictionary """


    def exam_percentage_passed(self):
        """ Return percentage of students that passed, failed, or were absent in the exam """


    def create_statistics_dict(self, semester):
        """ Perform calculations and return the results as a dictionary """


    def number_of_semesters(self):
        """ Get the number of semesters based on grades assigned at each exam period """


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

class Grade:
    """ Grade datatype. Contains the following info:
        - Str: The name of the grade
        - Int: The 'quantity' (counts how many times the grade has been awarded)
        - Int: The numerical weight of the grade (can also be None) 
        - Bool: The 'attended' value ('True' if it counts as exam attendance)
        - Bool: The 'passed' value ('True' if it counts as passing the exam) """
    
    def __init__(self, name: str, weight: int | None, attended: bool, passed: bool) -> 'Grade':
        """ NOTE: Use one of the classmethods to instantiate """
        self._grade_name: bool = name
        self._quantity: int = 0
        self._numeric_weight: int | None = weight
        self._attended: bool = attended
        self._passed: bool = passed
        if self._numeric_weight is not None:
            self._numeric: bool = True
        else:
            self._numeric = False

    @classmethod
    def create_passed(cls: 'Grade', name: str, weight: int) -> 'Grade':
        """ Instantiate a grade for when the exam was attended and passed """
        attended = True
        passed = True
        return Grade(name, weight, attended, passed)

    @classmethod
    def create_failed(cls: 'Grade', name: str, weight: int) -> 'Grade':
        """ Instantiate a grade for when the exam was attended but failed """
        attended = True
        passed = False
        return Grade(name, weight, attended, passed)

    @classmethod
    def create_not_attended(cls: 'Grade', name: str) -> 'Grade':
        """ Instantiate a grade for when the exam was not attended (and thereby failed) """
        weight = None
        attended = False
        passed = False
        return Grade(name, weight, attended, passed)

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
        dtu_grades.append(Grade.create_failed('00', 0))
        dtu_grades.append(Grade.create_failed('minus_3', -3))
        # Non-numeric grades (Custom grades used at DTU)
        dtu_grades.append(Grade.create_passed('pass', None))
        dtu_grades.append(Grade.create_failed('fail', None))
        dtu_grades.append(Grade.create_not_attended('absent'))
        dtu_grades.append(Grade.create_not_attended('ill'))
        dtu_grades.append(Grade.create_not_attended('not_approved'))
        return dtu_grades

    def set_quantity(self: 'Grade', quantity: int) -> None:
        """ Set the amount of times the grade has been awarded """
        self._quantity = quantity

    def passes_exam(self: 'Grade') -> bool:
        """ Returns 'True' if the grade passes the exam
            Returns 'False' if the grade does not pass the exam """
        return self._passed
    
    def attended_exam(self: 'Grade') -> bool:
        """ Returns 'True' if the grade counts as attending the exam
            Returns 'False' if the grade counts as absence from the exam """
        return self._attended

    def is_numeric(self: 'Grade') -> bool:
        """ Returns 'True' if the grade has a numeric representation
            Returns 'False' if the grade isn't a number """
        return self._numeric

    def get_name(self: 'Grade') -> bool:
        """ Return the name of the grade """
        return self._grade_name

    def get_weight(self: 'Grade') -> int | None:
        """ If the grade is numeric, return its numeric weight
            If the grade is not numeric, return 'None' """
        if self.is_numeric():
            return self._numeric_weight
        else:
            return None