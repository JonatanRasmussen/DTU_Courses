from typing import Dict, List
from abc import ABC, abstractmethod
#from web_scraping_tool import WebScrapingTool

#https://refactoring.guru/design-patterns/bridge

class Persistence:

    def data_exists():
        pass
    def cached_data_exists():
        pass

    def read_data():
        pass
    def write_data():
        pass

    def read_cache():
        pass
    def write_cache():
        pass

class DataRetrieval(ABC):
    def __init__(self) -> None:
        self.custom_object: any = None
        self.unparsed_data: any = None
        self.parsed_data: any = None

    @abstractmethod
    @staticmethod
    def scrape_data() -> any:
        pass

    @abstractmethod
    @staticmethod
    def parse_data() -> any:
        pass

    def set_unparsed_data(self, unparsed_data: any) -> None:
        self.unparsed_data = unparsed_data

    def scrape_and_store_data(self, custom_object: any) -> any:
        self.unparsed_data = self.scrape_data(custom_object)
        Persistence.write_cache(custom_object, self.unparsed_data)

    def parse_and_store_data(self, custom_object: any) -> any:
        self.parsed_data = self.parse_data(self.unparsed_data)
        Persistence.write_data(custom_object, self.parsed_data)

    def get_parsed_data(self) -> any:
        return self.parsed_data

    def get_retrieval_strategy_name(self) -> str:
        return self.__class__.__name__

class DtuCourses(DataRetrieval):

    @staticmethod
    def scrape_data() -> any:
        pass

    @staticmethod
    def parse_data() -> any:
        pass

class DtuEvaluation(DataRetrieval):

    @staticmethod
    def scrape_data() -> any:
        pass

    @staticmethod
    def parse_data() -> any:
        pass

class DtuGradeSheet(DataRetrieval):

    @staticmethod
    def scrape_data() -> any:
        pass

    @staticmethod
    def parse_data() -> any:
        pass

class DtuInfoPage(DataRetrieval):

    @staticmethod
    def scrape_data() -> any:
        pass

    @staticmethod
    def parse_data() -> any:
        pass

class DtuStudyLine(DataRetrieval):

    @staticmethod
    def scrape_data() -> any:
        pass

    @staticmethod
    def parse_data() -> any:
        pass

class DtuTeacher(DataRetrieval):

    @staticmethod
    def scrape_data() -> any:
        pass

    @staticmethod
    def parse_data() -> any:
        pass

class DataDomain(ABC):

    @abstractmethod
    @staticmethod
    def get_data_retrieval_strategy(self, custom_object: any) -> None:
        pass

    @staticmethod
    def get_domain_name(cls) -> str:
        return cls.__name__

class DtuData(DataDomain):

    @staticmethod
    def get_data_retrieval_strategy(custom_object: any) -> DataRetrieval:
        if isinstance(custom_object, 'Course'):
            return DtuCourses
        elif isinstance(custom_object, 'Evaluation'):
            return DtuEvaluation
        elif isinstance(custom_object, 'GradeSheet'):
            return DtuGradeSheet
        elif isinstance(custom_object, 'InfoPage'):
            return DtuInfoPage
        elif isinstance(custom_object, 'StudyLine'):
            return DtuStudyLine
        elif isinstance(custom_object, 'Teacher'):
            return DtuTeacher
        else:
            raise ValueError("Custom_object is of an unsupported type")

class DataAccess:
    def __init__(self, custom_object) -> None:
        self.custom_object: any = custom_object
        self.retrieval_strategy: DataRetrieval = self._get_retrieval_strategy()

    def access_data(self):
        if Persistence.data_exists(self.custom_object):
            return Persistence.read_data(self.custom_object)
        elif Persistence.cached_data_exists(self.custom_object):
            self.retrieval_strategy.set_unparsed_data(Persistence.read_cache(self.custom_object))
        else:
            self.retrieval_strategy.scrape_and_store_data(self.custom_object)
        self.retrieval_strategy.parse_and_store_data(self.custom_object)
        return self.retrieval_strategy.get_parsed_data()

    def _get_retrieval_strategy(self) -> DataRetrieval:
        data_domain: DataDomain = self.custom_object.get_data_domain()
        return data_domain.get_data_retrieval_strategy(self.custom_object)

class BaseDataType(ABC):
    def __init__(self) -> None:
        self.name: str = ""
        self.parent: any = None
        self.data_domain: DataDomain = None

    def get_name(self) -> str:
        return self.name
    def set_name(self, name: str) -> None:
        self.name = name

    def get_parent(self) -> any:
        return self.parent
    def set_parent(self, parent: any) -> None:
        self.parent = parent

    def get_data_domain(self) -> DataDomain:
        return self.data_domain
    def set_data_domain(self, data_domain: DataDomain) -> None:
        self.data_domain = data_domain

class School(BaseDataType):
    def __init__(self) -> None:
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

    def get_all_courses(self,) -> Dict[str, 'Course']:
        return self.years
    def get_course(self, name: str) -> 'Course':
        return self.years[name]
    def set_course(self, name: str, course: 'Course') -> None:
        self.years[name] = course


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



class Year(BaseDataType):
    def __init__(self) -> None:
        self.name: str = ""
        self.studylines: Dict[str, 'StudyLine'] = {}
        self.courses: Dict[str, 'Course'] = {}

    def get_school(self) -> School:
        return self.name

    def get_name(self) -> str:
        return self.name
    def set_name(self, name: str) -> None:
        self.name = name

    def get_all_studylines(self) -> Dict[str, 'StudyLine']:
        return self.studylines
    def get_studyline(self, name: str) -> 'StudyLine':
        return self.studylines[name]
    def set_studyline(self, name: str, studyline: 'StudyLine') -> None:
        self.studylines[name] = studyline

    def get_all_courses(self) -> Dict[str, 'Course']:
        return self.courses
    def get_course(self, name: str) -> 'Course':
        return self.courses[name]
    def set_course(self, name: str, course: 'Course') -> None:
        self.courses[name] = course


class Course(BaseDataType):
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


class CourseTerm(BaseDataType):
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


class Teacher(BaseDataType):
    pass

class StudyLine(BaseDataType):
    pass

class Evaluation(BaseDataType):
    pass

class GradeSheet(BaseDataType):
    pass

class InfoPage(BaseDataType):
    pass