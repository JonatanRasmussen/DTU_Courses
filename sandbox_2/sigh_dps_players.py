from typing import Dict, List
from abc import ABC, abstractmethod


class School:
    def __init__(self) -> None:
        self.name: str = ""
        self.teachers: Dict[str, 'Teacher'] = {}
        self.years: Dict[str, 'Year'] = {}

    def get_name(self) -> str:
        return self.name
    def set_name(self, name: str) -> None:
        self.name = name

    def get_teachers(self) -> Dict[str, 'Teacher']:
        return self.teachers
    def set_teacher(self, name: str, teacher: 'Teacher') -> None:
        self.teachers[name] = teacher

    def get_all_years(self) -> Dict[str, 'Year']:
        return self.years
    def get_year(self, name: str) -> 'Year':
        return self.years[name]
    def set_year(self, name: str, year: 'Year') -> None:
        self.years[name] = year

    def get_all_courses(self,) -> Dict[str, 'Year']:
        return self.years
    def get_year(self, name: str) -> 'Year':
        return self.years[name]
    def set_year(self, name: str, year: 'Year') -> None:
        self.years[name] = year


class SchoolBuilder(ABC):
    def __init__(self):
        self.school: School = School()
        self.most_recent_built_year: Year = None
        self.most_recent_built_course: Course = None
        self.most_recent_built_term: CourseTerm = None
        self.build()

    def build(self) -> None:
        self.build_years()
        self.build_teachers()

    @abstractmethod
    def generate_year_names() -> List[str]:
        pass

    def build_years(self) -> None:
        for name in self.generate_year_names():
            self.school.set_year(Year(name))
            self.most_recent_built_year = self.school.get_year(name)
            self.build_courses()
            self.build_study_lines()

    @abstractmethod
    def fetch_course_names(year_name: str) -> List[str]:
        pass

    def build_courses(self) -> None:
        year: Year = self.most_recent_built_year
        for name in self.fetch_course_names(year):
            year.set_course(name, Course(name))
            self.most_recent_built_course = year.get_course(name)
            self.build_terms()
            self.build_info_page()

    @abstractmethod
    def fetch_term_names() -> List[str]:
        pass

    def build_terms(self) -> None:
        course: Course = self.most_recent_built_course
        for name in self.course_term_names(course):
            course.set_term(name, CourseTerm(name))
            self.most_recent_built_term = course.get_term(name)
            self.build_evaluation()
            self.build_grade_sheet()

    @abstractmethod
    def fetch_teachers():
        pass

    def build_teachers(self):
        for teacher in self.fetch_teachers():
            self.school.set_teacher(teacher.get_name(), teacher)

    @abstractmethod
    def fetch_study_lines(year):
        pass

    def build_study_lines(self):
        year: Year = self.most_recent_built_year
        for study_line in self.fetch_study_lines():
            year.set_study_line(study_line.get_name(), study_line)

    @abstractmethod
    def fetch_info_page(year, course):
        pass

    def build_info_page(self):
        year: Course = self.most_recent_built_year
        course: Course = self.most_recent_built_course
        info_page: InfoPage = self.fetch_info_page(year, course)
        course.set_info_page(info_page)
        pass

    @abstractmethod
    def fetch_evaluation(year, course, term):
        pass

    def build_evaluation(self):
        year: Course = self.most_recent_built_year
        course: Course = self.most_recent_built_course
        term: CourseTerm = self.most_recent_built_term
        evaluation: Evaluation = self.fetch_evaluation(year, course, term)
        term.set_evaluation(evaluation)
        pass

    @abstractmethod
    def fetch_grade_sheet(year, course, term):
        pass

    def build_grade_sheet(self):
        year: Course = self.most_recent_built_year
        course: Course = self.most_recent_built_course
        term: CourseTerm = self.most_recent_built_term
        grade_sheet: GradeSheet = self.fetch_grade_sheet(year, course, term)
        term.set_grade_sheet(grade_sheet)
        pass



class Dtu(SchoolBuilder):
    def __init__(self, oldest_year: int, newest_year: int) -> None:
        self.oldest_year: int = oldest_year
        self.newest_year: int = newest_year

    @classmethod
    def predefined_year_interval(cls) -> None:
        oldest_year: int = 2017
        newest_year: int = 2023
        return cls(oldest_year, newest_year)

    def generate_year_names(self) -> List[str]:
        year_names: List[str] = []
        for year in range(self.oldest_year, self.newest_year):
            year_names.append(f"{str(year)}'-'{str(1+year)}")
        return year_names



class Year:
    def __init__(self) -> None:
        self.name: str = ""
        self.studylines: Dict[str, 'Studyline'] = {}
        self.courses: Dict[str, 'Course'] = {}

    def get_name(self) -> str:
        return self.name
    def set_name(self, name: str) -> None:
        self.name = name

    def get_all_studylines(self) -> Dict[str, 'Studyline']:
        return self.studylines
    def get_studyline(self, name: str) -> 'Studyline':
        return self.studylines[name]
    def set_studyline(self, name: str, studyline: 'Studyline') -> None:
        self.studylines[name] = studyline

    def get_all_courses(self) -> Dict[str, 'Course']:
        return self.courses
    def get_course(self, name: str) -> 'Course':
        return self.courses[name]
    def set_course(self, name: str, course: 'Course') -> None:
        self.courses[name] = course


class Course:
    def __init__(self) -> None:
        self.name: str = ""
        self.info_page: Dict[str, 'InfoPage'] = {}
        self.course_terms: Dict[str, 'CourseTerm'] = {}

    def get_name(self) -> str:
        return self.name
    def set_name(self, name: str) -> None:
        self.name = name

    def get_all_terms(self) -> Dict[str, 'CourseTerm']:
        return self.course_terms
    def get_term(self, name: str) -> 'CourseTerm':
        return self.course_terms[name]
    def set_term(self, name: str, course_term: 'CourseTerm') -> None:
        self.course_terms[name] = course_term

    def get_info_page(self) -> 'InfoPage':
        return self.info_page
    def set_info_page(self, info_page: 'InfoPage') -> None:
        self.info_page = info_page


class CourseTerm:
    def __init__(self) -> None:
        self.name: str = ""
        self.evaluation:'Evaluation' = None
        self.grade_sheet: 'GradeSheet' = None

    def get_name(self) -> str:
        return self.name
    def set_name(self, name: str) -> None:
        self.name = name

    def get_grade_sheet(self) -> 'GradeSheet':
        return self.grade_sheet
    def set_grade_sheet(self, grade_sheet: 'GradeSheet') -> None:
        self.grade_sheet = grade_sheet

    def get_evaluation(self) -> 'Evaluation':
        return self.evaluation
    def set_evaluation(self, evaluation: 'Evaluation') -> None:
        self.evaluation = evaluation


class Teacher:
    pass

class Studyline:
    pass

class Evaluation:
    pass

class GradeSheet:
    pass

class InfoPage:
    pass