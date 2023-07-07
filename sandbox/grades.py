class Grades:
    """ A class for handling DTU grades """

    def __init__(self: 'Grades'):
        """ temp """
        self._grade_dct: dict[str:int] = {}

    @classmethod
    def in_spring(cls: 'Grades') -> 'Grades':
        """ temp """
        return cls()

    def my_method(self: 'Grades'):
        """ temp """

    def add_new_grade(self: 'Grades', grade_name: str, amount: int) -> None:
        """ temp """
        if grade_name not in self._grade_dct:
            self._grade_dct[grade_name] = amount
        else:
            raise ValueError(f"CustomError: {grade_name} already exists in dict: {self._grade_dct}")


if __name__ == "__main__":
    # Test code, remove later
    pass