
class Grade:
    """ Grade datatype. Contains the following info:
        - Str: The name of the grade
        - Int: The 'quantity' (Number of students that have received the grade)
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
    def create_absent(cls: 'Grade', name: str) -> 'Grade':
        """ Instantiate a grade for when the exam was not attended (and thereby failed) """
        weight = None
        attended = False
        passed = False
        return Grade(name, weight, attended, passed)

    @classmethod
    def create_attended_but_failed(cls: 'Grade', name: str, weight: int) -> 'Grade':
        """ Instantiate a grade for when the exam was attended but failed """
        attended = True
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
        dtu_grades.append(Grade.create_attended_but_failed('00', 0))
        dtu_grades.append(Grade.create_attended_but_failed('minus_3', -3))
        # Non-numeric grades (Custom grades used at DTU)
        dtu_grades.append(Grade.create_passed('pass', None))
        dtu_grades.append(Grade.create_attended_but_failed('fail', None))
        dtu_grades.append(Grade.create_absent('absent'))
        dtu_grades.append(Grade.create_absent('ill'))
        dtu_grades.append(Grade.create_absent('not_approved'))
        return dtu_grades

    def set_quantity(self: 'Grade', quantity: int) -> None:
        """ Set the amount of students that have received the grade """
        self._quantity = quantity

    def get_quantity(self: 'Grade') -> int:
        """ Get the amount of students that have received the grade """
        return self._quantity

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